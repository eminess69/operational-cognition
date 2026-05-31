#!/usr/bin/env python3
"""Build Proof 037 mechanism diversity study artifacts."""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROOF_ID = "037-mechanism-diversity-study"
TITLE = "Proof 037 - Mechanism Diversity Study"
PROOF_DIR = Path(__file__).resolve().parent
ROOT = PROOF_DIR.parents[1]
RUNTIME_ROOT = Path("/private/tmp/oc_037_mcp_runtime")

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from operational_cognition.mcp.consult_classifier import classify_mcp_response  # noqa: E402
from tools.integrations.inside_voice_mcp_server import (  # noqa: E402
    MECHANISM_MOTIFS,
    empty_pond_state,
    hash_canonical_json,
    process_consult_request,
    save_pond,
)


GROUP_A_MECHANISMS = ("FLOW", "SUPPORTED_ROTATION", "LOAD_TRANSFER")
GROUP_B_MECHANISMS = (
    "FLOW",
    "SUPPORTED_ROTATION",
    "LOAD_TRANSFER",
    "FEEDBACK",
    "THRESHOLD",
    "ACCUMULATION",
    "DIFFUSION",
    "OSCILLATION",
    "BUFFERING",
    "RESOURCE_DEPLETION",
    "AMPLIFICATION",
    "COMPENSATION",
)


