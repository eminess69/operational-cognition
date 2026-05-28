# Gauntlet Design

The gauntlet uses six deterministic operational degradation scenarios. Each scenario includes the full severe-condition set: long-horizon sequence, omitted-range loss, stale authority, contradictory summaries, retry divergence, replay ambiguity, runtime drift, incomplete recovery trace, partial lineage corruption, compressed context degradation, temporal validity conflict, three linked contradiction chains, two authority conflicts, and at least one failed recovery branch.

Mode separation is the central control. Baseline artifacts may use only visible transcript order and visible summaries. Pond-backed artifacts may use recorded full-lineage data and the scenario consult response. Actual MCP-seasoned artifact refs are recorded only in pond-backed results and consult responses, not in baseline results.

Neutral hard gate:

- adapter_status: `pond_backed`
- contribution_grade: `bounded`
- gate_failures: `[]`
- runtime_stage_report_ref: `artifacts/integrations/inside_voice_runtime/runtime_stage_report.json`
- runtime_response_hash: `0624ced2bcbc40347694c56f38b994421cf1b93e4646c059d9e97c5d01ecde4c`

No promotion or endpoint expansion occurred.
