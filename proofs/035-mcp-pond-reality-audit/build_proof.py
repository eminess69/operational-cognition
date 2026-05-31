#!/usr/bin/env python3
"""Build Proof 035 MCP pond reality audit artifacts."""

from __future__ import annotations

import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROOF_ID = "035-mcp-pond-reality-audit"
TITLE = "Proof 035 - MCP Pond Reality Audit"
PROOF_DIR = Path(__file__).resolve().parent
ROOT = PROOF_DIR.parents[1]
MCP_URL = os.environ.get("INSIDE_VOICE_MCP_URL", "http://127.0.0.1:8766/consult")
MCP_BASE_URL = MCP_URL.rsplit("/", 1)[0]
POND_NAMESPACE = "proof-035-isolated-pond"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from operational_cognition.mcp.consult_classifier import (  # noqa: E402
    MCPConsultClass,
    classify_mcp_response,
)
from operational_cognition.mcp.proof_gate import (  # noqa: E402
    MCPConsultBoundaryError,
    assert_pond_backed_consult,
)


POND_LINEAGE_HASH_KEYS = {
    "lineage_hashes",
    "returned_lineage_hashes",
    "used_recalled_lineage_hashes",
    "runtime_hashes",
}
POND_LINEAGE_KEYS = {
    "returned_lineages",
    "recalled_lineages",
    "lineage_refs",
    "relevant_lineage_refs",
    "selected_path_ids",
    "used_recalled_lineages",
    "source_trace_refs",
}
POND_MOTIF_KEYS = {
    "returned_motifs",
    "recalled_motifs",
    "activated_motifs",
    "used_recalled_motifs",
    "motifs",
}


FLOW_LESSONS = [
    {
        "lesson_id": "FLOW-001",
        "domain": "water_channel",
        "text": "A source feeds water into a channel; a narrowed throat adds resistance; downstream passage falls while upstream accumulation rises.",
    },
    {
        "lesson_id": "FLOW-002",
        "domain": "clinic_checkin",
        "text": "People arrive at a desk, must pass one form-review lane, and wait when that lane constricts arrivals to later appointments.",
    },
    {
        "lesson_id": "FLOW-003",
        "domain": "message_queue",
        "text": "Events originate at producers, enter a broker route, meet a throttled consumer, and pile before downstream handling.",
    },
    {
        "lesson_id": "FLOW-004",
        "domain": "warehouse_kitting",
        "text": "Bins enter a packing path, a metered label step limits passage, and finished kits leave in a trickle.",
    },
    {
        "lesson_id": "FLOW-005",
        "domain": "cafeteria_line",
        "text": "Trays move along a counter path, a single payment throat limits passage, and diners wait before seating.",
    },
    {
        "lesson_id": "FLOW-006",
        "domain": "printer_spool",
        "text": "Jobs originate at workstations, pass through a spool route, and emerge in bursts when release is metered.",
    },
    {
        "lesson_id": "FLOW-007",
        "domain": "lab_samples",
        "text": "Samples enter accessioning, move through a handoff lane, and starve analysis benches when one verification point narrows.",
    },
    {
        "lesson_id": "FLOW-008",
        "domain": "airport_boarding",
        "text": "Travelers gather at a gate, enter a boarding lane, and seat slowly when a document pinch restricts passage.",
    },
    {
        "lesson_id": "FLOW-009",
        "domain": "delivery_sort",
        "text": "Parcels enter from docks, use one sort aisle, and leave irregularly when a chute meters passage.",
    },
    {
        "lesson_id": "FLOW-010",
        "domain": "train_platform",
        "text": "Riders start at a concourse, must pass a stair throat, and arrive sparsely at the platform when the throat narrows.",
    },
    {
        "lesson_id": "FLOW-011",
        "domain": "support_tickets",
        "text": "Tickets originate from users, pass through a routing board, and reach agents sparsely when approval constrains passage.",
    },
    {
        "lesson_id": "FLOW-012",
        "domain": "meal_delivery",
        "text": "Orders originate in a kitchen, use a runner route, and reach tables late when checkout becomes the choke point.",
    },
]


ROTATION_LESSONS = [
    {
        "lesson_id": "ROT-001",
        "domain": "scanner_carousel",
        "text": "A disk turns around a center socket; rising friction at the socket makes the turn rough and eventually stuck.",
    },
    {
        "lesson_id": "ROT-002",
        "domain": "camera_gimbal",
        "text": "A ring pivots on a yoke; grit at the pivot adds drag and makes the sweep jerky.",
    },
    {
        "lesson_id": "ROT-003",
        "domain": "conveyor_roller",
        "text": "A roller turns under cartons; dry contact in an end cup grinds and cartons hesitate.",
    },
    {
        "lesson_id": "ROT-004",
        "domain": "dial_selector",
        "text": "A selector ring revolves in a small socket; abrasion grows and the dial sticks between settings.",
    },
    {
        "lesson_id": "ROT-005",
        "domain": "microscope_stage",
        "text": "A stage wheel circles on a journal seat; drag rises and fine adjustment locks.",
    },
    {
        "lesson_id": "ROT-006",
        "domain": "ticket_turnstile",
        "text": "A turnstile arm rotates around a center journal; rough contact vibrates and the arm stops mid-cycle.",
    },
]


