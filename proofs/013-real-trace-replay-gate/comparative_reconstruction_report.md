# Comparative Reconstruction Report

## Method

Mode A used only `fixture/transcript.jsonl` and visible event ordering from `fixture/events.jsonl`.

Mode B used the complete fixture, including tool results, authority refs, omitted-range refs, temporal validity, environment refs, recovery trace, and public-safe pond-backed Inside Voice hashes.

## Comparison

| Probe | Visible-only | Full-lineage | Improvement | Evidence refs | Remaining uncertainty |
| --- | --- | --- | --- | --- | --- |
| P-001 tool-dependent action reconstruction | partially_reconstructed | reconstructed | yes | `A-008`, `TR-009`, `ENV-003` | None for local action chain. |
| P-002 contradiction resolution reconstruction | partially_reconstructed | reconstructed | yes | `C-001`, `C-002`, `C-003`, `C-004` | None for recorded corrections. |
| P-003 memory authority reconstruction | unresolved | reconstructed | yes | `MEM-002`, `MEM-003`, `AUTH-PROOF011-001`, `AUTH-RUNTIME-001` | Does not infer hidden memory outside fixture refs. |
| P-004 omitted-range recovery | partially_reconstructed | reconstructed | yes | `O-001`, `O-002`, `O-003`, `R-001` | Raw hidden reasoning remains excluded by design. |
| P-005 environment dependency reconstruction | unresolved | reconstructed | yes | `ENV-002`, `ENV-003`, `TR-007`, `TR-008` | Does not generalize to other runtime deployments. |
| P-006 recovery-loop reconstruction | partially_reconstructed | reconstructed | yes | `R-001`, `R-002`, `R-003`, `R-004`, `R-005` | None for recorded retry sequence. |
| P-007 authority lineage reconstruction | unresolved | reconstructed | yes | `AUTH-USER-005`, `AUTH-PROOF010-001`, `AUTH-PROOF011-001`, `AUTH-RUNTIME-001` | Does not recover authority outside public-safe refs. |
| P-008 temporal validity reconstruction | partially_reconstructed | reconstructed | yes | `TV-001`, `TV-002`, `TV-003`, `TV-004` | Future runtime changes may supersede these refs. |

## What Full-Lineage Reconstructed

Full-lineage replay reconstructed the commit-dependent MCP server environment, the candidate-risk gate action/result chain, the contradiction/correction sequence, the user/proof/runtime authority split, omitted-range recoverability, and the retry loop from fail-closed states to the passing gate.

Visible-only replay could infer that corrections and retries happened, but could not verify runtime hashes, environment commits, exact gate outcomes, authority refs, or omitted-range recovery refs.

## What Remained Unresolved

Within this fixture, no required probe remained unresolved under full-lineage replay. Remaining unresolved questions are outside this single trace:

- whether the same effect appears on additional independent real traces
- whether other runtime deployments produce the same candidate-risk gate behavior
- whether public-only traces with less tool lineage can support the same replay split

## Interpretation

Survivable lineage materially improved replay adequacy in this single redacted-real trace because all eight probes moved from partial or unresolved in visible-only replay to reconstructed in full-lineage replay.

Contradiction lineage mattered for resolving caller error, compaction preservation, request narrowing, and safe claim-boundary detection. Authority lineage mattered for separating user instructions, Proof 010/011 boundaries, and pond-backed runtime evidence. Recovery lineage mattered for reconstructing the fail-closed/retry loop. Environment lineage mattered for tying the successful gate to Belief Ledger commit `1c89d45` and the local MCP endpoint.

This report makes no global superiority claim and no target-system defect claim.

Proof 010 remains a synthetic-only fixture validation boundary. Proof 011 remains the candidate-selection gate for public or redacted-real traces.
