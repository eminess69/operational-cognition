# Public Lineage Summary

This file summarizes public-safe lineage for Proof 002.

## Consultation Source

- source: local Inside Voice MCP consultation endpoint
- endpoint: `http://127.0.0.1:8766`
- contract version: `inside_voice.mcp.consultation.v1`
- adapter status: `placeholder`
- mode: `proof_planning`
- request hash: `450b90efe817e368704117d3c711caec5df311c9ea9df379421297c94e6d3452`
- response hash: `1ac6030c5b1b554a930d5d0496396467b06234ba983ab73d2b6d44efe3b82ab1`

The raw MCP request and response are stored only under ignored `internal/` and are not part of the public proof pack.

## Planning Decision

Create a public replayability adequacy scaffold for evaluating whether visible replay artifacts preserve enough operational state for long-horizon agent audit.

## Sources Collected

The initial evidence set targets:

- OpenClaw trajectory bundle documentation
- OpenClaw compaction documentation
- OpenClaw memory documentation
- OpenHands browser session recording documentation
- OpenHands conversation architecture documentation
- OpenHands event architecture documentation
- OpenHands condenser architecture documentation
- OpenHands agent server architecture documentation
- shared rrweb documentation for browser/UI replay context

## Constraints Applied

- public evidence only
- no AGI claims
- no consciousness claims
- no black-box-solved claims
- no substrate internals
- no hidden chain-of-thought
- no target-system attack language
- distinguish visible replay from causal replay
- distinguish observed evidence from inference
- preserve uncertainty
- placeholder adapter status disclosed

## Current Claim Boundary

Proof 002 is an evidence collection scaffold. It does not claim target-system defects, security issues, or replay inadequacy. It only defines replay dimensions, initial evidence references, and unresolved adequacy questions.

## Unresolved Questions

- Which public artifacts capture exact model-visible context after compaction or condensation?
- Which artifacts capture memory state, recall results, and cross-session lineage?
- Which artifacts capture environment/workspace state with enough hashable references?
- Which artifacts capture recovery, retry, fallback, and cleanup loops?
- What minimum replay bundle is sufficient for operational cognition audits?

## Next Evidence Requirements

- public examples of exported replay bundles, if available
- public docs on trajectory redaction and truncation boundaries
- public docs on session branch restoration and recovery flow
- public docs on runtime configuration capture and environment snapshots
- public docs or issues that clarify limitations without overclaiming
