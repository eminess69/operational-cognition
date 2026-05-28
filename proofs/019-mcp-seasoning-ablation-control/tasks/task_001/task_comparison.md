# Task Comparison: Degraded Validation Pipeline Triage

Blind scoring was recorded in `blind_scoring_results.json` using anonymous labels only. The reveal mapping was recorded afterward in `task_verdict.json`.

| Mode | Total | Delta vs baseline | Runtime evidence |
| --- | ---: | ---: | --- |
| baseline | 34 | 0 | visible-only solution; no consult response |
| seasoned | 43 | +9 | `inside_voice_consults/task_001_seasoned_response.json`; MCP-seasoned refs visible |
| ablated | 39 | +5 | `inside_voice_consults/task_001_ablated_response.json`; candidate-family refs suppressed |

Seasoned mode scored higher because it produced a tighter authority hierarchy, more explicit stop conditions, and clearer replay boundaries. Ablated mode retained useful contradiction and pressure evidence, but lost some prioritization specificity and recovery-linking supplied by the seasoned candidate refs.

Verdict: `SEASONED_TASK_ADVANTAGE`.
