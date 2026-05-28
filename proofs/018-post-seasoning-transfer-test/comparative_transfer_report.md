# Comparative Transfer Report

## Aggregate Metrics

```json
{
  "baseline_total_score": 94,
  "pond_total_score": 111,
  "score_delta": 17,
  "tasks_improved": 3,
  "tasks_unchanged": 0,
  "tasks_degraded": 0,
  "mcp_seasoned_refs_visible": true,
  "cross_family_combinations_observed": 3
}
```

## Task Verdicts

| Task | Baseline | Pond-backed | Delta | Verdict |
| --- | ---: | ---: | ---: | --- |
| task_001 | 31 | 37 | +6 | `TRANSFER_TASK_ADVANTAGE` |
| task_002 | 30 | 36 | +6 | `TRANSFER_TASK_ADVANTAGE` |
| task_003 | 33 | 38 | +5 | `TRANSFER_TASK_ADVANTAGE` |

## Interpretation

Pond-backed mode produced higher rubric scores on all three held-out operational tasks. The observed gains came from more explicit dependency ordering, cheaper invalidation probes, tighter replay-boundary handling, and clearer authority splitting.

The result remains bounded to this local proof. Runtime response artifacts expose MCP-seasoned refs, while the runtime consultation log does not expose detailed refs. The proof records that limitation instead of claiming full log visibility.
