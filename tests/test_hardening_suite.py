"""
Unit Test Suite for PRAVAH Phase 2 Production Hardening
Standard Library Unittest Framework
Assignee: Chandragupta Maurya
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pravah_hardening import (
    SecurityGuard,
    MetadataExtractor,
    ErrorBoundary,
    CircuitBreaker,
    ProductionMonitor,
    ContractValidator
)


class TestSecurityGuard(unittest.TestCase):
    def setUp(self):
        self.guard = SecurityGuard()

    def test_validate_token_valid(self):
        is_valid, msg = self.guard.validate_token("Bearer pravah-prod-token-2026")
        self.assertTrue(is_valid)
        self.assertEqual(msg, "Authenticated")

    def test_validate_token_invalid(self):
        is_valid, msg = self.guard.validate_token("Bearer invalid-token")
        self.assertFalse(is_valid)
        self.assertIn("Invalid", msg)

    def test_sanitize_input_clean(self):
        is_valid, clean, msg = self.guard.sanitize_input("Normal text payload")
        self.assertTrue(is_valid)
        self.assertEqual(clean, "Normal text payload")

    def test_sanitize_input_script_injection(self):
        is_valid, clean, msg = self.guard.sanitize_input("<script>alert('hack')</script>")
        self.assertFalse(is_valid)
        self.assertIn("Script injection", msg)

    def test_sanitize_input_sql_injection(self):
        is_valid, clean, msg = self.guard.sanitize_input("SELECT * FROM users WHERE 1=1")
        self.assertFalse(is_valid)
        self.assertIn("SQL injection", msg)

    def test_sanitize_input_path_traversal(self):
        is_valid, clean, msg = self.guard.sanitize_input("../../etc/passwd")
        self.assertFalse(is_valid)
        self.assertIn("Path traversal", msg)

    def test_verify_request_headers(self):
        headers = {"X-Trace-ID": "trace-12345", "User-Agent": "PyTest"}
        is_valid, msg = self.guard.verify_request_headers(headers)
        self.assertTrue(is_valid)


class TestMetadataExtractor(unittest.TestCase):
    def test_calculate_sha256(self):
        content = b"hello pravah"
        digest = MetadataExtractor.calculate_sha256(content)
        self.assertEqual(len(digest), 64)
        self.assertEqual(digest, "a3bd8002d89fbad76c7ef34b44edefe4089f3e3bb62fb123bfdd0cd5e45a6f73")

    def test_extract_file_metadata(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            tf.write(b'{"test": "data"}')
            tf_path = tf.name
        
        try:
            meta = MetadataExtractor.extract_file_metadata(tf_path)
            self.assertEqual(meta["mime_type"], "application/json")
            self.assertEqual(meta["file_size_bytes"], 16)
            self.assertEqual(len(meta["sha256"]), 64)
        finally:
            if os.path.exists(tf_path):
                os.remove(tf_path)

    def test_extract_payload_metadata(self):
        payload = {"event": "CERTIFY", "status": "PASS"}
        meta = MetadataExtractor.extract_payload_metadata(payload, trace_id="trace-001")
        self.assertEqual(meta["trace_id"], "trace-001")
        self.assertEqual(meta["field_count"], 2)
        self.assertIn("payload_sha256", meta)

    def test_validate_schema(self):
        data = {"a": 1, "b": 2}
        is_valid, missing = MetadataExtractor.validate_schema(data, ["a", "b"])
        self.assertTrue(is_valid)
        self.assertEqual(missing, [])

        is_valid, missing = MetadataExtractor.validate_schema(data, ["a", "c"])
        self.assertFalse(is_valid)
        self.assertEqual(missing, ["c"])


class TestErrorBoundary(unittest.TestCase):
    def test_safe_execute_success(self):
        def dummy_func(a, b):
            return a + b
        
        success, val, err = ErrorBoundary.safe_execute(dummy_func, fallback_value=0, a=5, b=10)
        self.assertTrue(success)
        self.assertEqual(val, 15)
        self.assertIsNone(err)

    def test_safe_execute_failure(self):
        def failing_func():
            raise ValueError("Simulated runtime failure")
        
        success, val, err = ErrorBoundary.safe_execute(failing_func, fallback_value=-1)
        self.assertFalse(success)
        self.assertEqual(val, -1)
        self.assertIn("Simulated runtime failure", err)

    def test_circuit_breaker_threshold(self):
        cb = CircuitBreaker(name="test_cb", failure_threshold=2, recovery_time=10.0)
        def broken_func():
            raise Exception("Failure")

        # 1st fail
        with self.assertRaises(Exception):
            cb.execute(broken_func)
        self.assertEqual(cb.state, "CLOSED")

        # 2nd fail -> triggers OPEN
        with self.assertRaises(Exception):
            cb.execute(broken_func)
        self.assertEqual(cb.state, "OPEN")

        # 3rd attempt -> blocked by circuit breaker
        success, val, err = ErrorBoundary.safe_execute(broken_func, fallback_value="FALLBACK", circuit_breaker=cb)
        self.assertFalse(success)
        self.assertEqual(val, "FALLBACK")
        self.assertIn("Circuit Breaker Triggered", err)


class TestProductionMonitor(unittest.TestCase):
    def test_record_and_summary(self):
        mon = ProductionMonitor()
        mon.record_request(50.0, 200)
        mon.record_request(100.0, 200)
        mon.record_request(150.0, 500)
        
        summary = mon.get_summary()
        self.assertEqual(summary["total_requests"], 3)
        self.assertEqual(summary["failed_requests"], 1)
        self.assertEqual(summary["avg_latency_ms"], 100.0)
        self.assertEqual(summary["stability_score_pct"], 66.67)

    def test_export_prometheus_metrics(self):
        mon = ProductionMonitor()
        mon.record_request(80.0, 200)
        prom_text = mon.export_prometheus_metrics()
        self.assertIn("pravah_requests_total 1", prom_text)
        self.assertIn("pravah_stability_score_pct 100.0", prom_text)


if __name__ == "__main__":
    unittest.main()
