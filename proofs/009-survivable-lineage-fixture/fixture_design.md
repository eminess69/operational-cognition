# Fixture Design

## Design Goal

The fixture is a synthetic public bundle that makes the Proof 008 validation plan executable. It compares visible-only replay with full-lineage replay for the same short scenario.

## Scenario Requirements Covered

| Requirement | Fixture implementation |
| --- | --- |
| One user task | `T-001` asks for a safe config update only if runtime environment is staging. |
| One tool-dependent decision | `A-004` writes a no-op note because `TR-002` and `TR-003` show production guard conditions. |
| One explicit contradiction/correction | `C-001` resolves stale repo note `TR-001` against current runtime result `TR-002`. |
| One memory write | `ML-001` writes the user safety rule as `MEM-001`. |
| One later memory recall | `ML-002` recalls `MEM-001` before the guarded patch attempt. |
| One compression/summary boundary | `S-001` compresses `E-001` through `E-008`. |
| One omitted range | `O-001` omits detailed memory, tool, and contradiction events. |
| One environment dependency | `ENV-001` records production runtime state and the config hash. |
| One recovery/retry transition | `R-001` changes the trajectory after `TR-003` blocks a dry-run patch. |
| One later lineage-dependent action | `A-004` depends on runtime evidence, recalled memory, contradiction resolution, and recovery state. |

## Replay Comparison

Visible-only replay uses transcript turns, visible event order, and high-level action sequence. It should show that the agent did not modify config, but it should not fully reconstruct why that was safe.

Full-lineage replay uses transcript, events, tool results, memory, summary metadata, omitted ranges, contradiction refs, authority refs, temporal validity, environment snapshots, runtime config, recovery trace, provenance, and public lineage summary.

## Fixture Boundary

The fixture is intentionally synthetic. Its result can only validate fixture-level reconstructability. It cannot prove global sufficiency, target-system preservation, or target-system defects.
