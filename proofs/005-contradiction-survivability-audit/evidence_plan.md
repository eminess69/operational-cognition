# Evidence Plan

Proof 005 collects a bounded public evidence set around contradiction survivability and ambiguity preservation. The evidence layer supports later analysis without claiming that either target system has proven contradiction-preserving or contradiction-flattening behavior.

## Planned Evidence Sources

OpenClaw:

- compaction documentation
- memory documentation
- trajectory bundle documentation and examples, if public examples are available
- public recovery, restart, memory, or context-loss reports if they meet the evidence standard

OpenHands:

- condenser and history compression documentation
- event and conversation architecture documentation
- memory, recall, or condensed-view documentation if public
- browser/session replay documentation
- agent server, workspace, and runtime architecture documentation
- public recovery, restart, memory, or long-horizon ambiguity reports if they meet the evidence standard

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
- avoid unsupported contradiction survivability conclusions
- keep MCP consultation artifacts under ignored `internal/`

## Evidence Classification

Each source should be classified by the contradiction survivability dimensions it can inform:

- contradiction retention
- uncertainty retention
- stale assumption survivability
- rejected-alternative survivability
- source-authority survivability
- temporal contradiction survivability
- replay ambiguity survivability
- memory contradiction survivability
- summary contradiction survivability
- operational truth survivability

## Evidence Status

Evidence collection v0.1 is stored in `evidence_manifest.json` with normalized snapshots under `evidence/snapshots/`.

No contradiction survivability conclusion is claimed yet. Later claims must reference evidence IDs from the evidence manifest and identify claim level.
