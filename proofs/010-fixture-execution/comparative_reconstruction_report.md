# Comparative Reconstruction Report

## Status

This is fixture-level validation only.

## Method

Visible-only replay used transcript, visible event order, and high-level action sequence.

Full-lineage replay used the complete fixture bundle.

## Results

| Probe | Visible-only | Full-lineage | Improvement | Interpretation |
| --- | --- | --- | --- | --- |
| P-001 tool-dependent action | partially_reconstructed | reconstructed | yes | Full lineage identifies the runtime and guard results behind the final no-op action. |
| P-002 contradiction resolution | unresolved | reconstructed | yes | Full lineage resolves the stale repository note against current runtime evidence. |
| P-003 memory authority | unresolved | reconstructed | yes | Full lineage shows the remembered rule was user-derived and current. |
| P-004 omitted-range recovery | partially_reconstructed | reconstructed | yes | Full lineage recovers the omitted event range behind the compressed summary. |
| P-005 environment dependency | unresolved | reconstructed | yes | Full lineage identifies the production environment state and no-change final state. |
| P-006 recovery-loop reconstruction | partially_reconstructed | reconstructed | yes | Full lineage reconstructs the blocked dry run and safe fallback transition. |

## Finding

Full-lineage replay reconstructed all six fixture probes, while visible-only replay left several probes partial or unresolved.

Claim level: `observed` for fixture-local result.

## Boundary

This validates the fixture-level survivable-lineage claim only.
It does not prove universal sufficiency.
It does not evaluate OpenClaw or OpenHands.
It does not expose private substrate internals.

## Next step

Run the same fixture method against a public real-world or redacted-real trace.
