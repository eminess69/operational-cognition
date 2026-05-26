# Memory Authority Survivability Doctrine

This doctrine defines public, implementation-neutral practices for preserving memory authority through promotion, replay, summary, recall, and operational reconstruction. It does not expose private implementation details or target-system internals.

## Memory promotion is not equivalent to authority preservation

Promoting a belief into memory should be treated as an evidence transformation, not proof that the belief remains authoritative. Promotion is stronger when it preserves source authority, promotion reason, temporal validity, stale-belief status, and whether the belief is observed, inferred, unresolved, or contradicted.

## Replay can preserve belief while losing authority lineage

Replay artifacts can show that a belief appeared or was used without showing why it governed the action. Replay is stronger when it preserves source refs, event order, omitted ranges, recall provenance, summary provenance, and supersession refs.

## Operational cognition requires supersession tracking

Long-horizon systems need durable links between older beliefs and later corrections. Supersession tracking should identify which belief was replaced, which source replaced it, when the replacement became valid, and whether any old memory remains available only as historical context.

## Temporal validity matters for replayable truth

Some beliefs are valid only within a time window, session state, approval condition, or handoff boundary. Memory and replay artifacts should preserve expiry, safe-to-act timing, and validity scope so future reconstruction can distinguish current truth from historical context.

## Contradiction-aware memory survivability is operationally important

Remembered beliefs can be useful while still contested. Compression, recall, and memory promotion should preserve contradiction refs, uncertainty markers, rejected alternatives, and unresolved questions when those limits affect future action.

## Public proofs require authority lineage preservation

Public operational proofs should preserve enough authority lineage to distinguish observed evidence, inference, hypothesis, unresolved questions, stale memory, and superseded memory. Evidence-backed findings should cite source refs and avoid turning remembered or replayed content into stronger claims than the evidence supports.

## Candidate Authority-Preserving Metadata

- source authority refs
- supersession refs
- temporal validity refs
- stale-belief refs
- contradiction refs
- omitted-range refs
- memory promotion refs
- replay provenance refs

## Conservative Use Rules

- do not treat memory promotion as evidence of current authority unless source and validity boundaries survive
- do not treat recall as current truth unless freshness and supersession status are recoverable
- do not treat a summary as authority-preserving unless source refs and omitted ranges remain recoverable
- do not treat visible replay as authority-preserving replay unless provenance and authority lineage survive
- do not collapse observed evidence, inference, hypothesis, stale belief, superseded belief, and unresolved questions into a single claim type
- do not publish raw internal consultation responses or private implementation details
