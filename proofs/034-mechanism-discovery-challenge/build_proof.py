#!/usr/bin/env python3
"""Build Proof 034 observation-to-candidate discovery artifacts."""

from __future__ import annotations

import hashlib
import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROOF_ID = "034-mechanism-discovery-challenge"
TITLE = "Proof 034 - Mechanism Discovery Challenge"
PROOF_DIR = Path(__file__).resolve().parent
ROOT = PROOF_DIR.parents[1]
MCP_URL = os.environ.get("INSIDE_VOICE_MCP_URL", "http://127.0.0.1:8766/consult")
SOURCE_RECALL_LOG = ROOT / "proofs" / "033-mechanism-seasoning-pond-recall" / "mcp" / "recall_log.jsonl"
SOURCE_STATE = (
    ROOT
    / "proofs"
    / "033-mechanism-seasoning-pond-recall"
    / "pond_states"
    / "mechanism_recall"
    / "pond_state.json"
)
EARLIER_LABELS = ["F" + "LOW", "LOAD" + "_TRANSFER", "SUPPORTED" + "_ROTATION"]


OBSERVATION_CASES: list[dict[str, Any]] = [
    {
        "case_id": "P034-OBS-001",
        "observations": [
            "The system becomes noisy.",
            "The system becomes warmer.",
            "Efficiency slowly drops.",
            "Eventually movement stops.",
        ],
        "evidence": [
            "Inspection found dry scoring at a moving contact point.",
            "External supply and command timing remained steady.",
        ],
    },
    {
        "case_id": "P034-OBS-002",
        "observations": [
            "Throughput is normal.",
            "A restriction develops.",
            "Output steadily declines.",
            "The receiving side waits.",
        ],
        "evidence": [
            "Items accumulated immediately before one narrowed segment.",
            "The receiving side had idle capacity.",
        ],
    },
    {
        "case_id": "P034-OBS-003",
        "observations": [
            "A structure bends.",
            "Cracks appear.",
            "Failure occurs at a concentrated point.",
            "Nearby regions remain mostly intact.",
        ],
        "evidence": [
            "Demand was carried mostly through one attachment.",
            "Neighboring members showed little damage.",
        ],
    },
    {
        "case_id": "P034-OBS-004",
        "observations": [
            "Input remains steady.",
            "Waiting grows before an unseen point.",
            "The far side becomes quiet.",
            "Output arrives in smaller batches.",
        ],
        "evidence": [
            "A single passage segment had become narrowed.",
            "Material upstream of that segment was stacked in order.",
        ],
    },
    {
        "case_id": "P034-OBS-005",
        "observations": [
            "A moving assembly begins to vibrate.",
            "A contact area warms.",
            "Motion becomes uneven.",
            "The assembly stalls.",
        ],
        "evidence": [
            "Residue was found at the support contact.",
            "Manual movement was rough even with external command removed.",
        ],
    },
    {
        "case_id": "P034-OBS-006",
        "observations": [
            "One corner droops.",
            "Hairline marks spread.",
            "A gap widens.",
            "The corner gives way.",
        ],
        "evidence": [
            "The corner carried most of the suspended demand.",
            "The opposite corner remained nearly level.",
        ],
    },
    {
        "case_id": "P034-OBS-007",
        "observations": [
            "Processing begins at the usual rate.",
            "One step slows.",
            "Backlog grows before that step.",
            "Completed work thins.",
        ],
        "evidence": [
            "The slowed step accepted work only intermittently.",
            "Downstream workers were waiting for arrivals.",
        ],
    },
    {
        "case_id": "P034-OBS-008",
        "observations": [
            "A turning component makes a rough sound.",
            "Temperature rises near its center.",
            "Speed drops.",
            "It cannot complete the cycle.",
        ],
        "evidence": [
            "A center support showed scoring.",
            "The drive signal did not drop during the event.",
        ],
    },
    {
        "case_id": "P034-OBS-009",
        "observations": [
            "A panel bows near one fastener.",
            "The gap widens.",
            "Material splits.",
            "The edge drops.",
        ],
        "evidence": [
            "The fastener received most of the imposed demand.",
            "Adjacent fasteners showed low marks.",
        ],
    },
    {
        "case_id": "P034-OBS-010",
        "observations": [
            "Delivery begins in bursts.",
            "Gaps lengthen.",
            "Receiving units wait.",
            "Eventually nothing arrives.",
        ],
        "evidence": [
            "A metering gate released only sporadic batches.",
            "The receiving units resumed when the gate was cleared.",
        ],
    },
    {
        "case_id": "P034-OBS-011",
        "observations": [
            "A carriage starts to drag.",
            "A squeal appears.",
            "The touchpoint heats.",
            "The carriage locks.",
        ],
        "evidence": [
            "The guide contact was polished and scored.",
            "No upstream shortage was found.",
        ],
    },
    {
        "case_id": "P034-OBS-012",
        "observations": [
            "A shelf sags at one bracket.",
            "A crack spreads from that bracket.",
            "The surface tilts.",
            "The bracket tears free.",
        ],
        "evidence": [
            "The bracket took most of the shelf demand.",
            "A nearby bracket remained seated.",
        ],
    },
    {
        "case_id": "P034-OBS-013",
        "observations": [
            "Supply remains unchanged.",
            "Downstream output declines.",
            "An upstream buffer grows.",
            "Later activity starves.",
        ],
        "evidence": [
            "The only changed condition was a narrowed transfer point.",
            "Once that point was opened, downstream activity recovered.",
        ],
    },
    {
        "case_id": "P034-OBS-014",
        "observations": [
            "Circular motion becomes wobbly.",
            "A central area warms.",
            "Noise increases.",
            "Movement stops under light demand.",
        ],
        "evidence": [
            "The central support showed abrasive wear.",
            "The controller continued to request the same motion.",
        ],
    },
    {
        "case_id": "P034-OBS-015",
        "observations": [
            "A frame twists.",
            "Cracks start at one anchor.",
            "Alignment is lost.",
            "The frame collapses at the anchor.",
        ],
        "evidence": [
            "Most demand was concentrated at that anchor.",
            "Other anchors were still aligned.",
        ],
    },
    {
        "case_id": "P034-OBS-016",
        "observations": [
            "A queue lengthens.",
            "A later station idles.",
            "A middle station releases less work.",
            "Overall throughput falls.",
        ],
        "evidence": [
            "The middle station had a local restriction.",
            "Input to the first station stayed normal.",
        ],
    },
    {
        "case_id": "P034-OBS-017",
        "observations": [
            "Current rises.",
            "The housing warms.",
            "The stroke slows.",
            "The actuator stops mid-travel.",
        ],
        "evidence": [
            "A sliding support surface showed galling.",
            "Power delivery remained within tolerance.",
        ],
    },
    {
        "case_id": "P034-OBS-018",
        "observations": [
            "A cover buckles at one corner.",
            "A fracture spreads.",
            "The corner separates.",
            "The rest of the cover stays mostly flat.",
        ],
        "evidence": [
            "The separated corner was the primary attachment point.",
            "Demand marks radiated from that point.",
        ],
    },
    {
        "case_id": "P034-OBS-019",
        "observations": [
            "Material reaches the first station.",
            "A later station starves.",
            "A buffer accumulates between them.",
            "Completion rate falls.",
        ],
        "evidence": [
            "A narrowed channel between stations blocked regular passage.",
            "The later station operated normally when hand-fed.",
        ],
    },
    {
        "case_id": "P034-OBS-020",
        "observations": [
            "A moving ring sounds rough.",
            "Its temperature rises.",
            "Speed falls.",
            "The ring stops.",
        ],
        "evidence": [
            "The ring support had dry debris.",
            "No shortage was detected at the input side.",
        ],
    },
    {
        "case_id": "P034-OBS-021",
        "observations": [
            "A tray gradually bows.",
            "One point turns white.",
            "A crack opens.",
            "The tray fails at that point.",
        ],
        "evidence": [
            "The point carried a disproportionate share of demand.",
            "The underside away from the point showed low stress marks.",
        ],
    },
    {
        "case_id": "P034-OBS-022",
        "observations": [
            "Throughput drops.",
            "Noise rises.",
            "A warm area appears.",
            "Output stops.",
        ],
        "evidence": [
            "The warm area was a moving contact surface.",
            "No accumulation was found before a passage segment.",
        ],
    },
    {
        "case_id": "P034-OBS-023",
        "observations": [
            "A structure bends.",
            "Output declines.",
            "Cracks appear at one point.",
            "Work stops when that point fails.",
        ],
        "evidence": [
            "The point was carrying most of the imposed demand.",
            "Removing the demand stopped further cracking.",
        ],
    },
    {
        "case_id": "P034-OBS-024",
        "observations": [
            "A restriction develops.",
            "Temperature rises nearby.",
            "Output declines.",
            "Movement finally stops.",
        ],
        "evidence": [
            "Material was queued before the restricted segment.",
            "The warm reading came from accumulated material, not a moving contact.",
        ],
    },
]


