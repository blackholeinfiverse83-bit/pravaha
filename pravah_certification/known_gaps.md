# Pravah Unresolved Gap Register & Handover Log

**Last Updated:** `2026-08-27T06:26:10.598470+00:00`

## Open Infrastructure & Integration Gaps

### 1. TANTRA Core Deployment (Render Free Tier Suspended)
- **Classification:** `MOCK / BLOCKED`
- **Impact:** Production HTTP endpoint `https://tantra-core.onrender.com` returns `HTTP 503 Service Unavailable`.
- **Mitigation:** Fallback logic cleanly handles outage without throwing unhandled exceptions. Handed over to infrastructure owner for paid instance un-freezing.

### 2. Bucket Durable Artifact Storage (Render Free Tier Suspended)
- **Classification:** `MOCK / BLOCKED`
- **Impact:** Endpoint `https://bhiv-bucket-i1l6.onrender.com` returns `HTTP 503 Service Unavailable`.
- **Mitigation:** Execution artifacts stored locally in `bucket_evidence/` with explicit mock fallback logging.

### 3. Decision Brain In-Memory Demo Mode
- **Classification:** `LIVE (Demo Frozen)`
- **Impact:** `/decision-summary` reports `demo_frozen: true, stateless: true`. In-memory decision history is cleared upon process container restart.
- **Mitigation:** Persistent event logging is maintained via AppendOnlyLog and MASTERDB records.

## Handover Checklist for Incoming Engineer
1. **To reproduce certification suite:** Run `python scratch/run_certification_suite.py` from repository root.
2. **To inspect live service endpoints:** Query `http://163.128.209.18:8010/health`, `https://sarathi-9n5g.onrender.com/health`, and `https://masterdb-ingestion-certification-service.onrender.com/health`.
3. **To un-block TANTRA & Bucket:** Upgrade Render service instances to standard plan.
