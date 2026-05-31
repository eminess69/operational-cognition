# Proof 024 - Alzheimer's Contradiction Atlas

Status: `complete`

This proof separates a no-consult baseline from a consult-triggered reconstruction run. The task is evidence-lineage and contradiction mapping, not diagnosis, treatment recommendation, cure claim, or clinical guidance.

Corpus: `source_corpus.json` contains PubMed peer-reviewed records plus official/institutional summaries. Baseline artifacts live under `baseline/`. Consult artifacts live under `consult/`. Delta audit lives under `delta/`.

Consult endpoint used for Phase B: `http://127.0.0.1:8767/consult`.

Public boundary: Inside Voice output is advisory pressure and lineage support only. Biomedical claims are grounded in source IDs from `source_corpus.json`.
