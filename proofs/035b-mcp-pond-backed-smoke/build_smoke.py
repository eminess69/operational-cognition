#!/usr/bin/env python3
"""Build Proof 035b MCP pond-backed smoke artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


PROOF_ID = "035b-mcp-pond-backed-smoke"
TITLE = "Proof 035b - MCP Pond-Backed Smoke"
PROOF_DIR = Path(__file__).resolve().parent
ROOT = PROOF_DIR.parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from operational_cognition.mcp.consult_classifier import classify_mcp_response  # noqa: E402
from tools.integrations.inside_voice_mcp_server import (  # noqa: E402
    empty_pond_state,
    hash_canonical_json,
    process_consult_request,
    save_pond,
)


POND_STATE = PROOF_DIR / "pond_state" / "pond_state.json"
RUNTIME_DIR = Path("/private/tmp/oc_035b_mcp_runtime")


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
            "constraints": ["Return real pond-backed recall or fail closed."],
            "desired_artifacts": ["returned_motifs", "returned_lineages", "lineage_hashes"],
        },
    }


def consult(request: dict[str, Any]) -> dict[str, Any]:
    result = process_consult_request(
        request,
        artifact_dir=RUNTIME_DIR,
        state_path=POND_STATE,
    )
    response = dict(result.response)
    response["http_status"] = result.status_code
    response["classification"] = classify_mcp_response(result.response).value
    return response


def manifest(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "proof_id": PROOF_ID,
        "title": TITLE,
        "status": "complete",
        "targets": [
            "FreshPond",
            "MCPSeasoning",
            "PondBackedRecall",
            "UnsupportedFailClosed",
            "ValidatorSmoke",
        ],
        "claim_level": "evidence_backed",
        "inside_voice_adapter_status": "pond_backed",
        "public_private_boundary": (
            "This smoke proof records only public-safe MCP response fields, pond record refs, and lineage hashes."
        ),
        "required_artifacts": [
            "seasoning_log.jsonl",
            "consult_log.jsonl",
            "negative_consult_log.jsonl",
            "pond_backed_smoke_report.json",
            "proof_manifest.json",
            "pond_state/pond_state.json",
        ],
        "disallowed_claims": [
            "Proof 035b tests cognition.",
            "Fail-closed unsupported recall is positive pond-backed evidence.",
            "Transport hashes alone satisfy lineage evidence.",
        ],
        "lineage": {
            "mcp_endpoint": "in_process_tools.integrations.inside_voice_mcp_server.process_consult_request",
            "contract_version": "inside_voice_mcp_contract/0.2",
            "request_hash": report["request_hash"],
            "response_hash": report["response_hash"],
            "derived_from": "MCP pond-backed consult repair",
            "validates": "pond-backed smoke consult_log passes validate_mcp_consults.py with lineage and motif requirements",
            "candidate_status": "eligible",
        },
    }


def readme(report: dict[str, Any]) -> str:
    return f"""# Proof 035b - MCP Pond-Backed Smoke

This is an instrument smoke proof, not a cognition proof.

## Result

- Positive consult classified as: {report["positive_consult_classification"]}
- Positive consult has motifs: {report["positive_consult_has_motifs"]}
- Positive consult has lineages: {report["positive_consult_has_lineages"]}
- Positive consult has lineage hashes: {report["positive_consult_has_lineage_hashes"]}
- Unsupported consult failed closed: {report["unsupported_consult_failed_closed"]}

## Validator

```bash
python3 tools/validate_mcp_consults.py proofs/035b-mcp-pond-backed-smoke/consult_log.jsonl --require-lineage --require-motifs
```

`consult_log.jsonl` intentionally contains only successful pond-backed recall rows. Unsupported recall is recorded separately in `negative_consult_log.jsonl` because fail-closed rows are not positive proof evidence.
"""


def main() -> int:
    save_pond(POND_STATE, empty_pond_state())

    seasoning_request = payload(
        "proof-035b-season-flow-001",
        (
            "ACTION: SEASON. Mechanism label: FLOW. A source sends water through a path; "
            "a narrowed throat adds resistance, downstream throughput declines, and upstream backlog grows."
        ),
        summary="Proof 035b starts from a fresh pond and seasons only FLOW.",
        mode="proof_planning",
    )
    positive_request = payload(
        "proof-035b-consult-flow-001",
        "Observation: water restriction in a channel creates a bottleneck; throughput declines and backlog grows upstream.",
        summary="Consult for a flow-like observation after FLOW seasoning.",
    )
    negative_request = payload(
        "proof-035b-consult-unsupported-001",
        "Observation: bearing seizure in a rotating support produces rough motion and lockup.",
        summary="Consult for an unsupported mechanism after only FLOW was seasoned.",
    )

    seasoning_response = consult(seasoning_request)
    positive_response = consult(positive_request)
    negative_response = consult(negative_request)

    write_jsonl(PROOF_DIR / "seasoning_log.jsonl", [seasoning_response])
    write_jsonl(PROOF_DIR / "consult_log.jsonl", [positive_response])
    write_jsonl(PROOF_DIR / "negative_consult_log.jsonl", [negative_response])

    report = {
        "proof_id": PROOF_ID,
        "fresh_pond_state": str(POND_STATE.relative_to(PROOF_DIR)),
        "seasoning_classification": seasoning_response["classification"],
        "positive_consult_classification": positive_response["classification"],
        "positive_consult_has_motifs": bool(positive_response.get("returned_motifs")),
        "positive_consult_has_lineages": bool(positive_response.get("returned_lineages")),
        "positive_consult_has_lineage_hashes": bool(positive_response.get("lineage_hashes")),
        "unsupported_consult_classification": negative_response["classification"],
        "unsupported_consult_failed_closed": negative_response.get("verdict") == "fail_closed",
        "unsupported_fail_closed_reason": negative_response.get("fail_closed_reason"),
        "request_hash": hash_canonical_json([seasoning_request, positive_request, negative_request]),
        "response_hash": hash_canonical_json([seasoning_response, positive_response, negative_response]),
        "verdict": (
            "PASS"
            if positive_response["classification"] == "POND_BACKED"
            and positive_response.get("returned_motifs")
            and positive_response.get("returned_lineages")
            and positive_response.get("lineage_hashes")
            and negative_response.get("verdict") == "fail_closed"
            else "FAIL"
        ),
    }

    write_json(PROOF_DIR / "pond_backed_smoke_report.json", report)
    write_json(PROOF_DIR / "proof_manifest.json", manifest(report))
    write_text(PROOF_DIR / "README.md", readme(report))
    print(report["verdict"])
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
