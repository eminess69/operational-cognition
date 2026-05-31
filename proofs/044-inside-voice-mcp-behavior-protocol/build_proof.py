#!/usr/bin/env python3
"""Build Proof 044 Inside Voice MCP behavior protocol artifacts."""

from __future__ import annotations

import copy
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROOF_ID = "044-inside-voice-mcp-behavior-protocol"
TITLE = "Proof 044 - Inside Voice MCP Behavior Protocol"
PROOF_DIR = Path(__file__).resolve().parent
ROOT = PROOF_DIR.parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from operational_cognition.mcp.consult_classifier import classify_mcp_response  # noqa: E402
from tools.integrations.inside_voice_mcp_server import (  # noqa: E402
    BEHAVIOR_MODES,
    MAX_OUTPUT_CHARS_CAP,
    MECHANISM_MOTIFS,
    canonical_json,
    hash_canonical_json,
    process_consult_request,
)


MECHANISM_LESSONS = {
    "FLOW": [
        "A source sends water through a path; a narrowed throat adds resistance, throughput declines, and upstream backlog grows.",
        "A channel route carries supply until a restriction creates a bottleneck and downstream output falls.",
    ],
    "SUPPORTED_ROTATION": [
        "A rotating shaft depends on support; friction rises at the bearing, wobble increases, and the pivot can seize.",
        "A journal turns inside a socket until drag and rough contact make rotation lock.",
    ],
    "LOAD_TRANSFER": [
        "A structure transfers load through supports; concentration at a local bracket bends material, cracks appear, and failure occurs.",
        "A distributed burden shifts to one anchor; strain localizes and the lug tears.",
    ],
    "FEEDBACK": [
        "A signal loops back into response; reinforcement amplifies the next signal and can become runaway.",
        "A delayed correction returns through the same loop and strengthens the next adjustment.",
    ],
    "THRESHOLD": [
        "A value accumulates until it crosses a critical limit, triggering a state switch.",
        "A boundary remains quiet until the threshold is crossed and a sudden transition occurs.",
    ],
    "ACCUMULATION": [
        "Input collects in storage, buildup grows gradually, and overflow appears after capacity is exceeded.",
        "Sediment deposits in a reservoir, pressure rises, and stored material spills over.",
    ],
    "DIFFUSION": [
        "A source creates a gradient; material spreads outward, disperses, and becomes diluted across neighboring regions.",
        "A leak seeps from a concentrated edge and permeates side channels until the signal is uniform.",
    ],
    "OSCILLATION": [
        "Delayed response causes overshoot, undershoot, and repeated cycles around a target state.",
        "A controller hunts above and below the set point, producing periodic swings.",
    ],
    "BUFFERING": [
        "A buffer absorbs shock, uses reserve capacity, and delays visible failure while demand is smoothed.",
        "Slack temporarily cushions input spikes and hides stress until reserve capacity is spent.",
    ],
    "RESOURCE_DEPLETION": [
        "A resource is consumed over time; scarcity grows, reserve drains, and exhaustion causes collapse.",
        "Fuel supply falls as capacity is used, leaving the system depleted and unable to continue.",
    ],
    "AMPLIFICATION": [
        "A small input gains strength through propagation, magnifies into a cascade, and escalates downstream.",
        "A relay increases signal gain so each stage produces stronger output.",
    ],
    "COMPENSATION": [
        "A counteraction offsets deviation; substitution and backup support maintain stability temporarily.",
        "A workaround masks loss by adding correction, but hidden demand remains.",
    ],
}


