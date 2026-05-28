# Repeat Solution

## Repeat Variant

Design a deterministic validator for fixture-minimization artifact completeness. The surface details changed from a learning replay proof bundle to a fixture minimization bundle, but the replayed operational pattern is the same:

- verify lineage first
- prove separation from the source artifact
- require audit answers and a scoped verdict

## Recalled Evidence Used

The repeat replay response preserved these usable refs:

- `request_visible_ref:proofs/015-novel-learning-replay-test/inside_voice_learning_record.json`
- `request_visible_ref:proofs/015-novel-learning-replay-test/inside_voice_learning_consult_response.json`
- `repeat_replay_response.json#lineage.runtime.runtime_response_hash`
- `repeat_replay_response.json#lineage.runtime.corpus_hash`
- `repeat_replay_response.json#pressure_rankings`
- `repeat_replay_response.json#claim_boundary_audit`

The response also surfaced pressure and uncertainty signals. The repeat validator should therefore keep observed/inferred/unresolved labels visible and avoid treating recall as implementation authority.

## Fixture-Minimization Validator Structure

### 1. Lineage Gate

Require public-safe lineage before accepting the minimization bundle:

- `adapter_status == "pond_backed"`
- `contribution_grade` is `bounded` or `strong`
- `runtime_stage_report_ref` is present
- `pressure_rankings` is non-empty
- `gate_failures == []`
- `lineage.runtime.runtime_response_hash` is a SHA-256 value
- `lineage.runtime.corpus_hash` is a SHA-256 value

### 2. Separation Gate

Require proof that the minimized fixture is not just the original fixture renamed:

- an `original_fixture_hash`
- a `minimized_fixture_hash`
- a `forbidden_original_fixture_hash` in the replay request or minimization manifest
- a deterministic comparison report showing which elements were removed
- a leakage check that rejects copied raw local-only details

### 3. Audit Gate

Require explicit audit answers before the final verdict:

- Was the source fixture preserved by hash?
- Were minimization rules recorded?
- Were removed elements justified?
- Did replay still reconstruct the target behavior?
- Were boundary warnings preserved?
- Did the final verdict stay scoped to the fixture bundle?

Each answer should use the same bounded score set: `reconstructed`, `partially_reconstructed`, or `unresolved`.

## Verdict Discipline

The validator may report only fixture-minimization bundle completeness. It should not report broad model quality or hidden-state claims. If lineage, separation, or audit answers are missing, the bundle is invalid rather than partially accepted by narrative explanation.

## Replay Benefit Observed In This Repeat

The repeat solution was shorter and more directly structured than the first pass because it reused the three-layer pattern from `proof_015_learning_001`. The observed benefit is limited to this proof run: the repeated task had clearer gates, explicit separation checks, and a ready-made reconstruction score set.
