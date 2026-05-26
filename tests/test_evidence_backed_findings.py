from __future__ import annotations

import copy
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import validate_evidence_backed_findings as validator  # noqa: E402


EVIDENCE_MANIFEST = {
    "proof_id": "003-continuity-compression-audit",
    "status": "evidence_collection",
    "sources": [
        {"id": "source-a"},
        {"id": "source-b"},
    ],
}

VALID_FINDINGS = {
    "proof_id": "003-continuity-compression-audit",
    "analysis_id": "analysis_v0_1",
    "status": "analysis",
    "findings": [
        {
            "id": "F-001",
            "claim": "Public docs describe a compression mechanism.",
            "claim_level": "observed",
            "evidence_refs": ["source-a"],
            "reasoning_summary": "The source directly describes the mechanism.",
            "limitations": ["This does not establish end-to-end adequacy."],
            "public_private_boundary": "sanitized_public_artifacts_only",
        },
        {
            "id": "F-002",
            "claim": "Compression may reduce replay fidelity when source links are absent.",
            "claim_level": "inferred",
            "evidence_refs": ["source-a", "source-b"],
            "reasoning_summary": "The inference connects compression with missing source links.",
            "limitations": [],
            "public_private_boundary": "sanitized_public_artifacts_only",
        },
    ],
    "summary": {
        "observed_count": 1,
        "inferred_count": 1,
        "hypothesis_count": 0,
        "unresolved_count": 0,
    },
}


def test_valid_findings_pass() -> None:
    assert validator.validate_findings_data(VALID_FINDINGS, EVIDENCE_MANIFEST) == []


def test_public_evidence_backed_findings_validate() -> None:
    proof_ids = [
        "003-continuity-compression-audit",
        "004-operational-failure-reconstruction",
    ]
    for proof_id in proof_ids:
        proof_dir = ROOT / "proofs" / proof_id
        findings = json.loads((proof_dir / "evidence_backed_findings.json").read_text(encoding="utf-8"))
        manifest = json.loads((proof_dir / "evidence_manifest.json").read_text(encoding="utf-8"))

        assert validator.validate_findings_data(findings, manifest) == []


def test_duplicate_finding_id_fails() -> None:
    findings = copy.deepcopy(VALID_FINDINGS)
    findings["findings"][1]["id"] = "F-001"

    errors = validator.validate_findings_data(findings, EVIDENCE_MANIFEST)

    assert any("duplicate finding ID F-001" in error for error in errors)


def test_observed_without_evidence_fails() -> None:
    findings = copy.deepcopy(VALID_FINDINGS)
    findings["findings"][0]["evidence_refs"] = []

    errors = validator.validate_findings_data(findings, EVIDENCE_MANIFEST)

    assert any("observed/inferred findings require evidence_refs" in error for error in errors)


def test_invalid_evidence_ref_fails() -> None:
    findings = copy.deepcopy(VALID_FINDINGS)
    findings["findings"][0]["evidence_refs"] = ["missing-source"]

    errors = validator.validate_findings_data(findings, EVIDENCE_MANIFEST)

    assert any("unknown evidence_ref missing-source" in error for error in errors)


def test_summary_count_mismatch_fails() -> None:
    findings = copy.deepcopy(VALID_FINDINGS)
    findings["summary"]["observed_count"] = 2

    errors = validator.validate_findings_data(findings, EVIDENCE_MANIFEST)

    assert any("$.summary.observed_count: expected 1, got 2" in error for error in errors)


def test_disallowed_claim_fails() -> None:
    findings = copy.deepcopy(VALID_FINDINGS)
    findings["findings"][0]["claim"] = "This proves consciousness."

    errors = validator.validate_findings_data(findings, EVIDENCE_MANIFEST)

    assert any("disallowed claim text consciousness" in error for error in errors)
