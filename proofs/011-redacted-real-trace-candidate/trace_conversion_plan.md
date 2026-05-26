# Trace Conversion Plan

## Goal

Convert a safe public or redacted-real trace into the survivable-lineage fixture structure.

## Input Requirements

The candidate must provide enough public-safe evidence to identify:

- transcript turns or equivalent user/agent messages
- event order and event identifiers
- tool or action attempts
- tool result references or result manifests
- memory writes, recalls, or explicit absence of memory use
- compression, summary, or context-boundary events
- omitted ranges and their recoverable references
- contradictions, corrections, or decision reversals
- source authority references
- temporal validity metadata
- environment references
- runtime configuration
- recovery or retry transitions
- provenance for every converted artifact
- public lineage summary explaining scope and limits

## Conversion Mapping

| Candidate trace field | Fixture field | Conversion notes |
| --- | --- | --- |
| Conversation messages, issue comments, replay transcript, or agent turns | `transcript.jsonl` | Assign stable `T-` IDs and link each visible turn to an event where possible. |
| Ordered event stream, run log, CI chronology, or trajectory events | `events.jsonl` | Assign stable `E-` IDs and preserve ordering without adding inferred hidden steps. |
| Commands, tool calls, edits, or agent actions | `tool_actions.jsonl` | Assign stable `A-` IDs and link to events and results. |
| Tool outputs, CI result excerpts, public log refs, or artifact handles | `tool_results_manifest.json` | Assign stable `TR-` IDs; store references, summaries, hashes, and public source locations rather than unsafe raw material. |
| Memory writes, recalls, saved notes, or durable task state | `memory_log.jsonl` | Assign stable `ML-` and `MEM-` IDs. If memory is absent, do not infer it. |
| Summaries, context compression, rollups, or handoff notes | `compressed_context_summary.json` | Assign stable `S-` IDs and record the source range and retained references. |
| Gaps, elisions, omitted logs, or unavailable trace segments | `omitted_ranges.json` | Assign stable `O-` IDs and record what is unknown without strengthening the claim. |
| Corrections, contradicted observations, failed assumptions, or revised decisions | `contradiction_refs.json` | Assign stable `C-` IDs and cite the evidence that opened and resolved each contradiction. |
| Documentation, public source refs, maintainer comments, runtime facts, or authoritative artifacts | `authority_refs.json` | Assign stable `AUTH-` IDs and state the authority type and limits. |
| Dates, version windows, validity intervals, or stale/fresh evidence markers | `temporal_validity.json` | Assign stable `TV-` IDs and use exact dates or event-bounded validity where possible. |
| Runtime environment, repository state, CI runner, model/tool version, or platform facts | `environment_snapshot_manifest.json` | Assign stable `ENV-` IDs and include hashes or public refs when safe. |
| Replay parameters, model/tool settings, fixture version, or execution flags | `runtime_config.json` | Record only public-safe config needed for replay. |
| Retry, fallback, recovery, rollback, or alternate path after failure | `recovery_trace.jsonl` | Assign stable `R-` IDs and link to trigger and follow-up actions. |
| Artifact hashes, source refs, conversion notes, and redaction attestations | `provenance_manifest.json` | Include hashes for converted public artifacts and state the source boundary. |
| Human-readable lineage boundary and limitations | `public_lineage_summary.md` | Explain what the candidate can and cannot support. |

## Fail-Closed Criteria

Reject the candidate if any of the following are true:

- credentials are present
- private data is present
- private substrate internals are present
- target-system private internals are present
- lineage is insufficient for the required fixture fields
- provenance cannot be established
- visible-only replay cannot be distinguished from full-lineage replay
- redaction would convert unknown evidence into stronger claims
- the candidate depends on attack framing or target-system vulnerability claims

## Execution Gate

Conversion may prepare fixture-shaped artifacts, but replay execution is allowed only after `candidate_manifest.json` reports `candidate_status` as `eligible`, `redaction_complete` as `true`, all eligibility fields as `true`, and `decision.eligible_for_execution` as `true`.
