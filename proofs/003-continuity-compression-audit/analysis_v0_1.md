# Analysis v0.1

## Status

This is an initial evidence-backed analysis. It does not claim target-system defects, security issues, AGI, consciousness, black-box explanation, or substrate superiority.

The proof status is upgraded to `analysis`, but individual claims remain bounded as `observed`, `inferred`, `hypothesis`, or `unresolved`. The local MCP review was used only for bounded review support. The adapter status was `placeholder`, with request hash `429a0dff20456363ee1ba8406fa7bd59a1dd48eabf52e00ba05bbe064b3a7b58` and response hash `5b8eb4724da816f546fdab11963807007ad31d35f5a65489ab7a03cdd8ce23e0`.

## Evidence base

Proof 003 analysis v0.1 uses the public source IDs in `evidence_manifest.json`:

- `openclaw-doc-compaction`: compaction, summaries, recent context, successor transcripts, overflow retry, memory flush, identifier preservation, and compaction providers.
- `openclaw-doc-memory-overview`: memory files, daily notes, memory search/get surfaces, action-sensitive memory boundaries, truncation signals, and automatic memory flush before compaction.
- `openclaw-doc-trajectory-bundles`: ordered trajectory exports, prompt/tool/transcript timelines, runtime events, compactions, metadata, and bounded redaction.
- `openhands-doc-condenser-architecture`: history compression, threshold detection, summary generation, kept head/tail events, forgotten event IDs, summary offsets, and LLM-ready views.
- `openhands-doc-conversation-architecture`: conversation state, event storage, append-only event log, execution models, persistence, and workspace coordination.
- `openhands-doc-events-architecture`: typed events, event IDs, timestamps, source attribution, action/observation events, condensation events, and event-to-message conversion.
- `openhands-doc-agent-server-architecture`: remote execution, workspace isolation, container orchestration, streaming, resource limits, and deployment surfaces.
- `openhands-doc-browser-session-recording`: browser session recording and replay through rrweb.
- `shared-rrweb-readme`: shared visible browser replay context.

## Findings

### Observed

- F-001: Public docs describe compression mechanisms that preserve a summary and recent context while changing the active model-visible context. Evidence: `openclaw-doc-compaction`, `openhands-doc-condenser-architecture`.
- F-002: Public docs describe tool/action continuity surfaces, including OpenClaw call/result pairing at compaction splits and OpenHands action/observation event types. Evidence: `openclaw-doc-compaction`, `openhands-doc-events-architecture`.
- F-003: OpenClaw docs describe memory continuity surfaces, including durable files, memory search/get, and automatic memory flush before compaction. Evidence: `openclaw-doc-memory-overview`, `openclaw-doc-compaction`.
- F-004: Public docs describe temporal ordering surfaces relevant to compression replay, including ordered trajectory timelines, append-only event logs, event metadata, and condensation offsets. Evidence: `openclaw-doc-trajectory-bundles`, `openclaw-doc-compaction`, `openhands-doc-conversation-architecture`, `openhands-doc-events-architecture`, `openhands-doc-condenser-architecture`.
- F-009: Public docs describe recovery-loop compression triggers, including compaction on context overflow and condensation requests after context-limit errors. Evidence: `openclaw-doc-compaction`, `openhands-doc-condenser-architecture`, `openhands-doc-events-architecture`.

### Inferred

- F-007: Environment continuity under compression is only partially supported by the current evidence and remains dependent on external state capture. Evidence: `openhands-doc-agent-server-architecture`, `openhands-doc-conversation-architecture`, `openclaw-doc-trajectory-bundles`.
- F-008: Replayability can remain operationally meaningful after compression when summaries are linked to surviving event, transcript, tool, and metadata surfaces, but causal replay adequacy remains bounded. Evidence: `openclaw-doc-trajectory-bundles`, `openclaw-doc-compaction`, `openhands-doc-condenser-architecture`, `openhands-doc-events-architecture`, `openhands-doc-browser-session-recording`, `shared-rrweb-readme`.
- F-011: Compression may preserve task utility while reducing replay fidelity unless survivable lineage metadata is retained. Evidence: `openclaw-doc-compaction`, `openclaw-doc-trajectory-bundles`, `openhands-doc-condenser-architecture`, `openhands-doc-events-architecture`.

