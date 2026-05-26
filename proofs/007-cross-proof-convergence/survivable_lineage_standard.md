# Survivable Lineage Standard

This is an implementation-neutral public standard inferred from Proofs 001-006. It defines the lineage fields needed for audit-grade operational replay. It is not a claim that any target system currently satisfies the standard.

Claim boundary: the need for the standard is `inferred`; complete validation of the field list is `unresolved`.

## Why lineage must survive compression

Compression can preserve a useful summary and recent context while changing the active model-visible context. Proof 003 supports the inference that task utility can survive while replay fidelity weakens unless omitted ranges, summaries, event IDs, tool/action refs, memory refs, authority refs, contradiction refs, and provenance survive.

Compression should therefore be treated as an evidence transformation. A compressed artifact is stronger when it can point back to the source ranges it replaced, the summary it produced, the event and timestamp boundaries around the transformation, and the state that was retained or omitted.

## Why replay must preserve more than visible sequence

Visible replay can show transcript turns, browser activity, event order, or trajectory timelines. Proof 004 supports the inference that this can support partial reconstruction, but causal replay requires lineage across memory, environment, tool results, recovery loops, intent, and provenance.

Replay is audit-grade only when it can answer both what happened and what operational state was available when it happened. A replay that omits memory recalls, tool result hashes, runtime config, omitted ranges, contradiction state, or authority metadata may remain useful for inspection while remaining insufficient for causal explanation.

## Why memory requires authority metadata

Memory can preserve content without preserving why that content should govern future action. Proof 006 defines the authority question: source authority, stale status, supersession state, temporal validity, contradiction state, and recall provenance must remain reconstructable.

Memory entries, recalls, summaries, and promoted beliefs should preserve enough metadata to distinguish user instruction, tool observation, documentation fact, assistant inference, memory-derived claim, summary-derived claim, stale belief, superseded belief, and unresolved question.

## Why contradiction must remain reconstructable

Proof 005 defines contradiction survivability as a replay requirement. Compression, replay, and memory can preserve a coherent narrative while dropping conflicts, caveats, rejected alternatives, uncertainty markers, stale assumptions, or temporal conflicts.

Contradiction lineage should preserve where a conflict entered, which sources supported each side, whether it was resolved or superseded, and which later action depended on it. Without contradiction refs, replay can overstate certainty.

## Why recovery and environment state matter

Long-horizon outcomes can depend on retries, fallbacks, restarts, resumptions, cleanup, context-overflow handling, workspace state, runtime configuration, filesystem state, container state, browser state, dependencies, and external services.

Proofs 001-004 repeatedly identify environment and recovery state as relevant but incompletely reconstructed by visible replay alone. Recovery and environment refs are therefore required fields for causal replay adequacy, even when their complete capture remains unresolved.

## Minimum lineage fields

The minimum survivable lineage record should preserve:

- source refs
- event IDs
- timestamps
- omitted-range refs
- summary refs
- tool/action refs
- tool result refs or hashes
- memory write refs
- memory recall refs
- supersession refs
- contradiction refs
- authority refs
- temporal validity refs
- environment refs
- recovery-loop refs
- provenance hashes

## Field interpretation

`source refs` identify the public source or artifact that supports a claim, observation, memory, summary, or replay segment.

`event IDs` identify the events that carried state changes, actions, observations, summaries, recoveries, memory operations, or replay boundaries.

`timestamps` preserve ordering, before/after boundaries, validity windows, recovery timing, and summary insertion points.

`omitted-range refs` preserve links to transcript, event, or tool-result ranges removed by compression, condensation, truncation, redaction, or summarization.

`summary refs` identify the summary artifact, its source range, its creation event, and the retained head/tail or surrounding context.

`tool/action refs` identify action calls, tool calls, browser actions, commands, observations, and schemas relevant to a later state.

`tool result refs or hashes` preserve result identity, content hashes, truncation status, redaction status, error metadata, and source provenance.

`memory write refs` identify when memory was written, by what source context, with what authority, and with what validity or uncertainty boundary.

`memory recall refs` identify recall query, returned result, ranking or selection boundary if public, truncation, insertion point, and authority status.

`supersession refs` link older beliefs, instructions, assumptions, or summaries to later corrections or replacements.

`contradiction refs` preserve conflicts, rejected alternatives, uncertainty, unresolved questions, and resolution status.

`authority refs` preserve whether content came from a user instruction, tool observation, documentation fact, assistant inference, memory recall, summary, or other source class.

`temporal validity refs` preserve expiry, safe-to-act timing, session scope, approval windows, and before/after relationships.

`environment refs` identify workspace snapshots, filesystem diffs, runtime images, container IDs, dependency versions, browser state, network or service state, and redaction boundaries where available.

`recovery-loop refs` identify retries, fallbacks, restarts, resumptions, aborts, cleanup actions, context-overflow handling, status transitions, and pre/post recovery state.

`provenance hashes` preserve artifact integrity, capture boundaries, source hashes, replay bundle identity, and public manifest linkage.

