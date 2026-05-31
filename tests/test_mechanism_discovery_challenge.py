from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT / "proofs" / "034-mechanism-discovery-challenge"
RESERVED = ["F" + "LOW", "LOAD" + "_TRANSFER", "SUPPORTED" + "_ROTATION"]


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_observation_cases_are_observation_only() -> None:
    rows = jsonl(PROOF / "tests" / "observation_only_cases.jsonl")

    assert len(rows) == 24
    for row in rows:
        assert set(row) == {"case_id", "observations"}
        rendered = json.dumps(row, sort_keys=True)
        assert all(label not in rendered for label in RESERVED)
        assert "candidate" not in rendered.lower()
        assert "expected" not in rendered.lower()
        assert "answer" not in rendered.lower()


def test_mandatory_discovery_consults_are_recorded_before_candidates() -> None:
    consults = jsonl(PROOF / "mcp" / "discovery_consults.jsonl")
    candidates = load_json(PROOF / "results" / "initial_candidates.json")

    assert len(consults) == 24
    assert candidates["generated_after_discovery_consults"] is True
    assert all(row["phase"] == "mandatory_pond_consult" for row in consults)
    assert all(row["consultation_recorded_before_candidates"] is True for row in consults)
    assert all(row["adapter_status"] in {"placeholder", "pond_backed"} for row in consults)
    assert all(row["partial_lineage_matches"]["proof_033_recall_refs"] for row in consults)


def test_candidate_outputs_are_ranked_pathways_not_answers() -> None:
    candidates = load_json(PROOF / "results" / "initial_candidates.json")

    for item in candidates["items"]:
        assert "answer" not in item
        assert "identified_mechanism" not in item
        assert item["no_final_answer"] is True
        assert item["candidate_pathways"]
        for candidate in item["candidate_pathways"]:
            assert set(candidate) >= {"pathway", "reason", "weight"}
            assert 0.0 <= candidate["weight"] <= 1.0


def test_hostile_audit_matches_bounded_weak_signal() -> None:
    audit = load_json(PROOF / "analysis" / "discovery_audit.json")
    hostile = load_json(PROOF / "analysis" / "hostile_discovery_audit.json")
    final = hostile["final_verdict"]

    assert audit["questions"]["did_pond_consultation_increase_candidate_diversity"] is True
    assert audit["questions"]["did_pond_consultation_preserve_pathways_baseline_eliminated"] is False
    assert audit["questions"]["did_pond_consultation_improve_ranking_quality"] is False
    assert audit["questions"]["did_pond_consultation_reduce_premature_convergence"] is True
    assert final["candidate_diversity_improved"] is True
    assert final["premature_convergence_reduced"] is True
    assert final["remaining_codex_explanation"] is True
    assert final["remaining_pond_explanation"] is True
    assert final["hostile_verdict"].startswith("WEAK_SIGNAL")