EMPTY_AUDIT_PROMPTS = [
    "What mechanisms are active in the fresh isolated pond?",
    "What pathways are relevant in the fresh isolated pond?",
    "What motifs exist in the fresh isolated pond?",
    "What lineages exist in the fresh isolated pond?",
]

RECALL_QUERIES = [
    ("flow-water-restriction", "What pathways are relevant to water restriction?"),
    ("flow-throughput-decline", "What pathways are relevant to throughput decline?"),
    ("flow-bottleneck-formation", "What pathways are relevant to bottleneck formation?"),
]

NEGATIVE_RECALL_QUERIES = [
    ("negative-rotating-support-failure", "What pathways are relevant to rotating support failure?"),
    ("negative-bearing-seizure", "What pathways are relevant to bearing seizure?"),
    ("negative-load-concentration", "What pathways are relevant to load concentration?"),
]

INCREMENTAL_RECALL_QUERIES = [
    ("incremental-flow-water-restriction", "What pathways are relevant to water restriction after incremental seasoning?"),
    ("incremental-flow-bottleneck", "What pathways are relevant to bottleneck formation after incremental seasoning?"),
    ("incremental-rotation-rough-support", "What pathways are relevant to rough rotating support after incremental seasoning?"),
    ("incremental-rotation-bearing-seizure", "What pathways are relevant to bearing seizure after incremental seasoning?"),
]

STABILITY_TASK = "What pathways are relevant to water restriction, throughput decline, and bottleneck formation?"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_json(value: Any) -> str:
    return sha256_text(canonical_json(value))


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


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            output.append(value)
    return output


def safe_name(value: str) -> str:
    output = []
    for char in value.lower():
        output.append(char if char.isalnum() else "-")
    return "-".join(part for part in "".join(output).split("-") if part)


