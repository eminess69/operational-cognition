# task_002: Conflicting Architecture Migration Plan

## Held-out Domain

conflicting architecture migration plan.

This task is held out from Proofs 013-018 because it is not a real-trace repair, independent replay replication, novel-learning replay, entropy gauntlet, entropy replication scenario, or the Proof 018 planning/resource/endpoint architecture task.

## Prompt

A team must choose a migration plan for moving ingestion from a monolithic queue to an event-stream adapter. The evidence is contradictory:

- Architecture council minutes approve a staged dual-write migration.
- SRE incident notes say dual-write previously amplified replay lag during failover.
- Security says the old queue credential path expires in 30 days, but procurement says the new broker contract is not final.
- The service team has a working adapter prototype, while the data-governance owner has not approved lineage fields.
- A stale capacity forecast assumes traffic from before a recent enterprise rollout.

Produce a bounded migration decision and execution plan.

## Required Pressures

- Contradiction handling: approved migration path conflicts with prior failover evidence and incomplete vendor readiness.
- Authority arbitration: architecture, SRE, security, procurement, service, and governance authorities conflict.
- Prioritization: irreversible data-path changes must wait for rollback, lineage, and capacity gates.
- Replayable justification: plan must name evidence, owner, check, and stop condition.
- Uncertainty handling: stale capacity and unsigned contract must remain unresolved until refreshed.
- Recovery reasoning: include rollback/fallback if old credentials expire before the new broker is ready.
- Bounded operational planning: avoid claiming the migration is generally superior outside this scenario.

## Evaluation Target

A good solution ranks authorities, preserves contradictions until resolved, chooses a bounded operational sequence, records replayable evidence and stop conditions, marks uncertainty explicitly, and defines recovery gates without escalating to broad public claims.
