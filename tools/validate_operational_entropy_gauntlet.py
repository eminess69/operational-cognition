#!/usr/bin/env python3
"""Validate Proof 016 operational entropy gauntlet artifacts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROOF_ID = "016-operational-entropy-gauntlet"

REQUIRED_FILES = [
    "README.md",
    "entropy_scenario_design.md",
    "baseline_visible_only_results.md",
    "pond_backed_results.md",
    "entropy_event_log.jsonl",
    "contradiction_injection_report.md",
    "compression_loss_report.md",
    "recovery_reconstruction_report.md",
    "replay_integrity_report.md",
    "comparative_operational_integrity_report.md",
    "claim_register.json",
    "public_lineage_summary.md",
    "final_verdict.json",
    "proof_manifest.json",
]

REQUIRED_CONSULT_RESPONSES = [
    "hard_gate_response.json",
    "contradiction_arbitration_response.json",
    "stale_assumption_detection_response.json",
    "omitted_range_reconstruction_response.json",
    "recovery_decision_response.json",
    "replay_adequacy_response.json",
    "final_claim_boundary_audit_response.json",
]

REQUIRED_ENTROPY_IDS = {f"E-{index:03d}" for index in range(1, 9)}
REQUIRED_DIMENSIONS = {
    "contradiction preservation",
    "stale assumption handling",
    "authority reconstruction",
    "omitted-range recovery",
    "recovery-loop reconstruction",
    "temporal validity reconstruction",
    "replay adequacy",
    "operational continuity",
    "hallucination prevention",
    "reconstruction drift",
}
VALID_CLASSIFICATIONS = {"improved", "unchanged", "degraded", "unresolved"}
VALID_VERDICTS = {
    "ENTROPY_ADVANTAGE_OBSERVED",
    "PARTIAL_ENTROPY_ADVANTAGE",
    "NO_ENTROPY_ADVANTAGE",
    "INVALID_GAUNTLET",
    "FAIL_CLOSED",
}
COUNT_KEYS = {
    "baseline_reconstructed",
    "baseline_partial",
    "baseline_unresolved",
    "pond_reconstructed",
    "pond_partial",
    "pond_unresolved",
}
HASH_RE = re.compile(r"^[a-f0-9]{64}$")
OVERCLAIM_PATTERNS = [
    re.compile(r"\bglobally superior\b", re.IGNORECASE),
    re.compile(r"\buniversal superiority\b", re.IGNORECASE),
    re.compile(
        r"\bglobal superiority\b.{0,60}\b(true|made|validated|proven|confirmed|observed|demonstrated)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(validates|validated|proves|proven|demonstrates|demonstrated|confirms|confirmed|achieves|achieved)\b"
        r".{0,80}\b(agi|artificial general intelligence|consciousness|universal cognition|autonomous intelligence|black[-_ ]box[-_ ]solving)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(agi|artificial general intelligence|consciousness|universal cognition|autonomous intelligence|black[-_ ]box[-_ ]solving)\b"
        r".{0,80}\b(validates|validated|proves|proven|demonstrates|demonstrated|confirms|confirmed|achieves|achieved)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(validates|validated|proves|proven|demonstrates|demonstrated|confirms|confirmed|observes|observed)\b"
        r".{0,80}\btarget[-_ ]system defect\b",
        re.IGNORECASE,
    ),
]
NEGATION_MARKERS = (
    "no ",
    "not ",
    "does not ",
    "do not ",
    "without ",
    "disallowed",
    "blocked",
    "avoid",
    "forbidden",
)


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


def is_hash(value: Any) -> bool:
    return isinstance(value, str) and bool(HASH_RE.fullmatch(value))


def check_required_files(proof_dir: Path, errors: list[str]) -> None:
    for relative in REQUIRED_FILES:
        if not (proof_dir / relative).is_file():
            errors.append(f"missing required artifact: {relative}")
    if (proof_dir / "FAIL_CLOSED.md").exists():
        errors.append("FAIL_CLOSED.md present after passing gate")


def check_entropy_log(proof_dir: Path, errors: list[str]) -> None:
    path = proof_dir / "entropy_event_log.jsonl"
    text = read_text(path, errors)
    seen: set[str] = set()
    for index, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"entropy_event_log.jsonl:{index}: invalid JSON: {exc}")
            continue
        event_id = record.get("id")
        if event_id in seen:
            errors.append(f"entropy_event_log.jsonl:{index}.id: duplicate {event_id}")
        if event_id:
            seen.add(str(event_id))
        for field in ("name", "visible_only_effect", "full_lineage_effect", "expected_handling"):
            if not isinstance(record.get(field), str) or not record[field]:
                errors.append(f"entropy_event_log.jsonl:{index}.{field}: expected non-empty string")
    missing = REQUIRED_ENTROPY_IDS - seen
    if missing:
        errors.append(f"entropy_event_log.jsonl: missing entropy injections {sorted(missing)}")


def check_consult_response(doc: Any, label: str, errors: list[str]) -> None:
    if not isinstance(doc, dict):
        errors.append(f"{label}: expected object")
        return
    if doc.get("adapter_status") != "pond_backed":
        errors.append(f"{label}.adapter_status: expected pond_backed")
    if doc.get("contribution_grade") not in {"bounded", "strong"}:
        errors.append(f"{label}.contribution_grade: expected bounded or strong")
    if not doc.get("runtime_stage_report_ref"):
        errors.append(f"{label}.runtime_stage_report_ref: expected value")
    if not isinstance(doc.get("pressure_rankings"), list) or not doc["pressure_rankings"]:
        errors.append(f"{label}.pressure_rankings: expected non-empty array")
    if doc.get("gate_failures") != []:
        errors.append(f"{label}.gate_failures: expected []")
    rendered = json.dumps(doc, sort_keys=True)
    if "BROAD_UNSUPPORTED_CLAIM_BLOCKED" in rendered:
        errors.append(f"{label}: contains BROAD_UNSUPPORTED_CLAIM_BLOCKED")

    audits = doc.get("claim_boundary_audit")
    if not isinstance(audits, list):
        errors.append(f"{label}.claim_boundary_audit: expected array")
    elif not any(isinstance(item, dict) and item.get("id") == "audit.safe_negated_claim_boundary" for item in audits):
        errors.append(f"{label}.claim_boundary_audit: missing audit.safe_negated_claim_boundary")

    for field in ("recalled_motifs", "unresolved_tensions", "retrieved_artifact_refs"):
        if not isinstance(doc.get(field), list) or not doc[field]:
            errors.append(f"{label}.{field}: expected non-empty array")

    runtime = doc.get("lineage", {}).get("runtime", {}) if isinstance(doc.get("lineage"), dict) else {}
    for field in ("runtime_response_hash", "corpus_hash"):
        if not is_hash(runtime.get(field)):
            errors.append(f"{label}.lineage.runtime.{field}: expected sha256")


def check_consults(proof_dir: Path, errors: list[str]) -> None:
    consult_dir = proof_dir / "inside_voice_consults"
    if not consult_dir.is_dir():
        errors.append("missing consult evidence directory: inside_voice_consults")
        return
    for relative in REQUIRED_CONSULT_RESPONSES:
        path = consult_dir / relative
        if not path.is_file():
            errors.append(f"missing Inside Voice response artifact: inside_voice_consults/{relative}")
            continue
        check_consult_response(load_json(path, errors), relative, errors)


def check_replay_separation(proof_dir: Path, errors: list[str]) -> None:
    baseline = read_text(proof_dir / "baseline_visible_only_results.md", errors)
    pond = read_text(proof_dir / "pond_backed_results.md", errors)

    required_baseline_markers = [
        "mode: visible_only",
        "lineage_refs_used: false",
        "runtime_hashes_used: false",
        "contradiction_refs_used: false",
        "authority_refs_used: false",
        "omitted_range_refs_used: false",
        "recovery_refs_used: false",
        "pressure_rankings_used: false",
        "inside_voice_guidance_used: false",
    ]
    for marker in required_baseline_markers:
        if marker not in baseline:
            errors.append(f"baseline replay separation missing marker: {marker}")
    forbidden_baseline_markers = [
        "lineage_refs_used: true",
        "runtime_hashes_used: true",
        "inside_voice_guidance_used: true",
        "inside_voice_consults/",
    ]
    for marker in forbidden_baseline_markers:
        if marker in baseline:
            errors.append(f"baseline replay separation failure: contains {marker}")

    required_pond_markers = [
        "mode: pond_backed_full_lineage",
        "lineage_refs_used: true",
        "runtime_hashes_used: true",
        "inside_voice_guidance_used: true",
        "inside_voice_consults/hard_gate_response.json",
        "inside_voice_consults/replay_adequacy_response.json",
    ]
    for marker in required_pond_markers:
        if marker not in pond:
            errors.append(f"pond replay separation missing marker: {marker}")


def parse_comparison_table(text: str, errors: list[str]) -> dict[str, str]:
    classifications: dict[str, str] = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip().lower() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        dimension, classification = cells[0], cells[1]
        if dimension in {"dimension", "---"}:
            continue
        if dimension in REQUIRED_DIMENSIONS:
            if classification not in VALID_CLASSIFICATIONS:
                errors.append(f"comparative report {dimension}: invalid classification {classification}")
            else:
                classifications[dimension] = classification
    missing = REQUIRED_DIMENSIONS - set(classifications)
    if missing:
        errors.append(f"comparative report: missing dimensions {sorted(missing)}")
    return classifications


def check_counts(final_doc: Any, errors: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    if not isinstance(final_doc, dict):
        errors.append("final_verdict.json: expected object")
        return counts
    raw_counts = final_doc.get("measurable_reconstruction_counts")
    if not isinstance(raw_counts, dict):
        errors.append("final_verdict.measurable_reconstruction_counts: expected object")
        return counts
    missing = COUNT_KEYS - set(raw_counts)
    extra = set(raw_counts) - COUNT_KEYS
    if missing:
        errors.append(f"final_verdict.measurable_reconstruction_counts: missing {sorted(missing)}")
    if extra:
        errors.append(f"final_verdict.measurable_reconstruction_counts: unexpected {sorted(extra)}")
    for key in COUNT_KEYS:
        value = raw_counts.get(key)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            errors.append(f"final_verdict.measurable_reconstruction_counts.{key}: expected non-negative integer")
        else:
            counts[key] = value
    if counts:
        baseline_total = counts["baseline_reconstructed"] + counts["baseline_partial"] + counts["baseline_unresolved"]
        pond_total = counts["pond_reconstructed"] + counts["pond_partial"] + counts["pond_unresolved"]
        if baseline_total != pond_total:
            errors.append("final_verdict.measurable_reconstruction_counts: baseline and pond totals differ")
    return counts


def expected_verdict(classifications: dict[str, str], counts: dict[str, int], overclaim: bool) -> str:
    if overclaim:
        return "INVALID_GAUNTLET"
    improved = sum(1 for value in classifications.values() if value == "improved")
    required = {
        "contradiction preservation",
        "replay adequacy",
        "recovery-loop reconstruction",
    }
    if improved >= 6 and required.issubset({key for key, value in classifications.items() if value == "improved"}):
        if counts and counts.get("pond_reconstructed", 0) > counts.get("baseline_reconstructed", 0):
            return "ENTROPY_ADVANTAGE_OBSERVED"
        return "PARTIAL_ENTROPY_ADVANTAGE"
    if improved:
        return "PARTIAL_ENTROPY_ADVANTAGE"
    return "NO_ENTROPY_ADVANTAGE"


def check_final_verdict(final_doc: Any, expected: str, errors: list[str]) -> None:
    if not isinstance(final_doc, dict):
        errors.append("final_verdict.json: expected object")
        return
    verdict = final_doc.get("verdict")
    if verdict not in VALID_VERDICTS:
        errors.append("final_verdict.verdict: invalid verdict")
    elif verdict != expected:
        errors.append(f"final_verdict.verdict: expected {expected}, got {verdict}")
    if final_doc.get("adapter_status") != "pond_backed":
        errors.append("final_verdict.adapter_status: expected pond_backed")
    flags = final_doc.get("overclaim_flags")
    if not isinstance(flags, dict):
        errors.append("final_verdict.overclaim_flags: expected object")
    else:
        for field, value in flags.items():
            if value is not False:
                errors.append(f"final_verdict.overclaim_flags.{field}: expected false")


def positive_overclaim(text: str) -> str | None:
    for pattern in OVERCLAIM_PATTERNS:
        for match in pattern.finditer(text):
            prefix_window = text[max(0, match.start() - 140) : match.start()].lower()
            sentence_start = max(prefix_window.rfind("."), prefix_window.rfind("\n"), prefix_window.rfind(";"))
            prefix = prefix_window[sentence_start + 1 :]
            if any(marker in prefix for marker in NEGATION_MARKERS):
                continue
            return match.group(0)
    return None


def check_text_boundaries(proof_dir: Path, errors: list[str]) -> bool:
    combined = ""
    for path in sorted(proof_dir.rglob("*")):
        if path.is_file() and path.suffix in {".md", ".json", ".jsonl"}:
            combined += "\n" + read_text(path, errors)
    overclaim = positive_overclaim(combined)
    if overclaim:
        errors.append(f"positive overclaim detected: {overclaim}")
        return True
    return False


def check_manifest(manifest: Any, errors: list[str]) -> None:
    if not isinstance(manifest, dict):
        errors.append("proof_manifest.json: expected object")
        return
    if manifest.get("proof_id") != PROOF_ID:
        errors.append(f"proof_manifest.proof_id: expected {PROOF_ID}")
    if manifest.get("inside_voice_adapter_status") != "pond_backed":
        errors.append("proof_manifest.inside_voice_adapter_status: expected pond_backed")
    required = manifest.get("required_artifacts")
    if not isinstance(required, list):
        errors.append("proof_manifest.required_artifacts: expected array")
        return
    missing = set(REQUIRED_FILES) - set(required)
    if missing:
        errors.append(f"proof_manifest.required_artifacts: missing {sorted(missing)}")
    for response in REQUIRED_CONSULT_RESPONSES:
        entry = f"inside_voice_consults/{response}"
        if entry not in required:
            errors.append(f"proof_manifest.required_artifacts: missing {entry}")


def validate_operational_entropy_gauntlet(proof_dir: Path | str) -> list[str]:
    proof_dir = Path(proof_dir)
    if not proof_dir.is_absolute():
        proof_dir = ROOT / proof_dir

    errors: list[str] = []
    check_required_files(proof_dir, errors)
    if errors:
        return errors

    final_doc = load_json(proof_dir / "final_verdict.json", errors)
    manifest = load_json(proof_dir / "proof_manifest.json", errors)
    comparison_text = read_text(proof_dir / "comparative_operational_integrity_report.md", errors)

    check_entropy_log(proof_dir, errors)
    check_consults(proof_dir, errors)
    check_replay_separation(proof_dir, errors)
    classifications = parse_comparison_table(comparison_text, errors)
    counts = check_counts(final_doc, errors)
    overclaim = check_text_boundaries(proof_dir, errors)
    check_final_verdict(final_doc, expected_verdict(classifications, counts, overclaim), errors)
    check_manifest(manifest, errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_operational_entropy_gauntlet.py <proof_dir>", file=sys.stderr)
        return 2

    errors = validate_operational_entropy_gauntlet(Path(argv[1]))
    if errors:
        print("OPERATIONAL_ENTROPY_GAUNTLET_INVALID")
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("OPERATIONAL_ENTROPY_GAUNTLET_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
