# Negative & Failure Mode Test Results

**Timestamp:** `2026-08-27T06:26:04.052686+00:00`
**Environment:** `PROD-CERT`

| Test ID | Test Name | Expected Result | Actual Result | Status |
| --- | --- | --- | --- | --- |
| `NEG-TEST-001` | **Governance Block (PROD Action Scope Constraint)** | Governance block triggered (status: blocked / selected_action: noop) | Decision: noop, Execution Status: blocked | `PASS` |
| `NEG-TEST-002` | **Decision Brain Endpoint Failure / Unreachable** | HTTP 404 handled gracefully with default safe fallbacks | HTTP 404 returned cleanly without crashing system looper | `PASS` |
| `NEG-TEST-003` | **Redis Stream / Cache Outage Handling** | Runtime continues in-memory event buffering without execution corruption | In-memory event buffer activated, stateless fallback verified | `PASS` |
| `NEG-TEST-004` | **Bucket Storage Unavailable (HTTP 503)** | Bucket returns HTTP 503; system logs local artifact audit trail | HTTP 503 returned. Local evidence artifact created without blocking control plane. | `PASS` |
| `NEG-TEST-005` | **Invalid / Tampered Journal Event Verification** | Verification engine rejects tampered event with hash_chain_valid == false | Integrity check failed as expected: hash_chain_valid = False | `PASS` |
