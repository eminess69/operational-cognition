from __future__ import annotations

import json
import shutil
from pathlib import Path

from tools.validate_pond_backed_one_shot import ROOT, validate_proof


VALID_PROOF = ROOT / "proofs" / "012-pond-backed-one-shot-proof"


def copy_valid(tmp_path: Path) -> Path:
    target = tmp_path / "proof"
    shutil.copytree(VALID_PROOF, target)
    return target


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def test_valid_run_passes() -> None:
    assert validate_proof(VALID_PROOF) == []


def test_placeholder_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)

    usage_path = proof / "inside_voice_usage_report.json"
    usage = load_json(usage_path)
    usage["consultation"]["adapter_status"] = "placeholder"
    write_json(usage_path, usage)

    runtime_path = proof / "pond_backed_runtime_lineage.json"
    runtime = load_json(runtime_path)
    runtime["adapter_status"] = "placeholder"
    write_json(runtime_path, runtime)

    manifest_path = proof / "proof_manifest.json"
    manifest = load_json(manifest_path)
    manifest["inside_voice_adapter_status"] = "placeholder"
    write_json(manifest_path, manifest)

    errors = validate_proof(proof)
    assert any("expected pond_backed" in error for error in errors)


def test_empty_motifs_fail(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    usage_path = proof / "inside_voice_usage_report.json"
    usage = load_json(usage_path)
    usage["recalled_motifs"] = []
    write_json(usage_path, usage)

    errors = validate_proof(proof)
    assert any("recalled_motifs" in error for error in errors)


def test_missing_proof_010_boundary_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    usage_path = proof / "inside_voice_usage_report.json"
    usage = load_json(usage_path)
    usage["boundary_preservation"].pop("proof_010")
    write_json(usage_path, usage)

    errors = validate_proof(proof)
    assert "Proof 010 boundary not preserved as synthetic-only" in errors


def test_missing_proof_011_boundary_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    usage_path = proof / "inside_voice_usage_report.json"
    usage = load_json(usage_path)
    usage["boundary_preservation"].pop("proof_011")
    write_json(usage_path, usage)

    errors = validate_proof(proof)
    assert "Proof 011 boundary not preserved as real-trace gate" in errors


def test_global_superiority_claim_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    verdict_path = proof / "final_audit_verdict.json"
    verdict = load_json(verdict_path)
    verdict["global_superiority_claim"] = True
    write_json(verdict_path, verdict)

    errors = validate_proof(proof)
    assert "final_audit_verdict.json.global_superiority_claim: expected false" in errors


def test_invalid_verdict_fails(tmp_path: Path) -> None:
    proof = copy_valid(tmp_path)
    verdict_path = proof / "final_audit_verdict.json"
    verdict = load_json(verdict_path)
    verdict["verdict"] = "invalid_run"
    write_json(verdict_path, verdict)

    errors = validate_proof(proof)
    assert "final_audit_verdict.json.verdict: invalid verdict" in errors