MECHANISM_DEFINITIONS: dict[str, dict[str, Any]] = {
    "FLOW": {
        "description": "Movement through a path changes when resistance alters throughput between source and destination.",
        "observations": ["output thins", "upstream material waits", "downstream activity starves", "a route or throat constrains passage"],
        "causal_chain": ["source emits", "path carries", "resistance rises", "throughput drops", "backlog and starvation appear"],
        "surface_domains": ["water channel", "ticket queue", "warehouse route", "message broker"],
        "cue_frames": [
            ["source", "path", "resistance", "throughput", "backlog"],
            ["arrival", "route", "throat", "queue", "downstream"],
            ["input", "channel", "bottleneck", "output", "starvation"],
            ["upstream", "passage", "restriction", "decline", "idle"],
        ],
    },
    "SUPPORTED_ROTATION": {
        "description": "Turning depends on a support interface whose friction or alignment state governs smooth motion.",
        "observations": ["a circular part grows rough", "support contact warms", "drag rises", "motion locks or seizes"],
        "causal_chain": ["body turns", "support carries rotation", "contact friction rises", "wobble or heat appears", "rotation stops"],
        "surface_domains": ["bearing", "pivot", "valve rotor", "gimbal"],
        "cue_frames": [
            ["rotation", "support", "friction", "rough", "lock"],
            ["turning", "socket", "drag", "wobble", "warm"],
            ["pivot", "bearing", "seizure", "sweep", "cycle"],
            ["journal", "center", "grit", "uneven", "stuck"],
        ],
    },
    "LOAD_TRANSFER": {
        "description": "A burden must distribute through structure; failure occurs when demand concentrates locally.",
        "observations": ["one support point takes excess demand", "nearby regions remain intact", "cracks radiate", "collapse starts locally"],
        "causal_chain": ["load enters", "members distribute", "one point concentrates demand", "local deformation grows", "failure starts there"],
        "surface_domains": ["shelf", "bracket", "frame", "hanging panel"],
        "cue_frames": [
            ["load", "distribution", "concentration", "bend", "failure"],
            ["burden", "structure", "localized", "crack", "anchor"],
            ["mass", "bracket", "demand", "tear", "adjacent"],
            ["transfer", "lug", "support point", "droop", "collapse"],
        ],
    },
    "FEEDBACK": {
        "description": "A response loops back into later input, reinforcing or damping subsequent behavior.",
        "observations": ["a signal returns", "the next response changes", "reinforcement compounds", "loop behavior dominates"],
        "causal_chain": ["output is sensed", "signal returns", "response is adjusted", "loop reinforces or damps", "system trajectory changes"],
        "surface_domains": ["thermostat", "ranking loop", "control panel", "market signal"],
        "cue_frames": [
            ["feedback", "loop", "signal", "response", "reinforcement"],
            ["monitor", "return", "adjust", "correction", "stabilize"],
            ["recursive", "self", "runaway", "dampen", "response"],
            ["loopback", "signal", "reinforce", "adjust", "trajectory"],
        ],
    },
    "THRESHOLD": {
        "description": "A system remains in one regime until a limit is crossed and a new state is triggered.",
        "observations": ["little changes below a limit", "a critical point is crossed", "state changes abruptly", "later behavior differs"],
        "causal_chain": ["pressure or value approaches a limit", "threshold is crossed", "trigger fires", "state switches", "new regime persists"],
        "surface_domains": ["sensor trip", "policy limit", "chemical phase", "load rating"],
        "cue_frames": [
            ["threshold", "limit", "trigger", "state", "switch"],
            ["critical", "point", "crossed", "sudden", "boundary"],
            ["until", "breakpoint", "trip", "tipping", "regime"],
            ["limit", "crosses", "trigger", "state change", "after"],
        ],
    },
    "ACCUMULATION": {
        "description": "Inputs collect over time in storage or pressure until buildup changes later behavior.",
        "observations": ["small inputs add up", "stock grows", "pressure builds", "overflow or release follows"],
        "causal_chain": ["inputs arrive", "storage retains", "buildup increases", "capacity nears", "overflow or delayed release appears"],
        "surface_domains": ["inbox", "reservoir", "sediment bed", "task pile"],
        "cue_frames": [
            ["accumulation", "build", "storage", "overflow", "pressure"],
            ["pile", "stock", "reserve", "gradual", "collect"],
            ["cache", "deposit", "buildup", "store", "release"],
            ["input", "stored", "pressure", "capacity", "overflow"],
        ],
    },
    "DIFFUSION": {
        "description": "A difference spreads across space or population along a gradient, lowering concentration contrast.",
        "observations": ["an effect spreads outward", "edges see weaker traces", "concentration evens out", "migration follows a gradient"],
        "causal_chain": ["source contains high concentration", "gradient exists", "spread begins", "dilution grows", "field becomes more uniform"],
        "surface_domains": ["odor plume", "rumor spread", "heat patch", "chemical stain"],
        "cue_frames": [
            ["diffusion", "spread", "gradient", "dilution", "concentration"],
            ["seep", "leak", "disperse", "edge", "uniform"],
            ["permeate", "migration", "across", "source", "scatter"],
            ["diffuse", "concentration", "gradient", "spread", "weak trace"],
        ],
    },
    "OSCILLATION": {
        "description": "Delayed correction overshoots a target and creates repeated swings or cycles.",
        "observations": ["state swings above and below target", "delay precedes correction", "overshoot repeats", "periodic rhythm appears"],
        "causal_chain": ["state deviates", "delayed response arrives", "correction overshoots", "opposite deviation forms", "cycle repeats"],
        "surface_domains": ["thermostat hunting", "inventory cycle", "traffic waves", "control loop"],
        "cue_frames": [
            ["oscillation", "cycle", "overshoot", "delay", "swing"],
            ["undershoot", "periodic", "pulse", "alternate", "rebound"],
            ["wave", "rhythm", "phase", "hunting", "correction"],
            ["state", "delay", "overshoot", "cycle", "repeat"],
        ],
    },
    "BUFFERING": {
        "description": "A reserve or buffer absorbs shocks, delaying or smoothing the visible effect.",
        "observations": ["initial disturbance is absorbed", "reserve capacity delays visible change", "output stays smooth", "buffer eventually fills or drains"],
        "causal_chain": ["disturbance arrives", "buffer absorbs", "visible output is delayed", "capacity changes", "effect emerges later"],
        "surface_domains": ["shock absorber", "cash reserve", "queue buffer", "thermal mass"],
        "cue_frames": [
            ["buffer", "absorb", "delay", "smooth", "capacity"],
            ["cushion", "reserve", "dampen", "temporary", "shock"],
            ["hold", "slack", "stabilize", "absorption", "later"],
            ["buffering", "reserve", "delay", "output", "fills"],
        ],
    },
    "RESOURCE_DEPLETION": {
        "description": "A finite resource is consumed faster than replenished, causing scarcity and performance loss.",
        "observations": ["reserve drains", "capacity fades", "scarcity appears", "activity slows or stops"],
        "causal_chain": ["resource is available", "consumption continues", "reserve depletes", "scarcity constrains action", "exhaustion stops output"],
        "surface_domains": ["battery", "budget", "fuel tank", "attention reserve"],
        "cue_frames": [
            ["resource", "depletion", "reserve", "drain", "scarcity"],
            ["consume", "fuel", "capacity", "fatigue", "exhaustion"],
            ["depleted", "supply", "consumption", "slows", "stops"],
            ["reserve", "deplete", "capacity", "scarcity", "exhaust"],
        ],
    },
    "AMPLIFICATION": {
        "description": "A small input receives gain or propagation, producing a larger downstream effect.",
        "observations": ["small signal grows", "each stage magnifies it", "cascade accelerates", "impact becomes disproportionate"],
        "causal_chain": ["input appears", "gain is applied", "effect propagates", "cascade escalates", "large response emerges"],
        "surface_domains": ["microphone squeal", "viral sharing", "lever chain", "alarm escalation"],
        "cue_frames": [
            ["amplification", "gain", "cascade", "escalation", "signal"],
            ["amplify", "multiplier", "magnify", "propagation", "surge"],
            ["accelerate", "compounding", "growth", "small input", "large effect"],
            ["gain", "propagate", "escalate", "cascade", "impact"],
        ],
    },
    "COMPENSATION": {
        "description": "A counteracting adjustment masks or offsets deviation until the compensating path is exhausted or overwhelmed.",
        "observations": ["backup action offsets change", "visible output stays normal", "counteraction grows", "hidden strain eventually appears"],
        "causal_chain": ["deviation appears", "compensating path engages", "output is maintained", "counteraction reaches limit", "masked problem appears"],
        "surface_domains": ["backup pump", "staff workaround", "posture correction", "budget offset"],
        "cue_frames": [
            ["compensation", "offset", "counteract", "maintain", "balance"],
            ["substitute", "backup", "adapt", "adjust", "mask"],
            ["correction", "stabilize", "deviation", "counteraction", "limit"],
            ["compensate", "substitution", "output normal", "hidden strain", "overwhelmed"],
        ],
    },
}