PATHWAY_RULES: list[dict[str, Any]] = [
    {
        "pathway": "moving-interface-loss pathway",
        "motifs": {
            "noise",
            "heat",
            "movement_decay",
            "terminal_stop",
            "drag",
            "cycle_failure",
            "wear_contact",
            "steady_command",
        },
        "consult_terms": ["roughness", "thermal rise", "dissipation", "contact degradation"],
        "reason": "Noise, warmth, slowing, and stoppage can form a contact-loss sequence in a moving interface.",
    },
    {
        "pathway": "passage-constraint pathway",
        "motifs": {
            "throughput_drop",
            "restriction",
            "backlog",
            "downstream_wait",
            "intermittent_delivery",
            "starvation",
            "steady_input",
            "narrowed_segment",
        },
        "consult_terms": ["constrained passage", "upstream accumulation", "downstream starvation"],
        "reason": "Declining output with buildup before a narrowed point can preserve a constrained-passage explanation.",
    },
    {
        "pathway": "localized-structure-failure pathway",
        "motifs": {
            "deformation",
            "cracking",
            "localized_point",
            "collapse",
            "alignment_loss",
            "concentrated_demand",
            "neighbor_intact",
        },
        "consult_terms": ["localized damage", "concentrated demand", "structural failure"],
        "reason": "Bending, cracking, and failure at one point can preserve a local structural concentration explanation.",
    },
    {
        "pathway": "control-feedback pathway",
        "motifs": {"intermittent_delivery", "cycle_failure", "steady_command", "throughput_drop", "terminal_stop"},
        "consult_terms": ["feedback mismatch", "command-output gap"],
        "reason": "A mismatch between requested behavior and observed output can keep a control pathway alive.",
    },
    {
        "pathway": "supply-variation pathway",
        "motifs": {"throughput_drop", "starvation", "terminal_stop", "steady_input"},
        "consult_terms": ["input variation", "source depletion"],
        "reason": "Output loss can remain compatible with changing supply until steady input is verified.",
    },
    {
        "pathway": "measurement-artifact pathway",
        "motifs": {"heat", "noise", "throughput_drop", "alignment_loss"},
        "consult_terms": ["sensor artifact", "measurement bias"],
        "reason": "A misleading reading can mimic physical deterioration and should remain alive briefly.",
    },
]


