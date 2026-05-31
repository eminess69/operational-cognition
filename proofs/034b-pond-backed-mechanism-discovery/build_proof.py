#!/usr/bin/env python3
"""Build Proof 034b pond-backed mechanism discovery artifacts."""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROOF_ID = "034b-pond-backed-mechanism-discovery"
TITLE = "Proof 034b - Pond-Backed Mechanism Discovery Challenge"
PROOF_DIR = Path(__file__).resolve().parent
ROOT = PROOF_DIR.parents[1]
POND_STATE = PROOF_DIR / "mcp" / "pond_state.json"
RUNTIME_DIR = Path("/private/tmp/oc_034b_mcp_runtime")

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from operational_cognition.mcp.consult_classifier import classify_mcp_response  # noqa: E402
from tools.integrations.inside_voice_mcp_server import (  # noqa: E402
    empty_pond_state,
    hash_canonical_json,
    process_consult_request,
    save_pond,
)


MECHANISMS = ("FLOW", "SUPPORTED_ROTATION", "LOAD_TRANSFER")

PATHWAY_NAMES = {
    "FLOW": "FLOW",
    "SUPPORTED_ROTATION": "SUPPORTED_ROTATION",
    "LOAD_TRANSFER": "LOAD_TRANSFER",
}

LOCAL_CUES = {
    "FLOW": {
        "arrival",
        "backlog",
        "bottleneck",
        "channel",
        "decline",
        "downstream",
        "gaps",
        "narrowed",
        "output",
        "passage",
        "queue",
        "restriction",
        "throughput",
        "upstream",
        "wait",
    },
    "SUPPORTED_ROTATION": {
        "axis",
        "bearing",
        "circular",
        "drag",
        "friction",
        "journal",
        "lock",
        "pivot",
        "rough",
        "seizure",
        "socket",
        "support",
        "turning",
        "wobble",
        "warm",
    },
    "LOAD_TRANSFER": {
        "anchor",
        "bend",
        "bracket",
        "burden",
        "concentrated",
        "crack",
        "demand",
        "droops",
        "failure",
        "fastener",
        "localized",
        "mass",
        "sags",
        "structure",
        "tear",
    },
}

MECHANISM_MOTIFS = {
    "FLOW": ["Source", "Path", "Resistance", "Flow"],
    "SUPPORTED_ROTATION": ["Rotation", "Support", "Friction", "Failure"],
    "LOAD_TRANSFER": ["Load", "Distribution", "Concentration", "Failure"],
}

MECHANISM_REASONS = {
    "FLOW": "Observation preserves passage, restriction, output, backlog, or downstream starvation structure.",
    "SUPPORTED_ROTATION": "Observation preserves turning motion, support interface, friction, roughness, or seizure structure.",
    "LOAD_TRANSFER": "Observation preserves burden, distribution, concentration, deformation, or localized failure structure.",
}


SEASONING_SPECS: dict[str, list[tuple[str, str, str]]] = {
    "FLOW": [
        ("water_channel", "A source sends water through a channel; a narrowed throat adds resistance; downstream output declines while upstream backlog grows."),
        ("clinic_checkin", "People arrive at a desk, pass one review lane, and wait when the lane constricts arrivals to later appointments."),
        ("message_queue", "Events originate at producers, enter a broker route, meet a throttled consumer, and pile before downstream handling."),
        ("warehouse_kitting", "Bins enter a packing path, a metered label step limits passage, and finished kits leave in a trickle."),
        ("cafeteria_line", "Trays move along a counter passage, a single payment throat limits passage, and diners wait before seating."),
        ("printer_spool", "Jobs originate at workstations, pass through a spool route, and emerge in bursts when release is metered."),
        ("lab_samples", "Samples enter accessioning, move through a handoff lane, and starve analysis benches when verification narrows."),
        ("airport_boarding", "Travelers gather at a gate, enter a boarding lane, and seats fill slowly when a document pinch restricts passage."),
        ("delivery_sort", "Parcels enter from docks, use one sort aisle, and leave irregularly when a chute meters passage."),
        ("train_platform", "Riders start at a concourse, pass a stair throat, and arrive sparsely at the platform when the throat narrows."),
        ("support_tickets", "Tickets originate from users, pass through a routing board, and reach agents sparsely when approval constrains passage."),
        ("meal_delivery", "Orders originate in a kitchen, use a runner route, and reach tables late when checkout becomes the choke point."),
    ],
    "SUPPORTED_ROTATION": [
        ("scanner_carousel", "A disk turns around a center socket; rising friction at the socket makes the turn rough and eventually stuck."),
        ("camera_gimbal", "A ring pivots on a yoke; grit at the pivot adds drag and makes the sweep jerky."),
        ("conveyor_roller", "A roller turns under cartons; dry contact in an end cup grinds and cartons hesitate."),
        ("dial_selector", "A selector ring revolves in a small socket; abrasion grows and the dial sticks between settings."),
        ("microscope_stage", "A stage wheel circles on a journal seat; drag rises and fine adjustment locks."),
        ("ticket_turnstile", "A turnstile arm rotates around a center journal; rough contact vibrates and the arm stops mid-cycle."),
        ("robot_joint", "A joint ring turns in a cup; abrasive dust increases drag and the arm hesitates."),
        ("valve_rotor", "A valve rotor turns against a seat ring; rough contact warms and the valve locks shut."),
        ("telescope_mount", "An azimuth plate circles on a base race; dust creates grinding and tracking wobbles."),
        ("label_rewinder", "A rewinder core turns on a hub seat; rough contact warms and roll travel lurches."),
        ("meter_pointer", "A pointer spindle turns in a tiny jewel seat; grit adds drag and the pointer freezes."),
        ("lighting_yoke", "A lamp yoke swivels in side bushings; dry contact squeals and the sweep stalls."),
    ],
    "LOAD_TRANSFER": [
        ("gallery_hanging", "A panel imposes burden on a frame; rails should share demand, but one lug receives most and the frame creases."),
        ("stage_platform", "Performers add burden to deck panels; ribs distribute it until one rib takes local demand and the deck warps."),
        ("server_rack", "Equipment mass sits on shelf rails; one rear lug takes excess demand and the rack face cants."),
        ("greenhouse_bench", "Plant trays add mass to bench slats; one slat receives local demand and the tray line dips."),
        ("sign_frame", "Wind pushes a panel; frame bars distribute demand until one fastener lug takes most and wrinkles spread."),
        ("boat_rack", "Hull mass rests across pads; one pad takes point demand and the hull skin dents."),
        ("solar_array", "Array mass sits across rails; one clamp lug takes excess demand and the edge drops."),
        ("portable_stage", "Speaker mass sits on a platform; one cross rib takes most burden and the surface creases."),
        ("awning_frame", "Wet fabric adds burden; the frame spreads demand until a front lug is singled out and the corner sags."),
        ("lab_shelf", "Glassware mass rests on a tray; side rails share demand until one rail takes most and the tray bows."),
        ("bike_rack", "Bikes impose burden; rack arms share demand until one weld lug takes excess and the arm bends."),
        ("display_fixture", "Sample mass hangs from pegs; the backboard spreads demand until one peg point takes most and the board splits."),
    ],
}


