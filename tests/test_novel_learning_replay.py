from __future__ import annotations

import json
import shutil
from pathlib import Path

from tools.validate_novel_learning_replay import ROOT, validate_novel_learning_replay


VALID_PROOF = ROOT / "proofs" / "015-novel-learning-replay-test"


def copy_valid(tmp_path: Path) -> Path:
    target = tmp_path / "proof-015-copy"
    shutil.copytree(VALID_PROOF, target)
    return target


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_valid_proof_passes() -> None:
    assert validate_novel_learning_replay(VALID_PROOF) == []


def test_missing_learning_record_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    (proof / "inside_voice_learning_record.json").unlink()

    errors = validate_novel_learning_replay(proof)

    assert any("missing required artifact: inside_voice_learning_record.json" in error for error in errors)


def test_missing_repeat_response_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    (proof / "repeat_replay_response.json").unlink()

    errors = validate_novel_learning_replay(proof)

    assert any("missing required artifact: repeat_replay_response.json" in error for error in errors)


def test_full_original_solution_leaked_into_repeat_request_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    request_path = proof / "repeat_replay_request.json"
    request = load_json(request_path)
    original = (proof / "initial_codex_solution.md").read_text(encoding="utf-8")
    request["context"]["summary"] += "\n\n" + original
    write_json(request_path, request)

    errors = validate_novel_learning_replay(proof)

    assert any("includes full original solution text" in error for error in errors)


def test_invalid_verdict_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    verdict_path = proof / "final_verdict.json"
    verdict = load_json(verdict_path)
    verdict["verdict"] = "NO_LEARNING_REPLAY_ADVANTAGE"
    write_json(verdict_path, verdict)

    errors = validate_novel_learning_replay(proof)

    assert any("final_verdict.verdict: expected LEARNING_REPLAY_ADVANTAGE_OBSERVED" in error for error in errors)


def test_global_superiority_wording_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    readme = proof / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8") + "\nThis is globally superior.\n", encoding="utf-8")

    errors = validate_novel_learning_replay(proof)

    assert any("positive overclaim detected" in error for error in errors)


def test_missing_runtime_hash_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    response_path = proof / "repeat_replay_response.json"
    response = load_json(response_path)
    response["lineage"]["runtime"]["runtime_response_hash"] = ""
    write_json(response_path, response)

    errors = validate_novel_learning_replay(proof)

    assert any("repeat_replay_response.json.lineage.runtime.runtime_response_hash: expected sha256" in error for error in errors)
