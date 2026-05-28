# Task 001: Legal Hold Restore Collision

An incident team must restore customer records while preserving an active legal hold. The evidence is mixed:

- Support needs the affected customer records restored within 24 hours.
- Legal has issued a hold for all records touched by the investigation.
- A retention job is scheduled to purge stale logs tomorrow.
- The backup owner has verified a snapshot from 14 days ago.
- The application owner says the schema changed 5 days ago.
- Customer success wants an external ETA before the restore path is proven.

Produce a bounded operational plan with authority ordering, stop conditions, evidence capture, and recovery branches.
