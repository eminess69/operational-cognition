# Initial Codex Solution

## Problem

Design a deterministic validator for a proof bundle that tests whether one operational learning record can be preserved with lineage and replayed against a repeat variant.

## Solution

The validator should treat the proof directory as the only authority. It should not infer success from narrative text alone. It should require a complete artifact set, verify that Inside Voice returned pond-backed lineage, confirm replay separation, and reject overclaim wording.

## Required Artifact Checks

The proof directory must include:

- `README.md`
- `learning_task_selection.md`
- `initial_codex_solution.md`
- `inside_voice_learning_record.json`
- `repeat_replay_request.json`
- `repeat_replay_response.json`
- `repeat_solution.md`
- `comparative_learning_audit.md`
- `replay_reconstruction_results.json`
- `claim_register.json`
- `public_lineage_summary.md`
- `final_verdict.json`
- `proof_manifest.json`

The implementation may include additional consult artifacts, but the validator must not require private logs.

## Lineage Gate

The validator should inspect the recorded consult responses and require:

- `adapter_status == "pond_backed"`
- `contribution_grade` is `bounded` or `strong`
- `runtime_stage_report_ref` is non-empty
- `pressure_rankings` is a non-empty array
- `gate_failures == []`
- `lineage.runtime.runtime_response_hash` is a SHA-256 value
- `lineage.runtime.corpus_hash` is a SHA-256 value

If either the hard-gate response or repeat replay response is missing these fields, the proof is invalid.

## Separation Gate

The repeat request may include a learning identifier, a short task variant, constraints, desired artifacts, and file references. It must not paste the full first-pass solution. The validator should enforce this with two checks:

- a direct leak marker check using a `forbidden_original_solution_hash` value in the repeat request
- a length and phrase check that rejects large copied sections from `initial_codex_solution.md`

This avoids treating a copied solution as replay.

## Audit Gate

The reconstruction result must answer each required question using only:

- `reconstructed`
- `partially_reconstructed`
- `unresolved`

The final verdict must be one of the allowed proof verdicts. A positive replay advantage requires:

- the learned pattern was recalled
- source references were preserved
- the repeat solution used the recalled pattern
- at least five audit dimensions were improved or remained strong
- no overclaim flags were set

## Boundary Rules

The validator should reject unsupported claims using text scanning over public proof artifacts. It should block positive wording for global superiority, general intelligence, consciousness, or black-box-solved claims while allowing negated or disallowed-claim registers.

## Output

On success the CLI prints:

```text
NOVEL_LEARNING_REPLAY_VALID
```

On failure it prints:

```text
NOVEL_LEARNING_REPLAY_INVALID
```

followed by specific errors on stderr.

## Minimal Repeat Variant

A repeat variant can swap the surface task from "validator for replay artifact completeness" to "validator for fixture minimization artifact completeness" while keeping the same three-layer pattern:

- lineage gate
- separation gate
- audit gate

The repeat solution should be shorter and more structured if the replayed guidance is useful.
