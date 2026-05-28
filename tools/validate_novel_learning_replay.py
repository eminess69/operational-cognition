#!/usr/bin/env python3
"""Validate Proof 015 novel learning replay artifacts."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROOF_ID = "015-novel-learning-replay-test"

REQUIRED_FILES = [
    "README.md",
    "learning_task_selection.md",
    "initial_codex_solution.md",
    "inside_voice_learning_record.json",
    "repeat_replay_request.json",
    "repeat_replay_response.json",
    "repeat_solution.md",
    "comparative_learning_audit.md",
    "replay_reconstruction_results.json",
    "claim_register.json",
    "public_lineage_summary.md",
    "final_verdict.json",
    "proof_manifest.json",
]

REQUIRED_CONSULT_RESPONSES = [
    "hard_gate_response.json",
    "inside_voice_learning_consult_response.json",
    "repeat_replay_response.json",
]

VALID_RECONSTRUCTION_VALUES = {"reconstructed", "partially_reconstructed", "unresolved"}
VALID_VERDICTS = {
    "LEARNING_REPLAY_ADVANTAGE_OBSERVED",
    "PARTIAL_LEARNING_REPLAY_ADVANTAGE",
    "NO_LEARNING_REPLAY_ADVANTAGE",
    "INVALID_LEARNING_TEST",
    "FAIL_CLOSED",
}
REQUIRED_RECONSTRUCTION_QUESTIONS = {
    "learned_pattern_recalled",
    "source_refs_preserved",
    "applicability_conditions_preserved",
    "failure_modes_preserved",
    "boundary_rules_preserved",
    "repeat_solution_used_recalled_pattern",
    "repeat_solution_avoided_overclaiming",
    "replay_improved_actionability",
}
AUDIT_DIMENSIONS = {
    "task understanding",
    "solution completeness",
    "required lineage fields",
    "boundary handling",
    "contradiction handling",
    "replay testability",
    "hallucination prevention",
    "time/task compression",
    "repeatability",
}
VALID_AUDIT_CLASSIFICATIONS = {"improved", "unchanged", "degraded", "unresolved"}
HASH_RE = re.compile(r"^[a-f0-9]{64}$")

OVERCLAIM_PATTERNS = [
    re.compile(r"\bglobally superior\b", re.IGNORECASE),
    re.compile(r"\buniversal superiority\b", re.IGNORECASE),
    re.compile(r"\bglobal superiority\b.{0,50}\b(true|made|validated|proven|confirmed|observed)\b", re.IGNORECASE),
    re.compile(
        r"\b(proves|proven|validates|validated|demonstrates|demonstrated|confirms|confirmed|achieves|achieved)\b"
        r".{0,80}\b(agi|artificial general intelligence|consciousness|black[-_ ]box[-_ ]solved)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(agi|artificial general intelligence|consciousness|black[-_ ]box[-_ ]solved)\b"
        r".{0,80}\b(proves|proven|validates|validated|demonstrates|demonstrated|confirms|confirmed|achieves|achieved)\b",
        re.IGNORECASE,
    ),
]
NEGATION_MARKERS = ("no ", "not ", "false", "disallowed", "blocked", "without ", "does not ", "do not ")


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


def check_consult_response(response: Any, label: str, errors: list[str]) -> None:
    if not isinstance(response, dict):
        errors.append(f"{label}: expected object")
        return
    if response.get("adapter_status") != "pond_backed":
        errors.append(f"{label}.adapter_status: expected pond_backed")
    if response.get("contribution_grade") not in {"bounded", "strong"}:
        errors.append(f"{label}.contribution_grade: expected bounded or strong")
    if not response.get("runtime_stage_report_ref"):
        errors.append(f"{label}.runtime_stage_report_ref: expected value")
    if not isinstance(response.get("pressure_rankings"), list) or not response["pressure_rankings"]:
        errors.append(f"{label}.pressure_rankings: expected non-empty array")
    if response.get("gate_failures") != []:
        errors.append(f"{label}.gate_failures: expected []")

    lineage = response.get("lineage") if isinstance(response.get("lineage"), dict) else {}
    runtime = lineage.get("runtime") if isinstance(lineage.get("runtime"), dict) else {}
    for field in ("runtime_response_hash", "corpus_hash"):
        if not is_hash(runtime.get(field)):
            errors.append(f"{label}.lineage.runtime.{field}: expected sha256")


def canonical_learning_hash(record: dict[str, Any]) -> str:
    body = dict(record)
    body["content_hash"] = ""
    payload = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def check_learning_record(record: Any, errors: list[str]) -> None:
    if not isinstance(record, dict):
        errors.append("inside_voice_learning_record.json: expected object")
        return
    if record.get("learning_id") != "proof_015_learning_001":
        errors.append("inside_voice_learning_record.learning_id: expected proof_015_learning_001")
    if not isinstance(record.get("new_pattern"), str) or not record["new_pattern"]:
        errors.append("inside_voice_learning_record.new_pattern: expected non-empty string")
    if not isinstance(record.get("source_refs"), list) or not record["source_refs"]:
        errors.append("inside_voice_learning_record.source_refs: expected non-empty array")
    for field in (
        "applicability_conditions",
        "failure_modes",
        "required_lineage_fields",
        "contradiction_or_boundary_rules",
        "minimal_replay_test",
    ):
        if not isinstance(record.get(field), list) or not record[field]:
            errors.append(f"inside_voice_learning_record.{field}: expected non-empty array")
    if not is_hash(record.get("content_hash")):
        errors.append("inside_voice_learning_record.content_hash: expected sha256")
    elif canonical_learning_hash(record) != record.get("content_hash"):
        errors.append("inside_voice_learning_record.content_hash: mismatch")


def check_repeat_request(request: Any, original_solution: str, errors: list[str]) -> None:
    if not isinstance(request, dict):
        errors.append("repeat_replay_request.json: expected object")
        return
    request_text = json.dumps(request, sort_keys=True)
    decoded_strings = list(iter_strings(request))
    original_hash = hashlib.sha256(original_solution.encode("utf-8")).hexdigest()
    if original_hash not in request_text:
        errors.append("repeat_replay_request: missing forbidden_original_solution_hash")
    if original_solution and any(original_solution in value for value in decoded_strings):
        errors.append("repeat_replay_request: includes full original solution text")

    long_paragraphs = [part.strip() for part in original_solution.split("\n\n") if len(part.strip()) >= 240]
    for paragraph in long_paragraphs:
        if any(paragraph in value for value in decoded_strings):
            errors.append("repeat_replay_request: includes copied original solution section")
            break


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


def check_reconstruction(results_doc: Any, errors: list[str]) -> dict[str, str]:
    answers: dict[str, str] = {}
    if not isinstance(results_doc, dict):
        errors.append("replay_reconstruction_results.json: expected object")
        return answers
    results = results_doc.get("results")
    if not isinstance(results, list):
        errors.append("replay_reconstruction_results.results: expected array")
        return answers
    for index, result in enumerate(results):
        path = f"replay_reconstruction_results.results[{index}]"
        if not isinstance(result, dict):
            errors.append(f"{path}: expected object")
            continue
        question = result.get("question")
        answer = result.get("answer")
        if question in answers:
            errors.append(f"{path}.question: duplicate {question}")
        if not isinstance(question, str) or not question:
            errors.append(f"{path}.question: expected non-empty string")
        elif question not in REQUIRED_RECONSTRUCTION_QUESTIONS:
            errors.append(f"{path}.question: unexpected {question}")
        if answer not in VALID_RECONSTRUCTION_VALUES:
            errors.append(f"{path}.answer: expected one of {sorted(VALID_RECONSTRUCTION_VALUES)}")
        else:
            answers[question] = answer
        if not isinstance(result.get("evidence_refs"), list) or not result["evidence_refs"]:
            errors.append(f"{path}.evidence_refs: expected non-empty array")

    missing = REQUIRED_RECONSTRUCTION_QUESTIONS - set(answers)
    if missing:
        errors.append(f"replay_reconstruction_results.results: missing {sorted(missing)}")

    summary = results_doc.get("summary")
    if isinstance(summary, dict):
        expected_counts = {value: list(answers.values()).count(value) for value in VALID_RECONSTRUCTION_VALUES}
        for key, expected in expected_counts.items():
            if summary.get(key) != expected:
                errors.append(f"replay_reconstruction_results.summary.{key}: expected {expected}")
    else:
        errors.append("replay_reconstruction_results.summary: expected object")
    return answers


def parse_audit_classifications(text: str, errors: list[str]) -> dict[str, str]:
    classifications: dict[str, str] = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        dimension = cells[0].lower()
        classification = cells[1].lower()
        if dimension in {"dimension", "---"}:
            continue
        if dimension in AUDIT_DIMENSIONS:
            if classification not in VALID_AUDIT_CLASSIFICATIONS:
                errors.append(f"comparative_learning_audit.{dimension}: invalid classification {classification}")
            else:
                classifications[dimension] = classification
    missing = AUDIT_DIMENSIONS - set(classifications)
    if missing:
        errors.append(f"comparative_learning_audit: missing dimensions {sorted(missing)}")
    return classifications


def positive_overclaim(text: str) -> str | None:
    for pattern in OVERCLAIM_PATTERNS:
        for match in pattern.finditer(text):
            window_start = max(0, match.start() - 120)
            prefix_window = text[window_start : match.start()]
            sentence_start = max(prefix_window.rfind("."), prefix_window.rfind("\n"), prefix_window.rfind(";"))
            prefix = prefix_window[sentence_start + 1 :].lower()
            if any(marker in prefix for marker in NEGATION_MARKERS):
                continue
            return match.group(0)
    return None


def check_text_boundaries(proof_dir: Path, errors: list[str]) -> None:
    combined = ""
    for path in sorted(proof_dir.rglob("*")):
        if path.is_file() and path.suffix in {".md", ".json", ".jsonl"}:
            combined += "\n" + read_text(path, errors)
    overclaim = positive_overclaim(combined)
    if overclaim:
        errors.append(f"positive overclaim detected: {overclaim}")


def expected_verdict(answers: dict[str, str], audit: dict[str, str], overclaim_present: bool) -> str:
    if overclaim_present:
        return "INVALID_LEARNING_TEST"
    pattern_recalled = answers.get("learned_pattern_recalled") == "reconstructed"
    source_refs = answers.get("source_refs_preserved") == "reconstructed"
    used_pattern = answers.get("repeat_solution_used_recalled_pattern") == "reconstructed"
    if not pattern_recalled or not used_pattern:
        return "NO_LEARNING_REPLAY_ADVANTAGE"
    strong_count = sum(1 for value in audit.values() if value in {"improved", "unchanged"})
    if pattern_recalled and source_refs and used_pattern and strong_count >= 5:
        return "LEARNING_REPLAY_ADVANTAGE_OBSERVED"
    return "PARTIAL_LEARNING_REPLAY_ADVANTAGE"


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


def validate_novel_learning_replay(proof_dir: Path | str) -> list[str]:
    proof_dir = Path(proof_dir)
    if not proof_dir.is_absolute():
        proof_dir = ROOT / proof_dir

    errors: list[str] = []
    check_required_files(proof_dir, errors)
    if errors:
        return errors

    for relative in REQUIRED_CONSULT_RESPONSES:
        response_path = proof_dir / relative
        if not response_path.is_file():
            errors.append(f"missing Inside Voice response artifact: {relative}")
            continue
        check_consult_response(load_json(response_path, errors), relative, errors)

    learning_record = load_json(proof_dir / "inside_voice_learning_record.json", errors)
    repeat_request = load_json(proof_dir / "repeat_replay_request.json", errors)
    repeat_response = load_json(proof_dir / "repeat_replay_response.json", errors)
    reconstruction = load_json(proof_dir / "replay_reconstruction_results.json", errors)
    final_verdict = load_json(proof_dir / "final_verdict.json", errors)
    manifest = load_json(proof_dir / "proof_manifest.json", errors)

    original_solution = read_text(proof_dir / "initial_codex_solution.md", errors)
    audit_text = read_text(proof_dir / "comparative_learning_audit.md", errors)

    check_learning_record(learning_record, errors)
    check_repeat_request(repeat_request, original_solution, errors)
    answers = check_reconstruction(reconstruction, errors)
    audit = parse_audit_classifications(audit_text, errors)
    overclaim = positive_overclaim("\n".join(read_text(path, errors) for path in proof_dir.rglob("*") if path.is_file() and path.suffix in {".md", ".json", ".jsonl"}))
    check_text_boundaries(proof_dir, errors)

    if isinstance(repeat_response, dict):
        lineage_refs = repeat_response.get("lineage_refs")
        if not isinstance(lineage_refs, list) or not any("inside_voice_learning_record.json" in str(ref) for ref in lineage_refs):
            errors.append("repeat_replay_response.lineage_refs: missing learning record ref")

    check_final_verdict(final_verdict, expected_verdict(answers, audit, overclaim is not None), errors)

    if isinstance(manifest, dict):
        if manifest.get("proof_id") != PROOF_ID:
            errors.append(f"proof_manifest.proof_id: expected {PROOF_ID}")
        if manifest.get("inside_voice_adapter_status") != "pond_backed":
            errors.append("proof_manifest.inside_voice_adapter_status: expected pond_backed")
        required = manifest.get("required_artifacts")
        if isinstance(required, list):
            missing_manifest_entries = set(REQUIRED_FILES) - set(required)
            if missing_manifest_entries:
                errors.append(f"proof_manifest.required_artifacts: missing {sorted(missing_manifest_entries)}")
        else:
            errors.append("proof_manifest.required_artifacts: expected array")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_novel_learning_replay.py <proof_dir>", file=sys.stderr)
        return 2

    errors = validate_novel_learning_replay(Path(argv[1]))
    if errors:
        print("NOVEL_LEARNING_REPLAY_INVALID")
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("NOVEL_LEARNING_REPLAY_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
