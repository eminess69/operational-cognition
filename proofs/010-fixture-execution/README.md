# Proof 010: Survivable Lineage Fixture Execution v0.1

## Primary Question

Does full-lineage replay reconstruct fixture claims that visible-only replay leaves partial or unresolved?

## Status

Proof 010 is an `analysis` proof pack with claim level `evidence_backed` when validators pass.

This is fixture-level validation only. It does not claim universal proof, target-system defects, AGI, consciousness, black-box solution, substrate disclosure, or hidden chain-of-thought recovery.

## Derived From

This proof executes the synthetic fixture created in `proofs/009-survivable-lineage-fixture`.

## Method

The execution compares two replay modes across the six Proof 009 probes:

- Visible-only replay uses transcript, visible event order, and high-level action sequence.
- Full-lineage replay uses the complete fixture bundle with explicit fixture references.

## Required Artifacts

- `visible_replay_results.json`
- `full_lineage_replay_results.json`
- `comparative_reconstruction_report.md`
- `fixture_claim_register.json`
- `validation_verdict.json`
- `proof_manifest.json`

## Boundary

The validated scope is the synthetic fixture. Passing results support only the fixture-local survivable-lineage claim and do not establish universal sufficiency or evaluate OpenClaw, OpenHands, or private substrate internals.
