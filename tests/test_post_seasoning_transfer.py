from __future__ import annotations

import json
import shutil
from pathlib import Path

from tools.validate_post_seasoning_transfer import ROOT, validate_post_seasoning_transfer


VALID_PROOF = ROOT / "proofs" / "018-post-seasoning-transfer-test"


def copy_valid(tmp_path: Path) -> Path:
    target = tmp_path / "proof-018-copy"
    shutil.copytree(VALID_PROOF, target)
    return target


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_valid_proof_passes() -> None:
    assert validate_post_seasoning_transfer(VALID_PROOF) == []


def test_missing_mcp_seasoned_refs_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    refs_path = proof / "tasks" / "task_001" / "mcp_seasoned_refs_used.json"
    refs = load_json(refs_path)
    refs["refs"] = []
    write_json(refs_path, refs)

    errors = validate_post_seasoning_transfer(proof)

    assert any("mcp_seasoned_refs_used.json lacks MCP-seasoned refs" in error for error in errors)


def test_baseline_leak_of_mcp_refs_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    baseline = proof / "tasks" / "task_001" / "baseline_solution.md"
    baseline.write_text(
        baseline.read_text(encoding="utf-8")
        + "\nLeaked ref: artifacts/pond/mcp_seasoned_first_principles_admitted.jsonl#35\n",
        encoding="utf-8",
    )

    errors = validate_post_seasoning_transfer(proof)

    assert any("baseline mode cites forbidden MCP-seasoned material" in error for error in errors)


def test_invalid_final_verdict_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    verdict_path = proof / "final_verdict.json"
    verdict = load_json(verdict_path)
    verdict["verdict"] = "NO_POST_SEASONING_TRANSFER_ADVANTAGE"
    write_json(verdict_path, verdict)

    errors = validate_post_seasoning_transfer(proof)

    assert any("final_verdict.verdict: expected POST_SEASONING_TRANSFER_ADVANTAGE_OBSERVED" in error for error in errors)


def test_missing_runtime_hash_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    response_path = proof / "inside_voice_consults" / "task_002_pond_response.json"
    response = load_json(response_path)
    del response["lineage"]["runtime"]["runtime_response_hash"]
    write_json(response_path, response)

    errors = validate_post_seasoning_transfer(proof)

    assert any("task_002: missing or invalid runtime_response_hash" in error for error in errors)


def test_reusable_lineage_pool_mutation_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    visibility_path = proof / "mcp_seasoned_visibility_report.json"
    visibility = load_json(visibility_path)
    visibility["reusable_lineage_pool"]["post_test_sha256"] = "0" * 64
    write_json(visibility_path, visibility)

    errors = validate_post_seasoning_transfer(proof)

    assert any("reusable_lineage_pool" in error and "mutation" in error for error in errors)


def test_global_superiority_wording_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    readme = proof / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8") + "\nThis proves global superiority.\n", encoding="utf-8")

    errors = validate_post_seasoning_transfer(proof)

    assert any("positive overclaim detected" in error for error in errors)


def test_promotion_claim_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    summary = proof / "public_lineage_summary.md"
    summary.write_text(
        summary.read_text(encoding="utf-8") + "\nThis proof promotes candidates to reusable_lineage_pool.\n",
        encoding="utf-8",
    )

    errors = validate_post_seasoning_transfer(proof)

    assert any("positive overclaim detected" in error for error in errors)
