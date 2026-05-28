from __future__ import annotations

import json
import shutil
from pathlib import Path

from tools.validate_entropy_replication_gauntlet import ROOT, validate_entropy_replication_gauntlet


VALID_PROOF = ROOT / "proofs" / "017-entropy-replication-gauntlet"


def copy_valid(tmp_path: Path) -> Path:
    target = tmp_path / "proof-017-copy"
    shutil.copytree(VALID_PROOF, target)
    return target


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_valid_gauntlet_passes() -> None:
    assert validate_entropy_replication_gauntlet(VALID_PROOF) == []


def test_missing_scenario_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    shutil.rmtree(proof / "scenarios" / "scenario_005")

    errors = validate_entropy_replication_gauntlet(proof)

    assert any("scenario folders" in error for error in errors)


def test_missing_blind_pack_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    shutil.rmtree(proof / "blind_pack")

    errors = validate_entropy_replication_gauntlet(proof)

    assert any("missing blind pack artifact" in error for error in errors)


def test_invalid_aggregate_verdict_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    final_path = proof / "final_verdict.json"
    final = load_json(final_path)
    final["verdict"] = "NO_ENTROPY_REPLICATION_ADVANTAGE"
    write_json(final_path, final)

    errors = validate_entropy_replication_gauntlet(proof)

    assert any("final_verdict.verdict: expected ENTROPY_REPLICATION_ADVANTAGE_OBSERVED" in error for error in errors)


def test_missing_inside_voice_evidence_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    (proof / "inside_voice_consults" / "hard_gate_response.json").unlink()

    errors = validate_entropy_replication_gauntlet(proof)

    assert any("missing Inside Voice response artifact" in error for error in errors)


def test_global_superiority_wording_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    readme = proof / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8") + "\nThis is globally superior.\n", encoding="utf-8")

    errors = validate_entropy_replication_gauntlet(proof)

    assert any("positive overclaim detected" in error for error in errors)


def test_agi_consciousness_wording_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    summary = proof / "public_lineage_summary.md"
    summary.write_text(
        summary.read_text(encoding="utf-8") + "\nThis validates AGI and consciousness.\n",
        encoding="utf-8",
    )

    errors = validate_entropy_replication_gauntlet(proof)

    assert any("positive overclaim detected" in error for error in errors)


def test_target_system_defect_wording_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    report = proof / "comparative_entropy_report.md"
    report.write_text(
        report.read_text(encoding="utf-8") + "\nThis confirms target-system defect.\n",
        encoding="utf-8",
    )

    errors = validate_entropy_replication_gauntlet(proof)

    assert any("positive overclaim detected" in error for error in errors)
