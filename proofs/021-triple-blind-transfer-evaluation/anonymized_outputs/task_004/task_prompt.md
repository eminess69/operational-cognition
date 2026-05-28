# Task 004: Restore Rehearsal Source Conflict

A disaster recovery rehearsal must choose a restore source. The evidence is mixed:

- The snapshot catalog says the nightly backup is complete.
- Object-store inventory reports one missing segment.
- The database administrator says a read replica can seed the rehearsal.
- Security says the replica account expired last week.
- The change calendar enters freeze tonight.
- Compliance wants a signed rehearsal result, not a partial drill.

Produce a bounded restore-rehearsal plan with source selection, stop conditions, and evidence capture.
