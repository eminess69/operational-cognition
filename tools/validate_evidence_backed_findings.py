#!/usr/bin/env python3
"""Validate evidence-backed findings for an Operational Cognition proof."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

ALLOWED_CLAIM_LEVELS = {"observed", "inferred", "hypothesis", "unresolved"}
TOP_LEVEL_KEYS = {"analysis_id", "findings", "proof_id", "status", "summary"}
FINDING_KEYS = {
    "claim",
    "claim_level",
    "evidence_refs",
    "id",
    "limitations",
    "public_private_boundary",
    "reasoning_summary",
}
SUMMARY_KEYS = {"hypothesis_count", "inferred_count", "observed_count", "unresolved_count"}
DISALLOWED_PATTERNS = {
    "AGI": re.compile(r"\bAGI\b", re.IGNORECASE),
    "consciousness": re.compile(r"\bconsciousness\b", re.IGNORECASE),
    "superintelligence": re.compile(r"\bsuperintelligence\b", re.IGNORECASE),
    "black_box_solved": re.compile(r"\bblack[_ -]?box[_ -]?solved\b", re.IGNORECASE),
    "substrate_disclosure": re.compile(r"\bsubstrate[_ -]?disclosure\b", re.IGNORECASE),
    "hidden_chain_of_thought": re.compile(
        r"\bhidden[_ -]?chain(?:[_ -]?of)?[_ -]?thought\b", re.IGNORECASE
    ),
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def evidence_ids(evidence_manifest: Any) -> set[str]:
    if not isinstance(evidence_manifest, dict):
        return set()
    sources = evidence_manifest.get("sources")
    if not isinstance(sources, list):
        return set()
    return {source.get("id") for source in sources if isinstance(source, dict) and source.get("id")}


def iter_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        strings: list[str] = []
        for item in value:
            strings.extend(iter_strings(item))
        return strings
    if isinstance(value, dict):
        strings = []
        for item in value.values():
            strings.extend(iter_strings(item))
        return strings
    return []


def validate_disallowed_text(value: Any, path: str, errors: list[str]) -> None:
    for text in iter_strings(value):
        for label, pattern in DISALLOWED_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{path}: disallowed claim text {label}")


def validate_string_list(value: Any, path: str, errors: list[str], *, allow_empty: bool) -> None:
    if not isinstance(value, list):
        errors.append(f"{path}: expected array")
        return
    if not allow_empty and not value:
        errors.append(f"{path}: expected non-empty array")
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item:
            errors.append(f"{path}[{index}]: expected non-empty string")


def validate_finding(
    finding: Any,
    index: int,
    known_evidence_ids: set[str],
    seen_ids: set[str],
    errors: list[str],
) -> None:
    path = f"$.findings[{index}]"
    if not isinstance(finding, dict):
        errors.append(f"{path}: expected object")
        return

    missing = FINDING_KEYS - set(finding)
    unexpected = set(finding) - FINDING_KEYS
    for field in sorted(missing):
        errors.append(f"{path}: missing required field {field}")
    for field in sorted(unexpected):
        errors.append(f"{path}: unexpected field {field}")
    if missing:
        return

    finding_id = finding.get("id")
    if not isinstance(finding_id, str) or not finding_id:
        errors.append(f"{path}.id: expected non-empty string")
    elif finding_id in seen_ids:
        errors.append(f"{path}.id: duplicate finding ID {finding_id}")
    else:
        seen_ids.add(finding_id)

    if finding.get("claim_level") not in ALLOWED_CLAIM_LEVELS:
        errors.append(f"{path}.claim_level: expected one of {sorted(ALLOWED_CLAIM_LEVELS)}")

    for field in ("claim", "reasoning_summary", "public_private_boundary"):
        if not isinstance(finding.get(field), str) or not finding[field]:
            errors.append(f"{path}.{field}: expected non-empty string")

    validate_string_list(finding.get("limitations"), f"{path}.limitations", errors, allow_empty=True)
    validate_string_list(finding.get("evidence_refs"), f"{path}.evidence_refs", errors, allow_empty=True)

    evidence_refs = finding.get("evidence_refs")
    if isinstance(evidence_refs, list):
        for ref in evidence_refs:
            if isinstance(ref, str) and ref not in known_evidence_ids:
                errors.append(f"{path}.evidence_refs: unknown evidence_ref {ref}")

    if finding.get("claim_level") in {"observed", "inferred"} and not evidence_refs:
        errors.append(f"{path}.evidence_refs: observed/inferred findings require evidence_refs")

    validate_disallowed_text(finding, path, errors)


def validate_summary(summary: Any, findings: list[Any], errors: list[str]) -> None:
    if not isinstance(summary, dict):
        errors.append("$.summary: expected object")
        return

    missing = SUMMARY_KEYS - set(summary)
    unexpected = set(summary) - SUMMARY_KEYS
    for field in sorted(missing):
        errors.append(f"$.summary: missing required field {field}")
    for field in sorted(unexpected):
        errors.append(f"$.summary: unexpected field {field}")
    if missing:
        return

    counts = Counter(
        finding.get("claim_level")
        for finding in findings
        if isinstance(finding, dict) and finding.get("claim_level") in ALLOWED_CLAIM_LEVELS
    )
    expected = {
        "observed_count": counts["observed"],
        "inferred_count": counts["inferred"],
        "hypothesis_count": counts["hypothesis"],
        "unresolved_count": counts["unresolved"],
    }
    for field, value in expected.items():
        if summary.get(field) != value:
            errors.append(f"$.summary.{field}: expected {value}, got {summary.get(field)}")


def validate_findings_data(findings_doc: Any, evidence_manifest: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(findings_doc, dict):
        return ["$: expected object"]

    missing = TOP_LEVEL_KEYS - set(findings_doc)
    unexpected = set(findings_doc) - TOP_LEVEL_KEYS
    for field in sorted(missing):
        errors.append(f"$: missing required field {field}")
    for field in sorted(unexpected):
        errors.append(f"$: unexpected field {field}")
    if missing:
        return errors

    for field in ("proof_id", "analysis_id", "status"):
        if not isinstance(findings_doc.get(field), str) or not findings_doc[field]:
            errors.append(f"$.{field}: expected non-empty string")
    if findings_doc.get("status") != "analysis":
        errors.append("$.status: expected analysis")

    findings = findings_doc.get("findings")
    if not isinstance(findings, list) or not findings:
        errors.append("$.findings: expected non-empty array")
        return errors

    known_evidence_ids = evidence_ids(evidence_manifest)
    seen_ids: set[str] = set()
    for index, finding in enumerate(findings):
        validate_finding(finding, index, known_evidence_ids, seen_ids, errors)

    validate_summary(findings_doc.get("summary"), findings, errors)
    return errors


def validate_findings(findings_path: Path, evidence_manifest_path: Path) -> list[str]:
    try:
        findings_doc = load_json(findings_path)
        evidence_manifest = load_json(evidence_manifest_path)
    except (OSError, json.JSONDecodeError) as exc:
        return [str(exc)]
    return validate_findings_data(findings_doc, evidence_manifest)


def resolve_path(path_arg: str) -> Path:
    path = Path(path_arg)
    if not path.is_absolute():
        path = ROOT / path
    return path


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "usage: validate_evidence_backed_findings.py <findings.json> <evidence_manifest.json>",
            file=sys.stderr,
        )
        return 2

    errors = validate_findings(resolve_path(argv[1]), resolve_path(argv[2]))
    if errors:
        print("EVIDENCE_BACKED_FINDINGS_INVALID")
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("EVIDENCE_BACKED_FINDINGS_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
