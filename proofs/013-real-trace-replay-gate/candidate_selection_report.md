# Candidate Selection Report

## Selected Candidate

- candidate id: `proof_013_redacted_real_gate_repair_trace`
- candidate type: `redacted_real`
- source: local Proof 013 Codex/Inside Voice operational trace
- status: `eligible`

The candidate was selected because it contains a visible transcript, stable event ordering, tool/action evidence, contradiction/correction events, recovery/retry behavior, environment/runtime dependency, and enough lineage to separate visible-only replay from full-lineage replay.

## Why This Candidate Was Selected

The trace records a real operational sequence rather than a synthetic scenario:

- malformed `/consult` request corrected by user instruction
- Belief Ledger server restart dependency verified by commit hash
- claim-boundary false positive corrected by commit `1c89d45`
- candidate-risk gate response with `adapter_status: pond_backed`, `contribution_grade: strong`, empty `gate_failures`, deterministic `runtime_response_hash`, and deterministic `corpus_hash`
- tool evidence for `git`, `curl`, server start, response validation, and fail-closed recovery

## Rejected Candidates

| Candidate | Reason rejected |
| --- | --- |
| public GitHub issue or PR | Public availability alone did not provide the memory, omitted-range, environment, and recovery lineage needed for a fair full-lineage replay comparison without adding synthetic lineage. |
| prior Proof 010 fixture | Rejected because Proof 010 is explicitly synthetic-only and cannot satisfy the real-trace requirement. |
| raw hidden runtime internals | Rejected because private substrate internals are outside the public/private boundary. |
| unresolved failed hard-gate attempts alone | Rejected because the sequence was not replay-eligible until the `1c89d45` candidate-risk gate passed. |

## Lineage Coverage Matrix

| Requirement | Coverage | Evidence refs |
| --- | --- | --- |
| transcript or visible conversation | yes | `fixture/transcript.jsonl` |
| event ordering | yes | `fixture/events.jsonl` |
| tool/action evidence | yes | `fixture/tool_actions.jsonl`, `fixture/tool_results_manifest.json` |
| contradiction or correction | yes | `fixture/contradiction_refs.json` |
| recovery/retry behavior | yes | `fixture/recovery_trace.jsonl` |
| environment/runtime dependency | yes | `fixture/environment_snapshot_manifest.json`, `fixture/runtime_config.json` |
| memory/authority refs | yes | `fixture/memory_log.jsonl`, `fixture/authority_refs.json` |
| omitted-range refs | yes | `fixture/omitted_ranges.json` |
| temporal validity | yes | `fixture/temporal_validity.json` |
| provenance | yes | `fixture/provenance_manifest.json` |

## Provenance Status

Provenance is established for a redacted-real local trace. The source is the observed Proof 013 operational sequence and public-safe command/response summaries. No credentials, hidden chain-of-thought, private substrate internals, or target-system private internals are included.

## Replay Suitability

Replay modes can be separated. Visible-only replay receives only transcript and visible ordering. Full-lineage replay receives the fixture artifacts and Inside Voice runtime refs. This separation is sufficient for the eight required reconstruction probes.
