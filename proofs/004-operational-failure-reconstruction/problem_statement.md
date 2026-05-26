# Problem Statement

Long-horizon agent failures can involve many interacting surfaces: transcript turns, tool calls, memory recalls, environment state, browser sessions, retries, compaction events, restarts, and runtime configuration. Visible replay can show parts of a run, but operational failure reconstruction asks a stricter question: whether public artifacts preserve enough causal state to explain why the failure path occurred.

Proof 004 asks:

Can public replay artifacts, event logs, and continuity metadata reconstruct enough causal operational state to explain why long-horizon failures occurred?

The secondary question is:

Which operational continuity gaps prevent reliable causal reconstruction?

## Scope

This proof is limited to public documentation, public replay or trajectory artifacts when available, public issue or discussion records when later collected, and public metadata about continuity, replay, compaction, condensation, recovery, and runtime state.

Initial targets are OpenClaw and OpenHands. The proof focuses on replay artifacts, event systems, trajectory bundles, browser/session replay, memory surfaces, condensation or compaction flows, and recovery or restart paths.

## Out Of Scope

- mechanistic interpretability
- AGI claims
- consciousness claims
- black-box-solved claims
- substrate disclosure
- vulnerability research
- target-system attack framing
- Belief Ledger internals
- Inside Voice internals
- harmonic traceback implementation details
- private prompts, private traces, or hidden chain-of-thought

## Evidence Standard

This proof distinguishes observed public mechanisms from inferred replay implications and unresolved reconstruction questions. A visible replay surface is not treated as causal reconstruction unless it preserves enough provenance to connect events, tool results, memory state, environment state, timing, and recovery loops.

The current phase is evidence collection. All dimensions, taxonomy categories, and matrix assessments are preliminary and subject to source-backed revision.
