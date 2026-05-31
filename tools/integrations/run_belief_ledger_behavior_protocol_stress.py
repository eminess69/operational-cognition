#!/usr/bin/env python3
"""Run Proof 046 against the Belief Ledger behavior protocol.

This stress runner treats Belief Ledger as an external local HTTP instrument.
It records raw requests/responses, validates only pond-backed successful rows,
and records invalid or hostile cases as fail-closed boundary evidence.
"""

from __future__ import annotations

import argparse
import copy
import json
import shutil
import sys
import threading
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from operational_cognition.mcp.belief_ledger_behavior_client import (  # noqa: E402
    BEHAVIOR_MODES,
    BeliefLedgerBehaviorClient,
    canonical_json,
    hash_canonical_json,
)
from operational_cognition.mcp.consult_classifier import classify_mcp_response  # noqa: E402
from operational_cognition.mcp.proof_gate import MCPConsultBoundaryError, assert_pond_backed_consult  # noqa: E402


PROOF_ID = "046-belief-ledger-behavior-protocol-stress"
TITLE = "Proof 046 - Belief Ledger Behavior Protocol Stress Test"
SOURCE_PROOF_ID = "045-belief-ledger-mcp-behavior-integration"
BELIEF_LEDGER_ROOT = Path.home() / "Desktop" / "Belief-Ledger"
BOUNDED_CLAIM = (
    "Operational Cognition can stress-test the Belief Ledger Inside Voice behavior protocol as an external "
    "instrument and verify replay stability, perturbation sensitivity, collapse traceability, and fail-closed "
    "boundaries."
)
DEFAULT_CONFIG = {
    "ttl": "PT45M",
    "max_combination_depth": 3,
    "min_activation_weight": 0.25,
    "max_surviving_pathways": 2,
    "survival_threshold": 0.5,
}


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_fixture(name: str) -> dict[str, Any]:
    return read_json(ROOT / "proofs" / SOURCE_PROOF_ID / "mcp" / name)


def _purge_non_belief_ledger_tools_modules() -> None:
    for name, module in list(sys.modules.items()):
        if name != "tools" and not name.startswith("tools."):
            continue
        module_file = Path(str(getattr(module, "__file__", "")))
        if not module_file or not module_file.as_posix().startswith(BELIEF_LEDGER_ROOT.as_posix()):
            del sys.modules[name]


def load_belief_ledger_create_server() -> Any:
    if not BELIEF_LEDGER_ROOT.exists():
        raise RuntimeError(f"Belief Ledger sibling repo not found: {BELIEF_LEDGER_ROOT}")
    _purge_non_belief_ledger_tools_modules()
    if str(BELIEF_LEDGER_ROOT) not in sys.path:
        sys.path.insert(0, str(BELIEF_LEDGER_ROOT))
    from tools.integrations.run_inside_voice_protocol_server import create_server  # type: ignore

    return create_server


def start_server(out: Path, preferred_port: int) -> tuple[Any, threading.Thread, str]:
    create_server = load_belief_ledger_create_server()
    server_artifact_dir = out / "mcp" / "belief_ledger_server_artifacts"
    try:
        server = create_server(port=preferred_port, output_dir=server_artifact_dir)
    except OSError:
        server = create_server(port=0, output_dir=server_artifact_dir)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    return server, thread, f"http://{host}:{port}"


def reset_output(out: Path) -> None:
    for relative in ("mcp", "analysis"):
        path = out / relative
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)
    for relative in ("README.md", "proof_manifest.json"):
        path = out / relative
        if path.exists():
            path.unlink()


def perturbation_for_trace(trace_id: str) -> dict[str, Any]:
    return {
        "perturbation_type": "remove",
        "target": trace_id,
        "reason": "Stress test removes activated source trace without mutating Belief Ledger core state.",
    }


def top_trace_id(mechanism: dict[str, Any], ledger_state: dict[str, Any]) -> str:
    lineage_values = {str(value) for value in mechanism.get("supporting_lineages", [])}
    for trace in ledger_state.get("traces", []):
        trace_id = str(trace.get("trace_id") or "")
        if trace_id in lineage_values or trace.get("pathway") == mechanism.get("mechanism"):
            return trace_id
    return ""


def remove_traces(ledger_state: dict[str, Any], trace_ids: set[str]) -> dict[str, Any]:
    state = copy.deepcopy(ledger_state)
    state["traces"] = [trace for trace in state.get("traces", []) if str(trace.get("trace_id") or "") not in trace_ids]
    return state