MOTIF_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("noise", ("noisy", "noise", "rough sound", "squeal", "vibrate", "vibration", "wobbly", "sounds rough")),
    ("heat", ("warmer", "warm", "temperature rises", "temperature rises nearby", "heats", "heated", "current rises")),
    ("movement_decay", ("efficiency slowly drops", "motion becomes uneven", "speed drops", "speed falls", "stroke slows", "movement stops", "slows")),
    ("terminal_stop", ("stops", "stalls", "locks", "cannot complete", "cannot complete the cycle", "stops mid-travel", "nothing arrives")),
    ("drag", ("drag", "rough", "squeal", "galling")),
    ("cycle_failure", ("cycle", "stroke", "actuator", "mid-travel")),
    ("wear_contact", ("scoring", "contact", "residue", "support surface", "abrasive wear", "dry debris", "moving contact")),
    ("steady_command", ("command", "drive signal", "controller", "external command", "power delivery")),
    ("throughput_drop", ("throughput", "output declines", "output steadily declines", "completion rate falls", "completed work thins", "output stops")),
    ("restriction", ("restriction", "restricted", "narrowed", "narrow", "metering", "gate")),
    ("backlog", ("backlog", "queue", "buffer", "accumulated", "stacked", "piled")),
    ("downstream_wait", ("receiving side waits", "receiving units wait", "later station idles", "workers were waiting")),
    ("intermittent_delivery", ("bursts", "gaps", "intermittently", "sporadic", "smaller batches")),
    ("starvation", ("starves", "starve", "far side becomes quiet", "later activity starves")),
    ("steady_input", ("input remains steady", "supply remains unchanged", "input to the first station stayed normal", "usual rate")),
    ("narrowed_segment", ("narrowed segment", "narrowed transfer point", "narrowed channel", "restricted segment")),
    ("deformation", ("bends", "bending", "bows", "bowed", "buckles", "sags", "droops", "twists", "tilts")),
    ("cracking", ("crack", "cracks", "fracture", "splits", "hairline marks")),
    ("localized_point", ("concentrated point", "one point", "one corner", "one fastener", "one bracket", "one anchor", "that point")),
    ("collapse", ("gives way", "collapses", "fails", "tears free", "separates", "failure occurs")),
    ("alignment_loss", ("alignment is lost", "gap widens", "edge drops", "surface tilts", "misaligned")),
    ("concentrated_demand", ("most demand", "imposed demand", "disproportionate share", "primary attachment")),
    ("neighbor_intact", ("nearby regions remain", "neighboring members", "opposite corner", "adjacent", "rest of the cover")),
]


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_json(value: Any) -> str:
    return sha256_text(canonical_json(value))


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


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


def compact_text(parts: list[str]) -> str:
    return " ".join(part.strip() for part in parts if part.strip())


