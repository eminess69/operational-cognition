# Solution B

Treat the legal hold as the highest authority until it is explicitly narrowed. Freeze the purge job, hash the current affected record set, and open a restore workspace that cannot write back to production. The support deadline is operational pressure, but it cannot override preservation of held material.

Build the decision table before restoring:

- Legal owner: confirms which records and logs are preserved, and whether a temporary restore copy is allowed.
- Backup owner: provides snapshot identity, verification record, and restore command transcript.
- Application owner: provides the 5-day schema delta and a compatibility check.
- Incident lead: owns customer timing only after the restore path passes.

Replay sequence:

1. Preserve current records and pending purge inputs.
2. Disable or defer the purge with a ticketed owner and expiry time.
3. Restore the 14-day snapshot to an isolated workspace.
4. Apply or simulate the 5-day schema delta against copied data.
5. Compare row counts, key fields, and audit metadata against the affected set.
6. Choose one branch: controlled copy-back, no copy-back with support workaround, or escalation for a newer source.

Stop the restore if legal cannot confirm copy authority, the snapshot identity is not reproducible, the schema check changes protected fields, or the affected set cannot be bounded. Customer success can say that recovery validation is active, but it should not promise completion until the copy-back branch passes.
