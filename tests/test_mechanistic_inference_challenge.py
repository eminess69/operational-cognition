from __future__ import annotations

import json
from pathlib import Path

from operational_cognition.cli.mechanism_pond import answer_question, load_pond


ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT / "proofs" / "032-mechanistic-inference-challenge"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_proof_032_metrics_and_hostile_boundary() -> None:
    metrics = load_json(PROOF / "analysis" / "mechanistic_inference_metrics.json")
    hostile = load_json(PROOF / "analysis" / "hostile_mechanistic_inference_audit.json")

    assert metrics["consequence_only_accuracy"] == 1.0
    assert metrics["reordered_accuracy"] == 1.0
    assert metrics["missing_roles_accuracy"] == 1.0
    assert metrics["multicause_accuracy"] == 1.0
    assert metrics["novel_surface_accuracy"] == 1.0
    assert metrics["fail_closed_rate"] == 1.0
    assert metrics["hidden_cause_inference_rate"] == 1.0
    assert metrics["deterministic_replay_match"] is True
    assert hostile["hostile_verdict"] == "WEAK_SIGNAL"
    assert hostile["remaining_template_explanation"] is True
    assert hostile["remaining_parser_explanation"] is True


def test_consequence_only_prompt_uses_consequence_inference() -> None:
    state = load_pond(PROOF / "pond_states" / "mechanism_inference")
    result = answer_question(
        "Observed system: The machine became noisy. Then slower. Then hotter. Then stopped. "
        "Question: Which learned mechanism category would naturally make this observation chain expected?",
        state,
    )

    assert result["status"] == "ANSWERED"
    assert result["identified_mechanism"] == "supported_rotation"
    assert result["inference_mode"] == "CONSEQUENCE_INFERENCE"
    assert len(result["consequence_features"]) >= 3
    assert len(result["matched_roles"]) < 3
    assert result["source_tracebacks"]


def test_multicause_results_expose_candidate_ranking() -> None:
    results = load_json(PROOF / "results" / "multicause_results.json")
    item = results["items"][0]

    assert item["status"] == "ANSWERED"
    assert item["candidate_mechanisms"]
    assert item["confidence_ranking"]
    assert item["confidence_ranking"][0]["rank"] == 1
    assert item["confidence_ranking"][0]["mechanism_id"] == item["identified_mechanism"]
    assert {"candidate_mechanisms": [], "confidence_ranking": []}.keys() <= item.keys()


def test_ambiguous_consequence_prompt_fails_closed() -> None:
    state = load_pond(PROOF / "pond_states" / "mechanism_inference")
    result = answer_question(
        "Observed system: The object changed. Question: Could any learned mechanism make this observation expected? "
        "Return FAIL_CLOSED if not enough evidence.",
        state,
    )

    assert result["status"] == "FAIL_CLOSED"
    assert result["identified_mechanism"] == ""
    assert result["inference_mode"] == "UNSUPPORTED"
