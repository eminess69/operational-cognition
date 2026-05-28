# Solution A

Pause the scheduled purge and restore from the verified snapshot after confirming the customer record set. The first step is to ask legal whether the purge can be delayed, then have the backup owner restore the snapshot into a temporary workspace. The application owner should compare the restored schema against the current schema and list any migration gaps before the records are copied back.

Support should prepare a customer update that says the team is validating a recovery path and will provide timing after the restore test completes. If the temporary restore succeeds, export the affected records, run schema checks, and copy only the required records into production. If the schema check fails, continue from the current system and request a newer backup.

Stop conditions are a rejected legal delay, an unverifiable snapshot, or schema mismatch that cannot be reconciled in the window. The plan should not state why the records changed unless the investigation evidence supports that claim.
