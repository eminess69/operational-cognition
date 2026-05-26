# Operational Reconstruction Doctrine

## Replayability is not reconstruction

Replay can show what was visible, ordered, or recorded. Reconstruction requires enough lineage to explain how the recorded state, memory, tools, environment, timing, configuration, and recovery behavior contributed to the failure pathway.

## Causal replay requires survivable lineage

Causal replay requires more than a transcript or browser recording. It requires stable references that connect actions to observations, memory recalls, environment state, runtime configuration, and recovery events.

## Reconstruction requires provenance completeness

Public audits should state what provenance is available, what provenance is missing, and which causal claims therefore remain unresolved. A replay artifact should not be treated as complete unless its capture boundaries, source hashes, timestamps, redactions, and omitted ranges are visible enough for the audit question.

## Compression boundaries require replay metadata

Compaction, condensation, summarization, truncation, and redaction boundaries should identify what was preserved, what was omitted, what was summarized, and where the compressed representation entered the active context.

## Operational failure analysis depends on retained continuity

Failure reconstruction depends on continuity across transcript, event, tool/action, memory, environment, temporal, contradiction, recovery-loop, intent, and provenance dimensions. If a dimension is missing, the public claim should remain bounded to the dimensions that survived.

## Public proofs require bounded claims

Public proof artifacts must distinguish observed mechanisms, inferred implications, hypotheses, and unresolved questions. Placeholder MCP consultation is advisory only. Public outputs must not expose Belief Ledger internals, Inside Voice internals, harmonic traceback implementation, hidden chain-of-thought, private prompts, substrate state, or unsupported target-system conclusions.

## Candidate replay-preserving metadata

- event IDs
- timestamps
- omitted-range refs
- tool result refs
- memory refs
- recovery refs
- environment refs
- runtime config refs
- source hashes
