# Authority Survivability Taxonomy

Each category below is an initial taxonomy, subject to public evidence validation. These are possible authority-preservation limitations, not conclusions about either target system.

## Stale-memory authority drift

Previously valid memory may remain available after the condition that made it valid has expired, changed, or been superseded. This category applies only when evidence shows that stale status or freshness boundaries are absent, unavailable, or not propagated.

## Summary authority drift

Summaries may preserve a useful belief while losing source authority, omitted ranges, caveats, or supersession links. This category remains conservative until artifact-level evidence shows what summary metadata is retained.

## Replay authority ambiguity

Replay artifacts may show visible sequence or event order without showing which remembered beliefs were authoritative at each decision point. This category is about replay adequacy, not a defect claim.

## Supersession loss

Later corrections may fail to remain linked to the beliefs they replace. This category requires evidence that supersession refs are missing, inaccessible, or not used in a relevant replay or recall surface.

## Temporal validity collapse

Time-bound beliefs can become timeless memory after promotion, summary, or replay. This category applies when validity windows, expiry conditions, or safe-to-act timing are not reconstructable.

## Contradiction-insensitive memory

Memory may preserve a claim while losing known contradictions, uncertainty, rejected alternatives, or unresolved questions attached to it. This category remains unresolved until contradiction retention surfaces are mapped.

## Inferred-belief promotion

Assistant inferences or summary-derived claims may be promoted into memory without retaining their inferred status. This category is a hypothesis-level risk until public evidence shows how promotion metadata is represented.

## Operational truth authority collapse

Observed facts, tool outputs, user instructions, recalled memories, and assistant inferences may become indistinguishable in operational context. This category defines an audit risk and requires source-backed validation before any target-specific claim.

## Authority lineage loss

The chain from source event to memory entry to recall to later action may become incomplete after compression, restart, or reconstruction. This category applies only when public artifacts cannot recover the relevant lineage.

## Memory replay survivability gaps

Replay may preserve what memory content existed while failing to preserve why it was trusted, whether it was current, or whether it was superseded. This category asks whether replay surfaces can support authority-aware reconstruction.
