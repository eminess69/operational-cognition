# Proof 015 - Novel Learning Replay Test

## Purpose

This proof tests whether a single new operational learning record can be created during a task, sent through pond-backed Inside Voice with lineage, and replayed on a changed repeat variant to improve reconstruction and audit actionability.

## Selected Task

The selected task is a deterministic validator for replay artifact completeness. It is separate from Proofs 013 and 014 because it does not repair or replay an MCP/proof gate trace. It designs a proof-bundle validator pattern.

## Execution Summary

1. The hard gate passed with `adapter_status == "pond_backed"`, `contribution_grade == "bounded"`, non-empty pressure rankings, empty gate failures, and runtime hashes.
2. Codex created `initial_codex_solution.md`.
3. Codex extracted `inside_voice_learning_record.json` with learning id `proof_015_learning_001`.
4. The learning record was sent to `/consult` using the required bounded-learning wording.
5. A repeat request changed the surface task to fixture-minimization artifact completeness and did not paste the original solution.
6. The repeat response preserved learning-record refs, pressure refs, boundary audit output, and replay hashes.
7. The repeat solution used the three-layer replay pattern.
8. The comparative audit found six improved dimensions and three unchanged strong dimensions.

## Verdict

`LEARNING_REPLAY_ADVANTAGE_OBSERVED`

This verdict is scoped only to this proof bundle and repeat variant. It does not assert a general capability result.
