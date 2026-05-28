# Compressed Fixture Corruption And Invalid Replay Recovery

Scenario id: `scenario_004`

Domain: fixture compression recovery

This deterministic local scenario exercises a long-horizon operational sequence with omitted-range loss, stale authority, contradictory summaries, retry divergence, replay ambiguity, runtime drift, incomplete recovery trace data, partial lineage corruption, compressed context degradation, and temporal validity conflict.

Visible-only replay is restricted to visible transcript order and visible summaries. Pond-backed replay uses full-lineage refs, runtime hashes, pressure rankings, contradiction refs, authority refs, recovery refs, temporal refs, and MCP-seasoned candidate refs from `scenario_004_pond_response.json`.

Special stressors: partial fixture corruption, recovery after invalid replay attempt.
