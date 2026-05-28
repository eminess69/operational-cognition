# Learning Task Selection

## Selected Task

Design a validator for replay artifact completeness for a one-proof learning replay test.

The validator must prove only that the named proof bundle is internally complete enough to audit a bounded learning replay. It must not judge model quality outside the artifact bundle, and it must not rely on private data or external network state.

## Why This Is A New Domain

This task is not another MCP repair or proof-gate repair trace. The work product is an artifact-completeness validator for a novel learning/replay proof bundle:

- It validates that a compact operational learning record exists.
- It validates that a repeat replay request and response are present.
- It validates that lineage and runtime hashes survived through the consult path.
- It validates that the repeat request did not paste the original solution.
- It validates that reconstruction and verdict artifacts are complete and bounded.

Prior Proofs 009-014 focused on fixtures, real-trace replay, or independent real-trace replication. This proof uses those constraints as boundary context but selects a separate operational task: validating a learning replay proof bundle.

## Rejection Checks

- Already solved in Proofs 009-014: rejected. Those proofs include validators, but not this proof-specific replay-learning completeness rule.
- No meaningful learned rule: rejected. The new rule is a compact, replayable validation pattern.
- No replay/audit comparison possible: rejected. The same pattern can be replayed against a changed surface variant, then audited dimension by dimension.
- Requires private data: rejected. The proof uses only public-safe repository artifacts and runtime hashes.
- Requires external web access: rejected. The task is local-only.

## Selected Learning Pattern

Use a three-layer replay validator:

1. **Lineage gate:** verify pond-backed consult status and runtime hashes before accepting the proof bundle.
2. **Separation gate:** prove the repeat replay request references the learning artifact without pasting the full first-pass solution.
3. **Audit gate:** require reconstruction answers, final verdict discipline, and overclaim screening before declaring any replay advantage.

The pattern is intentionally narrow. It applies to a named proof bundle with public-safe artifacts, not to general claims about systems or models.
