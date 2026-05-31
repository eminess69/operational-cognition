#!/usr/bin/env python3
"""Run one Inside Voice behavior-protocol probe through the pond-backed MCP adapter."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from operational_cognition.mcp.consult_classifier import classify_mcp_response
from operational_cognition.mcp.proof_gate import MCPConsultBoundaryError, assert_pond_backed_consult
from tools.integrations.inside_voice_mcp_server import (
    MAX_OUTPUT_CHARS_CAP,
    canonical_json,
    hash_canonical_json,
    process_consult_request,
    write_json_artifact,
)


def build_request(mode: str, observation: str, max_output_chars: int) -> dict[str, Any]:
    request_id = f"behavior-probe-{hash_canonical_json({'mode': mode, 'observation': observation})[:16]}"
    return {
        "request_id": request_id,
        "task": (
            f"Inside Voice behavior protocol probe.\n"
            f"Mode: {mode}\n"
            f"Observation:\n{observation}\n"
            "Required:\n"
            "- returned motifs\n"
            "- returned lineages\n"
            "- lineage hashes\n"
            "- behavior fields for the requested mode"
        ),
        "context": {
            "summary": "Single behavior-protocol probe against the local Inside Voice pond.",
            "files": [],
            "constraints": ["No placeholder fallback.", "Fail closed if pond recall is unavailable."],
            "desired_artifacts": ["raw_request", "raw_response", "behavior_report", "validator_result"],
        },
        "mode": mode,
        "max_output_chars": max_output_chars,
        "require_lineage": True,
    }


def behavior_report(response: dict[str, Any]) -> dict[str, Any]:
    activated = response.get("activated_mechanisms", [])
    interactions = response.get("field_interactions", [])
    ranked = response.get("ranked_pathways", [])
    perturbations = response.get("perturbations", [])
    collapse_trace = response.get("collapse_trace", {})
    return {
        "request_id": response.get("request_id", ""),
        "mode": response.get("mode", ""),
        "classification": classify_mcp_response(response).value,
        "verdict": response.get("verdict", ""),
        "adapter_status": response.get("adapter_status", ""),
        "response_source": response.get("response_source", ""),
        "motif_count": len(response.get("returned_motifs", [])),
        "lineage_count": len(response.get("returned_lineages", [])),
        "lineage_hash_count": len(response.get("lineage_hashes", [])),
        "activated_mechanism_count": len(activated) if isinstance(activated, list) else 0,
        "interaction_count": len(interactions) if isinstance(interactions, list) else 0,
        "ranked_pathway_count": len(ranked) if isinstance(ranked, list) else 0,
        "perturbation_count": len(perturbations) if isinstance(perturbations, list) else 0,
        "collapse_trace_present": isinstance(collapse_trace, dict) and bool(collapse_trace),
        "fail_closed_reason": response.get("fail_closed_reason"),
    }


def validator_result(response: dict[str, Any]) -> dict[str, Any]:
    try:
        assert_pond_backed_consult(response, require_lineage=True, require_motifs=True)
    except MCPConsultBoundaryError as exc:
        return {
            "valid": False,
            "classification": classify_mcp_response(response).value,
            "error": str(exc),
        }
    return {
        "valid": True,
        "classification": classify_mcp_response(response).value,
        "error": None,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", required=True)
    parser.add_argument("--observation", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--state-path", type=Path, default=None)
    parser.add_argument("--max-output-chars", type=int, default=MAX_OUTPUT_CHARS_CAP)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    request = build_request(args.mode, args.observation, args.max_output_chars)
    result = process_consult_request(
        request,
        artifact_dir=args.out / "adapter_artifacts",
        state_path=args.state_path,
    )
    report = behavior_report(result.response)
    validation = validator_result(result.response)

    write_json_artifact(args.out / "raw_request.json", request)
    write_json_artifact(args.out / "raw_response.json", result.response)
    write_json_artifact(args.out / "parsed_behavior_report.json", report)
    write_json_artifact(args.out / "validator_result.json", validation)

    print(
        canonical_json(
            {
                "status_code": result.status_code,
                "classification": report["classification"],
                "validator_valid": validation["valid"],
                "out": str(args.out),
            }
        )
    )
    return 0 if result.status_code == 200 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
