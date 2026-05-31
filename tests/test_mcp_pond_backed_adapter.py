from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from operational_cognition.mcp.consult_classifier import MCPConsultClass, classify_mcp_response
from tools.integrations.inside_voice_mcp_server import process_consult_request


ROOT = Path(__file__).resolve().parents[1]


def payload(request_id: str, task: str, *, summary: str = "adapter regression test") -> dict:
    return {
        "request_id": request_id,
        "task": task,
        "mode": "audit",
        "max_output_chars": 8000,
        "require_lineage": True,
        "context": {
            "summary": summary,
            "files": [],
            "constraints": ["Return real pond-backed recall or fail closed."],
            "desired_artifacts": ["returned_motifs", "returned_lineages", "lineage_hashes"],
        },
    }


def season_flow(tmp_path: Path) -> tuple[Path, dict]:
    state_path = tmp_path / "pond_state.json"
    result = process_consult_request(
        payload(
            "season-flow-001",
            "ACTION: SEASON. Mechanism label: FLOW. A source sends water through a path; a narrowed throat adds resistance and downstream throughput declines.",
        ),
        artifact_dir=tmp_path / "artifacts",
        state_path=state_path,
    )
    assert result.status_code == 200
    return state_path, result.response


def recall_flow(state_path: Path, tmp_path: Path, request_id: str = "recall-flow-001") -> dict:
    result = process_consult_request(
        payload(
            request_id,
            "Water restriction in a channel creates a bottleneck; throughput declines and upstream backlog grows.",
        ),
        artifact_dir=tmp_path / "artifacts",
        state_path=state_path,
    )
    assert result.status_code == 200
    return result.response


def test_placeholder_text_cannot_appear_in_successful_response(tmp_path: Path) -> None:
    state_path, _seasoning = season_flow(tmp_path)
    response = recall_flow(state_path, tmp_path)

    assert response["verdict"] == "ok"
    assert "placeholder" not in json.dumps(response).lower()


def test_successful_consult_classifies_as_pond_backed(tmp_path: Path) -> None:
    state_path, _seasoning = season_flow(tmp_path)
    response = recall_flow(state_path, tmp_path)

    assert response["adapter_status"] == "pond_backed"
    assert response["response_source"] == "inside_voice_pond"
    assert classify_mcp_response(response) == MCPConsultClass.POND_BACKED


def test_missing_pond_state_fails_closed(tmp_path: Path) -> None:
    missing_state = tmp_path / "missing_pond_state.json"
    result = process_consult_request(
        payload("recall-missing-pond", "Water restriction causes throughput decline."),
        artifact_dir=tmp_path / "artifacts",
        state_path=missing_state,
    )

    assert result.status_code == 200
    assert result.response["adapter_status"] == "error"
    assert result.response["verdict"] == "fail_closed"
    assert result.response["fail_closed_reason"] == "pond_unavailable"
    assert classify_mcp_response(result.response) == MCPConsultClass.ERROR


def test_unknown_mode_fails_closed_without_placeholder(tmp_path: Path) -> None:
    state_path, _seasoning = season_flow(tmp_path)
    request = payload("unknown-mode-001", "Water restriction causes throughput decline.")
    request["mode"] = "not_a_protocol_mode"

    result = process_consult_request(
        request,
        artifact_dir=tmp_path / "artifacts",
        state_path=state_path,
    )

    assert result.status_code == 200
    assert result.response["adapter_status"] == "error"
    assert result.response["verdict"] == "fail_closed"
    assert result.response["fail_closed_reason"] == "unknown_mode"
    assert "placeholder" not in json.dumps(result.response).lower()
    assert classify_mcp_response(result.response) == MCPConsultClass.ERROR


def test_returned_lineage_hashes_are_stable(tmp_path: Path) -> None:
    state_path, _seasoning = season_flow(tmp_path)
    first = recall_flow(state_path, tmp_path, "recall-flow-stable-001")
    second = recall_flow(state_path, tmp_path, "recall-flow-stable-002")

    assert first["lineage_hashes"]
    assert first["lineage_hashes"] == second["lineage_hashes"]


