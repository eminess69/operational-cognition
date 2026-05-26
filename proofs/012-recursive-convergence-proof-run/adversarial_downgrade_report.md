# Adversarial Downgrade Report

## Claims That Remain Inferred

| Claim | Reason it remains inferred |
| --- | --- |
| C-001: Survivable lineage is the strongest recurring corpus-level requirement. | The convergence is repeated across public proof artifacts, but centrality may be influenced by proof design and taxonomy reuse. |
| C-002: Visible replay is insufficient for causal operational replay. | Proof 010 observes this in a synthetic fixture; the broader corpus-level claim is still an inference. |
| C-003: Compression can preserve utility while reducing replay fidelity. | Proof 003 and Proof 004 support the boundary, but not a universal compression-loss claim. |
| C-004: Memory persistence is not authority preservation. | Proof 006 defines authority requirements, but target-specific preservation is unresolved. |
| C-005: Contradiction and uncertainty survivability are required for operational truth. | The corpus supports the audit requirement, but not a target-system guarantee. |
| C-006: Environment and recovery state are necessary causal replay dimensions. | These dimensions recur in the corpus and fixture, but complete causal adequacy is not globally validated. |
| C-008: A real/redacted trace is required for stronger external validation. | The requirement follows from the fixture boundary and Proof 011 unresolved requirements; no eligible trace has been executed. |

## Claims That Remain Hypothesis-Level

| Claim | Reason it remains hypothesis-level |
| --- | --- |
| The Proof 007 minimum operational replay bundle is sufficient. | Proof 010 supports the bundle at synthetic fixture scope only. The bundle may be incomplete, excessive, or overfit. |
| A future public or redacted-real trace will reproduce the same visible-only versus full-lineage separation. | Proof 011 defines the path but no eligible candidate has been selected or executed. |
| The same convergence would appear in a corpus not designed around survivable lineage terminology. | Alternative-explanation pressure remains unresolved until independent trace validation. |

## Claims That Remain Unresolved

| Claim | Reason it remains unresolved |
| --- | --- |
| Any target system globally preserves survivable lineage. | No target-system replay validation has been run. |
| Any target system fails to preserve survivable lineage. | The proof corpus is not a defect claim and does not evaluate private target behavior. |
| The synthetic fixture is hard enough to establish external validity. | The fixture may be aligned with the expected answer. |
| The current MCP adapter output reflects live cognition rather than placeholder contract behavior. | The adapter status is `placeholder`. |

## Claims That Cannot Be Made Publicly

- Proof 010 validates survivable lineage beyond the synthetic fixture.
- Survivable lineage has been validated globally.
- The corpus proves any target-system preservation or failure claim.
- MCP placeholder output is evidence for target-system behavior.
- Private implementation details are needed to accept the public conclusion.

## Reasons Not to Overclaim

Proof 010 is synthetic fixture validation only.

The central claim survives as an inferred corpus-level requirement, not as observed global truth. The strongest public move is to keep survivable lineage as the leading implementation-neutral requirement and make the next validation requirement explicit: run the same visible-only versus full-lineage method against a public or redacted-real trace.