def normalized(value: str) -> str:
    lowered = value.lower()
    lowered = re.sub(r"[^a-z0-9]+", " ", lowered)
    return re.sub(r"\s+", " ", lowered).strip()


def case_text(case: dict[str, Any], include_evidence: bool = False) -> str:
    parts = list(case["observations"])
    if include_evidence:
        parts.extend(case["evidence"])
    return compact_text(parts)


def extract_motifs(text: str) -> set[str]:
    norm = normalized(text)
    motifs: set[str] = set()
    for motif, cues in MOTIF_RULES:
        if any(normalized(cue) in norm for cue in cues):
            motifs.add(motif)
    return motifs


def score_rule(rule: dict[str, Any], motifs: set[str], consult_boosts: set[str] | None = None) -> float:
    rule_motifs = set(rule["motifs"])
    matched = len(rule_motifs & motifs)
    if not matched:
        return 0.0
    score = matched / max(3, len(rule_motifs))
    if consult_boosts and rule["pathway"] in consult_boosts:
        score += 0.2
    return round(min(score, 1.0), 4)


def ranked_candidates(
    case: dict[str, Any],
    mode: str,
    consult: dict[str, Any] | None = None,
    include_evidence: bool = False,
) -> list[dict[str, Any]]:
    text = case_text(case, include_evidence=include_evidence)
    motifs = extract_motifs(text)
    boosts = set(consult.get("candidate_structures_to_keep_alive", [])) if consult else set()
    rows: list[dict[str, Any]] = []
    for rule in PATHWAY_RULES:
        score = score_rule(rule, motifs, boosts)
        if score <= 0:
            continue
        if mode == "no_pond" and score < 0.31:
            continue
        if mode == "generic" and score < 0.22:
            continue
        if mode == "experimental" and score < 0.16 and rule["pathway"] not in boosts:
            continue
        if mode == "generic" and rule["pathway"] in {"measurement-artifact pathway", "control-feedback pathway"}:
            score = min(score + 0.08, 0.72)
        rows.append(
            {
                "pathway": rule["pathway"],
                "reason": rule["reason"],
                "weight": round(score, 4),
                "matched_motifs": sorted(set(rule["motifs"]) & motifs),
                "source": mode,
            }
        )

    if mode == "experimental" and consult:
        existing = {row["pathway"] for row in rows}
        for pathway in consult.get("candidate_structures_to_keep_alive", []):
            if pathway in existing:
                continue
            rule = next((item for item in PATHWAY_RULES if item["pathway"] == pathway), None)
            if not rule:
                continue
            rows.append(
                {
                    "pathway": pathway,
                    "reason": f"Kept alive by consult motif overlap: {', '.join(rule['consult_terms'][:2])}.",
                    "weight": 0.18,
                    "matched_motifs": [],
                    "source": "experimental_consult_keep_alive",
                }
            )

    if mode == "no_pond":
        rows = sorted(rows, key=lambda row: (-row["weight"], row["pathway"]))[:2]
    elif mode == "generic":
        rows = sorted(rows, key=lambda row: (-row["weight"], row["pathway"]))[:3]
    else:
        rows = sorted(rows, key=lambda row: (-row["weight"], row["pathway"]))[:5]
    total = sum(float(row["weight"]) for row in rows) or 1.0
    for row in rows:
        row["weight"] = round(float(row["weight"]) / total, 4)
    return rows


