from __future__ import annotations

import json
import shutil
from pathlib import Path

from tools.validate_real_trace_replay_gate import ROOT, validate_real_trace_replay_gate


VALID_PROOF = ROOT / "proofs" / "013-real-trace-replay-gate"


def copy_valid(tmp_path: Path) -> Path:
    target = tmp_path / "proof-013-copy"
    shutil.copytree(VALID_PROOF, target)
    return target


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_valid_replay_gate_passes() -> None:
    assert validate_real_trace_replay_gate(VALID_PROOF) == []


def test_placeholder_runtime_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    runtime_path = proof / "fixture" / "runtime_config.json"
    runtime = load_json(runtime_path)
    runtime["inside_voice_gate"]["adapter_status"] = "placeholder"
    write_json(runtime_path, runtime)

    errors = validate_real_trace_replay_gate(proof)

    assert any("expected pond_backed" in error for error in errors)


def test_missing_replay_artifact_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    (proof / "full_lineage_replay_results.json").unlink()

    errors = validate_real_trace_replay_gate(proof)

    assert any("missing required artifact: full_lineage_replay_results.json" in error for error in errors)


def test_missing_contradiction_refs_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    (proof / "fixture" / "contradiction_refs.json").unlink()

    errors = validate_real_trace_replay_gate(proof)

    assert any("missing required artifact: fixture/contradiction_refs.json" in error for error in errors)


def test_missing_recovery_trace_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    (proof / "fixture" / "recovery_trace.jsonl").unlink()

    errors = validate_real_trace_replay_gate(proof)

    assert any("missing required artifact: fixture/recovery_trace.jsonl" in error for error in errors)


def test_missing_environment_refs_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    (proof / "fixture" / "environment_snapshot_manifest.json").unlink()

    errors = validate_real_trace_replay_gate(proof)

    assert any("missing required artifact: fixture/environment_snapshot_manifest.json" in error for error in errors)


def test_invalid_verdict_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    verdict_path = proof / "final_verdict.json"
    verdict = load_json(verdict_path)
    verdict["verdict"] = "TOO_STRONG"
    write_json(verdict_path, verdict)

    errors = validate_real_trace_replay_gate(proof)

    assert "final_verdict.verdict: invalid verdict" in errors


def test_global_superiority_wording_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    readme_path = proof / "README.md"
    readme_path.write_text(readme_path.read_text(encoding="utf-8") + "\nThis is globally superior.\n", encoding="utf-8")

    errors = validate_real_trace_replay_gate(proof)

    assert any("positive overclaim detected" in error for error in errors)
