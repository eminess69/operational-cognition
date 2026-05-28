from __future__ import annotations

import json
import shutil
from pathlib import Path

from tools.validate_real_trace_replication import ROOT, validate_real_trace_replication


VALID_PROOF = ROOT / "proofs" / "014-independent-real-trace-replication"


def copy_valid(tmp_path: Path) -> Path:
    target = tmp_path / "proof-014-copy"
    shutil.copytree(VALID_PROOF, target)
    return target


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_valid_replication_passes() -> None:
    assert validate_real_trace_replication(VALID_PROOF) == []


def test_fewer_than_two_valid_traces_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    shutil.rmtree(proof / "traces" / "trace_002")
    shutil.rmtree(proof / "traces" / "trace_003")
    final_verdict_path = proof / "final_verdict.json"
    final_verdict = load_json(final_verdict_path)
    final_verdict["valid_trace_count"] = 1
    final_verdict["verdict"] = "REPLICATION_ADVANTAGE_OBSERVED"
    write_json(final_verdict_path, final_verdict)

    errors = validate_real_trace_replication(proof)

    assert any("at least 2 trace folders are required" in error for error in errors)


def test_missing_replay_results_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    (proof / "traces" / "trace_001" / "full_lineage_replay_results.json").unlink()

    errors = validate_real_trace_replication(proof)

    assert any("missing required artifact: full_lineage_replay_results.json" in error for error in errors)


def test_missing_pond_backed_evidence_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    response_path = proof / "inside_voice_consults" / "hard_gate_response.json"
    response = load_json(response_path)
    response["adapter_status"] = "placeholder"
    write_json(response_path, response)

    errors = validate_real_trace_replication(proof)

    assert any("adapter_status: expected pond_backed" in error for error in errors)


def test_invalid_aggregate_verdict_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    final_verdict_path = proof / "final_verdict.json"
    final_verdict = load_json(final_verdict_path)
    final_verdict["verdict"] = "NO_REPLICATION_ADVANTAGE"
    write_json(final_verdict_path, final_verdict)

    errors = validate_real_trace_replication(proof)

    assert any("final_verdict.verdict: expected REPLICATION_ADVANTAGE_OBSERVED" in error for error in errors)


def test_global_superiority_wording_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    readme = proof / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8") + "\nThis is globally superior.\n", encoding="utf-8")

    errors = validate_real_trace_replication(proof)

    assert any("positive overclaim detected" in error for error in errors)


def test_target_system_defect_wording_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    readme = proof / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8") + "\nA target-system defect was proven.\n", encoding="utf-8")

    errors = validate_real_trace_replication(proof)

    assert any("positive overclaim detected" in error for error in errors)


def test_agi_consciousness_wording_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    readme = proof / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8") + "\nThis proves AGI and consciousness.\n", encoding="utf-8")

    errors = validate_real_trace_replication(proof)

    assert any("positive overclaim detected" in error for error in errors)
