from __future__ import annotations

import json
import shutil
from pathlib import Path

from tools.validate_extreme_operational_breakdown_gauntlet import (
    ROOT,
    validate_extreme_operational_breakdown_gauntlet,
)


VALID_PROOF = ROOT / "proofs" / "020-extreme-operational-breakdown-gauntlet"


def copy_valid(tmp_path: Path) -> Path:
    target = tmp_path / "proof-020-copy"
    shutil.copytree(VALID_PROOF, target)
    return target


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_valid_gauntlet_passes() -> None:
    assert validate_extreme_operational_breakdown_gauntlet(VALID_PROOF) == []


def test_missing_contradiction_chains_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    path = proof / "scenarios" / "scenario_001" / "contradiction_chain.json"
    chain = load_json(path)
    chain["chains"] = chain["chains"][:2]
    write_json(path, chain)

    errors = validate_extreme_operational_breakdown_gauntlet(proof)

    assert any("expected at least 3 linked contradiction chains" in error for error in errors)


def test_missing_authority_conflicts_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    path = proof / "scenarios" / "scenario_002" / "authority_conflicts.json"
    conflicts = load_json(path)
    conflicts["conflicts"] = conflicts["conflicts"][:1]
    write_json(path, conflicts)

    errors = validate_extreme_operational_breakdown_gauntlet(proof)

    assert any("expected at least 2 authority conflicts" in error for error in errors)


def test_seasoned_refs_leaking_into_baseline_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    path = proof / "scenarios" / "scenario_003" / "baseline_results.json"
    baseline = load_json(path)
    baseline["leaked_ref"] = "artifacts/pond/mcp_seasoned_first_principles_admitted.jsonl#13"
    write_json(path, baseline)

    errors = validate_extreme_operational_breakdown_gauntlet(proof)

    assert any("baseline mode cites forbidden MCP-seasoned" in error for error in errors)


def test_invalid_verdict_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    path = proof / "final_verdict.json"
    verdict = load_json(path)
    verdict["verdict"] = "NO_EXTREME_OPERATIONAL_ADVANTAGE"
    write_json(path, verdict)

    errors = validate_extreme_operational_breakdown_gauntlet(proof)

    assert any("final_verdict.verdict: expected EXTREME_OPERATIONAL_ADVANTAGE_OBSERVED" in error for error in errors)


def test_runtime_hash_missing_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    path = proof / "scenarios" / "scenario_004" / "pond_backed_results.json"
    pond = load_json(path)
    del pond["runtime_hashes"]["runtime_response_hash"]
    write_json(path, pond)

    errors = validate_extreme_operational_breakdown_gauntlet(proof)

    assert any("scenario_004 pond results: missing or invalid runtime_response_hash" in error for error in errors)


def test_reusable_lineage_pool_mutation_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    path = proof / "aggregate_results.json"
    aggregate = load_json(path)
    aggregate["reusable_lineage_pool"]["post_test_sha256"] = "0" * 64
    write_json(path, aggregate)

    errors = validate_extreme_operational_breakdown_gauntlet(proof)

    assert any("reusable_lineage_pool" in error and "mutation" in error for error in errors)


def test_agi_and_global_superiority_wording_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    readme = proof / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8") + "\nThis proves global superiority and AGI.\n",
        encoding="utf-8",
    )

    errors = validate_extreme_operational_breakdown_gauntlet(proof)

    assert any("positive overclaim detected" in error for error in errors)
