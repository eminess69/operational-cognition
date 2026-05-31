# Consult Failure Boundary Gauntlet

This gauntlet measures when `/consult` stops behaving like BEST_PATH retrieval. It is a controlled, deterministic stress harness: each case has known oracle lineages, source trace refs, artifact hashes, and expected boundary behavior.

The output root is:

```bash
artifacts/integrations/consult_failure_boundary
```

## Test Families

The runner covers nine stress families:

- `ambiguous_query`: short prompts with multiple valid lineages, including "Improve recall.", "Optimize routing.", and "Fix compression issue."
- `contradiction`: competing evidence for "Phase routing improves accuracy" and "Phase routing harms accuracy."
- `stale_context`: older and newer lineage probes, plus an explicit missing-current-lineage UNDER_CONTEXT case.
- `noise_injection`: 10x, 50x, and 100x irrelevant pond artifacts.
- `duplicate_lineage`: many near-identical paths competing with a canonical record.
- `adversarial_motif`: decoy motifs with shared terms and structure but different provenance.
- `context_flood`: increasing relevant context scale to find BEST_PATH -> TOP_K_PATHS -> CONTEXT_DUMP boundaries.
- `recursive_seasoning`: 10, 50, 100, and 250 cycles of consult output re-ingestion.
- `determinism_under_load`: 100 identical consult runs.

## Classifications

- `BEST_PATH`: one dominant lineage is selected with bounded supporting records.
- `TOP_K_PATHS`: multiple relevant lineages are retained as a bounded set.
- `UNDER_CONTEXT`: required current or critical evidence is absent.
- `CONTEXT_DUMP`: relevant context scale exceeds the configured bounded retrieval threshold.
- `FALSE_RECALL`: the wrong lineage is selected.
- `CONTAMINATION`: contradictory or recursively derived lineage leaks into the selected answer.
- `NONDETERMINISTIC`: identical input produces different ranking, hashes, or tracebacks.

## Required Metrics

The final report includes:

- `best_path_rate`
- `top_k_rate`
- `context_dump_rate`
- `false_recall_rate`
- `contamination_rate`
- `noise_resilience_score`
- `boundary_threshold`
- `traceback_completeness`
- `ranking_stability`
- `determinism_match`
- `token_efficiency`
- `latency_degradation`

## Hard Fail Conditions

The run fails if any of these occur:

- False recall without attribution.
- Contamination between contradictory lineages.
- Determinism below 100%.
- Traceback completeness below 100%.
- Recursive seasoning causes monotonic drift.
- Context dump appears below the configured relevance threshold.

## Artifacts

The runner writes:

- `consult_failure_boundary_report.json`
- `consult_failure_boundary_report.md`
- `consult_failure_boundary_responses.jsonl`
- `suite_metrics.json`
- `determinism_under_load.json`
- `noise_resilience_curve.json`
- `recursive_seasoning_report.json`
- `context_flood_boundary.json`

The JSON report answers:

- "What conditions cause consult to stop behaving like BEST_PATH retrieval?"
- "Where is the operational envelope of the pond?"

## Validation

```bash
python3 -m pytest -q tests/integrations/test_consult_failure_boundary_gauntlet.py
python3 tools/integrations/run_consult_failure_boundary_gauntlet.py --out artifacts/integrations/consult_failure_boundary
git diff --check
```