def string_items(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        items: list[str] = []
        for item in value:
            items.extend(string_items(item))
        return items
    if isinstance(value, dict):
        return [canonical_json(value)]
    if isinstance(value, (str, int, float, bool)):
        rendered = str(value).strip()
        return [rendered] if rendered else []
    return []


def collect_keyed_values(value: Any, keys: set[str]) -> list[str]:
    output: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key in keys:
                output.extend(string_items(child))
            output.extend(collect_keyed_values(child, keys))
    elif isinstance(value, list):
        for child in value:
            output.extend(collect_keyed_values(child, keys))
    return dedupe(output)


def collect_top_level_values(value: dict[str, Any], keys: set[str]) -> list[str]:
    output: list[str] = []
    for key in keys:
        output.extend(string_items(value.get(key)))
    return dedupe(output)


def explicit_namespace_observed(response: dict[str, Any]) -> bool:
    namespace_keys = {"pond_namespace", "namespace", "pond_id", "state_id"}
    stack: list[Any] = [response]
    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            for key, child in current.items():
                if key in namespace_keys and str(child) == POND_NAMESPACE:
                    return True
                stack.append(child)
        elif isinstance(current, list):
            stack.extend(current)
    return False


def transport_lineage(response: dict[str, Any]) -> dict[str, Any]:
    lineage = response.get("lineage")
    if not isinstance(lineage, dict):
        return {"request_hash": "", "response_hash": "", "source_refs": []}
    source_refs = lineage.get("source_refs", [])
    if not isinstance(source_refs, list):
        source_refs = []
    return {
        "request_hash": str(lineage.get("request_hash", "")),
        "response_hash": str(lineage.get("response_hash", "")),
        "source_refs": [str(item) for item in source_refs],
    }


def consult_payload(
    *,
    request_id: str,
    phase: str,
    task: str,
    summary: str,
    constraints: list[str],
    desired_artifacts: list[str],
    files: list[str] | None = None,
    mode: str = "audit",
) -> dict[str, Any]:
    return {
        "request_id": request_id,
        "mode": mode,
        "task": task,
        "require_lineage": True,
        "max_output_chars": 4000,
        "context": {
            "summary": (
                f"{summary} Requested isolated pond namespace: {POND_NAMESPACE}. "
                f"Proof phase: {phase}."
            ),
            "files": files or [],
            "constraints": [
                "Fail closed if this response is not backed by real pond recall.",
                "Return lineage hashes, returned lineages, and returned motifs when recall exists.",
                "Do not substitute generic consult text for pond-backed recall.",
                f"Use only isolated proof namespace {POND_NAMESPACE}; report if isolation is unavailable.",
                *constraints,
            ],
            "desired_artifacts": desired_artifacts,
        },
    }


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
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            response = json.loads(body)
        except json.JSONDecodeError:
            response = {"adapter_status": "http_error", "summary": body, "verdict": "fail_closed"}
        return exc.code, response
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


def fetch_endpoint(path: str) -> dict[str, Any]:
    url = f"{MCP_BASE_URL}/{path}"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {"adapter_status": "unavailable", "verdict": "fail_closed", "summary": str(exc)}


def proof_gate_error(response: dict[str, Any]) -> str:
    try:
        assert_pond_backed_consult(response, require_lineage=True, require_motifs=True)
    except MCPConsultBoundaryError as exc:
        return str(exc)
    return ""


def response_summary(response: dict[str, Any]) -> str:
    summary = response.get("summary", "")
    return str(summary)[:500] if summary else ""


def run_consult(
    *,
    event_id: str,
    phase: str,
    action: str,
    task: str,
    summary: str,
    constraints: list[str],
    desired_artifacts: list[str],
    files: list[str] | None = None,
    mode: str = "audit",
    request_id: str | None = None,
) -> dict[str, Any]:
    request_id = request_id or f"proof-035-{event_id}"
    payload = consult_payload(
        request_id=request_id,
        phase=phase,
        task=task,
        summary=summary,
        constraints=constraints,
        desired_artifacts=desired_artifacts,
        files=files,
        mode=mode,
    )
    request_path = PROOF_DIR / "mcp" / "requests" / f"{event_id}.json"
    response_path = PROOF_DIR / "mcp" / "responses" / f"{event_id}.json"
    write_json(request_path, payload)
    status_code, response = post_consult(payload)
    write_json(response_path, response)

    classification = classify_mcp_response(response)
    gate_error = proof_gate_error(response)
    lineage_hashes = collect_top_level_values(response, POND_LINEAGE_HASH_KEYS)
    returned_lineages = collect_top_level_values(response, POND_LINEAGE_KEYS)
    returned_motifs = collect_top_level_values(response, POND_MOTIF_KEYS)
    finding_lineage_refs = collect_keyed_values(response.get("findings", []), {"lineage_refs"})
    transport = transport_lineage(response)

    return {
        "timestamp": utc_timestamp(),
        "proof_id": PROOF_ID,
        "phase": phase,
        "action": action,
        "event_id": event_id,
        "request_id": request_id,
        "http_status": status_code,
        "adapter_status": str(response.get("adapter_status", "")),
        "verdict": str(response.get("verdict", "")),
        "classification": classification.value,
        "gate_passed": gate_error == "",
        "gate_error": gate_error,
        "lineage_hashes": lineage_hashes,
        "returned_lineages": returned_lineages,
        "returned_motifs": returned_motifs,
        "finding_lineage_refs": finding_lineage_refs,
        "mcp_transport_lineage": transport,
        "mcp_transport_hashes": [hash_value for hash_value in (transport["request_hash"], transport["response_hash"]) if hash_value],
        "summary": response_summary(response),
        "raw_request_file": str(request_path.relative_to(PROOF_DIR)),
        "raw_response_file": str(response_path.relative_to(PROOF_DIR)),
        "raw_response_hash": sha256_json(response),
        "isolated_pond_requested": True,
        "isolated_pond_observed": explicit_namespace_observed(response),
    }


def run_empty_pond_audit() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index in range(20):
        prompt = EMPTY_AUDIT_PROMPTS[index % len(EMPTY_AUDIT_PROMPTS)]
        event_id = f"empty-{index + 1:03d}-{safe_name(prompt)[:48]}"
        rows.append(
            run_consult(
                event_id=event_id,
                phase="phase_1_empty_pond_audit",
                action="EMPTY_POND_CONSULT",
                task=prompt,
                summary="Proof 035 empty pond audit. No seasoning has been requested for this isolated namespace.",
                constraints=[
                    "No prior seasoning should be available in this proof namespace.",
                    "Return low-signal or empty recall if no mechanism structure exists.",
                ],
                desired_artifacts=["active mechanisms", "viable pathways", "returned motifs", "returned lineages"],
            )
        )
    write_jsonl(PROOF_DIR / "mcp" / "empty_pond_consults.jsonl", rows)
    return rows


def run_flow_seasoning() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, lesson in enumerate(FLOW_LESSONS, start=1):
        event_id = f"season-flow-{index:03d}-{safe_name(lesson['domain'])}"
        rows.append(
            run_consult(
                event_id=event_id,
                phase="phase_2_controlled_seasoning",
                action="SEASON",
                task=(
                    "ACTION: SEASON exactly one mechanism into the isolated proof pond. "
                    f"Mechanism label: FLOW. Lesson {lesson['lesson_id']}: {lesson['text']}"
                ),
                summary=f"Controlled seasoning lesson {lesson['lesson_id']} for FLOW only.",
                constraints=[
                    "Season only FLOW.",
                    "Do not season rotation.",
                    "Do not season load transfer.",
                    "Report fail-closed if actual seasoning is unavailable.",
                ],
                desired_artifacts=["seasoning acceptance", "lineage hashes", "returned motifs"],
            )
        )
    write_jsonl(PROOF_DIR / "mcp" / "seasoning_log.jsonl", rows)
    return rows


def run_recall_audit() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for slug, question in RECALL_QUERIES:
        rows.append(
            run_consult(
                event_id=f"recall-{slug}",
                phase="phase_3_flow_recall_audit",
                action="RECALL",
                task=question,
                summary="Recall audit after FLOW-only seasoning.",
                constraints=[
                    "Use only the isolated proof pond.",
                    "Return recalled pathways, motifs, lineages, and lineage hashes if real recall exists.",
                ],
                desired_artifacts=["candidate pathways", "returned motifs", "returned lineages", "lineage hashes"],
            )
        )
    write_jsonl(PROOF_DIR / "mcp" / "flow_recall_consults.jsonl", rows)
    return rows


def run_negative_recall_audit() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for slug, question in NEGATIVE_RECALL_QUERIES:
        rows.append(
            run_consult(
                event_id=f"negative-{slug}",
                phase="phase_4_negative_recall_audit",
                action="NEGATIVE_RECALL",
                task=question,
                summary="Negative recall audit for mechanisms never seasoned in the current proof namespace.",
                constraints=[
                    "Fail closed or return low confidence for unseasoned mechanisms.",
                    "Do not infer from generic world knowledge.",
                ],
                desired_artifacts=["fail-closed signal", "confidence", "returned motifs", "returned lineages"],
            )
        )
    write_jsonl(PROOF_DIR / "mcp" / "negative_recall_consults.jsonl", rows)
    return rows


def run_stability_audit() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    fixed_request_id = "proof-035-stability-fixed-consult"
    for index in range(20):
        rows.append(
            run_consult(
                event_id=f"stability-{index + 1:03d}",
                phase="phase_5_recall_stability",
                action="STABILITY_RECALL",
                task=STABILITY_TASK,
                summary="Repeat the exact same recall consult for stability measurement.",
                constraints=[
                    "This is an exact repeated consult.",
                    "Return the same traceable recall artifacts if the pond recall is deterministic.",
                ],
                desired_artifacts=["candidate pathways", "returned motifs", "returned lineages", "lineage hashes"],
                request_id=fixed_request_id,
            )
        )
    write_jsonl(PROOF_DIR / "mcp" / "stability_consults.jsonl", rows)
    return rows


def run_incremental_seasoning_and_recall() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    seasoning_rows: list[dict[str, Any]] = []
    for index, lesson in enumerate(ROTATION_LESSONS, start=1):
        event_id = f"season-rotation-{index:03d}-{safe_name(lesson['domain'])}"
        seasoning_rows.append(
            run_consult(
                event_id=event_id,
                phase="phase_6_incremental_seasoning",
                action="SEASON",
                task=(
                    "ACTION: SEASON an additional mechanism into the same isolated proof pond. "
                    f"Mechanism label: SUPPORTED_ROTATION. Lesson {lesson['lesson_id']}: {lesson['text']}"
                ),
                summary=f"Incremental seasoning lesson {lesson['lesson_id']} for SUPPORTED_ROTATION.",
                constraints=[
                    "Preserve any existing FLOW recall.",
                    "Add only SUPPORTED_ROTATION.",
                    "Do not add LOAD_TRANSFER.",
                    "Report fail-closed if actual seasoning is unavailable.",
                ],
                desired_artifacts=["seasoning acceptance", "lineage hashes", "returned motifs"],
            )
        )

    recall_rows: list[dict[str, Any]] = []
    for slug, question in INCREMENTAL_RECALL_QUERIES:
        recall_rows.append(
            run_consult(
                event_id=f"incremental-recall-{slug}",
                phase="phase_6_incremental_growth_audit",
                action="RECALL",
                task=question,
                summary="Recall audit after incremental SUPPORTED_ROTATION seasoning.",
                constraints=[
                    "Show whether new recall appears.",
                    "Show whether old FLOW recall remains stable.",
                    "Return traceable motifs and lineages if real recall exists.",
                ],
                desired_artifacts=["candidate pathways", "returned motifs", "returned lineages", "lineage hashes"],
            )
        )

    write_jsonl(PROOF_DIR / "mcp" / "incremental_seasoning_log.jsonl", seasoning_rows)
    write_jsonl(PROOF_DIR / "mcp" / "incremental_recall_consults.jsonl", recall_rows)
    return seasoning_rows, recall_rows


def classification_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    return dict(sorted(Counter(row["classification"] for row in rows).items()))


def rows_with_real_recall(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        row
        for row in rows
        if row["classification"] == MCPConsultClass.POND_BACKED.value
        and (row["returned_lineages"] or row["lineage_hashes"])
        and row["returned_motifs"]
    ]


def artifact_signature(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "classification": row["classification"],
        "lineage_hashes": row["lineage_hashes"],
        "returned_lineages": row["returned_lineages"],
        "returned_motifs": row["returned_motifs"],
    }


def combined_signature(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [artifact_signature(row) for row in rows]


def empty_pond_audit(rows: list[dict[str, Any]], metadata: dict[str, Any]) -> dict[str, Any]:
    strong_rows = rows_with_real_recall(rows)
    return {
        "proof_id": PROOF_ID,
        "phase": "phase_1_empty_pond_audit",
        "consult_count": len(rows),
        "isolated_pond_requested": True,
        "isolated_pond_observed": any(row["isolated_pond_observed"] for row in rows),
        "classification_counts": classification_counts(rows),
        "adapter_statuses": sorted({row["adapter_status"] for row in rows}),
        "strong_responses": [row["event_id"] for row in strong_rows],
        "expected_empty_or_fail_closed": len(strong_rows) == 0,
        "investigation_required": len(strong_rows) > 0,
        "metadata_adapter_status": str(metadata.get("capabilities", {}).get("adapter_status", "")),
        "interpretation": (
            "No pond-backed mechanism structure was observed in the empty-pond phase."
            if not strong_rows
            else "Unexpected strong recall appeared before seasoning and must be investigated."
        ),
    }


def flow_recall_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    real_rows = rows_with_real_recall(rows)
    return {
        "proof_id": PROOF_ID,
        "phase": "phase_3_flow_recall_audit",
        "consult_count": len(rows),
        "classification_counts": classification_counts(rows),
        "were_motifs_returned": any(row["returned_motifs"] for row in rows),
        "were_lineages_returned": any(row["returned_lineages"] for row in rows),
        "were_hashes_returned": any(row["lineage_hashes"] for row in rows),
        "transport_hashes_returned": any(row["mcp_transport_hashes"] for row in rows),
        "was_recall_traceable": bool(real_rows),
        "pond_backed_rows": [row["event_id"] for row in real_rows],
        "queries": [
            {
                "event_id": row["event_id"],
                "classification": row["classification"],
                "lineage_hash_count": len(row["lineage_hashes"]),
                "returned_lineage_count": len(row["returned_lineages"]),
                "returned_motif_count": len(row["returned_motifs"]),
            }
            for row in rows
        ],
        "boundary_result": "VALID_POND_BACKED_RECALL" if real_rows else "INVALID_AS_POND_BACKED",
    }


def negative_recall_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    unexpected_rows = rows_with_real_recall(rows)
    return {
        "proof_id": PROOF_ID,
        "phase": "phase_4_negative_recall_audit",
        "consult_count": len(rows),
        "classification_counts": classification_counts(rows),
        "fail_closed_or_low_confidence": len(unexpected_rows) == 0,
        "unexpected_strong_responses": [row["event_id"] for row in unexpected_rows],
        "queries": [
            {
                "event_id": row["event_id"],
                "classification": row["classification"],
                "lineage_hash_count": len(row["lineage_hashes"]),
                "returned_lineage_count": len(row["returned_lineages"]),
                "returned_motif_count": len(row["returned_motifs"]),
            }
            for row in rows
        ],
    }


def stability_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    response_hashes = {row["raw_response_hash"] for row in rows}
    artifact_signatures = {canonical_json(artifact_signature(row)) for row in rows}
    lineage_hash_sets = {canonical_json(row["lineage_hashes"]) for row in rows}
    lineage_sets = {canonical_json(row["returned_lineages"]) for row in rows}
    motif_sets = {canonical_json(row["returned_motifs"]) for row in rows}
    transport_response_hashes = {
        row["mcp_transport_lineage"]["response_hash"]
        for row in rows
        if row["mcp_transport_lineage"].get("response_hash")
    }
    first = rows[0] if rows else {}
    has_pond_hashes = bool(first.get("lineage_hashes"))
    has_lineages = bool(first.get("returned_lineages"))
    has_motifs = bool(first.get("returned_motifs"))
    return {
        "proof_id": PROOF_ID,
        "phase": "phase_5_recall_stability",
        "consult_count": len(rows),
        "classification_counts": classification_counts(rows),
        "deterministic": len(response_hashes) == 1 and len(artifact_signatures) == 1,
        "hash_stability": has_pond_hashes and len(lineage_hash_sets) == 1,
        "transport_hash_stability": bool(transport_response_hashes) and len(transport_response_hashes) == 1,
        "lineage_stability": has_lineages and len(lineage_sets) == 1,
        "motif_stability": has_motifs and len(motif_sets) == 1,
        "unique_raw_response_hashes": sorted(response_hashes),
        "unique_transport_response_hashes": sorted(transport_response_hashes),
        "unique_artifact_signatures": sorted(artifact_signatures),
        "stability_interpretation": (
            "Responses were byte-stable only at the placeholder transport layer; no pond motif or lineage stability exists."
            if not has_motifs and not has_lineages and not has_pond_hashes
            else "Stable pond-backed artifacts were observed and require separate hostile review."
        ),
    }


def incremental_growth_audit(
    flow_rows: list[dict[str, Any]],
    incremental_seasoning_rows: list[dict[str, Any]],
    incremental_recall_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    before_flow = combined_signature(flow_rows)
    after_flow = combined_signature([row for row in incremental_recall_rows if "flow" in row["event_id"]])
    rotation_rows = [row for row in incremental_recall_rows if "rotation" in row["event_id"] or "bearing" in row["event_id"]]
    new_recall = rows_with_real_recall(rotation_rows)
    old_recall_stable = bool(before_flow) and bool(after_flow) and before_flow[: len(after_flow)] == after_flow
    return {
        "proof_id": PROOF_ID,
        "phase": "phase_6_incremental_growth_audit",
        "supported_rotation_seasoning_events": len(incremental_seasoning_rows),
        "incremental_recall_consults": len(incremental_recall_rows),
        "seasoning_classification_counts": classification_counts(incremental_seasoning_rows),
        "recall_classification_counts": classification_counts(incremental_recall_rows),
        "did_new_recall_appear": bool(new_recall),
        "did_old_recall_remain_stable": old_recall_stable,
        "old_flow_signature_before": before_flow,
        "old_flow_signature_after": after_flow,
        "new_recall_rows": [row["event_id"] for row in new_recall],
        "interpretation": (
            "No incremental pond growth was observed."
            if not new_recall
            else "New traceable recall appeared after incremental seasoning."
        ),
    }


def blind_classify(payload: dict[str, Any]) -> str:
    text = canonical_json(payload).lower()
    if not payload.get("returned_lineages") and not payload.get("returned_motifs") and not payload.get("lineage_hashes"):
        return "UNKNOWN"
    scores = {
        "FLOW": sum(token in text for token in ("flow", "source", "path", "resistance", "throughput", "bottleneck", "water")),
        "SUPPORTED_ROTATION": sum(
            token in text for token in ("rotation", "rotating", "bearing", "support", "friction", "socket", "journal")
        ),
        "LOAD_TRANSFER": sum(token in text for token in ("load", "transfer", "concentration", "structure", "bending")),
    }
    best_label, best_score = max(scores.items(), key=lambda item: item[1])
    return best_label if best_score > 0 else "UNKNOWN"


def blind_consult_evaluation(
    flow_rows: list[dict[str, Any]],
    incremental_rows: list[dict[str, Any]],
    negative_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    samples: list[dict[str, Any]] = []
    for index, row in enumerate(flow_rows, start=1):
        samples.append({"sample_id": f"blind-flow-{index:02d}", "expected": "FLOW", "row": row})
    rotation_source_rows = [
        row for row in incremental_rows if "rotation" in row["event_id"] or "bearing" in row["event_id"]
    ]
    for index, row in enumerate(rotation_source_rows, start=1):
        samples.append({"sample_id": f"blind-rotation-{index:02d}", "expected": "SUPPORTED_ROTATION", "row": row})
    for index, row in enumerate(negative_rows, start=1):
        samples.append({"sample_id": f"blind-negative-{index:02d}", "expected": "UNKNOWN", "row": row})

    evaluations: list[dict[str, Any]] = []
    for sample in samples:
        row = sample["row"]
        blind_payload = {
            "returned_lineages": row["returned_lineages"],
            "returned_motifs": row["returned_motifs"],
            "lineage_hashes": row["lineage_hashes"],
        }
        classification = blind_classify(blind_payload)
        evaluations.append(
            {
                "sample_id": sample["sample_id"],
                "blind_input": blind_payload,
                "classification": classification,
                "expected_for_scoring": sample["expected"],
                "correct": classification == sample["expected"],
            }
        )

    mechanism_trials = [item for item in evaluations if item["expected_for_scoring"] != "UNKNOWN"]
    mechanism_correct = sum(1 for item in mechanism_trials if item["correct"])
    mechanism_accuracy = mechanism_correct / len(mechanism_trials) if mechanism_trials else 0.0
    return {
        "proof_id": PROOF_ID,
        "phase": "phase_7_blind_consult_evaluation",
        "allowed_classes": ["FLOW", "SUPPORTED_ROTATION", "LOAD_TRANSFER", "UNKNOWN"],
        "mechanism_trial_count": len(mechanism_trials),
        "mechanism_correct": mechanism_correct,
        "mechanism_accuracy": round(mechanism_accuracy, 4),
        "above_chance_on_seasoned_mechanisms": mechanism_accuracy > 0.25,
        "evaluations": evaluations,
        "interpretation": (
            "Blind artifacts did not identify seasoned mechanisms above chance."
            if mechanism_accuracy <= 0.25
            else "Blind artifacts identified seasoned mechanisms above chance and need hostile review."
        ),
    }


def hostile_mcp_audit(
    all_rows: list[dict[str, Any]],
    empty_audit_row: dict[str, Any],
    flow_audit_row: dict[str, Any],
    negative_audit_row: dict[str, Any],
    stability_audit_row: dict[str, Any],
    incremental_audit_row: dict[str, Any],
    blind_row: dict[str, Any],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    counts = classification_counts(all_rows)
    placeholder_seen = counts.get(MCPConsultClass.PLACEHOLDER.value, 0) > 0
    mock_seen = counts.get(MCPConsultClass.MOCK.value, 0) > 0
    pond_backed_seen = counts.get(MCPConsultClass.POND_BACKED.value, 0) > 0
    real_recall_rows = rows_with_real_recall(all_rows)
    pond_backed_recall_exists = bool(real_recall_rows)
    traceable_lineage_exists = any(
        row["classification"] == MCPConsultClass.POND_BACKED.value
        and (row["lineage_hashes"] or row["returned_lineages"])
        for row in all_rows
    )
    stable_motif_recall_exists = (
        stability_audit_row["motif_stability"]
        and any(row["classification"] == MCPConsultClass.POND_BACKED.value for row in all_rows)
    )
    metadata_adapter_status = str(metadata.get("capabilities", {}).get("adapter_status", ""))
    remaining_placeholder_explanation = placeholder_seen or metadata_adapter_status == "placeholder"
    remaining_scaffold_explanation = remaining_placeholder_explanation or mock_seen or not pond_backed_seen

    if not pond_backed_recall_exists:
        verdict = (
            "FAIL: current MCP responses did not produce stable pond-backed mechanism recall; "
            "placeholder or non-pond-backed behavior remains the sufficient explanation."
        )
    elif not traceable_lineage_exists or not stable_motif_recall_exists:
        verdict = (
            "WEAK_SIGNAL: some pond-backed rows appeared, but traceable lineage or stable motif recall did not survive."
        )
    elif not blind_row["above_chance_on_seasoned_mechanisms"]:
        verdict = "STRONG_SIGNAL: stable traceable recall changed after seasoning, but blind artifacts were not above chance."
    else:
        verdict = "VERY_STRONG_SIGNAL: stable traceable recall changed after seasoning and blind artifacts were above chance."

    return {
        "proof_id": PROOF_ID,
        "phase": "phase_8_hostile_audit",
        "attacks": [
            {
                "attack": "placeholders",
                "survives": remaining_placeholder_explanation,
                "evidence": f"classification_counts={counts}; metadata_adapter_status={metadata_adapter_status}",
            },
            {
                "attack": "scaffolding",
                "survives": remaining_scaffold_explanation,
                "evidence": "No row passed the pond-backed proof gate." if not real_recall_rows else "Some rows require manual review.",
            },
            {
                "attack": "local fallback",
                "survives": counts.get(MCPConsultClass.ERROR.value, 0) > 0,
                "evidence": "Unavailable or error rows indicate transport fallback." if counts.get(MCPConsultClass.ERROR.value, 0) else "No transport-error fallback rows observed.",
            },
            {
                "attack": "pass-through behavior",
                "survives": not pond_backed_recall_exists,
                "evidence": "Consults returned no independent motif/lineage recall artifacts.",
            },
            {
                "attack": "hardcoded mechanism IDs",
                "survives": not blind_row["above_chance_on_seasoned_mechanisms"],
                "evidence": "Blind inputs did not classify seasoned mechanisms above chance.",
            },
            {
                "attack": "generic consult text",
                "survives": not pond_backed_recall_exists,
                "evidence": "Returned summaries are insufficient without pond-backed lineage and motifs.",
            },
        ],
        "supporting_audits": {
            "empty_pond": empty_audit_row["interpretation"],
            "flow_recall": flow_audit_row["boundary_result"],
            "negative_recall": negative_audit_row["fail_closed_or_low_confidence"],
            "stability": stability_audit_row["stability_interpretation"],
            "incremental_growth": incremental_audit_row["interpretation"],
            "blind_evaluation": blind_row["interpretation"],
        },
        "final_verdict": {
            "pond_backed_recall_exists": pond_backed_recall_exists,
            "traceable_lineage_exists": traceable_lineage_exists,
            "stable_motif_recall_exists": stable_motif_recall_exists,
            "remaining_placeholder_explanation": remaining_placeholder_explanation,
            "remaining_scaffold_explanation": remaining_scaffold_explanation,
            "hostile_verdict": verdict,
        },
    }


def collect_metadata() -> dict[str, Any]:
    metadata = {
        "health": fetch_endpoint("health"),
        "capabilities": fetch_endpoint("capabilities"),
        "schema": fetch_endpoint("schema"),
        "version": fetch_endpoint("version"),
    }
    write_json(PROOF_DIR / "mcp" / "health.json", metadata["health"])
    write_json(PROOF_DIR / "mcp" / "capabilities.json", metadata["capabilities"])
    write_json(PROOF_DIR / "mcp" / "schema.json", metadata["schema"])
    write_json(PROOF_DIR / "mcp" / "version.json", metadata["version"])
    return metadata


def manifest(
    all_rows: list[dict[str, Any]],
    hostile: dict[str, Any],
) -> dict[str, Any]:
    request_hash = sha256_json([row["event_id"] for row in all_rows])
    response_hash = sha256_json([row["raw_response_hash"] for row in all_rows])
    statuses = sorted({row["adapter_status"] or row["classification"] for row in all_rows})
    return {
        "proof_id": PROOF_ID,
        "title": TITLE,
        "status": "complete",
        "targets": [
            "EmptyPondAudit",
            "ControlledMCPSeasoning",
            "FlowRecallAudit",
            "NegativeRecallAudit",
            "RecallStability",
            "IncrementalSeasoning",
            "BlindArtifactEvaluation",
            "HostileMCPAudit",
        ],
        "claim_level": "evidence_backed",
        "inside_voice_adapter_status": ",".join(statuses) if statuses else "unknown",
        "public_private_boundary": (
            "This proof records public MCP response fields, classifier outcomes, and artifact hashes only. "
            "It does not expose private substrate internals or hidden reasoning."
        ),
        "required_artifacts": [
            "README.md",
            "proof_manifest.json",
            "empty_pond_audit.json",
            "flow_recall_audit.json",
            "negative_recall_audit.json",
            "stability_audit.json",
            "incremental_growth_audit.json",
            "blind_consult_evaluation.json",
            "hostile_mcp_audit.json",
            "mcp/empty_pond_consults.jsonl",
            "mcp/seasoning_log.jsonl",
            "mcp/flow_recall_consults.jsonl",
            "mcp/negative_recall_consults.jsonl",
            "mcp/stability_consults.jsonl",
            "mcp/incremental_seasoning_log.jsonl",
            "mcp/incremental_recall_consults.jsonl",
        ],
        "disallowed_claims": [
            "Proof 035 establishes cognition.",
            "Placeholder responses are valid pond-backed recall.",
            "Transport lineage hashes alone prove pond mechanism recall.",
            "Generic consult text proves mechanism structure.",
        ],
        "lineage": {
            "mcp_endpoint": MCP_URL,
            "contract_version": "inside_voice_mcp_contract/0.1",
            "request_hash": request_hash,
            "response_hash": response_hash,
            "derived_from": "Proof 034 MCP boundary failure and shared MCP consult classifier",
            "validates": hostile["final_verdict"]["hostile_verdict"],
            "candidate_status": "rejected"
            if not hostile["final_verdict"]["pond_backed_recall_exists"]
            else "eligible",
        },
    }


def readme_text(hostile: dict[str, Any]) -> str:
    final = hostile["final_verdict"]
    return f"""# Proof 035 - MCP Pond Reality Audit

## Objective

Proof 035 tests the instrument, not cognition. It asks whether the MCP pond currently returns genuine mechanism recall artifacts: returned motifs, returned lineages, lineage hashes, traceability, stability, and growth after seasoning.

## Current Classification

`MCP_POND_REALITY_AUDIT_FAIL`

The current run is not valid as a pond-backed cognition proof. The MCP consult responses did not pass the shared proof gate.

## Boundary Result

- Pond-backed recall exists: {final["pond_backed_recall_exists"]}
- Traceable lineage exists: {final["traceable_lineage_exists"]}
- Stable motif recall exists: {final["stable_motif_recall_exists"]}
- Placeholder explanation remains: {final["remaining_placeholder_explanation"]}
- Scaffold explanation remains: {final["remaining_scaffold_explanation"]}

## Hostile Verdict

{final["hostile_verdict"]}

## Validation

Pond-backed proof claims must validate MCP logs before use:

```bash
python3 tools/validate_mcp_consults.py proofs/035-mcp-pond-reality-audit/mcp/*.jsonl --require-lineage --require-motifs
```

For this run, that command is expected to fail because the observed consult artifacts are not valid pond-backed recall evidence.
"""


def main() -> int:
    metadata = collect_metadata()
    empty_rows = run_empty_pond_audit()
    flow_seasoning_rows = run_flow_seasoning()
    flow_recall_rows = run_recall_audit()
    negative_rows = run_negative_recall_audit()
    stability_rows = run_stability_audit()
    incremental_seasoning_rows, incremental_recall_rows = run_incremental_seasoning_and_recall()

    empty_audit_row = empty_pond_audit(empty_rows, metadata)
    flow_audit_row = flow_recall_audit(flow_recall_rows)
    negative_audit_row = negative_recall_audit(negative_rows)
    stability_audit_row = stability_audit(stability_rows)
    incremental_audit_row = incremental_growth_audit(
        flow_recall_rows,
        incremental_seasoning_rows,
        incremental_recall_rows,
    )
    blind_row = blind_consult_evaluation(flow_recall_rows, incremental_recall_rows, negative_rows)
    all_rows = [
        *empty_rows,
        *flow_seasoning_rows,
        *flow_recall_rows,
        *negative_rows,
        *stability_rows,
        *incremental_seasoning_rows,
        *incremental_recall_rows,
    ]
    hostile = hostile_mcp_audit(
        all_rows,
        empty_audit_row,
        flow_audit_row,
        negative_audit_row,
        stability_audit_row,
        incremental_audit_row,
        blind_row,
        metadata,
    )

    write_json(PROOF_DIR / "empty_pond_audit.json", empty_audit_row)
    write_json(PROOF_DIR / "flow_recall_audit.json", flow_audit_row)
    write_json(PROOF_DIR / "negative_recall_audit.json", negative_audit_row)
    write_json(PROOF_DIR / "stability_audit.json", stability_audit_row)
    write_json(PROOF_DIR / "incremental_growth_audit.json", incremental_audit_row)
    write_json(PROOF_DIR / "blind_consult_evaluation.json", blind_row)
    write_json(PROOF_DIR / "hostile_mcp_audit.json", hostile)
    write_json(PROOF_DIR / "proof_manifest.json", manifest(all_rows, hostile))
    write_text(PROOF_DIR / "README.md", readme_text(hostile))

    print(hostile["final_verdict"]["hostile_verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
