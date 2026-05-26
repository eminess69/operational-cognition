from __future__ import annotations

import copy
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import validate_claim_register as validator  # noqa: E402


EVIDENCE_MANIFEST = {
    "proof_id": "003-continuity-compression-audit",
    "status": "evidence_collection",
    "sources": [
        {"id": "source-a"},
        {"id": "source-b"},
    ],
}

VALID_REGISTER = {
    "proof_id": "003-continuity-compression-audit",
    "analysis_id": "analysis_v0_1",
    "claims": [
        {
            "claim_id": "C-001",
            "claim": "Public docs describe a compression mechanism.",
            "claim_level": "observed",
            "evidence_refs": ["source-a"],
            "appears_in": ["analysis_v0_1.md"],
            "risk_if_overstated": "Would imply more coverage than the source states.",
            "safe_public_wording": "Public docs describe this mechanism.",
        },
        {
            "claim_id": "C-002",
            "claim": "Compression can reduce replay fidelity when source links are absent.",
            "claim_level": "inferred",
            "evidence_refs": ["source-a", "source-b"],
            "appears_in": ["analysis_v0_1.md"],
            "risk_if_overstated": "Would turn an inference into a defect claim.",
            "safe_public_wording": "Replay fidelity may be reduced when source links are absent.",
        },
    ],
}


def test_valid_register_passes() -> None:
    assert validator.validate_register_data(VALID_REGISTER, EVIDENCE_MANIFEST) == []


def test_duplicate_claim_id_fails() -> None:
    register = copy.deepcopy(VALID_REGISTER)
    register["claims"][1]["claim_id"] = "C-001"

    errors = validator.validate_register_data(register, EVIDENCE_MANIFEST)

    assert any("duplicate claim ID C-001" in error for error in errors)


def test_observed_without_evidence_fails() -> None:
    register = copy.deepcopy(VALID_REGISTER)
    register["claims"][0]["evidence_refs"] = []

    errors = validator.validate_register_data(register, EVIDENCE_MANIFEST)

    assert any("observed claims require evidence_refs" in error for error in errors)


def test_invalid_evidence_ref_fails() -> None:
    register = copy.deepcopy(VALID_REGISTER)
    register["claims"][0]["evidence_refs"] = ["missing-source"]

    errors = validator.validate_register_data(register, EVIDENCE_MANIFEST)

    assert any("unknown evidence_ref missing-source" in error for error in errors)


def test_disallowed_claim_fails() -> None:
    register = copy.deepcopy(VALID_REGISTER)
    register["claims"][0]["claim"] = "This proves AGI."

    errors = validator.validate_register_data(register, EVIDENCE_MANIFEST)

    assert any("disallowed claim text AGI" in error for error in errors)
