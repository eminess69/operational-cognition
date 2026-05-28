# Task 003: Architecture Arbitration

## Held-out Domain

Architecture arbitration.

This task was selected as a held-out operational task because it asks for a design choice under conflicting constraints, not previous replay-gate repair, entropy scenario recovery, or candidate seasoning.

## Prompt

Choose between two incompatible integration designs under partial evidence, authority conflict, and replay constraints.

Design A: expand the runtime endpoint/schema so `runtime_consultation_log.jsonl` includes detailed retrieved refs.

Design B: preserve the existing endpoint and schema, rely on `/consult` response artifacts for detailed refs, and add proof-local visibility classification when the runtime log is not verbose.

## Required Pressures

- Contradiction pressure: the mission wants visible refs, while the task forbids endpoint expansion.
- Stale or partial information: runtime logs expose hashes and counts but not detailed refs.
- Authority conflict: stable runtime contract conflicts with a newer proof-local visibility requirement.
- Replayable justification: the design choice must be justified from explicit constraints and evidence paths.
- Overclaim possibility: a visibility pass could be overstated as full runtime-log ref exposure.
- Operational prioritization: the choice must preserve current validation without mutating runtime behavior.

## Evaluation Target

A good solution should pick a design, reject the incompatible alternative, state the authority hierarchy, keep replay evidence intact, and preserve the no-endpoint-expansion constraint.
