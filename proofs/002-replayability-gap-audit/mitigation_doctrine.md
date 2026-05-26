# Replayability Adequacy Doctrine

## Visible replay is not causal replay

Visible replay can show transcripts, browser events, messages, and action order. It does not automatically explain why a path occurred. Operational replay should distinguish observable playback from causal reconstruction.

## Operational replay requires state dimensions

Long-horizon agent behavior can depend on memory, compressed context, tool results, environment state, configuration, runtime mode, recovery loops, and cross-session lineage. A replay artifact that omits these dimensions may still be useful, but its adequacy for operational cognition audit remains bounded.

## Public proof requires bounded claims

Public replayability audits should only claim what public evidence supports. Observed mechanisms, inferred coverage, hypotheses, and unresolved gaps must be labeled separately. Placeholder MCP consultation is advisory only.

## Replay gaps should become evidence requirements, not accusations

Replayability gaps should be framed as evidence requirements for stronger audits. They should not be framed as proof of target-system defects, security issues, or inferiority.

## Minimum replay bundle for operational cognition audits

A minimum replay bundle for operational cognition audits should include:

- transcript
- tool/action log
- tool results
- environment snapshot references
- memory/context snapshot references
- runtime configuration
- recovery/retry loop trace
- source hashes
- lineage summary

The bundle should also record redaction, truncation, and omission boundaries so later auditors can distinguish missing state from intentionally withheld state.
