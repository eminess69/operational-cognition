# Proof 011: Redacted-Real Trace Candidate for Survivable Lineage Validation

## Primary Question

Can a real public or redacted-real operational trace be safely converted into the survivable-lineage fixture format for replay validation?

## Status

Proof 011 is an `evidence_collection` proof pack with claim level `planning_scaffold`.

No real trace has been selected or executed. The current candidate status is `not_selected`, and replay execution remains disabled until a candidate passes the eligibility checks in `candidate_manifest.json` and `eligibility_matrix.md`.

## Purpose

Proof 009 created a synthetic survivable-lineage fixture. Proof 010 validated replay behavior against that fixture. Proof 011 prepares the first disciplined bridge from public or redacted-real trace evidence into the same fixture structure without importing unsafe material or overstating what the evidence supports.

## Boundary

This proof is a candidate-preparation scaffold. It does not evaluate a live target, infer private internals, recover hidden chain of thought, or claim that any target system is defective. It only defines the conditions under which a public or redacted-real trace may be converted into the Proof 009/010 fixture format.

## Required Artifacts

- `candidate_selection_policy.md`
- `trace_conversion_plan.md`
- `eligibility_matrix.md`
- `redaction_policy.md`
- `candidate_manifest.json`
- `proof_manifest.json`
- `public_lineage_summary.md`
- `unresolved_requirements.md`
- `candidate/README.md`
- `candidate/.gitkeep`

## Execution Rule

The real-trace replay step must not run while `candidate_manifest.json` reports `candidate_status` as `not_selected`, `selected`, or `rejected`. A later update may mark the candidate `eligible` only after redaction is complete, provenance is established, required lineage fields are present, and visible-only replay can be distinguished from full-lineage replay.
