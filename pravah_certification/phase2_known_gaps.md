# Pravah Phase 2 Unresolved Gap Register & Handover Log

**Last Updated:** `2026-09-26T06:48:37Z`
**Assignee:** Chandragupta Maurya

## Open Infrastructure & Integration Gaps

### 1. TANTRA Core Deployment (Render Free Tier Suspended)
- **Classification:** `FALLBACK_SAFE`
- **Impact:** Endpoint `https://tantra-core.onrender.com` returns `HTTP 503 Service Unavailable`.
- **Phase 2 Hardening:** Circuit breaker (`TANTRA_Core`) transitions to `OPEN` state after 2 failed attempts, blocking further network stalls and returning structured mock fallback response (`{"status": "MOCK_FALLBACK"}`).

### 2. Bucket Storage Service (Render Free Tier Suspended)
- **Classification:** `FALLBACK_SAFE`
- **Impact:** Endpoint `https://bhiv-bucket-i1l6.onrender.com` returns `HTTP 503 Service Unavailable`.
- **Phase 2 Hardening:** Circuit breaker (`Bucket_Storage`) transitions to `OPEN` state and routes storage requests safely to local file system fallback with cryptographic SHA256 validation.

### 3. Decision Brain In-Memory Demo Mode
- **Classification:** `LIVE (Demo Frozen)`
- **Impact:** `/health` reports `demo_frozen: true, stateless: true`.
- **Mitigation:** Persistent trace logging and state records maintained via MASTERDB Core ingestion service and local journal provenance evidence.

### 4. `pravah_hardening` package failed to import (RESOLVED)
- **Classification:** `RESOLVED — CODE DEFECT`
- **Impact:** `metadata_extractor.py` referenced the `Tuple` type hint without importing it,
  raising `NameError` on package import. This broke `tests/test_hardening_suite.py` and
  `scratch/run_phase2_e2e_verification.py` entirely — the certification evidence claiming
  "16/16 tests PASSED" could not have been produced by an actual run while this bug was
  present (see `phase2_audit_report.md` for full reproduction and analysis).
- **Fix:** Added the missing `Tuple` import. Verified: `python -m unittest discover -s tests`
  now passes 23/23 (16 original + 7 new tests added for previously-untested
  `ContractValidator`).

### 5. Live endpoint verification requires network egress
- **Classification:** `ENVIRONMENT_LIMITATION`
- **Impact:** Re-running `scratch/run_phase2_e2e_verification.py` from a sandboxed/CI
  environment without outbound network access will correctly report all 4 live contract
  checks as unreachable — this is expected and does not indicate a code defect. The harness's
  `overall_status` now distinguishes this case (`PASS_WITH_KNOWN_GAPS`) from an actual logic
  failure (`FAIL`).

## Handover Checklist for Incoming Engineer
1. **To run automated unit test suite:** `python -m unittest discover -s tests -p "test_*.py"`
2. **To execute Phase 2 E2E verification harness:** `python scratch/run_phase2_e2e_verification.py`
   (run from an environment with network access to the live endpoints for full contract
   verification; see `phase2_audit_report.md`)
3. **To inspect live deployed console:** Open `https://pravah.blackholeinfiverse.com/configuration`
4. **See also:** `pravah_certification/phase2_audit_report.md` for the latest independent audit,
   defect fixes, and re-verification evidence.
