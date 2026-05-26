# Unresolved Questions

## Evidence gaps

- Which public examples show the original pre-compression event range, the generated summary, and the post-compression active context for transcript continuity?
- Which source IDs or exported artifacts demonstrate omitted-range references that can be followed after compression?
- Which examples show actual compressed outputs rather than architecture-level descriptions?

## Replay gaps

- For replayability continuity, what minimum set of source refs, hashes, event IDs, timestamps, and summary offsets is sufficient to replay compressed context?
- For tool/action continuity, are large, redacted, or truncated tool results preserved by content, hash, pointer, or omission marker?
- For temporal ordering continuity, can auditors reconstruct fine-grained order inside summarized ranges?

## Compression metadata gaps

- Do compression artifacts expose summarization boundaries, kept head/tail ranges, omitted ranges, model used for summarization, and summary instructions?
- Do successor transcripts or condensed views retain stable links back to the original transcript or event log?
- Are compaction retries, provider fallback choices, and condensation requests included as first-class replay events?

## Memory continuity gaps

- For memory continuity, are memory writes before compaction captured with timestamps, source refs, and original triggering context?
- Are memory search queries, result IDs, result content, and truncation boundaries replayable?
- Do memory promotion or consolidation passes preserve enough provenance to distinguish raw context from curated summaries?

## Environment continuity gaps

- For environment continuity, are workspace hashes, filesystem diffs, container IDs, dependency versions, browser state, and external-service references captured alongside compressed context?
- Can browser/UI replay be linked to the model-visible compressed context that caused the browser actions?
- Which environment state is intentionally omitted, redacted, or left outside replay artifacts?

## Causal lineage gaps

- For causal lineage continuity, can an auditor trace a later action back through summary text, omitted event IDs, tool results, memory refs, and environment state?
- Are rejected alternatives, failed branches, uncertainty, and contradictions preserved as lineage metadata or flattened into final summaries?
- Does action intent survive compression with source authority, expiry, approval boundaries, and scope changes intact?

## Validation requirements

- Build a public replay fixture with original context, compressed context, event log, memory refs, tool refs, environment refs, and recovery-loop refs.
- Compare replay from full context against replay from compressed context plus metadata.
- Label each continuity dimension as observed, inferred, hypothesis, or unresolved based on fixture results.
- Keep target-system language neutral and evidence-first throughout validation.
