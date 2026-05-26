# Survivable Lineage Validation Plan

## Validation Question

Can a public replay fixture show that full survivable-lineage replay reconstructs operational claims that visible-only replay cannot reconstruct? Claim level: `hypothesis` until executed. Evidence basis: `proofs/007-cross-proof-convergence/minimum_operational_replay_bundle.md`; `proofs/007-cross-proof-convergence/unresolved_convergence_questions.md`.

## Minimum Fixture

The minimum fixture is a public, synthetic or redacted-real session bundle with one bounded task, one tool-dependent decision, one explicit contradiction or correction, one memory write and recall, one compression or summary boundary, one environment dependency, and one recovery or retry transition. This shape is required because the corpus repeatedly marks visible replay, tool results, memory, compression, contradiction, authority, environment, runtime, recovery, and provenance as replay dimensions. Evidence basis: `proofs/002-replayability-gap-audit/replay_dimension_model.md`; `proofs/003-continuity-compression-audit/claim_register.json` `C-011`; `proofs/004-operational-failure-reconstruction/claim_register.json` `C-008`; `proofs/005-contradiction-survivability-audit/contradiction_replayability_matrix.md`; `proofs/006-memory-authority-survivability-audit/belief_replayability_matrix.md`; `proofs/007-cross-proof-convergence/minimum_operational_replay_bundle.md`.

## Required Fixture Artifacts

