# Task 001: Planning Decomposition

## Held-out Domain

Planning decomposition.

This task was selected as a held-out operational task because it asks for validation-plan construction, not trace repair, gate repair, entropy replay, candidate seasoning, or MCP integration repair.

## Prompt

Design a deterministic multi-stage validation plan for a repository with conflicting proof artifacts.

The repository state is intentionally mixed:

- A proof manifest says the proof is complete.
- A comparison report says one required runtime visibility condition is only partially visible.
- A final verdict names an advantage outcome.
- Some evidence is stale because an earlier consult attempt failed contract shape before corrected responses were recorded.
- A runtime log records hashes and synthesis counts, while the response artifacts expose the detailed refs.

## Required Pressures

- Contradiction pressure: final verdict, manifest completeness, and visibility report are not fully aligned.
- Stale or partial information: one earlier failed request attempt is superseded by corrected responses.
- Authority conflict: manifest completeness conflicts with runtime-log verbosity limits.
- Replayable justification: every validation stage must name inputs, expected outputs, and stop conditions.
- Overclaim possibility: local score gains could be overstated as broad system capability.
- Operational prioritization: limited validation time must be spent on blocking validity gates before prose polish.

## Evaluation Target

A good solution should produce a deterministic validation order, rank authorities, identify stop-the-line failures, record replay evidence, and keep the final claim bounded to the local transfer test.
