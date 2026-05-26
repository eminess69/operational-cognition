# Problem Statement

Long-horizon agent systems often expose artifacts such as transcripts, event logs, browser recordings, trajectory bundles, session files, summaries, and runtime metadata. These artifacts can be useful for debugging and audit. The unresolved question for this proof is whether visible replay artifacts preserve enough operational state to reconstruct why an agent took a path, recovered from an error, lost continuity, or diverged across sessions.

Proof 002 asks a replayability adequacy question, not a target-system accusation:

Do public replay/session/trajectory artifacts preserve enough operational state to reconstruct long-horizon agent failure pathways?

The secondary question is:

What state dimensions must be captured for replayability to support operational cognition audits?

## Scope

This proof is limited to public documentation and public evidence. It focuses on replay and reconstruction surfaces for OpenClaw and OpenHands, including trajectory bundles, browser/session replay, event logs, persistence, memory, compaction, environment/workspace state, runtime configuration, and recovery loops.

## Out Of Scope

- proving target-system defects
- asserting hidden vulnerabilities
- AGI or consciousness claims
- black-box interpretability claims
- substrate superiority claims
- Belief Ledger or Inside Voice internals
- private prompts, private traces, or hidden chain-of-thought
- attack language or exploitability framing

## Evidence Standard

This proof distinguishes visible replay from causal replay. Visible replay may show user-visible behavior, browser/UI events, transcripts, or tool-call sequences. Causal replay would need enough surrounding state to explain why a path occurred, including memory, compressed context, configuration, environment, tool results, and recovery/retry lineage.

The current phase is evidence collection. Any assessment remains preliminary until backed by source references and replay validation.
