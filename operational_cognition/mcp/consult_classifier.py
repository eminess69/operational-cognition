"""Classify MCP consult responses for proof-boundary validation."""

from __future__ import annotations

from enum import Enum
from typing import Any, Iterable


class MCPConsultClass(str, Enum):
    POND_BACKED = "POND_BACKED"
    PLACEHOLDER = "PLACEHOLDER"
    MOCK = "MOCK"
    ERROR = "ERROR"
    UNKNOWN = "UNKNOWN"


STATUS_KEYS = {
    "adapter_status",
    "mcp_status",
    "pond_recall_status",
    "consult_status",
    "response_source",
    "source",
    "verdict",
    "status",
}

POND_BACKED_VALUES = {"pond_backed", "pond-backed", "pond backed"}
PLACEHOLDER_VALUES = {"placeholder", "scaffold", "stub"}
MOCK_VALUES = {"mock", "mocked", "synthetic_mock", "test_mock"}
ERROR_VALUES = {
    "error",
    "fail",
    "failed",
    "fail_closed",
    "invalid",
    "unavailable",
    "http_error",
    "transport_error",
}

LINEAGE_LIST_KEYS = {
    "lineage_hashes",
    "returned_lineage_hashes",
    "used_recalled_lineage_hashes",
    "runtime_hashes",
    "returned_lineages",
    "lineage_refs",
    "relevant_lineage_refs",
    "source_trace_refs",
    "selected_path_ids",
    "used_recalled_lineages",
    "retrieved_artifact_refs",
}

LINEAGE_SCALAR_KEYS = {
    "request_hash",
    "response_hash",
    "runtime_response_hash",
    "corpus_hash",
    "artifact_hash",
}

MOTIF_KEYS = {
    "returned_motifs",
    "recalled_motifs",
    "activated_motifs",
    "used_recalled_motifs",
    "motifs",
}


def normalize_value(value: Any) -> str:
    return str(value).strip().lower().replace(" ", "_").replace("-", "_")


def _walk(value: Any) -> Iterable[tuple[str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key), child
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def _status_values(response: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for key, value in _walk(response):
        if key in STATUS_KEYS and isinstance(value, (str, int, float, bool)):
            values.append(normalize_value(value))
    return values


def _contains_any(values: Iterable[str], targets: set[str]) -> bool:
    for value in values:
        if value in targets:
            return True
        if any(target in value for target in targets):
            return True
    return False


def _non_empty_scalar(value: Any) -> bool:
    return isinstance(value, (str, int, float)) and bool(str(value).strip())


def _non_empty_list(value: Any) -> bool:
    if not isinstance(value, list):
        return False
    return any(_non_empty_scalar(item) or (isinstance(item, dict) and bool(item)) for item in value)


def _non_empty_dict(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    return any(_non_empty_scalar(item) or _non_empty_list(item) for item in value.values())


def classify_mcp_response(response: dict[str, Any]) -> MCPConsultClass:
    """Return the boundary class for an MCP consult response-like object."""

    if not isinstance(response, dict):
        return MCPConsultClass.UNKNOWN

    values = _status_values(response)
    if _contains_any(values, PLACEHOLDER_VALUES):
        return MCPConsultClass.PLACEHOLDER
    if _contains_any(values, MOCK_VALUES):
        return MCPConsultClass.MOCK
    if _contains_any(values, ERROR_VALUES):
        return MCPConsultClass.ERROR
    if _contains_any(values, POND_BACKED_VALUES):
        return MCPConsultClass.POND_BACKED
    return MCPConsultClass.UNKNOWN


def has_lineage_evidence(response: dict[str, Any]) -> bool:
    """Return true when a response carries lineage refs or lineage hashes."""

    if not isinstance(response, dict):
        return False
    for key, value in _walk(response):
        if key in LINEAGE_LIST_KEYS and (_non_empty_list(value) or _non_empty_dict(value)):
            return True
        if key in LINEAGE_SCALAR_KEYS and _non_empty_scalar(value):
            return True
    return False


def has_motif_evidence(response: dict[str, Any]) -> bool:
    """Return true when a response carries returned/recalled/activated motifs."""

    if not isinstance(response, dict):
        return False
    for key, value in _walk(response):
        if key in MOTIF_KEYS and (_non_empty_list(value) or _non_empty_dict(value)):
            return True
    return False


def boundary_summary(response: dict[str, Any]) -> str:
    if not isinstance(response, dict):
        return "non-dict response"
    fields = []
    for key in ("adapter_status", "mcp_status", "pond_recall_status", "verdict", "response_source"):
        if key in response:
            fields.append(f"{key}={response[key]!r}")
    return ", ".join(fields) if fields else "no boundary status fields"

