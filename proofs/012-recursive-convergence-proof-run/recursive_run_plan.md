# Recursive Run Plan

## Method

Proof 012 runs seven bounded recursive passes. Each pass calls the local Inside Voice MCP endpoint, records request and response hashes, then Codex reconciles the pass against public proof artifacts only.

The MCP adapter status is `placeholder`, so MCP output is not evidence for target-system behavior. It can only provide bounded advisory pressure. Public conclusions stand on the existing proof corpus and Proof 012 reconciliation.

## Public Evidence Base

- `proofs/003-continuity-compression-audit/claim_register.json`
- `proofs/004-operational-failure-reconstruction/claim_register.json`
- `proofs/005-contradiction-survivability-audit/contradiction_replayability_matrix.md`
- `proofs/006-memory-authority-survivability-audit/belief_replayability_matrix.md`
- `proofs/007-cross-proof-convergence/convergence_analysis.md`
- `proofs/007-cross-proof-convergence/cross_proof_claim_register.json`
- `proofs/008-recursive-deep-audit/convergence_pressure_report.md`
- `proofs/008-recursive-deep-audit/weakest_claims_report.md`
- `proofs/008-recursive-deep-audit/contradiction_cluster_report.md`
- `proofs/010-fixture-execution/visible_replay_results.json`
- `proofs/010-fixture-execution/full_lineage_replay_results.json`
- `proofs/010-fixture-execution/validation_verdict.json`
- `proofs/011-redacted-real-trace-candidate/unresolved_requirements.md`

## Passes

| Depth | Pass | Question | Reconciliation rule |
| --- | --- | --- | --- |
| 1 | synthesis | What are the strongest corpus-level operational laws? | Keep only laws supported by public proof refs. |
| 2 | adversarial | Which laws are overclaimed, unsupported, circular, or too broad? | Downgrade or bound claims with scope leakage. |
| 3 | contradiction | Which proof artifacts disagree, create unresolved tension, or weaken convergence? | Preserve tensions instead of resolving them rhetorically. |
| 4 | evidence sufficiency | Which claims are evidence-backed, inferred, hypothesis-level, or unresolved? | Separate fixture evidence, corpus inference, global claims, and target-system claims. |
| 5 | fixture validation | Does Proof 010 actually validate survivable lineage, or only a synthetic fixture? | Keep Proof 010 fixture-scoped. |
| 6 | alternative explanation | Could the convergence be caused by prompt framing, proof design, or taxonomy reuse rather than real operational necessity? | Treat design-induced convergence as a live alternative until real/public trace validation. |
| 7 | final convergence | After downgrades and alternative explanations, what claim still survives? | Publish only the strongest safe claim. |

## Stop Rule Applied

The run stopped after the required seven passes. Optional recursion was not continued because the final passes did not change claim levels, the MCP adapter remained placeholder, and further placeholder consultation would not add public evidence.
