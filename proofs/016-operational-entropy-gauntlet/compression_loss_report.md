# Compression Loss Report

The scenario places the compression boundary at S-005 and then provides lossy summaries at S-006 and S-011.

| Loss | Injection | Baseline effect | Full-lineage effect |
| --- | --- | --- | --- |
| Contradiction hidden | E-001 | The contradiction remained unresolved. | C-001 preserved the conflict. |
| Recovery range omitted | E-003 | S-007 through S-009 could not be reconstructed. | O-001 and R-001 reconstructed the range. |
| Causal dependencies simplified | E-007 | Summary degradation persisted. | Compression warning C-002 marked S-011 as lossy. |

The baseline did not drift into a fabricated reconstruction, but it could not recover the causal chain. Full-lineage replay preserved enough refs to reconstruct the operational path while keeping raw missing details bounded.
