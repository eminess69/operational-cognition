"""Local deterministic Inside Voice MCP pond-backed consultation server."""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
PROTOCOL_VERSION = "inside_voice_mcp_contract/0.2"
ADAPTER_STATUS = "pond_backed"
RESPONSE_SOURCE = "inside_voice_pond"
MAX_OUTPUT_CHARS_CAP = 8000
MIN_OUTPUT_CHARS = 1
MAX_TEXT_CHARS = 4000
MAX_LIST_ITEMS = 40
MAX_LIST_TEXT_CHARS = 500
ARTIFACT_DIR = PROJECT_ROOT / "artifacts/integrations/inside_voice_mcp"
DEFAULT_POND_STATE = PROJECT_ROOT / "artifacts/mcp_pond/pond_state.json"
POND_STATE_ENV = "INSIDE_VOICE_POND_STATE"
BEHAVIOR_MODES = (
    "recall",
    "activation_only",
    "field_interaction",
    "delayed_ranking",
    "collapse_trace",
    "perturbation",
)
LEGACY_RECALL_MODES = ("audit", "synthesis", "review", "proof_planning")
RECALL_MODES = ("recall",) + LEGACY_RECALL_MODES
ALLOWED_MODES = BEHAVIOR_MODES + LEGACY_RECALL_MODES
REQUIRED_REQUEST_FIELDS = {
    "request_id",
    "task",
    "context",
    "mode",
    "max_output_chars",
    "require_lineage",
}
REQUIRED_CONTEXT_FIELDS = {"summary", "files", "constraints", "desired_artifacts"}
LOCAL_HOSTS = {"127.0.0.1", "localhost"}

