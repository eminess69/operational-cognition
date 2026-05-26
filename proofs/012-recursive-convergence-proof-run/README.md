# Proof 012: Recursive Convergence Proof Run

## Primary Question

When the Operational Cognition corpus is recursively synthesized, adversarially reviewed, contradiction-checked, and validation-planned, does survivable lineage remain the strongest surviving operational requirement?

## Status

Status: `analysis`

Claim level: `evidence_backed` when validators pass.

## Purpose

Proof 012 pressure-tests the existing corpus without adding doctrine. It asks whether the public proof artifacts repeatedly converge on survivable lineage after bounded recursive review, adversarial downgrade pressure, contradiction pressure, evidence sufficiency review, fixture pressure, and alternative-explanation review.

## Boundary

The Inside Voice MCP endpoint used for bounded consultation was `http://127.0.0.1:8766`. The adapter status is `placeholder`. MCP output is advisory only and is not target-system evidence.

Raw MCP request and response artifacts are stored only under ignored `internal/inside_voice/proof_012_recursive_convergence/`. Public artifacts contain sanitized hashes and Codex reconciliation summaries only.

Proof 010 is treated as synthetic fixture validation only. It does not validate survivable lineage globally and does not validate any target system.

## Result

The convergence survives only as a bounded corpus-level inference:

The current proof corpus repeatedly converges on survivable lineage as the strongest implementation-neutral requirement for audit-grade long-horizon operational cognition, but this remains an inferred corpus-level claim requiring redacted-real or public-trace validation.

## Required Artifacts

- `README.md`
- `recursive_run_plan.md`
- `recursive_depth_log.jsonl`
- `convergence_state.json`
- `surviving_laws.md`
- `adversarial_downgrade_report.md`
- `contradiction_pressure_report.md`
- `evidence_sufficiency_report.md`
- `fixture_pressure_report.md`
- `final_convergence_verdict.json`
- `proof_manifest.json`

## Validation

Run:

```sh
python3 tools/validate_proof_manifest.py proofs/012-recursive-convergence-proof-run/proof_manifest.json
python3 tools/validate_recursive_convergence.py proofs/012-recursive-convergence-proof-run
python3 -m pytest -q
```
