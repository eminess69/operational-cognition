# Evidence Plan

Proof 003 collects a bounded public evidence set around compression, condensation, replayability, and continuity reconstruction. The evidence layer supports later analysis without claiming that continuity loss is proven.

## Planned Evidence Sources

OpenClaw:

- compaction documentation
- memory overview documentation
- trajectory bundle documentation when relevant to post-compression replay and lineage

OpenHands:

- condenser and history compression architecture documentation
- conversation and event architecture documentation
- browser session recording documentation when useful for visible replay boundaries
- agent server architecture documentation when useful for environment continuity

Shared:

- public replay library documentation when it clarifies visible replay semantics
- public summarization, compaction, or context-window management documentation if later needed

## Collection Rules

- collect public sources only
- preserve source URLs and retrieval timestamps
- normalize whitespace before hashing
- store bounded local snapshots
- avoid large scraped blobs
- distinguish observed evidence from inference
- preserve uncertainty and contradiction
- avoid target-system attack language
- avoid unsupported continuity-loss conclusions
- keep MCP consultation artifacts under ignored `internal/`

## Evidence Status

Evidence collection v0.1 is stored in `evidence_manifest.json` with normalized snapshots under `evidence/snapshots/`.

No continuity compression adequacy conclusions are claimed yet. Later claims must reference source IDs from the evidence manifest and identify their claim level.
