# Consult Prompt Patterns

## Planning Prompts

Use only when the initial risk is specific:

```
Current task: {task}
Baseline belief: {belief}
Known weak area: {weak_area}
What exact source lineage or evidence cluster should I preserve so I do not prematurely converge?
Do not answer with generic blind spots.
```

## Contradiction Prompts

```
Current leading conclusion: {claim}
Evidence supporting it: {supporting_refs}
What would make this conclusion wrong?
Which evidence cluster conflicts with it?
Which claim boundary am I crossing?
What public source lineage would falsify it?
```

## Recovery Prompts

```
Failed path: {failed_path}
What path should be recovered?
What motif or lineage did I drop?
What should I revisit first?
Only count recoveries that can be verified against public artifacts.
```

## Audit Prompts

```
Final candidate result: {summary}
Audit for unsupported claims, missing lineage, claim-boundary violations, prompt leakage, and overclaiming.
Return concrete changes only.
```

## Premature-Convergence Prompts

```
I am converging on: {current_answer}
Alternative paths checked: {checked_paths}
What alternative pathway is still underweighted, and what evidence would change the ranking?
```

## Lineage Prompts

```
Claim: {claim}
Current lineage: {lineage_refs}
Which required source lineage is missing, duplicated, or too weak?
Which refs are redundant with the baseline?
```
