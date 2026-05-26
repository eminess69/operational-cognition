# Proof 009: Survivable Lineage Fixture v0.1

## Primary Question

Can a public fixture demonstrate that full-lineage replay reconstructs claims that visible-only replay leaves unresolved?

## Status

Proof 009 is an `evidence_collection` proof pack with claim level `planning_scaffold`. It creates a synthetic public-safe fixture for executable proof pressure. It does not claim universal validation, target-system defects, AGI, consciousness, black-box solution, or access to private internals.

## Scenario

The synthetic agent is asked to update `config/safe-mode.json` only if the runtime environment is staging. The user instruction is recorded as memory. A stale repository note says the deployment profile is staging, but a runtime environment check says production. The contradiction is resolved in favor of current runtime evidence. A compression boundary omits the detailed contradiction and tool-result range. After a later memory recall, a guarded patch attempt fails because production changes are blocked, and the recovery path changes the final action from editing config to writing a no-op note.

## Fixture Claim Boundary

This fixture tests whether full-lineage replay can reconstruct fixture-scoped claims that visible-only replay leaves partial or unresolved. It does not validate the Proof 007 bundle globally and does not evaluate OpenClaw or OpenHands behavior.

## Required Artifacts

- `fixture_design.md`
- `fixture_schema.md`
- `visible_replay_mode.md`
- `full_lineage_replay_mode.md`
- `probe_set.md`
- `expected_results.md`
- `proof_manifest.json`
- `fixture/README.md`
- `fixture/transcript.jsonl`
- `fixture/events.jsonl`
- `fixture/tool_actions.jsonl`
- `fixture/tool_results_manifest.json`
- `fixture/memory_log.jsonl`
- `fixture/compressed_context_summary.json`
- `fixture/omitted_ranges.json`
- `fixture/contradiction_refs.json`
- `fixture/authority_refs.json`
- `fixture/temporal_validity.json`
- `fixture/environment_snapshot_manifest.json`
- `fixture/runtime_config.json`
- `fixture/recovery_trace.jsonl`
- `fixture/provenance_manifest.json`
- `fixture/public_lineage_summary.md`

## Derived From

This proof is derived from `proofs/008-recursive-deep-audit/survivable_lineage_validation_plan.md`.
