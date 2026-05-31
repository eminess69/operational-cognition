# Proof 037 - Mechanism Diversity Study

Proof 037 compares equal teaching volume with different mechanism diversity.

- Group A: 3 mechanisms, 96 examples each, 288 total.
- Group B: 12 mechanisms, 24 examples each, 288 total.

Both groups use fresh isolated pond states and pond-backed MCP seasoning/recall.

## Result

`FAIL`

## Metrics

- Group A valid candidate rate: 0.0
- Group B valid candidate rate: 0.0
- Group A candidate diversity: 1.0
- Group B candidate diversity: 1.0
- Group A combination depth: 1.0
- Group B combination depth: 1.0
- Group A premature convergence: 1.0
- Group B premature convergence: 1.0
- Improvement delta: 0.0

## Bounded Claim

With total seasoning volume held constant, the diverse 12-mechanism pond did not produce more valid recombination candidates, more candidate pathway diversity, or deeper mechanism combinations than the saturated 3-mechanism pond.

The hostile audit rejects training-volume and prompt-volume explanations because both groups used 288 seasoning examples and the same request contract. The remaining explanation is simpler: the current recall path converged on one dominant mechanism per case rather than recombining mechanisms.

## Harmonic Overlap

Multiple mechanisms activated together more often in Group B: 0 cases versus 0 in Group A.
