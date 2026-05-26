# Observed continuity pressure signals

This file tracks public, observable continuity-related patterns for Proof 001. It is an evidence collection aid only. Signals below are not validated conclusions, are not security findings, and do not establish superiority or substrate-level understanding.

## Memory persistence concerns

Observed OpenClaw documentation describes memory files, daily notes, memory search, and automatic memory flush before compaction. Reported OpenClaw issues describe concerns around reset-time memory flush, session index recovery after gateway restart, and new sessions appearing to ignore existing memory. These reports appear relevant to memory persistence but remain source reports, not independently validated findings.

Observed OpenHands documentation describes conversation history compression through condensers, including summarized events and forgotten event IDs. A reported OpenHands issue describes recall-action transcript role ordering with a strict-alternation backend. This appears relevant to memory/context insertion semantics, with unresolved generality.

## Long-horizon execution concerns

Observed public docs for both systems describe mechanisms for continuing long conversations, bounded context, background work, and action loops. Reported issues include stalled execution after a task-tracking action, long-running session resource growth, and non-interactive CLI requirements for running or resuming work. These are continuity pressure signals only.

## Replayability concerns

Observed OpenClaw documentation describes trajectory bundles for per-session runtime and transcript timelines. Observed OpenHands documentation describes browser session recording and replay through rrweb. These public mechanisms appear useful for replay evidence, but it remains unresolved whether they reconstruct every relevant environment, memory, tool, and recovery state needed for deterministic proof replay.

## Environmental state concerns

Reported issues include workspace initialization divergence in OpenHands and long-running process state growth in OpenClaw. These reports appear relevant to environment/session state consistency, but their scope is limited to the public reports and captured metadata.

## Tool/action lineage concerns

Observed OpenHands architecture documentation describes action/observation events, event logs, and tool execution patterns. Observed OpenClaw trajectory documentation describes captured prompts, transcript messages, tool calls, tool results, runtime events, and artifacts. Reported issues involving task tracking and recall actions appear relevant to tool/action lineage, but no generalized failure claim is made.

## Multi-session coordination concerns

Observed OpenClaw memory and compaction documentation describes disk-backed memory, session transcripts, and successor transcripts. Reported OpenClaw issues describe reset, restart, and new-session continuity concerns. The OpenHands CLI PRD reports resume and conversation-list requirements. These sources appear relevant to cross-session coordination, with unresolved differences between intended architecture, shipped behavior, and user-reported behavior.

## Architectural drift concerns

Observed OpenHands condenser documentation describes history compression, summaries, forgotten event IDs, and views. Observed OpenClaw compaction documentation describes summarized older turns, preserved recent messages, and full history staying on disk. These mechanisms appear to create places where represented context can diverge from full transcript history. This is a taxonomy signal only, not a claim that harmful drift occurred.
