# Minimum Operational Replay Bundle

This bundle defines the minimum candidate package required for operational replay adequacy. It is inferred from Proofs 001-006 and remains unvalidated until tested against a public replay fixture.

Visible replay alone is not enough for causal reconstruction. The bundle must preserve the public lineage needed to reconstruct what happened, what state was available, what was omitted, what was contradicted, what was authoritative, and what changed during recovery.

| Bundle item | Minimum content | Why it is required | Claim level |
| --- | --- | --- | --- |
| transcript | User, assistant, system-visible summaries, successor transcript boundaries, redaction or omission markers. | Provides visible task narrative and intent-bearing context. | inferred |
| event log | Event IDs, event types, timestamps, source fields, insertion points, state transitions, omitted-event refs. | Preserves ordering and typed state transitions beyond prose transcript. | inferred |
| tool/action log | Tool calls, action events, command or browser actions, observation IDs, schemas or schema refs, timestamps. | Reconstructs operational sequence and action/result pairing. | inferred |
| tool result hashes | Result refs or bodies where public, content hashes, truncation markers, redaction markers, error metadata, source refs. | Allows replay to distinguish actual tool evidence from summarized or omitted result content. | inferred |
| memory write/recall log | Memory write refs, triggering context, recall queries, recall result refs, insertion points, truncation and freshness status. | Preserves whether memory influenced later action and whether recall was current, stale, or superseded. | inferred |
| compressed context summary | Summary refs, source ranges, retained head/tail context, compaction or condensation event IDs, summary timestamps. | Links post-compression context to the raw ranges it replaced. | inferred |
| omitted-range references | Stable IDs, hashes, source refs, boundaries, redaction reasons, and recovery instructions for omitted transcript/event/tool ranges. | Makes compressed or redacted replay recoverable enough for audit. | inferred |
| contradiction/uncertainty refs | Conflicting claims, uncertainty markers, stale assumptions, rejected alternatives, unresolved questions, resolution status. | Prevents replay from flattening contested evidence into a clean narrative. | unresolved |
| source authority refs | Source class, source priority, user/tool/memory/summary/inference distinctions, authority changes over time. | Preserves why a claim or instruction should govern later action. | inferred |
| temporal validity metadata | Timestamps, validity windows, expiry conditions, session scope, approval timing, supersession boundaries. | Distinguishes current truth from historical context. | inferred |
| environment/workspace snapshot refs | Workspace hashes, filesystem diffs, runtime image refs, container refs, dependency refs, browser/session refs, external-state refs where public. | Captures state outside transcript and events that can cause or constrain actions. | unresolved |
| runtime config | Model or provider refs where public, tool policy, sandbox mode, plugin/skill list, approval policy, execution mode, resource limits. | Reconstructs available actions and operating constraints. | unresolved |
| recovery/retry trace | Retry events, fallback choices, context-overflow handling, restarts, resumptions, aborts, cleanup, pre/post recovery state links. | Explains continuation or divergence after failure, interruption, or context pressure. | unresolved |
| provenance manifest | Source hashes, artifact hashes, capture time, retrieval method, redaction policy, omitted artifact list, public/private boundary statement. | Establishes integrity and scope of the replay bundle itself. | inferred |
| public lineage summary | Human-readable summary of the replay bundle, claim levels, known gaps, and private-boundary exclusions. | Keeps public audit consumers from overstating what the replay can support. | inferred |

## Adequacy rule

A replay bundle is operationally adequate only for the questions its lineage can answer. A bundle can be adequate for visible sequence review while inadequate for memory influence, authority propagation, contradiction survival, recovery-loop explanation, environment reconstruction, or causal replay.

## Minimum acceptance criteria

- Every observed or inferred claim derived from the bundle has source refs.
- Every summary has source-range refs or explicit omitted-range refs.
- Every tool/action decision has event refs and tool result refs or hashes where tool output shaped later action.
- Every memory-derived claim has memory write or recall refs plus source authority and temporal validity metadata.
- Every contradiction or uncertainty that affects action remains linked to source refs and resolution status.
- Every recovery transition has pre/post state refs or is marked unresolved.
- Every environment dependency has a snapshot ref, config ref, hash, or explicit unresolved marker.
- Every public replay package includes a provenance manifest and public lineage summary.

## Current limitation

This bundle is a candidate standard. Proof 007 does not show that the bundle is sufficient in practice, and it does not claim that current target-system artifacts satisfy it. The next validation step is to build or collect a public fixture and test replay from visible sequence alone against replay from the full lineage bundle.