| Artifact | Minimum content | Validation role | Evidence basis |
| --- | --- | --- | --- |
| Transcript | Ordered user, assistant, system-visible summary, redaction, and omission markers. | Tests visible narrative reconstruction. | `proofs/002-replayability-gap-audit/replay_dimension_model.md`; `proofs/007-cross-proof-convergence/minimum_operational_replay_bundle.md` |
| Event log | Stable event IDs, event types, timestamps, source fields, insertion points, and state transitions. | Tests typed ordering beyond prose transcript. | `proofs/003-continuity-compression-audit/claim_register.json` `C-004`; `proofs/004-operational-failure-reconstruction/claim_register.json` `C-002`, `C-006` |
| Tool/action log | Tool calls, action events, command or browser actions, schemas or schema refs, observation IDs, and timestamps. | Tests action/result pairing. | `proofs/003-continuity-compression-audit/claim_register.json` `C-002`; `proofs/004-operational-failure-reconstruction/claim_register.json` `C-003` |
| Tool result hashes | Result refs or public bodies, content hashes, truncation markers, redaction markers, error metadata, and source refs. | Tests whether later claims can be tied to actual tool evidence. | `proofs/002-replayability-gap-audit/replayability_matrix.md`; `proofs/004-operational-failure-reconstruction/claim_register.json` `C-008` |
| Memory write/recall log | Write refs, triggering context, recall queries, recall result refs, insertion points, freshness, stale status, and supersession status. | Tests memory influence and authority reconstruction. | `proofs/004-operational-failure-reconstruction/claim_register.json` `C-004`; `proofs/006-memory-authority-survivability-audit/belief_replayability_matrix.md` |
| Compressed context summary | Summary refs, source ranges, retained head/tail context, compaction or condensation event IDs, and summary timestamps. | Tests compressed-context replay. | `proofs/003-continuity-compression-audit/claim_register.json` `C-001`, `C-006`, `C-011`; `proofs/007-cross-proof-convergence/survivable_lineage_standard.md` |
| Omitted-range refs | Stable IDs, source boundaries, hashes, redaction reasons, and recovery instructions for omitted transcript, event, or tool ranges. | Tests whether summary and redaction remain auditable. | `proofs/007-cross-proof-convergence/cross_proof_claim_register.json` `CPC-007`; `proofs/007-cross-proof-convergence/minimum_operational_replay_bundle.md` |
| Contradiction refs | Conflicting claims, source refs for each side, uncertainty markers, rejected alternatives, stale assumptions, resolution status, and dependent action refs. | Tests contradiction and uncertainty survivability. | `proofs/005-contradiction-dimension-model.md`; `proofs/005-contradiction-survivability-audit/contradiction_replayability_matrix.md`; `proofs/007-cross-proof-convergence/cross_proof_claim_register.json` `CPC-005` |
| Authority refs | Source class, source priority, user/tool/memory/summary/inference distinction, authority changes, and supersession links. | Tests operational authority reconstruction. | `proofs/006-memory-authority-survivability-audit/memory_authority_dimension_model.md`; `proofs/007-cross-proof-convergence/cross_proof_claim_register.json` `CPC-006` |
| Temporal validity metadata | Timestamps, validity windows, expiry conditions, session scope, approval timing, and supersession boundaries. | Tests current truth versus historical context. | `proofs/005-contradiction-dimension-model.md`; `proofs/006-memory-authority-survivability-audit/memory_authority_dimension_model.md`; `proofs/007-cross-proof-convergence/recurring_motifs.json` `M-004` |
| Environment snapshot refs | Workspace hashes, filesystem diffs, dependency refs, browser/session refs, container or runtime image refs, and redaction boundaries. | Tests environment-dependent reconstruction. | `proofs/002-replayability-gap-audit/replay_dimension_model.md`; `proofs/004-operational-failure-reconstruction/claim_register.json` `C-005`; `proofs/007-cross-proof-convergence/cross_proof_claim_register.json` `CPC-008` |
| Runtime config | Model or provider refs where public, tool policy, sandbox mode, approval mode, plugin or skill list, execution mode, and resource limits. | Tests available-action and constraint reconstruction. | `proofs/002-replayability-gap-audit/replay_dimension_model.md`; `proofs/007-cross-proof-convergence/minimum_operational_replay_bundle.md` |
| Recovery/retry trace | Retry events, fallback choices, context-overflow handling, restarts, resumptions, aborts, cleanup, and pre/post recovery state links. | Tests recovery-loop causal reconstruction. | `proofs/003-continuity-compression-audit/claim_register.json` `C-009`; `proofs/004-operational-failure-reconstruction/claim_register.json` `C-009`; `proofs/007-cross-proof-convergence/cross_proof_claim_register.json` `CPC-008` |
| Provenance manifest | Source hashes, artifact hashes, capture time, retrieval method, redaction policy, omitted artifact list, and public/private boundary statement. | Tests replay-bundle integrity. | `proofs/001-agent-continuity-audit/replayability_plan.md`; `proofs/004-operational-failure-reconstruction/claim_register.json` `C-011`; `docs/PROOF_STANDARD.md` |
| Public lineage summary | Human-readable claim levels, known gaps, replay modes, private-boundary exclusions, and fixture hash summary. | Tests whether public readers can avoid overclaiming fixture results. | `docs/PROOF_STANDARD.md`; `proofs/007-cross-proof-convergence/minimum_operational_replay_bundle.md` |

## Replay Modes

Mode A is visible-only replay using transcript, visible browser or event sequence, and public narrative ordering. Mode A tests the corpus claim that visible replay is useful but not causally sufficient. Evidence basis: `proofs/002-replayability-gap-audit/replay_dimension_model.md`; `proofs/004-operational-failure-reconstruction/claim_register.json` `C-008`; `proofs/007-cross-proof-convergence/cross_proof_claim_register.json` `CPC-004`.

Mode B is full-lineage replay using every required fixture artifact above. Mode B tests whether source, event, tool, result, memory, summary, omission, contradiction, authority, temporal, environment, runtime, recovery, and provenance links improve claim reconstruction. Evidence basis: `proofs/007-cross-proof-convergence/minimum_operational_replay_bundle.md`; `proofs/007-cross-proof-convergence/survivable_lineage_standard.md`.

## Acceptance Criteria

