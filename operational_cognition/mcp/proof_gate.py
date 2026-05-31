"""Fail-closed gates for proofs that claim pond-backed MCP consultation."""

from __future__ import annotations

from typing import Any

from operational_cognition.mcp.consult_classifier import (
    MCPConsultClass,
    boundary_summary,
    classify_mcp_response,
    has_lineage_evidence,
    has_motif_evidence,
)


class MCPConsultBoundaryError(AssertionError):
    """Raised when an MCP consult cannot support a pond-backed proof claim."""


def assert_pond_backed_consult(
    response: dict[str, Any],
    *,
    require_lineage: bool = True,
    require_motifs: bool = False,
) -> None:
    """Raise when a consult response is not valid pond-backed evidence."""

    classification = classify_mcp_response(response)
    if classification != MCPConsultClass.POND_BACKED:
        raise MCPConsultBoundaryError(
            "MCP consult rejected: "
            f"classification={classification.value}; expected=POND_BACKED; {boundary_summary(response)}"
        )

    if require_lineage and not has_lineage_evidence(response):
        raise MCPConsultBoundaryError(
            "MCP consult rejected: missing lineage evidence; expected lineage hashes or returned lineages"
        )

    if require_motifs and not has_motif_evidence(response):
        raise MCPConsultBoundaryError(
            "MCP consult rejected: missing motif evidence; expected returned/recalled/activated motifs"
        )
