# Evidence Plan

Proof 006 collects a bounded public evidence set around memory authority and belief survivability. The evidence layer supports later analysis without claiming that either target system has proven authority-preserving or authority-drifting behavior.

## Planned Evidence Sources

OpenClaw:

- memory documentation
- compaction documentation
- trajectory bundle documentation and examples, if public examples are available
- public memory promotion, memory recall, recovery, restart, or stale-context reports if they meet the evidence standard

OpenHands:

- condenser and history compression documentation
- event and conversation architecture documentation
- memory, recall, or condensed-view documentation if public
- browser/session replay documentation
- agent server, workspace, and runtime architecture documentation
- public recall, recovery, restart, memory, or long-horizon authority reports if they meet the evidence standard

Shared:

- public replay-library documentation where it clarifies visible replay semantics
- public event-log, provenance, summary, or replay adequacy references if later needed

## Collection Rules

- collect public sources only
- preserve source URLs and retrieval timestamps
- normalize whitespace before hashing
- store bounded local snapshots
- avoid large scraped blobs
- distinguish observed public evidence from inference
- preserve uncertainty and contradiction
- avoid target-system attack language
- avoid unsupported authority survivability conclusions
- keep MCP consultation artifacts under ignored `internal/`

## Evidence Classification

Each source should be classified by the authority survivability dimensions it can inform:

- memory authority retention
- stale-belief survivability
- supersession survivability
- source-authority survivability
- temporal validity survivability
- replay authority survivability
- summary authority survivability
- memory recall authority survivability
- contradiction-aware memory survivability
- operational truth authority survivability

## Evidence Status

Evidence collection v0.1 is stored in `evidence_manifest.json` with normalized snapshots under `evidence/snapshots/`.

No authority survivability conclusion is claimed yet. Later claims must reference evidence IDs from the evidence manifest and identify claim level.