### Hypothesis

- F-010: Intent continuity drift is a plausible compression risk when summaries omit constraints, authority, timing, or action boundaries. Evidence: `openclaw-doc-memory-overview`, `openclaw-doc-compaction`, `openhands-doc-condenser-architecture`.

### Unresolved

- F-005: Current public evidence does not establish whether contradiction continuity survives compression. Evidence: `openclaw-doc-compaction`, `openhands-doc-condenser-architecture`, `openclaw-doc-memory-overview`.
- F-006: Current public evidence does not establish full causal lineage continuity after compression. Evidence: `openhands-doc-condenser-architecture`, `openhands-doc-events-architecture`, `openclaw-doc-trajectory-bundles`, `openclaw-doc-compaction`.

## Continuity survivability assessment

Transcript continuity: observed mechanisms preserve summaries, recent context, and condensed views. Full transcript reconstructability from compressed active context is not established by current public evidence.

Tool/action continuity: observed mechanisms preserve or expose tool/action event structures. Exact replay of all tool result bodies, redaction boundaries, and tool schema versions remains bounded.

Memory continuity: observed OpenClaw mechanisms can move selected context into durable memory before compaction. Complete memory replay lineage remains unresolved because writes, recalls, indexes, and recall results are not yet validated as a replay bundle.

Environment continuity: inferred as only partially supported. Public docs describe workspaces, containers, runtime metadata, and trajectory surfaces, but compression evidence itself does not establish complete filesystem, container, dependency, browser, or external-service reconstruction.

Temporal ordering continuity: observed ordering surfaces exist through ordered timelines, append-only event logs, event metadata, and condensation offsets. Fine-grained omitted-range ordering remains an evidence requirement.

Contradiction continuity: unresolved. Public docs show summarization and some provenance-oriented memory surfaces, but not contradiction-preserving compression rules.

Replayability continuity: inferred as meaningful but bounded. Visible and event replay surfaces can survive compression, while causal replay requires source ranges, omitted IDs, metadata, memory refs, tool refs, and environment refs.

Recovery-loop continuity: observed triggers exist for compression during recovery from context pressure. Full recovery-loop replay still needs retry, fallback, error, cleanup, and restart metadata.

Intent continuity: hypothesis. Public docs support the relevance of guided summaries and action-sensitive memory boundaries, but do not validate that compressed summaries preserve constraints and authority in practice.

Causal lineage continuity: unresolved. Current public evidence exposes useful lineage surfaces, but does not establish a complete causal chain from original context through compression into later action.

## Key operational insight

Compression may preserve task utility while reducing replay fidelity unless survivable lineage metadata is retained.

Claim level: `inferred`.

Reasoning bridge: OpenClaw and OpenHands evidence both describe mechanisms intended to keep long contexts usable by summarizing or condensing prior history. The replay and event evidence shows that operational reconstruction depends on ordered timelines, event IDs, prompt surfaces, tool/action lineage, metadata, and retained omitted-range references. The evidence supports the distinction between continued task utility and audit-grade replay fidelity, but it does not yet establish a minimum sufficient metadata bundle.

## Public/private boundary

This analysis uses only public evidence snapshots and sanitized MCP lineage hashes. The raw MCP review artifact remains under ignored `internal/`. No private prompts, private traces, implementation internals, or hidden reasoning chains are included.

## Next validation requirements

- Collect public examples of compressed session artifacts with original event ranges, summaries, and omitted IDs.
- Compare model-visible compressed context against original transcript and event history for at least one public example.
- Determine whether contradiction, uncertainty, rejected alternatives, and source authority survive summary generation.
- Validate whether tool result bodies, tool result hashes, redaction boundaries, and tool schema versions survive compression.
- Validate memory continuity with memory write, memory search, recall result, and truncation metadata.
- Validate environment continuity with workspace hashes, filesystem diffs, container/runtime identifiers, browser replay references, and dependency versions.
- Define a minimum replay-preserving metadata bundle for compression boundaries.
