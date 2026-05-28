# Fixture Public Lineage Summary

This fixture converts a redacted-real local Proof 013 gate-repair trace into a public-safe replay bundle.

The visible baseline contains only the transcript-level task/correction sequence and event order. The full-lineage mode adds tool actions, result hashes, authority refs, omitted-range refs, temporal validity, environment refs, and recovery events.

No credentials, hidden chain-of-thought, private substrate internals, or target-system private internals are included. Local paths are retained only as environment dependency refs needed to reconstruct which checkout and MCP endpoint were used.
