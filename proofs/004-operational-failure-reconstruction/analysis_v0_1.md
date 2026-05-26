# Analysis v0.1

## Status

This is an initial evidence-backed analysis. It does not claim target-system defects, security issues, AGI, consciousness, black-box explanation, or substrate superiority.

The proof status is upgraded to `analysis`, but individual claims remain bounded as `observed`, `inferred`, `hypothesis`, or `unresolved`. The local MCP review was used only for bounded review support. The adapter status was `placeholder`, with request hash `487467c33954b5262ce53d163c85f1032a1fa982bab4cd6de169035c035d4712` and response hash `01c83374dee4611cc8d8a31de5874276b3a82d66c77356a3cd54facd9de3de58`.

## Evidence base

Proof 004 analysis v0.1 uses the public source IDs in `evidence_manifest.json`:

- `openclaw-doc-compaction`: compaction summaries, recent context preservation, full history on disk, tool call/result pairing across compaction chunks, context-overflow compaction and retry, and fallback behavior.
- `openclaw-doc-memory-overview`: Markdown memory files, loaded memory, memory search/get surfaces, memory boundaries, and memory interactions around compaction.
- `openclaw-doc-trajectory-bundles`: trajectory capture, transcript and tool-call timelines, runtime errors, timeout/abort/compaction/provider-error investigation questions, runtime settings, model/plugin/skill metadata, and redacted support bundles.
- `openhands-doc-agent-server-architecture`: remote execution, isolated workspaces, container orchestration, multi-user execution, monitoring, and runtime service surfaces.
- `openhands-doc-browser-session-recording`: browser session recording and replay using rrweb, captured DOM mutations, mouse movement, scrolling, browser events, and JSON replay artifacts.
- `openhands-doc-condenser-architecture`: history compression, threshold detection, summary generation, LLM-ready views, kept head/tail events, forgotten event IDs, and condensation metadata.
- `openhands-doc-conversation-architecture`: conversation lifecycle, state orchestration, conversation history, events, execution status, persistence, workspace coordination, and runtime services.
- `openhands-doc-events-architecture`: typed events, append-only event logs, event IDs, timestamps, source attribution, action events, observation events, and event conversion.
- `shared-rrweb-readme`: shared public context for browser replay semantics.

## Findings

### Observed

- F-001: Public evidence directly describes transcript and history surfaces relevant to transcript reconstruction. Evidence: `openclaw-doc-trajectory-bundles`, `openclaw-doc-compaction`, `openhands-doc-conversation-architecture`, `openhands-doc-condenser-architecture`.
- F-002: Public evidence directly describes event reconstruction surfaces, especially typed events and ordered event histories. Evidence: `openhands-doc-events-architecture`, `openhands-doc-conversation-architecture`, `openclaw-doc-trajectory-bundles`.
- F-003: Public evidence directly describes tool and action reconstruction surfaces. Evidence: `openclaw-doc-trajectory-bundles`, `openclaw-doc-compaction`, `openhands-doc-events-architecture`, `openhands-doc-browser-session-recording`.
- F-004: Public evidence directly describes memory surfaces relevant to reconstruction, but complete memory reconstruction is not established. Evidence: `openclaw-doc-memory-overview`, `openclaw-doc-compaction`, `openhands-doc-condenser-architecture`.
- F-006: Public evidence directly describes temporal reconstruction surfaces. Evidence: `openhands-doc-events-architecture`, `openhands-doc-conversation-architecture`, `openhands-doc-condenser-architecture`, `openclaw-doc-trajectory-bundles`, `openclaw-doc-compaction`.
- F-009: Public evidence directly describes recovery-loop reconstruction surfaces, but complete recovery-loop reconstruction is not established. Evidence: `openclaw-doc-compaction`, `openclaw-doc-trajectory-bundles`, `openhands-doc-conversation-architecture`, `openhands-doc-condenser-architecture`.
- F-011: Public evidence directly describes replay provenance surfaces, including trajectory metadata, event identifiers, omitted-event references, and browser recording artifacts. Evidence: `openclaw-doc-trajectory-bundles`, `openhands-doc-events-architecture`, `openhands-doc-condenser-architecture`, `openhands-doc-browser-session-recording`, `shared-rrweb-readme`.

### Inferred

- F-005: Environment reconstruction is relevant to causal failure analysis, but current public evidence only partially supports it. Evidence: `openhands-doc-agent-server-architecture`, `openhands-doc-conversation-architecture`, `openclaw-doc-trajectory-bundles`.
- F-008: Visible replay and event logs can support partial reconstruction, but causal operational reconstruction requires survivable lineage across memory, environment, tool results, recovery loops, intent, and provenance. Evidence: all current Proof 004 public source IDs.

