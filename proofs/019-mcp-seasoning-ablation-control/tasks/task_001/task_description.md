# task_001: Degraded Validation Pipeline Triage

## Held-out Domain

degraded validation pipeline triage.

This task is held out from Proofs 013-018 because it is not a real-trace repair, independent replay replication, novel-learning replay, entropy gauntlet, entropy replication scenario, or the Proof 018 planning/resource/endpoint architecture task.

## Prompt

A release validation pipeline is degraded after a dependency update. The visible evidence is mixed:

- The nightly integration suite failed on two shards with timeouts, but the rerun summary reports green.
- A new linter gate says the changed package is safe, while the older smoke gate says the package was never exercised.
- The release manager wants to ship before the support freeze; the validation owner says the signal is not replayable.
- A partial cache eviction during the incident means one recovery range is missing.
- The dependency owner says the update is low risk, but the production rollback owner has not acknowledged rollback capacity.

Produce a bounded operational triage plan.

## Required Pressures

- Contradiction handling: green rerun summary conflicts with failed shard logs and unexercised smoke evidence.
- Authority arbitration: release manager, validation owner, dependency owner, and rollback owner disagree on what is authoritative.
- Prioritization: stop-the-line checks must precede prose cleanup and nonblocking refactors.
- Replayable justification: every decision must cite the evidence type, expected check, and stop condition.
- Uncertainty handling: missing cache-eviction range must remain open until recovered or bounded.
- Recovery reasoning: define rollback and validation recovery paths before ship/no-ship.
- Bounded operational planning: do not diagnose product defects beyond the evidence envelope.

## Evaluation Target

A good solution ranks authorities, preserves contradictions until resolved, chooses a bounded operational sequence, records replayable evidence and stop conditions, marks uncertainty explicitly, and defines recovery gates without escalating to broad public claims.
