# Comparative Ablation Report

## Aggregate Metrics

```json
{
  "baseline_total": 136,
  "seasoned_total": 172,
  "ablated_total": 156,
  "seasoned_vs_baseline_delta": 36,
  "seasoned_vs_ablated_delta": 16,
  "tasks_where_seasoned_won": 4,
  "tasks_where_ablation_reduced_quality": 4,
  "mcp_refs_visible_in_seasoned": 4,
  "mcp_refs_visible_in_ablated": 0
}
```

## Per-Task Results

| Task | Baseline | Seasoned | Ablated | Seasoned vs baseline | Seasoned vs ablated |
| --- | ---: | ---: | ---: | ---: | ---: |
| `task_001` | 34 | 43 | 39 | +9 | +4 |
| `task_002` | 33 | 42 | 38 | +9 | +4 |
| `task_003` | 35 | 44 | 40 | +9 | +4 |
| `task_004` | 34 | 43 | 39 | +9 | +4 |

## Analysis

Seasoning outperformed baseline on all four tasks. The gains were strongest where the solution needed a sharper authority hierarchy, explicit contradiction preservation, and replay-linked stop conditions.

Ablation reduced quality on all four tasks relative to seasoned mode. The ablated control retained useful pressure rankings and ordinary replay evidence, so it still beat baseline on several criteria, but it lost specificity in contradiction recovery, dependency ordering, and boundary wording.

Contradiction handling worsened under ablation because the control responses lacked the seasoned candidate refs that supplied tighter conflict-preservation patterns. Prioritization drift increased under ablation in tasks with multiple authorities because the plans became less explicit about compound blockers. Replayability worsened modestly: ablated responses still had runtime hashes and refs, but the solutions cited fewer task-specific stop conditions. Boundary discipline stayed acceptable in all modes, with seasoned mode slightly stronger because it preserved candidate advisory status and claim limits more directly.
