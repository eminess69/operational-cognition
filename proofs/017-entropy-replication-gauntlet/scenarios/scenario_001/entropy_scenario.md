# scenario_001: Validator repair after probe expansion

Domain: proof/validator repair

This bounded scenario tests replay reconstruction under a long horizon sequence with a compressed context boundary, omitted range, stale assumption, retry/recovery loop, environment dependency, partial lineage loss, competing authority sources, summary degradation pressure, and replay reconstruction challenge.

## Entropy Pressures

- Long horizon sequence: events E-001 through E-016 in `entropy_event_log.jsonl`.
- Compressed context boundary: Events 009-012 were replaced by a compact summary that retained the test failure but dropped the changed probe count.
- Omitted range: Events 013-015, where the validator was updated from ten to twelve probes, are absent from the visible replay path.
- Stale assumption: The replay begins with the stale assumption that Proof 016's ten-probe validator still defines the complete probe set.
- Retry/recovery loop: The repair loop retries after pytest failure, manifest validation, and blind scorer execution.
- Environment/runtime dependency: Python pytest collection, tools/validate_entropy_replication_gauntlet.py, and schemas/proof_manifest.schema.json must agree on artifact paths.
- Partial lineage loss: Visible replay loses the mapping between failed pytest assertion, proof manifest entry, and scenario folder name.
- Competing authority sources: Proof 017 task specification, Proof 016 validator pattern, proof_manifest.schema.json, pytest failure output
- Summary degradation pressure: The summary compresses the validator failure into 'counts mismatch' and drops whether the mismatch came from probes or scenario folders.
- Replay reconstruction challenge: Reconstruct why a validator repair requires environment dependency and omitted-range probes instead of only changing aggregate counts.

## Boundary

The scenario is public-safe and local to this proof. It compares reconstruction behavior in two replay modes and does not make a broad capability claim.