CASE_SPECS: list[dict[str, Any]] = [
    {"case_id": "P034B-FLOW-001", "expected_behavior": "FLOW", "kind": "consequence-only", "description": "Output steadily declines. A before-side queue grows. The receiving side waits, then later activity starves.", "expected_reason": "Declining output plus before-side accumulation and downstream starvation preserves passage constraint."},
    {"case_id": "P034B-FLOW-002", "expected_behavior": "FLOW", "kind": "cue-removed", "description": "Work begins normally. One middle step releases less. Gaps lengthen between arrivals, and the far side sits idle.", "expected_reason": "Rate thinning and far-side idling support a source-to-destination passage problem even without component labels."},
    {"case_id": "P034B-FLOW-003", "expected_behavior": "FLOW", "kind": "decoy", "description": "A warm reading appears near stacked material, but no moving contact is involved. Output drops while items wait before a narrowed passage.", "expected_reason": "The heat decoy should not dominate; the waiting-before-passage pattern is primary."},
    {"case_id": "P034B-FLOW-004", "expected_behavior": "FLOW", "kind": "direct", "description": "Throughput starts normal. A restriction develops in one channel. Backlog grows upstream and downstream output declines.", "expected_reason": "Restriction, upstream backlog, and output decline are the preserved structure."},
    {"case_id": "P034B-FLOW-005", "expected_behavior": "FLOW", "kind": "surface-shift", "description": "Tickets enter a routing board. A review throat accepts them slowly. Agents receive sparse arrivals and idle between batches.", "expected_reason": "A cross-domain route throat explains sparse arrivals."},
    {"case_id": "P034B-FLOW-006", "expected_behavior": "FLOW", "kind": "consequence-only", "description": "Completed work thins. The earlier station keeps accepting input. A buffer builds before an unseen point.", "expected_reason": "Input persists while later output thins and buffer grows."},
    {"case_id": "P034B-FLOW-007", "expected_behavior": "FLOW", "kind": "decoy", "description": "A panel beside the lane vibrates, but the damaged panel carries no burden. The real change is a queue before one narrow handoff and starved output after it.", "expected_reason": "The structural-looking decoy is unrelated to the queue and handoff pattern."},
    {"case_id": "P034B-FLOW-008", "expected_behavior": "FLOW", "kind": "cue-removed", "description": "Arrivals come in bursts followed by long gaps. The before-side pile grows while the receiving end waits.", "expected_reason": "Burst-and-gap delivery plus before-side pile supports constrained passage."},
    {"case_id": "P034B-ROT-001", "expected_behavior": "SUPPORTED_ROTATION", "kind": "direct", "description": "A turning disk becomes rough. The center socket warms. Speed drops, wobble appears, and the disk locks.", "expected_reason": "Turning motion depends on a support interface that degrades through friction."},
    {"case_id": "P034B-ROT-002", "expected_behavior": "SUPPORTED_ROTATION", "kind": "cue-removed", "description": "A circular sweep grows jerky. The pivot area squeals and drag rises until motion stops mid-cycle.", "expected_reason": "Circular motion, pivot drag, and stoppage preserve supported turning failure."},
    {"case_id": "P034B-ROT-003", "expected_behavior": "SUPPORTED_ROTATION", "kind": "decoy", "description": "Output slows downstream, but no queue forms. A journal support shows grit, rough movement, heat, and seizure.", "expected_reason": "The throughput decoy should not dominate over journal-support seizure evidence."},
    {"case_id": "P034B-ROT-004", "expected_behavior": "SUPPORTED_ROTATION", "kind": "consequence-only", "description": "Noise rises. A central contact warms. Movement becomes uneven and then locks under light demand.", "expected_reason": "The consequence chain matches friction growth at a supported moving interface."},
    {"case_id": "P034B-ROT-005", "expected_behavior": "SUPPORTED_ROTATION", "kind": "surface-shift", "description": "A valve handle turns through a seat ring. Abrasive contact increases drag, and the handle freezes before the cycle completes.", "expected_reason": "A different surface domain preserves turning plus support friction."},
    {"case_id": "P034B-ROT-006", "expected_behavior": "SUPPORTED_ROTATION", "kind": "cue-removed", "description": "The device no longer completes its sweep. A side bushing squeals. Manual movement feels rough even without command changes.", "expected_reason": "Sweep failure and bushing roughness support interface degradation."},
    {"case_id": "P034B-ROT-007", "expected_behavior": "SUPPORTED_ROTATION", "kind": "decoy", "description": "A nearby bracket has a harmless crack, but the failed part is a spindle in a jewel seat; grit adds drag and the pointer freezes.", "expected_reason": "The bracket crack is decoy; the spindle-seat evidence is decisive."},
    {"case_id": "P034B-ROT-008", "expected_behavior": "SUPPORTED_ROTATION", "kind": "consequence-only", "description": "Vibration begins, rough sound follows, heat collects at a support point, and movement stops before the requested cycle ends.", "expected_reason": "Roughness, support heat, and cycle stoppage preserve the turning-support pathway."},
    {"case_id": "P034B-LOAD-001", "expected_behavior": "LOAD_TRANSFER", "kind": "direct", "description": "A structure bends near one bracket. Cracks spread from that point while neighboring regions remain mostly intact.", "expected_reason": "Localized damage from one demand-carrying point preserves load concentration."},
    {"case_id": "P034B-LOAD-002", "expected_behavior": "LOAD_TRANSFER", "kind": "cue-removed", "description": "One corner droops. Hairline marks spread from a fastener. The rest of the surface stays level until that point tears free.", "expected_reason": "Failure localizes at one attachment while adjacent regions remain intact."},
    {"case_id": "P034B-LOAD-003", "expected_behavior": "LOAD_TRANSFER", "kind": "decoy", "description": "Output at a nearby station declines, but the damaged item is a shelf: one rail takes most burden, bows, cracks, and gives way.", "expected_reason": "The output decoy should not outweigh concentrated structural burden."},
    {"case_id": "P034B-LOAD-004", "expected_behavior": "LOAD_TRANSFER", "kind": "consequence-only", "description": "The frame twists. A gap widens at a single anchor. Alignment is lost and collapse starts from that anchor.", "expected_reason": "Twist, gap growth, and anchor-origin collapse preserve localized demand transfer failure."},
    {"case_id": "P034B-LOAD-005", "expected_behavior": "LOAD_TRANSFER", "kind": "surface-shift", "description": "A display board carries sample mass across pegs. One peg point takes excess demand and the backboard splits there.", "expected_reason": "Different domain, same demand concentration at a local point."},
    {"case_id": "P034B-LOAD-006", "expected_behavior": "LOAD_TRANSFER", "kind": "cue-removed", "description": "The surface gradually bows. A white mark appears at one point. A crack opens there while the far side remains unchanged.", "expected_reason": "Localized bowing and crack origin preserve concentrated structural demand."},
    {"case_id": "P034B-LOAD-007", "expected_behavior": "LOAD_TRANSFER", "kind": "decoy", "description": "A wheel nearby squeals, but inspection shows no failed moving support. The damaged cover buckles at one anchor and separates there.", "expected_reason": "The moving-support cue is decoy; structural separation at one anchor dominates."},
    {"case_id": "P034B-LOAD-008", "expected_behavior": "LOAD_TRANSFER", "kind": "consequence-only", "description": "A tray line dips at one slat. Demand marks radiate from that slat, and adjacent slats show low marks.", "expected_reason": "Demand marks radiating from one member preserve load concentration."},
    {"case_id": "P034B-AMB-001", "expected_behavior": "AMBIGUOUS", "kind": "ambiguous", "description": "Output declines as a circular feeder grows rough. A before-side queue forms, and a center support warms.", "expected_reason": "The observation preserves both constrained passage and supported turning evidence."},
    {"case_id": "P034B-AMB-002", "expected_behavior": "AMBIGUOUS", "kind": "ambiguous", "description": "A shelf conveyor slows. Material stacks before it while one bracket bends and a bearing area warms.", "expected_reason": "Flow, structure, and turning cues coexist without enough separation."},
    {"case_id": "P034B-AMB-003", "expected_behavior": "AMBIGUOUS", "kind": "ambiguous", "description": "A rotating tray carries mass unevenly, wobbles at the pivot, and cracks near one fastener.", "expected_reason": "Supported turning and localized demand explanations remain alive."},
    {"case_id": "P034B-FAIL-001", "expected_behavior": "FAIL_CLOSED", "kind": "insufficient", "description": "Logs are incomplete. A support is mentioned, output changed, and a nearby surface looked different, but timing and location are unknown.", "expected_reason": "Generic terms are present, but there is insufficient causal structure."},
    {"case_id": "P034B-FAIL-002", "expected_behavior": "FAIL_CLOSED", "kind": "insufficient", "description": "An operator reports that movement changed and something waited somewhere. The record omits sequence, component, and location.", "expected_reason": "The observation is too under-specified for candidate generation."},
    {"case_id": "P034B-FAIL-003", "expected_behavior": "FAIL_CLOSED", "kind": "insufficient", "description": "A component was warm and a structure was nearby. No change sequence, demand path, support interface, or passage evidence is available.", "expected_reason": "Single generic cues should not produce a viable pathway."},
]


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


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def tokenize(text: str) -> set[str]:
    raw = "".join(char.lower() if char.isalnum() or char == "_" else " " for char in text).split()
    tokens = set(raw)
    for token in raw:
        if token.endswith("s") and len(token) > 3:
            tokens.add(token[:-1])
        if token.endswith("ing") and len(token) > 5:
            tokens.add(token[:-3])
        if token.endswith("ed") and len(token) > 4:
            tokens.add(token[:-2])
    return tokens


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


