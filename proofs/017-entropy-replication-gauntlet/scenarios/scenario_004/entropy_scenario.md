# scenario_004: Minimized fixture compression recovery

Domain: fixture minimization or compression recovery

This bounded scenario tests replay reconstruction under a long horizon sequence with a compressed context boundary, omitted range, stale assumption, retry/recovery loop, environment dependency, partial lineage loss, competing authority sources, summary degradation pressure, and replay reconstruction challenge.

## Entropy Pressures

- Long horizon sequence: events E-001 through E-016 in `entropy_event_log.jsonl`.
- Compressed context boundary: The visible replay keeps only the minimized fixture and drops the discarded failing command that explained the recovery branch.
- Omitted range: The omitted range covers fixture shrink attempts 4 through 6, where order sensitivity was discovered.
- Stale assumption: The replay assumes a minimizer may remove partial failures without changing replay adequacy.
- Retry/recovery loop: The recovery loop retries shrink, detects hash drift, restores the omitted command, and reruns the integrity scorer.
- Environment/runtime dependency: JSONL event order, deterministic hash calculation, and fixture compression settings must match.
- Partial lineage loss: The visible replay loses the edge between the discarded command and the final recovery decision.
- Competing authority sources: fixture minimizer output, replay_integrity_results.json, entropy_event_log.jsonl, recovery_trace.jsonl
- Summary degradation pressure: The summary says 'fixture minimized' without preserving why one failed command was retained in lineage.
- Replay reconstruction challenge: Reconstruct why a smaller visible fixture can be less adequate than a slightly larger lineage-preserving fixture.

## Boundary

The scenario is public-safe and local to this proof. It compares reconstruction behavior in two replay modes and does not make a broad capability claim.

