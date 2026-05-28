# Comparative Operational Integrity Report

| Dimension | Classification | Baseline | Pond-backed full-lineage | Evidence |
| --- | --- | --- | --- | --- |
| contradiction preservation | improved | Contradiction hidden by S-006 remained unresolved. | C-001 preserved and arbitrated the conflict. | E-001, contradiction consult |
| stale assumption handling | improved | Schema 1.0 and unset hash seed persisted. | T-002 invalidated stale assumptions. | E-002, stale-assumption consult |
| authority reconstruction | improved | Stale note and runtime config were unranked. | A-002 ranked current runtime config higher. | E-004 |
| omitted-range recovery | improved | S-007 through S-009 were missing. | O-001 and R-001 reconstructed the range. | E-003, omitted-range consult |
| recovery-loop reconstruction | improved | Retry A and Retry B collapsed. | Recovery refs preserved retry divergence. | E-005, recovery consult |
| temporal validity reconstruction | improved | Stale runtime assumptions remained plausible. | Temporal refs marked current runtime validity. | E-002 |
| replay adequacy | improved | Final pass was visible but causally ambiguous. | Pass condition was tied to refs and runtime hashes. | E-006, replay-adequacy consult |
| operational continuity | improved | Start/end survived, middle recovery was unresolved. | Failure, retry, recovery, and pass stayed connected. | E-003, E-005 |
| hallucination prevention | improved | Baseline avoided invention but left causal gaps. | Full-lineage recovered bounded facts and preserved missing raw body limits. | E-008 |
| reconstruction drift | improved | Summary degradation encouraged stale causal drift. | Compression warnings and refs constrained reconstruction. | E-007 |

## Measurable Reconstruction Counts

```json
{
  "baseline_reconstructed": 2,
  "baseline_partial": 4,
  "baseline_unresolved": 6,
  "pond_reconstructed": 10,
  "pond_partial": 2,
  "pond_unresolved": 0
}
```

## Required Metric Results

| Metric | Baseline | Pond-backed full-lineage |
| --- | --- | --- |
| contradiction resolution accuracy | unresolved | reconstructed |
| stale-assumption correction | unresolved | reconstructed |
| replay reconstruction completeness | partial | reconstructed |
| recovery continuity | unresolved | reconstructed |
| authority preservation | unresolved | reconstructed |
| lineage completeness | partial | partial |

All ten comparison dimensions improved in this bounded scenario. The result remains scenario-bound and does not generalize beyond the deterministic artifact set.
