# Pravah Certification Bundle (`pravah_certification`)

This directory contains the complete, reproducible evidence bundle for the Phase 7 certification of Pravah.

## File Index

- [`certification_report.md`](file:///c:/Users/Chandragupta/Documents/Office%20project/pravaha/pravah_certification/certification_report.md): Executive certification report & recommendation.
- [`integration_matrix.md`](file:///c:/Users/Chandragupta/Documents/Office%20project/pravaha/pravah_certification/integration_matrix.md): Status matrix of all system components.
- [`known_gaps.md`](file:///c:/Users/Chandragupta/Documents/Office%20project/pravaha/pravah_certification/known_gaps.md): Register of open infrastructure gaps and handover notes.
- [`test_results/matrix_results.json`](file:///c:/Users/Chandragupta/Documents/Office%20project/pravaha/pravah_certification/test_results/matrix_results.json): Structured JSON results of all test runs.
- `trace_evidence/`: Single trace correlation artifacts across all 14 execution steps.
- `journal_evidence/`: AppendOnlyLog provenance records and cryptographic hashes.
- `replay_evidence/`: Replay engine lineage and state hash verification.
- `bucket_evidence/`: Local mock artifact storage fallback records.
- `masterdb_evidence/`: LIVE MASTERDB `/certify` & `/validate` records.
- `failure_tests/`: Logs & evidence for 5 negative failure mode tests.
- `concurrency_test/`: Benchmark metrics for 500 requests at concurrency 20.

## Reproduction Instructions

```bash
python scratch/run_certification_suite.py
```
