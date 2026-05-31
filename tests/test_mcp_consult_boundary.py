from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from operational_cognition.mcp.consult_classifier import MCPConsultClass, classify_mcp_response
from operational_cognition.mcp.proof_gate import MCPConsultBoundaryError, assert_pond_backed_consult


ROOT = Path(__file__).resolve().parents[1]


def test_placeholder_response_fails() -> None:
    response = {"adapter_status": "placeholder", "verdict": "ok"}

    assert classify_mcp_response(response) == MCPConsultClass.PLACEHOLDER
    with pytest.raises(MCPConsultBoundaryError, match="PLACEHOLDER"):
        assert_pond_backed_consult(response)


def test_mock_response_fails() -> None:
    response = {"adapter_status": "mock", "verdict": "ok", "response_source": "mock_fixture"}

    assert classify_mcp_response(response) == MCPConsultClass.MOCK
    with pytest.raises(MCPConsultBoundaryError, match="MOCK"):
        assert_pond_backed_consult(response)


def test_unknown_response_fails() -> None:
    response = {"verdict": "ok", "summary": "No adapter status supplied."}

    assert classify_mcp_response(response) == MCPConsultClass.UNKNOWN
    with pytest.raises(MCPConsultBoundaryError, match="UNKNOWN"):
        assert_pond_backed_consult(response)


def test_pond_backed_with_lineage_passes() -> None:
    response = {
        "adapter_status": "pond_backed",
        "verdict": "ok",
        "returned_lineages": ["inside_voice_runtime:abc123"],
        "returned_motifs": ["boundary pressure"],
    }

    assert classify_mcp_response(response) == MCPConsultClass.POND_BACKED
    assert_pond_backed_consult(response, require_lineage=True, require_motifs=True)


def test_pond_backed_missing_lineage_fails_when_required() -> None:
    response = {"adapter_status": "pond_backed", "verdict": "ok", "returned_motifs": ["motif"]}

    with pytest.raises(MCPConsultBoundaryError, match="missing lineage"):
        assert_pond_backed_consult(response, require_lineage=True)


def test_pond_backed_missing_motif_fails_when_required() -> None:
    response = {
        "adapter_status": "pond_backed",
        "verdict": "ok",
        "lineage_hashes": ["a" * 64],
    }

    with pytest.raises(MCPConsultBoundaryError, match="missing motif"):
        assert_pond_backed_consult(response, require_lineage=True, require_motifs=True)


def test_validator_fails_current_proof_034_placeholder_consults() -> None:
    path = ROOT / "proofs" / "034-mechanism-discovery-challenge" / "mcp" / "discovery_consults.jsonl"
    completed = subprocess.run(
        [
            sys.executable,
            "tools/validate_mcp_consults.py",
            str(path),
            "--require-lineage",
            "--require-motifs",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode != 0
    assert "MCP_CONSULTS_INVALID" in completed.stdout
    assert "PLACEHOLDER" in completed.stderr


def test_validator_prints_valid_for_pond_backed_consult(tmp_path: Path) -> None:
    path = tmp_path / "consults.jsonl"
    path.write_text(
        (
            '{"adapter_status":"pond_backed","verdict":"ok",'
            '"lineage_hashes":["aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"],'
            '"returned_motifs":["traceable motif"]}\n'
        ),
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            "tools/validate_mcp_consults.py",
            str(path),
            "--require-lineage",
            "--require-motifs",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert completed.stdout.strip() == "MCP_CONSULTS_VALID"
    assert completed.stderr == ""
