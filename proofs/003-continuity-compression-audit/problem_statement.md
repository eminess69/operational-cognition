# Problem Statement

Long-horizon agent systems often keep working after context windows are pressured by summarizing, compacting, condensing, pruning, or otherwise reducing prior context. These mechanisms can preserve operational utility while changing the structure available for later audit. The unresolved question for this proof is what continuity survives compression and what cannot be reconstructed without additional lineage metadata.

Proof 003 asks a continuity compression adequacy question, not a target-system accusation:

When long-horizon agent context is compressed, summarized, compacted, or condensed, which operational continuity properties survive and which become unreconstructable?

The secondary question is:

Can replayability remain operationally meaningful after context compression?

## Scope

This proof is limited to public documentation and public evidence. It focuses on compression and condensation surfaces for OpenClaw and OpenHands, including compaction, memory flush or recall surfaces, event condensation, forgotten event IDs, kept head/tail context, transcript successors, replay artifacts, event logs, environment state references, and recovery loops.

## Out Of Scope

- mechanistic interpretability
- AGI claims
- consciousness claims
- black-box-solved claims
- substrate disclosure
- Belief Ledger internals
- Inside Voice internals
- harmonic traceback implementation details
- private prompts, private traces, or hidden chain-of-thought
- attack language or exploitability framing
- unsupported claims about target systems

## Evidence Standard

This proof distinguishes observed public mechanisms from inferred replayability implications. Compression may preserve enough information for continued task utility while still reducing fine-grained reconstruction fidelity. Any later assessment must reference evidence IDs, identify claim level, and preserve uncertainty where public artifacts do not establish the missing state.

The current phase is evidence collection. All categories and dimensions are initial operational scaffolds subject to evidence validation.
