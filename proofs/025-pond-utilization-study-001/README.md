# Pond Utilization Study 001

## What Was Tested

This proof tested six /consult protocols across three existing proof packs:

- Historical causal traceback: `proofs/022-challenger-causal-traceback`
- Software architecture reconstruction: `proofs/023-truth-reconstruction-challenge-002`
- Scientific contradiction mapping: `proofs/024-alzheimers-contradiction-atlas`

Each protocol was scored against a no-consult baseline using hostile criteria. Consults only received credit for valid direction changes, contradiction or evidence-cluster recovery, unsupported-claim reduction, lineage improvement, premature-convergence avoidance, or false-path abandonment.

The new live consult calls in this study all returned `pond_backed` bounded responses, but most were compacted to pressure rankings and claim-boundary fields. The scoring therefore caps credit by response-side specificity and relies on the existing proof audits for public verification.

## Best Protocol

Best average protocol: Protocol E - Contradiction-First Consult with `net_value_score=1.4`.

The strongest operating pattern is contradiction-first consultation at decision gates, followed by recovery-only consults when a specific failed path is visible, and a final late audit for claim boundaries.

## Failed Protocols

Lowest raw discovery score: Protocol D - Periodic Pressure Consult with `net_value_score=-0.45`. This is not a reason to ban pressure consults; it means scheduled consults become negative when they are not tied to falsifiable decision gates.

Worst operational prompt pattern: Protocol C - Early Planning Consult in its broad form. Broad early planning and periodic science pressure failed most often. They produced generic pressure, repeated baseline-visible facts, or prompt-side leakage. Late audit was useful but should not be counted as discovery.

## Current Pond Role

The pond currently behaves best as:

- Auditor: strong for claim-boundary and unsupported-claim reduction.
- Search accelerator: observed in the software architecture task where CSI displaced SSA.
- Weak-signal router: useful when the query names a concrete failed path or conflicting ranking.
- Cognitive continuity layer: bounded support where prior lineage resembles the current failure mode.

It is not a standalone historical, biomedical, or software-history authority. Scientific source claims still require public source IDs and independent verification.

## Recommended Next Experiment

Run an E/F/B hybrid against new unseen tasks with a control arm that uses the same adversarial questions without /consult. Pre-register baseline state, allowed prompts, and scoring before any consult response is seen.