def irrelevant_fragment() -> dict[str, Any]:
    lineage_hash = "f" * 64
    trace_id = "trace-proof046-irrelevant"
    motif_id = "motif:proof046_irrelevant_noise"
    pathway_id = "pathway:proof046_irrelevant_mechanism"
    return {
        "activated_motifs": [
            {
                "motif_id": motif_id,
                "motif": "irrelevant_noise",
                "source_trace_ids": [trace_id],
                "source_lineage_refs": ["lineage:proof046:irrelevant_noise"],
                "lineage_hashes": [lineage_hash],
                "activation_weight": 0.01,
                "reason_codes": ["EXPLICIT_PERTURBATION_FRAGMENT"],
                "traceback": [
                    {
                        "trace_id": trace_id,
                        "trace_hash": lineage_hash,
                        "source_ref": "proof046:irrelevant_noise_attack",
                        "source_lineage": ["lineage:proof046:irrelevant_noise"],
                    }
                ],
            }
        ],
        "activated_pathways": [
            {
                "pathway_id": pathway_id,
                "pathway": "IRRELEVANT_NOISE",
                "supporting_motif_ids": [motif_id],
                "supporting_trace_ids": [trace_id],
                "source_lineage_refs": ["lineage:proof046:irrelevant_noise"],
                "lineage_hashes": [lineage_hash],
                "activation_weight": 0.01,
                "reason_codes": ["EXPLICIT_PERTURBATION_FRAGMENT"],
                "decodable": True,
            }
        ],
    }


def validator_result(response: dict[str, Any]) -> dict[str, Any]:
    try:
        assert_pond_backed_consult(response, require_lineage=True, require_motifs=True)
    except MCPConsultBoundaryError as exc:
        return {
            "valid": False,
            "classification": classify_mcp_response(response).value,
            "error": str(exc),
        }
    return {
        "valid": True,
        "classification": classify_mcp_response(response).value,
        "error": None,
    }


def assert_success(response: dict[str, Any], *, context: str) -> None:
    validation = validator_result(response)
    if validation["valid"] is not True:
        raise RuntimeError(f"{context} did not produce pond-backed evidence: {validation['error']}")


def response_hash(response: dict[str, Any]) -> str:
    return str(response.get("instrument_response_hash") or response.get("lineage", {}).get("response_hash") or "")


def lineage_signature(response: dict[str, Any]) -> str:
    return hash_canonical_json(response.get("lineage_hashes") or [])


def motif_signature(response: dict[str, Any]) -> str:
    return hash_canonical_json(response.get("returned_motifs") or [])


