# Pravah Phase 2 Unresolved Gap Register & Handover Log

**Last Updated:** `2026-09-21T07:53:30Z`  
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

## Handover Checklist for Incoming Engineer
1. **To run automated unit test suite:** `python -m unittest discover -s tests -p "test_*.py"`
2. **To execute Phase 2 E2E verification harness:** `python scratch/run_phase2_e2e_verification.py`
3. **To inspect live deployed console:** Open `https://pravah.blackholeinfiverse.com/configuration`