def test_returned_motifs_are_non_empty_after_seasoning(tmp_path: Path) -> None:
    state_path, seasoning = season_flow(tmp_path)
    response = recall_flow(state_path, tmp_path)

    assert seasoning["returned_motifs"]
    assert response["returned_motifs"]
    assert {"Source", "Path", "Resistance", "Flow"}.issubset(set(response["returned_motifs"]))
    assert response["returned_lineages"]
    assert response["lineage_hashes"]


def test_extended_mechanism_catalog_is_pond_backed(tmp_path: Path) -> None:
    state_path = tmp_path / "pond_state.json"
    season = process_consult_request(
        payload(
            "season-feedback-001",
            "ACTION: SEASON. Mechanism label: FEEDBACK. A signal loops back into a response; reinforcement amplifies the next signal.",
        ),
        artifact_dir=tmp_path / "artifacts",
        state_path=state_path,
    )
    recall = process_consult_request(
        payload("recall-feedback-001", "A feedback loop reinforces each response and becomes runaway."),
        artifact_dir=tmp_path / "artifacts",
        state_path=state_path,
    )

    assert season.status_code == 200
    assert recall.status_code == 200
    assert recall.response["verdict"] == "ok"
    assert classify_mcp_response(recall.response) == MCPConsultClass.POND_BACKED
    assert "FEEDBACK" in {payload["mechanism"] for payload in recall.response["lineage_payloads"]}
    assert {"Signal", "Loop", "Response", "Reinforcement"}.issubset(set(recall.response["returned_motifs"]))


def test_activation_only_returns_mechanism_field(tmp_path: Path) -> None:
    state_path = tmp_path / "pond_state.json"
    lessons = [
        (
            "season-threshold-001",
            "ACTION: SEASON. Mechanism label: THRESHOLD. A value crosses a critical limit and triggers a state switch.",
        ),
        (
            "season-feedback-activation-001",
            "ACTION: SEASON. Mechanism label: FEEDBACK. A signal returns through a loop and reinforces the next response.",
        ),
    ]
    for request_id, task in lessons:
        result = process_consult_request(
            payload(request_id, task),
            artifact_dir=tmp_path / "artifacts",
            state_path=state_path,
        )
        assert result.status_code == 200

    activation_request = payload(
        "activation-field-001",
        (
            "Observation only. Activation only.\n"
            "Observation:\n"
            "A signal loops back and reinforces output after a critical limit is crossed.\n"
            "Required:\n"
            "- activated mechanisms\n"
            "- activated motifs\n"
            "- activated lineages\n"
            "- activation weights"
        ),
    )
    activation_request["mode"] = "activation_only"
    result = process_consult_request(
        activation_request,
        artifact_dir=tmp_path / "artifacts",
        state_path=state_path,
    )

    assert result.status_code == 200
    assert result.response["verdict"] == "ok"
    assert classify_mcp_response(result.response) == MCPConsultClass.POND_BACKED
    activated = {row["mechanism"] for row in result.response["activated_mechanisms"]}
    assert {"THRESHOLD", "FEEDBACK"}.issubset(activated)
    assert result.response["activation_weights"]


def test_negative_recall_fails_closed_without_placeholder(tmp_path: Path) -> None:
    state_path, _seasoning = season_flow(tmp_path)
    result = process_consult_request(
        payload("recall-unsupported", "Bearing seizure in a rotating support."),
        artifact_dir=tmp_path / "artifacts",
        state_path=state_path,
    )

    assert result.status_code == 200
    assert result.response["verdict"] == "fail_closed"
    assert result.response["fail_closed_reason"] == "no_relevant_pond_recall"
    assert "placeholder" not in json.dumps(result.response).lower()
    assert classify_mcp_response(result.response) == MCPConsultClass.ERROR


def test_validate_mcp_consults_passes_for_real_pond_backed_fixture(tmp_path: Path) -> None:
    state_path, _seasoning = season_flow(tmp_path)
    response = recall_flow(state_path, tmp_path)
    fixture = tmp_path / "pond_backed_consults.jsonl"
    fixture.write_text(json.dumps(response, sort_keys=True) + "\n", encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            "tools/validate_mcp_consults.py",
            str(fixture),
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
