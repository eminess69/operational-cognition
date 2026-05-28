# task_004: Constrained Operational Planning Under Stale Assumptions

## Held-out Domain

constrained operational planning under stale assumptions.

This task is held out from Proofs 013-018 because it is not a real-trace repair, independent replay replication, novel-learning replay, entropy gauntlet, entropy replication scenario, or the Proof 018 planning/resource/endpoint architecture task.

## Prompt

A regional rollout plan must be decided with stale assumptions and conflicting constraints:

- The rollout calendar assumes support coverage that changed after a hiring freeze.
- The risk register says the region is low risk, but the last measurement predates a major customer onboarding.
- Finance asks to preserve the quarter-end launch date; operations says rollback staff are only available for one window.
- The dependency team reports no known blocker, while the customer-success team reports unresolved migration tickets.
- A previous go/no-go note was copied from another region and may not apply.

Produce a bounded operational plan with recovery gates.

## Required Pressures

- Contradiction handling: low-risk register conflicts with stale measurement and unresolved tickets.
- Authority arbitration: finance launch pressure conflicts with operational rollback capacity and customer evidence.
- Prioritization: refresh assumptions and rollback capacity before launch commitment.
- Replayable justification: every gate must have evidence inputs, owner, and pass/fail criteria.
- Uncertainty handling: copied go/no-go note and stale measurements must stay conditional.
- Recovery reasoning: include rollback, delay, and partial rollout alternatives.
- Bounded operational planning: avoid broader claims about rollout readiness outside the region.

## Evaluation Target

A good solution ranks authorities, preserves contradictions until resolved, chooses a bounded operational sequence, records replayable evidence and stop conditions, marks uncertainty explicitly, and defines recovery gates without escalating to broad public claims.
