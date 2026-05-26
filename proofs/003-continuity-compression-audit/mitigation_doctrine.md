# Compression Governance Doctrine

## Compression is not equivalent to continuity preservation

Compression can keep a system operational while still removing detail needed for audit. A compressed context should not be treated as equivalent to the original context unless source ranges, hashes, timestamps, and omitted boundaries remain reconstructable.

## Summaries may preserve utility while losing replay fidelity

Summaries can preserve useful task state, current goals, recent decisions, and enough context to continue work. That does not mean they preserve the full evidence path. Replay analysis should separate continued task utility from reconstruction fidelity.

## Replayability requires survivable lineage

Operational replay after compression requires more than a final summary. It requires lineage that links the summary to source events, tool results, memory writes, environment state, and recovery actions.

## Compression boundaries should be explicit

Compression events should identify what was summarized, what was preserved verbatim, what was omitted, and where the compressed representation entered the active context. Auditors should be able to distinguish raw continuity from summarized continuity.

## Operational cognition requires reconstructability limits

Public audits should state what can be reconstructed, what requires inference, and what remains unreconstructable from available evidence. Compression adequacy should be evaluated as a bounded operational property, not as hidden mental-state access.

## Public proofs require bounded claims

Public proof artifacts must distinguish observed mechanisms, inferred implications, hypotheses, and unresolved questions. Placeholder MCP consultation is advisory only. Public outputs must not expose Belief Ledger internals, Inside Voice internals, harmonic traceback implementation, hidden chain-of-thought, private prompts, or substrate internals.

## Potential replay-preserving metadata categories

- source refs
- timestamps
- omitted ranges
- contradiction refs
- causal linkage refs
- recovery loop refs
- summarization boundaries
