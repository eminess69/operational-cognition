# Evidence Plan

Proof 002 collects a small public evidence set around replay/session/trajectory behavior. The evidence layer should support later analysis without claiming that replay gaps are proven.

## Planned Evidence Sources

OpenClaw:

- trajectory bundle documentation
- transcript/runtime/tool-call capture documentation
- compaction documentation when relevant to replay reconstruction
- memory documentation when relevant to memory state replay

OpenHands:

- browser session recording and replay documentation
- conversation/event architecture documentation
- condenser/history compression documentation when relevant to compressed context replay
- agent server or runtime architecture documentation when relevant to environment and configuration replay

Shared:

- public replay library documentation when it clarifies visible browser/UI replay semantics

## Collection Rules

- collect public sources only
- preserve source URLs and retrieval timestamps
- normalize whitespace before hashing
- store bounded local snapshots
- avoid large scraped blobs
- distinguish observed evidence from inference
- preserve uncertainty and contradiction
- avoid attack language and unsupported conclusions
- keep MCP consultation artifacts under ignored `internal/`

## Evidence Status

Evidence collection v0.1 is stored in `evidence_manifest.json` with normalized snapshots under `evidence/snapshots/`.

No replayability adequacy conclusions are claimed yet. Later claims must reference source IDs from the evidence manifest and identify their claim level.
