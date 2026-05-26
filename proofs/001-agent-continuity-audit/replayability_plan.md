# Replayability Plan

This proof must be replayable from public artifacts.

## Required Replay Materials

- source snapshot list
- evidence manifest
- hashable artifacts
- explicit hypothesis labels
- public lineage summaries
- deterministic proof manifest validation

## Replay Method

1. Record each public source used in the investigation.
2. Capture retrieval metadata and content hashes where practical.
3. Distinguish observed source content from interpretation.
4. Preserve contradictions and unresolved uncertainty.
5. Validate `proof_manifest.json` against the public schema.
6. Reconstruct investigation steps from public lineage summaries without relying on private substrate internals.

## Non-Replayable Material

Private consultation artifacts, Belief Ledger internals, Inside Voice implementation details, hidden reasoning chains, and substrate state are outside the public replay boundary.