The fixture supports moving from doctrine-level inference toward fixture-level proof only if Mode B reconstructs all required probe claims with explicit refs and Mode A fails or remains unresolved on at least memory influence, contradiction state, authority status, omitted-range recovery, environment dependency, or recovery-loop explanation. Evidence basis: `proofs/007-cross-proof-convergence/unresolved_convergence_questions.md`; `proofs/007-cross-proof-convergence/cross_proof_claim_register.json` `CPC-010`.

Each reconstructed claim must state `observed`, `inferred`, `hypothesis`, or `unresolved`, and every claim must cite fixture refs and source proof refs. Evidence basis: `docs/PROOF_STANDARD.md`; `proofs/003-continuity-compression-audit/claim_register.json`; `proofs/004-operational-failure-reconstruction/claim_register.json`.

The fixture validates only fixture-level adequacy. It does not prove universal sufficiency or target-system preservation. Evidence basis: `proofs/007-cross-proof-convergence/cross_proof_claim_register.json` `CPC-011`.

## Disproof Or Revision Criteria

If Mode B cannot reconstruct the contradiction, authority, memory, omitted-range, environment, runtime, recovery, or provenance probes, the candidate bundle is incomplete for that fixture. Evidence basis: `proofs/007-cross-proof-convergence/minimum_operational_replay_bundle.md`; `proofs/007-cross-proof-convergence/unresolved_convergence_questions.md`.

If Mode A reconstructs all probes with the same confidence as Mode B, the fixture does not validate the need for the full bundle; the scenario is too weak or the necessity claim must be narrowed. Evidence basis: `proofs/002-replayability-gap-audit/replay_dimension_model.md`; `proofs/007-cross-proof-convergence/cross_proof_claim_register.json` `CPC-004`, `CPC-010`.

If any artifact cannot be made public without violating the public/private boundary, that artifact must be replaced with a public hash/ref plus an explicit unresolved marker, and claims depending on undisclosed content must remain unresolved. Evidence basis: `docs/PUBLIC_PRIVATE_BOUNDARY.md`; `docs/PROOF_STANDARD.md`.

## Minimum Probe Set

1. Reconstruct why a tool-dependent action occurred from transcript alone and from full lineage. Evidence basis: `proofs/004-operational-failure-reconstruction/claim_register.json` `C-003`, `C-008`.
2. Reconstruct which contradiction was active at decision time and whether it was resolved or unresolved. Evidence basis: `proofs/005-contradiction-survivability-audit/contradiction_replayability_matrix.md`; `proofs/007-cross-proof-convergence/cross_proof_claim_register.json` `CPC-005`.
3. Reconstruct whether recalled memory was authoritative, stale, superseded, or merely historical. Evidence basis: `proofs/006-memory-authority-survivability-audit/belief_replayability_matrix.md`; `proofs/007-cross-proof-convergence/cross_proof_claim_register.json` `CPC-006`.
4. Reconstruct what compressed context omitted and which source ranges support the summary. Evidence basis: `proofs/003-continuity-compression-audit/claim_register.json` `C-006`, `C-011`; `proofs/007-cross-proof-convergence/cross_proof_claim_register.json` `CPC-007`.
5. Reconstruct which environment snapshot and runtime config constrained the action. Evidence basis: `proofs/002-replayability-gap-audit/replay_dimension_model.md`; `proofs/004-operational-failure-reconstruction/claim_register.json` `C-005`.
6. Reconstruct the retry or recovery path and its pre/post state. Evidence basis: `proofs/003-continuity-compression-audit/claim_register.json` `C-009`; `proofs/004-operational-failure-reconstruction/claim_register.json` `C-009`.

## Result Classification

`validated` is allowed only for fixture-scoped claims that pass Mode B with source refs, hashes, and public lineage. `inferred` remains appropriate for corpus-level survivable-lineage centrality. `hypothesis` remains appropriate for bundle sufficiency until at least one fixture passes. `unresolved` remains required for global target-system preservation. Evidence basis: `docs/PROOF_STANDARD.md`; `proofs/007-cross-proof-convergence/cross_proof_claim_register.json` `CPC-009`, `CPC-010`, and `CPC-011`.
