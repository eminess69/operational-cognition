#!/usr/bin/env python3
"""Validate a Proof 011 redacted-real/public trace candidate scaffold."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

VALID_STATUSES = {"not_selected", "selected", "rejected", "eligible"}
VALID_CANDIDATE_TYPES = {"public", "redacted_real", "none"}
BANNED_STRINGS = ("password", "secret", "token", "api_key", "private_key")

REQUIRED_FILES = [
    "README.md",
    "candidate_selection_policy.md",
    "trace_conversion_plan.md",
    "eligibility_matrix.md",
    "redaction_policy.md",
    "candidate_manifest.json",
    "proof_manifest.json",
    "public_lineage_summary.md",
    "unresolved_requirements.md",
    "candidate/README.md",
    "candidate/.gitkeep",
]

REQUIRED_ELIGIBILITY_FIELDS = [
    "has_transcript",
    "has_event_log",
    "has_tool_action_log",
    "has_tool_result_refs",
    "has_memory_refs",
    "has_compression_or_summary_boundary",
    "has_omitted_range_refs",
    "has_contradiction_or_correction",
    "has_authority_refs",
    "has_temporal_validity_refs",
    "has_environment_refs",
    "has_runtime_config",
    "has_recovery_or_retry_trace",
    "has_provenance_manifest",
]


def load_json(path: Path, errors: list[str]) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return None


def ensure_bool(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, bool):
        errors.append(f"{path}: expected boolean")


def ensure_string(value: Any, path: str, errors: list[str], *, allow_empty: bool = False) -> None:
    if not isinstance(value, str):
        errors.append(f"{path}: expected string")
        return
    if not allow_empty and not value:
        errors.append(f"{path}: expected non-empty string")


def ensure_string_list(value: Any, path: str, errors: list[str], *, allow_empty: bool) -> None:
    if not isinstance(value, list):
        errors.append(f"{path}: expected array")
        return
    if not allow_empty and not value:
        errors.append(f"{path}: expected non-empty array")
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item:
            errors.append(f"{path}[{index}]: expected non-empty string")


def check_required_files(proof_dir: Path, errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        if not (proof_dir / relative).is_file():
            errors.append(f"missing required artifact: {relative}")


def check_candidate_file_scan(proof_dir: Path, errors: list[str]) -> None:
    candidate_dir = proof_dir / "candidate"
    if not candidate_dir.is_dir():
        errors.append("missing required artifact: candidate/")
        return

    for path in sorted(candidate_dir.rglob("*")):
        if not path.is_file():
            continue
        try:
            content = path.read_bytes().lower()
        except OSError as exc:
            errors.append(f"{path}: cannot read candidate file: {exc}")
            continue
        for banned in BANNED_STRINGS:
            if banned.encode("utf-8") in content:
                errors.append(f"{path}: banned string detected: {banned}")


def check_manifest_shape(manifest: Any, errors: list[str]) -> None:
    if not isinstance(manifest, dict):
        errors.append("candidate_manifest: expected object")
        return

    if manifest.get("proof_id") != "011-redacted-real-trace-candidate":
        errors.append("candidate_manifest.proof_id: expected 011-redacted-real-trace-candidate")

    status = manifest.get("candidate_status")
    if status not in VALID_STATUSES:
        errors.append(f"candidate_manifest.candidate_status: expected one of {sorted(VALID_STATUSES)}")

    candidate_type = manifest.get("candidate_type")
    if candidate_type not in VALID_CANDIDATE_TYPES:
        errors.append(
            f"candidate_manifest.candidate_type: expected one of {sorted(VALID_CANDIDATE_TYPES)}"
        )

    ensure_string(manifest.get("source_description"), "candidate_manifest.source_description", errors)
    ensure_string_list(
        manifest.get("source_refs"),
        "candidate_manifest.source_refs",
        errors,
        allow_empty=True,
    )
    ensure_bool(manifest.get("redaction_required"), "candidate_manifest.redaction_required", errors)
    ensure_bool(manifest.get("redaction_complete"), "candidate_manifest.redaction_complete", errors)

    eligibility = manifest.get("eligibility")
    if not isinstance(eligibility, dict):
        errors.append("candidate_manifest.eligibility: expected object")
    else:
        for field in REQUIRED_ELIGIBILITY_FIELDS:
            if field not in eligibility:
                errors.append(f"candidate_manifest.eligibility: missing required field {field}")
            else:
                ensure_bool(eligibility[field], f"candidate_manifest.eligibility.{field}", errors)

    decision = manifest.get("decision")
    if not isinstance(decision, dict):
        errors.append("candidate_manifest.decision: expected object")
    else:
        ensure_bool(
            decision.get("eligible_for_execution"),
            "candidate_manifest.decision.eligible_for_execution",
            errors,
        )
        ensure_string(decision.get("reason"), "candidate_manifest.decision.reason", errors)


def check_status_rules(manifest: dict[str, Any], errors: list[str]) -> None:
    status = manifest.get("candidate_status")
    candidate_type = manifest.get("candidate_type")
    source_refs = manifest.get("source_refs")
    eligibility = manifest.get("eligibility")
    decision = manifest.get("decision")

    eligible_for_execution = None
    if isinstance(decision, dict):
        eligible_for_execution = decision.get("eligible_for_execution")

    if status == "not_selected":
        if candidate_type != "none":
            errors.append("candidate_manifest.candidate_type: not_selected requires none")
        if eligible_for_execution is not False:
            errors.append("candidate_manifest.decision.eligible_for_execution: not_selected requires false")

    if status != "eligible" and eligible_for_execution is True:
        errors.append("candidate_manifest.decision.eligible_for_execution: only eligible candidates may execute")

    if status == "eligible":
        if candidate_type == "none":
            errors.append("candidate_manifest.candidate_type: eligible requires public or redacted_real")
        if not isinstance(source_refs, list) or not source_refs:
            errors.append("candidate_manifest.source_refs: eligible requires at least one source ref")
        if manifest.get("redaction_complete") is not True:
            errors.append("candidate_manifest.redaction_complete: eligible requires true")
        if eligible_for_execution is not True:
            errors.append("candidate_manifest.decision.eligible_for_execution: eligible requires true")
        if isinstance(eligibility, dict):
            for field in REQUIRED_ELIGIBILITY_FIELDS:
                if eligibility.get(field) is not True:
                    errors.append(f"candidate_manifest.eligibility.{field}: eligible requires true")


def validate_trace_candidate(proof_dir: Path) -> list[str]:
    if not proof_dir.is_absolute():
        proof_dir = ROOT / proof_dir

    errors: list[str] = []
    check_required_files(proof_dir, errors)
    check_candidate_file_scan(proof_dir, errors)

    manifest_path = proof_dir / "candidate_manifest.json"
    manifest = load_json(manifest_path, errors)
    if manifest is not None:
        check_manifest_shape(manifest, errors)
        if isinstance(manifest, dict):
            check_status_rules(manifest, errors)

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_trace_candidate.py <proof_dir>", file=sys.stderr)
        return 2

    errors = validate_trace_candidate(Path(argv[1]))
    if errors:
        print("TRACE_CANDIDATE_INVALID")
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("TRACE_CANDIDATE_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