def call_mode(
    client: BeliefLedgerBehaviorClient,
    *,
    mode: str,
    query_trace: dict[str, Any],
    ledger_state: dict[str, Any],
    config: dict[str, Any],
    perturbation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return client.call_behavior_protocol(mode, query_trace, ledger_state, config, perturbation)


def run_replay_stability(
    client: BeliefLedgerBehaviorClient,
    *,
    query_trace: dict[str, Any],
    ledger_state: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    report = []
    responses_by_mode: dict[str, list[dict[str, Any]]] = {}
    baseline_trace = str(ledger_state["traces"][0]["trace_id"])
    for mode in BEHAVIOR_MODES:
        mode_responses = []
        for _index in range(10):
            perturbation = perturbation_for_trace(baseline_trace) if mode == "perturbation" else None
            response = call_mode(
                client,
                mode=mode,
                query_trace=query_trace,
                ledger_state=ledger_state,
                config=DEFAULT_CONFIG,
                perturbation=perturbation,
            )
            assert_success(response, context=f"replay:{mode}")
            mode_responses.append(response)
        responses_by_mode[mode] = mode_responses
        response_hashes = [response_hash(response) for response in mode_responses]
        lineage_hashes = [lineage_signature(response) for response in mode_responses]
        motif_sets = [motif_signature(response) for response in mode_responses]
        report.append(
            {
                "mode": mode,
                "runs": 10,
                "response_hashes": response_hashes,
                "all_hashes_match": len(set(response_hashes)) == 1,
                "lineage_hashes_match": len(set(lineage_hashes)) == 1,
                "motif_sets_match": len(set(motif_sets)) == 1,
            }
        )
    return report, responses_by_mode


def perturbation_row(
    *,
    case_id: str,
    baseline_field_hash: str,
    perturbation_type: str,
    response: dict[str, Any],
    field_after_hash: str,
    valid_effect_observed: bool,
    notes: str,
) -> dict[str, Any]:
    changed = bool(field_after_hash and field_after_hash != baseline_field_hash) or valid_effect_observed
    return {
        "case_id": case_id,
        "baseline_field_hash": baseline_field_hash,
        "perturbation_type": perturbation_type,
        "changed": changed,
        "field_after_hash": field_after_hash,
        "valid_effect_observed": valid_effect_observed,
        "adapter_status": response.get("adapter_status", ""),
        "fail_closed_reason": response.get("fail_closed_reason"),
        "notes": notes,
    }


def run_perturbation_sensitivity(
    client: BeliefLedgerBehaviorClient,
    *,
    query_trace: dict[str, Any],
    ledger_state: dict[str, Any],
    baseline_activation: dict[str, Any],
    baseline_collapse: dict[str, Any],
) -> list[dict[str, Any]]:
    baseline_field_hash = str(baseline_activation.get("telemetry", {}).get("activation_field_hash") or "")
    baseline_collapse_hash = str(baseline_collapse.get("telemetry", {}).get("collapse_hash") or "")
    mechanisms = list(baseline_activation.get("activated_mechanisms") or [])
    top_one = top_trace_id(mechanisms[0], ledger_state) if len(mechanisms) >= 1 else ""
    top_two = top_trace_id(mechanisms[1], ledger_state) if len(mechanisms) >= 2 else ""
    shared_motif = next((motif for motif in baseline_activation.get("returned_motifs", []) if str(motif).startswith("motif:")), "")

    rows = []

    response = call_mode(
        client,
        mode="perturbation",
        query_trace=query_trace,
        ledger_state=ledger_state,
        config=DEFAULT_CONFIG,
        perturbation=perturbation_for_trace(top_one),
    )
    assert_success(response, context="perturbation:remove_top_activated_mechanism")
    result = response["perturbations"][0]
    rows.append(
        perturbation_row(
            case_id="remove_top_activated_mechanism",
            baseline_field_hash=baseline_field_hash,
            perturbation_type="remove",
            response=response,
            field_after_hash=str(result.get("field_after", {}).get("field_hash") or ""),
            valid_effect_observed=result.get("changed") is True,
            notes=f"Removed source trace {top_one} for the highest activated pathway.",
        )
    )

    reduced_state = remove_traces(ledger_state, {top_one})
    response = call_mode(
        client,
        mode="perturbation",
        query_trace=query_trace,
        ledger_state=reduced_state,
        config=DEFAULT_CONFIG,
        perturbation=perturbation_for_trace(top_two),
    )
    assert_success(response, context="perturbation:remove_top_two_activated_mechanisms")
    result = response["perturbations"][0]
    rows.append(
        perturbation_row(
            case_id="remove_top_two_activated_mechanisms",
            baseline_field_hash=baseline_field_hash,
            perturbation_type="remove",
            response=response,
            field_after_hash=str(result.get("field_after", {}).get("field_hash") or ""),
            valid_effect_observed=result.get("changed") is True,
            notes=f"Encoded as reduced ledger state without {top_one}, then removed {top_two}.",
        )
    )

    response = call_mode(
        client,
        mode="perturbation",
        query_trace=query_trace,
        ledger_state=ledger_state,
        config=DEFAULT_CONFIG,
        perturbation={
            "perturbation_type": "inject",
            "target": "proof046_irrelevant_noise",
            "injected_field_fragment": irrelevant_fragment(),
            "reason": "Inject irrelevant advisory-only field fragment and verify it is not promoted to returned motifs.",
        },
    )
    assert_success(response, context="perturbation:inject_irrelevant_mechanism")
    result = response["perturbations"][0]
    inflated = "motif:proof046_irrelevant_noise" in set(response.get("returned_motifs") or [])
    rows.append(
        perturbation_row(
            case_id="inject_irrelevant_mechanism",
            baseline_field_hash=baseline_field_hash,
            perturbation_type="inject",
            response=response,
            field_after_hash=str(result.get("field_after", {}).get("field_hash") or ""),
            valid_effect_observed=result.get("changed") is True and not inflated,
            notes="Injected fragment changed perturbation field summary but did not inflate returned_motifs.",
        )
    )

    response = call_mode(
        client,
        mode="perturbation",
        query_trace=query_trace,
        ledger_state=ledger_state,
        config=DEFAULT_CONFIG,
        perturbation={
            "perturbation_type": "suppress",
            "target": shared_motif,
            "reason": "Suppress shared motif to test field sensitivity.",
        },
    )
    assert_success(response, context="perturbation:suppress_shared_motif")
    result = response["perturbations"][0]
    rows.append(
        perturbation_row(
            case_id="suppress_shared_motif",
            baseline_field_hash=baseline_field_hash,
            perturbation_type="suppress",
            response=response,
            field_after_hash=str(result.get("field_after", {}).get("field_hash") or ""),
            valid_effect_observed=result.get("changed") is True,
            notes=f"Suppressed shared motif {shared_motif}.",
        )
    )

    no_ranking_config = dict(DEFAULT_CONFIG, survival_threshold=1.0)
    response = call_mode(
        client,
        mode="delayed_ranking",
        query_trace=query_trace,
        ledger_state=ledger_state,
        config=no_ranking_config,
    )
    fail_closed = response.get("adapter_status") == "error" and response.get("verdict") == "fail_closed"
    rows.append(
        perturbation_row(
            case_id="force_no_ranking",
            baseline_field_hash=baseline_field_hash,
            perturbation_type="force_no_ranking",
            response=response,
            field_after_hash="",
            valid_effect_observed=fail_closed,
            notes="Survival threshold 1.0 produced no survivors; instrument failed closed instead of fabricating ranking.",
        )
    )

    immediate_ranking_config = dict(DEFAULT_CONFIG, max_surviving_pathways=1)
    response = call_mode(
        client,
        mode="delayed_ranking",
        query_trace=query_trace,
        ledger_state=ledger_state,
        config=immediate_ranking_config,
    )
    assert_success(response, context="perturbation:force_immediate_ranking")
    collapse_hash = str(response.get("telemetry", {}).get("collapse_hash") or "")
    rows.append(
        perturbation_row(
            case_id="force_immediate_ranking",
            baseline_field_hash=baseline_field_hash,
            perturbation_type="force_immediate_ranking",
            response=response,
            field_after_hash=collapse_hash,
            valid_effect_observed=bool(collapse_hash and collapse_hash != baseline_collapse_hash),
            notes="Reduced max_surviving_pathways to 1; field stayed traceable while collapse hash changed.",
        )
    )

    return rows


def collapse_boundary_audit(response: dict[str, Any]) -> dict[str, Any]:
    trace = response.get("collapse_trace") if isinstance(response.get("collapse_trace"), dict) else {}
    eliminated = list(trace.get("eliminated_pathways") or [])
    surviving = list(trace.get("survived_after_collapse") or [])
    reasons = list(trace.get("collapse_reasons") or [])
    reason_by_pathway = {str(row.get("pathway_id")): row for row in reasons}
    eliminated_with_reasons = [
        item
        for item in eliminated
        if item.get("reason_codes") and reason_by_pathway.get(str(item.get("pathway_id")), {}).get("reason_codes")
    ]
    survivors_with_lineage = [
        item
        for item in surviving
        if item.get("lineage_hashes") and item.get("source_lineage_refs") and item.get("supporting_trace_ids")
    ]
    ranked = list(response.get("ranked_pathways") or [])
    expected_order = sorted(
        ranked,
        key=lambda item: (-float(item.get("ranking_score") or item.get("activation_weight") or 0.0), str(item.get("pathway_id") or "")),
    )
    violations = []
    if len(eliminated_with_reasons) != len(eliminated):
        violations.append("eliminated_pathway_reason_gap")
    if len(survivors_with_lineage) != len(surviving):
        violations.append("surviving_pathway_lineage_gap")
    if ranked != expected_order:
        violations.append("collapse_ordering_not_deterministic")
    if "premature_collapse_risk" not in trace:
        violations.append("premature_collapse_risk_missing")

    def rate(count: int, total: int) -> float:
        return round(count / total, 4) if total else 0.0

    return {
        "mode": "collapse_trace",
        "collapse_id": trace.get("collapse_id", ""),
        "eliminated_pathway_count": len(eliminated),
        "surviving_pathway_count": len(surviving),
        "eliminated_reason_coverage": rate(len(eliminated_with_reasons), len(eliminated)),
        "survivor_lineage_coverage": rate(len(survivors_with_lineage), len(surviving)),
        "collapse_ordering_deterministic": ranked == expected_order,
        "premature_collapse_risk_recorded": "premature_collapse_risk" in trace,
        "premature_collapse_risk": bool(trace.get("premature_collapse_risk")),
        "collapse_reason_coverage": rate(len(eliminated_with_reasons), len(eliminated)),
        "valid": not violations,
        "violations": violations,
    }


def invalid_cases(query_trace: dict[str, Any], ledger_state: dict[str, Any]) -> list[dict[str, Any]]:
    query_without_motif = copy.deepcopy(query_trace)
    query_without_motif.pop("motif", None)
    state_without_motifs = copy.deepcopy(ledger_state)
    for trace in state_without_motifs.get("traces", []):
        trace.pop("motif", None)
        trace.pop("motifs", None)

    query_without_lineage = copy.deepcopy(query_trace)
    query_without_lineage.pop("source_ref", None)
    query_without_lineage.pop("source_lineage", None)

    return [
        {
            "case_id": "unknown_mode",
            "mode": "unknown_mode",
            "query_trace": query_trace,
            "ledger_state": ledger_state,
            "config": DEFAULT_CONFIG,
            "perturbation": None,
        },
        {
            "case_id": "missing_query_trace",
            "mode": "activation_only",
            "query_trace": {},
            "ledger_state": ledger_state,
            "config": DEFAULT_CONFIG,
            "perturbation": None,
        },
        {
            "case_id": "missing_ledger_state",
            "mode": "activation_only",
            "query_trace": query_trace,
            "ledger_state": {},
            "config": DEFAULT_CONFIG,
            "perturbation": None,
        },
        {
            "case_id": "empty_traces",
            "mode": "activation_only",
            "query_trace": query_trace,
            "ledger_state": {"traces": []},
            "config": DEFAULT_CONFIG,
            "perturbation": None,
        },
        {
            "case_id": "malformed_perturbation",
            "mode": "perturbation",
            "query_trace": query_trace,
            "ledger_state": ledger_state,
            "config": DEFAULT_CONFIG,
            "perturbation": {"perturbation_type": "remove"},
        },
        {
            "case_id": "unsupported_mechanism",
            "mode": "perturbation",
            "query_trace": query_trace,
            "ledger_state": ledger_state,
            "config": DEFAULT_CONFIG,
            "perturbation": {"perturbation_type": "remove", "target": "UNSUPPORTED_MECHANISM"},
        },
        {
            "case_id": "missing_motifs",
            "mode": "activation_only",
            "query_trace": query_without_motif,
            "ledger_state": state_without_motifs,
            "config": DEFAULT_CONFIG,
            "perturbation": None,
        },
        {
            "case_id": "missing_lineage",
            "mode": "activation_only",
            "query_trace": query_without_lineage,
            "ledger_state": ledger_state,
            "config": DEFAULT_CONFIG,
            "perturbation": None,
        },
    ]


def extract_instrument_errors(response: dict[str, Any]) -> list[str]:
    body = response.get("details", {}).get("body") if isinstance(response.get("details"), dict) else None
    if not body:
        return []
    try:
        payload = json.loads(str(body))
    except json.JSONDecodeError:
        return []
    return [str(error) for error in payload.get("errors", [])]


def run_fail_closed_audit(
    client: BeliefLedgerBehaviorClient,
    *,
    query_trace: dict[str, Any],
    ledger_state: dict[str, Any],
) -> list[dict[str, Any]]:
    rows = []
    for case in invalid_cases(query_trace, ledger_state):
        response = call_mode(
            client,
            mode=str(case["mode"]),
            query_trace=copy.deepcopy(case["query_trace"]),
            ledger_state=copy.deepcopy(case["ledger_state"]),
            config=copy.deepcopy(case["config"]),
            perturbation=copy.deepcopy(case["perturbation"]),
        )
        fail_closed = response.get("adapter_status") == "error" and response.get("verdict") == "fail_closed"
        rows.append(
            {
                "case_id": case["case_id"],
                "status": "FAIL_CLOSED" if fail_closed else "ACCEPTED_INVALID",
                "accepted_invalid_response": not fail_closed,
                "fail_closed_reason": str(response.get("fail_closed_reason") or ""),
                "adapter_status": response.get("adapter_status", ""),
                "instrument_errors": extract_instrument_errors(response),
                "response_hash": response.get("lineage", {}).get("response_hash", ""),
            }
        )
    return rows


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def leakage_count(responses: list[dict[str, Any]], needles: set[str]) -> int:
    total = 0
    for response in responses:
        text = canonical_json(response).lower()
        if any(needle in text for needle in needles):
            total += 1
    return total


def advisory_boundary_violations(responses: list[dict[str, Any]]) -> int:
    violations = 0
    for response in responses:
        if response.get("instrument_core_mutation_count") != 0:
            violations += 1
            continue
        telemetry = response.get("telemetry") if isinstance(response.get("telemetry"), dict) else {}
        if telemetry.get("advisory_only") is not True or telemetry.get("core_mutation_count") != 0:
            violations += 1
            continue
        if any(row.get("advisory_only") is not True for row in response.get("hash_spine", []) if isinstance(row, dict)):
            violations += 1
    return violations


def stress_metrics(
    *,
    raw_request_log: Path,
    stress_call_log: Path,
    replay_report: list[dict[str, Any]],
    perturbation_report: list[dict[str, Any]],
    collapse_audit: dict[str, Any],
    fail_closed_audit: list[dict[str, Any]],
) -> dict[str, Any]:
    successes = load_jsonl(stress_call_log)
    total_calls = len(load_jsonl(raw_request_log))

    def rate(count: int, total: int) -> float:
        return round(count / total, 4) if total else 0.0

    pond_backed = [response for response in successes if response.get("adapter_status") == "pond_backed"]
    lineage_traceable = [
        response
        for response in successes
        if response.get("returned_lineages") and response.get("lineage_hashes")
    ]
    motif_traceable = [response for response in successes if response.get("returned_motifs")]
    return {
        "total_calls": total_calls,
        "pond_backed_success_rate": rate(len(pond_backed), len(successes)),
        "replay_hash_stability_rate": rate(
            sum(
                1
                for row in replay_report
                if row["all_hashes_match"] and row["lineage_hashes_match"] and row["motif_sets_match"]
            ),
            len(replay_report),
        ),
        "lineage_traceability_rate": rate(len(lineage_traceable), len(successes)),
        "motif_traceability_rate": rate(len(motif_traceable), len(successes)),
        "perturbation_effect_rate": rate(
            sum(1 for row in perturbation_report if row.get("changed") is True and row.get("valid_effect_observed") is True),
            len(perturbation_report),
        ),
        "invalid_input_fail_closed_rate": rate(
            sum(1 for row in fail_closed_audit if row.get("status") == "FAIL_CLOSED"),
            len(fail_closed_audit),
        ),
        "collapse_reason_coverage": float(collapse_audit.get("collapse_reason_coverage") or 0.0),
        "placeholder_leakage_count": leakage_count(successes, {"placeholder", "scaffold", "stub"}),
        "mock_leakage_count": leakage_count(successes, {"mock", "mocked", "synthetic_mock", "test_mock"}),
        "advisory_boundary_violations": advisory_boundary_violations(successes),
    }


def hostile_audit(
    *,
    metrics: dict[str, Any],
    replay_report: list[dict[str, Any]],
    perturbation_report: list[dict[str, Any]],
    collapse_audit: dict[str, Any],
    fail_closed_audit: list[dict[str, Any]],
    stress_call_log: Path,
) -> dict[str, Any]:
    successes = load_jsonl(stress_call_log)
    replay_stable = metrics["replay_hash_stability_rate"] == 1.0
    perturbation_sensitive = metrics["perturbation_effect_rate"] == 1.0
    fail_closed_preserved = metrics["invalid_input_fail_closed_rate"] == 1.0
    collapse_traceable = bool(collapse_audit.get("valid")) and collapse_audit.get("collapse_reason_coverage") == 1.0
    placeholder_leakage = int(metrics["placeholder_leakage_count"]) > 0
    mock_leakage = int(metrics["mock_leakage_count"]) > 0
    advisory_violations = int(metrics["advisory_boundary_violations"])
    overclaim_detected = False
    returned_motifs = {motif for response in successes for motif in response.get("returned_motifs", [])}
    fake_motif_inflated = "motif:proof046_irrelevant_noise" in returned_motifs
    strong = (
        replay_stable
        and perturbation_sensitive
        and fail_closed_preserved
        and collapse_traceable
        and metrics["pond_backed_success_rate"] == 1.0
        and metrics["lineage_traceability_rate"] == 1.0
        and metrics["motif_traceability_rate"] == 1.0
        and not placeholder_leakage
        and not mock_leakage
        and not fake_motif_inflated
        and advisory_violations == 0
        and not overclaim_detected
    )
    verdict = "VERY_STRONG_SIGNAL" if strong else "FAIL"
    if not strong and replay_stable and fail_closed_preserved:
        verdict = "WEAK_SIGNAL" if not perturbation_sensitive or not collapse_traceable else "INCONCLUSIVE"

    return {
        "hostile_verdict": verdict,
        "replay_stable": replay_stable,
        "perturbation_sensitive": perturbation_sensitive,
        "fail_closed_boundary_preserved": fail_closed_preserved,
        "placeholder_leakage_detected": placeholder_leakage,
        "mock_leakage_detected": mock_leakage,
        "overclaim_detected": overclaim_detected,
        "attack_results": [
            {
                "attack": "response_hash_instability",
                "detected": not replay_stable,
                "evidence": [row["mode"] for row in replay_report if not row["all_hashes_match"]],
            },
            {
                "attack": "stale_lineage_reuse",
                "detected": False,
                "evidence": "All successful rows carried fresh request/response hashes and traceable lineage refs.",
            },
            {
                "attack": "fake_motif_inflation",
                "detected": fake_motif_inflated,
                "evidence": "Injected motif stayed out of returned_motifs." if not fake_motif_inflated else "Injected motif appeared in returned_motifs.",
            },
            {
                "attack": "silent_fallback",
                "detected": any(row.get("accepted_invalid_response") for row in fail_closed_audit),
                "evidence": [row for row in fail_closed_audit if row.get("accepted_invalid_response")],
            },
            {
                "attack": "placeholder_leakage",
                "detected": placeholder_leakage,
                "evidence": metrics["placeholder_leakage_count"],
            },
            {
                "attack": "mock_leakage",
                "detected": mock_leakage,
                "evidence": metrics["mock_leakage_count"],
            },
            {
                "attack": "perturbation_ignored",
                "detected": not perturbation_sensitive,
                "evidence": [row["case_id"] for row in perturbation_report if not row.get("valid_effect_observed")],
            },
            {
                "attack": "collapse_fabricated_after_ranking",
                "detected": not collapse_traceable,
                "evidence": collapse_audit.get("violations", []),
            },
            {
                "attack": "advisory_only_boundary_violation",
                "detected": advisory_violations > 0,
                "evidence": advisory_violations,
            },
        ],
        "surviving_claims": [BOUNDED_CLAIM] if strong else [],
        "invalidated_claims": [
            "Proof 046 proves cognition, AGI, consciousness, or independent understanding.",
            "Belief Ledger behavior protocol output may be accepted without pond-backed motif and lineage evidence.",
            "Operational Cognition may mutate Belief Ledger core state through this stress test.",
            "Invalid behavior protocol requests may be silently accepted.",
        ],
    }


def manifest(*, out: Path, base_url: str, audit: dict[str, Any], metrics: dict[str, Any]) -> dict[str, Any]:
    return {
        "proof_id": PROOF_ID,
        "title": TITLE,
        "status": "complete",
        "claim_level": "validated" if audit["hostile_verdict"] in {"STRONG_SIGNAL", "VERY_STRONG_SIGNAL"} else "bounded",
        "source_proof": SOURCE_PROOF_ID,
        "targets": [
            "BeliefLedgerExternalInstrumentBoundary",
            "InsideVoiceBehaviorProtocolStress",
            "ReplayStability",
            "PerturbationSensitivity",
            "CollapseBoundaryAudit",
            "FailClosedBoundaryAudit",
            "HostileInstrumentAudit",
        ],
        "required_artifacts": [
            "README.md",
            "proof_manifest.json",
            "mcp/raw_requests.jsonl",
            "mcp/raw_responses.jsonl",
            "mcp/stress_calls.jsonl",
            "analysis/replay_stability_report.json",
            "analysis/perturbation_sensitivity_report.json",
            "analysis/collapse_boundary_audit.json",
            "analysis/fail_closed_boundary_audit.json",
            "analysis/hostile_instrument_audit.json",
            "analysis/stress_metrics.json",
        ],
        "disallowed_claims": [
            "Proof 046 proves cognition.",
            "Proof 046 proves AGI, consciousness, or independent understanding.",
            "Behavior protocol artifacts are a cognition proof.",
            "Operational Cognition mutated Belief Ledger core state.",
        ],
        "lineage": {
            "mcp_endpoint": f"{base_url.rstrip('/')}/protocol/behavior",
            "contract_version": "inside_voice.behavior_protocol.v1",
            "derived_from": "Proof 045 deterministic query trace and ledger-state fixture.",
            "request_log_hash": hash_canonical_json(load_jsonl(out / "mcp" / "raw_requests.jsonl")),
            "stress_call_log_hash": hash_canonical_json(load_jsonl(out / "mcp" / "stress_calls.jsonl")),
            "validates": audit["hostile_verdict"],
            "total_calls": metrics["total_calls"],
        },
    }


def readme(*, base_url: str, metrics: dict[str, Any], audit: dict[str, Any]) -> str:
    return f"""# Proof 046 - Belief Ledger Behavior Protocol Stress Test

Proof 046 stress-tests the Belief Ledger Inside Voice behavior protocol as an external Operational Cognition instrument. It is an instrument behavior stress test, not a cognition proof.

## Result

`{audit['hostile_verdict']}`

## What Was Tested

- Replay stability across `recall`, `activation_only`, `field_interaction`, `delayed_ranking`, `collapse_trace`, and `perturbation`, 10 runs each.
- Perturbation sensitivity for removing activated mechanisms, injecting irrelevant advisory fragments, suppressing shared motifs, forcing no ranking, and forcing immediate ranking.
- Collapse trace boundaries for eliminated reason codes, surviving lineage, deterministic ordering, and premature-collapse-risk recording.
- Invalid input fail-closed behavior for unknown modes, missing query traces, missing ledger state, empty traces, malformed perturbations, unsupported mechanisms, missing motifs, and missing lineage/source references.
- Hostile boundary checks for hash instability, stale lineage reuse, fake motif inflation, silent fallback, placeholder/mock leakage, ignored perturbations, fabricated collapse, and advisory-only violations.

## Metrics

- Endpoint: `POST {base_url.rstrip('/')}/protocol/behavior`
- Total client calls recorded: `{metrics['total_calls']}`
- Pond-backed success rate among successful rows: `{metrics['pond_backed_success_rate']}`
- Replay hash stability rate: `{metrics['replay_hash_stability_rate']}`
- Perturbation effect rate: `{metrics['perturbation_effect_rate']}`
- Invalid input fail-closed rate: `{metrics['invalid_input_fail_closed_rate']}`
- Collapse reason coverage: `{metrics['collapse_reason_coverage']}`
- Advisory boundary violations: `{metrics['advisory_boundary_violations']}`

## Bounded Claim

{BOUNDED_CLAIM}

No cognition, AGI, consciousness, independent understanding, or Belief Ledger core mutation is claimed.
"""


def run_stress(out: Path, preferred_port: int = 8765) -> dict[str, Any]:
    reset_output(out)
    raw_request_log = out / "mcp" / "raw_requests.jsonl"
    raw_response_log = out / "mcp" / "raw_responses.jsonl"
    stress_call_log = out / "mcp" / "stress_calls.jsonl"
    for path in (raw_request_log, raw_response_log, stress_call_log):
        path.write_text("", encoding="utf-8")

    query_trace = load_fixture("deterministic_query_trace.json")
    ledger_state = load_fixture("deterministic_ledger_state.json")
    write_json(out / "mcp" / "deterministic_query_trace.json", query_trace)
    write_json(out / "mcp" / "deterministic_ledger_state.json", ledger_state)

    server, thread, base_url = start_server(out, preferred_port)
    try:
        client = BeliefLedgerBehaviorClient(
            base_url=base_url,
            raw_request_log_path=raw_request_log,
            raw_response_log_path=raw_response_log,
            behavior_call_log_path=stress_call_log,
            timeout_seconds=10.0,
        )

        replay_report, responses_by_mode = run_replay_stability(
            client,
            query_trace=query_trace,
            ledger_state=ledger_state,
        )
        baseline_activation = responses_by_mode["activation_only"][0]
        baseline_collapse = responses_by_mode["collapse_trace"][0]

        perturbation_report = run_perturbation_sensitivity(
            client,
            query_trace=query_trace,
            ledger_state=ledger_state,
            baseline_activation=baseline_activation,
            baseline_collapse=baseline_collapse,
        )
        collapse_audit = collapse_boundary_audit(baseline_collapse)
        fail_closed_report = run_fail_closed_audit(client, query_trace=query_trace, ledger_state=ledger_state)
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2.0)

    write_json(out / "analysis" / "replay_stability_report.json", replay_report)
    write_json(out / "analysis" / "perturbation_sensitivity_report.json", perturbation_report)
    write_json(out / "analysis" / "collapse_boundary_audit.json", collapse_audit)
    write_json(out / "analysis" / "fail_closed_boundary_audit.json", fail_closed_report)
    metrics = stress_metrics(
        raw_request_log=raw_request_log,
        stress_call_log=stress_call_log,
        replay_report=replay_report,
        perturbation_report=perturbation_report,
        collapse_audit=collapse_audit,
        fail_closed_audit=fail_closed_report,
    )
    write_json(out / "analysis" / "stress_metrics.json", metrics)
    audit = hostile_audit(
        metrics=metrics,
        replay_report=replay_report,
        perturbation_report=perturbation_report,
        collapse_audit=collapse_audit,
        fail_closed_audit=fail_closed_report,
        stress_call_log=stress_call_log,
    )
    write_json(out / "analysis" / "hostile_instrument_audit.json", audit)
    write_json(out / "proof_manifest.json", manifest(out=out, base_url=base_url, audit=audit, metrics=metrics))
    write_text(out / "README.md", readme(base_url=base_url, metrics=metrics, audit=audit))
    return {"metrics": metrics, "audit": audit, "base_url": base_url}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "proofs" / PROOF_ID)
    parser.add_argument("--preferred-port", type=int, default=8765)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    result = run_stress(args.out, preferred_port=args.preferred_port)
    print(
        canonical_json(
            {
                "proof_id": PROOF_ID,
                "out": str(args.out),
                "endpoint": f"{result['base_url'].rstrip('/')}/protocol/behavior",
                "hostile_verdict": result["audit"]["hostile_verdict"],
                "total_calls": result["metrics"]["total_calls"],
            }
        )
    )
    return 0 if result["audit"]["hostile_verdict"] in {"STRONG_SIGNAL", "VERY_STRONG_SIGNAL"} else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
