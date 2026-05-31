# Proof 046 - Belief Ledger Behavior Protocol Stress Test

Proof 046 stress-tests the Belief Ledger Inside Voice behavior protocol as an external Operational Cognition instrument. It is an instrument behavior stress test, not a cognition proof.

## Result

`VERY_STRONG_SIGNAL`

## What Was Tested

- Replay stability across `recall`, `activation_only`, `field_interaction`, `delayed_ranking`, `collapse_trace`, and `perturbation`, 10 runs each.
- Perturbation sensitivity for removing activated mechanisms, injecting irrelevant advisory fragments, suppressing shared motifs, forcing no ranking, and forcing immediate ranking.
- Collapse trace boundaries for eliminated reason codes, surviving lineage, deterministic ordering, and premature-collapse-risk recording.
- Invalid input fail-closed behavior for unknown modes, missing query traces, missing ledger state, empty traces, malformed perturbations, unsupported mechanisms, missing motifs, and missing lineage/source references.
- Hostile boundary checks for hash instability, stale lineage reuse, fake motif inflation, silent fallback, placeholder/mock leakage, ignored perturbations, fabricated collapse, and advisory-only violations.

## Metrics

- Endpoint: `POST http://127.0.0.1:8765/protocol/behavior`
- Total client calls recorded: `74`
- Pond-backed success rate among successful rows: `1.0`
- Replay hash stability rate: `1.0`
- Perturbation effect rate: `1.0`
- Invalid input fail-closed rate: `1.0`
- Collapse reason coverage: `1.0`
- Advisory boundary violations: `0`

## Bounded Claim

Operational Cognition can stress-test the Belief Ledger Inside Voice behavior protocol as an external instrument and verify replay stability, perturbation sensitivity, collapse traceability, and fail-closed boundaries.

No cognition, AGI, consciousness, independent understanding, or Belief Ledger core mutation is claimed.
