from __future__ import annotations

import json
import shutil
from pathlib import Path

from tools.validate_trace_candidate import REQUIRED_ELIGIBILITY_FIELDS, validate_trace_candidate


ROOT = Path(__file__).resolve().parents[1]
PROOF_DIR = ROOT / "proofs" / "011-redacted-real-trace-candidate"


def copy_candidate(tmp_path: Path) -> Path:
    destination = tmp_path / "proof-011-copy"
    shutil.copytree(PROOF_DIR, destination)
    return destination


def load_manifest(proof_dir: Path) -> dict:
    return json.loads((proof_dir / "candidate_manifest.json").read_text(encoding="utf-8"))


def write_manifest(proof_dir: Path, manifest: dict) -> None:
    (proof_dir / "candidate_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )


def make_eligible_manifest(proof_dir: Path) -> dict:
    manifest = load_manifest(proof_dir)
    manifest["candidate_status"] = "eligible"
    manifest["candidate_type"] = "public"
    manifest["source_refs"] = ["https://example.invalid/public-trace"]
    manifest["redaction_complete"] = True
    manifest["eligibility"] = {field: True for field in REQUIRED_ELIGIBILITY_FIELDS}
    manifest["decision"] = {
        "eligible_for_execution": True,
        "reason": "Candidate has complete public-safe lineage.",
    }
    return manifest


def test_not_selected_candidate_passes() -> None:
    assert validate_trace_candidate(PROOF_DIR) == []


def test_eligible_without_redaction_fails(tmp_path: Path) -> None:
    proof_dir = copy_candidate(tmp_path)
    manifest = make_eligible_manifest(proof_dir)
    manifest["redaction_complete"] = False
    write_manifest(proof_dir, manifest)

    errors = validate_trace_candidate(proof_dir)

    assert any("redaction_complete: eligible requires true" in error for error in errors)


def test_eligible_without_required_fields_fails(tmp_path: Path) -> None:
    proof_dir = copy_candidate(tmp_path)
    manifest = make_eligible_manifest(proof_dir)
    manifest["eligibility"]["has_tool_result_refs"] = False
    write_manifest(proof_dir, manifest)

    errors = validate_trace_candidate(proof_dir)

    assert any("has_tool_result_refs: eligible requires true" in error for error in errors)


def test_banned_string_fails(tmp_path: Path) -> None:
    proof_dir = copy_candidate(tmp_path)
    (proof_dir / "candidate" / "trace.txt").write_text("api_key=redacted\n", encoding="utf-8")

    errors = validate_trace_candidate(proof_dir)

    assert any("banned string detected: api_key" in error for error in errors)


def test_invalid_candidate_status_fails(tmp_path: Path) -> None:
    proof_dir = copy_candidate(tmp_path)
    manifest = load_manifest(proof_dir)
    manifest["candidate_status"] = "pending"
    write_manifest(proof_dir, manifest)

    errors = validate_trace_candidate(proof_dir)

    assert any("candidate_status: expected one of" in error for error in errors)
