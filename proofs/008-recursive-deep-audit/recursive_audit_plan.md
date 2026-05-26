# Recursive Audit Plan

## Purpose

Proof 008 recursively audits Proofs 001-007 to pressure-test the corpus without creating new doctrine beyond existing proof artifacts. The audit is bounded to public proof outputs, sanitized MCP lineage hashes, and explicit unresolved markers. Evidence basis: `docs/PROOF_STANDARD.md`, `docs/PUBLIC_PRIVATE_BOUNDARY.md`, and `proofs/007-cross-proof-convergence/convergence_analysis.md`.

## Audit Inputs

| Input | Role in Proof 008 | Evidence basis |
| --- | --- | --- |
| Proof 001 | Continuity pressure signals and replayability boundary. | `proofs/001-agent-continuity-audit/continuity_signals.md`; `proofs/001-agent-continuity-audit/replayability_plan.md` |
| Proof 002 | Replay dimensions and gap taxonomy. | `proofs/002-replayability-gap-audit/replay_dimension_model.md`; `proofs/002-replayability-gap-audit/replay_gap_taxonomy.md` |
| Proof 003 | Compression utility versus replay-fidelity boundary. | `proofs/003-continuity-compression-audit/analysis_v0_1.md`; `proofs/003-continuity-compression-audit/claim_register.json` |
| Proof 004 | Causal reconstruction requirements. | `proofs/004-operational-failure-reconstruction/analysis_v0_1.md`; `proofs/004-operational-failure-reconstruction/claim_register.json` |
| Proof 005 | Contradiction and uncertainty survivability requirements. | `proofs/005-contradiction-dimension-model.md`; `proofs/005-contradiction-survivability-audit/contradiction_replayability_matrix.md` |
| Proof 006 | Memory authority and stale-belief survivability requirements. | `proofs/006-memory-authority-survivability-audit/memory_authority_dimension_model.md`; `proofs/006-memory-authority-survivability-audit/belief_replayability_matrix.md` |
| Proof 007 | Cross-proof synthesis and candidate minimum replay bundle. | `proofs/007-cross-proof-convergence/cross_proof_claim_register.json`; `proofs/007-cross-proof-convergence/minimum_operational_replay_bundle.md` |

## Bounded Recursion Passes

| Pass | MCP task | Public use | Boundary |
| --- | --- | --- | --- |
| Synthesis | Synthesize strongest cross-proof operational requirements. | Advisory pressure check for recurring requirements. | Claims must still cite public proof artifacts. |
| Adversarial | Find overclaims, weak claims, missing evidence, and unsupported convergence. | Advisory pressure check for claim downgrades and unresolved clusters. | Missing evidence cannot become a target-system defect claim. |
| Validation | Design the minimum public fixture needed to validate survivable lineage. | Advisory pressure check for fixture completeness. | The fixture remains a validation plan, not proof of sufficiency. |

Evidence basis for bounded MCP handling: `docs/PROOF_STANDARD.md`; `recursive_consultation_log.md`.

## Claim-Level Rules

- Observed claims in Proof 008 describe repeated corpus patterns, not new target-system behavior. Evidence basis: `proofs/007-cross-proof-convergence/cross_proof_claim_register.json` claim `CPC-002`.
- Inferred claims in Proof 008 must remain conservative syntheses from Proofs 001-007. Evidence basis: `proofs/003-continuity-compression-audit/claim_register.json` claim `C-011`; `proofs/004-operational-failure-reconstruction/claim_register.json` claim `C-008`; `proofs/007-cross-proof-convergence/cross_proof_claim_register.json` claim `CPC-009`.
- Hypothesis claims in Proof 008 must identify the missing fixture or artifact needed for validation. Evidence basis: `proofs/007-cross-proof-convergence/cross_proof_claim_register.json` claim `CPC-010`.
- Unresolved claims in Proof 008 stay unresolved unless a cited public proof artifact already resolves them. Evidence basis: `proofs/003-continuity-compression-audit/claim_register.json` claims `C-005` and `C-006`; `proofs/004-operational-failure-reconstruction/claim_register.json` claim `C-007`; `proofs/007-cross-proof-convergence/cross_proof_claim_register.json` claim `CPC-011`.

## Audit Outputs

The audit outputs are scoped to convergence pressure, contradiction clusters, weak claim boundaries, evidence gaps, fixture design, and the survivable-lineage validation plan. Evidence basis: `proofs/007-cross-proof-convergence/unresolved_convergence_questions.md`; `proofs/007-cross-proof-convergence/minimum_operational_replay_bundle.md`.