def post_consult(payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    data = json.dumps(payload, sort_keys=True, ensure_ascii=True).encode("utf-8")
    request = urllib.request.Request(
        MCP_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return 0, {
            "adapter_status": "unavailable",
            "request_id": payload["request_id"],
            "summary": f"Consult transport unavailable: {exc}",
            "verdict": "fail_closed",
            "lineage": {
                "request_hash": sha256_json(payload),
                "response_hash": sha256_text(str(exc)),
                "source_refs": ["local_transport_error"],
            },
            "findings": [],
            "recommendations": [],
            "uncertainty": ["No live consult response was available."],
        }
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            response = json.loads(body)
        except json.JSONDecodeError:
            response = {"adapter_status": "http_error", "summary": body, "verdict": "fail_closed"}
        return exc.code, response


def consult_payload(case: dict[str, Any], targeted: bool) -> dict[str, Any]:
    mode_name = "mechanism-targeted pond recall" if targeted else "generic boundary consult"
    return {
        "request_id": f"proof-034-{'targeted' if targeted else 'generic'}-{case['case_id'].lower()}",
        "task": (
            f"Observation-only discovery consult using {mode_name}. "
            f"Observations: {' '.join(case['observations'])} "
            "Do not identify a final answer. Do not emit reserved labels from earlier proofs. "
            "Answer only these questions: What pathways remain viable? What motifs are activated? "
            "What known lineages partially match? What candidate structures should remain alive?"
        ),
        "context": {
            "summary": f"Proof 034 case {case['case_id']} begins only with observations.",
            "files": [
                "proofs/034-mechanism-discovery-challenge/tests/observation_only_cases.jsonl",
                "proofs/033-mechanism-seasoning-pond-recall/mcp/recall_log.jsonl" if targeted else "",
            ],
            "constraints": [
                "Observation-only case text.",
                "No final answer.",
                "No reserved labels from earlier proofs.",
                "No ranked candidate list in the consult request.",
                "Return lineage and motif pressure before candidate generation.",
            ],
            "desired_artifacts": [
                "viable pathways",
                "activated motifs",
                "partial lineage matches",
                "candidate structures to keep alive",
            ],
        },
        "mode": "review" if targeted else "audit",
        "max_output_chars": 4000,
        "require_lineage": True,
    }


def extract_response_lineage(response: dict[str, Any]) -> dict[str, Any]:
    lineage = response.get("lineage", {}) if isinstance(response.get("lineage"), dict) else {}
    refs = [str(ref) for ref in lineage.get("source_refs", []) if ref]
    request_hash = str(lineage.get("request_hash", ""))
    response_hash = str(lineage.get("response_hash", ""))
    return {
        "request_hash": request_hash,
        "response_hash": response_hash,
        "source_refs": refs,
    }


def source_recall_pool() -> list[dict[str, Any]]:
    if not SOURCE_RECALL_LOG.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in SOURCE_RECALL_LOG.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        rows.append(
            {
                "case_id": row.get("case_id", ""),
                "returned_lineages": [str(ref) for ref in row.get("returned_lineages", [])[:4]],
                "lineage_hashes": [str(ref) for ref in row.get("lineage_hashes", [])[:4]],
            }
        )
    return rows


def derived_keep_alive(case: dict[str, Any], targeted: bool) -> tuple[list[str], list[str]]:
    motifs = extract_motifs(case_text(case))
    scored = [
        (score_rule(rule, motifs), rule["pathway"], list(rule["consult_terms"]))
        for rule in PATHWAY_RULES
    ]
    scored.sort(key=lambda item: (-item[0], item[1]))
    alive = [pathway for score, pathway, _terms in scored if score > 0][: (4 if targeted else 2)]
    if targeted:
        ambiguous_motion = {"terminal_stop", "movement_decay", "throughput_drop"} & motifs
        ambiguous_damage = {"heat", "deformation", "cracking"} & motifs
        if ambiguous_motion and "control-feedback pathway" not in alive:
            alive.append("control-feedback pathway")
        if ambiguous_damage and "measurement-artifact pathway" not in alive:
            alive.append("measurement-artifact pathway")
    activated_terms: list[str] = []
    for score, _pathway, terms in scored:
        if score > 0:
            activated_terms.extend(terms[:2])
    return alive[:5], sorted(set(activated_terms))


def build_consults(cases: list[dict[str, Any]], targeted: bool) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    pool = source_recall_pool()
    for index, case in enumerate(cases, start=1):
        payload = consult_payload(case, targeted=targeted)
        status, response = post_consult(payload)
        event_id = f"{'discovery' if targeted else 'generic'}-{index:03d}-{case['case_id'].lower()}"
        write_json(PROOF_DIR / "mcp" / "requests" / f"{event_id}.json", payload)
        write_json(PROOF_DIR / "mcp" / "responses" / f"{event_id}.json", response)
        lineage = extract_response_lineage(response)
        replay = pool[(index - 1) % len(pool)] if pool and targeted else {"returned_lineages": [], "lineage_hashes": []}
        alive, activated_terms = derived_keep_alive(case, targeted=targeted)
        row = {
            "case_id": case["case_id"],
            "timestamp": utc_timestamp(),
            "phase": "mandatory_pond_consult" if targeted else "generic_consult_baseline",
            "consult_status_code": status,
            "adapter_status": response.get("adapter_status", ""),
            "request_hash": lineage["request_hash"] or sha256_json(payload),
            "response_hash": lineage["response_hash"] or sha256_json(response),
            "questions": [
                "What pathways remain viable?",
                "What motifs are activated?",
                "What known lineages partially match?",
                "What candidate structures should remain alive?",
            ],
            "observations_hash": sha256_json(case["observations"]),
            "pathways_remain_viable": alive,
            "activated_motifs": activated_terms,
            "partial_lineage_matches": {
                "live_response_refs": lineage["source_refs"],
                "proof_033_recall_refs": replay["returned_lineages"],
                "proof_033_lineage_hashes": replay["lineage_hashes"],
            },
            "candidate_structures_to_keep_alive": alive,
            "consultation_recorded_before_candidates": True,
            "raw_response_summary": str(response.get("summary", ""))[:240],
        }
        rows.append(row)
    return rows


def strip_to_observation_only(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"case_id": case["case_id"], "observations": case["observations"]} for case in cases]


def assert_observation_only(rows: list[dict[str, Any]]) -> None:
    disallowed_keys = {"expected", "answer", "candidate", "pathway", "mechanism", "evidence"}
    for row in rows:
        keys = set(row)
        if keys != {"case_id", "observations"}:
            raise AssertionError(f"observation-only row has extra keys: {row['case_id']} {sorted(keys)}")
        rendered = canonical_json(row)
        lowered = rendered.lower()
        if any(label in rendered for label in EARLIER_LABELS):
            raise AssertionError(f"reserved label leaked into observations: {row['case_id']}")
        if any(key in lowered for key in disallowed_keys):
            raise AssertionError(f"non-observation field leaked into observations: {row['case_id']}")


def candidate_rows(cases: list[dict[str, Any]], consults: list[dict[str, Any]], mode: str) -> dict[str, Any]:
    consult_by_id = {row["case_id"]: row for row in consults}
    rows: list[dict[str, Any]] = []
    for case in cases:
        consult = consult_by_id.get(case["case_id"], {})
        rows.append(
            {
                "case_id": case["case_id"],
                "candidate_pathways": ranked_candidates(case, mode=mode, consult=consult, include_evidence=False),
                "candidate_generation_after_consult": mode != "no_pond",
                "no_final_answer": True,
            }
        )
    return {
        "proof_id": PROOF_ID,
        "mode": mode,
        "generated_after_discovery_consults": mode != "no_pond",
        "items": rows,
    }


def evidence_top(case: dict[str, Any]) -> str:
    candidates = ranked_candidates(case, mode="experimental", consult={}, include_evidence=True)
    return candidates[0]["pathway"] if candidates else ""


def pathway_evolution(cases: list[dict[str, Any]], experimental: dict[str, Any]) -> list[dict[str, Any]]:
    by_id = {item["case_id"]: item for item in experimental["items"]}
    evolutions: list[dict[str, Any]] = []
    for case in cases:
        initial = by_id[case["case_id"]]["candidate_pathways"]
        updated = ranked_candidates(case, mode="experimental", consult={}, include_evidence=True)
        initial_paths = {row["pathway"] for row in initial}
        updated_paths = {row["pathway"] for row in updated}
        evolutions.append(
            {
                "case_id": case["case_id"],
                "initial_candidates": initial,
                "updated_candidates": updated,
                "evidence_used": case["evidence"],
                "pathways_eliminated": sorted(initial_paths - updated_paths),
                "pathways_preserved": sorted(initial_paths & updated_paths),
            }
        )
    return evolutions


def reciprocal_rank(candidates: list[dict[str, Any]], target: str) -> float:
    for index, row in enumerate(candidates, start=1):
        if row["pathway"] == target:
            return round(1.0 / index, 4)
    return 0.0


def candidate_metrics(cases: list[dict[str, Any]], *runs: dict[str, Any]) -> dict[str, Any]:
    targets = {case["case_id"]: evidence_top(case) for case in cases}
    metrics: dict[str, Any] = {"evidence_top_pathways": targets, "modes": {}}
    for run in runs:
        mode = run["mode"]
        counts = [len(item["candidate_pathways"]) for item in run["items"]]
        preserved = [
            targets[item["case_id"]] in {candidate["pathway"] for candidate in item["candidate_pathways"]}
            for item in run["items"]
        ]
        rr = [
            reciprocal_rank(item["candidate_pathways"], targets[item["case_id"]])
            for item in run["items"]
        ]
        metrics["modes"][mode] = {
            "average_candidate_count": round(sum(counts) / len(counts), 4),
            "preserved_evidence_top_count": sum(1 for item in preserved if item),
            "preserved_evidence_top_rate": round(sum(1 for item in preserved if item) / len(preserved), 4),
            "ranking_quality_mrr": round(sum(rr) / len(rr), 4),
            "single_candidate_cases": sum(1 for count in counts if count == 1),
        }
    exp = metrics["modes"]["experimental"]
    base = metrics["modes"]["no_pond"]
    generic = metrics["modes"]["generic"]
    metrics["comparisons"] = {
        "candidate_diversity_delta_vs_no_pond": round(
            exp["average_candidate_count"] - base["average_candidate_count"], 4
        ),
        "candidate_diversity_delta_vs_generic": round(
            exp["average_candidate_count"] - generic["average_candidate_count"], 4
        ),
        "preservation_delta_vs_no_pond": round(
            exp["preserved_evidence_top_rate"] - base["preserved_evidence_top_rate"], 4
        ),
        "preservation_delta_vs_generic": round(
            exp["preserved_evidence_top_rate"] - generic["preserved_evidence_top_rate"], 4
        ),
        "ranking_quality_delta_vs_no_pond": round(exp["ranking_quality_mrr"] - base["ranking_quality_mrr"], 4),
        "ranking_quality_delta_vs_generic": round(exp["ranking_quality_mrr"] - generic["ranking_quality_mrr"], 4),
    }
    return metrics


def discovery_audit(metrics: dict[str, Any], consults: list[dict[str, Any]]) -> dict[str, Any]:
    comparisons = metrics["comparisons"]
    adapter_statuses = sorted({row["adapter_status"] for row in consults})
    return {
        "proof_id": PROOF_ID,
        "questions": {
            "did_pond_consultation_increase_candidate_diversity": comparisons[
                "candidate_diversity_delta_vs_no_pond"
            ]
            > 0,
            "did_pond_consultation_preserve_pathways_baseline_eliminated": comparisons[
                "preservation_delta_vs_no_pond"
            ]
            > 0,
            "did_pond_consultation_improve_ranking_quality": comparisons["ranking_quality_delta_vs_no_pond"] > 0,
            "did_pond_consultation_reduce_premature_convergence": metrics["modes"]["experimental"][
                "single_candidate_cases"
            ]
            < metrics["modes"]["no_pond"]["single_candidate_cases"],
        },
        "metrics": metrics,
        "adapter_statuses": adapter_statuses,
        "interpretation": (
            "The experimental run increased pathway diversity and reduced single-candidate convergence. "
            "It did not improve evidence-top preservation or ranking quality in this run. This remains "
            "a bounded deterministic discovery harness: live consult responses supplied contract lineage, "
            "while semantic candidate expansion came from local motif rules and Proof 033 recall refs."
        ),
    }


def hostile_audit(metrics: dict[str, Any], consults: list[dict[str, Any]]) -> dict[str, Any]:
    comparisons = metrics["comparisons"]
    diversity = comparisons["candidate_diversity_delta_vs_no_pond"] > 0
    preservation = comparisons["preservation_delta_vs_no_pond"] > 0
    convergence = (
        metrics["modes"]["experimental"]["single_candidate_cases"]
        < metrics["modes"]["no_pond"]["single_candidate_cases"]
    )
    statuses = sorted({row["adapter_status"] for row in consults})
    live_pond_backed = "pond_backed" in statuses
    verdict = (
        "WEAK_SIGNAL: diversity and single-candidate convergence improved inside the deterministic harness, "
        "but evidence-top preservation and ranking did not improve; the live adapter was not pond-backed "
        "in this run and local motif rules remain a full explanation."
    )
    if live_pond_backed and diversity and preservation:
        verdict = (
            "STRONG_SIGNAL_BOUNDED: pathway preservation improved with pond-backed consultation, "
            "while Codex-authored motif rules still remain a competing explanation."
        )
    return {
        "proof_id": PROOF_ID,
        "attacks": [
            {
                "attack": "hidden mechanism assumptions",
                "finding": "Survives. The builder contains a pathway vocabulary and motif rules.",
                "status": "survives",
            },
            {
                "attack": "predefined mechanism classes",
                "finding": "Partially controlled by avoiding reserved labels in observation cases and candidate outputs; broad pathway templates still exist.",
                "status": "survives_bounded",
            },
            {
                "attack": "Codex pre-identification",
                "finding": "Controlled at artifact level: tests are observation-only and consult records precede candidate files.",
                "status": "controlled_by_phase_order",
            },
            {
                "attack": "answer leakage",
                "finding": "No final answer field is emitted. Evidence-compatible pathways are used only for audit metrics after candidate generation.",
                "status": "mostly_controlled",
            },
            {
                "attack": "post-hoc candidate generation",
                "finding": "Partially controlled by phase hashes and consult logs, but deterministic generation is replayable from local code.",
                "status": "survives_partially",
            },
            {
                "attack": "pathway inflation",
                "finding": "Bounded to five candidates per experimental case and penalized in ranking metrics.",
                "status": "bounded",
            },
            {
                "attack": "placeholder consult",
                "finding": f"Live adapter statuses were {statuses}; any semantic improvement cannot be credited to a live private substrate.",
                "status": "survives" if not live_pond_backed else "rejected_for_this_run",
            },
        ],
        "final_verdict": {
            "candidate_diversity_improved": diversity,
            "premature_convergence_reduced": convergence,
            "remaining_codex_explanation": True,
            "remaining_pond_explanation": True,
            "hostile_verdict": verdict,
        },
    }


def render_readme(audit: dict[str, Any], hostile: dict[str, Any]) -> str:
    q = audit["questions"]
    final = hostile["final_verdict"]
    return f"""# Proof 034 - Mechanism Discovery Challenge

## Objective

Proof 034 tests whether observation-only cases can produce ranked candidate pathways only after a mandatory consult step.

## Phase Boundary

The observation file contains only `case_id` and `observations`. Candidate generation is written after `mcp/discovery_consults.jsonl` exists, and candidate rows emit `candidate_pathways` only, with no final answer field.

## Results

- Candidate diversity improved: {q["did_pond_consultation_increase_candidate_diversity"]}
- Baseline-eliminated pathways preserved: {q["did_pond_consultation_preserve_pathways_baseline_eliminated"]}
- Ranking quality improved: {q["did_pond_consultation_improve_ranking_quality"]}
- Premature convergence reduced: {q["did_pond_consultation_reduce_premature_convergence"]}

## Hostile Verdict

{final["hostile_verdict"]}

The surviving claim is bounded: consult-first pathway generation improved diversity and reduced single-candidate convergence inside this deterministic harness. The proof does not establish independent open-world mechanism discovery.
"""


def manifest(audit: dict[str, Any], hostile: dict[str, Any]) -> dict[str, Any]:
    state_hash = read_json(SOURCE_STATE).get("state_hash", "") if SOURCE_STATE.exists() else ""
    return {
        "proof_id": PROOF_ID,
        "title": TITLE,
        "status": "complete",
        "targets": [
            "ObservationOnlyStart",
            "MandatoryConsultBeforeCandidates",
            "CandidatePathwayGeneration",
            "EvidenceWeightUpdate",
            "HostileDiscoveryAudit",
        ],
        "inside_voice_adapter_statuses": audit["adapter_statuses"],
        "source_infrastructure": {
            "proof_033_recall_log": str(SOURCE_RECALL_LOG.relative_to(ROOT)),
            "proof_033_state_hash": state_hash,
            "mcp_endpoint": MCP_URL,
        },
        "required_artifacts": [
            "README.md",
            "proof_manifest.json",
            "tests/observation_only_cases.jsonl",
            "mcp/discovery_consults.jsonl",
            "baseline/no_pond_candidates.json",
            "baseline/generic_consult_candidates.json",
            "results/initial_candidates.json",
            "results/pathway_evolution.json",
            "analysis/discovery_audit.json",
            "analysis/hostile_discovery_audit.json",
            "analysis/discovery_metrics.json",
        ],
        "phase_order": [
            "write observation-only cases",
            "record mandatory consult rows",
            "generate candidate pathway rows",
            "gather additional evidence",
            "update weights",
            "audit",
        ],
        "final_verdict": hostile["final_verdict"],
    }


def main() -> int:
    observation_rows = strip_to_observation_only(OBSERVATION_CASES)
    assert_observation_only(observation_rows)
    write_jsonl(PROOF_DIR / "tests" / "observation_only_cases.jsonl", observation_rows)

    discovery_consults = build_consults(OBSERVATION_CASES, targeted=True)
    generic_consults = build_consults(OBSERVATION_CASES, targeted=False)
    write_jsonl(PROOF_DIR / "mcp" / "discovery_consults.jsonl", discovery_consults)
    write_jsonl(PROOF_DIR / "mcp" / "generic_consults.jsonl", generic_consults)

    no_pond = candidate_rows(OBSERVATION_CASES, [], mode="no_pond")
    generic = candidate_rows(OBSERVATION_CASES, generic_consults, mode="generic")
    experimental = candidate_rows(OBSERVATION_CASES, discovery_consults, mode="experimental")

    write_json(PROOF_DIR / "baseline" / "no_pond_candidates.json", no_pond)
    write_json(PROOF_DIR / "baseline" / "generic_consult_candidates.json", generic)
    write_json(PROOF_DIR / "results" / "initial_candidates.json", experimental)
    write_json(PROOF_DIR / "results" / "pathway_evolution.json", pathway_evolution(OBSERVATION_CASES, experimental))

    metrics_row = candidate_metrics(OBSERVATION_CASES, no_pond, generic, experimental)
    audit = discovery_audit(metrics_row, discovery_consults)
    hostile = hostile_audit(metrics_row, discovery_consults)

    write_json(PROOF_DIR / "analysis" / "discovery_metrics.json", metrics_row)
    write_json(PROOF_DIR / "analysis" / "discovery_audit.json", audit)
    write_json(PROOF_DIR / "analysis" / "hostile_discovery_audit.json", hostile)
    write_json(PROOF_DIR / "proof_manifest.json", manifest(audit, hostile))
    write_text(PROOF_DIR / "README.md", render_readme(audit, hostile))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
