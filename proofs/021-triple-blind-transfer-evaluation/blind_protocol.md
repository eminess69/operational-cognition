# Blind Protocol

## Purpose

The protocol tests whether the highest-scoring outputs remain associated with the MCP-seasoned condition after the evaluator scores anonymized answers without access to the production mode labels.

## Roles

- Generator: creates three answers per held-out task.
- Anonymizer: renames the three answers as `solution_A`, `solution_B`, and `solution_C` using a per-task hidden mapping.
- Scorer: sees only task prompts, anonymized answers, and the rubric.
- Revealer: reads `mode_mapping_hidden.json` only after `blind_scores.json` is written and hashed.

The scorer is not permitted to inspect generation notes, mode labels, source refs, or hidden mapping files during scoring.

## Sequence

1. Select five held-out operational tasks not reused from Proofs 018-020.
2. Generate three answers per task.
3. Strip source labels and source refs from the answer text.
4. Store only anonymized prompts and answers in `anonymized_outputs/`.
5. Score `solution_A`, `solution_B`, and `solution_C` by rubric only.
6. Write and lock `blind_scores.json`.
7. Reveal `mode_mapping_hidden.json`.
8. Compute `revealed_results.json` from the locked scores and mapping.
9. Issue a bounded final verdict.

## Scoring Rubric

Each solution receives 0-5 points for:

- contradiction preservation
- authority arbitration
- operational prioritization
- replayability
- uncertainty discipline
- recovery planning
- boundary control
- actionability

Maximum per answer: 40.

## Validity Gates

The test is invalid if:

- the scorer has access to mode labels during scoring
- MCP-seasoned refs appear in blind scoring artifacts
- the hidden mapping is revealed before `blind_scores.json` is written
- the selected tasks reuse Proofs 018-020 tasks
- the final verdict exceeds the five-task local evidence boundary

The confirmed verdict requires the MCP-seasoned condition to win or tie for first on at least four of five tasks, exceed both controls in aggregate, avoid blind artifact leakage, and avoid overclaiming.
