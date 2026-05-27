#!/usr/bin/env python3
"""Validate Proof 012 pond-backed one-shot artifacts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "one_shot_plan.md",
    "inside_voice_usage_report.json",
    "pond_backed_runtime_lineage.json",
    "survivable_lineage_validation_package.md",
    "claim_register.json",
    "comparative_baseline_report.md",
    "final_audit_verdict.json",
    "proof_manifest.json",
]

VALID_VERDICTS = {
    "POND_BACKED_ONE_SHOT_VALID",
    "POND_BACKED_ONE_SHOT_PARTIAL",
    "POND_BACKED_ONE_SHOT_FAILED",
}

REQUIRED_CLAIM_IDS = {
    "PB-001",
    "PB-002",
    "PB-003",
    "PB-004",
    "PB-005",
    "PB-006",
    "PB-007",
    "PB-008",
    "PB-009",
}

POSITIVE_OVERCLAIM_PATTERNS = [
    re.compile(r"\bagi\b.{0,40}\b(validated|proven|demonstrated|achieved|confirmed)\b"),
    re.compile(r"\b(validates|proves|demonstrates|confirms)\b.{0,40}\bagi\b"),
    re.compile(r"\bconsciousness\b.{0,40}\b(validated|proven|demonstrated|achieved|confirmed)\b"),
    re.compile(r"\b(validates|proves|demonstrates|confirms)\b.{0,40}\bconsciousness\b"),
    re.compile(r"\bblack[-_ ]box[-_ ]solved\b.{0,20}\b(true|validated|proven|confirmed)\b"),
    re.compile(r"\b(solves|solved|proves)\b.{0,40}\bblack[-_ ]box\b"),
    re.compile(r"\bglobally superior\b"),
    re.compile(r"\buniversal superiority\b"),
    re.compile(r"\b(always|universally)\b.{0,30}\bsuperior\b"),
    re.compile(r"\bglobal superiority claim\b.{0,20}\b(true|made|validated|proven|confirmed)\b"),
]

NEGATION_MARKERS = (
    "no ",
    "not ",
    "does not ",
    "do not ",
    "without ",
    "disallowed",
    "blocked",
    "false",
)


def load_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        errors.append(f"{path.name}: cannot read: {exc}")
    except json.JSONDecodeError as exc:
        errors.append(f"{path.name}: invalid json: {exc}")
    return {}


def text_has_positive_overclaim(text: str) -> str | None:
    lowered = text.lower()
    for pattern in POSITIVE_OVERCLAIM_PATTERNS:
        for match in pattern.finditer(lowered):
            prefix = lowered[max(0, match.start() - 160) : match.start()]
            if any(marker in prefix for marker in NEGATION_MARKERS):
                continue
            return match.group(0)
    return None


def non_empty_list(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 0


def validate_claim_register(claim_register: dict[str, Any], errors: list[str]) -> None:
    claims = claim_register.get("claims")
    if not isinstance(claims, list):
        errors.append("claim_register.json.claims: expected non-empty list")
        return

    claim_ids = {claim.get("claim_id") for claim in claims if isinstance(claim, dict)}
    missing = sorted(REQUIRED_CLAIM_IDS - claim_ids)
    if missing:
        errors.append(f"claim_register.json.claims: missing required claims {', '.join(missing)}")

    for claim in claims:
        if not isinstance(claim, dict):
            errors.append("claim_register.json.claims: each claim must be an object")
            continue
        claim_id = claim.get("claim_id", "<missing>")
        for field in ("claim_level", "safe_public_wording", "risk_if_overstated"):
            if not isinstance(claim.get(field), str) or not claim[field].strip():
                errors.append(f"claim_register.json.{claim_id}.{field}: expected non-empty string")
        if not non_empty_list(claim.get("evidence_refs")):
            errors.append(f"claim_register.json.{claim_id}.evidence_refs: expected non-empty list")


def validate_boundaries(usage: dict[str, Any], runtime: dict[str, Any], package_text: str, errors: list[str]) -> None:
    boundaries = usage.get("boundary_preservation", {})
    proof_010 = str(boundaries.get("proof_010", "")).lower()
    proof_011 = str(boundaries.get("proof_011", "")).lower()

    runtime_boundaries = runtime.get("operational_boundaries", [])
    boundary_ids = {
        boundary.get("id")
        for boundary in runtime_boundaries
        if isinstance(boundary, dict)
    }

    package_lower = package_text.lower()

    if (
        "proof 010" not in proof_010
        or "synthetic" not in proof_010
        or "only" not in proof_010
        or "boundary.proof_010.synthetic_fixture_only" not in boundary_ids
        or "why proof 010 is synthetic-only" not in package_lower
    ):
        errors.append("Proof 010 boundary not preserved as synthetic-only")

    if (
        "proof 011" not in proof_011
        or "real-trace" not in proof_011
        or "gate" not in proof_011
        or "boundary.proof_011.real_trace_gate" not in boundary_ids
        or "why proof 011 is the real-trace gate" not in package_lower
    ):
        errors.append("Proof 011 boundary not preserved as real-trace gate")


def validate_proof(proof_dir: Path | str) -> list[str]:
    proof_dir = Path(proof_dir)
    if not proof_dir.is_absolute():
        proof_dir = ROOT / proof_dir

    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (proof_dir / relative).is_file():
            errors.append(f"missing required file: {relative}")

    if errors:
        return errors

    usage = load_json(proof_dir / "inside_voice_usage_report.json", errors)
    runtime = load_json(proof_dir / "pond_backed_runtime_lineage.json", errors)
    claim_register = load_json(proof_dir / "claim_register.json", errors)
    final_verdict = load_json(proof_dir / "final_audit_verdict.json", errors)
    manifest = load_json(proof_dir / "proof_manifest.json", errors)

    if errors:
        return errors

    if usage.get("consultation", {}).get("adapter_status") != "pond_backed":
        errors.append("inside_voice_usage_report.json.consultation.adapter_status: expected pond_backed")
    if runtime.get("adapter_status") != "pond_backed":
        errors.append("pond_backed_runtime_lineage.json.adapter_status: expected pond_backed")
    if manifest.get("inside_voice_adapter_status") != "pond_backed":
        errors.append("proof_manifest.json.inside_voice_adapter_status: expected pond_backed")

    if not non_empty_list(usage.get("recalled_motifs")):
        errors.append("inside_voice_usage_report.json.recalled_motifs: expected non-empty list")
    if not non_empty_list(usage.get("retrieved_artifact_refs")):
        errors.append("inside_voice_usage_report.json.retrieved_artifact_refs: expected non-empty list")
    if not non_empty_list(usage.get("lineage_refs")):
        errors.append("inside_voice_usage_report.json.lineage_refs: expected non-empty list")
    if not non_empty_list(usage.get("unresolved_tensions")):
        errors.append("inside_voice_usage_report.json.unresolved_tensions: expected non-empty list")
    if not non_empty_list(usage.get("claim_pressure")):
        errors.append("inside_voice_usage_report.json.claim_pressure: expected non-empty list")

    runtime_hashes = usage.get("runtime_hashes", {})
    if not runtime_hashes.get("response_hash"):
        errors.append("inside_voice_usage_report.json.runtime_hashes.response_hash: expected value")
    if not runtime_hashes.get("runtime_response_hash"):
        errors.append("inside_voice_usage_report.json.runtime_hashes.runtime_response_hash: expected value")
    if not runtime.get("runtime_evidence_artifact_path"):
        errors.append("pond_backed_runtime_lineage.json.runtime_evidence_artifact_path: expected value")

    artifact_path = runtime.get("runtime_evidence_artifact_path")
    if isinstance(artifact_path, str) and not (ROOT / artifact_path).is_file():
        errors.append(f"runtime evidence artifact missing: {artifact_path}")

    package_text = (proof_dir / "survivable_lineage_validation_package.md").read_text(encoding="utf-8")
    validate_boundaries(usage, runtime, package_text, errors)

    if final_verdict.get("verdict") not in VALID_VERDICTS:
        errors.append("final_audit_verdict.json.verdict: invalid verdict")
    if final_verdict.get("adapter_status") != "pond_backed":
        errors.append("final_audit_verdict.json.adapter_status: expected pond_backed")
    if final_verdict.get("runtime_hash_stable") is not True:
        errors.append("final_audit_verdict.json.runtime_hash_stable: expected true")
    if final_verdict.get("inside_voice_contribution_observed") is not True:
        errors.append("final_audit_verdict.json.inside_voice_contribution_observed: expected true")
    if final_verdict.get("global_superiority_claim") is not False:
        errors.append("final_audit_verdict.json.global_superiority_claim: expected false")
    if final_verdict.get("next_required_validation") != "execute real-trace replay gate":
        errors.append("final_audit_verdict.json.next_required_validation: expected execute real-trace replay gate")

    validate_claim_register(claim_register, errors)

    combined = []
    for path in proof_dir.iterdir():
        if path.suffix in {".md", ".json"}:
            combined.append(path.read_text(encoding="utf-8"))
    positive_overclaim = text_has_positive_overclaim("\n".join(combined))
    if positive_overclaim:
        errors.append(f"positive overclaim detected: {positive_overclaim}")

    comparative = (proof_dir / "comparative_baseline_report.md").read_text(encoding="utf-8")
    if "pond_backed_advantage_observed" not in comparative:
        errors.append("comparative_baseline_report.md: missing allowed bounded verdict")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_pond_backed_one_shot.py <proof_dir>", file=sys.stderr)
        return 2

    errors = validate_proof(argv[1])
    if errors:
        print("POND_BACKED_ONE_SHOT_INVALID")
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("POND_BACKED_ONE_SHOT_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