SECRET_PATTERNS = (
    re.compile(r"(?i)\b(api[_-]?key|token|secret|password)\s*[:=]\s*([^\s,;]+)"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{8,}\b"),
)

MECHANISM_MOTIFS = {
    "FLOW": ["Source", "Path", "Resistance", "Flow"],
    "SUPPORTED_ROTATION": ["Rotation", "Support", "Friction", "Failure"],
    "LOAD_TRANSFER": ["Load", "Distribution", "Concentration", "Failure"],
    "FEEDBACK": ["Signal", "Loop", "Response", "Reinforcement"],
    "THRESHOLD": ["Accumulation", "Limit", "Trigger", "StateChange"],
    "ACCUMULATION": ["Input", "Storage", "BuildUp", "Overflow"],
    "DIFFUSION": ["Source", "Gradient", "Spread", "Dilution"],
    "OSCILLATION": ["State", "Delay", "Overshoot", "Cycle"],
    "BUFFERING": ["Input", "Buffer", "Absorption", "Delay"],
    "RESOURCE_DEPLETION": ["Resource", "Consumption", "Scarcity", "Exhaustion"],
    "AMPLIFICATION": ["Input", "Gain", "Propagation", "Escalation"],
    "COMPENSATION": ["Deviation", "Counteraction", "Substitution", "Stabilization"],
}

MECHANISM_CUES = {
    "FLOW": [
        "source",
        "supply",
        "input",
        "upstream",
        "origin",
        "water",
        "path",
        "pipe",
        "channel",
        "route",
        "lane",
        "throughput",
        "passage",
        "flow",
        "output",
        "arrival",
        "restriction",
        "resistance",
        "bottleneck",
        "choke",
        "narrow",
        "throat",
        "queue",
        "backlog",
        "decline",
    ],
    "SUPPORTED_ROTATION": [
        "rotation",
        "rotating",
        "rotate",
        "turn",
        "bearing",
        "support",
        "socket",
        "journal",
        "pivot",
        "friction",
        "drag",
        "rough",
        "seizure",
        "seize",
        "wobble",
        "lock",
    ],
    "LOAD_TRANSFER": [
        "load",
        "transfer",
        "burden",
        "mass",
        "distribution",
        "structure",
        "support",
        "concentration",
        "localized",
        "bend",
        "crack",
        "failure",
        "anchor",
        "bracket",
        "lug",
    ],
    "FEEDBACK": [
        "feedback",
        "loop",
        "signal",
        "response",
        "reinforce",
        "reinforcement",
        "self",
        "recursive",
        "adjust",
        "correction",
        "runaway",
        "dampen",
        "stabilize",
        "monitor",
        "return",
    ],
    "THRESHOLD": [
        "threshold",
        "limit",
        "tipping",
        "trigger",
        "trip",
        "crossed",
        "crosses",
        "critical",
        "point",
        "boundary",
        "until",
        "sudden",
        "state",
        "switch",
        "breakpoint",
    ],
    "ACCUMULATION": [
        "accumulation",
        "accumulate",
        "build",
        "buildup",
        "pile",
        "store",
        "storage",
        "stock",
        "reserve",
        "cache",
        "pressure",
        "gradual",
        "overflow",
        "deposit",
        "collect",
    ],
    "DIFFUSION": [
        "diffusion",
        "diffuse",
        "spread",
        "disperse",
        "gradient",
        "concentration",
        "dilution",
        "seep",
        "leak",
        "scatter",
        "permeate",
        "migration",
        "edge",
        "uniform",
        "across",
    ],
    "OSCILLATION": [
        "oscillation",
        "oscillate",
        "cycle",
        "swing",
        "overshoot",
        "undershoot",
        "periodic",
        "pulse",
        "alternate",
        "wave",
        "rhythm",
        "rebound",
        "delay",
        "phase",
        "hunting",
    ],
    "BUFFERING": [
        "buffer",
        "buffering",
        "absorb",
        "absorption",
        "dampen",
        "cushion",
        "reserve",
        "delay",
        "smooth",
        "temporary",
        "slack",
        "shock",
        "hold",
        "stabilize",
        "capacity",
    ],
    "RESOURCE_DEPLETION": [
        "resource",
        "depletion",
        "deplete",
        "depleted",
        "exhaustion",
        "exhaust",
        "scarcity",
        "consumption",
        "consume",
        "fuel",
        "reserve",
        "drain",
        "capacity",
        "fatigue",
        "supply",
    ],
    "AMPLIFICATION": [
        "amplification",
        "amplify",
        "gain",
        "multiplier",
        "magnify",
        "cascade",
        "escalate",
        "escalation",
        "accelerate",
        "compounding",
        "propagate",
        "propagation",
        "signal",
        "growth",
        "surge",
    ],
    "COMPENSATION": [
        "compensation",
        "compensate",
        "offset",
        "counteract",
        "counteraction",
        "substitute",
        "substitution",
        "backup",
        "balance",
        "adapt",
        "adjust",
        "maintain",
        "stabilize",
        "mask",
        "correction",
    ],
}


class ContractValidationError(ValueError):
    """Raised when a consultation request fails the public contract."""


class PondUnavailableError(RuntimeError):
    """Raised when recall is requested before a pond exists."""


class PondRecallMiss(RuntimeError):
    """Raised when the pond is available but no record matches the request."""


@dataclass(frozen=True)
class ConsultationResult:
    status_code: int
    response: dict[str, Any]


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def hash_canonical_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def write_json_artifact(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def append_jsonl_artifact(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(canonical_json(value) + "\n")


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def is_local_host(host: str) -> bool:
    return host in LOCAL_HOSTS


def validate_bind_host(host: str, allow_nonlocal: bool = False) -> str:
    if is_local_host(host) or allow_nonlocal:
        return host
    raise ContractValidationError(
        f"refusing non-local host {host!r}; use --allow-nonlocal only for controlled development"
    )


def pond_state_path(path: Path | None = None) -> Path:
    if path is not None:
        return path
    configured = os.environ.get(POND_STATE_ENV)
    return Path(configured) if configured else DEFAULT_POND_STATE


def build_health_payload(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> dict[str, Any]:
    return {
        "ok": True,
        "service": "inside_voice_mcp",
        "verdict": "INSIDE_VOICE_MCP_HEALTHY",
        "protocol_version": PROTOCOL_VERSION,
        "host": host,
        "port": port,
        "local_only": is_local_host(host),
        "endpoints": ["/health", "/schema", "/consult", "/version", "/capabilities"],
    }


def build_schema_payload() -> dict[str, Any]:
    request_schema = {
        "type": "object",
        "required": sorted(REQUIRED_REQUEST_FIELDS),
        "additionalProperties": False,
        "properties": {
            "request_id": {"type": "string", "minLength": 1},
            "task": {"type": "string"},
            "context": {
                "type": "object",
                "required": sorted(REQUIRED_CONTEXT_FIELDS),
                "additionalProperties": False,
                "properties": {
                    "summary": {"type": "string"},
                    "files": {"type": "array", "items": {"type": "string"}},
                    "constraints": {"type": "array", "items": {"type": "string"}},
                    "desired_artifacts": {"type": "array", "items": {"type": "string"}},
                },
            },
            "mode": {
                "type": "string",
                "description": "Behavior protocol mode. Unknown modes are accepted by contract validation and fail closed with unknown_mode.",
            },
            "max_output_chars": {
                "type": "integer",
                "minimum": MIN_OUTPUT_CHARS,
                "maximum": MAX_OUTPUT_CHARS_CAP,
            },
            "require_lineage": {"type": "boolean"},
        },
    }
    response_schema = {
        "type": "object",
        "required": [
            "request_id",
            "adapter_status",
            "verdict",
            "response_source",
            "returned_motifs",
            "returned_lineages",
            "lineage_hashes",
            "recall_summary",
            "fail_closed_reason",
            "mode",
        ],
        "properties": {
            "request_id": {"type": "string"},
            "adapter_status": {"type": "string", "enum": ["pond_backed", "error"]},
            "verdict": {"type": "string", "enum": ["ok", "fail_closed"]},
            "response_source": {"type": "string", "enum": [RESPONSE_SOURCE]},
            "mode": {"type": "string"},
            "returned_motifs": {"type": "array", "items": {"type": "string"}},
            "returned_lineages": {"type": "array", "items": {"type": "string"}},
            "lineage_hashes": {"type": "array", "items": {"type": "string"}},
            "recall_summary": {"type": "string"},
            "fail_closed_reason": {"type": ["string", "null"]},
        },
    }
    return {
        "service": "inside_voice_mcp",
        "protocol_version": PROTOCOL_VERSION,
        "canonical_json": {"sort_keys": True, "separators": [",", ":"], "encoding": "utf-8"},
        "request_schema": request_schema,
        "response_schema": response_schema,
        "privacy_boundary": {
            "never_expose": [
                "hidden_chain_of_thought",
                "belief_ledger_internal_trace_structures",
                "harmonic_traceback_implementation_details",
                "private_substrate_scoring_internals",
                "full_mcp_prompt_internals",
                "secrets_env_vars_tokens",
            ],
            "expose_only": [
                "summary",
                "findings",
                "recommendations",
                "uncertainty",
                "lineage_hashes",
                "source_refs",
                "returned_motifs",
                "returned_lineages",
            ],
        },
        "fail_closed": [
            "missing_request_id",
            "invalid_mode",
            "unknown_mode",
            "malformed_context",
            "pond_unavailable",
            "empty_pond",
            "no_relevant_pond_recall",
            "lineage_required_but_unavailable",
            "consultation_exception",
        ],
    }


def write_health_artifact(
    artifact_dir: Path = ARTIFACT_DIR,
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
) -> dict[str, Any]:
    payload = build_health_payload(host=host, port=port)
    write_json_artifact(artifact_dir / "mcp_health.json", payload)
    return payload


def write_schema_artifact(artifact_dir: Path = ARTIFACT_DIR) -> dict[str, Any]:
    payload = build_schema_payload()
    write_json_artifact(artifact_dir / "mcp_schema.json", payload)
    return payload


def _require_exact_fields(value: dict[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        raise ContractValidationError(f"{label} missing required field(s): {', '.join(missing)}")
    if extra:
        raise ContractValidationError(f"{label} contains unknown field(s): {', '.join(extra)}")


def _require_string(value: Any, label: str, *, non_empty: bool = False, max_chars: int = MAX_TEXT_CHARS) -> str:
    if not isinstance(value, str):
        raise ContractValidationError(f"{label} must be a string")
    if non_empty and not value.strip():
        raise ContractValidationError(f"{label} must be a non-empty string")
    if len(value) > max_chars:
        raise ContractValidationError(f"{label} exceeds {max_chars} characters")
    return value


def _require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list):
        raise ContractValidationError(f"{label} must be an array of strings")
    if len(value) > MAX_LIST_ITEMS:
        raise ContractValidationError(f"{label} exceeds {MAX_LIST_ITEMS} entries")
    output: list[str] = []
    for index, item in enumerate(value):
        output.append(_require_string(item, f"{label}[{index}]", max_chars=MAX_LIST_TEXT_CHARS))
    return output


def validate_consult_request(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ContractValidationError("request body must be a JSON object")
    _require_exact_fields(payload, REQUIRED_REQUEST_FIELDS, "request")

    request_id = _require_string(payload["request_id"], "request_id", non_empty=True, max_chars=200)
    task = _require_string(payload["task"], "task")

    context = payload["context"]
    if not isinstance(context, dict):
        raise ContractValidationError("context must be an object")
    _require_exact_fields(context, REQUIRED_CONTEXT_FIELDS, "context")

    mode = _require_string(payload["mode"], "mode", non_empty=True, max_chars=80)

    max_output_chars = payload["max_output_chars"]
    if type(max_output_chars) is not int:
        raise ContractValidationError("max_output_chars must be an integer")
    if max_output_chars < MIN_OUTPUT_CHARS:
        raise ContractValidationError(f"max_output_chars must be at least {MIN_OUTPUT_CHARS}")
    if max_output_chars > MAX_OUTPUT_CHARS_CAP:
        raise ContractValidationError(f"max_output_chars exceeds allowed cap {MAX_OUTPUT_CHARS_CAP}")

    require_lineage = payload["require_lineage"]
    if type(require_lineage) is not bool:
        raise ContractValidationError("require_lineage must be a boolean")

    return {
        "request_id": request_id,
        "task": task,
        "context": {
            "summary": _require_string(context["summary"], "context.summary"),
            "files": _require_string_list(context["files"], "context.files"),
            "constraints": _require_string_list(context["constraints"], "context.constraints"),
            "desired_artifacts": _require_string_list(context["desired_artifacts"], "context.desired_artifacts"),
        },
        "mode": mode,
        "max_output_chars": max_output_chars,
        "require_lineage": require_lineage,
    }


def scrub_private_text(value: str, max_chars: int = 220) -> str:
    text = value.replace("\r", " ").replace("\n", " ").strip()
    for pattern in SECRET_PATTERNS:
        text = pattern.sub(lambda match: f"{match.group(1)}=<redacted>" if match.groups() else "<redacted>", text)
    if len(text) > max_chars:
        return text[: max_chars - 3].rstrip() + "..."
    return text


def normalize(text: str) -> str:
    lowered = text.lower()
    lowered = re.sub(r"[^a-z0-9_]+", " ", lowered)
    return re.sub(r"\s+", " ", lowered).strip()


def tokens(text: str) -> set[str]:
    raw = set(normalize(text).split())
    expanded = set(raw)
    for token in raw:
        if token.endswith("s") and len(token) > 3:
            expanded.add(token[:-1])
        if token.endswith("ing") and len(token) > 5:
            expanded.add(token[:-3])
        if token.endswith("ed") and len(token) > 4:
            expanded.add(token[:-2])
    return expanded


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            output.append(value)
    return output


def empty_pond_state() -> dict[str, Any]:
    return {
        "schema_version": "inside_voice_mcp_pond_state.v1",
        "state_id": "inside_voice_mcp_local_pond",
        "records": [],
    }


def load_pond(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise PondUnavailableError("pond_unavailable")
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PondUnavailableError("pond_unavailable") from exc
    if not isinstance(state, dict):
        raise PondUnavailableError("pond_unavailable")
    records = state.get("records")
    if not isinstance(records, list):
        raise PondUnavailableError("pond_unavailable")
    return state


def save_pond(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def load_or_create_pond(path: Path) -> dict[str, Any]:
    if not path.exists():
        state = empty_pond_state()
        save_pond(path, state)
        return state
    return load_pond(path)


def mechanism_from_request(request: dict[str, Any]) -> str:
    text = f"{request['task']} {request['context']['summary']}"
    patterns = [
        r"mechanism\s+label\s*[:=]\s*([A-Z_]+)",
        r"mechanism\s*[:=]\s*([A-Z_]+)",
        r"mechanism\s+into.*?\b(FLOW|SUPPORTED_ROTATION|LOAD_TRANSFER)\b",
        r"\b(FLOW|SUPPORTED_ROTATION|LOAD_TRANSFER)\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            candidate = match.group(1).upper()
            if candidate in MECHANISM_MOTIFS:
                return candidate
    return ""


def is_seasoning_request(request: dict[str, Any]) -> bool:
    task = normalize(request["task"])
    summary = normalize(request["context"]["summary"])
    return (
        task.startswith("action season")
        or task.startswith("season ")
        or "mechanism label" in task
        or summary.startswith("action season")
    )


def source_refs(request: dict[str, Any]) -> list[str]:
    refs = ["request", "context.summary"]
    refs.extend(request["context"]["files"])
    return dedupe(refs)


def lesson_text(request: dict[str, Any]) -> str:
    return scrub_private_text(f"{request['task']} {request['context']['summary']}", max_chars=1200)


def record_lineage_payload(request: dict[str, Any], mechanism: str, text: str) -> dict[str, Any]:
    matched_cues = sorted(tokens(text) & set(MECHANISM_CUES[mechanism]))
    payload = {
        "request_id": request["request_id"],
        "mechanism": mechanism,
        "lesson_text": text,
        "motifs": MECHANISM_MOTIFS[mechanism],
        "cues": matched_cues,
        "source_refs": source_refs(request),
    }
    payload["payload_hash"] = hash_canonical_json(payload)
    return payload


def season_pond(request: dict[str, Any], path: Path) -> dict[str, Any]:
    mechanism = mechanism_from_request(request)
    if not mechanism:
        raise PondRecallMiss("unsupported_or_missing_mechanism")

    state = load_or_create_pond(path)
    text = lesson_text(request)
    lineage_payload = record_lineage_payload(request, mechanism, text)
    lineage_hash = hash_canonical_json(lineage_payload)
    record_id = f"pond:{mechanism.lower()}:{lineage_hash[:16]}"
    record = {
        "record_id": record_id,
        "mechanism": mechanism,
        "motifs": MECHANISM_MOTIFS[mechanism],
        "cues": sorted(set(MECHANISM_CUES[mechanism]) | set(lineage_payload["cues"])),
        "lesson_text": text,
        "lineage_payload": lineage_payload,
        "lineage_hash": lineage_hash,
    }

    records = [item for item in state["records"] if isinstance(item, dict) and item.get("record_id") != record_id]
    records.append(record)
    state["records"] = sorted(records, key=lambda item: str(item.get("record_id", "")))
    state["updated_by_request_id"] = request["request_id"]
    save_pond(path, state)

    return build_success_response(
        request,
        [record],
        recall_summary=f"Seasoned {mechanism} into local pond state with traceable lineage.",
        action="season",
    )


def record_score(record: dict[str, Any], query: str) -> dict[str, Any]:
    query_tokens = tokens(query)
    cues = {str(cue).lower() for cue in record.get("cues", []) if isinstance(cue, str)}
    motifs = {normalize(str(motif)) for motif in record.get("motifs", []) if isinstance(motif, str)}
    lesson_tokens = tokens(str(record.get("lesson_text", "")))
    cue_hits = sorted(query_tokens & cues)
    motif_hits = sorted(query_tokens & motifs)
    lesson_hits = sorted(query_tokens & lesson_tokens)
    score = len(cue_hits) * 2.0 + len(motif_hits) * 1.5 + min(len(lesson_hits), 8) * 0.25
    return {
        "record": record,
        "score": round(score, 4),
        "cue_hits": cue_hits,
        "motif_hits": motif_hits,
        "lesson_hits": lesson_hits,
    }


def recall_from_pond(request: dict[str, Any], path: Path) -> dict[str, Any]:
    state = load_pond(path)
    records = [record for record in state.get("records", []) if isinstance(record, dict)]
    if not records:
        raise PondRecallMiss("empty_pond")

    query = request["task"]
    scored = [record_score(record, query) for record in records]
    scored.sort(key=lambda row: (-row["score"], str(row["record"].get("record_id", ""))))
    selected = [row for row in scored if row["score"] >= 2.0][:5]
    if not selected:
        raise PondRecallMiss("no_relevant_pond_recall")

    return build_success_response(
        request,
        [row["record"] for row in selected],
        recall_summary=f"Returned {len(selected)} traceable pond record(s) ranked by motif/cue overlap.",
        action="recall",
        score_rows=selected,
    )


def activation_query_text(task: str) -> str:
    match = re.search(r"observation\s*:\s*(.*?)(?:\n\s*required\s*:|$)", task, flags=re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return task


def activation_from_pond(request: dict[str, Any], path: Path) -> dict[str, Any]:
    state = load_pond(path)
    records = [record for record in state.get("records", []) if isinstance(record, dict)]
    if not records:
        raise PondRecallMiss("empty_pond")

    query = activation_query_text(request["task"])
    scored = [record_score(record, query) for record in records]
    by_mechanism: dict[str, list[dict[str, Any]]] = {}
    for row in scored:
        mechanism = str(row["record"].get("mechanism", ""))
        if row["score"] >= 2.0 and mechanism:
            by_mechanism.setdefault(mechanism, []).append(row)
    if not by_mechanism:
        raise PondRecallMiss("no_relevant_pond_recall")

    mechanism_scores = {
        mechanism: max(row["score"] for row in rows)
        for mechanism, rows in by_mechanism.items()
    }
    total_score = sum(mechanism_scores.values()) or 1.0
    activated_mechanisms = []
    selected_records: list[dict[str, Any]] = []
    score_rows: list[dict[str, Any]] = []
    for mechanism in sorted(by_mechanism):
        rows = sorted(
            by_mechanism[mechanism],
            key=lambda row: (-row["score"], str(row["record"].get("record_id", ""))),
        )
        top_rows = rows[:2]
        selected_records.extend(row["record"] for row in top_rows)
        score_rows.extend(top_rows)
        activated_mechanisms.append(
            {
                "mechanism": mechanism,
                "activation_weight": round(mechanism_scores[mechanism] / total_score, 4),
                "supporting_motifs": [
                    str(motif)
                    for motif in top_rows[0]["record"].get("motifs", [])
                    if isinstance(motif, str)
                ],
                "supporting_lineages": [
                    str(row["record"].get("record_id", ""))
                    for row in top_rows
                    if row["record"].get("record_id")
                ],
                "supporting_lineage_hashes": [
                    str(row["record"].get("lineage_hash", ""))
                    for row in top_rows
                    if row["record"].get("lineage_hash")
                ],
            }
        )

    response = build_success_response(
        request,
        selected_records,
        recall_summary=f"Activated {len(activated_mechanisms)} mechanism field(s) before ranking.",
        action="activation",
        score_rows=score_rows,
    )
    response["activated_mechanisms"] = activated_mechanisms
    response["activation_weights"] = {
        row["mechanism"]: row["activation_weight"]
        for row in activated_mechanisms
    }
    return compact_response_to_limit(response, request["max_output_chars"])


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, (str, int, float)) and str(item)]


def activated_from_response(response: dict[str, Any]) -> list[dict[str, Any]]:
    activated: list[dict[str, Any]] = []
    rows = response.get("activated_mechanisms", [])
    if not isinstance(rows, list):
        return activated
    for row in rows:
        if not isinstance(row, dict):
            continue
        mechanism = str(row.get("mechanism", ""))
        if not mechanism:
            continue
        try:
            activation_weight = float(row.get("activation_weight", 0.0))
        except (TypeError, ValueError):
            activation_weight = 0.0
        activated.append(
            {
                "mechanism": mechanism,
                "activation_weight": round(activation_weight, 4),
                "supporting_motifs": _string_list(row.get("supporting_motifs")),
                "supporting_lineages": _string_list(row.get("supporting_lineages")),
                "supporting_lineage_hashes": _string_list(row.get("supporting_lineage_hashes")),
            }
        )
    activated.sort(key=lambda item: (-item["activation_weight"], item["mechanism"]))
    return activated


def shared_motifs_for(rows: list[dict[str, Any]]) -> list[str]:
    counts: dict[str, int] = {}
    for row in rows:
        for motif in row.get("supporting_motifs", []):
            counts[str(motif)] = counts.get(str(motif), 0) + 1
    return sorted(motif for motif, count in counts.items() if count > 1)


def interaction_payload(
    request: dict[str, Any],
    rows: tuple[dict[str, Any], ...],
) -> dict[str, Any]:
    mechanisms = [str(row["mechanism"]) for row in rows]
    motifs = dedupe(
        [motif for row in rows for motif in row.get("supporting_motifs", []) if isinstance(motif, str)]
    )
    lineages = dedupe(
        [lineage for row in rows for lineage in row.get("supporting_lineages", []) if isinstance(lineage, str)]
    )
    lineage_hashes = dedupe(
        [lineage_hash for row in rows for lineage_hash in row.get("supporting_lineage_hashes", []) if isinstance(lineage_hash, str)]
    )
    shared_motifs = shared_motifs_for(list(rows))
    activation_mass = sum(float(row.get("activation_weight", 0.0)) for row in rows)
    interaction_weight = round(activation_mass + min(len(shared_motifs) * 0.05, 0.2), 4)
    pathway = " + ".join(mechanisms)
    return {
        "pathway_id": f"pathway:{hash_canonical_json({'request_id': request['request_id'], 'pathway': pathway, 'motifs': motifs})[:16]}",
        "pathway": pathway,
        "mechanisms": mechanisms,
        "combination_depth": len(mechanisms),
        "interaction_weight": interaction_weight,
        "supporting_motifs": motifs,
        "shared_motifs": shared_motifs,
        "supporting_lineages": lineages,
        "supporting_lineage_hashes": lineage_hashes,
        "reason": "Interaction candidate formed before collapse from co-activated pond-backed mechanisms.",
    }


def build_field_interactions(
    request: dict[str, Any],
    activated: list[dict[str, Any]],
    *,
    depths: tuple[int, ...] = (2, 3),
    limit: int = 12,
    suppress_motif: str | None = None,
) -> list[dict[str, Any]]:
    interactions: list[dict[str, Any]] = []
    for depth in depths:
        if len(activated) < depth:
            continue
        for rows in itertools.combinations(activated, depth):
            interaction = interaction_payload(request, rows)
            if suppress_motif and suppress_motif in interaction["supporting_motifs"]:
                continue
            interactions.append(interaction)
    interactions.sort(key=lambda item: (-float(item["interaction_weight"]), item["pathway"]))
    return interactions[:limit]


def field_interaction_from_pond(request: dict[str, Any], path: Path) -> dict[str, Any]:
    response = activation_from_pond(request, path)
    activated = activated_from_response(response)
    interactions = build_field_interactions(request, activated)
    response["field_interactions"] = interactions
    response["interaction_window"] = {
        "ranking_deferred": True,
        "pairwise_pathways": sum(1 for item in interactions if item["combination_depth"] == 2),
        "triple_pathways": sum(1 for item in interactions if item["combination_depth"] == 3),
    }
    response["recall_summary"] = (
        f"Activated {len(activated)} mechanism field(s) and formed {len(interactions)} interaction candidate(s) before collapse."
    )
    response["summary"] = response["recall_summary"]
    return compact_response_to_limit(response, request["max_output_chars"])


def delayed_ranking_from_pond(request: dict[str, Any], path: Path) -> dict[str, Any]:
    response = field_interaction_from_pond(request, path)
    interactions = response.get("field_interactions", [])
    if not isinstance(interactions, list):
        interactions = []
    ranked_pathways = []
    for rank, interaction in enumerate(interactions[:6], start=1):
        if not isinstance(interaction, dict):
            continue
        row = copy.deepcopy(interaction)
        row["rank"] = rank
        row["weight"] = row.get("interaction_weight", 0.0)
        row["reason"] = "Ranked only after the interaction window formed pair/triple pathways."
        ranked_pathways.append(row)
    response["ranked_pathways"] = ranked_pathways
    response["recall_summary"] = f"Delayed ranking preserved interaction candidates, then ranked {len(ranked_pathways)} pathway(s)."
    response["summary"] = response["recall_summary"]
    return compact_response_to_limit(response, request["max_output_chars"])


def collapse_trace_from_pond(request: dict[str, Any], path: Path) -> dict[str, Any]:
    response = delayed_ranking_from_pond(request, path)
    activated = activated_from_response(response)
    ranked = response.get("ranked_pathways", [])
    if not isinstance(ranked, list):
        ranked = []
    survived = [copy.deepcopy(row) for row in ranked[:1] if isinstance(row, dict)]
    eliminated = []
    for row in ranked[1:]:
        if not isinstance(row, dict):
            continue
        eliminated.append(
            {
                "pathway_id": row.get("pathway_id", ""),
                "pathway": row.get("pathway", ""),
                "mechanisms": row.get("mechanisms", []),
                "elimination_reason": "Lower delayed-ranking support after interaction window.",
                "supporting_motifs": row.get("supporting_motifs", []),
                "supporting_lineages": row.get("supporting_lineages", []),
            }
        )
    response["collapse_trace"] = {
        "activated_before_collapse": [row["mechanism"] for row in activated],
        "survived_after_collapse": survived,
        "eliminated_pathways": eliminated,
        "collapse_reason": "Delayed-ranking collapse selected the highest supported interaction pathway.",
    }
    response["activated_before_collapse"] = response["collapse_trace"]["activated_before_collapse"]
    response["survived_after_collapse"] = survived
    response["eliminated_pathways"] = eliminated
    response["collapse_reason"] = response["collapse_trace"]["collapse_reason"]
    response["recall_summary"] = (
        f"Captured collapse from {len(activated)} activated mechanism(s) to {len(survived)} surviving pathway(s)."
    )
    response["summary"] = response["recall_summary"]
    return compact_response_to_limit(response, request["max_output_chars"])


def _perturbation_variant(
    request: dict[str, Any],
    name: str,
    activated: list[dict[str, Any]],
    *,
    suppress_motif: str | None = None,
    force_no_ranking: bool = False,
) -> dict[str, Any]:
    interactions = build_field_interactions(request, activated, suppress_motif=suppress_motif)
    ranked = [] if force_no_ranking else interactions[:6]
    return {
        "perturbation": name,
        "activated_mechanisms": [row["mechanism"] for row in activated],
        "suppressed_motif": suppress_motif,
        "field_size": len(interactions),
        "ranked_pathways": ranked,
        "valid_pathway_count": sum(
            1 for interaction in interactions if interaction.get("supporting_lineages") and interaction.get("supporting_lineage_hashes")
        ),
        "notes": [
            "Ranking disabled for this variant." if force_no_ranking else "Variant ranked after interaction window.",
        ],
    }


def perturbation_from_pond(request: dict[str, Any], path: Path) -> dict[str, Any]:
    response = field_interaction_from_pond(request, path)
    activated = activated_from_response(response)
    baseline_interactions = response.get("field_interactions", [])
    if not isinstance(baseline_interactions, list):
        baseline_interactions = []

    activated_names = {row["mechanism"] for row in activated}
    irrelevant = next((mechanism for mechanism in MECHANISM_MOTIFS if mechanism not in activated_names), "")
    injected = []
    if irrelevant:
        injected = activated + [
            {
                "mechanism": irrelevant,
                "activation_weight": 0.01,
                "supporting_motifs": MECHANISM_MOTIFS[irrelevant],
                "supporting_lineages": [],
                "supporting_lineage_hashes": [],
            }
        ]

    shared_motif = ""
    for interaction in baseline_interactions:
        if isinstance(interaction, dict) and interaction.get("shared_motifs"):
            shared_motif = str(interaction["shared_motifs"][0])
            break
    if not shared_motif and response.get("returned_motifs"):
        shared_motif = str(response["returned_motifs"][0])

    perturbations = [
        _perturbation_variant(request, "baseline", activated),
        _perturbation_variant(request, "remove_top_activated", activated[1:]),
        _perturbation_variant(request, "remove_top_two_activated", activated[2:]),
    ]
    if injected:
        perturbations.append(_perturbation_variant(request, "inject_irrelevant_mechanism", injected))
    perturbations.append(
        _perturbation_variant(
            request,
            "suppress_shared_motif",
            activated,
            suppress_motif=shared_motif or None,
        )
    )
    perturbations.append(_perturbation_variant(request, "force_no_ranking", activated, force_no_ranking=True))

    response["perturbations"] = perturbations
    response["perturbation_summary"] = {
        "top_mechanism_removed": activated[0]["mechanism"] if activated else "",
        "top_two_mechanisms_removed": [row["mechanism"] for row in activated[:2]],
        "injected_irrelevant_mechanism": irrelevant,
        "suppressed_shared_motif": shared_motif,
        "ranking_forced_off": True,
    }
    response["recall_summary"] = f"Ran {len(perturbations)} field perturbation variant(s) over pond-backed activation."
    response["summary"] = response["recall_summary"]
    return compact_response_to_limit(response, request["max_output_chars"])


def response_hash_material(response: dict[str, Any]) -> dict[str, Any]:
    material = copy.deepcopy(response)
    material.pop("non_hash_metadata", None)
    lineage = material.get("lineage")
    if isinstance(lineage, dict):
        lineage.pop("response_hash", None)
    return material


def finalize_response(response: dict[str, Any]) -> dict[str, Any]:
    response = copy.deepcopy(response)
    response.setdefault("lineage", {})["response_hash"] = hash_canonical_json(response_hash_material(response))
    return response


def build_success_response(
    request: dict[str, Any],
    records: list[dict[str, Any]],
    *,
    recall_summary: str,
    action: str,
    score_rows: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    returned_motifs = dedupe(
        [str(motif) for record in records for motif in record.get("motifs", []) if isinstance(motif, str)]
    )
    returned_lineages = [str(record["record_id"]) for record in records if record.get("record_id")]
    lineage_hashes = [str(record["lineage_hash"]) for record in records if record.get("lineage_hash")]
    lineage_payloads = [record.get("lineage_payload", {}) for record in records]
    findings = [
        {
            "id": f"{action}-pond-record-{index:03d}",
            "claim": f"Returned pond record {record.get('record_id', '')}.",
            "evidence": [str(record.get("record_id", "")), str(record.get("lineage_hash", ""))],
            "confidence": "high",
            "risk": "low",
            "lineage_refs": [str(record.get("record_id", ""))],
        }
        for index, record in enumerate(records, start=1)
    ]
    if score_rows:
        for index, row in enumerate(score_rows, start=1):
            findings.append(
                {
                    "id": f"rank-score-{index:03d}",
                    "claim": f"Motif/cue overlap score {row['score']} for {row['record'].get('record_id', '')}.",
                    "evidence": row["cue_hits"] + row["motif_hits"],
                    "confidence": "medium",
                    "risk": "medium",
                    "lineage_refs": [str(row["record"].get("record_id", ""))],
                }
            )

    response = {
        "request_id": request["request_id"],
        "adapter_status": ADAPTER_STATUS,
        "verdict": "ok",
        "response_source": RESPONSE_SOURCE,
        "returned_motifs": returned_motifs,
        "returned_lineages": returned_lineages,
        "lineage_hashes": lineage_hashes,
        "recall_summary": recall_summary,
        "fail_closed_reason": None,
        "mode": request["mode"],
        "summary": recall_summary,
        "findings": findings,
        "recommendations": [
            {
                "id": "validate-pond-backed-boundary",
                "action": "Run validate_mcp_consults.py before using this response as proof evidence.",
                "reason": "Pond-backed claims require non-empty motifs and lineage evidence.",
                "blocking": True,
            }
        ],
        "uncertainty": [
            "Recall is deterministic over the local pond state and may miss records outside that state.",
        ],
        "lineage_payloads": lineage_payloads,
        "lineage": {
            "request_hash": hash_canonical_json(request),
            "response_hash": "",
            "source_refs": returned_lineages,
        },
    }
    return compact_response_to_limit(response, request["max_output_chars"])


def fail_closed_response(request: dict[str, Any], reason: str, *, status: str = "pond_backed") -> dict[str, Any]:
    response = {
        "request_id": request["request_id"],
        "adapter_status": "error" if status == "error" else ADAPTER_STATUS,
        "verdict": "fail_closed",
        "response_source": RESPONSE_SOURCE,
        "returned_motifs": [],
        "returned_lineages": [],
        "lineage_hashes": [],
        "recall_summary": "",
        "fail_closed_reason": reason,
        "mode": request["mode"],
        "summary": f"Inside Voice pond recall failed closed: {reason}.",
        "findings": [
            {
                "id": "fail-closed",
                "claim": f"Pond recall failed closed: {reason}.",
                "evidence": ["pond_state"],
                "confidence": "high",
                "risk": "high",
                "lineage_refs": [],
            }
        ],
        "recommendations": [
            {
                "id": "repair-pond-or-season",
                "action": "Create or season the pond before relying on recall.",
                "reason": "Empty recall must not be treated as pond-backed evidence.",
                "blocking": True,
            }
        ],
        "uncertainty": ["No motifs or lineages were returned."],
        "lineage": {
            "request_hash": hash_canonical_json(request),
            "response_hash": "",
            "source_refs": [],
        },
    }
    return finalize_response(response)


def compact_response_to_limit(response: dict[str, Any], max_output_chars: int) -> dict[str, Any]:
    response = finalize_response(response)
    if len(canonical_json(response)) <= max_output_chars:
        return response

    compact = copy.deepcopy(response)
    compact["findings"] = compact["findings"][:3]
    compact["lineage_payloads"] = compact.get("lineage_payloads", [])[:3]
    compact["uncertainty"] = ["Response details were compacted; motifs, lineages, and hashes are preserved."]
    return finalize_response(compact)


def consult_inside_voice(request: dict[str, Any], state_path: Path | None = None) -> dict[str, Any]:
    path = pond_state_path(state_path)
    try:
        if request["mode"] not in ALLOWED_MODES:
            return fail_closed_response(request, "unknown_mode", status="error")
        if is_seasoning_request(request):
            return season_pond(request, path)
        if request["mode"] == "activation_only":
            return activation_from_pond(request, path)
        if request["mode"] == "field_interaction":
            return field_interaction_from_pond(request, path)
        if request["mode"] == "delayed_ranking":
            return delayed_ranking_from_pond(request, path)
        if request["mode"] == "collapse_trace":
            return collapse_trace_from_pond(request, path)
        if request["mode"] == "perturbation":
            return perturbation_from_pond(request, path)
        if request["mode"] in RECALL_MODES:
            return recall_from_pond(request, path)
        return fail_closed_response(request, "unknown_mode", status="error")
    except PondUnavailableError:
        return fail_closed_response(request, "pond_unavailable", status="error")
    except PondRecallMiss as exc:
        return fail_closed_response(request, str(exc), status="pond_backed")


def _request_hash_for_error(payload: Any) -> str:
    try:
        return hash_canonical_json(payload)
    except TypeError:
        return hashlib.sha256(repr(payload).encode("utf-8")).hexdigest()


def error_response(reason: str, payload: Any | None = None) -> dict[str, Any]:
    request_id = ""
    mode = "audit"
    if isinstance(payload, dict):
        if isinstance(payload.get("request_id"), str):
            request_id = payload["request_id"]
        if isinstance(payload.get("mode"), str):
            mode = payload["mode"]
    response = {
        "request_id": request_id,
        "adapter_status": "error",
        "verdict": "fail_closed",
        "response_source": RESPONSE_SOURCE,
        "returned_motifs": [],
        "returned_lineages": [],
        "lineage_hashes": [],
        "recall_summary": "",
        "fail_closed_reason": reason,
        "mode": mode,
        "summary": "Inside Voice MCP consultation failed closed.",
        "findings": [
            {
                "id": "fail-closed",
                "claim": scrub_private_text(reason),
                "evidence": ["contract_validation"],
                "confidence": "high",
                "risk": "high",
                "lineage_refs": [],
            }
        ],
        "recommendations": [
            {
                "id": "repair-request",
                "action": "Submit a request matching the published Inside Voice MCP schema.",
                "reason": "Malformed or unstable consultation inputs are rejected by contract.",
                "blocking": True,
            }
        ],
        "uncertainty": ["The pond adapter was not invoked for this failed request."],
        "lineage": {
            "request_hash": _request_hash_for_error(payload),
            "response_hash": "",
            "source_refs": [],
        },
    }
    return finalize_response(response)


def assert_lineage_available(response: dict[str, Any]) -> None:
    if response.get("verdict") == "fail_closed":
        return
    lineage = response.get("lineage")
    if not isinstance(lineage, dict):
        raise ContractValidationError("lineage required but unavailable")
    for field in ("request_hash", "response_hash", "source_refs"):
        if field not in lineage:
            raise ContractValidationError("lineage required but unavailable")
    if not lineage["request_hash"] or not lineage["response_hash"]:
        raise ContractValidationError("lineage required but unavailable")
    if not response.get("returned_motifs") or not response.get("returned_lineages") or not response.get("lineage_hashes"):
        raise ContractValidationError("pond-backed response missing motifs or lineage evidence")


def write_consultation_artifacts(
    request_payload: Any,
    response: dict[str, Any],
    artifact_dir: Path = ARTIFACT_DIR,
) -> None:
    entry = {
        "event": "inside_voice_mcp_consultation",
        "request_id": response.get("request_id", ""),
        "mode": response.get("mode", ""),
        "request_hash": response.get("lineage", {}).get("request_hash", ""),
        "response_hash": response.get("lineage", {}).get("response_hash", ""),
        "request": request_payload,
        "response": response,
        "non_hash_metadata": {"timestamp_utc": utc_timestamp()},
    }
    append_jsonl_artifact(artifact_dir / "consultation_log.jsonl", entry)
    write_json_artifact(artifact_dir / "latest_consultation.json", entry)


def process_consult_request(
    payload: Any,
    artifact_dir: Path = ARTIFACT_DIR,
    adapter: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
    state_path: Path | None = None,
) -> ConsultationResult:
    try:
        request = validate_consult_request(payload)
        if adapter is None:
            response = consult_inside_voice(request, state_path=state_path)
        else:
            response = adapter(request)
        if request["require_lineage"]:
            assert_lineage_available(response)
        status_code = 200
    except ContractValidationError as exc:
        response = error_response(str(exc), payload)
        status_code = 400
    except Exception:
        response = error_response("consultation_exception", payload)
        status_code = 500

    write_consultation_artifacts(payload, response, artifact_dir)
    return ConsultationResult(status_code=status_code, response=response)


def capabilities_payload() -> dict[str, Any]:
    return {
        "service": "inside_voice_mcp",
        "protocol_version": PROTOCOL_VERSION,
        "modes": list(ALLOWED_MODES),
        "behavior_modes": list(BEHAVIOR_MODES),
        "legacy_recall_modes": list(LEGACY_RECALL_MODES),
        "max_output_chars_cap": MAX_OUTPUT_CHARS_CAP,
        "adapter_status": ADAPTER_STATUS,
        "response_source": RESPONSE_SOURCE,
        "pond_state_env": POND_STATE_ENV,
        "local_only_default": True,
    }


def make_handler(artifact_dir: Path, host: str, port: int) -> type[BaseHTTPRequestHandler]:
    class InsideVoiceMCPHandler(BaseHTTPRequestHandler):
        server_version = "InsideVoiceMCP/0.2"

        def log_message(self, format: str, *args: Any) -> None:
            return

        def _send_json(self, status_code: int, payload: dict[str, Any]) -> None:
            body = (canonical_json(payload) + "\n").encode("utf-8")
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:
            if self.path == "/health":
                self._send_json(200, write_health_artifact(artifact_dir, host=host, port=port))
                return
            if self.path == "/schema":
                self._send_json(200, write_schema_artifact(artifact_dir))
                return
            if self.path == "/version":
                self._send_json(200, {"service": "inside_voice_mcp", "protocol_version": PROTOCOL_VERSION})
                return
            if self.path == "/capabilities":
                self._send_json(200, capabilities_payload())
                return
            self._send_json(404, error_response("unknown endpoint", {"request_id": "", "mode": "audit"}))

        def do_POST(self) -> None:
            if self.path != "/consult":
                self._send_json(404, error_response("unknown endpoint", {"request_id": "", "mode": "audit"}))
                return

            try:
                content_length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                content_length = 0

            if content_length <= 0:
                result = process_consult_request({}, artifact_dir)
                self._send_json(400, result.response)
                return

            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                malformed = {"malformed_json_sha256": hashlib.sha256(body).hexdigest()}
                response = error_response("malformed_json_body", malformed)
                write_consultation_artifacts(malformed, response, artifact_dir)
                self._send_json(400, response)
                return

            result = process_consult_request(payload, artifact_dir)
            self._send_json(result.status_code, result.response)

    return InsideVoiceMCPHandler


def create_server(
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    artifact_dir: Path = ARTIFACT_DIR,
    allow_nonlocal: bool = False,
) -> ThreadingHTTPServer:
    validate_bind_host(host, allow_nonlocal=allow_nonlocal)
    handler = make_handler(artifact_dir=artifact_dir, host=host, port=port)
    return ThreadingHTTPServer((host, port), handler)


def run_server(
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    artifact_dir: Path = ARTIFACT_DIR,
    allow_nonlocal: bool = False,
) -> None:
    server = create_server(host=host, port=port, artifact_dir=artifact_dir, allow_nonlocal=allow_nonlocal)
    write_health_artifact(artifact_dir, host=host, port=port)
    write_schema_artifact(artifact_dir)
    print(f"Inside Voice MCP server listening on http://{host}:{port}", flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the local Inside Voice MCP pond-backed consultation server.")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--allow-nonlocal", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    try:
        run_server(host=args.host, port=args.port, allow_nonlocal=args.allow_nonlocal)
    except KeyboardInterrupt:
        print("Inside Voice MCP server stopped")
        return 0
    except ContractValidationError as exc:
        print(f"INSIDE_VOICE_MCP_CONTRACT_FAIL: {exc}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
