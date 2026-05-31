# Truth Reconstruction Challenge 002

Target: `kubernetes/kubernetes`

Baseline was run first under `baseline/` with no Inside Voice consultation. The consult run then used five `/consult` calls under `consult/inside_voice_consults/`.

Result: consultation changed the investigation direction. The baseline selected CRI, CRDs, and Server-Side Apply. The consult phase recovered CSI as the stronger third architectural decision, then public Kubernetes sources verified the recovered lineage.

Required artifacts:

- `consultation_log.jsonl`
- `architecture_truth_map.json`
- `lost_context_recovery.json`
- `memory_dependency_report.json`
- `architectural_narrative.md`

Public claim boundary: Inside Voice output is advisory memory/lineage pressure only. Historical claims are grounded in public Kubernetes sources.
