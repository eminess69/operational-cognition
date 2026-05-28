#!/usr/bin/env python3
"""Validate Proof 013 real-trace replay gate artifacts."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROOF_ID = "013-real-trace-replay-gate"
PROBE_IDS = [f"P-{index:03d}" for index in range(1, 9)]
VALID_SCORES = {"reconstructed", "partially_reconstructed", "unresolved"}
VALID_CLAIM_LEVELS = {"observed", "inferred", "hypothesis", "unresolved"}
VALID_VERDICTS = {
    "REAL_TRACE_ADVANTAGE_OBSERVED",
    "PARTIAL_REAL_TRACE_ADVANTAGE",
    "NO_REAL_TRACE_ADVANTAGE",
    "INVALID_TRACE",
    "FAIL_CLOSED",
}

REQUIRED_FILES = [
    "README.md",
    "candidate_selection_report.md",
    "candidate_redaction_report.md",
    "candidate_conversion_report.md",
    "visible_only_replay_results.json",
    "full_lineage_replay_results.json",
    "comparative_reconstruction_report.md",
    "reconstruction_probe_results.json",
    "claim_register.json",
    "public_lineage_summary.md",
    "final_verdict.json",
    "proof_manifest.json",
    "fixture/transcript.jsonl",
    "fixture/events.jsonl",
    "fixture/tool_actions.jsonl",
    "fixture/tool_results_manifest.json",
    "fixture/memory_log.jsonl",
    "fixture/compressed_context_summary.json",
    "fixture/omitted_ranges.json",
    "fixture/contradiction_refs.json",
    "fixture/authority_refs.json",
    "fixture/temporal_validity.json",
    "fixture/environment_snapshot_manifest.json",
    "fixture/runtime_config.json",
    "fixture/recovery_trace.jsonl",
    "fixture/provenance_manifest.json",
    "fixture/public_lineage_summary.md",
]

SUMMARY_KEYS = ("reconstructed", "partially_reconstructed", "unresolved")
BANNED_SECRET_STRINGS = ("password", "api_key", "private_key")
POSITIVE_OVERCLAIM_PATTERNS = [
    re.compile(r"\bglobally superior\b", re.IGNORECASE),
    re.compile(r"\buniversal superiority\b", re.IGNORECASE),
    re.compile(r"\bglobal superiority claim\b.{0,30}\b(true|made|validated|proven|confirmed)\b", re.IGNORECASE),
    re.compile(r"\b(agi|consciousness)\b.{0,40}\b(validated|proven|demonstrated|achieved|confirmed)\b", re.IGNORECASE),
    re.compile(r"\b(validates|proves|demonstrates|confirms)\b.{0,40}\b(agi|consciousness)\b", re.IGNORECASE),
    re.compile(r"\bblack[-_ ]box[-_ ]solved\b.{0,30}\b(true|validated|proven|confirmed)\b", re.IGNORECASE),
    re.compile(r"\btarget[-_ ]system defect\b.{0,30}\b(true|validated|proven|confirmed|observed)\b", re.IGNORECASE),
]
NEGATION_MARKERS = ("no ", "not ", "false", "disallowed", "blocked", "without ")


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


def check_jsonl(path: Path, label: str, errors: list[str]) -> None:
    try:
        lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except OSError as exc:
        errors.append(f"{label}: cannot read: {exc}")
        return
    if not lines:
        errors.append(f"{label}: expected non-empty jsonl")
        return
    seen: set[str] = set()
    for index, line in enumerate(lines, start=1):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{label}:{index}: invalid JSON: {exc}")
            continue
        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id:
            errors.append(f"{label}:{index}.id: expected non-empty string")
        elif record_id in seen:
            errors.append(f"{label}:{index}.id: duplicate {record_id}")
        seen.add(record_id)


def expected_summary(results: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(result.get("score") for result in results if result.get("score") in VALID_SCORES)
    return {key: counts[key] for key in SUMMARY_KEYS}


def check_summary(doc: dict[str, Any], results: list[dict[str, Any]], label: str, errors: list[str]) -> None:
    summary = doc.get("summary")
    if not isinstance(summary, dict):
        errors.append(f"{label}.summary: expected object")
        return
    expected = expected_summary(results)
    for key, value in expected.items():
        if summary.get(key) != value:
            errors.append(f"{label}.summary.{key}: expected {value}, got {summary.get(key)}")


def check_replay_results(doc: Any, mode: str, errors: list[str]) -> list[dict[str, Any]]:
    if not isinstance(doc, dict):
        errors.append(f"{mode}: expected object")
        return []
    if doc.get("proof_id") != PROOF_ID:
        errors.append(f"{mode}.proof_id: expected {PROOF_ID}")
    if doc.get("mode") != mode:
        errors.append(f"{mode}.mode: expected {mode}")
    if doc.get("source_fixture") != "proofs/013-real-trace-replay-gate/fixture":
        errors.append(f"{mode}.source_fixture: expected proofs/013-real-trace-replay-gate/fixture")

    raw_results = doc.get("results")
    if not isinstance(raw_results, list):
        errors.append(f"{mode}.results: expected array")
        return []

    results = [item for item in raw_results if isinstance(item, dict)]
    if len(results) != len(raw_results):
        errors.append(f"{mode}.results: expected only objects")

    seen: set[str] = set()
    for index, result in enumerate(results):
        path = f"{mode}.results[{index}]"
        probe_id = result.get("probe_id")
        if probe_id in seen:
            errors.append(f"{path}.probe_id: duplicate {probe_id}")
        if probe_id not in PROBE_IDS:
            errors.append(f"{path}.probe_id: expected one of {PROBE_IDS}")
        else:
            seen.add(probe_id)
        if result.get("score") not in VALID_SCORES:
            errors.append(f"{path}.score: expected one of {sorted(VALID_SCORES)}")
        if result.get("claim_level") not in VALID_CLAIM_LEVELS:
            errors.append(f"{path}.claim_level: expected one of {sorted(VALID_CLAIM_LEVELS)}")
        if not isinstance(result.get("reason"), str) or not result["reason"]:
            errors.append(f"{path}.reason: expected non-empty string")
        refs_field = "available_refs" if mode == "visible_only" else "fixture_refs"
        if not isinstance(result.get(refs_field), list):
            errors.append(f"{path}.{refs_field}: expected array")

    for probe_id in PROBE_IDS:
        if probe_id not in seen:
            errors.append(f"{mode}: missing probe {probe_id}")
    check_summary(doc, results, mode, errors)
    return results


def check_probe_expectations(visible: list[dict[str, Any]], full: list[dict[str, Any]], errors: list[str]) -> None:
    weak_visible = sum(1 for result in visible if result.get("score") in {"partially_reconstructed", "unresolved"})
    if weak_visible < len(PROBE_IDS):
        errors.append("visible_only: expected every probe to remain partial or unresolved")
    for result in full:
        if result.get("score") != "reconstructed":
            errors.append(f"full_lineage: {result.get('probe_id')} must be reconstructed")


def check_runtime(runtime_config: Any, final_verdict: Any, manifest: Any, errors: list[str]) -> None:
    if not isinstance(runtime_config, dict):
        errors.append("fixture/runtime_config.json: expected object")
        return
    gate = runtime_config.get("inside_voice_gate")
    if not isinstance(gate, dict):
        errors.append("runtime_config.inside_voice_gate: expected object")
        return
    if gate.get("adapter_status") != "pond_backed":
        errors.append("runtime_config.inside_voice_gate.adapter_status: expected pond_backed")
    if gate.get("contribution_grade") != "strong":
        errors.append("runtime_config.inside_voice_gate.contribution_grade: expected strong")
    if not gate.get("runtime_response_hash"):
        errors.append("runtime_config.inside_voice_gate.runtime_response_hash: expected value")
    if not gate.get("corpus_hash"):
        errors.append("runtime_config.inside_voice_gate.corpus_hash: expected value")

    if isinstance(final_verdict, dict):
        if final_verdict.get("adapter_status") != "pond_backed":
            errors.append("final_verdict.adapter_status: expected pond_backed")
        if final_verdict.get("contribution_grade") != "strong":
            errors.append("final_verdict.contribution_grade: expected strong")
        if final_verdict.get("runtime_hash_stable") is not True:
            errors.append("final_verdict.runtime_hash_stable: expected true")
    if isinstance(manifest, dict) and manifest.get("inside_voice_adapter_status") != "pond_backed":
        errors.append("proof_manifest.inside_voice_adapter_status: expected pond_backed")


def check_provenance(provenance: Any, errors: list[str]) -> None:
    if not isinstance(provenance, dict):
        errors.append("fixture/provenance_manifest.json: expected object")
        return
    if provenance.get("provenance_status") != "established_for_redacted_local_trace":
        errors.append("provenance_manifest.provenance_status: expected established_for_redacted_local_trace")
    if provenance.get("redaction_complete") is not True:
        errors.append("provenance_manifest.redaction_complete: expected true")
    if provenance.get("visible_only_separable_from_full_lineage") is not True:
        errors.append("provenance_manifest.visible_only_separable_from_full_lineage: expected true")
    if not isinstance(provenance.get("source_refs"), list) or not provenance["source_refs"]:
        errors.append("provenance_manifest.source_refs: expected non-empty array")


def check_claim_register(register: Any, errors: list[str]) -> None:
    if not isinstance(register, dict):
        errors.append("claim_register.json: expected object")
        return
    claims = register.get("claims")
    if not isinstance(claims, list) or not claims:
        errors.append("claim_register.claims: expected non-empty array")
        return
    for index, claim in enumerate(claims):
        path = f"claim_register.claims[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{path}: expected object")
            continue
        if claim.get("classification") not in VALID_CLAIM_LEVELS:
            errors.append(f"{path}.classification: expected one of {sorted(VALID_CLAIM_LEVELS)}")
        if not isinstance(claim.get("evidence_refs"), list) or not claim["evidence_refs"]:
            errors.append(f"{path}.evidence_refs: expected non-empty array")
        for field in ("claim_id", "claim", "safe_public_wording", "risk_if_overstated"):
            if not isinstance(claim.get(field), str) or not claim[field]:
                errors.append(f"{path}.{field}: expected non-empty string")


def check_verdict(verdict: Any, errors: list[str]) -> None:
    if not isinstance(verdict, dict):
        errors.append("final_verdict.json: expected object")
        return
    if verdict.get("verdict") not in VALID_VERDICTS:
        errors.append("final_verdict.verdict: invalid verdict")
    if verdict.get("global_superiority_claim") is not False:
        errors.append("final_verdict.global_superiority_claim: expected false")
    for field in ("agi_claim", "consciousness_claim", "black_box_solved_claim", "target_system_defect_claim"):
        if verdict.get(field) is not False:
            errors.append(f"final_verdict.{field}: expected false")
    if verdict.get("next_required_validation") != "additional independent real-trace replay runs":
        errors.append("final_verdict.next_required_validation: expected additional independent real-trace replay runs")


def text_has_positive_overclaim(text: str) -> str | None:
    for pattern in POSITIVE_OVERCLAIM_PATTERNS:
        for match in pattern.finditer(text):
            prefix = text[max(0, match.start() - 120) : match.start()].lower()
            if any(marker in prefix for marker in NEGATION_MARKERS):
                continue
            return match.group(0)
    return None


def check_text_boundaries(proof_dir: Path, errors: list[str]) -> None:
    combined = ""
    for path in sorted(proof_dir.rglob("*")):
        if not path.is_file() or path.suffix not in {".md", ".json", ".jsonl"}:
            continue
        text = read_text(path, errors)
        lowered = text.lower()
        for banned in BANNED_SECRET_STRINGS:
            if banned in lowered:
                errors.append(f"{path.relative_to(proof_dir)}: banned secret marker detected: {banned}")
        combined += "\n" + text

    overclaim = text_has_positive_overclaim(combined)
    if overclaim:
        errors.append(f"positive overclaim detected: {overclaim}")

    comparative = read_text(proof_dir / "comparative_reconstruction_report.md", errors).lower()
    if "proof 010" not in comparative or "synthetic" not in comparative:
        errors.append("Proof 010 synthetic-only boundary not preserved")
    if "proof 011" not in comparative and "candidate" not in comparative:
        errors.append("Proof 011 candidate gate boundary not preserved")
    if "global superiority claim" not in comparative and "global superiority" not in combined.lower():
        errors.append("no global superiority boundary not recorded")


def validate_real_trace_replay_gate(proof_dir: Path | str) -> list[str]:
    proof_dir = Path(proof_dir)
    if not proof_dir.is_absolute():
        proof_dir = ROOT / proof_dir

    errors: list[str] = []
    check_required_files(proof_dir, errors)
    if errors:
        return errors

    for relative in ("fixture/transcript.jsonl", "fixture/events.jsonl", "fixture/tool_actions.jsonl", "fixture/memory_log.jsonl", "fixture/recovery_trace.jsonl"):
        check_jsonl(proof_dir / relative, relative, errors)

    visible_doc = load_json(proof_dir / "visible_only_replay_results.json", errors)
    full_doc = load_json(proof_dir / "full_lineage_replay_results.json", errors)
    probe_doc = load_json(proof_dir / "reconstruction_probe_results.json", errors)
    claim_register = load_json(proof_dir / "claim_register.json", errors)
    final_verdict = load_json(proof_dir / "final_verdict.json", errors)
    manifest = load_json(proof_dir / "proof_manifest.json", errors)
    runtime_config = load_json(proof_dir / "fixture/runtime_config.json", errors)
    provenance = load_json(proof_dir / "fixture/provenance_manifest.json", errors)

    visible_results = check_replay_results(visible_doc, "visible_only", errors)
    full_results = check_replay_results(full_doc, "full_lineage", errors)
    check_probe_expectations(visible_results, full_results, errors)

    if isinstance(probe_doc, dict):
        results = probe_doc.get("results")
        if not isinstance(results, list) or len(results) != len(PROBE_IDS):
            errors.append("reconstruction_probe_results.results: expected eight probe comparisons")
    else:
        errors.append("reconstruction_probe_results.json: expected object")

    check_runtime(runtime_config, final_verdict, manifest, errors)
    check_provenance(provenance, errors)
    check_claim_register(claim_register, errors)
    check_verdict(final_verdict, errors)
    check_text_boundaries(proof_dir, errors)

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_real_trace_replay_gate.py <proof_dir>", file=sys.stderr)
        return 2

    errors = validate_real_trace_replay_gate(Path(argv[1]))
    if errors:
        print("REAL_TRACE_REPLAY_GATE_INVALID")
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("REAL_TRACE_REPLAY_GATE_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
