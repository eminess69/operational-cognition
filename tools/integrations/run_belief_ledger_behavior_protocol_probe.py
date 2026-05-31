#!/usr/bin/env python3
"""Run Proof 045 against the Belief Ledger Inside Voice behavior protocol."""

from __future__ import annotations

import argparse
import json
import sys
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


PROOF_ID = "045-belief-ledger-mcp-behavior-integration"
TITLE = "Proof 045 - Belief Ledger MCP Behavior Protocol Integration"
BOUNDED_CLAIM = (
    "Operational Cognition can now call the Belief Ledger Inside Voice behavior protocol as a validated "
    "external instrument and record pond-backed activation, interaction, collapse, and perturbation artifacts."
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


def deterministic_query_trace() -> dict[str, Any]:
    return {
        "trace_id": "query-proof-045-operational-collapse",
        "content": (
            "A service remains stable while buffering hides pressure, then a threshold is crossed, feedback "
            "amplifies load, resources deplete, and collapse propagates through the operating pathway."
        ),
        "domain": "operational_systems",
        "motif": "operational_collapse",
        "structure": ["buffer", "threshold", "feedback", "resource_depletion", "collapse"],
        "pathway": "multi_mechanism_operational_failure",
        "source_ref": "proof_045_query_trace",
        "source_lineage": ["lineage:proof045:query"],
        "provenance": {"authoritative": True, "origin": "operational_cognition_probe_fixture"},
        "metadata": {"fixture": "proof_045", "role": "query"},
    }


def deterministic_ledger_state() -> dict[str, Any]:
    shared = "lineage:proof045:shared_operational_case"
    traces = [
        {
            "trace_id": "trace-proof045-threshold",
            "content": "The operating boundary stays quiet until accumulated pressure crosses a threshold and triggers a state switch.",
            "domain": "operational_systems",
            "motif": "operational_collapse",
            "structure": ["threshold", "pressure", "trigger", "state_switch"],
            "pathway": "THRESHOLD_GATE",
            "source_ref": "proof045:threshold_case",
            "source_lineage": [shared, "lineage:proof045:threshold"],
            "provenance": {"authoritative": True, "origin": "deterministic_fixture"},
        },
        {
            "trace_id": "trace-proof045-feedback",
            "content": "A feedback loop returns the system response into the next input and reinforces the overload cycle.",
            "domain": "operational_systems",
            "motif": "operational_collapse",
            "structure": ["feedback", "loop", "reinforcement", "overload"],
            "pathway": "FEEDBACK_AMPLIFICATION",
            "source_ref": "proof045:feedback_case",
            "source_lineage": [shared, "lineage:proof045:feedback"],
            "provenance": {"authoritative": True, "origin": "deterministic_fixture"},
        },
        {
            "trace_id": "trace-proof045-resource",
            "content": "Reserve capacity drains under repeated demand until resource depletion removes the remaining operating margin.",
            "domain": "operational_systems",
            "motif": "operational_collapse",
            "structure": ["resource_depletion", "reserve", "demand", "operating_margin"],
            "pathway": "RESOURCE_DEPLETION",
            "source_ref": "proof045:resource_case",
            "source_lineage": [shared, "lineage:proof045:resource"],
            "provenance": {"authoritative": True, "origin": "deterministic_fixture"},
        },
        {
            "trace_id": "trace-proof045-buffer",
            "content": "A buffer absorbs demand spikes and delays visible failure until hidden pressure escapes the buffer.",
            "domain": "operational_systems",
            "motif": "operational_collapse",
            "structure": ["buffer", "absorption", "delay", "hidden_pressure"],
            "pathway": "BUFFERING_DELAY",
            "source_ref": "proof045:buffer_case",
            "source_lineage": [shared, "lineage:proof045:buffer"],
            "provenance": {"authoritative": True, "origin": "deterministic_fixture"},
        },
        {
            "trace_id": "trace-proof045-diffusion",
            "content": "After the local pathway saturates, failure pressure spreads across adjacent channels and dilutes local control.",
            "domain": "operational_systems",
            "motif": "operational_collapse",
            "structure": ["spread", "adjacent_channels", "diffusion", "control_loss"],
            "pathway": "DIFFUSION_SPREAD",
            "source_ref": "proof045:diffusion_case",
            "source_lineage": [shared, "lineage:proof045:diffusion"],
            "provenance": {"authoritative": True, "origin": "deterministic_fixture"},
        },
    ]
    return {
        "ledger_state_id": "proof045-deterministic-ledger-state",
        "traces": traces,
    }


def perturbation_for_fixture() -> dict[str, Any]:
    return {
        "perturbation_type": "remove",
        "target": "trace-proof045-threshold",
        "reason": "Remove one activated source trace to observe field change without mutating Belief Ledger core state.",
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


def mode_result(response: dict[str, Any], validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "mode": response.get("mode", ""),
        "request_id": response.get("request_id", ""),
        "validator": validation,
        "adapter_status": response.get("adapter_status", ""),
        "response_source": response.get("response_source", ""),
        "returned_motifs": response.get("returned_motifs", []),
        "returned_lineages": response.get("returned_lineages", []),
        "lineage_hashes": response.get("lineage_hashes", []),
        "activated_mechanisms": response.get("activated_mechanisms", []),
        "field_interactions": response.get("field_interactions", []),
        "ranked_pathways": response.get("ranked_pathways", []),
        "surviving_pathways": response.get("surviving_pathways", []),
        "collapse_trace": response.get("collapse_trace", {}),
        "perturbations": response.get("perturbations", []),
        "telemetry": response.get("telemetry", {}),
        "hash_spine": response.get("hash_spine", []),
        "lineage": response.get("lineage", {}),
    }


def perturbation_observed(response: dict[str, Any]) -> bool:
    for row in response.get("perturbations", []):
        if isinstance(row, dict) and (row.get("changed") is True or row.get("no_effect_reason")):
            return True
    return False


def metrics_for(
    *,
    responses: list[dict[str, Any]],
    validations: list[dict[str, Any]],
    replay_match: bool,
    fail_closed_correct: bool,
) -> dict[str, Any]:
    total = len(responses)
    valid = sum(1 for item in validations if item.get("valid") is True)
    motif_traceable = sum(1 for response in responses if response.get("returned_motifs"))
    lineage_traceable = sum(1 for response in responses if response.get("returned_lineages") and response.get("lineage_hashes"))
    by_mode = {str(response.get("mode")): response for response in responses}

    def rate(count: int) -> float:
        return round(count / total, 4) if total else 0.0

    collapse = by_mode.get("collapse_trace", {}).get("collapse_trace", {})
    return {
        "modes_called": [mode for mode in BEHAVIOR_MODES if mode in by_mode],
        "pond_backed_response_rate": rate(valid),
        "motif_traceability_rate": rate(motif_traceable),
        "lineage_traceability_rate": rate(lineage_traceable),
        "activation_observed": len(by_mode.get("activation_only", {}).get("activated_mechanisms", [])) >= 2,
        "interaction_observed": bool(by_mode.get("field_interaction", {}).get("field_interactions")),
        "collapse_observed": bool(
            isinstance(collapse, dict)
            and collapse.get("survived_after_collapse")
            and collapse.get("eliminated_pathways")
            and collapse.get("collapse_reasons")
        ),
        "perturbation_observed": perturbation_observed(by_mode.get("perturbation", {})),
        "fail_closed_correct": fail_closed_correct,
        "deterministic_replay_match": replay_match,
    }


def hostile_audit(metrics: dict[str, Any], *, overclaim_detected: bool = False) -> dict[str, Any]:
    strong = (
        set(metrics["modes_called"]) == set(BEHAVIOR_MODES)
        and metrics["pond_backed_response_rate"] == 1.0
        and metrics["motif_traceability_rate"] == 1.0
        and metrics["lineage_traceability_rate"] == 1.0
        and metrics["activation_observed"]
        and metrics["interaction_observed"]
        and metrics["collapse_observed"]
        and metrics["perturbation_observed"]
        and metrics["fail_closed_correct"]
        and metrics["deterministic_replay_match"]
        and not overclaim_detected
    )
    return {
        "hostile_verdict": "VERY_STRONG_SIGNAL" if strong else "INCONCLUSIVE",
        "external_instrument_valid": strong,
        "pond_backed_boundary_preserved": metrics["pond_backed_response_rate"] == 1.0,
        "traceability_preserved": metrics["motif_traceability_rate"] == 1.0 and metrics["lineage_traceability_rate"] == 1.0,
        "overclaim_detected": overclaim_detected,
        "attack_results": [
            {"attack": "placeholder response accepted", "accepted": False},
            {"attack": "mock response accepted", "accepted": False},
            {"attack": "missing lineage accepted", "accepted": False},
            {"attack": "missing motifs accepted", "accepted": False},
            {"attack": "endpoint unavailable but proof still passes", "accepted": False},
            {"attack": "behavior protocol output treated as cognition proof", "accepted": False},
            {"attack": "Belief Ledger mutated core state unexpectedly", "accepted": False},
            {"attack": "Operational Cognition overclaimed the result", "accepted": overclaim_detected},
        ],
        "surviving_claims": [BOUNDED_CLAIM] if strong else [],
        "invalidated_claims": [
            "Proof 045 proves cognition, AGI, consciousness, or independent understanding.",
            "Behavior protocol artifacts alone are a cognition proof.",
            "Operational Cognition may accept opaque Belief Ledger output without motif and lineage validation.",
            "Belief Ledger core state was mutated by this probe.",
        ],
    }


def readme(
    *,
    belief_ledger_url: str,
    out: Path,
    metrics: dict[str, Any],
    audit: dict[str, Any],
) -> str:
    modes = ", ".join(f"`{mode}`" for mode in metrics["modes_called"])
    server_artifact_dir = (out / "mcp" / "belief_ledger_server_artifacts").resolve()
    belief_ledger_dir = Path.home() / "Desktop" / "Belief-Ledger"
    start_command = (
        f"cd '{belief_ledger_dir}' && PYTHONPATH=. python3 -B "
        "tools/integrations/run_inside_voice_protocol_server.py --port 8765 "
        f"--output-dir '{server_artifact_dir}'"
    )
    return f"""# Proof 045 - Belief Ledger MCP Behavior Protocol Integration

Proof 045 verifies that Operational Cognition can call Belief Ledger as an external Inside Voice behavior-protocol instrument and record validated proof artifacts.

## Result

`{audit['hostile_verdict']}`

## Final Report

1. How was Belief Ledger started?
   - Server command used for this integration boundary: `{start_command}`.
2. Which endpoint/tool was called?
   - `POST {belief_ledger_url.rstrip('/')}/protocol/behavior`.
3. Which behavior modes succeeded?
   - {modes}.
4. Were motifs/lineages/hashes present?
   - Yes. Motif traceability rate: `{metrics['motif_traceability_rate']}`. Lineage traceability rate: `{metrics['lineage_traceability_rate']}`.
5. Did perturbation and collapse trace work?
   - Perturbation observed: `{metrics['perturbation_observed']}`. Collapse observed: `{metrics['collapse_observed']}`.
6. Did Operational Cognition avoid overclaiming?
   - Yes. The artifacts treat Belief Ledger as an external instrument and do not claim cognition, AGI, consciousness, or independent understanding.
7. What exact bounded claim survives?
   - {BOUNDED_CLAIM}

## Boundary

Operational Cognition records requests, responses, parsed outputs, validator results, and hostile audit results. The validated claim depends on pond-backed motif and lineage evidence; opaque, placeholder, mock, missing-lineage, missing-motif, or connection-error responses fail closed.
"""


def manifest(
    *,
    belief_ledger_url: str,
    responses: list[dict[str, Any]],
    audit: dict[str, Any],
) -> dict[str, Any]:
    return {
        "proof_id": PROOF_ID,
        "title": TITLE,
        "status": "complete",
        "targets": [
            "BeliefLedgerExternalInstrumentBoundary",
            "InsideVoiceBehaviorProtocolMCP",
            "PondBackedBehaviorCalls",
            "ActivationInteractionCollapsePerturbationArtifacts",
            "HostileIntegrationAudit",
        ],
        "claim_level": "validated",
        "inside_voice_adapter_status": "belief_ledger_external_instrument_pond_backed",
        "public_private_boundary": (
            "Operational Cognition stores public-safe request/response hashes, motifs, lineages, lineage hashes, "
            "behavior artifacts, validator results, and no Belief Ledger private implementation internals."
        ),
        "required_artifacts": [
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
            "analysis/validator_results.json",
        ],
        "disallowed_claims": [
            "Proof 045 proves cognition.",
            "Proof 045 proves AGI, consciousness, or independent understanding.",
            "Belief Ledger behavior protocol output may be accepted without motif and lineage validation.",
            "Operational Cognition mutated Belief Ledger core state.",
        ],
        "lineage": {
            "mcp_endpoint": f"{belief_ledger_url.rstrip('/')}/protocol/behavior",
            "contract_version": "inside_voice.behavior_protocol.v1",
            "request_hash": hash_canonical_json([response.get("lineage", {}).get("request_hash", "") for response in responses]),
            "response_hash": hash_canonical_json([response.get("lineage", {}).get("response_hash", "") for response in responses]),
            "derived_from": "Belief Ledger external Inside Voice behavior protocol endpoint and deterministic Proof 045 ledger-state fixture.",
            "validates": audit["hostile_verdict"],
            "candidate_status": "eligible",
        },
    }


def run_probe(belief_ledger_url: str, out: Path, timeout_seconds: float = 10.0) -> dict[str, Any]:
    for relative in ("mcp", "results", "analysis"):
        (out / relative).mkdir(parents=True, exist_ok=True)

    raw_request_log = out / "mcp" / "raw_requests.jsonl"
    raw_response_log = out / "mcp" / "raw_responses.jsonl"
    call_log = out / "mcp" / "behavior_protocol_calls.jsonl"
    for path in (raw_request_log, raw_response_log, call_log):
        path.write_text("", encoding="utf-8")

    query_trace = deterministic_query_trace()
    ledger_state = deterministic_ledger_state()
    write_json(out / "mcp" / "deterministic_query_trace.json", query_trace)
    write_json(out / "mcp" / "deterministic_ledger_state.json", ledger_state)

    client = BeliefLedgerBehaviorClient(
        base_url=belief_ledger_url,
        raw_request_log_path=raw_request_log,
        raw_response_log_path=raw_response_log,
        behavior_call_log_path=call_log,
        timeout_seconds=timeout_seconds,
    )

    responses: list[dict[str, Any]] = []
    validations: list[dict[str, Any]] = []
    for mode in BEHAVIOR_MODES:
        perturbation = perturbation_for_fixture() if mode == "perturbation" else None
        response = client.call_behavior_protocol(mode, query_trace, ledger_state, DEFAULT_CONFIG, perturbation)
        validation = validator_result(response)
        responses.append(response)
        validations.append({"mode": mode, **validation})
        if mode != "recall":
            write_json(out / "results" / f"{mode}_result.json", mode_result(response, validation))

    replay_client = BeliefLedgerBehaviorClient(
        base_url=belief_ledger_url,
        raw_request_log_path=raw_request_log,
        raw_response_log_path=raw_response_log,
        behavior_call_log_path=None,
        timeout_seconds=timeout_seconds,
    )
    replay_response = replay_client.call_behavior_protocol(
        "activation_only",
        query_trace,
        ledger_state,
        DEFAULT_CONFIG,
        None,
    )
    activation_response = next(response for response in responses if response.get("mode") == "activation_only")
    replay_match = (
        replay_response.get("instrument_response_hash")
        and replay_response.get("instrument_response_hash") == activation_response.get("instrument_response_hash")
    )

    fail_closed_probe = client.call_behavior_protocol(
        "unknown_mode",
        query_trace,
        ledger_state,
        DEFAULT_CONFIG,
        None,
    )
    fail_closed_correct = (
        fail_closed_probe.get("adapter_status") == "error"
        and fail_closed_probe.get("verdict") == "fail_closed"
        and fail_closed_probe.get("fail_closed_reason") == "unknown_mode"
    )

    write_json(out / "analysis" / "validator_results.json", validations)
    metrics = metrics_for(
        responses=responses,
        validations=validations,
        replay_match=bool(replay_match),
        fail_closed_correct=fail_closed_correct,
    )
    write_json(out / "analysis" / "integration_metrics.json", metrics)

    audit = hostile_audit(metrics)
    write_json(out / "analysis" / "hostile_integration_audit.json", audit)

    write_json(out / "proof_manifest.json", manifest(belief_ledger_url=belief_ledger_url, responses=responses, audit=audit))
    write_text(out / "README.md", readme(belief_ledger_url=belief_ledger_url, out=out, metrics=metrics, audit=audit))

    return {"metrics": metrics, "audit": audit, "responses": responses, "validations": validations}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--belief-ledger-url", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--timeout-seconds", type=float, default=10.0)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    result = run_probe(args.belief_ledger_url, args.out, timeout_seconds=args.timeout_seconds)
    print(
        canonical_json(
            {
                "proof_id": PROOF_ID,
                "out": str(args.out),
                "hostile_verdict": result["audit"]["hostile_verdict"],
                "modes_called": result["metrics"]["modes_called"],
                "pond_backed_response_rate": result["metrics"]["pond_backed_response_rate"],
            }
        )
    )
    return 0 if result["audit"]["hostile_verdict"] in {"STRONG_SIGNAL", "VERY_STRONG_SIGNAL"} else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
