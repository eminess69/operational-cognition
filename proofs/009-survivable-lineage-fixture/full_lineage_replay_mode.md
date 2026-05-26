# Full-Lineage Replay Mode

## Inputs

Full-lineage replay uses every fixture artifact:

- transcript
- event log
- tool/action log
- tool result hashes
- memory write/recall log
- compressed context summary
- omitted-range refs
- contradiction refs
- authority refs
- temporal validity metadata
- environment snapshot refs
- runtime config
- recovery/retry trace
- provenance manifest
- public lineage summary

## Required Reconstructable Claims

| Claim | Fixture refs |
| --- | --- |
| Tool result supported the final action. | `A-004`, `TR-002`, `TR-003`, `TR-004`, `AUTH-RUNTIME-001`, `AUTH-RECOVERY-001` |
| Memory recall was current, not stale. | `ML-001`, `ML-002`, `MEM-001`, `TV-001`, `TV-004` |
| Contradiction was resolved. | `C-001`, `TR-001`, `TR-002`, `AUTH-DOC-001`, `AUTH-RUNTIME-001`, `E-008` |
| Compressed summary omitted a specific range. | `S-001`, `O-001`, `E-002`, `E-008` |
| Environment state constrained the action. | `ENV-001`, `TV-003`, `TR-002`, `TR-003` |
| Recovery retry changed trajectory. | `R-001`, `A-003`, `TR-003`, `A-004` |
| Final action authority came from specific sources. | `AUTH-USER-001`, `AUTH-RUNTIME-001`, `AUTH-RECOVERY-001`, `A-004` |

## Boundary

Full-lineage replay is expected to reconstruct this fixture. Passing this fixture would be fixture-level validation only.
