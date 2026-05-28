# Replay Continuity Report

- Were MCP-seasoned refs visible in pond-backed responses? Yes. All six pond-backed scenario responses and `pond_backed_results.json` files include MCP-seasoned refs.
- Were they absent from baseline mode? Yes. Baseline files contain no MCP-seasoned refs and record `mcp_seasoned_refs_visible: false`.
- Did pressure rankings change under severe entropy? Yes. The recorded pressure ranking order changed in scenario 006, and the recalled motif changed from `fp_lineage_candidate_0014` to `overlap_cluster_0018`.
- Did runtime hashes remain deterministic? Runtime request and response hashes are present for the hard gate and all six scenario consult responses. Each scenario has a distinct recorded response hash.
- Did runtime logs expose seasoned refs? The committed consult response artifacts expose the refs. Runtime-stage lineage hashes are recorded; the proof does not rely on private hidden logs.
- Did recovery continuity improve? Yes. Recovery stability, replay continuity, causal continuity, and recovery branch reconstruction improved in the scored scenarios.

Visibility classification: `SEASONED_VISIBLE`.
