# Replay Gap Taxonomy

Each category below is an initial taxonomy, subject to evidence validation. These are possible replayability pressure points, not conclusions about either target system.

## Visible-only replay gap

Initial taxonomy, subject to evidence validation.

Visible replay may show transcripts, browser events, or session timelines while leaving causal state unresolved. Public evidence can indicate visible replay mechanisms without proving causal replay adequacy.

## Memory-state replay gap

Initial taxonomy, subject to evidence validation.

Replay can appear incomplete if durable memory files, memory search indexes, recall results, or memory promotion/flush events are not captured with enough provenance to reconstruct model-visible context.

## Environment-state replay gap

Initial taxonomy, subject to evidence validation.

Replay may not reconstruct workspace files, sandbox state, container images, installed tools, ports, external services, or filesystem diffs that influenced an action path.

## Tool-result provenance gap

Initial taxonomy, subject to evidence validation.

Tool/action logs can preserve the existence of calls while leaving returned data, truncation, source hashes, redaction decisions, or error provenance unresolved.

## Compressed-context reconstruction gap

Initial taxonomy, subject to evidence validation.

History compression can create divergence between the full transcript and what the model actually saw. Adequate replay may need summaries, forgotten event IDs, compaction boundaries, and preserved tail context.

## Recovery-loop replay gap

Initial taxonomy, subject to evidence validation.

Retries, fallback models, stuck detection, timeouts, restarts, aborts, and cleanup behavior can shape long-horizon outcomes. Public evidence may indicate these mechanisms without proving that replay artifacts reconstruct them end to end.

## Cross-session replay gap

Initial taxonomy, subject to evidence validation.

Replay can become unresolved when work spans sessions, branches, sub-agents, cron runs, heartbeats, or resumed conversations without a complete lineage bridge.

## Causal-lineage replay gap

Initial taxonomy, subject to evidence validation.

Replay may show what happened while leaving why it happened unresolved. Causal lineage can require model-visible prompt state, memory recalls, tool schemas, configuration, environment state, and decision boundary metadata.

## Configuration/runtime replay gap

Initial taxonomy, subject to evidence validation.

Replay can vary when model IDs, provider routing, tool policies, approval modes, plugin lists, skill context, sandbox settings, or runtime images are not captured or are only partially captured.
