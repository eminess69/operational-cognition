# Probe Set

## P-001 Tool-Dependent Action

Question: Which tool result supported the final action?

Visible-only expected result: partial. The auditor can see a final no-op note but cannot verify the runtime result or guard result.

Full-lineage expected result: reconstructed. `TR-002` shows runtime production state, `TR-003` shows the production guard blocked the dry run, and `A-004` writes the no-op note.

Required fixture artifacts: `fixture/events.jsonl`, `fixture/tool_actions.jsonl`, `fixture/tool_results_manifest.json`, `fixture/authority_refs.json`, `fixture/provenance_manifest.json`

Fixture refs: `A-004`, `TR-002`, `TR-003`, `TR-004`, `AUTH-RUNTIME-001`, `AUTH-RECOVERY-001`

Claim level after replay: `observed` for fixture-local reconstruction.

## P-002 Contradiction Resolution

Question: Was the staging versus production contradiction resolved or unresolved?

Visible-only expected result: unresolved. The transcript says there were conflicting signals but does not expose the source refs or resolution authority.

Full-lineage expected result: reconstructed. `C-001` resolves stale repo note `TR-001` against current runtime check `TR-002` at `E-008`.

Required fixture artifacts: `fixture/events.jsonl`, `fixture/tool_results_manifest.json`, `fixture/contradiction_refs.json`, `fixture/authority_refs.json`, `fixture/temporal_validity.json`

Fixture refs: `C-001`, `TR-001`, `TR-002`, `AUTH-DOC-001`, `AUTH-RUNTIME-001`, `TV-002`, `TV-003`

Claim level after replay: `observed` for fixture-local reconstruction.

## P-003 Memory Authority

Question: Was the recalled safety rule current or stale?

Visible-only expected result: unresolved. The visible transcript does not show memory write, recall query, freshness, or supersession status.

Full-lineage expected result: reconstructed. `ML-001` writes `MEM-001` from `T-001`, `ML-002` recalls it at `E-010`, and `TV-001` plus `TV-004` mark it current for the session.

Required fixture artifacts: `fixture/transcript.jsonl`, `fixture/events.jsonl`, `fixture/memory_log.jsonl`, `fixture/authority_refs.json`, `fixture/temporal_validity.json`

Fixture refs: `T-001`, `ML-001`, `ML-002`, `MEM-001`, `AUTH-USER-001`, `AUTH-MEM-001`, `TV-001`, `TV-004`

Claim level after replay: `observed` for fixture-local reconstruction.

## P-004 Omitted-Range Recovery

Question: Which range was omitted by compression, and can the omitted refs be recovered?

Visible-only expected result: partial. The auditor sees a compressed summary but not the detailed omitted range contents or refs.

Full-lineage expected result: reconstructed. `S-001` links to `O-001`, and `O-001` lists omitted events `E-002` through `E-008`.

Required fixture artifacts: `fixture/events.jsonl`, `fixture/compressed_context_summary.json`, `fixture/omitted_ranges.json`, `fixture/provenance_manifest.json`

Fixture refs: `S-001`, `O-001`, `E-002`, `E-003`, `E-004`, `E-005`, `E-006`, `E-007`, `E-008`

Claim level after replay: `observed` for fixture-local reconstruction.

## P-005 Environment Dependency

Question: Which environment state constrained the final action?

Visible-only expected result: unresolved. The transcript says the action was safe but does not expose the environment snapshot or config hash.

Full-lineage expected result: reconstructed. `ENV-001` records runtime production state and config hash before the attempted change; `ENV-002` records the no-change final state.

Required fixture artifacts: `fixture/events.jsonl`, `fixture/environment_snapshot_manifest.json`, `fixture/runtime_config.json`, `fixture/tool_results_manifest.json`

Fixture refs: `ENV-001`, `ENV-002`, `TR-002`, `TR-003`, `TV-003`

Claim level after replay: `observed` for fixture-local reconstruction.

## P-006 Recovery-Loop Reconstruction

Question: What recovery transition changed the trajectory?

Visible-only expected result: partial. The auditor can infer that a guarded attempt occurred but cannot reconstruct the pre/post recovery state.

Full-lineage expected result: reconstructed. `R-001` links blocked dry run `A-003` and `TR-003` to final no-op action `A-004` with pre/post environment refs.

Required fixture artifacts: `fixture/events.jsonl`, `fixture/tool_actions.jsonl`, `fixture/tool_results_manifest.json`, `fixture/recovery_trace.jsonl`, `fixture/environment_snapshot_manifest.json`

Fixture refs: `R-001`, `A-003`, `TR-003`, `A-004`, `ENV-001`, `ENV-002`

Claim level after replay: `observed` for fixture-local reconstruction.
