# Visible-Only Replay Mode

## Inputs

Visible-only replay is limited to:

- transcript turns in `fixture/transcript.jsonl`
- visible event order from `fixture/events.jsonl`
- high-level action sequence from `fixture/tool_actions.jsonl`

## What Is Reconstructable

An auditor can reconstruct that the user requested a safe config update, the agent checked environment-related state, context was compressed, a guarded attempt occurred, and the final visible outcome was a no-op note rather than a config change.

## Expected Unresolved Areas

Visible-only replay should leave these areas unresolved or partial:

- why the later action was safe
- whether recalled memory was current
- which contradiction was resolved
- what exact tool result supported the action
- what environment state constrained the action
- what recovery transition changed the trajectory
- which source gave the final action operational authority

## Boundary

Visible-only replay remains useful for sequence review. It is not expected to support causal reconstruction for this fixture.
