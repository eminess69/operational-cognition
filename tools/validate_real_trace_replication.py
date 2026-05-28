#!/usr/bin/env python3
"""Validate Proof 014 independent real-trace replication artifacts."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROOF_ID = "014-independent-real-trace-replication"
PROBE_IDS = [f"P-{index:03d}" for index in range(1, 9)]
VALID_SCORES = {"reconstructed", "partially_reconstructed", "unresolved"}
VALID_CLAIM_LEVELS = {"observed", "inferred", "hypothesis", "unresolved", "bounded"}
TRACE_VERDICTS = {
    "TRACE_ADVANTAGE_OBSERVED",
    "TRACE_PARTIAL_ADVANTAGE",
    "TRACE_NO_ADVANTAGE",
    "TRACE_INVALID",
}
AGGREGATE_VERDICTS = {
    "REPLICATION_ADVANTAGE_OBSERVED",
    "PARTIAL_REPLICATION_ADVANTAGE",
    "NO_REPLICATION_ADVANTAGE",
    "INVALID_REPLICATION",
    "FAIL_CLOSED",
}
SUMMARY_KEYS = ("reconstructed", "partially_reconstructed", "unresolved")
RECONSTRUCTION_RANK = {"unresolved": 0, "partially_reconstructed": 1, "reconstructed": 2}
BOUNDARY_PROBES = {"P-002", "P-005", "P-006", "P-007"}
REQUIRED_CONSULTS = {
    "hard_gate",
    "candidate_selection_risk",
    "contradiction_mapping",
    "replay_adequacy",
    "final_claim_boundary_audit",
}
REQUIRED_CLAIMS = {
    "pond_backed_runtime_participated",
    "independent_traces_used",
    "full_lineage_improved_each_valid_trace",
    "aggregate_verdict_bounded",
    "no_global_superiority_claim",
    "no_target_system_defect_claim",
    "proof_010_synthetic_only_boundary_preserved",
    "proof_011_013_real_trace_boundaries_preserved",
    "remaining_unresolved_questions_preserved",
}

REQUIRED_TOP_FILES = [
    "README.md",
    "replication_plan.md",
    "candidate_selection_report.md",
    "candidate_redaction_report.md",
    "candidate_conversion_report.md",
    "trace_results.json",
    "comparative_reconstruction_report.md",
    "replication_summary.md",
    "claim_register.json",
    "public_lineage_summary.md",
    "final_verdict.json",
    "proof_manifest.json",
]

REQUIRED_TRACE_FILES = [
    "fixture/README.md",
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
    "visible_only_replay_results.json",
    "full_lineage_replay_results.json",
    "reconstruction_probe_results.json",
    "comparative_reconstruction_report.md",
    "trace_verdict.json",
    "public_lineage_summary.md",
]

LOCAL_PATH_RE = re.compile(r"(?<![\w.-])/(?:Users|private|tmp|var|home)/[^\s,;)>\]\"']+")
HASH_RE = re.compile(r"^[a-f0-9]{64}$")
OVERCLAIM_PATTERNS = [
    re.compile(r"\bglobally superior\b", re.IGNORECASE),
    re.compile(r"\buniversal superiority\b", re.IGNORECASE),
    re.compile(r"\bglobal superiority claim\b.{0,40}\b(true|made|validated|proven|confirmed)\b", re.IGNORECASE),
    re.compile(r"\b(agi|consciousness)\b.{0,50}\b(validated|proven|demonstrated|achieved|confirmed)\b", re.IGNORECASE),
    re.compile(r"\b(validates|proves|demonstrates|confirms)\b.{0,50}\b(agi|consciousness)\b", re.IGNORECASE),
    re.compile(r"\bblack[-_ ]box[-_ ]solved\b.{0,40}\b(true|validated|proven|confirmed)\b", re.IGNORECASE),
    re.compile(r"\btarget[-_ ]system defect\b.{0,50}\b(true|validated|proven|confirmed|observed)\b", re.IGNORECASE),
    re.compile(r"\b(validates|proves|demonstrates|confirms)\b.{0,50}\btarget[-_ ]system defect\b", re.IGNORECASE),
]
NEGATION_MARKERS = ("no ", "not ", "false", "disallowed", "blocked", "without ", "does not ", "do not ")
BANNED_SECRET_STRINGS = ("api_key", "private_key", "password", "bearer ")


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


def check_required_files(base: Path, required: list[str], errors: list[str]) -> None:
    for relative in required:
        if not (base / relative).is_file():
            errors.append(f"missing required artifact: {relative}")


def check_jsonl(path: Path, label: str, errors: list[str]) -> None:
    text = read_text(path, errors)
    if not text:
        return
    lines = [line for line in text.splitlines() if line.strip()]
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


def is_hash(value: Any) -> bool:
    return isinstance(value, str) and bool(HASH_RE.fullmatch(value))


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


def check_replay_results(doc: Any, trace_id: str, mode: str, errors: list[str]) -> list[dict[str, Any]]:
    label = f"{trace_id}.{mode}"
    if not isinstance(doc, dict):
        errors.append(f"{label}: expected object")
        return []
    if doc.get("proof_id") != PROOF_ID:
        errors.append(f"{label}.proof_id: expected {PROOF_ID}")
    if doc.get("trace_id") != trace_id:
        errors.append(f"{label}.trace_id: expected {trace_id}")
    if doc.get("mode") != mode:
        errors.append(f"{label}.mode: expected {mode}")
    expected_fixture = f"proofs/{PROOF_ID}/traces/{trace_id}/fixture"
    if doc.get("source_fixture") != expected_fixture:
        errors.append(f"{label}.source_fixture: expected {expected_fixture}")

    raw_results = doc.get("results")
    if not isinstance(raw_results, list):
        errors.append(f"{label}.results: expected array")
        return []
    results = [item for item in raw_results if isinstance(item, dict)]
    if len(results) != len(raw_results):
        errors.append(f"{label}.results: expected only objects")

    seen: set[str] = set()
    refs_field = "available_refs" if mode == "visible_only" else "fixture_refs"
    for index, result in enumerate(results):
        path = f"{label}.results[{index}]"
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
        if not isinstance(result.get(refs_field), list):
            errors.append(f"{path}.{refs_field}: expected array")

    for probe_id in PROBE_IDS:
        if probe_id not in seen:
            errors.append(f"{label}: missing probe {probe_id}")
    check_summary(doc, results, label, errors)
    return results


def improvement_count(visible: list[dict[str, Any]], full: list[dict[str, Any]]) -> int:
    visible_by_id = {item.get("probe_id"): item.get("score") for item in visible}
    count = 0
    for result in full:
        probe_id = result.get("probe_id")
        if RECONSTRUCTION_RANK.get(result.get("score"), -1) > RECONSTRUCTION_RANK.get(visible_by_id.get(probe_id), -1):
            count += 1
    return count


def improved_boundary_probe(visible: list[dict[str, Any]], full: list[dict[str, Any]]) -> bool:
    visible_by_id = {item.get("probe_id"): item.get("score") for item in visible}
    for result in full:
        probe_id = result.get("probe_id")
        if probe_id in BOUNDARY_PROBES and RECONSTRUCTION_RANK.get(result.get("score"), -1) > RECONSTRUCTION_RANK.get(
            visible_by_id.get(probe_id), -1
        ):
            return True
    return False


def check_probe_comparisons(
    probe_doc: Any,
    trace_id: str,
    visible: list[dict[str, Any]],
    full: list[dict[str, Any]],
    errors: list[str],
) -> None:
    if not isinstance(probe_doc, dict):
        errors.append(f"{trace_id}.reconstruction_probe_results.json: expected object")
        return
    results = probe_doc.get("results")
    if not isinstance(results, list) or len(results) != len(PROBE_IDS):
        errors.append(f"{trace_id}.reconstruction_probe_results.results: expected eight probe comparisons")
        return
    visible_by_id = {item.get("probe_id"): item.get("score") for item in visible}
    full_by_id = {item.get("probe_id"): item.get("score") for item in full}
    for index, result in enumerate(results):
        probe_id = result.get("probe_id")
        if probe_id not in PROBE_IDS:
            errors.append(f"{trace_id}.reconstruction_probe_results.results[{index}].probe_id: invalid")
            continue
        if result.get("visible_only") != visible_by_id.get(probe_id):
            errors.append(f"{trace_id}.reconstruction_probe_results.{probe_id}.visible_only: mismatch")
        if result.get("full_lineage") != full_by_id.get(probe_id):
            errors.append(f"{trace_id}.reconstruction_probe_results.{probe_id}.full_lineage: mismatch")
        expected_improved = RECONSTRUCTION_RANK[full_by_id[probe_id]] > RECONSTRUCTION_RANK[visible_by_id[probe_id]]
        if result.get("improvement") is not expected_improved:
            errors.append(f"{trace_id}.reconstruction_probe_results.{probe_id}.improvement: mismatch")


def check_provenance(provenance: Any, trace_id: str, errors: list[str]) -> bool:
    if not isinstance(provenance, dict):
        errors.append(f"{trace_id}.fixture/provenance_manifest.json: expected object")
        return False
    ok = True
    if provenance.get("provenance_status") != "established_for_redacted_local_trace":
        errors.append(f"{trace_id}.provenance_status: expected established_for_redacted_local_trace")
        ok = False
    if provenance.get("redaction_complete") is not True:
        errors.append(f"{trace_id}.redaction_complete: expected true")
        ok = False
    if provenance.get("visible_only_separable_from_full_lineage") is not True:
        errors.append(f"{trace_id}.visible_only_separable_from_full_lineage: expected true")
        ok = False
    if not isinstance(provenance.get("source_refs"), list) or not provenance["source_refs"]:
        errors.append(f"{trace_id}.source_refs: expected non-empty array")
        ok = False
    if not is_hash(provenance.get("fixture_hash")):
        errors.append(f"{trace_id}.fixture_hash: expected sha256")
        ok = False
    return ok


def check_runtime_config(runtime_config: Any, trace_id: str, errors: list[str]) -> None:
    if not isinstance(runtime_config, dict):
        errors.append(f"{trace_id}.fixture/runtime_config.json: expected object")
        return
    gate = runtime_config.get("inside_voice_gate")
    if not isinstance(gate, dict):
        errors.append(f"{trace_id}.inside_voice_gate: expected object")
        return
    if gate.get("adapter_status") != "pond_backed":
        errors.append(f"{trace_id}.inside_voice_gate.adapter_status: expected pond_backed")
    if gate.get("contribution_grade") not in {"bounded", "strong"}:
        errors.append(f"{trace_id}.inside_voice_gate.contribution_grade: expected bounded or strong")
    for field in ("request_hash", "response_hash", "runtime_response_hash", "corpus_hash"):
        if not is_hash(gate.get(field)):
            errors.append(f"{trace_id}.inside_voice_gate.{field}: expected sha256")
    if gate.get("gate_failures") != []:
        errors.append(f"{trace_id}.inside_voice_gate.gate_failures: expected []")


def check_tool_results(tool_results: Any, trace_id: str, errors: list[str]) -> None:
    if not isinstance(tool_results, dict):
        errors.append(f"{trace_id}.fixture/tool_results_manifest.json: expected object")
        return
    results = tool_results.get("tool_results")
    if not isinstance(results, list) or not results:
        errors.append(f"{trace_id}.tool_results: expected non-empty array")
        return
    for index, result in enumerate(results):
        if not isinstance(result, dict):
            errors.append(f"{trace_id}.tool_results[{index}]: expected object")
            continue
        if not isinstance(result.get("id"), str) or not result["id"]:
            errors.append(f"{trace_id}.tool_results[{index}].id: expected non-empty string")
        if not is_hash(result.get("result_hash")):
            errors.append(f"{trace_id}.tool_results[{index}].result_hash: expected sha256")


def expected_trace_verdict(visible: list[dict[str, Any]], full: list[dict[str, Any]], provenance_ok: bool) -> str:
    if not provenance_ok:
        return "TRACE_INVALID"
    full_reconstructed = sum(1 for result in full if result.get("score") == "reconstructed")
    visible_weak = sum(1 for result in visible if result.get("score") in {"partially_reconstructed", "unresolved"})
    improved = improvement_count(visible, full)
    same_scores = all(result.get("score") == {item.get("probe_id"): item.get("score") for item in visible}.get(result.get("probe_id")) for result in full)
    if full_reconstructed >= 6 and visible_weak >= 3 and improved_boundary_probe(visible, full):
        return "TRACE_ADVANTAGE_OBSERVED"
    if improved >= 2:
        return "TRACE_PARTIAL_ADVANTAGE"
    if same_scores:
        return "TRACE_NO_ADVANTAGE"
    return "TRACE_INVALID"


def check_trace(trace_dir: Path, errors: list[str]) -> dict[str, Any]:
    trace_id = trace_dir.name
    check_required_files(trace_dir, REQUIRED_TRACE_FILES, errors)
    if any(error.startswith("missing required artifact:") for error in errors):
        return {"trace_id": trace_id, "verdict": "TRACE_INVALID", "valid": False}

    for relative in ("fixture/transcript.jsonl", "fixture/events.jsonl", "fixture/tool_actions.jsonl", "fixture/memory_log.jsonl", "fixture/recovery_trace.jsonl"):
        check_jsonl(trace_dir / relative, f"{trace_id}.{relative}", errors)

    visible_doc = load_json(trace_dir / "visible_only_replay_results.json", errors)
    full_doc = load_json(trace_dir / "full_lineage_replay_results.json", errors)
    probe_doc = load_json(trace_dir / "reconstruction_probe_results.json", errors)
    verdict_doc = load_json(trace_dir / "trace_verdict.json", errors)
    provenance = load_json(trace_dir / "fixture" / "provenance_manifest.json", errors)
    runtime_config = load_json(trace_dir / "fixture" / "runtime_config.json", errors)
    tool_results = load_json(trace_dir / "fixture" / "tool_results_manifest.json", errors)

    visible = check_replay_results(visible_doc, trace_id, "visible_only", errors)
    full = check_replay_results(full_doc, trace_id, "full_lineage", errors)
    check_probe_comparisons(probe_doc, trace_id, visible, full, errors)
    provenance_ok = check_provenance(provenance, trace_id, errors)
    check_runtime_config(runtime_config, trace_id, errors)
    check_tool_results(tool_results, trace_id, errors)

    expected = expected_trace_verdict(visible, full, provenance_ok)
    actual = verdict_doc.get("verdict") if isinstance(verdict_doc, dict) else None
    if actual not in TRACE_VERDICTS:
        errors.append(f"{trace_id}.trace_verdict.verdict: invalid verdict")
    elif actual != expected:
        errors.append(f"{trace_id}.trace_verdict.verdict: expected {expected}, got {actual}")

    return {
        "trace_id": trace_id,
        "verdict": actual or "TRACE_INVALID",
        "valid": actual != "TRACE_INVALID" and provenance_ok,
        "visible_reconstructed": sum(1 for result in visible if result.get("score") == "reconstructed"),
        "visible_weak": sum(1 for result in visible if result.get("score") in {"partially_reconstructed", "unresolved"}),
        "full_reconstructed": sum(1 for result in full if result.get("score") == "reconstructed"),
        "improvement_count": improvement_count(visible, full),
    }


def expected_aggregate_verdict(trace_summaries: list[dict[str, Any]]) -> str:
    valid = [item for item in trace_summaries if item.get("valid")]
    if len(valid) < 2:
        return "INVALID_REPLICATION"
    advantage = sum(1 for item in valid if item.get("verdict") == "TRACE_ADVANTAGE_OBSERVED")
    partial = sum(1 for item in valid if item.get("verdict") == "TRACE_PARTIAL_ADVANTAGE")
    no_advantage = sum(1 for item in valid if item.get("verdict") == "TRACE_NO_ADVANTAGE")
    if advantage >= 2:
        return "REPLICATION_ADVANTAGE_OBSERVED"
    if advantage >= 1 or partial >= 2:
        return "PARTIAL_REPLICATION_ADVANTAGE"
    if no_advantage == len(valid):
        return "NO_REPLICATION_ADVANTAGE"
    return "INVALID_REPLICATION"


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
    audit = response.get("claim_boundary_audit")
    if not isinstance(audit, list) or not any(item.get("id") == "audit.safe_negated_claim_boundary" for item in audit if isinstance(item, dict)):
        errors.append(f"{label}.claim_boundary_audit: missing audit.safe_negated_claim_boundary")
    boundaries = response.get("operational_boundaries")
    boundary_ids = {item.get("id") for item in boundaries if isinstance(item, dict)} if isinstance(boundaries, list) else set()
    if "boundary.proof_010.synthetic_fixture_only" not in boundary_ids:
        errors.append(f"{label}.operational_boundaries: missing Proof 010 synthetic-only boundary")
    if "boundary.proof_011.real_trace_gate" not in boundary_ids:
        errors.append(f"{label}.operational_boundaries: missing Proof 011 real-trace boundary")
    lineage = response.get("lineage") if isinstance(response.get("lineage"), dict) else {}
    runtime = lineage.get("runtime") if isinstance(lineage.get("runtime"), dict) else {}
    for field in ("runtime_response_hash", "corpus_hash"):
        if not is_hash(runtime.get(field)):
            errors.append(f"{label}.lineage.runtime.{field}: expected sha256")


def check_inside_voice_consults(proof_dir: Path, trace_results: Any, errors: list[str]) -> None:
    consult_dir = proof_dir / "inside_voice_consults"
    if not consult_dir.is_dir():
        errors.append("inside_voice_consults: missing directory")
        return
    recorded = set()
    if isinstance(trace_results, dict) and isinstance(trace_results.get("inside_voice_consults"), list):
        for item in trace_results["inside_voice_consults"]:
            if isinstance(item, dict) and isinstance(item.get("consult_type"), str):
                recorded.add(item["consult_type"])
    missing_recorded = REQUIRED_CONSULTS - recorded
    if missing_recorded:
        errors.append(f"trace_results.inside_voice_consults: missing {sorted(missing_recorded)}")

    for consult_type in REQUIRED_CONSULTS:
        request_path = consult_dir / f"{consult_type}_request.json"
        response_path = consult_dir / f"{consult_type}_response.json"
        if not request_path.is_file():
            errors.append(f"missing Inside Voice request artifact: {request_path.relative_to(proof_dir)}")
        if not response_path.is_file():
            errors.append(f"missing Inside Voice response artifact: {response_path.relative_to(proof_dir)}")
            continue
        response = load_json(response_path, errors)
        check_consult_response(response, f"inside_voice_consults.{consult_type}", errors)


def check_claim_register(register: Any, errors: list[str]) -> None:
    if not isinstance(register, dict):
        errors.append("claim_register.json: expected object")
        return
    claims = register.get("claims")
    if not isinstance(claims, list) or not claims:
        errors.append("claim_register.claims: expected non-empty array")
        return
    seen: set[str] = set()
    for index, claim in enumerate(claims):
        path = f"claim_register.claims[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{path}: expected object")
            continue
        claim_id = claim.get("claim_id")
        if isinstance(claim_id, str):
            seen.add(claim_id)
        if claim.get("claim_level") not in VALID_CLAIM_LEVELS:
            errors.append(f"{path}.claim_level: expected one of {sorted(VALID_CLAIM_LEVELS)}")
        if not isinstance(claim.get("evidence_refs"), list) or not claim["evidence_refs"]:
            errors.append(f"{path}.evidence_refs: expected non-empty array")
        for field in ("claim_id", "safe_public_wording", "risk_if_overstated"):
            if not isinstance(claim.get(field), str) or not claim[field]:
                errors.append(f"{path}.{field}: expected non-empty string")
    missing = REQUIRED_CLAIMS - seen
    if missing:
        errors.append(f"claim_register.claims: missing {sorted(missing)}")


def check_final_verdict(final_verdict: Any, expected: str, valid_trace_count: int, errors: list[str]) -> None:
    if not isinstance(final_verdict, dict):
        errors.append("final_verdict.json: expected object")
        return
    if final_verdict.get("verdict") not in AGGREGATE_VERDICTS:
        errors.append("final_verdict.verdict: invalid aggregate verdict")
    elif final_verdict.get("verdict") != expected:
        errors.append(f"final_verdict.verdict: expected {expected}, got {final_verdict.get('verdict')}")
    if final_verdict.get("valid_trace_count") != valid_trace_count:
        errors.append(f"final_verdict.valid_trace_count: expected {valid_trace_count}")
    if final_verdict.get("adapter_status") != "pond_backed":
        errors.append("final_verdict.adapter_status: expected pond_backed")
    for field in ("global_superiority_claim", "target_system_defect_claim", "agi_claim", "consciousness_claim", "black_box_solved_claim"):
        if final_verdict.get(field) is not False:
            errors.append(f"final_verdict.{field}: expected false")


def text_has_positive_overclaim(text: str) -> str | None:
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
        if not path.is_file() or path.suffix not in {".md", ".json", ".jsonl"}:
            continue
        text = read_text(path, errors)
        lowered = text.lower()
        for banned in BANNED_SECRET_STRINGS:
            if banned in lowered:
                errors.append(f"{path.relative_to(proof_dir)}: banned secret marker detected: {banned}")
        if LOCAL_PATH_RE.search(text):
            errors.append(f"{path.relative_to(proof_dir)}: local path leaked across public/private boundary")
        combined += "\n" + text

    overclaim = text_has_positive_overclaim(combined)
    if overclaim:
        errors.append(f"positive overclaim detected: {overclaim}")

    lowered = combined.lower()
    for phrase in ("public/private", "redacted", "proof 010", "synthetic", "proof 011", "proof 013"):
        if phrase not in lowered:
            errors.append(f"public/private or proof boundary text missing: {phrase}")


def validate_real_trace_replication(proof_dir: Path | str) -> list[str]:
    proof_dir = Path(proof_dir)
    if not proof_dir.is_absolute():
        proof_dir = ROOT / proof_dir

    errors: list[str] = []
    check_required_files(proof_dir, REQUIRED_TOP_FILES, errors)
    if errors:
        return errors

    trace_root = proof_dir / "traces"
    trace_dirs = sorted(path for path in trace_root.glob("trace_*") if path.is_dir()) if trace_root.is_dir() else []
    if len(trace_dirs) < 2:
        errors.append("at least 2 trace folders are required")

    trace_summaries = [check_trace(trace_dir, errors) for trace_dir in trace_dirs]
    valid_trace_count = sum(1 for item in trace_summaries if item.get("valid"))
    expected_verdict = expected_aggregate_verdict(trace_summaries)

    trace_results = load_json(proof_dir / "trace_results.json", errors)
    final_verdict = load_json(proof_dir / "final_verdict.json", errors)
    claim_register = load_json(proof_dir / "claim_register.json", errors)
    manifest = load_json(proof_dir / "proof_manifest.json", errors)

    if isinstance(trace_results, dict):
        if trace_results.get("valid_trace_count") != valid_trace_count:
            errors.append(f"trace_results.valid_trace_count: expected {valid_trace_count}")
        result_ids = {item.get("trace_id") for item in trace_results.get("traces", []) if isinstance(item, dict)}
        expected_ids = {item.get("trace_id") for item in trace_summaries}
        if result_ids != expected_ids:
            errors.append("trace_results.traces: trace ids do not match trace folders")
    else:
        errors.append("trace_results.json: expected object")

    check_inside_voice_consults(proof_dir, trace_results, errors)
    check_final_verdict(final_verdict, expected_verdict, valid_trace_count, errors)
    check_claim_register(claim_register, errors)
    check_text_boundaries(proof_dir, errors)

    if isinstance(manifest, dict):
        if manifest.get("proof_id") != PROOF_ID:
            errors.append(f"proof_manifest.proof_id: expected {PROOF_ID}")
        if manifest.get("inside_voice_adapter_status") != "pond_backed":
            errors.append("proof_manifest.inside_voice_adapter_status: expected pond_backed")
        lineage = manifest.get("lineage") if isinstance(manifest.get("lineage"), dict) else {}
        for field in ("request_hash", "response_hash"):
            if not is_hash(lineage.get(field)):
                errors.append(f"proof_manifest.lineage.{field}: expected sha256")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_real_trace_replication.py <proof_dir>", file=sys.stderr)
        return 2

    errors = validate_real_trace_replication(Path(argv[1]))
    if errors:
        print("REAL_TRACE_REPLICATION_INVALID")
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("REAL_TRACE_REPLICATION_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
