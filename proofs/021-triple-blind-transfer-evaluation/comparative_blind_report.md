# Comparative Blind Report

## Pre-Reveal State

The scorer evaluated only `solution_A`, `solution_B`, and `solution_C` for each task. The blind score file records no mode mapping and no source refs. The locked blind score hash is:

`75803b2f097766f4545f88470f179a49a3a597e84b7a0fb7e2a07284523b03f8`

## Post-Reveal Result

| Metric | baseline visible-only | pond-backed ablated | pond-backed MCP-seasoned |
| --- | ---: | ---: | ---: |
| Aggregate score | 152 | 158 | 174 |
| Delta vs MCP-seasoned | -22 | -16 | 0 |
| First-place or tied tasks | 0 | 0 | 5 |

## Task-Level Result

| Task | Winner after reveal | Score spread |
| --- | --- | --- |
| `task_001` | pond-backed MCP-seasoned | 36 vs 32 vs 30 |
| `task_002` | pond-backed MCP-seasoned | 35 vs 31 vs 29 |
| `task_003` | pond-backed MCP-seasoned | 34 vs 32 vs 31 |
| `task_004` | pond-backed MCP-seasoned | 34 vs 30 vs 30 |
| `task_005` | pond-backed MCP-seasoned | 35 vs 33 vs 32 |

## Interpretation Boundary

The result satisfies the proof-local confirmation criteria. It remains bounded to five held-out operational fixtures, the anonymized answer set, and the rubric in `blind_protocol.md`. It does not support claims about unrelated tasks, target systems, or broad capability.
