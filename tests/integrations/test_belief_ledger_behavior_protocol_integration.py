from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path
from typing import Iterator

import pytest

from operational_cognition.mcp.belief_ledger_behavior_client import (
    BEHAVIOR_PROTOCOL_SCHEMA,
    BehaviorProtocolValidationError,
    BeliefLedgerBehaviorClient,
    build_behavior_protocol_request,
    hash_canonical_json,
    _validate_behavior_data,
)
from tools.integrations.run_belief_ledger_behavior_protocol_probe import (
    DEFAULT_CONFIG,
    deterministic_ledger_state,
    deterministic_query_trace,
    perturbation_for_fixture,
    run_probe,
)


BELIEF_LEDGER_ROOT = Path.home() / "Desktop" / "Belief-Ledger"
if not BELIEF_LEDGER_ROOT.exists():
    pytest.skip("Belief Ledger sibling repo is required for this integration test.", allow_module_level=True)
if str(BELIEF_LEDGER_ROOT) not in sys.path:
    sys.path.insert(0, str(BELIEF_LEDGER_ROOT))

from belief_ledger.integrations.inside_voice.behavior_protocol import run_behavior_protocol  # noqa: E402


class _InProcessResponse:
    status = 200

    def __init__(self, payload: dict[str, object]):
        self._body = json.dumps(payload, sort_keys=True).encode("utf-8")

    def read(self) -> bytes:
        return self._body

    def __enter__(self) -> "_InProcessResponse":
        return self

    def __exit__(self, *_exc: object) -> None:
        return None


@pytest.fixture()
def belief_ledger_url(monkeypatch: pytest.MonkeyPatch) -> Iterator[str]:
    def in_process_urlopen(request: urllib.request.Request, timeout: float | None = None) -> _InProcessResponse:
        payload = json.loads((request.data or b"{}").decode("utf-8"))
        data = run_behavior_protocol(payload)
        return _InProcessResponse(
            {
                "ok": True,
                "verdict": "INSIDE_VOICE_PROTOCOL_SERVER_READY",
                "data": data,
                "errors": [],
                "warnings": [],
            }
        )

    monkeypatch.setattr(urllib.request, "urlopen", in_process_urlopen)
    yield "http://belief-ledger.test"


def client_for(tmp_path: Path, url: str) -> BeliefLedgerBehaviorClient:
    return BeliefLedgerBehaviorClient(
        base_url=url,
        raw_request_log_path=tmp_path / "raw_requests.jsonl",
        raw_response_log_path=tmp_path / "raw_responses.jsonl",
        behavior_call_log_path=tmp_path / "behavior_protocol_calls.jsonl",
    )


def test_client_builds_valid_deterministic_request() -> None:
    query = deterministic_query_trace()
    state = deterministic_ledger_state()
    first = build_behavior_protocol_request("activation_only", query, state, DEFAULT_CONFIG)
    second = build_behavior_protocol_request("activation_only", query, state, DEFAULT_CONFIG)

    assert first == second
    assert first["mode"] == "activation_only"
    assert first["query_trace"]["trace_id"] == "query-proof-045-operational-collapse"
    assert first["ledger_state"]["traces"]
    assert first["run_id"].startswith("oc-proof-045-")
    assert hash_canonical_json(first) == hash_canonical_json(second)


def test_unknown_mode_fails_closed(tmp_path: Path, belief_ledger_url: str) -> None:
    client = client_for(tmp_path, belief_ledger_url)

    response = client.call_behavior_protocol(
        "not_a_mode",
        deterministic_query_trace(),
        deterministic_ledger_state(),
        DEFAULT_CONFIG,
    )

    assert response["adapter_status"] == "error"
    assert response["verdict"] == "fail_closed"
    assert response["fail_closed_reason"] == "unknown_mode"
    assert (tmp_path / "raw_requests.jsonl").read_text(encoding="utf-8")
    assert not (tmp_path / "behavior_protocol_calls.jsonl").exists()


