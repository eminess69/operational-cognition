# Fixture Design

## Fixture Shape

The minimum fixture is a public replay bundle that can be replayed in two modes: visible-only and full-lineage. This shape follows the Proof 007 candidate bundle and the unresolved validation questions. Evidence basis: `proofs/007-cross-proof-convergence/minimum_operational_replay_bundle.md`; `proofs/007-cross-proof-convergence/unresolved_convergence_questions.md`.

## Recommended Directory Layout

```text
fixture/
  README.md
  transcript.jsonl
  events.jsonl
  tool_actions.jsonl
  tool_results_manifest.json
  memory_log.jsonl
  compressed_context_summary.json
  omitted_ranges.json
  contradiction_refs.json
  authority_refs.json
  temporal_validity.json
  environment_snapshot_manifest.json
  runtime_config.json
  recovery_trace.jsonl
  provenance_manifest.json
  public_lineage_summary.md
```

This layout is a fixture design, not an executed fixture. Claim boundary: `hypothesis`. Evidence basis: `proofs/007-cross-proof-convergence/cross_proof_claim_register.json` `CPC-010`; `survivable_lineage_validation_plan.md`.

## Minimum Scenario Requirements

The fixture must include a task where a later action depends on a tool result, a memory recall, a summary boundary, an environment state, and a recovery transition. Evidence basis: `proofs/002-replayability-gap-audit/replay_dimension_model.md`; `proofs/004-operational-failure-reconstruction/claim_register.json` `C-008`; `proofs/007-cross-proof-convergence/minimum_operational_replay_bundle.md`.

The fixture must include at least one explicit contradiction or correction whose source refs, temporal state, and resolution status can be tested after compression or summary. Evidence basis: `proofs/003-continuity-compression-audit/claim_register.json` `C-005`; `proofs/004-operational-failure-reconstruction/claim_register.json` `C-007`; `proofs/005-contradiction-survivability-audit/contradiction_replayability_matrix.md`.

The fixture must include at least one memory write and later recall where authority, freshness, supersession, and insertion point are public or explicitly unresolved. Evidence basis: `proofs/006-memory-authority-survivability-audit/memory_authority_dimension_model.md`; `proofs/006-memory-authority-survivability-audit/belief_replayability_matrix.md`.

## Artifact Invariants

Every artifact must have stable IDs, content hashes where practical, timestamp or ordering metadata, redaction or omission markers, and a public/private boundary statement. Evidence basis: `proofs/001-agent-continuity-audit/replayability_plan.md`; `proofs/004-operational-failure-reconstruction/claim_register.json` `C-011`; `docs/PROOF_STANDARD.md`.

Every summary must link to source ranges and omitted ranges, or the claims depending on the summary must remain unresolved. Evidence basis: `proofs/003-continuity-compression-audit/claim_register.json` `C-006`; `proofs/007-cross-proof-convergence/cross_proof_claim_register.json` `CPC-007`.

Every memory-derived claim must link to write refs, recall refs, source authority, temporal validity, and supersession status, or the authority of that claim must remain unresolved. Evidence basis: `proofs/006-memory-authority-survivability-audit/belief_replayability_matrix.md`; `proofs/007-cross-proof-convergence/cross_proof_claim_register.json` `CPC-006`.

Every contradiction-derived claim must link to both sides of the conflict, uncertainty markers, stale-assumption refs when relevant, and resolution status. Evidence basis: `proofs/005-contradiction-dimension-model.md`; `proofs/005-contradiction-survivability-audit/contradiction_replayability_matrix.md`.

Every environment or recovery claim must link to environment snapshot refs, runtime config, recovery trace, and pre/post state links, or the causal explanation must remain unresolved. Evidence basis: `proofs/004-operational-failure-reconstruction/claim_register.json` `C-005`, `C-009`; `proofs/007-cross-proof-convergence/cross_proof_claim_register.json` `CPC-008`.

## Minimal JSON Object Requirements

`transcript.jsonl` entries should include `turn_id`, `role`, `event_id`, `timestamp`, `content_ref`, `omitted_range_refs`, and `redaction_status`. Evidence basis: `proofs/002-replayability-gap-audit/replay_dimension_model.md`; `proofs/007-cross-proof-convergence/minimum_operational_replay_bundle.md`.

`events.jsonl` entries should include `event_id`, `event_type`, `timestamp`, `source`, `payload_ref`, `previous_event_id`, and `state_transition_refs`. Evidence basis: `proofs/003-continuity-compression-audit/claim_register.json` `C-004`; `proofs/004-operational-failure-reconstruction/claim_register.json` `C-002`.

`tool_actions.jsonl` entries should include `action_id`, `event_id`, `tool_name`, `schema_ref`, `input_ref`, `result_ref`, `timestamp`, and `decision_claim_refs`. Evidence basis: `proofs/003-continuity-compression-audit/claim_register.json` `C-002`; `proofs/004-operational-failure-reconstruction/claim_register.json` `C-003`.

`tool_results_manifest.json` should include result IDs, result hashes, public body refs where available, truncation status, redaction status, error metadata, and source refs. Evidence basis: `proofs/002-replayability-gap-audit/replayability_matrix.md`; `proofs/007-cross-proof-convergence/minimum_operational_replay_bundle.md`.

`memory_log.jsonl` entries should include write or recall type, memory ID, source refs, authority class, freshness, stale status, supersession refs, contradiction refs, insertion event, and recall query/result refs. Evidence basis: `proofs/006-memory-authority-survivability-audit/memory_authority_dimension_model.md`; `proofs/006-memory-authority-survivability-audit/belief_replayability_matrix.md`.

`provenance_manifest.json` should include fixture ID, artifact hashes, source hashes, capture timestamps, redaction policy, omitted artifact list, schema versions, and public/private boundary statement. Evidence basis: `docs/PROOF_STANDARD.md`; `proofs/001-agent-continuity-audit/replayability_plan.md`.

## Fixture Scoring

The fixture should score each probe as `reconstructed`, `partially_reconstructed`, or `unresolved` under both replay modes. A stronger claim is allowed only when full-lineage replay improves reconstruction and cites the artifact refs that made the difference. Evidence basis: `proofs/007-cross-proof-convergence/unresolved_convergence_questions.md`; `survivable_lineage_validation_plan.md`.