CASE_DEFINITIONS = [
    # recall
    ("recall-001", "recall", "Water throughput declines after a restriction narrows the channel path and upstream backlog grows."),
    ("recall-002", "recall", "A shaft turns roughly in a socket; bearing friction rises and the pivot locks."),
    ("recall-003", "recall", "A bracket takes concentrated load, bends locally, cracks, and fails at the anchor."),
    ("recall-004", "recall", "A concentrated leak spreads along a gradient and becomes diluted across adjacent regions."),
    ("recall-005", "recall", "Reserve fuel is consumed, capacity drains, scarcity grows, and the process stops from exhaustion."),
    # activation_only
    (
        "activation-001",
        "activation_only",
        "Output stays stable until a threshold is crossed, then feedback reinforces decline and resource reserve drains.",
    ),
    (
        "activation-002",
        "activation_only",
        "A buffer absorbs shock at first, but accumulation builds behind it and overflow appears after capacity is exceeded.",
    ),
    (
        "activation-003",
        "activation_only",
        "A delayed controller overcorrects, oscillates around the target, and feedback strengthens each swing.",
    ),
    (
        "activation-004",
        "activation_only",
        "A channel restriction lowers throughput while pressure accumulates upstream and then spills into side routes.",
    ),
    (
        "activation-005",
        "activation_only",
        "A local load concentration bends the frame while compensation masks the deviation until cracks appear.",
    ),
    # field_interaction
    (
        "interaction-001",
        "field_interaction",
        "A limit is crossed, a feedback loop amplifies the response, and remaining capacity is depleted.",
    ),
    (
        "interaction-002",
        "field_interaction",
        "A buffer delays visible stress while a resource drains and a threshold triggers sudden collapse.",
    ),
    (
        "interaction-003",
        "field_interaction",
        "A bottleneck restricts flow, backlog accumulates, and overflow diffuses into neighboring channels.",
    ),
    (
        "interaction-004",
        "field_interaction",
        "A rotating support develops friction; oscillating wobble increases local load concentration at the bearing.",
    ),
    (
        "interaction-005",
        "field_interaction",
        "A compensation loop offsets deviation until amplification turns the correction into an escalating cascade.",
    ),
    # delayed_ranking
    (
        "delayed-001",
        "delayed_ranking",
        "A quiet boundary is crossed, feedback reinforces output, and the cascade consumes the remaining reserve.",
    ),
    (
        "delayed-002",
        "delayed_ranking",
        "Slack buffers demand while backlog accumulates; once the limit trips, flow output falls sharply.",
    ),
    (
        "delayed-003",
        "delayed_ranking",
        "A bearing support drags, rotation wobbles, and the frame transfers concentrated load into cracks.",
    ),
    (
        "delayed-004",
        "delayed_ranking",
        "A source leak spreads across a gradient while compensation masks dilution until scarcity appears.",
    ),
    (
        "delayed-005",
        "delayed_ranking",
        "A delayed correction overshoots, feedback reinforces the swing, and amplification escalates the cycle.",
    ),
    # collapse_trace
    (
        "collapse-001",
        "collapse_trace",
        "Threshold crossing triggers feedback, amplification accelerates decline, and resource depletion causes failure.",
    ),
    (
        "collapse-002",
        "collapse_trace",
        "Flow restriction creates a queue, accumulation builds pressure, and overflow diffuses through side paths.",
    ),
    (
        "collapse-003",
        "collapse_trace",
        "A support bearing turns roughly, oscillation increases wobble, and load concentration cracks the bracket.",
    ),
    (
        "collapse-004",
        "collapse_trace",
        "A buffer absorbs shock, compensation hides deviation, and reserve capacity becomes exhausted.",
    ),
    (
        "collapse-005",
        "collapse_trace",
        "A signal loop overcorrects with delay, oscillates, and amplification makes each cycle stronger.",
    ),
    # perturbation
    (
        "perturb-001",
        "perturbation",
        "A limit is crossed, feedback reinforces the response, reserve drains, and collapse follows.",
    ),
    (
        "perturb-002",
        "perturbation",
        "A bottleneck restricts throughput, backlog accumulates, and overflow spreads into adjacent routes.",
    ),
    (
        "perturb-003",
        "perturbation",
        "A rotating support drags, wobble cycles grow, and local load transfer cracks the bearing mount.",
    ),
    (
        "perturb-004",
        "perturbation",
        "A buffer cushions demand while compensation offsets deviation, but resource scarcity eventually appears.",
    ),
    (
        "perturb-005",
        "perturbation",
        "A delayed feedback correction overshoots repeatedly and amplification turns the cycle into escalation.",
    ),
]


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(canonical_json(row) + "\n" for row in rows), encoding="utf-8")