### Hypothesis

- F-010: Intent reconstruction drift is a plausible operational risk when summaries, memory recalls, or condensed views omit constraints, authority, timing, or scope changes. Evidence: `openclaw-doc-memory-overview`, `openclaw-doc-compaction`, `openhands-doc-condenser-architecture`, `openhands-doc-conversation-architecture`.

### Unresolved

- F-007: Current public evidence does not establish contradiction reconstruction. Evidence: `openclaw-doc-compaction`, `openclaw-doc-memory-overview`, `openhands-doc-condenser-architecture`.

## Operational reconstruction assessment

Transcript reconstruction: observed surfaces exist. OpenClaw documents transcript-relevant trajectory capture and compaction behavior; OpenHands documents conversation history and condensed views. Complete transcript reconstruction across every omitted, compacted, or condensed range still requires exported examples.

Event reconstruction: observed surfaces exist. OpenHands documents typed, append-only events, event IDs, timestamps, and conversation state built from event history. OpenClaw trajectory documentation describes structured timelines. Event reconstruction does not automatically reconstruct external environment or memory state.

Tool/action reconstruction: observed surfaces exist. OpenClaw trajectory documentation describes tool calls and support-bundle uses, while compaction documentation describes preserving tool call/result pairs across split boundaries. OpenHands documents action and observation events and browser session recording. Complete tool-result reconstruction remains bounded by result retention, redaction, truncation, and schema provenance.

Memory reconstruction: observed memory surfaces exist, especially in OpenClaw documentation. Current evidence does not establish full reconstruction of memory writes, recall queries, recall results, indexes, or memory influence on later action.

Environment reconstruction: inferred as partially supported. The evidence describes workspaces, containers, runtime services, execution environments, and trajectory metadata. It does not establish complete filesystem diffs, dependency versions, browser session state, external service state, or runtime configuration snapshots for failed public sessions.

Temporal reconstruction: observed surfaces exist. The evidence describes append-only event histories, event timestamps, trajectory timelines, compaction/retry boundaries, and condensation metadata. Fine-grained ordering inside omitted or summarized ranges remains unresolved.

Contradiction reconstruction: unresolved. Current public evidence does not establish that conflicts, stale assumptions, rejected alternatives, corrections, or uncertainty markers survive summaries, memory surfaces, or condensed views.

Causal reconstruction: inferred as partial and bounded. Public replay, event, trajectory, browser, memory, compression, and runtime surfaces can support partial reconstruction, but the current evidence does not establish complete causal reconstruction of a failed long-horizon session.

Recovery-loop reconstruction: observed surfaces exist. OpenClaw documents context-overflow compaction and retry, fallback behavior, and trajectory investigation of timeouts, aborts, compactions, and provider errors. OpenHands documents lifecycle and context-management surfaces. Complete recovery-loop reconstruction still needs retry, fallback, cleanup, restart, and resume lineage.

Intent reconstruction: hypothesis. Transcript, memory, conversation, and summary surfaces make intent reconstruction relevant, but current evidence does not validate whether constraints, approvals, prohibitions, authority, timing, and changed scope survive replay or summarization.

Replay provenance reconstruction: observed surfaces exist. Public evidence describes trajectory metadata, event metadata, forgotten event IDs, browser recording artifacts, and replay tooling. This proof pack also records source hashes. Provenance completeness still depends on omitted ranges, redaction policy, capture boundaries, and artifact availability.

## Key operational insight

Visible replay and event logs can support partial reconstruction, but causal operational reconstruction requires survivable lineage across memory, environment, tool results, recovery loops, intent, and provenance.

Claim level: `inferred`.

Reasoning bridge: the current public evidence describes multiple useful reconstruction surfaces: transcript and history artifacts, structured event logs, tool/action lineage, browser recording, memory surfaces, compression boundaries, workspace/runtime surfaces, and provenance metadata. Those surfaces support partial reconstruction. The same evidence also shows that causal explanation depends on state that can live outside visible replay, including memory, environment, tool results, recovery loops, intent, and provenance. The current evidence does not establish a complete causal replay bundle.

## Public/private boundary

This analysis uses only public evidence snapshots and sanitized MCP lineage hashes. The raw MCP review artifact remains under ignored `internal/`. No private prompts, private traces, implementation internals, hidden reasoning chains, secrets, or unsupported target-system conclusions are included.

## Next validation requirements

- public failed-session examples
- before/after compression artifacts
- event logs with omitted ranges
- memory recall/write traces
- tool result hashes
- environment snapshots
- runtime config
- recovery/retry traces
- public replay bundles that connect transcript, event, memory, tool, environment, recovery, intent, and provenance dimensions
