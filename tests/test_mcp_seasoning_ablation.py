from __future__ import annotations

import json
import shutil
from pathlib import Path

from tools.validate_mcp_seasoning_ablation import ROOT, validate_mcp_seasoning_ablation


VALID_PROOF = ROOT / "proofs" / "019-mcp-seasoning-ablation-control"


def copy_valid(tmp_path: Path) -> Path:
    target = tmp_path / "proof-019-copy"
    shutil.copytree(VALID_PROOF, target)
    return target


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_valid_proof_passes() -> None:
    assert validate_mcp_seasoning_ablation(VALID_PROOF) == []


def test_seasoned_refs_leaking_into_ablated_mode_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    response_path = proof / "inside_voice_consults" / "task_001_ablated_response.json"
    response = load_json(response_path)
    response["retrieved_artifact_refs"].append("artifacts/pond/mcp_seasoned_first_principles_admitted.jsonl#1")
    write_json(response_path, response)

    errors = validate_mcp_seasoning_ablation(proof)

    assert any("seasoned refs leaked into ablated mode" in error for error in errors)


def test_missing_blind_scores_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    (proof / "tasks" / "task_002" / "blind_scoring_results.json").unlink()

    errors = validate_mcp_seasoning_ablation(proof)

    assert any("blind_scoring_results.json" in error for error in errors)


def test_invalid_verdict_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    verdict_path = proof / "final_verdict.json"
    verdict = load_json(verdict_path)
    verdict["verdict"] = "NO_SEASONING_TRANSFER_ADVANTAGE"
    write_json(verdict_path, verdict)

    errors = validate_mcp_seasoning_ablation(proof)

    assert any("final_verdict.verdict: expected SEASONING_TRANSFER_ADVANTAGE_CONFIRMED" in error for error in errors)


def test_missing_runtime_hashes_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    response_path = proof / "inside_voice_consults" / "task_003_ablated_response.json"
    response = load_json(response_path)
    del response["lineage"]["runtime_response_hash"]
    write_json(response_path, response)

    errors = validate_mcp_seasoning_ablation(proof)

    assert any("task_003 ablated: missing or invalid runtime_response_hash" in error for error in errors)


def test_reusable_lineage_pool_mutation_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    aggregate_path = proof / "aggregate_results.json"
    aggregate = load_json(aggregate_path)
    aggregate["reusable_lineage_pool"]["post_test_sha256"] = "0" * 64
    write_json(aggregate_path, aggregate)

    errors = validate_mcp_seasoning_ablation(proof)

    assert any("reusable_lineage_pool" in error and "mutation" in error for error in errors)


def test_promotion_claim_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    readme = proof / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8") + "\nThis proof promotes candidates to reusable_lineage_pool.\n",
        encoding="utf-8",
    )

    errors = validate_mcp_seasoning_ablation(proof)

    assert any("positive overclaim detected" in error for error in errors)


def test_agi_and_global_superiority_wording_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    readme = proof / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8") + "\nThis proves global superiority and AGI.\n",
        encoding="utf-8",
    )

    errors = validate_mcp_seasoning_ablation(proof)

    assert any("positive overclaim detected" in error for error in errors)
