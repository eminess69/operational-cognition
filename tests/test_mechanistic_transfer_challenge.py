from __future__ import annotations

import json
from pathlib import Path

from operational_cognition.cli.mechanism_pond import answer_question, load_pond


ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT / "proofs" / "030-mechanistic-transfer-challenge"
PROOF_031 = ROOT / "proofs" / "031-mechanistic-transfer-cue-invariance"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_proof_030_metrics_and_hostile_boundary() -> None:
    metrics = load_json(PROOF / "analysis" / "mechanism_transfer_metrics.json")
    hostile = load_json(PROOF / "analysis" / "hostile_mechanism_audit.json")

    assert metrics["mechanism_transfer_rate"] == 1.0
    assert metrics["hidden_mechanism_transfer_rate"] == 1.0
    assert metrics["fail_closed_rate_on_unsupported_items"] == 1.0
    assert metrics["unseasoned_baseline_all_fail_closed"] is True
    assert hostile["hostile_verdict"] == "FAIL"
    assert hostile["failure_condition_triggered"] == "parser_explanation_survives"


def test_hidden_fan_mapping_uses_required_shape() -> None:
    state = load_pond(PROOF / "pond_states" / "mechanism_seasoned")
    result = answer_question(
        "Observed system: The room fan slows down over time, becomes noisy, and eventually stops. "
        "Question: What component category is most likely involved? Explain why.",
        state,
    )

    assert result["status"] == "ANSWERED"
    assert result["identified_mechanism"] == "supported_rotation"
    assert result["component_category"] == "rotational support interface"
    assert result["observed_system"]
    assert len(result["supporting_motifs"]) >= 3
    assert result["source_mechanism"] == "SUPPORTED_ROTATION"
    assert result["transfer_confidence"] > 0.0
    assert result["confidence"] == result["transfer_confidence"]
    assert result["evidence_features"]
    assert result["motif_lineage"]
    assert result["rejected_mechanisms"]


def test_unseasoned_pond_fails_closed_on_transfer_prompt() -> None:
    state = load_pond(PROOF / "pond_states" / "unseasoned")
    item = load_jsonl(PROOF / "tests" / "cross_domain_transfer_test.jsonl")[1]

    result = answer_question(item["question"], state)

    assert result["status"] == "FAIL_CLOSED"
    assert result["identified_mechanism"] == ""
    assert result["supporting_motifs"] == []
    assert result["transfer_confidence"] == 0.0


def test_unsupported_prompt_fails_closed_with_candidate_evidence() -> None:
    state = load_pond(PROOF / "pond_states" / "mechanism_seasoned")
    item = load_jsonl(PROOF / "tests" / "fail_closed_test.jsonl")[3]

    result = answer_question(item["question"], state)

    assert result["status"] == "FAIL_CLOSED"
    assert result["fail_closed_reason"] == "insufficient_motif_support"
    assert result["identified_mechanism"] == ""
    assert result["candidate_evidence"]


def test_proof_031_cue_invariance_metrics_and_hostile_boundary() -> None:
    metrics = load_json(PROOF_031 / "analysis" / "cue_invariance_metrics.json")
    hostile = load_json(PROOF_031 / "analysis" / "hostile_cue_invariance_audit.json")

    assert metrics["cue_removed_accuracy"] == 1.0
    assert metrics["cue_swapped_accuracy"] == 1.0
    assert metrics["decoy_cue_accuracy"] == 1.0
    assert metrics["neutral_physics_accuracy"] == 1.0
    assert metrics["ambiguous_fail_closed_rate"] == 1.0
    assert metrics["deterministic_replay_match"] is True
    assert hostile["hostile_verdict"] == "WEAK_SIGNAL"
    assert hostile["remaining_parser_explanation"] is True


def test_proof_031_result_items_have_required_shape() -> None:
    results = load_json(PROOF_031 / "results" / "cue_swapped_results.json")
    item = results["items"][0]

    for field in [
        "question",
        "status",
        "identified_mechanism",
        "evidence_features",
        "rejected_mechanisms",
        "motif_lineage",
        "source_tracebacks",
        "confidence",
    ]:
        assert field in item

    assert item["status"] in {"ANSWERED", "FAIL_CLOSED"}
    assert item["identified_mechanism"] == item["expected_mechanism"]
    assert item["source_tracebacks"]
