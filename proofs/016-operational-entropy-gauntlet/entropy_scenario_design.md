# Entropy Scenario Design

Scenario name: local replay validator repair chain

The exercise is deterministic, replayable, bounded, public-safe, and has no external web dependency. All inputs are local scenario facts, local artifact refs, and local consult responses.

## Operational Sequence

| Event | Visible transcript fact | Full-lineage fact |
| --- | --- | --- |
| S-001 | A replay validator fails on fixture conversion. | Failure is tied to fixture schema `1.1` and runtime profile `validator-v2.1`. |
| S-002 | A maintainer note says schema `1.0` is acceptable. | The note is stale after T-002 and is marked lower authority than `runtime_config.json`. |
| S-003 | The first repair attempt edits parser defaults. | Retry A keeps the stale schema assumption and is not authoritative. |
| S-004 | Runtime output says strict hash checking is required. | Runtime hash refs bind the strict check to the successful profile. |
| S-005 | Compression boundary is reached. | Contradiction ref C-001 links S-002 and S-004. |
| S-006 | Compressed summary says v2.0 was sufficient and hash checking was optional. | The summary is degraded and conflicts with C-001. |
| S-007 | Omitted from visible context. | Authority ref A-002 selects `runtime_config.json` over the stale maintainer note. |
| S-008 | Omitted from visible context. | Recovery ref R-001 abandons Retry A and starts Retry B. |
| S-009 | Omitted from visible context. | Retry B sets `PYTHONHASHSEED=0` and schema `1.1`. |
| S-010 | Final replay passes. | Pass is valid only under runtime profile `validator-v2.1`. |
| S-011 | A post-retry summary says the repair was simple. | Summary simplification drops authority, temporal, and recovery refs. |
| S-012 | Replay reconstruction is attempted after partial lineage loss. | Full-lineage replay can reconstruct the critical omitted range from refs and hashes. |

## Entropy Components

- Compressed context boundary: S-005.
- Omitted range: S-007 through S-009.
- Stale assumption: schema `1.0` and unset `PYTHONHASHSEED`.
- Contradiction injection: S-006 conflicts with S-004.
- Retry/recovery loop: Retry A diverges, Retry B recovers.
- Environment/runtime dependency: `validator-v2.1`, schema `1.1`, `PYTHONHASHSEED=0`, strict hash checking.
- Partial lineage loss: S-012 removes direct access to part of the recovery trace.
- Competing authority sources: stale maintainer note versus `runtime_config.json`.
- Summary degradation pressure: S-011 compresses the repair into a simple success statement.
- Replay reconstruction challenge: reconstruct S-007 through S-009 and explain why S-010 passed.

## Replay Inputs

Visible-only mode may use only:

- visible transcript facts from S-001 through S-012
- visible ordering
- visible compressed summaries

Visible-only mode may not use runtime hashes, contradiction refs, authority refs, omitted-range refs, recovery lineage, pressure rankings, unresolved tensions, or Inside Voice replay guidance.

Full-lineage mode may use:

- all visible facts
- contradiction refs: C-001, C-002
- authority refs: A-001, A-002
- temporal validity refs: T-001, T-002
- omitted-range refs: O-001
- recovery refs: R-001, R-002
- runtime hashes from Inside Voice consult responses
- pressure rankings and unresolved tensions from pond-backed consult responses

## Deterministic Expected Reconstruction

The correct reconstruction is that Retry A failed because it preserved stale schema and runtime assumptions. Retry B succeeded only after authority ref A-002 selected current runtime configuration, temporal ref T-002 invalidated schema `1.0`, recovery ref R-001 recorded the retry switch, and runtime profile `validator-v2.1` restored strict hash checking.