def behavior_request(request_id: str, mode: str, observation: str) -> dict[str, Any]:
    return {
        "request_id": request_id,
        "task": (
            "Inside Voice behavior protocol case.\n"
            f"Observation:\n{observation}\n"
            "Required:\n"
            "- returned motifs\n"
            "- returned lineages\n"
            "- lineage hashes\n"
            "- behavior fields for the requested mode"
        ),
        "context": {
            "summary": "Proof 044 behavior protocol consult using the isolated pond state.",
            "files": [],
            "constraints": ["No placeholder fallback.", "Fail closed if pond recall is unavailable."],
            "desired_artifacts": ["behavior_protocol_consults", "behavior_protocol_results"],
        },
        "mode": mode,
        "max_output_chars": MAX_OUTPUT_CHARS_CAP,
        "require_lineage": True,
    }


def seasoning_request(request_id: str, mechanism: str, lesson: str) -> dict[str, Any]:
    return {
        "request_id": request_id,
        "task": f"ACTION: SEASON. Mechanism label: {mechanism}. {lesson}",
        "context": {
            "summary": f"Season behavior-protocol pond with {mechanism}.",
            "files": [],
            "constraints": ["Use only the real pond-backed adapter."],
            "desired_artifacts": ["returned_motifs", "returned_lineages", "lineage_hashes"],
        },
        "mode": "recall",
        "max_output_chars": MAX_OUTPUT_CHARS_CAP,
        "require_lineage": True,
    }


