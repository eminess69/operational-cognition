# Proof 026 - Premature Convergence Challenge

Status: `complete`

Domain: Boeing 737 MAX.

Question: What was the primary failure mechanism?

The proof separates a no-consult baseline from a Protocol E consult run. Consultation was forbidden during data gathering and used only after the baseline had a leading answer.

Key artifacts:

- `baseline/hypothesis_rankings.json`
- `baseline/evidence_clusters.json`
- `baseline/convergence_log.json`
- `baseline/final_verdict.md`
- `decision_gate_log.jsonl`
- `consult/hypothesis_rankings.json`
- `consult/evidence_clusters.json`
- `consult/final_verdict.md`
- `delta/consult_vs_baseline_report.json`
- `metrics.json`

Primary result: `premature_convergence_resistance` improved from 3 to 6 active explanations before final convergence.

Boundary: consult responses are advisory contradiction pressure only. Public engineering/history claims are grounded in `source_corpus.json`.
