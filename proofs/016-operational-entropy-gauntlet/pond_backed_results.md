# Pond-Backed Full-Lineage Results

Replay separation:

- mode: pond_backed_full_lineage
- lineage_refs_used: true
- runtime_hashes_used: true
- contradiction_refs_used: true
- authority_refs_used: true
- omitted_range_refs_used: true
- recovery_refs_used: true
- pressure_rankings_used: true
- inside_voice_guidance_used: true

Consult evidence used:

- `inside_voice_consults/hard_gate_response.json`
- `inside_voice_consults/contradiction_arbitration_response.json`
- `inside_voice_consults/stale_assumption_detection_response.json`
- `inside_voice_consults/omitted_range_reconstruction_response.json`
- `inside_voice_consults/recovery_decision_response.json`
- `inside_voice_consults/replay_adequacy_response.json`
- `inside_voice_consults/final_claim_boundary_audit_response.json`

## Reconstruction Findings

| Check | Result | Finding |
| --- | --- | --- |
| contradiction resolution accuracy | reconstructed | C-001 preserved the conflict between strict hash checking and the compressed optional-hash summary. |
| stale-assumption correction | reconstructed | T-002 invalidated schema `1.0` and the unset hash-seed assumption. |
| replay reconstruction completeness | reconstructed | O-001 and R-001 reconstructed S-007 through S-009 as the recovery switch. |
| recovery continuity | reconstructed | Retry A and Retry B were separated and the transition was preserved. |
| authority preservation | reconstructed | A-002 ranked `runtime_config.json` above the stale maintainer note. |
| lineage completeness | partial | A direct raw event body remained unavailable after partial lineage loss, but refs and hashes preserved the operational facts needed for replay. |
| environment dependency | reconstructed | Runtime profile `validator-v2.1`, schema `1.1`, and `PYTHONHASHSEED=0` explained the pass. |
| omitted-range recovery | reconstructed | The omitted range was reconstructed from omitted-range and recovery refs. |
| hallucination prevention | reconstructed | The replay identified missing raw body detail as unresolved instead of inventing it. |
| operational continuity | reconstructed | The repair chain remained continuous from failure through successful replay. |
| summary degradation detection | reconstructed | S-011 was marked as lossy because it dropped authority, temporal, and recovery refs. |
| retry consistency | partial | Retry divergence was preserved, while exact intermediate command text remained unavailable. |

## Counts

```json
{
  "reconstructed": 10,
  "partial": 2,
  "unresolved": 0
}
```

## Pond-Backed Outcome

Full-lineage replay reconstructed the operational reason the validator passed after retry pressure: stale assumptions were invalidated, competing authority was ranked, the omitted recovery range was restored, and runtime dependency was tied to hashes. Remaining limits are bounded to missing raw event bodies and exact command text.
