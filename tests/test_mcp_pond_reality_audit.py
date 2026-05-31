from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT / "proofs" / "035-mcp-pond-reality-audit"


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def all_mcp_rows() -> list[dict]:
    rows: list[dict] = []
    for path in sorted((PROOF / "mcp").glob("*.jsonl")):
        rows.extend(jsonl(path))
    return rows


def test_phase_counts_match_proof_035_protocol() -> None:
    assert len(jsonl(PROOF / "mcp" / "empty_pond_consults.jsonl")) == 20
    assert len(jsonl(PROOF / "mcp" / "seasoning_log.jsonl")) == 12
    assert len(jsonl(PROOF / "mcp" / "flow_recall_consults.jsonl")) == 3
    assert len(jsonl(PROOF / "mcp" / "negative_recall_consults.jsonl")) == 3
    assert len(jsonl(PROOF / "mcp" / "stability_consults.jsonl")) == 20
    assert len(jsonl(PROOF / "mcp" / "incremental_seasoning_log.jsonl")) == 6
    assert len(jsonl(PROOF / "mcp" / "incremental_recall_consults.jsonl")) == 4


def test_current_mcp_rows_are_placeholder_and_fail_gate() -> None:
    rows = all_mcp_rows()

    assert len(rows) == 68
    assert Counter(row["classification"] for row in rows) == {"PLACEHOLDER": 68}
    assert Counter(row["adapter_status"] for row in rows) == {"placeholder": 68}
    assert all(row["gate_passed"] is False for row in rows)
    assert all("classification=PLACEHOLDER" in row["gate_error"] for row in rows)


def test_transport_hashes_do_not_count_as_pond_recall() -> None:
    flow = load_json(PROOF / "flow_recall_audit.json")
    stability = load_json(PROOF / "stability_audit.json")

    assert flow["transport_hashes_returned"] is True
    assert flow["were_hashes_returned"] is False
    assert flow["were_lineages_returned"] is False
    assert flow["were_motifs_returned"] is False
    assert flow["was_recall_traceable"] is False
    assert stability["transport_hash_stability"] is True
    assert stability["hash_stability"] is False
    assert stability["lineage_stability"] is False
    assert stability["motif_stability"] is False


def test_hostile_mcp_audit_currently_fails_as_instrument() -> None:
    hostile = load_json(PROOF / "hostile_mcp_audit.json")
    final = hostile["final_verdict"]

    assert final == {
        "pond_backed_recall_exists": False,
        "traceable_lineage_exists": False,
        "stable_motif_recall_exists": False,
        "remaining_placeholder_explanation": True,
        "remaining_scaffold_explanation": True,
        "hostile_verdict": (
            "FAIL: current MCP responses did not produce stable pond-backed mechanism recall; "
            "placeholder or non-pond-backed behavior remains the sufficient explanation."
        ),
    }


def test_blind_evaluation_does_not_identify_seasoned_mechanisms() -> None:
    blind = load_json(PROOF / "blind_consult_evaluation.json")
    mechanism_trials = [row for row in blind["evaluations"] if row["expected_for_scoring"] != "UNKNOWN"]

    assert blind["above_chance_on_seasoned_mechanisms"] is False
    assert blind["mechanism_accuracy"] == 0.0
    assert mechanism_trials
    assert all(row["classification"] == "UNKNOWN" for row in mechanism_trials)


def test_validator_rejects_proof_035_mcp_logs() -> None:
    paths = sorted((PROOF / "mcp").glob("*.jsonl"))
    completed = subprocess.run(
        [
            sys.executable,
            "tools/validate_mcp_consults.py",
            *[str(path) for path in paths],
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


def test_proof_035_manifest_validates() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "tools/validate_proof_manifest.py",
            "proofs/035-mcp-pond-reality-audit/proof_manifest.json",
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert completed.stdout.strip() == "PROOF_MANIFEST_VALID"