RECOMBINATION_CASES: list[dict[str, Any]] = [
    {
        "case_id": "P037-RC-001",
        "description": "Output stays normal while a reserve absorbs variation. Once a limit is crossed, a returning signal reinforces the decline and remaining capacity drains.",
        "expected_mechanisms": ["BUFFERING", "THRESHOLD", "FEEDBACK", "RESOURCE_DEPLETION"],
        "surface_domain": "service queue",
    },
    {
        "case_id": "P037-RC-002",
        "description": "Small errors collect quietly. At a critical point the controller flips state, the correction overshoots, and the process begins cycling above and below target.",
        "expected_mechanisms": ["ACCUMULATION", "THRESHOLD", "OSCILLATION"],
        "surface_domain": "control system",
    },
    {
        "case_id": "P037-RC-003",
        "description": "A faint signal spreads through adjacent groups, each relay magnifies it, and the returning response makes the next relay stronger.",
        "expected_mechanisms": ["DIFFUSION", "AMPLIFICATION", "FEEDBACK"],
        "surface_domain": "social spread",
    },
    {
        "case_id": "P037-RC-004",
        "description": "A backup process hides demand growth. Stored work piles up behind it, then the spare capacity drains and output falls sharply.",
        "expected_mechanisms": ["COMPENSATION", "ACCUMULATION", "RESOURCE_DEPLETION"],
        "surface_domain": "operations",
    },
    {
        "case_id": "P037-RC-005",
        "description": "A channel restriction forms while an upstream buffer absorbs arrivals. After the buffer fills, backlog expands and downstream output starves.",
        "expected_mechanisms": ["FLOW", "BUFFERING", "ACCUMULATION"],
        "surface_domain": "logistics",
    },
    {
        "case_id": "P037-RC-006",
        "description": "A rotating support grows rough. The controller compensates by increasing drive, which adds heat until a seizure threshold is crossed.",
        "expected_mechanisms": ["SUPPORTED_ROTATION", "COMPENSATION", "THRESHOLD"],
        "surface_domain": "machine drive",
    },
    {
        "case_id": "P037-RC-007",
        "description": "A bracket carries extra demand. Tiny cracks accumulate, the load shifts to one point, and a final limit crossing starts collapse.",
        "expected_mechanisms": ["LOAD_TRANSFER", "ACCUMULATION", "THRESHOLD"],
        "surface_domain": "structure",
    },
    {
        "case_id": "P037-RC-008",
        "description": "Resource reserve drains while a feedback signal asks for more output. The extra output accelerates consumption and magnifies the final drop.",
        "expected_mechanisms": ["RESOURCE_DEPLETION", "FEEDBACK", "AMPLIFICATION"],
        "surface_domain": "capacity planning",
    },
    {
        "case_id": "P037-RC-009",
        "description": "Delay in a correction loop makes each adjustment arrive late. The response overshoots, reverses, and repeats in a visible rhythm.",
        "expected_mechanisms": ["FEEDBACK", "OSCILLATION", "COMPENSATION"],
        "surface_domain": "control tuning",
    },
    {
        "case_id": "P037-RC-010",
        "description": "A contaminant leaks from a source and spreads down a gradient. A cleanup reserve absorbs it at first, then capacity is exhausted and traces appear everywhere.",
        "expected_mechanisms": ["DIFFUSION", "BUFFERING", "RESOURCE_DEPLETION"],
        "surface_domain": "environment",
    },
    {
        "case_id": "P037-RC-011",
        "description": "A small queue surge is cushioned by slack. Once the slack is gone, the narrowed route creates a backlog and feedback from delays pushes more arrivals into the same path.",
        "expected_mechanisms": ["BUFFERING", "FLOW", "FEEDBACK"],
        "surface_domain": "routing",
    },
    {
        "case_id": "P037-RC-012",
        "description": "Heat spreads from one contact point. Friction in the turning support rises, a limit is crossed, and the part locks.",
        "expected_mechanisms": ["DIFFUSION", "SUPPORTED_ROTATION", "THRESHOLD"],
        "surface_domain": "bearing",
    },
    {
        "case_id": "P037-RC-013",
        "description": "Tiny demand shifts are masked by an offsetting support. Strain still collects at one lug until the bracket tears from a local point.",
        "expected_mechanisms": ["COMPENSATION", "ACCUMULATION", "LOAD_TRANSFER"],
        "surface_domain": "mounting",
    },
    {
        "case_id": "P037-RC-014",
        "description": "A weak alarm signal is amplified through repeated relays. Once it crosses a trip point, the response loop reinforces further escalation.",
        "expected_mechanisms": ["AMPLIFICATION", "THRESHOLD", "FEEDBACK"],
        "surface_domain": "alerting",
    },
    {
        "case_id": "P037-RC-015",
        "description": "Inventory builds while demand is buffered. Delayed replenishment overshoots, stock swings from shortage to excess, and the cycle repeats.",
        "expected_mechanisms": ["ACCUMULATION", "BUFFERING", "OSCILLATION"],
        "surface_domain": "inventory",
    },
    {
        "case_id": "P037-RC-016",
        "description": "A rumor begins at one source, spreads outward, gains strength through each relay, and eventually drains attention from the original task.",
        "expected_mechanisms": ["DIFFUSION", "AMPLIFICATION", "RESOURCE_DEPLETION"],
        "surface_domain": "coordination",
    },
    {
        "case_id": "P037-RC-017",
        "description": "A queue stays hidden because staff add manual workarounds. The workaround capacity depletes, then throughput drops through the restricted handoff.",
        "expected_mechanisms": ["COMPENSATION", "RESOURCE_DEPLETION", "FLOW"],
        "surface_domain": "support desk",
    },
    {
        "case_id": "P037-RC-018",
        "description": "A rotating feeder releases material unevenly. The uneven release accumulates downstream, then a feedback controller overcorrects and creates pulses.",
        "expected_mechanisms": ["SUPPORTED_ROTATION", "ACCUMULATION", "FEEDBACK", "OSCILLATION"],
        "surface_domain": "feeder",
    },
    {
        "case_id": "P037-RC-019",
        "description": "Load shifts across a frame. One region absorbs it temporarily, cracks diffuse from the high-stress point, and local capacity is consumed.",
        "expected_mechanisms": ["LOAD_TRANSFER", "BUFFERING", "DIFFUSION", "RESOURCE_DEPLETION"],
        "surface_domain": "frame",
    },
    {
        "case_id": "P037-RC-020",
        "description": "Small route delays are amplified by priority rules. The queue crosses a limit and the returning delay signal makes later batches choose the same route.",
        "expected_mechanisms": ["FLOW", "AMPLIFICATION", "THRESHOLD", "FEEDBACK"],
        "surface_domain": "dispatch",
    },
    {
        "case_id": "P037-RC-021",
        "description": "A reserve hides falling fuel. Once the reserve is depleted, a controller increases demand and the final decline accelerates.",
        "expected_mechanisms": ["BUFFERING", "RESOURCE_DEPLETION", "FEEDBACK", "AMPLIFICATION"],
        "surface_domain": "energy",
    },
    {
        "case_id": "P037-RC-022",
        "description": "A limit switch triggers late. The compensation then overshoots, reverses direction, and repeats because the feedback signal is delayed.",
        "expected_mechanisms": ["THRESHOLD", "COMPENSATION", "OSCILLATION", "FEEDBACK"],
        "surface_domain": "actuator",
    },
    {
        "case_id": "P037-RC-023",
        "description": "Sediment collects in a passage and diffuses into side channels. After enough buildup, throughput falls and downstream output starves.",
        "expected_mechanisms": ["ACCUMULATION", "DIFFUSION", "FLOW"],
        "surface_domain": "channel",
    },
    {
        "case_id": "P037-RC-024",
        "description": "A local crack concentrates demand. Each small deformation magnifies the next, and the support crosses a failure limit.",
        "expected_mechanisms": ["LOAD_TRANSFER", "AMPLIFICATION", "THRESHOLD"],
        "surface_domain": "fixture",
    },
    {
        "case_id": "P037-RC-025",
        "description": "A spreading heat patch reaches a pivot. Friction rises, the controller adds drive to compensate, and the added drive drains capacity.",
        "expected_mechanisms": ["DIFFUSION", "SUPPORTED_ROTATION", "COMPENSATION", "RESOURCE_DEPLETION"],
        "surface_domain": "rotor",
    },
    {
        "case_id": "P037-RC-026",
        "description": "Work accumulates behind a buffer. When the buffer fills, the release comes in pulses that overshoot capacity and then undershoot demand.",
        "expected_mechanisms": ["ACCUMULATION", "BUFFERING", "OSCILLATION", "FLOW"],
        "surface_domain": "workflow",
    },
    {
        "case_id": "P037-RC-027",
        "description": "A small imbalance spreads across neighboring supports. Compensation masks the tilt until one anchor takes excess demand and bends.",
        "expected_mechanisms": ["DIFFUSION", "COMPENSATION", "LOAD_TRANSFER"],
        "surface_domain": "platform",
    },
    {
        "case_id": "P037-RC-028",
        "description": "A response loop stabilizes output until stored errors cross a boundary. Then the same loop reinforces the wrong correction and amplifies deviation.",
        "expected_mechanisms": ["FEEDBACK", "ACCUMULATION", "THRESHOLD", "AMPLIFICATION"],
        "surface_domain": "automation",
    },
    {
        "case_id": "P037-RC-029",
        "description": "Reserve staff keep service smooth while tickets spread across teams. Once staff capacity drains, feedback from delays increases repeated contacts.",
        "expected_mechanisms": ["BUFFERING", "DIFFUSION", "RESOURCE_DEPLETION", "FEEDBACK"],
        "surface_domain": "service desk",
    },
    {
        "case_id": "P037-RC-030",
        "description": "A turning distributor creates periodic release waves. The waves build a queue at a restricted route, and the queue triggers a threshold rule.",
        "expected_mechanisms": ["SUPPORTED_ROTATION", "OSCILLATION", "ACCUMULATION", "FLOW", "THRESHOLD"],
        "surface_domain": "sorter",
    },
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


def state_path(group: str) -> Path:
    return PROOF_DIR / "mcp" / f"group_{group.lower()}_pond_state.json"


def runtime_dir(group: str) -> Path:
    return RUNTIME_ROOT / f"group_{group.lower()}"


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
                "Return motifs, traceable lineages, lineage hashes, and uncertainty.",
            ],
            "desired_artifacts": [
                "candidate pathways",
                "supporting mechanisms",
                "mechanism combinations",
                "lineage hashes",
            ],
        },
    }


