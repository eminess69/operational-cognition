from __future__ import annotations

import json
import shutil
from pathlib import Path

from tools.validate_triple_blind_transfer import ROOT, validate_triple_blind_transfer


VALID_PROOF = ROOT / "proofs" / "021-triple-blind-transfer-evaluation"


def copy_valid(tmp_path: Path) -> Path:
    target = tmp_path / "proof-021-copy"
    shutil.copytree(VALID_PROOF, target)
    return target


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_valid_proof_passes() -> None:
    assert validate_triple_blind_transfer(VALID_PROOF) == []


def test_mode_name_in_blind_scores_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    scores_path = proof / "blind_scores.json"
    scores = load_json(scores_path)
    scores["tasks"]["task_001"]["results"]["solution_A"]["rationale"] += " baseline_visible_only"
    write_json(scores_path, scores)

    errors = validate_triple_blind_transfer(proof)

    assert any("blind artifact contains source-identifying text" in error for error in errors)


def test_mcp_ref_in_anonymized_output_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    output_path = proof / "anonymized_outputs" / "task_002" / "solution_C.md"
    output_path.write_text(
        output_path.read_text(encoding="utf-8") + "\nartifacts/pond/mcp_seasoned_hidden.jsonl#4\n",
        encoding="utf-8",
    )

    errors = validate_triple_blind_transfer(proof)

    assert any("blind artifact contains source-identifying text" in error for error in errors)


def test_reveal_hash_mismatch_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    scores_path = proof / "blind_scores.json"
    scores = load_json(scores_path)
    scores["tasks"]["task_003"]["results"]["solution_A"]["scores"]["actionability"] = 3
    scores["tasks"]["task_003"]["results"]["solution_A"]["total_score"] = 32
    write_json(scores_path, scores)

    errors = validate_triple_blind_transfer(proof)

    assert any("blind_scores_sha256 mismatch" in error for error in errors)


def test_reused_task_title_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    mapping_path = proof / "mode_mapping_hidden.json"
    mapping = load_json(mapping_path)
    mapping["tasks"]["task_005"]["title"] = "Planning Decomposition"
    write_json(mapping_path, mapping)

    errors = validate_triple_blind_transfer(proof)

    assert any("reuses Proofs 018-020" in error for error in errors)


def test_invalid_confirmed_verdict_fails_when_mapping_changes(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    mapping_path = proof / "mode_mapping_hidden.json"
    mapping = load_json(mapping_path)
    mapping["tasks"]["task_001"]["label_to_mode"] = {
        "solution_A": "pond_backed_mcp_seasoned",
        "solution_B": "baseline_visible_only",
        "solution_C": "pond_backed_ablated",
    }
    mapping["tasks"]["task_002"]["label_to_mode"] = {
        "solution_A": "pond_backed_ablated",
        "solution_B": "pond_backed_mcp_seasoned",
        "solution_C": "baseline_visible_only",
    }
    write_json(mapping_path, mapping)

    errors = validate_triple_blind_transfer(proof)

    assert any("final_verdict.verdict: expected" in error for error in errors)


def test_mode_mapping_in_blind_scores_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    scores_path = proof / "blind_scores.json"
    scores = load_json(scores_path)
    scores["mode_mapping_included"] = True
    scores["mode_mapping"] = {"solution_A": "pond_backed_mcp_seasoned"}
    write_json(scores_path, scores)

    errors = validate_triple_blind_transfer(proof)

    assert any("mode_mapping_included" in error for error in errors)