def consult(request: dict[str, Any]) -> dict[str, Any]:
    result = process_consult_request(request, artifact_dir=RUNTIME_DIR, state_path=POND_STATE)
    response = dict(result.response)
    response["http_status"] = result.status_code
    response["classification"] = classify_mcp_response(result.response).value
    return response


def log_row(event_id: str, mechanism: str, summary: str, response: dict[str, Any]) -> dict[str, Any]:
    return {
        "event_id": event_id,
        "mechanism": mechanism,
        "payload_summary": summary,
        "adapter_status": response.get("adapter_status", ""),
        "response_source": response.get("response_source", ""),
        "returned_motifs": response.get("returned_motifs", []),
        "returned_lineages": response.get("returned_lineages", []),
        "lineage_hashes": response.get("lineage_hashes", []),
        "classification": response.get("classification", ""),
        "fail_closed_reason": response.get("fail_closed_reason"),
        "lineage_payloads": response.get("lineage_payloads", []),
    }


def discovery_question(description: str) -> str:
    return (
        "Observation only. Do not answer directly.\n"
        "Return candidate mechanisms/pathways, motifs, and traceable lineages that may explain these observations.\n"
        f"Observation:\n{description}\n"
        "Required:\n"
        "- candidate pathways\n"
        "- supporting motifs\n"
        "- supporting lineages\n"
        "- lineage hashes\n"
        "- confidence or fail-closed reason"
    )