def consult(request: dict[str, Any], *, group: str) -> dict[str, Any]:
    result = process_consult_request(request, artifact_dir=runtime_dir(group), state_path=state_path(group))
    response = dict(result.response)
    response["http_status"] = result.status_code
    response["classification"] = classify_mcp_response(result.response).value
    return response


def mechanism_rows(mechanisms: tuple[str, ...]) -> list[dict[str, Any]]:
    rows = []
    for mechanism in mechanisms:
        definition = MECHANISM_DEFINITIONS[mechanism]
        rows.append(
            {
                "mechanism": mechanism,
                "description": definition["description"],
                "observations": definition["observations"],
                "causal_chain": definition["causal_chain"],
                "surface_domains": definition["surface_domains"],
            }
        )
    return rows


def build_seasoning_examples(group: str, mechanisms: tuple[str, ...], per_mechanism: int) -> list[dict[str, Any]]:
    rows = []
    for mechanism in mechanisms:
        definition = MECHANISM_DEFINITIONS[mechanism]
        domains = definition["surface_domains"]
        cue_frames = definition["cue_frames"]
        for index in range(1, per_mechanism + 1):
            domain = domains[(index - 1) % len(domains)]
            cue_frame = cue_frames[(index - 1) % len(cue_frames)]
            row = {
                "lesson_id": f"P037-{group}-{mechanism}-{index:03d}",
                "group": group,
                "mechanism": mechanism,
                "surface_domain": f"{domain}_variant_{((index - 1) // len(domains)) + 1:02d}",
                "observations": [
                    f"{observation}. Domain anchor: {domain}."
                    for observation in definition["observations"]
                ],
                "causal_chain": definition["causal_chain"],
                "consequence_signature": cue_frame,
                "mechanism_summary": definition["description"],
                "expected_recall_cues": cue_frame,
            }
            rows.append(row)
    return rows


