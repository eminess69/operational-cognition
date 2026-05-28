from __future__ import annotations

import json
import shutil
from pathlib import Path

from tools.validate_operational_entropy_gauntlet import ROOT, validate_operational_entropy_gauntlet


VALID_PROOF = ROOT / "proofs" / "016-operational-entropy-gauntlet"


def copy_valid(tmp_path: Path) -> Path:
    target = tmp_path / "proof-016-copy"
    shutil.copytree(VALID_PROOF, target)
    return target


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_valid_gauntlet_passes() -> None:
    assert validate_operational_entropy_gauntlet(VALID_PROOF) == []


def test_missing_entropy_injections_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    log_path = proof / "entropy_event_log.jsonl"
    lines = [line for line in log_path.read_text(encoding="utf-8").splitlines() if '"E-008"' not in line]
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    errors = validate_operational_entropy_gauntlet(proof)

    assert any("missing entropy injections" in error for error in errors)


def test_missing_consult_evidence_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    (proof / "inside_voice_consults" / "hard_gate_response.json").unlink()

    errors = validate_operational_entropy_gauntlet(proof)

    assert any("missing Inside Voice response artifact" in error for error in errors)


def test_replay_separation_failure_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    baseline_path = proof / "baseline_visible_only_results.md"
    baseline_path.write_text(
        baseline_path.read_text(encoding="utf-8").replace(
            "inside_voice_guidance_used: false",
            "inside_voice_guidance_used: true",
        ),
        encoding="utf-8",
    )

    errors = validate_operational_entropy_gauntlet(proof)

    assert any("baseline replay separation" in error for error in errors)


def test_invalid_verdict_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    verdict_path = proof / "final_verdict.json"
    verdict = load_json(verdict_path)
    verdict["verdict"] = "NO_ENTROPY_ADVANTAGE"
    write_json(verdict_path, verdict)

    errors = validate_operational_entropy_gauntlet(proof)

    assert any("final_verdict.verdict: expected ENTROPY_ADVANTAGE_OBSERVED" in error for error in errors)


def test_global_superiority_wording_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    readme = proof / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8") + "\nThis is globally superior.\n", encoding="utf-8")

    errors = validate_operational_entropy_gauntlet(proof)

    assert any("positive overclaim detected" in error for error in errors)


def test_agi_consciousness_wording_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    summary = proof / "public_lineage_summary.md"
    summary.write_text(
        summary.read_text(encoding="utf-8") + "\nThis validates AGI and consciousness.\n",
        encoding="utf-8",
    )

    errors = validate_operational_entropy_gauntlet(proof)

    assert any("positive overclaim detected" in error for error in errors)
