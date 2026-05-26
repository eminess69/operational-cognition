#!/usr/bin/env python3
"""Validate Proof 010 fixture execution artifacts."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

PROOF_ID = "010-fixture-execution"
SOURCE_FIXTURE = "proofs/009-survivable-lineage-fixture"
PROBE_IDS = [f"P-{index:03d}" for index in range(1, 7)]
VALID_SCORES = {"reconstructed", "partially_reconstructed", "unresolved"}
VALID_CLAIM_LEVELS = {"observed", "inferred", "hypothesis", "unresolved"}
VALID_VERDICTS = {"FIXTURE_VALIDATED", "FIXTURE_PARTIAL", "FIXTURE_FAILED"}
SUMMARY_KEYS = ("reconstructed", "partially_reconstructed", "unresolved")

REQUIRED_FILES = [
    "README.md",
    "visible_replay_results.json",
    "full_lineage_replay_results.json",
    "comparative_reconstruction_report.md",
    "fixture_claim_register.json",
    "validation_verdict.json",
    "proof_manifest.json",
]


def load_json(path: Path, errors: list[str]) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return None


def ensure_string(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value:
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


def expected_summary(results: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(
        result.get("score")
        for result in results
        if isinstance(result, dict) and result.get("score") in VALID_SCORES
    )
    return {key: counts[key] for key in SUMMARY_KEYS}


def check_summary(summary: Any, results: list[dict[str, Any]], label: str, errors: list[str]) -> None:
    if not isinstance(summary, dict):
        errors.append(f"{label}.summary: expected object")
        return

    missing = set(SUMMARY_KEYS) - set(summary)
    unexpected = set(summary) - set(SUMMARY_KEYS)
    for field in sorted(missing):
        errors.append(f"{label}.summary: missing required field {field}")
    for field in sorted(unexpected):
        errors.append(f"{label}.summary: unexpected field {field}")
    if missing:
        return

    expected = expected_summary(results)
    for field, value in expected.items():
        if summary.get(field) != value:
            errors.append(f"{label}.summary.{field}: expected {value}, got {summary.get(field)}")


def check_probe_results(doc: Any, mode: str, errors: list[str]) -> list[dict[str, Any]]:
    label = mode
    if not isinstance(doc, dict):
        errors.append(f"{label}: expected object")
        return []

    if doc.get("proof_id") != PROOF_ID:
        errors.append(f"{label}.proof_id: expected {PROOF_ID}")
    if doc.get("mode") != mode:
        errors.append(f"{label}.mode: expected {mode}")
    if doc.get("source_fixture") != SOURCE_FIXTURE:
        errors.append(f"{label}.source_fixture: expected {SOURCE_FIXTURE}")

    raw_results = doc.get("results")
    if not isinstance(raw_results, list):
        errors.append(f"{label}.results: expected array")
        return []

    results = [item for item in raw_results if isinstance(item, dict)]
    if len(results) != len(raw_results):
        errors.append(f"{label}.results: expected only objects")

    seen: set[str] = set()
    for index, result in enumerate(results):
        path = f"{label}.results[{index}]"
        probe_id = result.get("probe_id")
        if not isinstance(probe_id, str) or not probe_id:
            errors.append(f"{path}.probe_id: expected non-empty string")
        elif probe_id in seen:
            errors.append(f"{label}: duplicate probe {probe_id}")
        else:
            seen.add(probe_id)

        score = result.get("score")
        if score not in VALID_SCORES:
            errors.append(f"{path}.score: expected one of {sorted(VALID_SCORES)}")

        claim_level = result.get("claim_level")
        if claim_level not in VALID_CLAIM_LEVELS:
            errors.append(f"{path}.claim_level: expected one of {sorted(VALID_CLAIM_LEVELS)}")

        ensure_string(result.get("reason"), f"{path}.reason", errors)

        if mode == "visible_only":
            ensure_string_list(
                result.get("available_refs"),
                f"{path}.available_refs",
                errors,
                allow_empty=True,
            )
            ensure_string_list(
                result.get("missing_refs"),
                f"{path}.missing_refs",
                errors,
                allow_empty=True,
            )
        else:
            ensure_string_list(
                result.get("fixture_refs"),
                f"{path}.fixture_refs",
                errors,
                allow_empty=False,
            )

    for probe_id in PROBE_IDS:
        if probe_id not in seen:
            errors.append(f"{label}: missing probe {probe_id}")
    for probe_id in sorted(seen - set(PROBE_IDS)):
        errors.append(f"{label}: unexpected probe {probe_id}")

    check_summary(doc.get("summary"), results, label, errors)
    return results


def check_mode_expectations(
    visible_results: list[dict[str, Any]],
    full_results: list[dict[str, Any]],
    errors: list[str],
) -> None:
    partial_or_unresolved = sum(
        1
        for result in visible_results
        if result.get("score") in {"partially_reconstructed", "unresolved"}
    )
    if partial_or_unresolved < 3:
        errors.append("visible_only: expected at least three partial/unresolved probes")

    for result in full_results:
        if result.get("score") != "reconstructed":
            errors.append(f"full_lineage: {result.get('probe_id')} must be reconstructed")


def check_claim_register(register: Any, errors: list[str]) -> None:
    if not isinstance(register, dict):
        errors.append("fixture_claim_register: expected object")
        return
    if register.get("proof_id") != PROOF_ID:
        errors.append(f"fixture_claim_register.proof_id: expected {PROOF_ID}")

    claims = register.get("claims")
    if not isinstance(claims, list):
        errors.append("fixture_claim_register.claims: expected array")
        return
    if len(claims) < len(PROBE_IDS) + 1:
        errors.append("fixture_claim_register.claims: expected six probe claims plus aggregate claim")

    seen_claim_ids: set[str] = set()
    probe_claim_refs: set[str] = set()
    has_aggregate_claim = False
    for index, claim in enumerate(claims):
        path = f"fixture_claim_register.claims[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{path}: expected object")
            continue

        for field in (
            "claim_id",
            "claim",
            "claim_level",
            "evidence_refs",
            "risk_if_overstated",
            "safe_public_wording",
        ):
            if field not in claim:
                errors.append(f"{path}: missing required field {field}")

        claim_id = claim.get("claim_id")
        if isinstance(claim_id, str) and claim_id:
            if claim_id in seen_claim_ids:
                errors.append(f"{path}.claim_id: duplicate claim ID {claim_id}")
            seen_claim_ids.add(claim_id)
            if "AGGREGATE" in claim_id.upper():
                has_aggregate_claim = True
        else:
            errors.append(f"{path}.claim_id: expected non-empty string")

        if claim.get("claim_level") not in VALID_CLAIM_LEVELS:
            errors.append(f"{path}.claim_level: expected one of {sorted(VALID_CLAIM_LEVELS)}")

        for field in ("claim", "risk_if_overstated", "safe_public_wording"):
            ensure_string(claim.get(field), f"{path}.{field}", errors)

        evidence_refs = claim.get("evidence_refs")
        ensure_string_list(evidence_refs, f"{path}.evidence_refs", errors, allow_empty=False)
        if isinstance(evidence_refs, list):
            probe_claim_refs.update(ref for ref in evidence_refs if ref in PROBE_IDS)
            if all(probe_id in evidence_refs for probe_id in PROBE_IDS):
                has_aggregate_claim = True

    for probe_id in PROBE_IDS:
        if probe_id not in probe_claim_refs:
            errors.append(f"fixture_claim_register: missing claim coverage for {probe_id}")
    if not has_aggregate_claim:
        errors.append("fixture_claim_register: missing aggregate claim")


def expected_verdict(visible_summary: dict[str, int], full_summary: dict[str, int]) -> str:
    full_reconstructed = full_summary.get("reconstructed") == len(PROBE_IDS)
    visible_weak = (
        visible_summary.get("partially_reconstructed", 0) + visible_summary.get("unresolved", 0)
    ) >= 3
    if full_reconstructed and visible_weak:
        return "FIXTURE_VALIDATED"
    if full_reconstructed or visible_weak:
        return "FIXTURE_PARTIAL"
    return "FIXTURE_FAILED"


def check_verdict(
    verdict_doc: Any,
    visible_results: list[dict[str, Any]],
    full_results: list[dict[str, Any]],
    errors: list[str],
) -> None:
    if not isinstance(verdict_doc, dict):
        errors.append("validation_verdict: expected object")
        return

    visible_summary = expected_summary(visible_results)
    full_summary = expected_summary(full_results)
    expected = expected_verdict(visible_summary, full_summary)

    if verdict_doc.get("proof_id") != PROOF_ID:
        errors.append(f"validation_verdict.proof_id: expected {PROOF_ID}")
    if verdict_doc.get("scope") != "fixture_level_only":
        errors.append("validation_verdict.scope: expected fixture_level_only")
    if verdict_doc.get("verdict") not in VALID_VERDICTS:
        errors.append(f"validation_verdict.verdict: expected one of {sorted(VALID_VERDICTS)}")
    elif verdict_doc.get("verdict") != expected:
        errors.append(f"validation_verdict.verdict: expected {expected}, got {verdict_doc.get('verdict')}")

    if verdict_doc.get("visible_only_summary") != visible_summary:
        errors.append("validation_verdict.visible_only_summary: does not match visible results")
    if verdict_doc.get("full_lineage_summary") != full_summary:
        errors.append("validation_verdict.full_lineage_summary: does not match full-lineage results")

    expected_improvement = expected == "FIXTURE_VALIDATED"
    if verdict_doc.get("aggregate_improvement") is not expected_improvement:
        errors.append(
            "validation_verdict.aggregate_improvement: expected "
            f"{expected_improvement}, got {verdict_doc.get('aggregate_improvement')}"
        )

    ensure_string_list(
        verdict_doc.get("limitations"),
        "validation_verdict.limitations",
        errors,
        allow_empty=False,
    )
    ensure_string(
        verdict_doc.get("next_required_validation"),
        "validation_verdict.next_required_validation",
        errors,
    )


def validate_fixture_execution(proof_dir: Path) -> list[str]:
    if not proof_dir.is_absolute():
        proof_dir = ROOT / proof_dir

    errors: list[str] = []
    check_required_files(proof_dir, errors)
    if errors:
        return errors

    visible_doc = load_json(proof_dir / "visible_replay_results.json", errors)
    full_doc = load_json(proof_dir / "full_lineage_replay_results.json", errors)
    claim_register = load_json(proof_dir / "fixture_claim_register.json", errors)
    verdict_doc = load_json(proof_dir / "validation_verdict.json", errors)
    if errors:
        return errors

    visible_results = check_probe_results(visible_doc, "visible_only", errors)
    full_results = check_probe_results(full_doc, "full_lineage", errors)
    check_mode_expectations(visible_results, full_results, errors)
    check_claim_register(claim_register, errors)
    check_verdict(verdict_doc, visible_results, full_results, errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_fixture_execution.py <proof_dir>", file=sys.stderr)
        return 2

    errors = validate_fixture_execution(Path(argv[1]))
    if errors:
        print("FIXTURE_EXECUTION_INVALID")
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("FIXTURE_EXECUTION_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
