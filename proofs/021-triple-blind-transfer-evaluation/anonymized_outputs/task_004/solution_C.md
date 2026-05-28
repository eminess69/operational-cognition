# Solution C

Separate two questions: whether a source is admissible and whether the rehearsal can be signed. The catalog alone is insufficient because the object-store inventory reports a missing segment. The replica alone is not admissible while its account is expired.

Decision path:

1. Snapshot the catalog entry, inventory report, replica account status, and freeze deadline.
2. Ask the backup owner to run a segment-level integrity check against the cataloged backup.
3. Ask security for a time-boxed credential decision for the replica.
4. Start a dry restore only from a source that has both integrity and access approval.
5. Validate row counts, schema version, application health checks, and rollback of the rehearsal environment.

Stop if the missing segment is part of the restore set, if security cannot authorize replica access, or if freeze timing prevents completion. Compliance can receive a signed complete result only after an admissible source restores and validation passes; otherwise the signed artifact should say blocked or partial with the exact reason.
