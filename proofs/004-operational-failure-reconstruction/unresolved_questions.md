# Unresolved Questions

## Evidence gaps

- Which public failed-session examples include transcript, event log, trajectory, browser replay, memory, environment, runtime, and recovery artifacts for the same run? Affected dimensions: transcript reconstruction, event reconstruction, tool/action reconstruction, memory reconstruction, environment reconstruction, causal reconstruction, recovery-loop reconstruction. Expected evidence: public replay bundle or public failed-session artifact set.
- Which public artifacts show before/after compaction or condensation state with stable links to the original range? Affected dimensions: transcript reconstruction, temporal reconstruction, replay provenance reconstruction. Expected evidence: original event range, summary or compacted view, omitted-range refs, and source hashes.
- Which public examples show actual exported artifacts rather than architecture-level documentation? Affected dimensions: all reconstruction dimensions. Expected evidence: bounded public exports with timestamps and source IDs.

## Replay gaps

- Can visible replay be linked to the exact model-visible context that preceded each action? Affected dimensions: transcript reconstruction, event reconstruction, causal reconstruction. Expected evidence: replay artifact plus model-visible context refs.
- Are browser replay events linked to agent actions, observations, and timestamps in the main event log? Affected dimensions: tool/action reconstruction, temporal reconstruction, replay provenance reconstruction. Expected evidence: browser recording IDs, event IDs, and synchronized timestamps.
- Are omitted ranges replayable through stable IDs, hashes, or source references? Affected dimensions: transcript reconstruction, temporal reconstruction, replay provenance reconstruction. Expected evidence: omitted-range refs and source-hash metadata.

## Memory reconstruction gaps

- Which artifacts record memory writes with source context, timestamps, and authorizing event IDs? Affected dimensions: memory reconstruction, intent reconstruction, causal reconstruction. Expected evidence: memory write logs, source event refs, and source hashes.
- Which artifacts record memory recall queries, recall result IDs, returned content, truncation, and ranking or selection boundaries? Affected dimensions: memory reconstruction, causal reconstruction. Expected evidence: recall traces and returned-result provenance.
- Can an auditor distinguish durable memory, recalled memory, summarized memory, and absent memory in replay artifacts? Affected dimensions: memory reconstruction, replay provenance reconstruction. Expected evidence: memory state snapshots and recall/write lineage.

## Environment reconstruction gaps

- Which artifacts preserve workspace hashes, filesystem diffs, dependency versions, container images, browser session state, and external-service references? Affected dimensions: environment reconstruction, causal reconstruction. Expected evidence: environment snapshots, runtime config refs, and dependency hashes.
- Can workspace or browser state be tied to the action that observed or modified it? Affected dimensions: environment reconstruction, tool/action reconstruction, temporal reconstruction. Expected evidence: action IDs, observation IDs, filesystem/browser refs, and timestamps.
- Which environment state is intentionally omitted, redacted, or left outside replay artifacts? Affected dimensions: environment reconstruction, replay provenance reconstruction. Expected evidence: redaction policy, omission markers, and provenance notes.

## Causal lineage gaps

- Can a later action be traced back through transcript context, event IDs, tool results, memory recalls, environment state, runtime config, and recovery events? Affected dimensions: causal reconstruction, replay provenance reconstruction. Expected evidence: joined public lineage bundle.
- Are tool result bodies, hashes, truncation markers, redaction reasons, and tool schema versions available when tool outputs shape later action? Affected dimensions: tool/action reconstruction, causal reconstruction. Expected evidence: tool result refs and schema/config metadata.
- Are rejected alternatives, stale assumptions, corrections, and uncertainty markers retained rather than flattened into a summary? Affected dimensions: contradiction reconstruction, causal reconstruction. Expected evidence: contradiction refs, source authority, and before/after summaries.

## Recovery-loop gaps

- Which artifacts preserve retries, fallback choices, context-overflow handling, aborts, cleanup, restarts, resumptions, and status transitions? Affected dimensions: recovery-loop reconstruction, temporal reconstruction. Expected evidence: recovery event traces, error refs, and state transition logs.
- Can the state before a restart or retry be linked to the state after recovery? Affected dimensions: recovery-loop reconstruction, environment reconstruction, memory reconstruction. Expected evidence: pre/post snapshots and recovery refs.
- Are recovery events represented as first-class replay events or only inferred from surrounding logs? Affected dimensions: event reconstruction, recovery-loop reconstruction, replay provenance reconstruction. Expected evidence: event schemas and public replay examples.

## Intent reconstruction gaps

- Which artifacts preserve user intent, constraints, approvals, prohibitions, authority, timing, and scope changes across summaries and memory recalls? Affected dimensions: intent reconstruction, transcript reconstruction, memory reconstruction. Expected evidence: source-linked intent refs and before/after summary comparisons.
- Can replay distinguish user-stated intent from summary-derived or inferred intent? Affected dimensions: intent reconstruction, replay provenance reconstruction. Expected evidence: source event IDs, summary metadata, and memory refs.
- How are expired, revised, or contradicted instructions represented in replay artifacts? Affected dimensions: intent reconstruction, contradiction reconstruction, temporal reconstruction. Expected evidence: instruction lineage and timestamped revisions.

## Validation requirements

- Build or collect a public failed-session fixture that includes transcript, event log, tool results, memory traces, environment snapshots, runtime config, recovery traces, and replay provenance.
- Compare causal reconstruction from visible replay alone against causal reconstruction from replay plus lineage metadata.
- Label each reconstruction dimension as `observed`, `inferred`, `hypothesis`, or `unresolved` based on public fixture results.
- Keep language neutral, bounded, and evidence-first; do not convert unresolved reconstruction gaps into unsupported target-system defect claims.
