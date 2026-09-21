"""
PRAVAH Production Monitoring & Telemetry Engine
Phase 2: Advanced Integration & Security Hardening
Assignee: Chandragupta Maurya
"""

import time
import math
from typing import Dict, Any, List


class ProductionMonitor:
    """Tracks system performance, request latency, throughput, error rates, and stability score."""
    
    def __init__(self):
        self.metrics: Dict[str, List[float]] = {
            "latencies_ms": [],
            "status_codes": [],
            "error_count": [0],
            "total_count": [0]
        }
        self.start_time = time.time()

    def record_request(self, latency_ms: float, status_code: int):
        """Record an API request telemetry metric."""
        self.metrics["latencies_ms"].append(latency_ms)
        self.metrics["status_codes"].append(status_code)
        self.metrics["total_count"][0] += 1
        if status_code >= 400:
            self.metrics["error_count"][0] += 1

    def get_summary(self) -> Dict[str, Any]:
        """Compute aggregated production telemetry summary."""
        total = self.metrics["total_count"][0]
        errors = self.metrics["error_count"][0]
        latencies = self.metrics["latencies_ms"]
        
        avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
        p95_latency = sorted(latencies)[int(len(latencies) * 0.95)] if latencies else 0.0
        
        success_rate = ((total - errors) / total * 100.0) if total > 0 else 100.0
        stability_score = max(0.0, round(success_rate, 2))
        
        elapsed = time.time() - self.start_time
        rps = round(total / elapsed, 2) if elapsed > 0 else 0.0

        return {
            "total_requests": total,
            "failed_requests": errors,
            "success_rate_pct": round(success_rate, 2),
            "stability_score_pct": stability_score,
            "avg_latency_ms": round(avg_latency, 2),
            "p95_latency_ms": round(p95_latency, 2),
            "throughput_rps": rps,
            "uptime_seconds": round(elapsed, 2)
        }

    def export_prometheus_metrics(self) -> str:
        """Export metrics formatted for Prometheus scraper."""
        summary = self.get_summary()
        lines = [
            "# HELP pravah_requests_total Total number of API requests processed.",
            "# TYPE pravah_requests_total counter",
            f"pravah_requests_total {summary['total_requests']}",
            "# HELP pravah_requests_failed Total number of failed requests.",
            "# TYPE pravah_requests_failed counter",
            f"pravah_requests_failed {summary['failed_requests']}",
            "# HELP pravah_latency_avg_ms Average request latency in milliseconds.",
            "# TYPE pravah_latency_avg_ms gauge",
            f"pravah_latency_avg_ms {summary['avg_latency_ms']}",
            "# HELP pravah_stability_score_pct System stability score percentage.",
            "# TYPE pravah_stability_score_pct gauge",
            f"pravah_stability_score_pct {summary['stability_score_pct']}"
        ]
        return "\n".join(lines) + "\n"
