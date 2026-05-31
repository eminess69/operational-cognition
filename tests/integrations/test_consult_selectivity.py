from __future__ import annotations

import json
from pathlib import Path

from tools.integrations.measure_consult_selectivity import (
    build_consult_response,
    build_context_dump_response,
    build_controlled_context,
    build_task_bundle,
    compare_consult_runs,
    evaluate_consult_response,
    response_hash,
    run_measurement,
    validate_response_contract,
)


def test_controlled_measurement_passes_acceptance(tmp_path: Path) -> None:
    report = run_measurement(tmp_path)

    assert report["acceptance"]["passed"] is True
    assert report["answer"] == "BEST_PATH"
    assert report["aggregate"]["hard_failures"] == []
    assert report["aggregate"]["verdict_counts"] == {"BEST_PATH": 8}
    assert report["baseline_aggregates"]["inside_voice_ranked"]["token_reduction_vs_full_dump_min"] >= 0.50
    assert report["baseline_aggregates"]["inside_voice_ranked"]["relevance_precision_min"] >= 0.80
    assert report["baseline_aggregates"]["inside_voice_ranked"]["traceback_completeness_min"] == 1.0
    assert report["baseline_aggregates"]["inside_voice_ranked"]["deterministic_ranking_match_rate"] == 1.0

    expected_artifacts = [
        "consult_selectivity_report.json",
        "consult_selectivity_report.md",
        "consult_responses.jsonl",
        "context_exclusion_audit.jsonl",
        "determinism_report.json",
    ]
    for name in expected_artifacts:
        assert (tmp_path / name).is_file()
        assert (tmp_path / name).stat().st_size > 0

    responses = [json.loads(line) for line in (tmp_path / "consult_responses.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len(responses) == 8
    assert all(response["verdict"] == "BEST_PATH" for response in responses)


def test_response_contract_fields_are_traceable() -> None:
    context = build_controlled_context()
    task = build_task_bundle()[0]
    response = build_consult_response(task, context)

    assert validate_response_contract(response) == []
    assert response["response_hash"] == response_hash(response)
    assert response["selected_path_ids"] == ["path.claim_boundary"]
    assert response["ranked_context_items"]
    assert all(item["source_trace_ref"] for item in response["ranked_context_items"])
    assert all(item["artifact_lineage"]["artifact_hash"] for item in response["ranked_context_items"])

    metrics = evaluate_consult_response(task, context, response, deterministic_ranking_match=True)
    assert metrics["verdict"] == "BEST_PATH"
    assert metrics["traceback_completeness"] == 1.0
    assert metrics["lineage_completeness"] == 1.0


def test_context_dump_is_classified_as_dump_for_targeted_task() -> None:
    context = build_controlled_context()
    task = build_task_bundle()[0]
    response = build_context_dump_response(task, context)

    metrics = evaluate_consult_response(task, context, response, deterministic_ranking_match=True)

    assert metrics["verdict"] == "CONTEXT_DUMP"
    assert metrics["irrelevant_token_ratio"] > 0.20
    assert any("Full context dump returned" in failure for failure in metrics["hard_failures"])


def test_missing_traceback_is_invalid() -> None:
    context = build_controlled_context()
    task = build_task_bundle()[0]
    response = build_consult_response(task, context)
    response["ranked_context_items"][0]["source_trace_ref"] = ""
    response["source_trace_refs"][0] = ""
    response["response_hash"] = response_hash(response)

    metrics = evaluate_consult_response(task, context, response, deterministic_ranking_match=True)

    assert metrics["verdict"] == "INVALID"
    assert metrics["traceback_completeness"] < 1.0
    assert any("source trace or artifact lineage" in failure for failure in metrics["hard_failures"])


def test_ranked_consult_is_deterministic_for_same_query_and_config() -> None:
    context = build_controlled_context()

    for task in build_task_bundle():
        first = build_consult_response(task, context)
        second = build_consult_response(task, context)
        comparison = compare_consult_runs(first, second)

        assert comparison["deterministic_ranking_match"] is True
        assert first["response_hash"] == second["response_hash"]
        assert first["ranked_context_items"] == second["ranked_context_items"]
