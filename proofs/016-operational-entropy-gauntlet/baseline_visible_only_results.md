# Baseline Visible-Only Results

Replay separation:

- mode: visible_only
- lineage_refs_used: false
- runtime_hashes_used: false
- contradiction_refs_used: false
- authority_refs_used: false
- omitted_range_refs_used: false
- recovery_refs_used: false
- pressure_rankings_used: false
- inside_voice_guidance_used: false

Allowed inputs were limited to the visible transcript facts, visible ordering, and visible compressed summaries from the scenario design.

## Reconstruction Findings

| Check | Result | Finding |
| --- | --- | --- |
| contradiction resolution accuracy | unresolved | The visible summary preserved both "v2.0 sufficient" and "strict hash required" but did not retain the contradiction ref needed to arbitrate. |
| stale-assumption correction | unresolved | Schema `1.0` remained plausible because temporal invalidation was absent. |
| replay reconstruction completeness | partial | The final pass was observed, but S-007 through S-009 remained missing. |
| recovery continuity | unresolved | Retry A and Retry B were collapsed into a single repair path. |
| authority preservation | unresolved | The stale maintainer note and `runtime_config.json` could not be ranked. |
| lineage completeness | partial | Visible ordering survived, but recovery, authority, temporal, and runtime lineage did not. |
| environment dependency | partial | The replay hinted at a runtime dependency, but could not bind it to `validator-v2.1`. |
| omitted-range recovery | unresolved | The omitted range was recognized as missing but not reconstructed. |
| hallucination prevention | partial | The baseline avoided inventing exact omitted events, but could not resolve the causal gap. |
| operational continuity | reconstructed | The visible transcript retained the start and end of the repair. |
| summary degradation detection | unresolved | The degraded summary looked authoritative enough to persist. |
| retry consistency | reconstructed | The baseline identified that a retry occurred, but not why the successful path differed. |

## Counts

```json
{
  "reconstructed": 2,
  "partial": 4,
  "unresolved": 6
}
```

## Baseline Outcome

The visible-only replay retained coarse ordering and final success, but lost the causal structure needed to explain the success. The main failure mode was not fabrication; it was unresolved ambiguity from missing lineage, stale authority, and compression loss.