def test_missing_motifs_or_lineages_fail_validation() -> None:
    base = {
        "schema_version": BEHAVIOR_PROTOCOL_SCHEMA,
        "mode": "activation_only",
        "core_mutation_count": 0,
        "advisory_only": True,
        "artifacts": {
            "activation_field": {
                "core_mutation_count": 0,
                "activated_motifs": [],
                "activated_pathways": [],
                "lineage_hashes": [],
                "lineage_refs": [],
            }
        },
    }

    with pytest.raises(BehaviorProtocolValidationError, match="missing_motifs"):
        _validate_behavior_data(base, mode="activation_only")

    missing_lineage = json.loads(json.dumps(base))
    missing_lineage["artifacts"]["activation_field"]["activated_motifs"] = [
        {"motif": "operational_collapse", "motif_id": "motif:operational_collapse"}
    ]
    missing_lineage["artifacts"]["activation_field"]["activated_pathways"] = [
        {"pathway": "THRESHOLD_GATE", "supporting_motif_ids": ["motif:operational_collapse"]}
    ]
    with pytest.raises(BehaviorProtocolValidationError, match="missing_lineages"):
        _validate_behavior_data(missing_lineage, mode="activation_only")


def test_activation_only_response_has_multiple_activated_mechanisms(tmp_path: Path, belief_ledger_url: str) -> None:
    response = client_for(tmp_path, belief_ledger_url).call_behavior_protocol(
        "activation_only",
        deterministic_query_trace(),
        deterministic_ledger_state(),
        DEFAULT_CONFIG,
    )

    assert response["adapter_status"] == "pond_backed"
    assert len(response["activated_mechanisms"]) >= 2


def test_field_interaction_response_has_interactions(tmp_path: Path, belief_ledger_url: str) -> None:
    response = client_for(tmp_path, belief_ledger_url).call_behavior_protocol(
        "field_interaction",
        deterministic_query_trace(),
        deterministic_ledger_state(),
        DEFAULT_CONFIG,
    )

    assert response["adapter_status"] == "pond_backed"
    assert response["field_interactions"]


def test_delayed_ranking_response_has_surviving_pathways(tmp_path: Path, belief_ledger_url: str) -> None:
    response = client_for(tmp_path, belief_ledger_url).call_behavior_protocol(
        "delayed_ranking",
        deterministic_query_trace(),
        deterministic_ledger_state(),
        DEFAULT_CONFIG,
    )

    assert response["adapter_status"] == "pond_backed"
    assert response["surviving_pathways"]
    assert any(row["collapse_status"] == "survived" for row in response["ranked_pathways"])


def test_collapse_trace_has_eliminated_surviving_pathways_and_reasons(tmp_path: Path, belief_ledger_url: str) -> None:
    response = client_for(tmp_path, belief_ledger_url).call_behavior_protocol(
        "collapse_trace",
        deterministic_query_trace(),
        deterministic_ledger_state(),
        DEFAULT_CONFIG,
    )
    trace = response["collapse_trace"]

    assert response["adapter_status"] == "pond_backed"
    assert trace["survived_after_collapse"]
    assert trace["eliminated_pathways"]
    assert trace["collapse_reasons"]


def test_perturbation_changes_field_or_records_no_effect_reason(tmp_path: Path, belief_ledger_url: str) -> None:
    response = client_for(tmp_path, belief_ledger_url).call_behavior_protocol(
        "perturbation",
        deterministic_query_trace(),
        deterministic_ledger_state(),
        DEFAULT_CONFIG,
        perturbation_for_fixture(),
    )

    assert response["adapter_status"] == "pond_backed"
    assert response["perturbations"]
    assert response["perturbations"][0].get("changed") is True or response["perturbations"][0].get("no_effect_reason")


def test_probe_writes_deterministic_proof_artifacts(tmp_path: Path, belief_ledger_url: str) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"

    first_result = run_probe(belief_ledger_url, first)
    second_result = run_probe(belief_ledger_url, second)

    assert first_result["audit"]["hostile_verdict"] == "VERY_STRONG_SIGNAL"
    assert second_result["audit"]["hostile_verdict"] == "VERY_STRONG_SIGNAL"
    assert json.loads((first / "analysis" / "integration_metrics.json").read_text(encoding="utf-8")) == json.loads(
        (second / "analysis" / "integration_metrics.json").read_text(encoding="utf-8")
    )
    assert (first / "mcp" / "behavior_protocol_calls.jsonl").read_text(encoding="utf-8") == (
        second / "mcp" / "behavior_protocol_calls.jsonl"
    ).read_text(encoding="utf-8")
    for relative in [
        "README.md",
        "proof_manifest.json",
        "mcp/raw_requests.jsonl",
        "mcp/raw_responses.jsonl",
        "mcp/behavior_protocol_calls.jsonl",
        "results/activation_only_result.json",
        "results/field_interaction_result.json",
        "results/delayed_ranking_result.json",
        "results/collapse_trace_result.json",
        "results/perturbation_result.json",
        "analysis/integration_metrics.json",
        "analysis/hostile_integration_audit.json",
    ]:
        assert (first / relative).is_file()
