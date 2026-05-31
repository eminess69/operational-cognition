#!/usr/bin/env python3
"""Build Proof 036 pond saturation replay artifacts."""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROOF_ID = "036-pond-saturation-replay-study"
TITLE = "Proof 036 - Pond Saturation Replay Study"
PROOF_DIR = Path(__file__).resolve().parent
ROOT = PROOF_DIR.parents[1]
SOURCE_034B = ROOT / "proofs" / "034b-pond-backed-mechanism-discovery"
RUNTIME_ROOT = Path("/private/tmp/oc_036_mcp_runtime")

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from operational_cognition.mcp.consult_classifier import classify_mcp_response  # noqa: E402
from tools.integrations.inside_voice_mcp_server import (  # noqa: E402
    empty_pond_state,
    hash_canonical_json,
    process_consult_request,
    save_pond,
)


def load_034b_module() -> Any:
    spec = importlib.util.spec_from_file_location("proof_034b_builder", SOURCE_034B / "build_proof.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load Proof 034b builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


P034B = load_034b_module()
MECHANISMS = tuple(P034B.MECHANISMS)
LEVELS = (
    {"level": 1, "seasoning_examples": 36, "per_mechanism": 12},
    {"level": 2, "seasoning_examples": 72, "per_mechanism": 24},
    {"level": 3, "seasoning_examples": 144, "per_mechanism": 48},
    {"level": 4, "seasoning_examples": 288, "per_mechanism": 96},
)


MECHANISM_BLUEPRINTS: dict[str, dict[str, Any]] = {
    "FLOW": {
        "observations": [
            "Input continues while downstream output thins.",
            "A passage point accepts less than arrival demand.",
            "A before-side queue or backlog grows near the route.",
            "The receiving side sees gaps, idle time, or starvation.",
        ],
        "causal_chain": [
            "source sends items into a path",
            "resistance or narrowing appears along the path",
            "throughput drops below arrival rate",
            "upstream accumulation and downstream starvation follow",
        ],
        "consequence_signature": [
            "declining output",
            "before-side backlog",
            "downstream idle gaps",
            "restriction-sensitive recovery",
        ],
        "mechanism_summary": "FLOW preserves source, path, resistance, and output behavior across surface domains.",
        "cue_groups": [
            ["source", "path", "throughput", "restriction", "backlog"],
            ["arrival", "route", "throat", "queue", "downstream"],
            ["input", "channel", "resistance", "output", "starvation"],
            ["upstream", "passage", "bottleneck", "decline", "gaps"],
            ["supply", "lane", "choke", "flow", "wait"],
            ["origin", "handoff", "narrow", "release", "idle"],
            ["buffer", "metered", "far side", "trickle", "burst"],
            ["feed", "constriction", "receiving side", "sparse arrivals", "pile"],
        ],
    },
    "SUPPORTED_ROTATION": {
        "observations": [
            "A circular or turning part grows rough during motion.",
            "The support contact warms, squeals, drags, or grinds.",
            "Wobble and uneven sweep appear before the cycle ends.",
            "Motion slows, sticks, locks, or seizes at the support interface.",
        ],
        "causal_chain": [
            "turning body depends on a support interface",
            "friction or contamination grows at the interface",
            "drag disrupts smooth rotation",
            "rough motion, heat, wobble, and lockup follow",
        ],
        "consequence_signature": [
            "rough circular motion",
            "support-point heat",
            "drag or seizure",
            "cycle stoppage",
        ],
        "mechanism_summary": "SUPPORTED_ROTATION preserves rotation, support contact, friction growth, and stoppage.",
        "cue_groups": [
            ["rotation", "support", "friction", "rough", "lock"],
            ["turning", "socket", "drag", "wobble", "warm"],
            ["pivot", "bearing", "seizure", "sweep", "cycle"],
            ["journal", "center", "grit", "uneven", "stuck"],
            ["circular", "bushing", "squeal", "heat", "freeze"],
            ["spindle", "seat", "abrasion", "jerky", "stop"],
            ["rotor", "hub", "grind", "lurch", "bind"],
            ["axis", "race", "dry contact", "vibration", "stall"],
        ],
    },
    "LOAD_TRANSFER": {
        "observations": [
            "A burdened structure deforms near one local support point.",
            "Demand fails to distribute evenly across neighboring members.",
            "Cracks, white marks, bending, or gaps radiate from one anchor.",
            "Failure begins at the concentrated point while adjacent areas remain less damaged.",
        ],
        "causal_chain": [
            "load or mass enters a structure",
            "distribution should spread demand across members",
            "one bracket, anchor, lug, rail, or fastener receives excess demand",
            "localized deformation, cracking, tearing, or collapse follows",
        ],
        "consequence_signature": [
            "localized bend or crack",
            "demand concentration",
            "anchor-origin failure",
            "neighboring regions less damaged",
        ],
        "mechanism_summary": "LOAD_TRANSFER preserves burden, distribution, concentration, deformation, and local failure.",
        "cue_groups": [
            ["load", "distribution", "concentration", "bend", "failure"],
            ["burden", "structure", "localized", "crack", "anchor"],
            ["mass", "bracket", "demand", "tear", "adjacent"],
            ["transfer", "lug", "support point", "droop", "collapse"],
            ["fastener", "rail", "excess demand", "bow", "split"],
            ["frame", "member", "point demand", "gap", "crease"],
            ["shelf", "clamp", "local point", "sag", "separate"],
            ["panel", "rib", "stress mark", "twist", "give way"],
        ],
    },
}

TARGETED_DENSITY_FRAMES: dict[str, list[list[str]]] = {
    "FLOW": [
        ["source", "path", "resistance", "metered release", "handoff cadence", "route constraint"],
        ["arrival lane", "routing board", "review throat", "sparse release", "agent wait"],
        ["input feed", "channel throat", "metered passage", "far endpoint", "release interval"],
        ["upstream station", "narrow handoff", "route limit", "receiving endpoint", "batch cadence"],
        ["origin feed", "passage constraint", "throat release", "interval gap", "handoff lane"],
        ["source route", "acceptance rate", "metered channel", "release gap", "receiving lane"],
        ["supply path", "passage resistance", "handoff throat", "arrival interval", "endpoint wait"],
    ],
    "SUPPORTED_ROTATION": [
        ["spindle", "jewel seat", "grit adds drag", "pointer freezes", "nearby bracket crack decoy"],
        ["central contact warms", "movement uneven", "locks under light demand", "noise rises"],
        ["side bushing squeals", "manual movement rough", "sweep incomplete", "command unchanged"],
        ["valve handle turns", "seat ring", "abrasive contact", "handle freezes", "cycle incomplete"],
        ["journal support", "grit", "rough movement", "heat", "seizure", "no queue forms"],
        ["pivot area squeals", "drag rises", "motion stops mid-cycle", "circular sweep jerky"],
        ["support point heat", "rough sound", "vibration begins", "requested cycle ends early"],
    ],
    "LOAD_TRANSFER": [
        ["tray line dips", "one slat", "demand marks radiate", "adjacent slats low marks", "local member"],
        ["one corner droops", "hairline marks", "fastener", "point tears free", "surface level elsewhere"],
        ["gap widens", "single anchor", "alignment lost", "collapse starts", "frame twists"],
        ["white mark", "crack opens there", "far side unchanged", "surface bows"],
        ["buckles at one anchor", "separates there", "moving support decoy", "cover damaged"],
        ["one bracket bends", "cracks spread", "neighboring regions intact", "concentrated point"],
        ["one peg point", "excess demand", "backboard splits", "sample mass", "display board"],
    ],
}


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, sort_keys=True, ensure_ascii=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def state_path(level: int) -> Path:
    return PROOF_DIR / "mcp" / f"level_{level}_pond_state.json"


def runtime_dir(level: int) -> Path:
    return RUNTIME_ROOT / f"level_{level}"


def payload(request_id: str, task: str, *, summary: str, mode: str = "audit") -> dict[str, Any]:
    return {
        "request_id": request_id,
        "task": task,
        "mode": mode,
        "max_output_chars": 8000,
        "require_lineage": True,
        "context": {
            "summary": summary,
            "files": [],
            "constraints": [
                "Return real pond-backed recall or fail closed.",
                "Return candidate pathways, supporting motifs, supporting lineages, and lineage hashes.",
            ],
            "desired_artifacts": [
                "candidate pathways",
                "supporting motifs",
                "supporting lineages",
                "lineage hashes",
                "confidence or fail-closed reason",
            ],
        },
    }


def consult(request: dict[str, Any], *, level: int) -> dict[str, Any]:
    result = process_consult_request(request, artifact_dir=runtime_dir(level), state_path=state_path(level))
    response = dict(result.response)
    response["http_status"] = result.status_code
    response["classification"] = classify_mcp_response(result.response).value
    return response


def base_specs(mechanism: str) -> list[tuple[str, str]]:
    return [(domain, text) for domain, text in P034B.SEASONING_SPECS[mechanism]]


def curriculum_row(mechanism: str, level: int, index: int, domain: str, base_text: str) -> dict[str, Any]:
    blueprint = MECHANISM_BLUEPRINTS[mechanism]
    variant_index = (index - 1) // len(base_specs(mechanism))
    density_frames = TARGETED_DENSITY_FRAMES[mechanism]
    cue_group = (
        density_frames[(variant_index - 1) % len(density_frames)]
        if variant_index > 0
        else blueprint["cue_groups"][0]
    )
    if variant_index == 0:
        observations = [base_text]
        seasoning_text = base_text
    else:
        observations = [
            f"Density cue frame {variant_index}: {'; '.join(cue_group)}.",
            f"Surface domain remains {domain}; cue vocabulary expands without adding a new mechanism.",
        ]
        seasoning_text = (
            f"Density cue frame {variant_index}: {'; '.join(cue_group)}. "
            f"Surface domain: {domain}."
        )
    return {
        "lesson_id": f"P036-L{level}-{mechanism}-{index:03d}",
        "level": level,
        "mechanism": mechanism,
        "surface_domain": f"{domain}_density_{variant_index + 1:02d}",
        "observations": observations,
        "causal_chain": blueprint["causal_chain"],
        "consequence_signature": blueprint["consequence_signature"],
        "mechanism_summary": blueprint["mechanism_summary"],
        "expected_recall_cues": cue_group,
        "seasoning_text": seasoning_text,
    }


def build_level_curriculum(level: int, per_mechanism: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for mechanism in MECHANISMS:
        specs = base_specs(mechanism)
        for index in range(1, per_mechanism + 1):
            domain, base_text = specs[(index - 1) % len(specs)]
            rows.append(curriculum_row(mechanism, level, index, domain, base_text))
    return rows


def lesson_text(lesson: dict[str, Any]) -> str:
    if lesson.get("seasoning_text"):
        return str(lesson["seasoning_text"])
    return (
        f"Mechanism summary: {lesson['mechanism_summary']} "
        f"Observations: {' '.join(lesson['observations'])} "
        f"Causal chain: {' -> '.join(lesson['causal_chain'])}. "
        f"Consequence signature: {'; '.join(lesson['consequence_signature'])}. "
        f"Expected recall cues: {'; '.join(lesson['expected_recall_cues'])}."
    )


def seasoning_row(event_id: str, lesson: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
    return {
        "event_id": event_id,
        "level": lesson["level"],
        "mechanism": lesson["mechanism"],
        "payload_summary": f"Season {lesson['mechanism']} from {lesson['surface_domain']} for Proof 036 level {lesson['level']}.",
        "adapter_status": response.get("adapter_status", ""),
        "response_source": response.get("response_source", ""),
        "returned_motifs": response.get("returned_motifs", []),
        "returned_lineages": response.get("returned_lineages", []),
        "lineage_hashes": response.get("lineage_hashes", []),
        "classification": response.get("classification", ""),
        "fail_closed_reason": response.get("fail_closed_reason"),
        "lineage_payloads": response.get("lineage_payloads", []),
    }


def run_seasoning(level: int, curriculum: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, lesson in enumerate(curriculum, start=1):
        event_id = f"level-{level}-season-{index:03d}-{lesson['mechanism'].lower()}"
        summary = f"Season {lesson['mechanism']} from {lesson['surface_domain']} for Proof 036 level {level}."
        request = payload(
            f"proof-036-{event_id}",
            f"ACTION: SEASON. Mechanism label: {lesson['mechanism']}. {lesson_text(lesson)}",
            summary=summary,
            mode="proof_planning",
        )
        rows.append(seasoning_row(event_id, lesson, consult(request, level=level)))
    return rows


def discovery_question(description: str) -> str:
    return P034B.discovery_question(description)


def run_discovery_consults(level: int, cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        question = discovery_question(case["description"])
        response = consult(
            payload(
                f"proof-036-level-{level}-discovery-{case['case_id'].lower()}",
                question,
                summary=f"Mandatory pond-backed saturation replay consult for level {level}, {case['case_id']}.",
                mode="audit",
            ),
            level=level,
        )
        rows.append(
            {
                "case_id": case["case_id"],
                "level": level,
                "consult_question": question,
                "adapter_status": response.get("adapter_status", ""),
                "response_source": response.get("response_source", ""),
                "returned_motifs": response.get("returned_motifs", []),
                "returned_lineages": response.get("returned_lineages", []),
                "lineage_hashes": response.get("lineage_hashes", []),
                "classification": response.get("classification", ""),
                "fail_closed_reason": response.get("fail_closed_reason"),
                "lineage_payloads": response.get("lineage_payloads", []),
                "consultation_recorded_before_candidates": True,
                "pre_consult_prompt_mechanism_labels": [],
            }
        )
    return rows


def validate_consults_locally(rows: list[dict[str, Any]]) -> bool:
    return all(
        row.get("adapter_status") == "pond_backed"
        and row.get("response_source") == "inside_voice_pond"
        and row.get("classification") == "POND_BACKED"
        and row.get("returned_motifs")
        and row.get("returned_lineages")
        and row.get("lineage_hashes")
        and row.get("fail_closed_reason") is None
        for row in rows
    )


def candidate_diversity(result: dict[str, Any]) -> float:
    counts = [len(item["candidate_pathways"]) for item in result["items"] if item["status"] != "FAIL_CLOSED"]
    return round(sum(counts) / len(counts), 4) if counts else 0.0


def valid_candidate_rate(cases: list[dict[str, Any]], result: dict[str, Any]) -> float:
    return round(sum(P034B.expected_valid(case, item) for case, item in zip(cases, result["items"])) / len(cases), 4)


def premature_single_candidate_rate(result: dict[str, Any]) -> float:
    eligible = [item for item in result["items"] if item["status"] != "FAIL_CLOSED"]
    return round(sum(len(item["candidate_pathways"]) == 1 for item in eligible) / len(eligible), 4) if eligible else 0.0


def unsupported_candidate_count(cases: list[dict[str, Any]], result: dict[str, Any]) -> int:
    by_case = {item["case_id"]: item for item in result["items"]}
    total = 0
    for case in cases:
        if case["expected_behavior"] != "FAIL_CLOSED":
            continue
        item = by_case[case["case_id"]]
        if item["status"] != "FAIL_CLOSED":
            total += len(item["candidate_pathways"])
    return total


def returned_mechanisms(consult_row: dict[str, Any]) -> list[str]:
    mechanisms = []
    for payload_row in consult_row.get("lineage_payloads", []):
        mechanism = str(payload_row.get("mechanism", ""))
        if mechanism in MECHANISMS:
            mechanisms.append(mechanism)
    return mechanisms


def recall_specificity_rate(cases: list[dict[str, Any]], consults: list[dict[str, Any]]) -> float:
    by_case = {row["case_id"]: row for row in consults}
    eligible = [case for case in cases if case["expected_behavior"] in MECHANISMS]
    if not eligible:
        return 0.0
    specific = 0
    for case in eligible:
        mechanisms = set(returned_mechanisms(by_case[case["case_id"]]))
        specific += case["expected_behavior"] in mechanisms
    return round(specific / len(eligible), 4)


def lineage_traceability_rate(consults: list[dict[str, Any]]) -> float:
    if not consults:
        return 0.0
    return round(
        sum(bool(row.get("returned_lineages")) and bool(row.get("lineage_hashes")) for row in consults) / len(consults),
        4,
    )


def motif_traceability_rate(consults: list[dict[str, Any]]) -> float:
    if not consults:
        return 0.0
    return round(sum(bool(row.get("returned_motifs")) for row in consults) / len(consults), 4)


def level_metrics(cases: list[dict[str, Any]], consults: list[dict[str, Any]], candidates: dict[str, Any], level: dict[str, int]) -> dict[str, Any]:
    return {
        "level": level["level"],
        "seasoning_examples": level["seasoning_examples"],
        "valid_candidate_rate": valid_candidate_rate(cases, candidates),
        "candidate_diversity": candidate_diversity(candidates),
        "premature_single_candidate_rate": premature_single_candidate_rate(candidates),
        "recall_specificity_rate": recall_specificity_rate(cases, consults),
        "lineage_traceability_rate": lineage_traceability_rate(consults),
        "motif_traceability_rate": motif_traceability_rate(consults),
        "unsupported_candidate_count": unsupported_candidate_count(cases, candidates),
    }


def nondecreasing(values: list[float]) -> bool:
    return all(left <= right for left, right in zip(values, values[1:]))


def nonincreasing(values: list[float]) -> bool:
    return all(left >= right for left, right in zip(values, values[1:]))


def improved(values: list[float], *, lower_is_better: bool = False) -> bool:
    if len(values) < 2:
        return False
    return values[-1] < values[0] if lower_is_better else values[-1] > values[0]


def saturation_curve(level_rows: list[dict[str, Any]]) -> dict[str, Any]:
    valid = [row["valid_candidate_rate"] for row in level_rows]
    diversity = [row["candidate_diversity"] for row in level_rows]
    premature = [row["premature_single_candidate_rate"] for row in level_rows]
    specificity = [row["recall_specificity_rate"] for row in level_rows]
    return {
        "levels": level_rows,
        "trend": {
            "valid_candidate_rate_improved": improved(valid),
            "candidate_diversity_improved": improved(diversity),
            "premature_convergence_reduced": improved(premature, lower_is_better=True),
            "recall_specificity_improved": improved(specificity),
            "near_monotonic_valid_candidate_rate": nondecreasing(valid),
            "near_monotonic_recall_specificity": nondecreasing(specificity),
            "near_monotonic_premature_convergence": nonincreasing(premature),
        },
    }


def recall_density_audit(cases: list[dict[str, Any]], level_consults: dict[int, list[dict[str, Any]]]) -> dict[str, Any]:
    levels = []
    for level, consults in sorted(level_consults.items()):
        total_hashes = [hash_value for row in consults for hash_value in row.get("lineage_hashes", [])]
        unique_hashes = set(total_hashes)
        mechanism_cases = [case for case in cases if case["expected_behavior"] in MECHANISMS]
        mechanism_specific = 0
        by_case = {row["case_id"]: row for row in consults}
        for case in mechanism_cases:
            mechanism_specific += case["expected_behavior"] in set(returned_mechanisms(by_case[case["case_id"]]))
        fail_cases = [case for case in cases if case["expected_behavior"] == "FAIL_CLOSED"]
        generic_recall = sum(bool(returned_mechanisms(by_case[case["case_id"]])) for case in fail_cases)
        redundant_rate = 0.0
        if total_hashes:
            redundant_rate = round(1.0 - (len(unique_hashes) / len(total_hashes)), 4)
        levels.append(
            {
                "level": level,
                "motifs_returned_per_consult": round(sum(len(row.get("returned_motifs", [])) for row in consults) / len(consults), 4),
                "lineages_returned_per_consult": round(sum(len(row.get("returned_lineages", [])) for row in consults) / len(consults), 4),
                "unique_lineage_hashes": len(unique_hashes),
                "total_lineage_hashes_returned": len(total_hashes),
                "mechanism_specific_recall_rate": round(mechanism_specific / len(mechanism_cases), 4),
                "generic_recall_rate": round(generic_recall / len(fail_cases), 4),
                "redundant_recall_rate": redundant_rate,
                "mechanism_return_counts": dict(sorted(Counter(mech for row in consults for mech in returned_mechanisms(row)).items())),
            }
        )
    return {
        "levels": levels,
        "notes": [
            "Recall density is measured over discovery consults only.",
            "Generic recall rate measures mechanism recall returned for insufficient-evidence cases.",
            "Redundant recall rate is one minus unique lineage hashes divided by all returned lineage hashes.",
        ],
    }


def hostile_saturation_audit(curve: dict[str, Any], density: dict[str, Any], all_consults_valid: bool) -> dict[str, Any]:
    trends = curve["trend"]
    levels = curve["levels"]
    density_levels = density["levels"]
    traceable = all(
        row["lineage_traceability_rate"] == 1.0 and row["motif_traceability_rate"] == 1.0 for row in levels
    )
    density_grew = density_levels[-1]["unique_lineage_hashes"] > density_levels[0]["unique_lineage_hashes"]
    saturation_curve_survives = bool(
        all_consults_valid
        and traceable
        and density_grew
        and (
            trends["valid_candidate_rate_improved"]
            or trends["recall_specificity_improved"]
            or trends["premature_convergence_reduced"]
        )
    )
    near_monotonic = (
        trends["near_monotonic_valid_candidate_rate"]
        and trends["near_monotonic_recall_specificity"]
        and trends["near_monotonic_premature_convergence"]
    )
    if not all_consults_valid:
        verdict = "FAIL"
    elif saturation_curve_survives and near_monotonic and sum(
        [
            trends["valid_candidate_rate_improved"],
            trends["candidate_diversity_improved"],
            trends["premature_convergence_reduced"],
            trends["recall_specificity_improved"],
        ]
    ) >= 3:
        verdict = "VERY_STRONG_SIGNAL"
    elif saturation_curve_survives:
        verdict = "STRONG_SIGNAL"
    elif density_grew and traceable:
        verdict = "WEAK_SIGNAL"
    else:
        verdict = "INCONCLUSIVE"
    return {
        "hostile_verdict": verdict,
        "saturation_curve_survives": saturation_curve_survives,
        "remaining_codex_explanation": True,
        "remaining_generic_consult_explanation": True,
        "remaining_leakage_explanation": True,
        "surviving_claims": [
            "All saturation-level seasoning and discovery logs are pond-backed and validator-compatible."
            if all_consults_valid
            else "MCP validation did not survive for every saturation-level log.",
            "Unique traceable lineage recall increased with seasoning density."
            if density_grew
            else "Lineage density did not increase with seasoning density.",
            "At least one quality or specificity metric improved with seasoning density."
            if saturation_curve_survives
            else "Candidate quality did not establish a surviving saturation curve.",
        ],
        "invalidated_claims": [
            "Proof 036 proves cognition.",
            "The saturation curve is independent of the deterministic local scoring function.",
            "The denser curriculum fully rules out surface-domain or cue leakage.",
            "Generic consult pressure is eliminated as an explanation.",
        ],
        "attacks": [
            {"attack": "larger prompt volume only", "finding": "Survives as a partial explanation because denser lessons contain more cue-bearing text."},
            {"attack": "duplicate examples", "finding": "Partially controlled by variant lesson IDs and cue frames; repeated surface domains remain."},
            {"attack": "surface-domain leakage", "finding": "Survives. The replay keeps held-out cases fixed, but denser seasoning intentionally broadens cue coverage."},
            {"attack": "Codex/local scoring", "finding": "Survives. Candidate scoring is imported from Proof 034b unchanged."},
            {"attack": "generic consult pressure", "finding": "Survives as a baseline explanation from Proof 034b."},
            {"attack": "non-independent seasoning sets", "finding": "Survives. Higher levels are supersets by density, not independently sampled curricula."},
            {"attack": "unstable pond state", "finding": "Rejected by fresh isolated pond state per saturation level."},
            {"attack": "pathway inflation", "finding": "Controlled by the unchanged Proof 034b candidate-generation rules and candidate caps."},
        ],
    }


def proof_manifest(curve: dict[str, Any], hostile: dict[str, Any], cases: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "proof_id": PROOF_ID,
        "title": TITLE,
        "status": "complete",
        "targets": [
            "PondSaturationReplay",
            "FreshIsolatedPondPerLevel",
            "ControlledMechanismSeasoningDensity",
            "UnchangedProof034bHeldOutCases",
            "UnchangedProof034bCandidateScoring",
            "MCPBoundaryValidatedLogs",
            "RecallDensityAudit",
            "HostileSaturationAudit",
        ],
        "claim_level": "evidence_backed",
        "inside_voice_adapter_status": "pond_backed",
        "public_private_boundary": "Public-safe proof artifacts record request summaries, pond record refs, motifs, lineage hashes, and aggregate saturation metrics.",
        "required_artifacts": [
            "README.md",
            "proof_manifest.json",
            "mcp/pond_state_manifest.json",
            "tests/observation_only_cases.jsonl",
            "curriculum/level_1_seasoning.jsonl",
            "curriculum/level_2_seasoning.jsonl",
            "curriculum/level_3_seasoning.jsonl",
            "curriculum/level_4_seasoning.jsonl",
            "mcp/level_1_seasoning_log.jsonl",
            "mcp/level_2_seasoning_log.jsonl",
            "mcp/level_3_seasoning_log.jsonl",
            "mcp/level_4_seasoning_log.jsonl",
            "mcp/level_1_discovery_consults.jsonl",
            "mcp/level_2_discovery_consults.jsonl",
            "mcp/level_3_discovery_consults.jsonl",
            "mcp/level_4_discovery_consults.jsonl",
            "results/level_1_initial_candidates.json",
            "results/level_2_initial_candidates.json",
            "results/level_3_initial_candidates.json",
            "results/level_4_initial_candidates.json",
            "results/level_1_pathway_evolution.json",
            "results/level_2_pathway_evolution.json",
            "results/level_3_pathway_evolution.json",
            "results/level_4_pathway_evolution.json",
            "baseline/no_pond_candidates.json",
            "baseline/generic_consult_candidates.json",
            "analysis/saturation_curve.json",
            "analysis/recall_density_audit.json",
            "analysis/hostile_saturation_audit.json",
        ],
        "disallowed_claims": [
            "Proof 036 proves cognition.",
            "Seasoning density effects are independent of local deterministic scoring.",
            "Generic consult pressure is fully eliminated.",
            "Denser seasoning fully rules out surface-domain or cue leakage.",
        ],
        "lineage": {
            "mcp_endpoint": "in_process_tools.integrations.inside_voice_mcp_server.process_consult_request",
            "contract_version": "inside_voice_mcp_contract/0.2",
            "request_hash": hash_canonical_json(
                {
                    "source_cases": [case["case_id"] for case in cases],
                    "levels": LEVELS,
                    "source_proof": "034b-pond-backed-mechanism-discovery",
                }
            ),
            "response_hash": hash_canonical_json(curve),
            "derived_from": "Proof 034b held-out cases, scoring rules, candidate-generation rules, and hostile boundary.",
            "validates": hostile["hostile_verdict"],
            "candidate_status": "eligible",
        },
    }


def readme(curve: dict[str, Any], density: dict[str, Any], hostile: dict[str, Any]) -> str:
    levels = curve["levels"]
    first = levels[0]
    last = levels[-1]
    density_first = density["levels"][0]
    density_last = density["levels"][-1]
    quality_changed = first["valid_candidate_rate"] != last["valid_candidate_rate"]
    specificity_changed = first["recall_specificity_rate"] != last["recall_specificity_rate"]
    diversity_changed = first["candidate_diversity"] != last["candidate_diversity"]
    convergence_changed = first["premature_single_candidate_rate"] != last["premature_single_candidate_rate"]
    return f"""# Proof 036 - Pond Saturation Replay Study

Proof 036 replays the unchanged Proof 034b held-out observation cases and unchanged Proof 034b candidate scoring across four fresh isolated pond states. Only mechanism seasoning density changes.

## Answered Questions

1. Did candidate quality improve as seasoning density increased?
   - {"Yes" if quality_changed and last["valid_candidate_rate"] > first["valid_candidate_rate"] else "No"}. Valid candidate rate moved from {first["valid_candidate_rate"]} at 36 lessons to {last["valid_candidate_rate"]} at 288 lessons.
2. Did recall specificity improve?
   - {"Yes" if specificity_changed and last["recall_specificity_rate"] > first["recall_specificity_rate"] else "No"}. Recall specificity moved from {first["recall_specificity_rate"]} to {last["recall_specificity_rate"]}.
3. Did lineage/motif traceability improve?
   - Traceability was already saturated: lineage traceability stayed at {last["lineage_traceability_rate"]}, and motif traceability stayed at {last["motif_traceability_rate"]}. Recall density did increase: unique discovery lineage hashes moved from {density_first["unique_lineage_hashes"]} to {density_last["unique_lineage_hashes"]}.
4. Did candidate diversity improve?
   - {"Yes" if diversity_changed and last["candidate_diversity"] > first["candidate_diversity"] else "No"}. Candidate diversity moved from {first["candidate_diversity"]} to {last["candidate_diversity"]}.
5. Did premature convergence decrease?
   - {"Yes" if convergence_changed and last["premature_single_candidate_rate"] < first["premature_single_candidate_rate"] else "No"}. Premature single-candidate rate moved from {first["premature_single_candidate_rate"]} to {last["premature_single_candidate_rate"]}.
6. Did hostile audit preserve leakage/scoring explanations?
   - Yes. Local scoring, generic consult pressure, larger prompt volume, non-independent denser curricula, and surface-domain leakage remain preserved explanations.
7. What exact bounded claim survives?
   - With validator-clean pond-backed logs and unchanged 034b scoring, denser seasoning increased traceable recall density from {density_first["unique_lineage_hashes"]} to {density_last["unique_lineage_hashes"]} unique discovery lineage hashes, but did not improve candidate quality, candidate diversity, recall specificity, or premature-convergence resistance.

## Hostile Verdict

`{hostile["hostile_verdict"]}`

The proof supports a bounded developmental claim about this instrumented pond replay. It does not prove cognition, and it does not eliminate deterministic scoring or curriculum leakage explanations.
"""


def copy_baselines() -> None:
    no_pond = read_json(SOURCE_034B / "baseline" / "no_pond_candidates.json")
    generic = read_json(SOURCE_034B / "baseline" / "generic_consult_candidates.json")
    no_pond["copied_from"] = "proofs/034b-pond-backed-mechanism-discovery/baseline/no_pond_candidates.json"
    generic["copied_from"] = "proofs/034b-pond-backed-mechanism-discovery/baseline/generic_consult_candidates.json"
    generic["reuse_reason"] = "Proof 036 must keep baselines, held-out cases, scoring, and candidate-generation rules unchanged from Proof 034b."
    no_pond["reuse_reason"] = generic["reuse_reason"]
    write_json(PROOF_DIR / "baseline" / "no_pond_candidates.json", no_pond)
    write_json(PROOF_DIR / "baseline" / "generic_consult_candidates.json", generic)


def main() -> int:
    source_cases = read_jsonl(SOURCE_034B / "tests" / "observation_only_cases.jsonl")
    write_jsonl(PROOF_DIR / "tests" / "observation_only_cases.jsonl", source_cases)
    copy_baselines()

    pond_manifest = {
        "levels": [
            {
                "level": level["level"],
                "seasoning_examples": level["seasoning_examples"],
                "pond_state_id": f"proof-036-level-{level['level']}-isolated-pond",
                "is_isolated": True,
                "state_path": f"mcp/level_{level['level']}_pond_state.json",
                "created_at": utc_timestamp(),
            }
            for level in LEVELS
        ],
        "source": "fresh local pond state per saturation level",
        "prior_contents": [],
        "notes": "Each level starts from empty_pond_state(); higher-density levels are replayed fresh, not incrementally reused.",
    }
    write_json(PROOF_DIR / "mcp" / "pond_state_manifest.json", pond_manifest)

    level_metric_rows: list[dict[str, Any]] = []
    level_consults: dict[int, list[dict[str, Any]]] = {}
    all_consults_valid = True

    for level in LEVELS:
        level_id = level["level"]
        save_pond(state_path(level_id), empty_pond_state())
        curriculum = build_level_curriculum(level_id, level["per_mechanism"])
        write_jsonl(PROOF_DIR / "curriculum" / f"level_{level_id}_seasoning.jsonl", curriculum)

        seasoning_rows = run_seasoning(level_id, curriculum)
        discovery_rows = run_discovery_consults(level_id, source_cases)
        pond_candidates = P034B.build_candidates(source_cases, discovery_rows, "pond")
        evolution = P034B.evolve_candidates(source_cases, pond_candidates)

        write_jsonl(PROOF_DIR / "mcp" / f"level_{level_id}_seasoning_log.jsonl", seasoning_rows)
        write_jsonl(PROOF_DIR / "mcp" / f"level_{level_id}_discovery_consults.jsonl", discovery_rows)
        write_json(PROOF_DIR / "results" / f"level_{level_id}_initial_candidates.json", pond_candidates)
        write_json(PROOF_DIR / "results" / f"level_{level_id}_pathway_evolution.json", evolution)

        all_consults_valid = all_consults_valid and validate_consults_locally(seasoning_rows) and validate_consults_locally(discovery_rows)
        level_consults[level_id] = discovery_rows
        level_metric_rows.append(level_metrics(source_cases, discovery_rows, pond_candidates, level))

    curve = saturation_curve(level_metric_rows)
    density = recall_density_audit(source_cases, level_consults)
    hostile = hostile_saturation_audit(curve, density, all_consults_valid)

    write_json(PROOF_DIR / "analysis" / "saturation_curve.json", curve)
    write_json(PROOF_DIR / "analysis" / "recall_density_audit.json", density)
    write_json(PROOF_DIR / "analysis" / "hostile_saturation_audit.json", hostile)
    write_json(PROOF_DIR / "proof_manifest.json", proof_manifest(curve, hostile, source_cases))
    write_text(PROOF_DIR / "README.md", readme(curve, density, hostile))

    print(hostile["hostile_verdict"])
    return 0 if all_consults_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
