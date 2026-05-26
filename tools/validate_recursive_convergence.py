#!/usr/bin/env python3
"""Validate Proof 012 recursive convergence artifacts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "recursive_run_plan.md",
    "recursive_depth_log.jsonl",
    "convergence_state.json",
    "surviving_laws.md",
    "adversarial_downgrade_report.md",
    "contradiction_pressure_report.md",
    "evidence_sufficiency_report.md",
    "fixture_pressure_report.md",
    "final_convergence_verdict.json",
    "proof_manifest.json",
]

VALID_PASS_TYPES = {
    "synthesis",
    "adversarial",
    "contradiction",
    "evidence_sufficiency",
    "fixture_validation",
    "alternative_explanation",
    "final_convergence",
}
VALID_CLAIM_LEVELS = {"observed", "inferred", "hypothesis", "unresolved"}
VALID_VERDICTS = {
    "CONVERGENCE_SURVIVES_BOUNDED",
    "CONVERGENCE_DOWNGRADED",
    "CONVERGENCE_UNSUPPORTED",
}
REQUIRED_CLAIMS = {f"C-{index:03d}" for index in range(1, 9)}
RAW_MCP_MARKERS = [
    "Deterministic placeholder consultation accepted",
    "mcp.file_ref",
    "mcp.constraint",
    "mcp.rec.",
    "lineage_refs",
    "source_refs",
    "response_summary",
    "request_body_hash",
    "response_body_hash",
]
PRIVATE_MARKERS = [
    "hidden chain-of-thought",
    "private scoring",
    "substrate state",
    "Belief Ledger internals",
    "Inside Voice implementation details",
    "harmonic traceback implementation",
]
FORBIDDEN_PUBLIC_ASSERTIONS = [
    "Proof 010 validates survivable lineage globally",
    "Proof 010 proves survivable lineage globally",
    "Proof 010 validates global survivable lineage",
    "Survivable lineage is globally validated",
    "Survivable lineage is universally validated",
    "MCP output is target-system evidence",
    "MCP output validates target-system behavior",
]


def load_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return None


def read_text(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"{path}: cannot read: {exc}")
        return ""


def check_required_files(proof_dir: Path, errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        if not (proof_dir / relative).is_file():
            errors.append(f"missing required artifact: {relative}")


def public_texts(proof_dir: Path, errors: list[str]) -> dict[str, str]:
    texts: dict[str, str] = {}
    for relative in REQUIRED_FILES:
        path = proof_dir / relative
        if path.suffix in {".md", ".json", ".jsonl"} and path.is_file():
            texts[relative] = read_text(path, errors)
    return texts


def check_no_private_or_raw_markers(texts: dict[str, str], errors: list[str]) -> None:
    for relative, text in texts.items():
        for marker in RAW_MCP_MARKERS:
            if marker in text:
                errors.append(f"{relative}: raw MCP body marker appears: {marker}")
        for marker in PRIVATE_MARKERS:
            if marker in text:
                errors.append(f"{relative}: private marker appears: {marker}")
        for assertion in FORBIDDEN_PUBLIC_ASSERTIONS:
            if assertion in text:
                errors.append(f"{relative}: forbidden public assertion appears: {assertion}")


def ensure_non_empty_string(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value:
        errors.append(f"{path}: expected non-empty string")


def check_depth_log(proof_dir: Path, errors: list[str]) -> None:
    path = proof_dir / "recursive_depth_log.jsonl"
    lines = [line for line in read_text(path, errors).splitlines() if line.strip()]
    if len(lines) < 7:
        errors.append("recursive_depth_log.jsonl: expected at least 7 passes")
        return

    seen_passes: set[str] = set()
    for index, line in enumerate(lines, start=1):
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"recursive_depth_log.jsonl:{index}: invalid JSON: {exc}")
            continue

        if entry.get("depth") != index:
            errors.append(f"recursive_depth_log.jsonl:{index}: depth must be {index}")
        pass_type = entry.get("pass_type")
        if pass_type not in VALID_PASS_TYPES:
            errors.append(f"recursive_depth_log.jsonl:{index}.pass_type: invalid")
        else:
            seen_passes.add(pass_type)
        ensure_non_empty_string(
            entry.get("mcp_request_hash"),
            f"recursive_depth_log.jsonl:{index}.mcp_request_hash",
            errors,
        )
        ensure_non_empty_string(
            entry.get("mcp_response_hash"),
            f"recursive_depth_log.jsonl:{index}.mcp_response_hash",
            errors,
        )
        ensure_non_empty_string(
            entry.get("codex_reconciliation_summary"),
            f"recursive_depth_log.jsonl:{index}.codex_reconciliation_summary",
            errors,
        )
        if not isinstance(entry.get("claim_changes"), list):
            errors.append(f"recursive_depth_log.jsonl:{index}.claim_changes: expected array")
        else:
            for change_index, change in enumerate(entry["claim_changes"]):
                if not isinstance(change, dict):
                    errors.append(
                        f"recursive_depth_log.jsonl:{index}.claim_changes[{change_index}]: expected object"
                    )
                    continue
                ensure_non_empty_string(
                    change.get("claim_id"),
                    f"recursive_depth_log.jsonl:{index}.claim_changes[{change_index}].claim_id",
                    errors,
                )
                if change.get("before") not in VALID_CLAIM_LEVELS:
                    errors.append(
                        f"recursive_depth_log.jsonl:{index}.claim_changes[{change_index}].before: invalid"
                    )
                if change.get("after") not in VALID_CLAIM_LEVELS:
                    errors.append(
                        f"recursive_depth_log.jsonl:{index}.claim_changes[{change_index}].after: invalid"
                    )
                ensure_non_empty_string(
                    change.get("reason"),
                    f"recursive_depth_log.jsonl:{index}.claim_changes[{change_index}].reason",
                    errors,
                )
        if not isinstance(entry.get("new_unresolved_questions"), list):
            errors.append(f"recursive_depth_log.jsonl:{index}.new_unresolved_questions: expected array")
        if not isinstance(entry.get("stop_signal"), bool):
            errors.append(f"recursive_depth_log.jsonl:{index}.stop_signal: expected boolean")

    missing = VALID_PASS_TYPES - seen_passes
    for pass_type in sorted(missing):
        errors.append(f"recursive_depth_log.jsonl: missing required pass {pass_type}")


def check_convergence_state(proof_dir: Path, errors: list[str]) -> None:
    state = load_json(proof_dir / "convergence_state.json", errors)
    if not isinstance(state, dict):
        errors.append("convergence_state.json: expected object")
        return
    if state.get("adapter_status") != "placeholder":
        errors.append("convergence_state.json.adapter_status: expected placeholder")
    if state.get("passes_completed") != 7:
        errors.append("convergence_state.json.passes_completed: expected 7")

    claims = state.get("claims")
    if not isinstance(claims, list):
        errors.append("convergence_state.json.claims: expected array")
        return
    claim_ids = {claim.get("claim_id") for claim in claims if isinstance(claim, dict)}
    for claim_id in sorted(REQUIRED_CLAIMS - claim_ids):
        errors.append(f"convergence_state.json.claims: missing {claim_id}")

    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            errors.append(f"convergence_state.json.claims[{index}]: expected object")
            continue
        for field in (
            "claim_id",
            "claim",
            "initial_level",
            "final_level",
            "supporting_proofs",
            "strongest_evidence",
            "weakest_boundary",
            "survived_adversarial_review",
            "survived_alternative_explanation_review",
            "required_next_validation",
        ):
            if field not in claim:
                errors.append(f"convergence_state.json.claims[{index}]: missing {field}")
        if claim.get("initial_level") not in VALID_CLAIM_LEVELS:
            errors.append(f"convergence_state.json.claims[{index}].initial_level: invalid")
        if claim.get("final_level") not in VALID_CLAIM_LEVELS:
            errors.append(f"convergence_state.json.claims[{index}].final_level: invalid")
        if not isinstance(claim.get("supporting_proofs"), list) or not claim.get("supporting_proofs"):
            errors.append(f"convergence_state.json.claims[{index}].supporting_proofs: expected non-empty array")
        if not isinstance(claim.get("strongest_evidence"), list) or not claim.get("strongest_evidence"):
            errors.append(f"convergence_state.json.claims[{index}].strongest_evidence: expected non-empty array")
        if not isinstance(claim.get("survived_adversarial_review"), bool):
            errors.append(f"convergence_state.json.claims[{index}].survived_adversarial_review: expected boolean")
        if not isinstance(claim.get("survived_alternative_explanation_review"), bool):
            errors.append(
                f"convergence_state.json.claims[{index}].survived_alternative_explanation_review: expected boolean"
            )
        ensure_non_empty_string(
            claim.get("required_next_validation"),
            f"convergence_state.json.claims[{index}].required_next_validation",
            errors,
        )


def check_surviving_laws(proof_dir: Path, errors: list[str]) -> None:
    text = read_text(proof_dir / "surviving_laws.md", errors)
    sections = re.split(r"(?m)^## Law \d+:", text)
    law_sections = sections[1:]
    if not law_sections:
        errors.append("surviving_laws.md: expected at least one law")
        return
    for index, section in enumerate(law_sections, start=1):
        lowered = section.lower()
        for required in (
            "claim level:",
            "supporting proof refs:",
            "limitation:",
            "next validation needed:",
        ):
            if required not in lowered:
                errors.append(f"surviving_laws.md: Law {index} missing {required.rstrip(':')}")


def check_reports(proof_dir: Path, errors: list[str]) -> None:
    adversarial = read_text(proof_dir / "adversarial_downgrade_report.md", errors)
    for heading in (
        "Claims That Remain Inferred",
        "Claims That Remain Hypothesis-Level",
        "Claims That Remain Unresolved",
        "Claims That Cannot Be Made Publicly",
        "Reasons Not to Overclaim",
    ):
        if heading not in adversarial:
            errors.append(f"adversarial_downgrade_report.md: missing section {heading}")
    if "Proof 010 is synthetic fixture validation only." not in adversarial:
        errors.append("adversarial_downgrade_report.md: missing Proof 010 fixture warning")

    evidence = read_text(proof_dir / "evidence_sufficiency_report.md", errors)
    for marker in (
        "sufficient_for_fixture",
        "sufficient_for_corpus_inference",
        "insufficient_for_global_claim",
        "insufficient_for_target_system_claim",
    ):
        if marker not in evidence:
            errors.append(f"evidence_sufficiency_report.md: missing {marker}")

    fixture = read_text(proof_dir / "fixture_pressure_report.md", errors)
    if "Fixture Hardening Requirements" not in fixture:
        errors.append("fixture_pressure_report.md: missing fixture hardening requirements")


def check_final_verdict(proof_dir: Path, errors: list[str]) -> None:
    verdict = load_json(proof_dir / "final_convergence_verdict.json", errors)
    if not isinstance(verdict, dict):
        errors.append("final_convergence_verdict.json: expected object")
        return
    if verdict.get("verdict") not in VALID_VERDICTS:
        errors.append("final_convergence_verdict.json.verdict: invalid")
    if verdict.get("central_claim_level") not in VALID_CLAIM_LEVELS:
        errors.append("final_convergence_verdict.json.central_claim_level: invalid")
    if verdict.get("passes_completed") != 7:
        errors.append("final_convergence_verdict.json.passes_completed: expected 7")
    ensure_non_empty_string(verdict.get("strongest_safe_public_claim"), "final_convergence_verdict.json.strongest_safe_public_claim", errors)
    ensure_non_empty_string(verdict.get("next_required_validation"), "final_convergence_verdict.json.next_required_validation", errors)
    if verdict.get("fixture_scope") != "synthetic_fixture_only":
        errors.append("final_convergence_verdict.json.fixture_scope: expected synthetic_fixture_only")
    if verdict.get("mcp_adapter_status") != "placeholder":
        errors.append("final_convergence_verdict.json.mcp_adapter_status: expected placeholder")
    if "inferred corpus-level claim requiring redacted-real or public-trace validation" not in str(
        verdict.get("strongest_safe_public_claim", "")
    ):
        errors.append("final_convergence_verdict.json.strongest_safe_public_claim: missing bounded wording")


def check_manifest(proof_dir: Path, errors: list[str]) -> None:
    manifest = load_json(proof_dir / "proof_manifest.json", errors)
    if not isinstance(manifest, dict):
        errors.append("proof_manifest.json: expected object")
        return
    if manifest.get("inside_voice_adapter_status") != "placeholder":
        errors.append("proof_manifest.json.inside_voice_adapter_status: expected placeholder")
    required = manifest.get("required_artifacts")
    if not isinstance(required, list):
        errors.append("proof_manifest.json.required_artifacts: expected array")
        return
    for artifact in REQUIRED_FILES:
        if artifact not in required:
            errors.append(f"proof_manifest.json.required_artifacts: missing {artifact}")


def validate_recursive_convergence(proof_dir: Path) -> list[str]:
    if not proof_dir.is_absolute():
        proof_dir = ROOT / proof_dir

    errors: list[str] = []
    check_required_files(proof_dir, errors)
    if errors:
        return errors

    texts = public_texts(proof_dir, errors)
    check_no_private_or_raw_markers(texts, errors)
    check_depth_log(proof_dir, errors)
    check_convergence_state(proof_dir, errors)
    check_surviving_laws(proof_dir, errors)
    check_reports(proof_dir, errors)
    check_final_verdict(proof_dir, errors)
    check_manifest(proof_dir, errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_recursive_convergence.py <proof_dir>", file=sys.stderr)
        return 2

    errors = validate_recursive_convergence(Path(argv[1]))
    if errors:
        print("RECURSIVE_CONVERGENCE_INVALID")
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("RECURSIVE_CONVERGENCE_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
