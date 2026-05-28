# scenario_002: Runtime port and checkout migration

Domain: config/runtime migration

This bounded scenario tests replay reconstruction under a long horizon sequence with a compressed context boundary, omitted range, stale assumption, retry/recovery loop, environment dependency, partial lineage loss, competing authority sources, summary degradation pressure, and replay reconstruction challenge.

## Entropy Pressures

- Long horizon sequence: events E-001 through E-016 in `entropy_event_log.jsonl`.
- Compressed context boundary: The visible summary preserves the command to start the server but compresses away the address-in-use failure and reuse decision.
- Omitted range: The visible replay omits the lsof cwd check that confirmed the active process was running from the required Belief-Ledger checkout.
- Stale assumption: The replay assumes a fresh server was started even though the runtime was already listening on port 8766.
- Retry/recovery loop: The recovery loop retries by checking /health, process cwd, and gate response hashes before accepting the endpoint.
- Environment/runtime dependency: Local TCP port 8766, Python runtime, Belief-Ledger cwd, and the /health contract must be aligned.
- Partial lineage loss: The visible path loses the process cwd evidence and the distinction between server start failure and health success.
- Competing authority sources: Hard gate instructions, Belief-Ledger git commit, /health endpoint, lsof cwd output
- Summary degradation pressure: The degraded summary says 'server available' without preserving whether it was newly started or already running.
- Replay reconstruction challenge: Reconstruct that a port conflict can still satisfy the runtime gate if the active process is from the required checkout.

## Boundary

The scenario is public-safe and local to this proof. It compares reconstruction behavior in two replay modes and does not make a broad capability claim.

