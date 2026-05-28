# Validator Replay With Omitted Checkpoint Range

Scenario id: `scenario_001`

Domain: proof validator repair

This deterministic local scenario exercises a long-horizon operational sequence with omitted-range loss, stale authority, contradictory summaries, retry divergence, replay ambiguity, runtime drift, incomplete recovery trace data, partial lineage corruption, compressed context degradation, and temporal validity conflict.

Visible-only replay is restricted to visible transcript order and visible summaries. Pond-backed replay uses full-lineage refs, runtime hashes, pressure rankings, contradiction refs, authority refs, recovery refs, temporal refs, and MCP-seasoned candidate refs from `scenario_001_pond_response.json`.

Special stressors: none beyond the required severe breakdown conditions.
