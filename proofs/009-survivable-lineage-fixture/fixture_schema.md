# Fixture Schema

## Shared Rules

Every fixture file uses stable IDs and public-safe content. JSONL files contain one JSON object per non-empty line. JSON files contain a single object.

All cross-file refs are fixture-local IDs. Required ID prefixes are:

- `T-` transcript turns
- `E-` events
- `A-` tool actions
- `TR-` tool results
- `ML-` memory log entries
- `MEM-` memory entries
- `S-` compressed summaries
- `O-` omitted ranges
- `C-` contradiction refs
- `AUTH-` authority refs
- `TV-` temporal validity refs
- `ENV-` environment snapshots
- `R-` recovery transitions

## Required Files

| File | Required primary IDs |
| --- | --- |
| `fixture/transcript.jsonl` | `turn_id`, `event_id` |
| `fixture/events.jsonl` | `event_id` |
| `fixture/tool_actions.jsonl` | `action_id`, `event_id`, `result_ref` |
| `fixture/tool_results_manifest.json` | `tool_results[].result_id` |
| `fixture/memory_log.jsonl` | `memory_event_id`, `memory_id`, `event_id` |
| `fixture/compressed_context_summary.json` | `summary_id`, `event_id`, `omitted_range_refs` |
| `fixture/omitted_ranges.json` | `omitted_ranges[].omitted_range_id` |
| `fixture/contradiction_refs.json` | `contradictions[].contradiction_id` |
| `fixture/authority_refs.json` | `authority_refs[].authority_id` |
| `fixture/temporal_validity.json` | `temporal_refs[].temporal_id` |
| `fixture/environment_snapshot_manifest.json` | `snapshots[].snapshot_id` |
| `fixture/runtime_config.json` | `runtime_config_id` |
| `fixture/recovery_trace.jsonl` | `recovery_event_id`, `event_id` |
| `fixture/provenance_manifest.json` | `fixture_id`, `artifact_hashes` |

## Resolver Expectations

The validator resolves transcript event refs, tool result refs, memory refs, summary omitted-range refs, contradiction authority and temporal refs, environment snapshot refs, recovery refs, and probe refs where practical.

`fixture/provenance_manifest.json` must include SHA-256 hashes for public fixture artifacts other than itself. The validator verifies those hashes against local file contents.
