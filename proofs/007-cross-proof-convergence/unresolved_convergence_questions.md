# Unresolved Convergence Questions

## Replay adequacy

- What minimum lineage is sufficient to move from visible replay to causal operational replay?
- Can a public replay bundle link each visible action to the exact model-visible context, event IDs, tool results, memory recalls, environment state, runtime config, and recovery state available at that time?
- Which replay questions can be answered from transcript and event order alone, and which require the full operational replay bundle?

## Compression survivability

- Do compressed summaries preserve stable refs to omitted transcript ranges, event ranges, tool results, memory writes, memory recalls, and source hashes?
- Are summary instructions, summary timestamps, kept head/tail ranges, forgotten event IDs, and summary insertion points available in public replay artifacts?
- Can auditors reconstruct what changed between full context, compressed context, and later action context?

## Contradiction survivability

- Do contradictions, uncertainty markers, rejected alternatives, stale assumptions, and unresolved questions survive compression, memory recall, and replay?
- Are contradiction refs linked to source authority, temporal validity, and resolution or supersession status?
- Can replay distinguish a resolved contradiction from a flattened contradiction or an omitted contradiction?

## Memory authority

- Do memory writes preserve source authority, triggering context, timestamp, temporal validity, contradiction status, and promotion reason?
- Do memory recalls preserve recall query, returned result refs, insertion point, freshness, stale status, supersession status, and authority class?
- Can replay distinguish user instruction, tool observation, documentation fact, assistant inference, memory-derived claim, and summary-derived claim?

## Causal reconstruction

- Can a later action be traced through transcript context, event log, tool result refs or hashes, memory write/recall refs, environment state, runtime config, contradiction refs, and recovery refs?
- What claims remain reconstructable when omitted ranges are unavailable?
- How should public audits classify claims that are visible in replay but not causally reconstructable?

## Environment reconstruction

- Which workspace snapshots, filesystem diffs, dependency refs, container refs, browser/session refs, runtime image refs, and external-state refs are needed for replay adequacy?
- Which environment state can be represented by hashes or refs rather than raw public disclosure?
- Can environment refs be linked to the actions that observed or modified them?

## Recovery-loop reconstruction

- Which artifacts preserve retries, fallback choices, context-overflow handling, restarts, resumptions, aborts, cleanup, and status transitions?
- Can pre-recovery state be linked to post-recovery state with event IDs, timestamps, environment refs, memory refs, and summary refs?
- Are recovery events first-class replay events or inferred from surrounding logs?

## Validation fixtures

- What public fixture should be used to test the minimum operational replay bundle?
- Can the same fixture be replayed from visible sequence alone and from the full lineage bundle to compare reconstruction strength?
- What metrics should decide whether survivable lineage is sufficient: claim reconstructability, contradiction retention, authority retention, causal trace completeness, or unresolved-gap reduction?
- How should fixture results update claim levels across observed, inferred, hypothesis, and unresolved?

