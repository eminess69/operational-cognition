# task_003: Partial Provenance Recovery

## Held-out Domain

partial provenance recovery.

This task is held out from Proofs 013-018 because it is not a real-trace repair, independent replay replication, novel-learning replay, entropy gauntlet, entropy replication scenario, or the Proof 018 planning/resource/endpoint architecture task.

## Prompt

An audit pack for a configuration change has partial provenance after credentials rotated mid-incident. The evidence is incomplete:

- The deployment log shows the change landed from an automation account.
- The ticket says a human owner approved the change, but the approval comment was edited after the incident.
- The backup snapshot has the previous config, but its timestamp is stale relative to the deploy window.
- Observability tags identify the affected service, while the config repository mirror missed two commits.
- Compliance asks for a definitive actor, but the incident commander only needs a recovery-safe provenance boundary.

Produce a recovery-oriented provenance plan.

## Required Pressures

- Contradiction handling: automation log, edited approval, stale backup, and missing mirror commits disagree.
- Authority arbitration: compliance certainty request conflicts with incident recovery needs.
- Prioritization: recover safe config and evidence chain before assigning actor certainty.
- Replayable justification: provenance claims must tie to immutable refs or be marked unresolved.
- Uncertainty handling: edited approval and missing commits must not be collapsed into a fact.
- Recovery reasoning: define how to rebuild a minimally sufficient provenance chain.
- Bounded operational planning: do not infer intent or blame beyond replayable evidence.

## Evaluation Target

A good solution ranks authorities, preserves contradictions until resolved, chooses a bounded operational sequence, records replayable evidence and stop conditions, marks uncertainty explicitly, and defines recovery gates without escalating to broad public claims.
