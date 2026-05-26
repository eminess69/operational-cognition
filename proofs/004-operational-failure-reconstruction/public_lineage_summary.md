# Public Lineage Summary

This file summarizes public-safe lineage for Proof 004.

## Consultation Source

- source: local Inside Voice MCP consultation endpoint
- endpoint: `http://127.0.0.1:8766`
- contract version: `inside_voice.mcp.consultation.v1`
- adapter status: `placeholder`
- mode: `proof_planning`
- request hash: `abfb390b7a12239f88735e1ab613d468021418f6ee375c2f33c1380d827e773e`
- response hash: `30107566dc8672f33d436399aab5a080ec18a6d8d75c69353138aaa7c4d36359`

The raw MCP request and response are stored only under ignored `internal/` and are not part of the public proof pack.

## Planning Decision

Create a public operational failure reconstruction scaffold for evaluating whether replay artifacts, event logs, trajectory bundles, browser/session replay, memory surfaces, and continuity metadata can support bounded causal reconstruction of long-horizon failure pathways.

## Evidence Collected

The initial evidence set targets public documentation for:

- OpenClaw trajectory bundles
- OpenClaw compaction
- OpenClaw memory
- OpenHands events architecture
- OpenHands conversation architecture
- OpenHands condenser architecture
- OpenHands browser session recording
- OpenHands agent server architecture
- rrweb browser replay context

## Constraints Applied

- public evidence only
- no AGI claims
- no consciousness claims
- no black-box-solved claims
- no substrate internals
- no hidden chain-of-thought
- avoid target-system attack framing
- distinguish observed public evidence from inference
- preserve uncertainty
- disclose placeholder adapter status
- do not expose private implementation internals

## Current Claim Boundary

Proof 004 is an evidence collection scaffold. It does not claim that public artifacts are sufficient or insufficient for complete causal reconstruction. It defines the reconstruction dimensions, gap taxonomy, and replay adequacy questions that later evidence-backed analysis must test.

## Unresolved Reconstruction Questions

- Which artifacts preserve model-visible context after compaction, condensation, or restart?
- Which artifacts preserve tool results, truncation markers, redaction reasons, and result provenance?
- Which artifacts preserve memory writes, recall queries, recall results, and memory index state?
- Which artifacts preserve environment, workspace, runtime, browser, and dependency provenance?
- Which artifacts preserve recovery-loop state before and after retry, restart, abort, or resume?
- Which artifacts preserve contradictions, stale assumptions, rejected alternatives, and uncertainty markers?

## Replay Adequacy Implications

Visible replay can support operational review, but causal replay adequacy requires survivable lineage across transcript, event, tool/action, memory, environment, temporal, contradiction, recovery-loop, intent, and provenance dimensions.

## Next Investigation Requirements

- collect public examples of exported trajectories or replay bundles if available
- collect public docs or reports that clarify recovery and restart semantics
- map evidence IDs to each reconstruction dimension
- identify which dimensions are observed, inferred, hypothesis-level, or unresolved
- defer any causal adequacy claim until it is explicitly evidence-backed
