# Solution C

Start by preserving the logs at risk from the purge job, then run the restore in a non-production workspace. Legal should approve the hold scope, while support and customer success should wait for the test outcome before giving a firm ETA.

The backup owner should document the snapshot identifier, restore command, and checksum. The application owner should compare the snapshot structure with the current schema and prepare a migration patch if the restored records are compatible. If the patch is uncertain, keep the restored copy isolated and use it only to reconstruct a customer-safe workaround.

The operational branch is:

1. Freeze deletion.
2. Restore in isolation.
3. Verify schema compatibility.
4. Copy back only if legal and application owners approve.
5. Record unresolved gaps.

Do not assign cause or intent from this evidence. The plan should stay focused on preserving held data and producing a recoverable customer path.