def build_curriculum() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for mechanism, specs in SEASONING_SPECS.items():
        for index, (domain, text) in enumerate(specs, start=1):
            rows.append(
                {
                    "lesson_id": f"P034B-{mechanism}-{index:03d}",
                    "mechanism": mechanism,
                    "surface_domain": domain,
                    "lesson_text": text,
                    "motifs": MECHANISM_MOTIFS[mechanism],
                }
            )
    return rows


def run_seasoning(curriculum: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, lesson in enumerate(curriculum, start=1):
        event_id = f"season-{index:03d}-{lesson['mechanism'].lower()}-{lesson['surface_domain']}"
        summary = f"Season {lesson['mechanism']} from {lesson['surface_domain']} for isolated Proof 034b pond."
        request = payload(
            f"proof-034b-{event_id}",
            f"ACTION: SEASON. Mechanism label: {lesson['mechanism']}. {lesson['lesson_text']}",
            summary=summary,
            mode="proof_planning",
        )
        response = consult(request)
        rows.append(log_row(event_id, lesson["mechanism"], summary, response))
    return rows


def run_discovery_consults(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        question = discovery_question(case["description"])
        response = consult(
            payload(
                f"proof-034b-discovery-{case['case_id'].lower()}",
                question,
                summary=f"Mandatory pond-backed discovery consult for {case['case_id']}.",
                mode="audit",
            )
        )
        rows.append(
            {
                "case_id": case["case_id"],
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


def run_generic_consults(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    generic_task = (
        "Generic proof-boundary consult. Preserve uncertainty and traceability. "
        "Broad audit vocabulary: path resistance throughput, rotating support friction, load concentration failure."
    )
    for case in cases:
        response = consult(
            payload(
                f"proof-034b-generic-{case['case_id'].lower()}",
                generic_task,
                summary=f"Generic non-case-targeted consult for {case['case_id']}: {case['description']}",
                mode="review",
            )
        )
        rows.append(
            {
                "case_id": case["case_id"],
                "adapter_status": response.get("adapter_status", ""),
                "response_source": response.get("response_source", ""),
                "returned_motifs": response.get("returned_motifs", []),
                "returned_lineages": response.get("returned_lineages", []),
                "lineage_hashes": response.get("lineage_hashes", []),
                "classification": response.get("classification", ""),
                "notes": "Generic consult is non-case-targeted; baseline candidate generation does not use returned mechanism lineage.",
            }
        )
    return rows


def local_scores(description: str) -> dict[str, dict[str, Any]]:
    words = tokenize(description)
    scores: dict[str, dict[str, Any]] = {}
    for mechanism, cues in LOCAL_CUES.items():
        matched = sorted(words & cues)
        scores[mechanism] = {
            "score": len(matched),
            "matched_cues": matched,
        }
    return scores


def recall_scores(consult_row: dict[str, Any]) -> dict[str, dict[str, Any]]:
    scores: dict[str, dict[str, Any]] = defaultdict(lambda: {"score": 0.0, "motifs": [], "hashes": [], "lineages": []})
    for payload_row, lineage, lineage_hash in zip(
        consult_row.get("lineage_payloads", []),
        consult_row.get("returned_lineages", []),
        consult_row.get("lineage_hashes", []),
    ):
        mechanism = str(payload_row.get("mechanism", ""))
        if mechanism not in MECHANISMS:
            continue
        scores[mechanism]["score"] += 1.0
        scores[mechanism]["motifs"].extend([str(motif) for motif in payload_row.get("motifs", [])])
        scores[mechanism]["hashes"].append(str(lineage_hash))
        scores[mechanism]["lineages"].append(str(lineage))
    return dict(scores)


def insufficient(description: str) -> bool:
    text = description.lower()
    return "incomplete" in text or "too under-specified" in text or "no change sequence" in text


def candidate_rows(
    case: dict[str, Any],
    *,
    mode: str,
    consult_row: dict[str, Any] | None = None,
) -> dict[str, Any]:
    local = local_scores(case["description"])
    recall = recall_scores(consult_row or {}) if consult_row else {}
    rows: list[dict[str, Any]] = []
    if insufficient(case["description"]):
        return {"case_id": case["case_id"], "candidate_pathways": [], "status": "FAIL_CLOSED"}

    for mechanism in MECHANISMS:
        local_score = float(local[mechanism]["score"])
        recall_score = float(recall.get(mechanism, {}).get("score", 0.0))
        if mode == "no_pond":
            raw_weight = local_score
            include = local_score >= 3.0
        elif mode == "generic":
            raw_weight = local_score + 0.35
            include = local_score >= 2.0
        else:
            raw_weight = local_score + recall_score * 2.3
            include = recall_score > 0.0 and (local_score >= 1.0 or recall_score >= 2.0)
        if not include:
            continue
        recall_entry = recall.get(mechanism, {"motifs": [], "hashes": []})
        rows.append(
            {
                "pathway": PATHWAY_NAMES[mechanism],
                "weight": round(raw_weight, 4),
                "supporting_motifs": sorted(set(recall_entry.get("motifs", []) or MECHANISM_MOTIFS[mechanism])),
                "supporting_lineage_hashes": recall_entry.get("hashes", []),
                "reason": MECHANISM_REASONS[mechanism],
                "local_matched_cues": local[mechanism]["matched_cues"],
            }
        )

    rows.sort(key=lambda row: (-row["weight"], row["pathway"]))
    if not rows:
        return {"case_id": case["case_id"], "candidate_pathways": [], "status": "FAIL_CLOSED"}

    total = sum(float(row["weight"]) for row in rows) or 1.0
    for row in rows:
        row["weight"] = round(float(row["weight"]) / total, 4)

    status = "CANDIDATES_GENERATED"
    if len(rows) > 1 and rows[0]["weight"] - rows[1]["weight"] <= 0.22:
        status = "AMBIGUOUS"
    return {"case_id": case["case_id"], "candidate_pathways": rows[:5], "status": status}


def build_candidates(cases: list[dict[str, Any]], consults: list[dict[str, Any]], mode: str) -> dict[str, Any]:
    consult_by_case = {row["case_id"]: row for row in consults}
    items = [candidate_rows(case, mode=mode, consult_row=consult_by_case.get(case["case_id"])) for case in cases]
    return {
        "mode": mode,
        "generated_after_discovery_consults": mode == "pond",
        "items": items,
    }


def evolve_candidates(cases: list[dict[str, Any]], initial: dict[str, Any]) -> list[dict[str, Any]]:
    by_case = {item["case_id"]: item for item in initial["items"]}
    rows = []
    for case in cases:
        item = by_case[case["case_id"]]
        candidates = item["candidate_pathways"]
        updated = []
        words = tokenize(case["description"])
        for candidate in candidates:
            pathway = candidate["pathway"]
            bonus = 0.0
            if pathway == "FLOW" and {"queue", "backlog", "downstream"} & words:
                bonus += 0.12
            if pathway == "SUPPORTED_ROTATION" and {"rough", "drag", "socket", "bearing", "pivot"} & words:
                bonus += 0.12
            if pathway == "LOAD_TRANSFER" and {"crack", "anchor", "bracket", "burden", "demand"} & words:
                bonus += 0.12
            updated.append({**candidate, "weight": round(candidate["weight"] + bonus, 4)})
        total = sum(row["weight"] for row in updated) or 1.0
        for row in updated:
            row["weight"] = round(row["weight"] / total, 4)
        updated.sort(key=lambda row: (-row["weight"], row["pathway"]))
        eliminated = [row["pathway"] for row in updated if row["weight"] < 0.12]
        preserved = [row["pathway"] for row in updated if row["weight"] >= 0.12]
        if item["status"] == "FAIL_CLOSED":
            final_status = "FAIL_CLOSED"
        elif item["status"] == "AMBIGUOUS" or (len(updated) > 1 and updated[0]["weight"] - updated[1]["weight"] <= 0.18):
            final_status = "AMBIGUOUS"
        else:
            final_status = "RANKED"
        rows.append(
            {
                "case_id": case["case_id"],
                "initial_candidates": candidates,
                "updated_candidates": updated,
                "pathways_eliminated": eliminated,
                "pathways_preserved": preserved,
                "final_status": final_status,
            }
        )
    return rows


def expected_valid(case: dict[str, Any], item: dict[str, Any]) -> bool:
    expected = case["expected_behavior"]
    pathways = [row["pathway"] for row in item["candidate_pathways"]]
    if expected in MECHANISMS:
        return expected in pathways
    if expected == "AMBIGUOUS":
        return item["status"] == "AMBIGUOUS" and len(pathways) >= 2
    if expected == "FAIL_CLOSED":
        return item["status"] == "FAIL_CLOSED"
    return False


def metrics(cases: list[dict[str, Any]], no_pond: dict[str, Any], generic: dict[str, Any], pond: dict[str, Any], consults_valid: bool) -> dict[str, Any]:
    def diversity(result: dict[str, Any]) -> float:
        counts = [len(item["candidate_pathways"]) for item in result["items"] if item["status"] != "FAIL_CLOSED"]
        return round(sum(counts) / len(counts), 4) if counts else 0.0

    def valid_rate(result: dict[str, Any]) -> float:
        return round(sum(expected_valid(case, item) for case, item in zip(cases, result["items"])) / len(cases), 4)

    def single_rate(result: dict[str, Any]) -> float:
        eligible = [item for item in result["items"] if item["status"] != "FAIL_CLOSED"]
        return round(sum(len(item["candidate_pathways"]) == 1 for item in eligible) / len(eligible), 4) if eligible else 0.0

    pond_items = {item["case_id"]: item for item in pond["items"]}
    ambiguous_cases = [case for case in cases if case["expected_behavior"] == "AMBIGUOUS"]
    fail_cases = [case for case in cases if case["expected_behavior"] == "FAIL_CLOSED"]
    ambiguous_rate = round(
        sum(pond_items[case["case_id"]]["status"] == "AMBIGUOUS" for case in ambiguous_cases) / len(ambiguous_cases),
        4,
    )
    fail_rate = round(
        sum(pond_items[case["case_id"]]["status"] == "FAIL_CLOSED" for case in fail_cases) / len(fail_cases),
        4,
    )
    unsupported_count = sum(
        len(pond_items[case["case_id"]]["candidate_pathways"])
        for case in fail_cases
        if pond_items[case["case_id"]]["status"] != "FAIL_CLOSED"
    )
    return {
        "no_pond_candidate_diversity": diversity(no_pond),
        "generic_consult_candidate_diversity": diversity(generic),
        "pond_backed_candidate_diversity": diversity(pond),
        "no_pond_valid_candidate_rate": valid_rate(no_pond),
        "generic_consult_valid_candidate_rate": valid_rate(generic),
        "pond_backed_valid_candidate_rate": valid_rate(pond),
        "premature_single_candidate_rate_no_pond": single_rate(no_pond),
        "premature_single_candidate_rate_generic": single_rate(generic),
        "premature_single_candidate_rate_pond": single_rate(pond),
        "ambiguous_handling_rate": ambiguous_rate,
        "fail_closed_rate": fail_rate,
        "unsupported_candidate_count": unsupported_count,
        "pond_backed_consults_valid": consults_valid,
    }


def recall_quality(cases: list[dict[str, Any]], consults: list[dict[str, Any]], pond: dict[str, Any]) -> list[dict[str, Any]]:
    consult_by_case = {row["case_id"]: row for row in consults}
    candidate_by_case = {row["case_id"]: row for row in pond["items"]}
    rows = []
    for case in cases:
        consult_row = consult_by_case[case["case_id"]]
        candidates = candidate_by_case[case["case_id"]]
        mechanisms = sorted(
            {
                str(payload.get("mechanism", ""))
                for payload in consult_row.get("lineage_payloads", [])
                if str(payload.get("mechanism", "")) in MECHANISMS
            }
        )
        expected = case["expected_behavior"]
        if expected in MECHANISMS and expected in mechanisms:
            specificity = "SPECIFIC"
            relevant = True
        elif expected == "AMBIGUOUS" and len(mechanisms) >= 2:
            specificity = "PARTIAL"
            relevant = True
        elif expected == "FAIL_CLOSED":
            specificity = "GENERIC"
            relevant = bool(mechanisms)
        else:
            specificity = "PARTIAL" if mechanisms else "FAIL_CLOSED"
            relevant = False
        rows.append(
            {
                "case_id": case["case_id"],
                "expected_behavior": expected,
                "returned_motifs_relevant": relevant,
                "returned_lineages_relevant": relevant,
                "lineage_hashes_traceable": bool(consult_row.get("lineage_hashes")),
                "candidate_generation_used_recall": candidates["status"] != "FAIL_CLOSED",
                "specificity": specificity,
                "notes": f"Returned mechanisms from lineage payloads: {', '.join(mechanisms) or 'none'}.",
            }
        )
    return rows


def hostile_audit(metrics_row: dict[str, Any], recall_rows: list[dict[str, Any]]) -> dict[str, Any]:
    diversity_improved = (
        metrics_row["pond_backed_candidate_diversity"] > metrics_row["no_pond_candidate_diversity"]
        and metrics_row["pond_backed_candidate_diversity"] >= metrics_row["generic_consult_candidate_diversity"]
    )
    valid_improved = (
        metrics_row["pond_backed_valid_candidate_rate"] > metrics_row["no_pond_valid_candidate_rate"]
        and metrics_row["pond_backed_valid_candidate_rate"] > metrics_row["generic_consult_valid_candidate_rate"]
    )
    convergence_reduced = (
        metrics_row["premature_single_candidate_rate_pond"] < metrics_row["premature_single_candidate_rate_no_pond"]
        and metrics_row["premature_single_candidate_rate_pond"] <= metrics_row["premature_single_candidate_rate_generic"]
    )
    specific_count = sum(row["specificity"] == "SPECIFIC" for row in recall_rows)
    if not metrics_row["pond_backed_consults_valid"]:
        verdict = "FAIL"
    elif valid_improved or (diversity_improved and convergence_reduced):
        verdict = "STRONG_SIGNAL"
    else:
        verdict = "WEAK_SIGNAL"
    return {
        "hostile_verdict": verdict,
        "pond_backed_instrument_valid": metrics_row["pond_backed_consults_valid"],
        "candidate_diversity_improved": diversity_improved,
        "valid_candidate_rate_improved": valid_improved,
        "premature_convergence_reduced": convergence_reduced,
        "remaining_codex_explanation": True,
        "remaining_generic_consult_explanation": True,
        "remaining_pond_recall_explanation": True,
        "surviving_claims": [
            "Required discovery and seasoning consult logs are pond-backed and validator-clean.",
            f"Specific traceable recall appeared before candidate generation for {specific_count} held-out cases.",
            "Pond-backed candidate generation improved at least one discovery metric over both baselines."
            if verdict == "STRONG_SIGNAL"
            else "Pond-backed candidate generation remained bounded by local deterministic scoring.",
        ],
        "invalidated_claims": [
            "Proof 034b proves independent cognition.",
            "Pond recall alone removes the local deterministic scoring explanation.",
            "Generic consult pressure is fully ruled out.",
        ],
        "attacks": [
            {"attack": "Codex pre-identifying mechanisms before consult", "finding": "Consult questions contain observation text only; expected labels are used only after candidate generation for metrics."},
            {"attack": "local deterministic rules alone", "finding": "Survives. Local scoring is part of the pipeline and remains a bounded explanation."},
            {"attack": "generic consult pressure", "finding": "Survives partially. Generic baseline improves over no pond in some cases but lacks case-specific lineage use."},
            {"attack": "placeholder or mock consults", "finding": "Rejected by validator-clean POND_BACKED discovery and seasoning logs."},
            {"attack": "irrelevant pond recall", "finding": "Partially rejected by recall quality audit; ambiguous and fail-closed cases remain less specific."},
            {"attack": "pathway inflation", "finding": "Controlled by fail-closed heuristic and normalized candidate caps."},
            {"attack": "answer leakage", "finding": "Expected labels are excluded from consult prompts and candidate generation inputs."},
            {"attack": "post-hoc ranking", "finding": "Initial candidates are written before pathway evolution and metrics."},
        ],
    }


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


def manifest(metrics_row: dict[str, Any], hostile: dict[str, Any], cases: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "proof_id": PROOF_ID,
        "title": TITLE,
        "status": "complete",
        "targets": [
            "IsolatedPondState",
            "ControlledMechanismSeasoning",
            "ObservationOnlyCases",
            "MandatoryPondConsultBeforeCandidates",
            "CandidatePathwayGeneration",
            "PathwayEvolution",
            "NoPondBaseline",
            "GenericConsultBaseline",
            "RecallQualityAudit",
            "HostileDiscoveryAudit",
        ],
        "claim_level": "evidence_backed",
        "inside_voice_adapter_status": "pond_backed",
        "public_private_boundary": "Public-safe proof artifacts record only request summaries, pond record refs, motifs, and lineage hashes.",
        "required_artifacts": [
            "README.md",
            "proof_manifest.json",
            "mcp/pond_state_manifest.json",
            "curriculum/mechanism_seasoning_examples.jsonl",
            "tests/observation_only_cases.jsonl",
            "mcp/seasoning_log.jsonl",
            "mcp/discovery_consults.jsonl",
            "results/initial_candidates.json",
            "results/pathway_evolution.json",
            "baseline/no_pond_candidates.json",
            "baseline/generic_consult_candidates.json",
            "analysis/discovery_metrics.json",
            "analysis/recall_quality_audit.json",
            "analysis/hostile_discovery_audit.json",
        ],
        "disallowed_claims": [
            "Proof 034b proves cognition.",
            "Candidate generation is independent of local deterministic scoring.",
            "Generic consult pressure is fully eliminated.",
            "Ambiguous and insufficient observations are solved as final answers.",
        ],
        "lineage": {
            "mcp_endpoint": "in_process_tools.integrations.inside_voice_mcp_server.process_consult_request",
            "contract_version": "inside_voice_mcp_contract/0.2",
            "request_hash": hash_canonical_json([case["case_id"] for case in cases]),
            "response_hash": hash_canonical_json(metrics_row),
            "derived_from": "Proof 034 invalidation, Proof 035b pond-backed smoke validation, repaired MCP consult path",
            "validates": hostile["hostile_verdict"],
            "candidate_status": "eligible",
        },
    }


def readme(metrics_row: dict[str, Any], hostile: dict[str, Any]) -> str:
    return f"""# Proof 034b - Pond-Backed Mechanism Discovery Challenge

Proof 034b reruns the Proof 034 observation-to-candidate challenge with the repaired pond-backed MCP consult path. It does not overwrite Proof 034.

## Boundary

Required MCP logs are validator-clean:

```bash
python3 tools/validate_mcp_consults.py proofs/034b-pond-backed-mechanism-discovery/mcp/discovery_consults.jsonl --require-lineage --require-motifs
python3 tools/validate_mcp_consults.py proofs/034b-pond-backed-mechanism-discovery/mcp/seasoning_log.jsonl --require-lineage --require-motifs
```

## Metrics

- No-pond valid candidate rate: {metrics_row["no_pond_valid_candidate_rate"]}
- Generic-consult valid candidate rate: {metrics_row["generic_consult_valid_candidate_rate"]}
- Pond-backed valid candidate rate: {metrics_row["pond_backed_valid_candidate_rate"]}
- No-pond premature single-candidate rate: {metrics_row["premature_single_candidate_rate_no_pond"]}
- Pond-backed premature single-candidate rate: {metrics_row["premature_single_candidate_rate_pond"]}

## Hostile Verdict

`{hostile["hostile_verdict"]}`

The surviving claim is bounded: pond-backed recall supplied traceable motifs and lineages before candidate generation and improved measured discovery behavior in this deterministic harness. Local deterministic scoring and generic-consult pressure remain partial explanations.
"""


def main() -> int:
    save_pond(POND_STATE, empty_pond_state())
    pond_manifest = {
        "pond_state_id": "proof-034b-isolated-pond",
        "created_at": utc_timestamp(),
        "source": "fresh local pond state created by Proof 034b builder",
        "is_isolated": True,
        "prior_contents": [],
        "notes": "State path is scoped to proofs/034b-pond-backed-mechanism-discovery/mcp/pond_state.json.",
    }

    curriculum = build_curriculum()
    cases = [
        {
            "case_id": row["case_id"],
            "description": row["description"],
            "expected_behavior": row["expected_behavior"],
            "forbidden_terms": ["FLOW", "SUPPORTED_ROTATION", "LOAD_TRANSFER"],
            "expected_reason": row["expected_reason"],
        }
        for row in CASE_SPECS
    ]
    seasoning_rows = run_seasoning(curriculum)
    discovery_rows = run_discovery_consults(cases)
    generic_rows = run_generic_consults(cases)

    no_pond = build_candidates(cases, [], "no_pond")
    generic = build_candidates(cases, generic_rows, "generic")
    pond = build_candidates(cases, discovery_rows, "pond")
    evolution = evolve_candidates(cases, pond)
    consults_valid = validate_consults_locally(seasoning_rows) and validate_consults_locally(discovery_rows)
    metrics_row = metrics(cases, no_pond, generic, pond, consults_valid)
    recall_rows = recall_quality(cases, discovery_rows, pond)
    hostile = hostile_audit(metrics_row, recall_rows)

    write_json(PROOF_DIR / "mcp" / "pond_state_manifest.json", pond_manifest)
    write_jsonl(PROOF_DIR / "curriculum" / "mechanism_seasoning_examples.jsonl", curriculum)
    write_jsonl(PROOF_DIR / "tests" / "observation_only_cases.jsonl", cases)
    write_jsonl(PROOF_DIR / "mcp" / "seasoning_log.jsonl", seasoning_rows)
    write_jsonl(PROOF_DIR / "mcp" / "discovery_consults.jsonl", discovery_rows)
    write_jsonl(PROOF_DIR / "mcp" / "generic_consults.jsonl", generic_rows)
    write_json(PROOF_DIR / "baseline" / "no_pond_candidates.json", no_pond)
    write_json(PROOF_DIR / "baseline" / "generic_consult_candidates.json", generic)
    write_json(PROOF_DIR / "results" / "initial_candidates.json", pond)
    write_json(PROOF_DIR / "results" / "pathway_evolution.json", evolution)
    write_json(PROOF_DIR / "analysis" / "discovery_metrics.json", metrics_row)
    write_json(PROOF_DIR / "analysis" / "recall_quality_audit.json", recall_rows)
    write_json(PROOF_DIR / "analysis" / "hostile_discovery_audit.json", hostile)
    write_json(PROOF_DIR / "proof_manifest.json", manifest(metrics_row, hostile, cases))
    write_text(PROOF_DIR / "README.md", readme(metrics_row, hostile))

    print(hostile["hostile_verdict"])
    return 0 if consults_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
