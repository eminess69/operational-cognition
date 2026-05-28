# Breakdown Taxonomy

The scenarios use these bounded degradation classes:

- Omitted-range loss: required event ranges are absent from the visible replay window.
- Stale authority source: visible summaries cite an older manifest or runtime assumption.
- Contradictory summaries: compressed summaries disagree with event order or branch state.
- Retry divergence: retries follow different recovery branches from the same visible prompt.
- Replay ambiguity: visible-only state supports multiple incompatible reconstructions.
- Environment/runtime drift: runtime assumptions change between event capture and replay.
- Incomplete recovery trace: the trace ends before a branch is fully closed.
- Partial lineage corruption: a lineage record is damaged but not fully absent.
- Compressed context degradation: compression removes ordering, authority, or branch evidence.
- Temporal validity conflict: timestamps or validity windows conflict with visible claims.
- Failed recovery branch: at least one recovery path is explicitly recorded as failed.

The taxonomy treats these as scenario stressors, not target-system defects.