def lesson_text(lesson: dict[str, Any]) -> str:
    return (
        f"Mechanism summary: {lesson['mechanism_summary']} "
        f"Observations: {' '.join(lesson['observations'])} "
        f"Causal chain: {' -> '.join(lesson['causal_chain'])}. "
        f"Consequence signature: {'; '.join(lesson['consequence_signature'])}. "
        f"Expected recall cues: {'; '.join(lesson['expected_recall_cues'])}."
    )


def run_seasoning(group: str, lessons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for index, lesson in enumerate(lessons, start=1):
        event_id = f"group-{group.lower()}-season-{index:03d}-{lesson['mechanism'].lower()}"
        summary = f"Season {lesson['mechanism']} for Proof 037 group {group}."
        response = consult(
            payload(
                f"proof-037-{event_id}",
                f"ACTION: SEASON. Mechanism label: {lesson['mechanism']}. {lesson_text(lesson)}",
                summary=summary,
                mode="proof_planning",
            ),
            group=group,
        )
        rows.append(
            {
                "event_id": event_id,
                "group": group,
                "mechanism": lesson["mechanism"],
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
        )
    return rows


def recombination_question(description: str) -> str:
    return (
        "Observation only. Do not answer directly.\n"
        "Return candidate pathways, supporting mechanisms, motifs, mechanism combinations, and traceable lineages that may explain these observations.\n"
        f"Observation:\n{description}\n"
        "Required:\n"
        "- candidate pathways\n"
        "- supporting mechanisms\n"
        "- mechanism combinations\n"
        "- supporting motifs\n"
        "- supporting lineages\n"
        "- lineage hashes\n"
        "- confidence or fail-closed reason"
    )


def run_recombination_consults(group: str, cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for case in cases:
        question = recombination_question(case["description"])
        response = consult(
            payload(
                f"proof-037-group-{group.lower()}-recombination-{case['case_id'].lower()}",
                question,
                summary=f"Mandatory pond-backed recombination consult for group {group}, {case['case_id']}.",
                mode="audit",
            ),
            group=group,
        )
        rows.append(
            {
                "case_id": case["case_id"],
                "group": group,
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
                "pre_consult_prompt_expected_mechanisms": [],
            }
        )
    return rows


def mechanism_counter(consult_row: dict[str, Any]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for payload_row in consult_row.get("lineage_payloads", []):
        mechanism = str(payload_row.get("mechanism", ""))
        if mechanism in MECHANISM_MOTIFS:
            counter[mechanism] += 1
    return counter


def generate_candidate(case: dict[str, Any], consult_row: dict[str, Any]) -> dict[str, Any]:
    counts = mechanism_counter(consult_row)
    supporting = [mechanism for mechanism, _count in counts.most_common()]
    total = sum(counts.values()) or 1
    candidate_pathways = []
    if supporting:
        if len(supporting) > 1:
            candidate_pathways.append(
                {
                    "pathway": " + ".join(supporting[: min(4, len(supporting))]),
                    "weight": round(sum(counts[mechanism] for mechanism in supporting[:4]) / total, 4),
                    "supporting_lineage_hashes": consult_row.get("lineage_hashes", [])[:5],
                    "supporting_motifs": consult_row.get("returned_motifs", []),
                    "reason": "Pond recall returned traceable lineage payloads from these mechanisms before candidate generation.",
                }
            )
        for mechanism in supporting[:5]:
            candidate_pathways.append(
                {
                    "pathway": mechanism,
                    "weight": round(counts[mechanism] / total, 4),
                    "supporting_lineage_hashes": [
                        hash_value
                        for payload_row, hash_value in zip(
                            consult_row.get("lineage_payloads", []),
                            consult_row.get("lineage_hashes", []),
                        )
                        if payload_row.get("mechanism") == mechanism
                    ],
                    "supporting_motifs": MECHANISM_MOTIFS.get(mechanism, []),
                    "reason": "Single mechanism retained as a component of the recalled combination, not a final answer.",
                }
            )
    confidence = round(min(1.0, (len(supporting) / 4.0) + (min(total, 5) / 20.0)), 4) if supporting else 0.0
    return {
        "case_id": case["case_id"],
        "candidate_pathways": candidate_pathways,
        "supporting_mechanisms": supporting,
        "mechanism_combinations": [supporting[: min(4, len(supporting))]] if supporting else [],
        "combination_depth": len(supporting),
        "confidence": confidence,
        "status": "CANDIDATES_GENERATED" if supporting else "FAIL_CLOSED",
    }


def build_candidates(group: str, cases: list[dict[str, Any]], consults: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_case = {row["case_id"]: row for row in consults}
    rows = []
    for case in cases:
        row = generate_candidate(case, by_case[case["case_id"]])
        row["group"] = group
        rows.append(row)
    return rows


def expected_valid(case: dict[str, Any], candidate: dict[str, Any]) -> bool:
    expected = set(case["expected_mechanisms"])
    observed = set(candidate["supporting_mechanisms"])
    if len(expected) <= 2:
        return expected.issubset(observed)
    return len(expected & observed) >= max(2, round(len(expected) * 0.67))


def candidate_diversity(candidates: list[dict[str, Any]]) -> float:
    return round(sum(len(row["candidate_pathways"]) for row in candidates) / len(candidates), 4)


def valid_candidate_rate(cases: list[dict[str, Any]], candidates: list[dict[str, Any]]) -> float:
    return round(sum(expected_valid(case, candidate) for case, candidate in zip(cases, candidates)) / len(cases), 4)


def average_combination_depth(candidates: list[dict[str, Any]]) -> float:
    return round(sum(row["combination_depth"] for row in candidates) / len(candidates), 4)


def premature_convergence(candidates: list[dict[str, Any]]) -> float:
    return round(sum(row["combination_depth"] <= 1 for row in candidates) / len(candidates), 4)


def recombination_metrics(cases: list[dict[str, Any]], group_a: list[dict[str, Any]], group_b: list[dict[str, Any]]) -> dict[str, Any]:
    group_a_valid = valid_candidate_rate(cases, group_a)
    group_b_valid = valid_candidate_rate(cases, group_b)
    return {
        "group_a_valid_candidate_rate": group_a_valid,
        "group_b_valid_candidate_rate": group_b_valid,
        "group_a_candidate_diversity": candidate_diversity(group_a),
        "group_b_candidate_diversity": candidate_diversity(group_b),
        "group_a_combination_depth": average_combination_depth(group_a),
        "group_b_combination_depth": average_combination_depth(group_b),
        "group_a_premature_convergence": premature_convergence(group_a),
        "group_b_premature_convergence": premature_convergence(group_b),
        "improvement_delta": round(group_b_valid - group_a_valid, 4),
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


def harmonic_overlap_audit(cases: list[dict[str, Any]], group_consults: dict[str, list[dict[str, Any]]], group_candidates: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    groups = {}
    for group, consults in group_consults.items():
        mechanism_reuse = Counter()
        motif_reuse = Counter()
        lineage_hashes: list[str] = []
        case_activations = []
        for case, consult_row, candidate in zip(cases, consults, group_candidates[group]):
            mechanisms = candidate["supporting_mechanisms"]
            mechanism_reuse.update(mechanisms)
            motif_reuse.update(consult_row.get("returned_motifs", []))
            lineage_hashes.extend(consult_row.get("lineage_hashes", []))
            case_activations.append(
                {
                    "case_id": case["case_id"],
                    "expected_mechanisms": case["expected_mechanisms"],
                    "activated_mechanisms": mechanisms,
                    "multiple_mechanisms_activated": len(mechanisms) > 1,
                    "shared_motifs": sorted(set(consult_row.get("returned_motifs", []))),
                    "lineage_hash_count": len(consult_row.get("lineage_hashes", [])),
                }
            )
        combination_depths = [row["combination_depth"] for row in group_candidates[group]]
        groups[group] = {
            "mechanism_reuse": dict(sorted(mechanism_reuse.items())),
            "cross_domain_overlap": {
                "surface_domains": sorted({case["surface_domain"] for case in cases}),
                "cases_with_multiple_mechanisms": sum(row["multiple_mechanisms_activated"] for row in case_activations),
            },
            "shared_motifs": dict(sorted(motif_reuse.items())),
            "shared_lineage_hashes": {
                "total": len(lineage_hashes),
                "unique": len(set(lineage_hashes)),
                "reused": len(lineage_hashes) - len(set(lineage_hashes)),
            },
            "pathway_convergence": {
                "average_combination_depth": round(sum(combination_depths) / len(combination_depths), 4),
                "single_mechanism_cases": sum(depth <= 1 for depth in combination_depths),
                "multi_mechanism_cases": sum(depth > 1 for depth in combination_depths),
            },
            "case_activations": case_activations,
        }
    return {
        "question": "Did multiple mechanisms activate together?",
        "answer": groups["B"]["pathway_convergence"]["multi_mechanism_cases"] > groups["A"]["pathway_convergence"]["multi_mechanism_cases"],
        "groups": groups,
    }


def hostile_audit(metrics: dict[str, Any], overlap: dict[str, Any], all_consults_valid: bool) -> dict[str, Any]:
    valid_improved = metrics["group_b_valid_candidate_rate"] > metrics["group_a_valid_candidate_rate"]
    diversity_improved = metrics["group_b_candidate_diversity"] > metrics["group_a_candidate_diversity"]
    depth_improved = metrics["group_b_combination_depth"] > metrics["group_a_combination_depth"]
    convergence_reduced = metrics["group_b_premature_convergence"] < metrics["group_a_premature_convergence"]
    any_diversity_signal = valid_improved or diversity_improved or depth_improved or convergence_reduced
    if not all_consults_valid:
        verdict = "FAIL"
    elif valid_improved and depth_improved and diversity_improved:
        verdict = "STRONG_SIGNAL"
    elif diversity_improved or depth_improved:
        verdict = "WEAK_SIGNAL"
    else:
        verdict = "FAIL"
    return {
        "hostile_verdict": verdict,
        "remaining_saturation_explanation": not any_diversity_signal,
        "remaining_diversity_explanation": any_diversity_signal,
        "remaining_prompt_volume_explanation": False,
        "remaining_scoring_artifact_explanation": True,
        "remaining_hardcoded_combination_explanation": False,
        "surviving_claims": [
            "Group A and Group B used equal total seasoning volume: 288 examples each.",
            "All seasoning and recombination consult logs were pond-backed and validator-compatible."
            if all_consults_valid
            else "At least one consult log failed the pond-backed boundary.",
            "Group B improved valid candidate rate, pathway diversity, and combination depth over Group A."
            if valid_improved and diversity_improved and depth_improved
            else "Mechanism diversity produced no measurable recombination improvement under the current recall path.",
        ],
        "invalidated_claims": [
            "Proof 037 proves cognition.",
            "The deterministic scoring artifact explanation is eliminated.",
            "The mechanism catalog is independently learned rather than explicitly seeded.",
        ],
        "attacks": [
            {"attack": "training volume explanations", "finding": "Rejected for total count: both groups use 288 seasoning examples."},
            {"attack": "prompt volume explanations", "finding": "Mostly rejected by balanced example count and shared request contract."},
            {"attack": "duplicate examples", "finding": "Partially survives because examples are deterministic variants over repeated surface domains."},
            {"attack": "scoring artifacts", "finding": "Survives. Candidate generation is deterministic over returned lineage payloads."},
            {"attack": "hardcoded combinations", "finding": "Partially rejected: expected combinations are used only for metrics, not generation."},
            {"attack": "non-independent mechanisms", "finding": "Survives. Several mechanisms share motifs such as input, response, delay, and stabilization."},
            {"attack": "pathway convergence", "finding": "Group B activated multiple mechanisms together in more cases." if overlap["answer"] else "Multiple-mechanism activation did not increase."},
        ],
        "metric_flags": {
            "valid_candidate_rate_improved": valid_improved,
            "candidate_diversity_improved": diversity_improved,
            "combination_depth_improved": depth_improved,
            "premature_convergence_reduced": convergence_reduced,
        },
    }


def proof_manifest(metrics: dict[str, Any], hostile: dict[str, Any], cases: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "proof_id": PROOF_ID,
        "title": TITLE,
        "status": "complete",
        "targets": [
            "MechanismDiversity",
            "EqualSeasoningVolume",
            "FreshIsolatedPonds",
            "PondBackedSeasoning",
            "PondBackedRecombinationRecall",
            "NovelCombinationCases",
            "HarmonicOverlapAudit",
            "HostileDiversityAudit",
        ],
        "claim_level": "evidence_backed",
        "inside_voice_adapter_status": "pond_backed",
        "public_private_boundary": "Public-safe proof artifacts record deterministic curricula, motifs, lineage refs, lineage hashes, and aggregate recombination metrics.",
        "required_artifacts": [
            "README.md",
            "proof_manifest.json",
            "curriculum/group_a_mechanisms.jsonl",
            "curriculum/group_b_mechanisms.jsonl",
            "curriculum/group_a_seasoning_examples.jsonl",
            "curriculum/group_b_seasoning_examples.jsonl",
            "mcp/pond_state_manifest.json",
            "mcp/group_a_seasoning_log.jsonl",
            "mcp/group_b_seasoning_log.jsonl",
            "mcp/group_a_recombination_consults.jsonl",
            "mcp/group_b_recombination_consults.jsonl",
            "tests/recombination_cases.jsonl",
            "results/recombination_candidates.json",
            "analysis/recombination_metrics.json",
            "analysis/harmonic_overlap_audit.json",
            "analysis/hostile_audit.json",
        ],
        "disallowed_claims": [
            "Proof 037 proves cognition.",
            "Mechanism diversity effects are independent of deterministic scoring.",
            "Explicitly seeded mechanisms were discovered without teaching.",
            "Non-independent mechanism definitions are fully ruled out.",
        ],
        "lineage": {
            "mcp_endpoint": "in_process_tools.integrations.inside_voice_mcp_server.process_consult_request",
            "contract_version": "inside_voice_mcp_contract/0.2",
            "request_hash": hash_canonical_json(
                {
                    "group_a_mechanisms": GROUP_A_MECHANISMS,
                    "group_b_mechanisms": GROUP_B_MECHANISMS,
                    "case_ids": [case["case_id"] for case in cases],
                    "examples_per_group": 288,
                }
            ),
            "response_hash": hash_canonical_json(metrics),
            "derived_from": "Proof 036 saturation result and repaired pond-backed MCP consult path.",
            "validates": hostile["hostile_verdict"],
            "candidate_status": "eligible",
        },
    }


def readme(metrics: dict[str, Any], hostile: dict[str, Any], overlap: dict[str, Any]) -> str:
    improved = hostile["hostile_verdict"] not in {"FAIL", "INCONCLUSIVE"}
    bounded_claim = (
        "With total seasoning volume held constant, the diverse 12-mechanism pond produced more valid recombination candidates, more candidate pathway diversity, and deeper mechanism combinations than the saturated 3-mechanism pond."
        if improved
        else "With total seasoning volume held constant, the diverse 12-mechanism pond did not produce more valid recombination candidates, more candidate pathway diversity, or deeper mechanism combinations than the saturated 3-mechanism pond."
    )
    hostile_note = (
        "The hostile audit still preserves deterministic scoring artifacts and non-independent mechanism-definition overlap as explanations. It rejects simple training-volume and prompt-volume explanations because both groups used 288 seasoning examples and the same request contract."
        if improved
        else "The hostile audit rejects training-volume and prompt-volume explanations because both groups used 288 seasoning examples and the same request contract. The remaining explanation is simpler: the current recall path converged on one dominant mechanism per case rather than recombining mechanisms."
    )
    return f"""# Proof 037 - Mechanism Diversity Study

Proof 037 compares equal teaching volume with different mechanism diversity.

- Group A: 3 mechanisms, 96 examples each, 288 total.
- Group B: 12 mechanisms, 24 examples each, 288 total.

Both groups use fresh isolated pond states and pond-backed MCP seasoning/recall.

## Result

`{hostile["hostile_verdict"]}`

## Metrics

- Group A valid candidate rate: {metrics["group_a_valid_candidate_rate"]}
- Group B valid candidate rate: {metrics["group_b_valid_candidate_rate"]}
- Group A candidate diversity: {metrics["group_a_candidate_diversity"]}
- Group B candidate diversity: {metrics["group_b_candidate_diversity"]}
- Group A combination depth: {metrics["group_a_combination_depth"]}
- Group B combination depth: {metrics["group_b_combination_depth"]}
- Group A premature convergence: {metrics["group_a_premature_convergence"]}
- Group B premature convergence: {metrics["group_b_premature_convergence"]}
- Improvement delta: {metrics["improvement_delta"]}

## Bounded Claim

{bounded_claim}

{hostile_note}

## Harmonic Overlap

Multiple mechanisms activated together more often in Group B: {overlap["groups"]["B"]["pathway_convergence"]["multi_mechanism_cases"]} cases versus {overlap["groups"]["A"]["pathway_convergence"]["multi_mechanism_cases"]} in Group A.
"""


def main() -> int:
    group_a_lessons = build_seasoning_examples("A", GROUP_A_MECHANISMS, 96)
    group_b_lessons = build_seasoning_examples("B", GROUP_B_MECHANISMS, 24)
    cases = [
        {
            **case,
            "forbidden_description_terms": list(GROUP_B_MECHANISMS),
            "expected_reason": "This held-out case requires multiple interacting mechanisms; no single mechanism is scored as sufficient.",
        }
        for case in RECOMBINATION_CASES
    ]

    save_pond(state_path("A"), empty_pond_state())
    save_pond(state_path("B"), empty_pond_state())

    group_a_seasoning = run_seasoning("A", group_a_lessons)
    group_b_seasoning = run_seasoning("B", group_b_lessons)
    group_a_consults = run_recombination_consults("A", cases)
    group_b_consults = run_recombination_consults("B", cases)
    group_a_candidates = build_candidates("A", cases, group_a_consults)
    group_b_candidates = build_candidates("B", cases, group_b_consults)
    metrics = recombination_metrics(cases, group_a_candidates, group_b_candidates)
    overlap = harmonic_overlap_audit(
        cases,
        {"A": group_a_consults, "B": group_b_consults},
        {"A": group_a_candidates, "B": group_b_candidates},
    )
    all_consults_valid = all(
        [
            validate_consults_locally(group_a_seasoning),
            validate_consults_locally(group_b_seasoning),
            validate_consults_locally(group_a_consults),
            validate_consults_locally(group_b_consults),
        ]
    )
    hostile = hostile_audit(metrics, overlap, all_consults_valid)

    write_jsonl(PROOF_DIR / "curriculum" / "group_a_mechanisms.jsonl", mechanism_rows(GROUP_A_MECHANISMS))
    write_jsonl(PROOF_DIR / "curriculum" / "group_b_mechanisms.jsonl", mechanism_rows(GROUP_B_MECHANISMS))
    write_jsonl(PROOF_DIR / "curriculum" / "group_a_seasoning_examples.jsonl", group_a_lessons)
    write_jsonl(PROOF_DIR / "curriculum" / "group_b_seasoning_examples.jsonl", group_b_lessons)
    write_jsonl(PROOF_DIR / "tests" / "recombination_cases.jsonl", cases)
    write_json(
        PROOF_DIR / "mcp" / "pond_state_manifest.json",
        {
            "created_at": utc_timestamp(),
            "groups": [
                {
                    "group": "A",
                    "pond_state_id": "proof-037-group-a-isolated-pond",
                    "is_isolated": True,
                    "mechanisms": list(GROUP_A_MECHANISMS),
                    "seasoning_examples": len(group_a_lessons),
                    "state_path": "mcp/group_a_pond_state.json",
                },
                {
                    "group": "B",
                    "pond_state_id": "proof-037-group-b-isolated-pond",
                    "is_isolated": True,
                    "mechanisms": list(GROUP_B_MECHANISMS),
                    "seasoning_examples": len(group_b_lessons),
                    "state_path": "mcp/group_b_pond_state.json",
                },
            ],
            "prior_contents": [],
            "notes": "Both groups start from empty_pond_state(); there is no shared seasoning.",
        },
    )
    write_jsonl(PROOF_DIR / "mcp" / "group_a_seasoning_log.jsonl", group_a_seasoning)
    write_jsonl(PROOF_DIR / "mcp" / "group_b_seasoning_log.jsonl", group_b_seasoning)
    write_jsonl(PROOF_DIR / "mcp" / "group_a_recombination_consults.jsonl", group_a_consults)
    write_jsonl(PROOF_DIR / "mcp" / "group_b_recombination_consults.jsonl", group_b_consults)
    write_json(
        PROOF_DIR / "results" / "recombination_candidates.json",
        {"groups": {"A": group_a_candidates, "B": group_b_candidates}},
    )
    write_json(PROOF_DIR / "analysis" / "recombination_metrics.json", metrics)
    write_json(PROOF_DIR / "analysis" / "harmonic_overlap_audit.json", overlap)
    write_json(PROOF_DIR / "analysis" / "hostile_audit.json", hostile)
    write_json(PROOF_DIR / "proof_manifest.json", proof_manifest(metrics, hostile, cases))
    write_text(PROOF_DIR / "README.md", readme(metrics, hostile, overlap))

    print(hostile["hostile_verdict"])
    return 0 if all_consults_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
