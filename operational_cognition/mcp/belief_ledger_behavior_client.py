"""Belief Ledger Inside Voice behavior-protocol MCP client.

Operational Cognition treats Belief Ledger as an external instrument. This
client records the wire request/response and exposes only validated,
pond-backed behavior rows to proof artifacts.
"""

from __future__ import annotations

import hashlib
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_BELIEF_LEDGER_URL = "http://127.0.0.1:8765"
DEFAULT_ENDPOINT_PATH = "/protocol/behavior"
RESPONSE_SOURCE = "belief_ledger_inside_voice_behavior_protocol"
BEHAVIOR_PROTOCOL_SCHEMA = "inside_voice.behavior_protocol.v1"
BEHAVIOR_MODES = (
    "recall",
    "activation_only",
    "field_interaction",
    "delayed_ranking",
    "collapse_trace",
    "perturbation",
)


class BehaviorProtocolValidationError(ValueError):
    """Raised when the external behavior response cannot support a proof row."""


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def hash_canonical_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _dedupe_sorted(values: list[Any]) -> list[str]:
    return sorted({str(value) for value in values if str(value)})


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _append_jsonl(path: Path | None, row: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(canonical_json(row) + "\n")


def build_behavior_protocol_request(
    mode: str,
    query_trace: dict[str, Any],
    ledger_state: dict[str, Any],
    config: dict[str, Any] | None = None,
    perturbation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the deterministic Belief Ledger `/protocol/behavior` payload."""

    behavior_config = dict(config or {})
    behavior_perturbation = dict(perturbation or {})
    hash_material = {
        "mode": mode,
        "query_trace": query_trace,
        "ledger_state": ledger_state,
        "config": behavior_config,
        "perturbation": behavior_perturbation,
    }
    return {
        "run_id": f"oc-proof-045-{hash_canonical_json(hash_material)[:16]}",
        "mode": mode,
        "query_trace": query_trace,
        "ledger_state": ledger_state,
        "config": behavior_config,
        "perturbation": behavior_perturbation,
    }


def _response_hash_material(response: dict[str, Any]) -> dict[str, Any]:
    material = json.loads(canonical_json(response))
    lineage = material.get("lineage")
    if isinstance(lineage, dict):
        lineage["response_hash"] = ""
    return material


def _finalize_response(response: dict[str, Any]) -> dict[str, Any]:
    response.setdefault("lineage", {})["response_hash"] = hash_canonical_json(_response_hash_material(response))
    return response


def _fail_closed_response(
    *,
    mode: str,
    request_payload: dict[str, Any],
    reason: str,
    endpoint: str,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    response = {
        "request_id": str(request_payload.get("run_id") or ""),
        "adapter_status": "error",
        "verdict": "fail_closed",
        "response_source": RESPONSE_SOURCE,
        "mode": mode,
        "returned_motifs": [],
        "returned_lineages": [],
        "lineage_hashes": [],
        "recall_summary": "",
        "fail_closed_reason": reason,
        "summary": f"Belief Ledger behavior protocol call failed closed: {reason}.",
        "details": details or {},
        "endpoint": endpoint,
        "lineage": {
            "request_hash": hash_canonical_json(request_payload),
            "instrument_request_hash": "",
            "response_hash": "",
            "instrument_response_hash": "",
            "source_refs": [],
        },
    }
    return _finalize_response(response)


def _extract_traceability(data: dict[str, Any]) -> dict[str, Any]:
    artifacts = _dict(data.get("artifacts"))
    field = _dict(artifacts.get("activation_field"))
    activated_motifs = [_dict(item) for item in _list(field.get("activated_motifs"))]
    activated_pathways = [_dict(item) for item in _list(field.get("activated_pathways"))]
    hash_spine = [_dict(item) for item in _list(data.get("hash_spine"))]

    motifs = _dedupe_sorted(
        [item.get("motif") for item in activated_motifs]
        + [item.get("motif_id") for item in activated_motifs]
        + [motif for item in activated_pathways for motif in _list(item.get("supporting_motif_ids"))]
    )
    lineages = _dedupe_sorted(
        _list(field.get("lineage_refs"))
        + _list(field.get("source_trace_ids"))
        + [ref for item in activated_motifs for ref in _list(item.get("source_lineage_refs"))]
        + [trace for item in activated_motifs for trace in _list(item.get("source_trace_ids"))]
        + [ref for item in activated_pathways for ref in _list(item.get("source_lineage_refs"))]
        + [trace for item in activated_pathways for trace in _list(item.get("supporting_trace_ids"))]
    )
    lineage_hashes = _dedupe_sorted(
        _list(field.get("lineage_hashes"))
        + [lineage_hash for item in activated_motifs for lineage_hash in _list(item.get("lineage_hashes"))]
        + [lineage_hash for item in activated_pathways for lineage_hash in _list(item.get("lineage_hashes"))]
        + [lineage_hash for item in hash_spine for lineage_hash in _list(item.get("lineage_hashes"))]
    )
    return {
        "returned_motifs": motifs,
        "returned_lineages": lineages,
        "lineage_hashes": lineage_hashes,
    }


def _activated_mechanisms(data: dict[str, Any]) -> list[dict[str, Any]]:
    field = _dict(_dict(data.get("artifacts")).get("activation_field"))
    mechanisms = []
    for pathway in [_dict(item) for item in _list(field.get("activated_pathways"))]:
        mechanism = str(pathway.get("pathway") or pathway.get("pathway_id") or "")
        if not mechanism:
            continue
        mechanisms.append(
            {
                "mechanism": mechanism,
                "pathway_id": str(pathway.get("pathway_id") or ""),
                "activation_weight": pathway.get("activation_weight", 0.0),
                "supporting_motifs": _list(pathway.get("supporting_motif_ids")),
                "supporting_lineages": _list(pathway.get("source_lineage_refs")) + _list(pathway.get("supporting_trace_ids")),
                "supporting_lineage_hashes": _list(pathway.get("lineage_hashes")),
            }
        )
    return mechanisms


def _field_interactions(data: dict[str, Any]) -> list[dict[str, Any]]:
    interaction = _dict(_dict(data.get("artifacts")).get("field_interaction"))
    rows = []
    for candidate in [_dict(item) for item in _list(interaction.get("candidate_interactions"))]:
        rows.append(
            {
                "pathway_id": str(candidate.get("candidate_id") or ""),
                "pathway": " + ".join(str(item) for item in _list(candidate.get("pathway_ids"))),
                "mechanisms": _list(candidate.get("pathway_ids")),
                "combination_depth": candidate.get("combination_depth", 0),
                "interaction_weight": candidate.get("interaction_weight", 0.0),
                "supporting_motifs": _list(candidate.get("shared_motifs")),
                "shared_motifs": _list(candidate.get("shared_motifs")),
                "supporting_lineages": _list(candidate.get("shared_lineages")) + _list(candidate.get("supporting_trace_ids")),
                "supporting_lineage_hashes": _list(candidate.get("lineage_hashes")),
            }
        )
    return rows


def _collapse_artifact(data: dict[str, Any]) -> dict[str, Any]:
    return _dict(_dict(data.get("artifacts")).get("delayed_collapse_trace"))


def _ranked_pathways(data: dict[str, Any]) -> list[dict[str, Any]]:
    collapse = _collapse_artifact(data)
    rows = []
    for survivor in [_dict(item) for item in _list(collapse.get("surviving_pathways"))]:
        row = dict(survivor)
        row["rank"] = survivor.get("survival_rank", len(rows) + 1)
        row["collapse_status"] = "survived"
        rows.append(row)
    for eliminated in [_dict(item) for item in _list(collapse.get("eliminated_pathways"))]:
        row = dict(eliminated)
        row["rank"] = eliminated.get("elimination_rank", len(rows) + 1)
        row["collapse_status"] = "eliminated"
        rows.append(row)
    rows.sort(key=lambda item: int(item.get("rank") or 0))
    return rows


def _collapse_trace(data: dict[str, Any]) -> dict[str, Any]:
    collapse = _collapse_artifact(data)
    if not collapse:
        return {}
    return {
        "collapse_id": collapse.get("collapse_id", ""),
        "survived_after_collapse": _list(collapse.get("surviving_pathways")),
        "eliminated_pathways": _list(collapse.get("eliminated_pathways")),
        "collapse_reasons": _list(collapse.get("collapse_reasons")),
        "collapse_reason": "Belief Ledger delayed-collapse trace preserved survivors, eliminations, and reason codes.",
        "premature_collapse_risk": bool(collapse.get("premature_collapse_risk")),
    }


def _perturbations(data: dict[str, Any]) -> list[dict[str, Any]]:
    perturbation = _dict(_dict(data.get("artifacts")).get("perturbation_result"))
    return [perturbation] if perturbation else []


def _validate_behavior_data(data: dict[str, Any], *, mode: str) -> None:
    if data.get("schema_version") != BEHAVIOR_PROTOCOL_SCHEMA:
        raise BehaviorProtocolValidationError("schema_version_missing_or_unrecognized")
    if data.get("mode") != mode:
        raise BehaviorProtocolValidationError("mode_mismatch")
    if data.get("core_mutation_count") != 0 or data.get("advisory_only") is not True:
        raise BehaviorProtocolValidationError("instrument_boundary_not_preserved")

    artifacts = _dict(data.get("artifacts"))
    field = _dict(artifacts.get("activation_field"))
    if not field or field.get("core_mutation_count") != 0:
        raise BehaviorProtocolValidationError("activation_field_missing_or_mutating")

    traceability = _extract_traceability(data)
    if not traceability["returned_motifs"]:
        raise BehaviorProtocolValidationError("missing_motifs")
    if not traceability["returned_lineages"]:
        raise BehaviorProtocolValidationError("missing_lineages")
    if not traceability["lineage_hashes"]:
        raise BehaviorProtocolValidationError("missing_lineage_hashes")

    if mode == "activation_only" and len(_activated_mechanisms(data)) < 1:
        raise BehaviorProtocolValidationError("activation_missing")
    if mode == "field_interaction" and not _field_interactions(data):
        raise BehaviorProtocolValidationError("field_interactions_missing")
    if mode == "delayed_ranking" and not _list(_collapse_artifact(data).get("surviving_pathways")):
        raise BehaviorProtocolValidationError("surviving_pathways_missing")
    if mode == "collapse_trace":
        collapse = _collapse_artifact(data)
        if not _list(collapse.get("surviving_pathways")):
            raise BehaviorProtocolValidationError("collapse_survivors_missing")
        if not _list(collapse.get("eliminated_pathways")):
            raise BehaviorProtocolValidationError("collapse_eliminations_missing")
        if not _list(collapse.get("collapse_reasons")):
            raise BehaviorProtocolValidationError("collapse_reasons_missing")
    if mode == "perturbation":
        perturbation = _dict(artifacts.get("perturbation_result"))
        if not perturbation:
            raise BehaviorProtocolValidationError("perturbation_result_missing")
        if perturbation.get("changed") is not True and not perturbation.get("no_effect_reason"):
            raise BehaviorProtocolValidationError("perturbation_no_change_without_reason")


def _normalize_success_response(
    *,
    mode: str,
    request_payload: dict[str, Any],
    endpoint: str,
    envelope: dict[str, Any],
    data: dict[str, Any],
) -> dict[str, Any]:
    _validate_behavior_data(data, mode=mode)
    traceability = _extract_traceability(data)
    response = {
        "request_id": str(data.get("run_id") or request_payload.get("run_id") or ""),
        "adapter_status": "pond_backed",
        "verdict": "ok",
        "response_source": RESPONSE_SOURCE,
        "mode": mode,
        "returned_motifs": traceability["returned_motifs"],
        "returned_lineages": traceability["returned_lineages"],
        "lineage_hashes": traceability["lineage_hashes"],
        "recall_summary": "Validated Belief Ledger behavior protocol response with motifs, lineage refs, lineage hashes, and no core mutation.",
        "fail_closed_reason": None,
        "endpoint": endpoint,
        "instrument_ok": bool(envelope.get("ok", True)),
        "instrument_verdict": str(envelope.get("verdict") or ""),
        "instrument_schema_version": str(data.get("schema_version") or ""),
        "instrument_response_hash": str(data.get("response_hash") or ""),
        "instrument_core_mutation_count": data.get("core_mutation_count"),
        "activated_mechanisms": _activated_mechanisms(data),
        "field_interactions": _field_interactions(data),
        "ranked_pathways": _ranked_pathways(data),
        "surviving_pathways": _list(_collapse_artifact(data).get("surviving_pathways")),
        "collapse_trace": _collapse_trace(data),
        "perturbations": _perturbations(data),
        "perturbation_summary": _dict(_dict(data.get("artifacts")).get("perturbation_result")),
        "hash_spine": _list(data.get("hash_spine")),
        "telemetry": _dict(data.get("telemetry")),
        "lineage": {
            "request_hash": hash_canonical_json(request_payload),
            "instrument_request_hash": str(data.get("request_hash") or ""),
            "response_hash": "",
            "instrument_response_hash": str(data.get("response_hash") or ""),
            "source_refs": traceability["returned_lineages"],
        },
    }
    return _finalize_response(response)


@dataclass
class BeliefLedgerBehaviorClient:
    """HTTP client for the Belief Ledger behavior protocol endpoint."""

    base_url: str = DEFAULT_BELIEF_LEDGER_URL
    raw_request_log_path: Path | None = None
    raw_response_log_path: Path | None = None
    behavior_call_log_path: Path | None = None
    timeout_seconds: float = 10.0
    endpoint_path: str = DEFAULT_ENDPOINT_PATH

    @property
    def endpoint_url(self) -> str:
        return f"{self.base_url.rstrip('/')}{self.endpoint_path}"

    def call_behavior_protocol(
        self,
        mode: str,
        query_trace: dict[str, Any],
        ledger_state: dict[str, Any],
        config: dict[str, Any] | None = None,
        perturbation: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload = build_behavior_protocol_request(mode, query_trace, ledger_state, config, perturbation)
        request_hash = hash_canonical_json(payload)
        endpoint = self.endpoint_url
        _append_jsonl(
            self.raw_request_log_path,
            {
                "event": "belief_ledger_behavior_protocol_request",
                "endpoint": endpoint,
                "mode": mode,
                "request_hash": request_hash,
                "request": payload,
            },
        )

        if mode not in BEHAVIOR_MODES:
            response = _fail_closed_response(
                mode=mode,
                request_payload=payload,
                reason="unknown_mode",
                endpoint=endpoint,
            )
            _append_jsonl(self.raw_response_log_path, {"request_hash": request_hash, "response": response})
            return response

        body = canonical_json(payload).encode("utf-8")
        request = urllib.request.Request(
            endpoint,
            data=body,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response_handle:
                status_code = int(getattr(response_handle, "status", 200))
                response_body = response_handle.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            response_body = exc.read().decode("utf-8", errors="replace")
            fail = _fail_closed_response(
                mode=mode,
                request_payload=payload,
                reason="http_error",
                endpoint=endpoint,
                details={"status_code": int(exc.code), "body": response_body},
            )
            _append_jsonl(
                self.raw_response_log_path,
                {"request_hash": request_hash, "status_code": int(exc.code), "body": response_body, "response": fail},
            )
            return fail
        except (OSError, TimeoutError) as exc:
            fail = _fail_closed_response(
                mode=mode,
                request_payload=payload,
                reason="connection_error",
                endpoint=endpoint,
                details={"error": str(exc)},
            )
            _append_jsonl(self.raw_response_log_path, {"request_hash": request_hash, "response": fail})
            return fail

        try:
            envelope = json.loads(response_body)
        except json.JSONDecodeError:
            fail = _fail_closed_response(
                mode=mode,
                request_payload=payload,
                reason="invalid_json_response",
                endpoint=endpoint,
                details={"status_code": status_code, "body": response_body},
            )
            _append_jsonl(
                self.raw_response_log_path,
                {"request_hash": request_hash, "status_code": status_code, "body": response_body, "response": fail},
            )
            return fail

        _append_jsonl(
            self.raw_response_log_path,
            {
                "event": "belief_ledger_behavior_protocol_response",
                "request_hash": request_hash,
                "status_code": status_code,
                "raw_response": envelope,
            },
        )

        if not isinstance(envelope, dict):
            return _fail_closed_response(
                mode=mode,
                request_payload=payload,
                reason="non_object_response",
                endpoint=endpoint,
            )
        if envelope.get("ok") is False:
            return _fail_closed_response(
                mode=mode,
                request_payload=payload,
                reason="instrument_fail_closed",
                endpoint=endpoint,
                details={"errors": _list(envelope.get("errors")), "verdict": envelope.get("verdict")},
            )

        data = _dict(envelope.get("data") if "data" in envelope else envelope)
        try:
            normalized = _normalize_success_response(
                mode=mode,
                request_payload=payload,
                endpoint=endpoint,
                envelope=envelope,
                data=data,
            )
        except BehaviorProtocolValidationError as exc:
            return _fail_closed_response(
                mode=mode,
                request_payload=payload,
                reason=str(exc),
                endpoint=endpoint,
                details={"instrument_response_hash": data.get("response_hash", "")},
            )

        _append_jsonl(self.behavior_call_log_path, normalized)
        return normalized


def call_behavior_protocol(
    mode: str,
    query_trace: dict[str, Any],
    ledger_state: dict[str, Any],
    config: dict[str, Any] | None = None,
    perturbation: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Call the default Belief Ledger behavior endpoint and fail closed."""

    client = BeliefLedgerBehaviorClient(base_url=os.environ.get("BELIEF_LEDGER_URL", DEFAULT_BELIEF_LEDGER_URL))
    return client.call_behavior_protocol(mode, query_trace, ledger_state, config, perturbation)

