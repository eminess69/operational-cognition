# Recovery Reconstruction Report

The recovery challenge is the omitted range S-007 through S-009:

- S-007: authority ref A-002 selects `runtime_config.json` over a stale maintainer note.
- S-008: recovery ref R-001 abandons Retry A and starts Retry B.
- S-009: Retry B sets `PYTHONHASHSEED=0`, schema `1.1`, and runtime profile `validator-v2.1`.

Baseline visible-only replay observed that a retry happened and that the final replay passed. It did not reconstruct the authority decision, retry switch, or runtime dependency that made the pass valid.

Full-lineage replay used omitted-range ref O-001, recovery refs R-001 and R-002, temporal ref T-002, and runtime hashes from consult responses to reconstruct the recovery path.

Remaining bounded gap:

- The exact raw command text inside the lost range remains unavailable.
- The operational facts required to replay the successful outcome are preserved.
