# Runtime Log Visibility Report

## Questions

Did the per-task consult responses expose MCP-seasoned refs?

Yes. All three successful per-task consult responses expose `mcp_seasoned` refs in `retrieved_artifact_refs`.

Did `runtime_consultation_log.jsonl` expose MCP-seasoned refs?

No. The runtime log entries for `proof-018-task-001-pond-backed`, `proof-018-task-002-pond-backed`, and `proof-018-task-003-pond-backed` expose request hashes, response hashes, corpus hashes, schema version, counts, and synthesis text. They do not include detailed retrieved artifact refs.

## Classification

`RESPONSE_VISIBLE_LOG_NOT_VERBOSE`

The refs are visible in response artifacts but not in the runtime consultation log. This is a logging-verbosity gap, not a reason to claim full runtime-log ref visibility.

## Evidence

Response-visible refs:

- `task_001`: `artifacts/pond/mcp_seasoned_first_principles_admitted.jsonl#35`, `artifacts/pond/mcp_seasoned_reusable_lineage_candidates.jsonl#35`, `artifacts/pond/mcp_seasoned_first_principles_admitted.jsonl#49`
- `task_002`: `artifacts/pond/mcp_seasoned_first_principles_admitted.jsonl#49`, `artifacts/pond/mcp_seasoned_reusable_lineage_candidates.jsonl#49`, `artifacts/pond/mcp_seasoned_first_principles_admitted.jsonl#19`
- `task_003`: `artifacts/pond/mcp_seasoned_first_principles_admitted.jsonl#49`, `artifacts/pond/mcp_seasoned_reusable_lineage_candidates.jsonl#49`, `artifacts/pond/mcp_seasoned_first_principles_admitted.jsonl#19`

Runtime-log-visible fields:

- `request_id`
- `request_hash`
- `response_hash`
- `corpus_hash`
- `schema_version`
- `proof_ref_count`
- `recalled_motif_count`
- `claim_pressure_count`
- `unresolved_tension_count`
- `synthesis_result`

## Boundary

The proof uses response-visible refs for transfer scoring and records the runtime-log limitation explicitly.
