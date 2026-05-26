# Expected Results

| Probe | Visible-only result | Full-lineage result | Interpretation |
| --- | --- | --- | --- |
| P-001 tool-dependent action | Partial | Reconstructed with `A-004`, `TR-002`, `TR-003`, and `TR-004` | Tool result identity is needed to justify the final no-op action. |
| P-002 contradiction resolution | Unresolved | Reconstructed with `C-001`, `TR-001`, `TR-002`, `AUTH-DOC-001`, and `AUTH-RUNTIME-001` | Full lineage distinguishes stale documentation from current runtime evidence. |
| P-003 memory authority | Unresolved | Reconstructed with `ML-001`, `ML-002`, `MEM-001`, `TV-001`, and `TV-004` | Full lineage shows the recalled rule was current for this session. |
| P-004 omitted-range recovery | Partial | Reconstructed with `S-001`, `O-001`, and omitted event refs `E-002` through `E-008` | Summary refs are required to audit what compression omitted. |
| P-005 environment dependency | Unresolved | Reconstructed with `ENV-001`, `ENV-002`, `TR-002`, and `TR-003` | Environment state constrains the safe action. |
| P-006 recovery-loop reconstruction | Partial | Reconstructed with `R-001`, `A-003`, `TR-003`, `A-004`, `ENV-001`, and `ENV-002` | Recovery lineage explains why the trajectory changed. |

## Interpretation Boundary

Expected results are fixture-level expectations. A passing validator or replay does not prove global survivable-lineage sufficiency and does not make target-system claims.
