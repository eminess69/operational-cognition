# Evidence Plan

Proof 004 collects a bounded public evidence set around operational failure reconstruction. The evidence layer supports later analysis without claiming that any target-system failure has been causally reconstructed.

## Planned Evidence Sources

OpenClaw:

- trajectory bundle documentation and examples, if public examples are available
- compaction documentation
- memory documentation
- public restart, recovery, or session-continuity reports if they meet the evidence standard

OpenHands:

- event and conversation architecture documentation
- condenser and history compression documentation
- browser session recording documentation
- agent server, workspace, and runtime architecture documentation
- public recovery, restart, or long-horizon failure reports if they meet the evidence standard

Shared:

- public replay-library documentation where it clarifies visible replay semantics
- public event-log, provenance, or replay adequacy references if later needed

## Collection Rules

- collect public sources only
- preserve source URLs and retrieval timestamps
- normalize whitespace before hashing
- store bounded local snapshots
- avoid large scraped blobs
- distinguish observed public evidence from inference
- preserve uncertainty and contradiction
- avoid target-system attack language
- avoid unsupported reconstruction adequacy conclusions
- keep MCP consultation artifacts under ignored `internal/`

## Evidence Classification

Each source should be classified by the reconstruction dimensions it can inform:

- transcript reconstruction
- event reconstruction
- tool/action reconstruction
- memory reconstruction
- environment reconstruction
- temporal reconstruction
- contradiction reconstruction
- causal reconstruction
- recovery-loop reconstruction
- intent reconstruction
- replay provenance reconstruction

## Evidence Status

Evidence collection v0.1 is stored in `evidence_manifest.json` with normalized snapshots under `evidence/snapshots/`.

No causal reconstruction adequacy conclusion is claimed yet. Later claims must reference evidence IDs from the evidence manifest and identify claim level.
