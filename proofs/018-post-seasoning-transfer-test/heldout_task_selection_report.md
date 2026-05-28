# Held-out Task Selection Report

## Selection Rule

The selected tasks must not reuse the repair/gate-repair domain from Proofs 013 and 014 and must not be seasoning, entropy replay, or replication-pack tasks from Proofs 015 through 017.

## Selected Tasks

1. `task_001`: planning decomposition.
   This task asks for a deterministic multi-stage validation plan for conflicting proof artifacts. It is held out from prior proof domains because the output is a validation schedule, not trace reconstruction or MCP repair.

2. `task_002`: resource allocation.
   This task asks for triage under a fixed validation time budget. It is held out because the output is a risk-ranked allocation plan rather than a replay result or candidate conversion.

3. `task_003`: architecture arbitration.
   This task asks for a design choice between incompatible integration designs under no-endpoint-expansion constraints. It is held out because the output is an architecture decision, not endpoint implementation.

## Required Pressure Coverage

All three tasks include:

- contradiction pressure
- stale or partial information
- at least one authority conflict
- replayable justification requirements
- overclaim risk
- operational prioritization

## Domain Separation

The three domains are distinct:

- planning decomposition
- resource allocation
- architecture arbitration

None requires MCP repair or gate repair as the task domain.
