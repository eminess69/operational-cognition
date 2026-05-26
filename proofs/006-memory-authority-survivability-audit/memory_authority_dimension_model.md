# Memory Authority Dimension Model

This model defines initial dimensions for evaluating whether remembered beliefs remain operationally authoritative through memory promotion, summary, replay, recovery, and reconstruction. Each dimension is subject to public evidence validation.

Allowed claim levels: `observed`, `inferred`, `hypothesis`, `unresolved`.

## Memory authority retention

Definition: Whether a remembered belief preserves the authority status it had when created, such as user instruction, tool observation, documentation fact, assistant inference, or summary-derived claim.

Why it matters: A belief can survive as text while losing the reason it should or should not govern future action.

Public evidence surfaces: Memory documentation, event logs, conversation state, trajectory bundles, recall outputs, summaries, and condensed views.

Authority drift risks: Summaries or memory files may merge observations, user instructions, and assistant inferences without preserving their different authority levels.

Unresolved questions: Which artifacts preserve authority class, source refs, and action boundaries after memory promotion or replay?

Current claim level: unresolved.

## Stale-belief survivability

Definition: Whether beliefs that were once useful remain detectable as stale after later events, corrections, or changed conditions.

Why it matters: Long-lived memory can reintroduce old assumptions unless staleness and validity boundaries survive recall.

Public evidence surfaces: Memory files, memory search, recall actions, compaction summaries, restart flows, daily notes, and recovery reports.

Authority drift risks: A stale belief may become operationally active again if recalled without expiry, supersession, or freshness metadata.

Unresolved questions: Which public artifacts expose stale-belief markers or freshness checks, and which only expose remembered content?

Current claim level: unresolved.

## Supersession survivability

Definition: Whether a later correction, replacement decision, or updated fact remains linked to the earlier belief it supersedes.

Why it matters: Operational systems need to know which belief is current when older memory, summaries, and replay artifacts coexist.

Public evidence surfaces: Event order, timestamps, memory promotion records, summaries with omitted ranges, trajectory timelines, and conversation state.

Authority drift risks: Older beliefs may remain available after a newer correction if supersession links are omitted.

Unresolved questions: Which artifacts preserve supersession refs across condensation, compaction, memory promotion, and restart?

Current claim level: unresolved.

## Source-authority survivability

Definition: Whether source identity and precedence survive when beliefs are saved, summarized, recalled, or replayed.

Why it matters: User instructions, trusted documentation, tool observations, memory recalls, and assistant inferences should not carry identical operational authority.

Public evidence surfaces: Event source fields, conversation roles, memory documentation, recall surfaces, tool/action records, and summary metadata.

Authority drift risks: Source authority can blur when multiple sources are rendered as a single summary or memory note.

Unresolved questions: Which source distinctions remain recoverable after memory recall and history condensation?

Current claim level: inferred.

## Temporal validity survivability

Definition: Whether the time window during which a belief is valid remains available after memory promotion, summary, replay, or recovery.

Why it matters: Some remembered beliefs are valid only before a deadline, after approval, until a handoff, or within a specific session state.

Public evidence surfaces: Timestamps, event order, memory action boundaries, recovery records, daily notes, and trajectory timelines.

Authority drift risks: Time-bound instructions can become timeless statements when compressed or stored as durable memory.

Unresolved questions: Which artifacts preserve validity windows, expiry conditions, and safe-to-act timing?

Current claim level: inferred.

## Replay authority survivability

Definition: Whether replay artifacts preserve enough provenance to show which remembered beliefs were authoritative at the time of action.

Why it matters: Replay can preserve visible behavior while losing why a belief was treated as governing.

Public evidence surfaces: Trajectory bundles, browser/session replay, event logs, conversation state, runtime metadata, and public proof manifests.

Authority drift risks: Replay may show sequence without source authority, supersession state, omitted ranges, or memory promotion provenance.

Unresolved questions: Which replay surfaces distinguish visible replay from authority-preserving operational replay?

Current claim level: unresolved.

## Summary authority survivability

Definition: Whether a summary preserves the authority lineage of the beliefs it compresses.

Why it matters: Summaries can become the model-visible state, so their wording may govern future behavior even when omitted events carried caveats.

Public evidence surfaces: Compaction summaries, condenser events, forgotten event IDs, successor transcripts, condensed views, and summary prompts when public.

Authority drift risks: A summary may promote an inference, omit a caveat, or weaken a supersession boundary while remaining operationally useful.

Unresolved questions: Which summary artifacts retain source refs, omitted ranges, contradiction refs, and validity refs?

Current claim level: hypothesis.

## Memory recall authority survivability

Definition: Whether recalled memory is presented with enough context to determine its authority relative to the current task.

Why it matters: Recall can inject old knowledge into a new decision context, where authority may depend on source, freshness, and applicability.

Public evidence surfaces: Memory search, memory get, recall actions, conversation events, role placement, and issue reports about recall behavior.

Authority drift risks: Recalled content may appear as operational context without explicit authority class, freshness status, or supersession status.

Unresolved questions: Which recall surfaces distinguish durable fact, working note, inferred commitment, stale note, and user instruction?

Current claim level: unresolved.

## Contradiction-aware memory survivability

Definition: Whether memory preserves known conflicts, uncertainty, rejected alternatives, and unresolved questions attached to a belief.

Why it matters: A belief can remain useful while contested. Losing contestation can turn an unresolved belief into apparent truth.

Public evidence surfaces: Memory docs, contradiction or freshness tracking docs, event logs, summaries, omitted ranges, and public proof claim registers when available.

Authority drift risks: Memory may retain the most compact claim while dropping the contradiction or uncertainty that limits its authority.

Unresolved questions: Which artifacts preserve contradiction refs and uncertainty markers through promotion, recall, and replay?

Current claim level: unresolved.

## Operational truth authority survivability

Definition: Whether the system preserves the boundary between observed fact, tool output, source-backed claim, assistant inference, recalled belief, and unresolved question.

Why it matters: Operational truth degrades when remembered or replayed content can no longer be tied to its evidential basis.

Public evidence surfaces: Evidence manifests, event logs, trajectory bundles, memory provenance, summary metadata, conversation state, and replay artifacts.

Authority drift risks: Operationally convenient memory may become authoritative even when its evidence status is unknown, stale, inferred, or contradicted.

Unresolved questions: Which public artifacts are sufficient to reconstruct operational truth authority after compression and recovery?

Current claim level: unresolved.
