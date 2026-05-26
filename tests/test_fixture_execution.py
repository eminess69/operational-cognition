from __future__ import annotations

import json
import shutil
from pathlib import Path

from tools.validate_fixture_execution import validate_fixture_execution


ROOT = Path(__file__).resolve().parents[1]
PROOF_DIR = ROOT / "proofs" / "010-fixture-execution"


def copy_execution(tmp_path: Path) -> Path:
    destination = tmp_path / "proof-010-copy"
    shutil.copytree(PROOF_DIR, destination)
    return destination


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def test_valid_execution_passes() -> None:
    assert validate_fixture_execution(PROOF_DIR) == []


def test_missing_probe_fails(tmp_path: Path) -> None:
    proof_dir = copy_execution(tmp_path)
    visible_path = proof_dir / "visible_replay_results.json"
    visible = load_json(visible_path)
    visible["results"] = visible["results"][:-1]
    write_json(visible_path, visible)

    errors = validate_fixture_execution(proof_dir)

    assert any("visible_only: missing probe P-006" in error for error in errors)


def test_bad_score_fails(tmp_path: Path) -> None:
    proof_dir = copy_execution(tmp_path)
    visible_path = proof_dir / "visible_replay_results.json"
    visible = load_json(visible_path)
    visible["results"][0]["score"] = "mostly_reconstructed"
    write_json(visible_path, visible)

    errors = validate_fixture_execution(proof_dir)

    assert any("score: expected one of" in error for error in errors)


def test_incorrect_verdict_fails(tmp_path: Path) -> None:
    proof_dir = copy_execution(tmp_path)
    verdict_path = proof_dir / "validation_verdict.json"
    verdict = load_json(verdict_path)
    verdict["verdict"] = "FIXTURE_FAILED"
    write_json(verdict_path, verdict)

    errors = validate_fixture_execution(proof_dir)

    assert any("validation_verdict.verdict: expected FIXTURE_VALIDATED" in error for error in errors)


def test_full_lineage_unresolved_fails(tmp_path: Path) -> None:
    proof_dir = copy_execution(tmp_path)
    full_path = proof_dir / "full_lineage_replay_results.json"
    full = load_json(full_path)
    full["results"][0]["score"] = "unresolved"
    full["summary"] = {
        "reconstructed": 5,
        "partially_reconstructed": 0,
        "unresolved": 1,
    }
    write_json(full_path, full)

    verdict_path = proof_dir / "validation_verdict.json"
    verdict = load_json(verdict_path)
    verdict["full_lineage_summary"] = full["summary"]
    verdict["verdict"] = "FIXTURE_PARTIAL"
    verdict["aggregate_improvement"] = False
    write_json(verdict_path, verdict)

    errors = validate_fixture_execution(proof_dir)

    assert any("full_lineage: P-001 must be reconstructed" in error for error in errors)


def test_visible_only_too_strong_fails(tmp_path: Path) -> None:
    proof_dir = copy_execution(tmp_path)
    visible_path = proof_dir / "visible_replay_results.json"
    visible = load_json(visible_path)
    for result in visible["results"]:
        result["score"] = "reconstructed"
    visible["summary"] = {
        "reconstructed": 6,
        "partially_reconstructed": 0,
        "unresolved": 0,
    }
    write_json(visible_path, visible)

    verdict_path = proof_dir / "validation_verdict.json"
    verdict = load_json(verdict_path)
    verdict["visible_only_summary"] = visible["summary"]
    verdict["verdict"] = "FIXTURE_PARTIAL"
    verdict["aggregate_improvement"] = False
    write_json(verdict_path, verdict)

    errors = validate_fixture_execution(proof_dir)

    assert any("visible_only: expected at least three partial/unresolved probes" in error for error in errors)
