from __future__ import annotations

import json
from pathlib import Path

from tools.integrations.run_consult_failure_boundary_gauntlet import (
    build_case_bundle,
    build_consult_response,
    compare_consult_runs,
    context_flood_cases,
    evaluate_response,
    run_determinism_under_load,
    run_gauntlet,
)


def test_failure_boundary_gauntlet_writes_operating_envelope(tmp_path: Path) -> None:
    report = run_gauntlet(tmp_path)

    assert report["acceptance"]["passed"] is True
    assert report["hard_failures"] == []
    assert report["metrics"]["determinism_match"] == 1.0
    assert report["metrics"]["traceback_completeness"] == 1.0
    assert report["metrics"]["false_recall_rate"] == 0.0
    assert report["metrics"]["contamination_rate"] == 0.0
    assert report["metrics"]["noise_resilience_score"] == 1.0
    assert report["metrics"]["boundary_threshold"]["classification"] == "CONTEXT_DUMP"

    expected_artifacts = [
        "consult_failure_boundary_report.json",
        "consult_failure_boundary_report.md",
        "consult_failure_boundary_responses.jsonl",
        "suite_metrics.json",
        "determinism_under_load.json",
        "noise_resilience_curve.json",
        "recursive_seasoning_report.json",
        "context_flood_boundary.json",
    ]
    for name in expected_artifacts:
        path = tmp_path / name
        assert path.is_file()
        assert path.stat().st_size > 0

    persisted = json.loads((tmp_path / "consult_failure_boundary_report.json").read_text(encoding="utf-8"))
    assert persisted["answers"]["what_conditions_cause_consult_to_stop_behaving_like_best_path_retrieval"]
    assert persisted["answers"]["where_is_the_operational_envelope_of_the_pond"]


def test_ambiguous_queries_emerge_as_top_k_paths() -> None:
    cases = [case for case in build_case_bundle() if case.suite_id == "ambiguous_query"]

    for case in cases:
        response = build_consult_response(case)
        metrics = evaluate_response(case, response)

        assert metrics["classification"] == "TOP_K_PATHS"
        assert metrics["path_ambiguity"] >= 2
        assert metrics["traceback_completeness"] == 1.0


def test_contradiction_suite_keeps_lineages_separated() -> None:
    case = next(case for case in build_case_bundle() if case.suite_id == "contradiction")
    response = build_consult_response(case)
    metrics = evaluate_response(case, response)

    assert metrics["classification"] == "TOP_K_PATHS"
    assert response["boundary_signals"]["contradiction_detected"] is True
    assert len(response["boundary_signals"]["contradiction_attribution"]) == 2
    assert metrics["contamination"] is False
    assert metrics["hard_failures"] == []


def test_context_flood_identifies_best_top_k_and_dump_boundaries() -> None:
    classifications = []
    relevant_counts = []

    for case in context_flood_cases():
        response = build_consult_response(case)
        metrics = evaluate_response(case, response)
        classifications.append(metrics["classification"])
        relevant_counts.append(response["boundary_signals"]["candidate_relevant_item_count"])

    assert classifications[0] == "BEST_PATH"
    assert "TOP_K_PATHS" in classifications
    assert "CONTEXT_DUMP" in classifications
    assert relevant_counts[classifications.index("CONTEXT_DUMP")] == 32


def test_stale_missing_current_is_under_context_not_false_recall() -> None:
    case = next(case for case in build_case_bundle() if case.case_id == "stale_missing_current_recommendation")
    response = build_consult_response(case)
    metrics = evaluate_response(case, response)

    assert metrics["classification"] == "UNDER_CONTEXT"
    assert response["boundary_signals"]["missing_required_evidence"] == ["ST-NEW-001", "lineage.recall_policy_2026"]
    assert metrics["false_recall"] is False
    assert metrics["hard_failures"] == []


def test_adversarial_motifs_do_not_induce_false_recall() -> None:
    case = next(case for case in build_case_bundle() if case.suite_id == "adversarial_motif")
    response = build_consult_response(case)
    metrics = evaluate_response(case, response)

    assert metrics["classification"] == "BEST_PATH"
    assert metrics["false_recall"] is False
    assert "lineage.target_phase_recall" in metrics["selected_lineage_ids"]
    assert "lineage.decoy_phase_recall_elsewhere" not in metrics["selected_lineage_ids"]


def test_recursive_seasoning_has_no_selected_derived_output_or_drift(tmp_path: Path) -> None:
    report = run_gauntlet(tmp_path)
    recursive = report["operating_envelope"]["recursive_seasoning"]

    assert recursive["monotonic_drift"] is False
    assert recursive["max_drift_score"] == 0.0
    assert recursive["contamination_rate"] == 0.0
    assert all(record["classification"] == "BEST_PATH" for record in recursive["records"])


def test_determinism_under_load_matches_hashes_rankings_and_tracebacks() -> None:
    case = next(case for case in build_case_bundle() if case.suite_id == "determinism_under_load")
    report = run_determinism_under_load(case, repetitions=100)

    assert report["determinism_match"] == 1.0
    assert report["hashes_identical"] is True
    assert report["rankings_identical"] is True
    assert report["tracebacks_identical"] is True
    assert report["comparison_failures"] == []


def test_single_case_ranking_hash_and_tracebacks_are_deterministic() -> None:
    case = next(case for case in build_case_bundle() if case.case_id == "noise_100x_irrelevant")
    first = build_consult_response(case)
    second = build_consult_response(case)
    comparison = compare_consult_runs(first, second)

    assert comparison["deterministic_match"] is True
    assert first["response_hash"] == second["response_hash"]
    assert first["ranked_context_items"] == second["ranked_context_items"]
