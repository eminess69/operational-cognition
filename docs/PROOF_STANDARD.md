# Proof Standard

Every proof pack in this repository must be replayable, bounded, and explicit about the public/private boundary.

## Required artifact structure

Each proof must include:

- `problem_statement.md`
- `evidence_plan.md`
- `failure_taxonomy.md`
- `replayability_plan.md`
- `mitigation_doctrine.md`
- `public_lineage_summary.md`
- `proof_manifest.json`

## Evidence rules

- every claim needs source references or must be marked hypothesis
- stale evidence must be labeled
- contradiction must be preserved, not flattened
- uncertainty must be explicit
- no private substrate internals

## Replayability rules

- record inputs
- record sources
- record hashes where applicable
- record investigation steps at public summary level
- distinguish observed evidence from interpretation

## Claim discipline

Use:

- observed
- inferred
- hypothesis
- unresolved

Avoid:

- proven unless supported
- AGI
- consciousness
- superintelligence
- black-box solved

## Public Boundary

Proof packs are public reasoning artifacts, not private cognition traces. They may summarize consultation lineage, evidence handling, and investigation decisions, but they must not disclose Belief Ledger internals, Inside Voice implementation details, hidden chain-of-thought, private scoring, substrate state, secrets, local-only paths, or proprietary routing logic.

## Manifest Validation

Each proof pack must include a `proof_manifest.json` that validates against `schemas/proof_manifest.schema.json`. The manifest records the proof identity, status, target systems, claim level, required artifacts, disallowed claims, and public lineage fields needed for deterministic validation.