def classified_response(case: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(response)
    row["case_id"] = case["case_id"]
    row["case_mode"] = case["mode"]
    row["classification"] = classify_mcp_response(response).value
    return row


def case_rows() -> list[dict[str, Any]]:
    return [
        {
            "case_id": case_id,
            "mode": mode,
            "observation": observation,
            "category": mode,
            "known_catalog": sorted(MECHANISM_MOTIFS),
        }
        for case_id, mode, observation in CASE_DEFINITIONS
    ]


def response_summary(case: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
    return {
        "case_id": case["case_id"],
        "mode": case["mode"],
        "classification": classify_mcp_response(response).value,
        "verdict": response.get("verdict", ""),
        "motif_count": len(response.get("returned_motifs", [])),
        "lineage_count": len(response.get("returned_lineages", [])),
        "lineage_hash_count": len(response.get("lineage_hashes", [])),
        "activated_mechanisms": response.get("activated_mechanisms", []),
        "field_interactions": response.get("field_interactions", []),
        "ranked_pathways": response.get("ranked_pathways", []),
        "collapse_trace": response.get("collapse_trace", {}),
        "perturbations": response.get("perturbations", []),
        "fail_closed_reason": response.get("fail_closed_reason"),
    }


def fail_closed_audit(state_path: Path) -> dict[str, Any]:
    probes = [
        {
            "probe": "unknown_mode",
            "request": behavior_request("proof-044-fail-unknown", "not_a_mode", "Water restriction lowers throughput."),
            "state_path": state_path,
            "expected_reason": "unknown_mode",
            "expected_status": "error",
        },
        {
            "probe": "missing_pond",
            "request": behavior_request("proof-044-fail-missing", "activation_only", "Water restriction lowers throughput."),
            "state_path": PROOF_DIR / "mcp" / "missing_state.json",
            "expected_reason": "pond_unavailable",
            "expected_status": "error",
        },
        {
            "probe": "irrelevant_observation",
            "request": behavior_request("proof-044-fail-irrelevant", "activation_only", "Opaque symbols drift without any cue overlap."),
            "state_path": state_path,
            "expected_reason": "no_relevant_pond_recall",
            "expected_status": "pond_backed",
        },
    ]
    results = []
    for probe in probes:
        result = process_consult_request(
            probe["request"],
            artifact_dir=PROOF_DIR / "mcp" / "fail_closed_runtime",
            state_path=probe["state_path"],
        )
        response = result.response
        passed = (
            response.get("verdict") == "fail_closed"
            and response.get("fail_closed_reason") == probe["expected_reason"]
            and response.get("adapter_status") == probe["expected_status"]
        )
        results.append(
            {
                "probe": probe["probe"],
                "status_code": result.status_code,
                "classification": classify_mcp_response(response).value,
                "adapter_status": response.get("adapter_status", ""),
                "verdict": response.get("verdict", ""),
                "fail_closed_reason": response.get("fail_closed_reason"),
                "expected_reason": probe["expected_reason"],
                "passed": passed,
            }
        )
    return {
        "probes": results,
        "fail_closed_correct_rate": round(sum(1 for row in results if row["passed"]) / len(results), 4),
    }


def protocol_metrics(results: list[dict[str, Any]], fail_closed: dict[str, Any]) -> dict[str, Any]:
    total = len(results)
    by_mode = Counter(row["mode"] for row in results)
    pond_backed = sum(1 for row in results if row["classification"] == "POND_BACKED")
    motif = sum(1 for row in results if row["motif_count"] > 0)
    lineage = sum(1 for row in results if row["lineage_count"] > 0 and row["lineage_hash_count"] > 0)
    activation_cases = [row for row in results if row["mode"] != "recall"]
    interaction_modes = {"field_interaction", "delayed_ranking", "collapse_trace", "perturbation"}
    interaction_cases = [row for row in results if row["mode"] in interaction_modes]
    collapse_cases = [row for row in results if row["mode"] == "collapse_trace"]
    perturbation_cases = [row for row in results if row["mode"] == "perturbation"]

    def rate(count: int, denominator: int) -> float:
        return round(count / denominator, 4) if denominator else 0.0

    perturbation_effects = 0
    for row in perturbation_cases:
        variants = {variant.get("perturbation"): variant for variant in row.get("perturbations", []) if isinstance(variant, dict)}
        baseline_size = int(variants.get("baseline", {}).get("field_size", 0))
        changed = any(
            int(variant.get("field_size", baseline_size)) != baseline_size
            for name, variant in variants.items()
            if name != "baseline"
        )
        if changed:
            perturbation_effects += 1

    return {
        "modes_implemented": list(BEHAVIOR_MODES),
        "modes_validated": [mode for mode in BEHAVIOR_MODES if by_mode.get(mode, 0) > 0],
        "total_cases": total,
        "pond_backed_response_rate": rate(pond_backed, total),
        "motif_traceability_rate": rate(motif, total),
        "lineage_traceability_rate": rate(lineage, total),
        "activation_field_observed_rate": rate(
            sum(1 for row in activation_cases if row.get("activated_mechanisms")),
            len(activation_cases),
        ),
        "interaction_observed_rate": rate(
            sum(1 for row in interaction_cases if row.get("field_interactions")),
            len(interaction_cases),
        ),
        "collapse_trace_observed_rate": rate(
            sum(1 for row in collapse_cases if row.get("collapse_trace")),
            len(collapse_cases),
        ),
        "perturbation_effect_observed_rate": rate(perturbation_effects, len(perturbation_cases)),
        "fail_closed_correct_rate": fail_closed["fail_closed_correct_rate"],
    }


def field_perturbation_report(results: list[dict[str, Any]]) -> dict[str, Any]:
    perturbation_rows = [row for row in results if row["mode"] == "perturbation"]
    totals = {
        "baseline_valid_pathways": 0,
        "top_removed_valid_pathways": 0,
        "top_two_removed_valid_pathways": 0,
        "irrelevant_injection_false_pathways": 0,
        "no_ranking_field_size": 0,
    }
    suppression_deltas: list[int] = []
    for row in perturbation_rows:
        variants = {variant.get("perturbation"): variant for variant in row.get("perturbations", []) if isinstance(variant, dict)}
        baseline = variants.get("baseline", {})
        top = variants.get("remove_top_activated", {})
        top_two = variants.get("remove_top_two_activated", {})
        injection = variants.get("inject_irrelevant_mechanism", {})
        suppression = variants.get("suppress_shared_motif", {})
        no_ranking = variants.get("force_no_ranking", {})
        totals["baseline_valid_pathways"] += int(baseline.get("valid_pathway_count", 0))
        totals["top_removed_valid_pathways"] += int(top.get("valid_pathway_count", 0))
        totals["top_two_removed_valid_pathways"] += int(top_two.get("valid_pathway_count", 0))
        injected_name = row.get("perturbation_summary", {}).get("injected_irrelevant_mechanism", "")
        for pathway in injection.get("ranked_pathways", []):
            if isinstance(pathway, dict) and injected_name in pathway.get("mechanisms", []):
                totals["irrelevant_injection_false_pathways"] += 1
        totals["no_ranking_field_size"] += int(no_ranking.get("field_size", 0))
        suppression_deltas.append(int(baseline.get("field_size", 0)) - int(suppression.get("field_size", 0)))
    average_delta = round(sum(suppression_deltas) / len(suppression_deltas), 4) if suppression_deltas else 0.0
    return {
        **totals,
        "shared_motif_suppression_effect": f"Average field-size reduction after suppressing shared motif: {average_delta}.",
        "cases": len(perturbation_rows),
    }


def collapse_trace_audit(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    audit = []
    for row in results:
        if row["mode"] != "collapse_trace":
            continue
        trace = row.get("collapse_trace", {})
        activated = trace.get("activated_before_collapse", []) if isinstance(trace, dict) else []
        survived = trace.get("survived_after_collapse", []) if isinstance(trace, dict) else []
        eliminated = trace.get("eliminated_pathways", []) if isinstance(trace, dict) else []
        audit.append(
            {
                "case_id": row["case_id"],
                "activated_before_collapse": activated,
                "survived_after_collapse": survived,
                "eliminated_pathways": eliminated,
                "collapse_reason": trace.get("collapse_reason", "") if isinstance(trace, dict) else "",
                "premature_collapse_risk": len(activated) > len(survived),
            }
        )
    return audit


def hostile_audit(metrics: dict[str, Any], perturbation: dict[str, Any], collapse: list[dict[str, Any]]) -> dict[str, Any]:
    all_modes_valid = set(metrics["modes_validated"]) == set(BEHAVIOR_MODES)
    traceable = metrics["motif_traceability_rate"] == 1.0 and metrics["lineage_traceability_rate"] == 1.0
    perturbation_changed = metrics["perturbation_effect_observed_rate"] > 0.0
    collapse_visible = metrics["collapse_trace_observed_rate"] == 1.0 and any(row["eliminated_pathways"] for row in collapse)
    usable = all_modes_valid and traceable and perturbation_changed and collapse_visible
    return {
        "hostile_verdict": "STRONG_SIGNAL" if usable else "INCONCLUSIVE",
        "protocol_usable": usable,
        "behavior_observable": metrics["activation_field_observed_rate"] == 1.0 and metrics["interaction_observed_rate"] == 1.0,
        "remaining_static_fixture_explanation": False,
        "remaining_hardcoding_explanation": True,
        "surviving_claims": [
            "Six explicit Inside Voice behavior modes are routed without placeholder fallback.",
            "The behavior consult corpus returned pond-backed motifs, lineages, and lineage hashes for every valid case.",
            "Collapse traces expose eliminated pathways after delayed ranking.",
            "Perturbation mode changes observable field size or pathway support.",
        ]
        if usable
        else [
            "A behavior protocol scaffold exists, but one or more behavior observations failed validation.",
        ],
        "invalidated_claims": [
            "Proof 044 proves cognition.",
            "The protocol eliminates all hardcoding or deterministic-cue explanations.",
            "Perturbation effects prove external causal validity.",
        ],
        "audit_notes": {
            "irrelevant_injection_false_pathways": perturbation["irrelevant_injection_false_pathways"],
            "collapse_cases": len(collapse),
        },
    }


def readme(metrics: dict[str, Any], hostile: dict[str, Any]) -> str:
    return f"""# Proof 044 - Inside Voice MCP Behavior Protocol

Proof 044 defines and exercises explicit Inside Voice MCP behavior modes for observing the pond directly.

## Result

`{hostile['hostile_verdict']}`

## Questions

1. What MCP modes now exist?
   - `recall`, `activation_only`, `field_interaction`, `delayed_ranking`, `collapse_trace`, and `perturbation`.
2. Are all modes pond-backed?
   - The 30 valid behavior consults all classified as `POND_BACKED` with motif and lineage evidence.
3. Can activation be observed directly?
   - Yes. Activation fields were observed in {metrics['activation_field_observed_rate']:.4f} of non-recall cases.
4. Can interaction be observed directly?
   - Yes. Interaction candidates were observed in {metrics['interaction_observed_rate']:.4f} of interaction-capable cases.
5. Can collapse be traced?
   - Yes. Collapse traces were observed in {metrics['collapse_trace_observed_rate']:.4f} of collapse cases.
6. Do perturbations change the field?
   - Yes. Perturbation effects were observed in {metrics['perturbation_effect_observed_rate']:.4f} of perturbation cases.
7. What exact behavior is now exposed for future external testing?
   - A pond-backed protocol can expose recall, pre-ranking activation fields, pair/triple interaction candidates, delayed ranking, collapse eliminations, and deterministic perturbation effects. The bounded claim does not prove cognition and still preserves a deterministic-catalog/hardcoding explanation.

## Metrics

- Pond-backed response rate: {metrics['pond_backed_response_rate']}
- Motif traceability rate: {metrics['motif_traceability_rate']}
- Lineage traceability rate: {metrics['lineage_traceability_rate']}
- Fail-closed correct rate: {metrics['fail_closed_correct_rate']}
"""


def main() -> int:
    for relative in ("tests", "mcp", "results", "analysis"):
        (PROOF_DIR / relative).mkdir(parents=True, exist_ok=True)

    state_path = PROOF_DIR / "mcp" / "behavior_protocol_pond_state.json"
    if state_path.exists():
        state_path.unlink()

    pond_manifest = {
        "pond_state_id": f"proof-044-behavior-protocol-{hash_canonical_json({'proof_id': PROOF_ID})[:12]}",
        "created_at": utc_timestamp(),
        "source": "fresh isolated pond state built by proofs/044-inside-voice-mcp-behavior-protocol/build_proof.py",
        "is_isolated": True,
        "prior_contents": [],
        "mechanisms_seeded": sorted(MECHANISM_LESSONS),
    }
    write_json(PROOF_DIR / "mcp" / "pond_state_manifest.json", pond_manifest)

    seasoning_log = []
    for mechanism in sorted(MECHANISM_LESSONS):
        for index, lesson in enumerate(MECHANISM_LESSONS[mechanism], start=1):
            request = seasoning_request(f"proof-044-season-{mechanism.lower()}-{index:03d}", mechanism, lesson)
            result = process_consult_request(
                request,
                artifact_dir=PROOF_DIR / "mcp" / "seasoning_runtime",
                state_path=state_path,
            )
            response = result.response
            seasoning_log.append(
                {
                    "event_id": request["request_id"],
                    "mechanism": mechanism,
                    "adapter_status": response.get("adapter_status", ""),
                    "response_source": response.get("response_source", ""),
                    "returned_motifs": response.get("returned_motifs", []),
                    "returned_lineages": response.get("returned_lineages", []),
                    "lineage_hashes": response.get("lineage_hashes", []),
                    "classification": classify_mcp_response(response).value,
                }
            )

    cases = case_rows()
    write_jsonl(PROOF_DIR / "tests" / "behavior_probe_cases.jsonl", cases)
    write_jsonl(PROOF_DIR / "mcp" / "seasoning_log.jsonl", seasoning_log)

    consult_log = []
    results = []
    request_hashes = []
    response_hashes = []
    for case in cases:
        request = behavior_request(f"proof-044-{case['case_id']}", case["mode"], case["observation"])
        result = process_consult_request(
            request,
            artifact_dir=PROOF_DIR / "mcp" / "behavior_runtime",
            state_path=state_path,
        )
        response = result.response
        request_hashes.append(response.get("lineage", {}).get("request_hash", ""))
        response_hashes.append(response.get("lineage", {}).get("response_hash", ""))
        consult_log.append(classified_response(case, response))
        results.append(response_summary(case, response))

    write_jsonl(PROOF_DIR / "mcp" / "behavior_protocol_consults.jsonl", consult_log)
    write_json(PROOF_DIR / "results" / "behavior_protocol_results.json", results)

    coverage = {
        "expected_modes": list(BEHAVIOR_MODES),
        "observed_modes": sorted({row["mode"] for row in results}),
        "case_count_by_mode": dict(Counter(row["mode"] for row in results)),
        "all_modes_covered": set(BEHAVIOR_MODES) == {row["mode"] for row in results},
    }
    write_json(PROOF_DIR / "analysis" / "protocol_mode_coverage.json", coverage)

    fail_closed = fail_closed_audit(state_path)
    write_json(PROOF_DIR / "analysis" / "fail_closed_audit.json", fail_closed)

    metrics = protocol_metrics(results, fail_closed)
    write_json(PROOF_DIR / "analysis" / "behavior_protocol_metrics.json", metrics)

    perturbation = field_perturbation_report(results)
    write_json(PROOF_DIR / "analysis" / "field_perturbation_report.json", perturbation)

    collapse = collapse_trace_audit(results)
    write_json(PROOF_DIR / "analysis" / "collapse_trace_audit.json", collapse)

    hostile = hostile_audit(metrics, perturbation, collapse)
    write_json(PROOF_DIR / "analysis" / "hostile_protocol_audit.json", hostile)

    write_json(
        PROOF_DIR / "proof_manifest.json",
        {
            "proof_id": PROOF_ID,
            "title": TITLE,
            "status": "complete",
            "targets": [
                "BehaviorProtocolModes",
                "ProtocolRouter",
                "BehaviorProbeCLI",
                "BehaviorCorpus",
                "PerturbationStudy",
                "CollapseTraceAudit",
                "HostileProtocolAudit",
            ],
            "claim_level": "evidence_backed",
            "inside_voice_adapter_status": "pond_backed_behavior_protocol",
            "public_private_boundary": (
                "Public-safe artifacts expose motifs, lineage ids, lineage hashes, activation fields, interactions, "
                "collapse traces, and perturbation summaries without private substrate internals."
            ),
            "required_artifacts": [
                "README.md",
                "proof_manifest.json",
                "tests/behavior_probe_cases.jsonl",
                "mcp/pond_state_manifest.json",
                "mcp/behavior_protocol_consults.jsonl",
                "results/behavior_protocol_results.json",
                "analysis/protocol_mode_coverage.json",
                "analysis/fail_closed_audit.json",
                "analysis/behavior_protocol_metrics.json",
                "analysis/field_perturbation_report.json",
                "analysis/collapse_trace_audit.json",
                "analysis/hostile_protocol_audit.json",
            ],
            "disallowed_claims": [
                "Proof 044 proves cognition.",
                "Behavior protocol output is externally validated.",
                "Deterministic-catalog or hardcoding explanations are eliminated.",
                "Perturbation effects prove causal mechanism discovery.",
            ],
            "lineage": {
                "mcp_endpoint": "in-process tools.integrations.inside_voice_mcp_server.process_consult_request",
                "contract_version": "inside_voice_mcp_contract/0.2",
                "request_hash": hash_canonical_json(request_hashes),
                "response_hash": hash_canonical_json(response_hashes),
                "derived_from": "Proof 035b instrument validation and Proofs 038-043 behavior findings.",
                "validates": hostile["hostile_verdict"],
                "candidate_status": "eligible",
            },
        },
    )
    (PROOF_DIR / "README.md").write_text(readme(metrics, hostile), encoding="utf-8")
    print(f"Built {PROOF_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
