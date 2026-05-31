# Consult Selectivity Measurement

This measurement checks whether `/consult` behaves like a selective lineage retriever or like an oversized context dump.

The controlled bundle contains eight targeted tasks and a larger pond fixture with unrelated proof, UI, CI, document, presentation, and spreadsheet context. Each task has a known small set of required lineage ids and item ids. The harness compares:

1. Full pond/context dump.
2. Naive keyword retrieval.
3. Inside Voice ranked consult output.

## Response Contract

Every measured consult response must include:

- `request_id`
- `query`
- `task`
- `selected_path_ids`
- `ranked_context_items`
- `source_trace_refs`
- `relevance_scores`
- `excluded_context_summary`
- `response_hash`
- `verdict`

Each `ranked_context_items` entry must include `item_id`, `path_id`, `lineage_id`, `source_trace_ref`, `artifact_lineage.artifact_ref`, `artifact_lineage.artifact_hash`, `relevance_score`, and `token_estimate`.

## Metrics

The harness records these per response:

- `response_token_estimate`
- `number_of_recalled_items`
- `number_of_distinct_lineages`
- `relevance_score_per_item`
- `top_path_score`
- `irrelevant_item_count`
- `duplicate_or_redundant_item_count`
- `traceback_completeness`
- `compression_ratio_vs_full_context`
- `answer_quality_delta`

The baseline comparison records:

- `token_reduction_vs_full_dump`
- `relevance_precision`
- `lineage_completeness`
- `deterministic_ranking_match`
- `task_success_delta`
- `context_efficiency_score`

## Classifications

- `BEST_PATH`: one primary ranked lineage plus minimal supporting evidence.
- `TOP_K_PATHS`: a bounded ranked set of relevant paths.
- `CONTEXT_DUMP`: broad context with weak or no task relevance, or insufficient token reduction.
- `UNDER_CONTEXT`: omitted required lineage or required items.
- `INVALID`: missing tracebacks, hashes, metadata, or deterministic ranking.

## Hard Fail Conditions

The run fails if any consult response has:

- Any recalled item without source trace or artifact lineage.
- More than 20% irrelevant context by token estimate.
- No deterministic response hash.
- Different ranking for the same query and configuration.
- Full context dump output when a bounded path exists.

## Acceptance Criteria

The ranked consult output passes only if:

- Context size is reduced by at least 50% versus the full dump.
- Relevance precision is at least 0.80.
- Traceback completeness is 100%.
- Deterministic ranking match is 100%.
- Targeted tasks are not classified as `CONTEXT_DUMP`.

## Validation

```bash
PYTHONPATH=. python3 -m pytest -q tests/integrations/test_consult_selectivity.py
PYTHONPATH=. python3 tools/integrations/measure_consult_selectivity.py --out artifacts/integrations/consult_selectivity
git diff --check
```

## Artifacts

The measurement writes:

- `artifacts/integrations/consult_selectivity/consult_selectivity_report.json`
- `artifacts/integrations/consult_selectivity/consult_selectivity_report.md`
- `artifacts/integrations/consult_selectivity/consult_responses.jsonl`
- `artifacts/integrations/consult_selectivity/context_exclusion_audit.jsonl`
- `artifacts/integrations/consult_selectivity/determinism_report.json`

The report's `answer` field directly answers whether `/consult` is returning best-path lineage, bounded top-k lineage, or context dumps.
