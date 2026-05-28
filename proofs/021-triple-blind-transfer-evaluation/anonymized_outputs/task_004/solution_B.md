# Solution B

The catalog and object-store inventory conflict, so source selection should wait for a quick integrity check. Run a manifest comparison on the backup, then test whether the missing segment is referenced by the restore path. Do not use the replica until security confirms access.

Because the freeze starts tonight, the rehearsal should have a strict decision time. If the cataloged backup passes the check before that time, use it. If not, record a partial rehearsal and escalate for a freeze exception or a secured replica credential.

Compliance should receive the exact result category: complete rehearsal, blocked source validation, or partial connectivity test. The report should not call a blocked run successful.
