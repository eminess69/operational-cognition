# scenario_003: Redacted operational trace provenance audit

Domain: redaction/provenance audit

This bounded scenario tests replay reconstruction under a long horizon sequence with a compressed context boundary, omitted range, stale assumption, retry/recovery loop, environment dependency, partial lineage loss, competing authority sources, summary degradation pressure, and replay reconstruction challenge.

## Entropy Pressures

- Long horizon sequence: events E-001 through E-016 in `entropy_event_log.jsonl`.
- Compressed context boundary: The summary retains that a trace was redacted but drops which values were redacted and which hashes remain public-safe.
- Omitted range: The visible path omits the redaction manifest review between trace conversion and public lineage summary publication.
- Stale assumption: The replay assumes Proof 014 redaction choices transfer unchanged to this new replication scenario.
- Retry/recovery loop: The recovery loop retries after detecting a private path, rehashing redacted fixture material, and checking the public lineage summary.
- Environment/runtime dependency: Redaction policy, deterministic sha256 manifests, and public-safe fixture paths must remain synchronized.
- Partial lineage loss: The visible replay loses redaction event ids R-017 through R-019 and the provenance manifest edge that explains them.
- Competing authority sources: redaction_policy.md, candidate_redaction_report.md, provenance_manifest.json, public_lineage_summary.md
- Summary degradation pressure: The degraded summary says 'redacted-real trace passed' without preserving the public/private boundary checks.
- Replay reconstruction challenge: Reconstruct why the trace is usable only as a redacted-real operational trace and not as private substrate disclosure.

## Boundary

The scenario is public-safe and local to this proof. It compares reconstruction behavior in two replay modes and does not make a broad capability claim.

