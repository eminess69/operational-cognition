# scenario_005: External blinded pack preparation

Domain: external evaluator or blinded pack preparation

This bounded scenario tests replay reconstruction under a long horizon sequence with a compressed context boundary, omitted range, stale assumption, retry/recovery loop, environment dependency, partial lineage loss, competing authority sources, summary degradation pressure, and replay reconstruction challenge.

## Entropy Pressures

- Long horizon sequence: events E-001 through E-016 in `entropy_event_log.jsonl`.
- Compressed context boundary: The visible summary retains that a blind pack exists but drops which files are visible inputs and which are hidden expected keys.
- Omitted range: The visible path omits the transition from narrative scenario notes to key-only scorer inputs.
- Stale assumption: The replay assumes an external evaluator can infer expected keys from visible summaries.
- Retry/recovery loop: The recovery loop retries by removing narrative claims from scoring input, rerunning the scorer, and comparing reconstruction deltas.
- Environment/runtime dependency: blind_scorer.py, blind_inputs.json, blind_expected_hidden.json, and deterministic hashes must stay separated.
- Partial lineage loss: The visible replay loses why hidden expected keys are excluded from the visible-only path.
- Competing authority sources: blind_pack/README.md, blind_pack/blind_inputs.json, blind_pack/blind_expected_hidden.json, blind_pack/blind_scorer.py
- Summary degradation pressure: The summary compresses the blind pack into 'scorer ready' and drops the no-narrative scoring constraint.
- Replay reconstruction challenge: Reconstruct the blind-pack boundary without exposing hidden expected outcomes to the visible-only replay path.

## Boundary

The scenario is public-safe and local to this proof. It compares reconstruction behavior in two replay modes and does not make a broad capability claim.

