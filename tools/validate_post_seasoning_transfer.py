#!/usr/bin/env python3
"""Validate Proof 018 post-seasoning transfer artifacts."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROOF_ID = "018-post-seasoning-transfer-test"

REQUIRED_ROOT_FILES = [
    "README.md",
    "transfer_test_design.md",
    "heldout_task_selection_report.md",
    "baseline_results.json",
    "pond_backed_results.json",
    "mcp_seasoned_visibility_report.json",
    "comparative_transfer_report.md",
    "cross_family_combination_report.md",
    "runtime_log_visibility_report.md",
    "claim_register.json",
    "public_lineage_summary.md",
    "final_verdict.json",
    "proof_manifest.json",
]

REQUIRED_CONSULT_FILES = [
    "hard_gate_request.json",
    "hard_gate_response.json",
    "task_001_pond_request.json",
    "task_001_pond_response.json",
    "task_002_pond_request.json",
    "task_002_pond_response.json",
    "task_003_pond_request.json",
    "task_003_pond_response.json",
]

TASK_IDS = ["task_001", "task_002", "task_003"]
REQUIRED_TASK_FILES = [
    "task_description.md",
    "baseline_solution.md",
    "pond_backed_solution.md",
    "baseline_scores.json",
    "pond_backed_scores.json",
    "mcp_seasoned_refs_used.json",
    "task_comparison.md",
    "task_verdict.json",
]

SCORE_KEYS = [
    "task_completeness",
    "contradiction_handling",
    "authority_handling",
    "replayability",
    "prioritization_quality",
    "boundary_discipline",
    "hallucination_prevention",
    "actionability",
]

VALID_TASK_VERDICTS = {
    "TRANSFER_TASK_ADVANTAGE",
    "TRANSFER_TASK_PARTIAL",
    "TRANSFER_TASK_NO_ADVANTAGE",
    "TRANSFER_TASK_INVALID",
}

VALID_FINAL_VERDICTS = {
    "POST_SEASONING_TRANSFER_ADVANTAGE_OBSERVED",
    "PARTIAL_POST_SEASONING_TRANSFER_ADVANTAGE",
    "NO_POST_SEASONING_TRANSFER_ADVANTAGE",
    "INVALID_TRANSFER_TEST",
    "FAIL_CLOSED",
}

HASH_RE = re.compile(r"^[a-f0-9]{64}$")
MCP_REF_RE = re.compile(
    r"(mcp[_-]seasoned|MCP_SEASONED_CANDIDATE|artifacts/pond/mcp_seasoned_|fp_lineage_candidate_|seasoning_id)",
    re.IGNORECASE,
)
BASELINE_FORBIDDEN_RE = re.compile(
    r"(mcp[_-]seasoned|MCP_SEASONED_CANDIDATE|artifacts/pond/mcp_seasoned_|fp_lineage_candidate_|seasoning_id|inside_voice_consults/task_|pressure:[a-f0-9])",
    re.IGNORECASE,
)

OVERCLAIM_PATTERNS = [
    re.compile(r"\bglobally superior\b", re.IGNORECASE),
    re.compile(r"\buniversal superiority\b", re.IGNORECASE),
    re.compile(
        r"\b(validates|validated|proves|proven|demonstrates|demonstrated|confirms|confirmed|shows|showed|is)\b"
        r".{0,90}\b(global[-_ ]superiority|system[-_ ]wide superiority|universal superiority)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(global[-_ ]superiority|system[-_ ]wide superiority|universal superiority)\b.{0,90}"
        r"\b(validates|validated|proves|proven|demonstrates|demonstrated|confirms|confirmed|shown|true|made)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(validates|validated|proves|proven|demonstrates|demonstrated|confirms|confirmed|achieves|achieved)\b"
        r".{0,90}\b(agi|artificial general intelligence|consciousness|black[-_ ]box[-_ ]solv(?:ed|ing))\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(agi|artificial general intelligence|consciousness|black[-_ ]box[-_ ]solv(?:ed|ing))\b"
        r".{0,90}\b(validates|validated|proves|proven|demonstrates|demonstrated|confirms|confirmed|achieves|achieved)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(promotes?|promoted|promotion)\b.{0,90}\b(candidates?|mcp[-_ ]seasoned|reusable_lineage_pool|reusable lineage pool)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(candidates?|mcp[-_ ]seasoned|reusable_lineage_pool|reusable lineage pool)\b.{0,90}\b(promotes?|promoted|promotion)\b",
        re.IGNORECASE,
    ),
]

NEGATION_MARKERS = (
    "no ",
    "not ",
    "does not ",
    "do not ",
    "without ",
    "false",
    "disallowed",
    "blocked",
    "avoid",
    "forbidden",
    "reject",
    "rejected",
    "outside",
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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_hash(value: Any) -> bool:
    return isinstance(value, str) and bool(HASH_RE.fullmatch(value))


def has_mcp_ref(value: Any) -> bool:
    return bool(MCP_REF_RE.search(json.dumps(value, sort_keys=True) if not isinstance(value, str) else value))


def positive_overclaim(text: str) -> str | None:
    for pattern in OVERCLAIM_PATTERNS:
        for match in pattern.finditer(text):
            matched_text = match.group(0).lower()
            if any(marker in matched_text for marker in NEGATION_MARKERS):
                continue
            prefix_window = text[max(0, match.start() - 180) : match.start()].lower()
            sentence_start = max(prefix_window.rfind("."), prefix_window.rfind("\n"), prefix_window.rfind(";"))
            prefix = prefix_window[sentence_start + 1 :]
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


def check_required_files(proof_dir: Path, errors: list[str]) -> None:
    for relative in REQUIRED_ROOT_FILES:
        if not (proof_dir / relative).is_file():
            errors.append(f"missing required artifact: {relative}")

    consult_dir = proof_dir / "inside_voice_consults"
    for relative in REQUIRED_CONSULT_FILES:
        if not (consult_dir / relative).is_file():
            errors.append(f"missing consult artifact: inside_voice_consults/{relative}")

    task_root = proof_dir / "tasks"
    found = {path.name for path in task_root.iterdir() if path.is_dir()} if task_root.is_dir() else set()
    expected = set(TASK_IDS)
    if found != expected:
        errors.append(f"task folders: expected {sorted(expected)}, got {sorted(found)}")
        return

    for task_id in TASK_IDS:
        for relative in REQUIRED_TASK_FILES:
            if not (task_root / task_id / relative).is_file():
                errors.append(f"missing task artifact: tasks/{task_id}/{relative}")


def check_hard_gate(proof_dir: Path, errors: list[str]) -> None:
    response = load_json(proof_dir / "inside_voice_consults" / "hard_gate_response.json", errors)
    if not isinstance(response, dict):
        return
    if response.get("adapter_status") != "pond_backed":
        errors.append("hard gate adapter_status: expected pond_backed")
    if response.get("contribution_grade") not in {"bounded", "strong"}:
        errors.append("hard gate contribution_grade: expected bounded or strong")
    if not response.get("runtime_stage_report_ref"):
        errors.append("hard gate missing runtime_stage_report_ref")
    if not response.get("pressure_rankings"):
        errors.append("hard gate pressure_rankings empty")
    if response.get("gate_failures") != []:
        errors.append("hard gate gate_failures not empty")
    if "BROAD_UNSUPPORTED_CLAIM_BLOCKED" in json.dumps(response):
        errors.append("hard gate contains BROAD_UNSUPPORTED_CLAIM_BLOCKED")

    audit = response.get("claim_boundary_audit")
    audit_text = json.dumps(audit, sort_keys=True) if isinstance(audit, list) else ""
    if "SAFE_NEGATED_CLAIM_LANGUAGE" not in audit_text and "safe_negated" not in audit_text.lower():
        errors.append("hard gate missing safe-negated boundary handling")

    runtime = response.get("lineage", {}).get("runtime")
    check_runtime_hashes(runtime, "hard gate", errors)


def check_runtime_hashes(runtime: Any, label: str, errors: list[str]) -> None:
    if not isinstance(runtime, dict):
        errors.append(f"{label}: missing runtime hashes")
        return
    for field in ("corpus_hash", "runtime_request_hash", "runtime_response_hash"):
        if not is_hash(runtime.get(field)):
            errors.append(f"{label}: missing or invalid {field}")
    if not runtime.get("schema_version"):
        errors.append(f"{label}: missing schema_version")


def check_baseline_separation(proof_dir: Path, errors: list[str]) -> bool:
    leaked = False
    baseline_paths = [proof_dir / "baseline_results.json"]
    for task_id in TASK_IDS:
        baseline_paths.extend(
            [
                proof_dir / "tasks" / task_id / "baseline_solution.md",
                proof_dir / "tasks" / task_id / "baseline_scores.json",
            ]
        )
    for path in baseline_paths:
        text = read_text(path, errors)
        match = BASELINE_FORBIDDEN_RE.search(text)
        if match:
            errors.append(f"baseline mode cites forbidden MCP-seasoned material in {path}: {match.group(0)}")
            leaked = True
    return leaked


def score_total(score: dict[str, Any], path: Path, errors: list[str]) -> int | None:
    total = 0
    for key in SCORE_KEYS:
        value = score.get(key)
        if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 5:
            errors.append(f"{path}: invalid score field {key}")
            return None
        total += value
    if score.get("total_score") != total:
        errors.append(f"{path}: total_score expected {total}, got {score.get('total_score')}")
    return total


def check_task_artifacts(proof_dir: Path, errors: list[str]) -> dict[str, Any]:
    metrics: dict[str, Any] = {
        "baseline_total": 0,
        "pond_total": 0,
        "tasks_improved": 0,
        "tasks_unchanged": 0,
        "tasks_degraded": 0,
        "refs_visible_by_task": {},
    }

    for task_id in TASK_IDS:
        task_dir = proof_dir / "tasks" / task_id
        baseline_score = load_json(task_dir / "baseline_scores.json", errors)
        pond_score = load_json(task_dir / "pond_backed_scores.json", errors)
        verdict = load_json(task_dir / "task_verdict.json", errors)
        refs_used = load_json(task_dir / "mcp_seasoned_refs_used.json", errors)
        response = load_json(proof_dir / "inside_voice_consults" / f"{task_id}_pond_response.json", errors)

        if not all(isinstance(item, dict) for item in (baseline_score, pond_score, verdict, refs_used, response)):
            continue

        baseline_total = score_total(baseline_score, task_dir / "baseline_scores.json", errors)
        pond_total = score_total(pond_score, task_dir / "pond_backed_scores.json", errors)
        if baseline_total is None or pond_total is None:
            continue

        metrics["baseline_total"] += baseline_total
        metrics["pond_total"] += pond_total
        if pond_total > baseline_total:
            metrics["tasks_improved"] += 1
        elif pond_total == baseline_total:
            metrics["tasks_unchanged"] += 1
        else:
            metrics["tasks_degraded"] += 1

        if verdict.get("verdict") not in VALID_TASK_VERDICTS:
            errors.append(f"{task_id}: invalid task verdict {verdict.get('verdict')}")
        if verdict.get("baseline_total_score") != baseline_total:
            errors.append(f"{task_id}: task verdict baseline_total_score mismatch")
        if verdict.get("pond_total_score") != pond_total:
            errors.append(f"{task_id}: task verdict pond_total_score mismatch")
        if verdict.get("score_delta") != pond_total - baseline_total:
            errors.append(f"{task_id}: task verdict score_delta mismatch")

        if response.get("adapter_status") != "pond_backed":
            errors.append(f"{task_id}: response adapter_status expected pond_backed")
        if response.get("gate_failures") != []:
            errors.append(f"{task_id}: response gate_failures not empty")
        check_runtime_hashes(response.get("lineage", {}).get("runtime"), task_id, errors)

        response_refs_visible = has_mcp_ref(response.get("retrieved_artifact_refs", [])) or has_mcp_ref(
            response.get("pressure_rankings", [])
        )
        refs_file_visible = has_mcp_ref(refs_used.get("refs", []))
        pond_solution_visible = has_mcp_ref(read_text(task_dir / "pond_backed_solution.md", errors))
        metrics["refs_visible_by_task"][task_id] = response_refs_visible and refs_file_visible and pond_solution_visible

        if not response_refs_visible:
            errors.append(f"{task_id}: response lacks MCP-seasoned refs")
        if not refs_file_visible:
            errors.append(f"{task_id}: mcp_seasoned_refs_used.json lacks MCP-seasoned refs")
        if not pond_solution_visible:
            errors.append(f"{task_id}: pond_backed_solution.md lacks MCP-seasoned refs")

        refs_runtime = refs_used.get("runtime_hashes")
        check_runtime_hashes(refs_runtime, f"{task_id} refs file", errors)

    return metrics


def expected_final_verdict(metrics: dict[str, Any], visibility: dict[str, Any], overclaiming: bool) -> str:
    refs_visible_by_task = metrics.get("refs_visible_by_task", {})
    improved_tasks = sorted(metrics.get("improved_task_ids", set()))
    refs_visible_all_improved = all(refs_visible_by_task.get(task_id) for task_id in improved_tasks)
    cross_family_count = int(visibility.get("cross_family_combinations_observed", 0))
    if overclaiming:
        return "INVALID_TRANSFER_TEST"
    if (
        metrics["tasks_improved"] >= 2
        and metrics["pond_total"] > metrics["baseline_total"]
        and refs_visible_all_improved
        and cross_family_count >= 1
    ):
        return "POST_SEASONING_TRANSFER_ADVANTAGE_OBSERVED"
    if metrics["tasks_improved"] >= 1 or any(refs_visible_by_task.values()):
        return "PARTIAL_POST_SEASONING_TRANSFER_ADVANTAGE"
    if metrics["tasks_improved"] == 0:
        return "NO_POST_SEASONING_TRANSFER_ADVANTAGE"
    return "INVALID_TRANSFER_TEST"


def check_visibility_reports(proof_dir: Path, errors: list[str]) -> dict[str, Any]:
    visibility = load_json(proof_dir / "mcp_seasoned_visibility_report.json", errors)
    if not isinstance(visibility, dict):
        return {"cross_family_combinations_observed": 0}

    per_task = visibility.get("per_task")
    if not isinstance(per_task, list) or len(per_task) != 3:
        errors.append("mcp_seasoned_visibility_report.per_task expected 3 entries")
    else:
        response_visible = all(bool(item.get("response_refs_visible")) for item in per_task)
        log_visible = all(bool(item.get("runtime_log_refs_visible")) for item in per_task)
        expected = "RUNTIME_VISIBILITY_CONFIRMED" if response_visible and log_visible else (
            "RESPONSE_VISIBLE_LOG_NOT_VERBOSE" if response_visible and not log_visible else "SEASONED_RECALL_NOT_VISIBLE"
        )
        if visibility.get("classification") != expected:
            errors.append(f"visibility classification expected {expected}, got {visibility.get('classification')}")
        for item in per_task:
            if not has_mcp_ref(item.get("refs", [])):
                errors.append(f"{item.get('task_id')}: visibility report lacks MCP-seasoned refs")

    runtime_report = read_text(proof_dir / "runtime_log_visibility_report.md", errors)
    if "RESPONSE_VISIBLE_LOG_NOT_VERBOSE" not in runtime_report:
        errors.append("runtime_log_visibility_report.md missing RESPONSE_VISIBLE_LOG_NOT_VERBOSE classification")

    cross_report = read_text(proof_dir / "cross_family_combination_report.md", errors)
    cross_count = cross_report.count("cross_family_combination_observed")
    if cross_count < 1:
        errors.append("cross_family_combination_report.md lacks observed combination classification")
    visibility["cross_family_combinations_observed"] = cross_count
    return visibility


def check_reusable_pool(visibility: dict[str, Any], errors: list[str]) -> None:
    pool = visibility.get("reusable_lineage_pool") if isinstance(visibility, dict) else None
    if not isinstance(pool, dict):
        errors.append("mcp_seasoned_visibility_report missing reusable_lineage_pool")
        return
    pre_hash = pool.get("pre_test_sha256")
    post_hash = pool.get("post_test_sha256")
    if not is_hash(pre_hash) or not is_hash(post_hash):
        errors.append("reusable_lineage_pool hash missing or invalid")
    if pre_hash != post_hash or pool.get("unchanged") is not True:
        errors.append("reusable_lineage_pool mutation detected in recorded hashes")

    path_value = pool.get("path")
    if isinstance(path_value, str):
        pool_path = Path(path_value)
        if pool_path.exists():
            current_hash = sha256_file(pool_path)
            if current_hash != pre_hash or current_hash != post_hash:
                errors.append("reusable_lineage_pool current hash differs from recorded proof hash")


def check_final_math(proof_dir: Path, metrics: dict[str, Any], visibility: dict[str, Any], errors: list[str]) -> None:
    final = load_json(proof_dir / "final_verdict.json", errors)
    baseline = load_json(proof_dir / "baseline_results.json", errors)
    pond = load_json(proof_dir / "pond_backed_results.json", errors)
    if not all(isinstance(item, dict) for item in (final, baseline, pond)):
        return

    improved_task_ids = set()
    for task_id in TASK_IDS:
        verdict = load_json(proof_dir / "tasks" / task_id / "task_verdict.json", errors)
        if isinstance(verdict, dict) and verdict.get("score_delta", 0) > 0:
            improved_task_ids.add(task_id)
    metrics["improved_task_ids"] = improved_task_ids

    aggregate = final.get("aggregate_metrics", {})
    expected_values = {
        "baseline_total_score": metrics["baseline_total"],
        "pond_total_score": metrics["pond_total"],
        "score_delta": metrics["pond_total"] - metrics["baseline_total"],
        "tasks_improved": metrics["tasks_improved"],
        "tasks_unchanged": metrics["tasks_unchanged"],
        "tasks_degraded": metrics["tasks_degraded"],
    }
    for field, expected in expected_values.items():
        if aggregate.get(field) != expected:
            errors.append(f"final_verdict.aggregate_metrics.{field}: expected {expected}, got {aggregate.get(field)}")

    if baseline.get("aggregate", {}).get("baseline_total_score") != metrics["baseline_total"]:
        errors.append("baseline_results aggregate total mismatch")
    if pond.get("aggregate", {}).get("pond_total_score") != metrics["pond_total"]:
        errors.append("pond_backed_results aggregate total mismatch")

    if aggregate.get("mcp_seasoned_refs_visible") is not True:
        errors.append("final verdict missing mcp_seasoned_refs_visible true")
    if aggregate.get("cross_family_combinations_observed", 0) < 1:
        errors.append("final verdict missing cross-family combination count")

    verdict = final.get("verdict")
    if verdict not in VALID_FINAL_VERDICTS:
        errors.append(f"final_verdict.verdict: invalid {verdict}")
        return

    overclaiming = positive_overclaim(json.dumps(final, sort_keys=True)) is not None
    expected = expected_final_verdict(metrics, visibility, overclaiming)
    if verdict != expected:
        errors.append(f"final_verdict.verdict: expected {expected}, got {verdict}")


def validate_post_seasoning_transfer(proof_dir: Path) -> list[str]:
    if not proof_dir.is_absolute():
        proof_dir = ROOT / proof_dir

    errors: list[str] = []
    if not proof_dir.is_dir():
        return [f"proof directory not found: {proof_dir}"]

    check_required_files(proof_dir, errors)
    check_hard_gate(proof_dir, errors)
    baseline_leaked = check_baseline_separation(proof_dir, errors)
    metrics = check_task_artifacts(proof_dir, errors)
    visibility = check_visibility_reports(proof_dir, errors)
    check_reusable_pool(visibility, errors)
    check_text_boundaries(proof_dir, errors)
    check_final_math(proof_dir, metrics, visibility, errors)

    if baseline_leaked:
        final = load_json(proof_dir / "final_verdict.json", errors)
        if isinstance(final, dict) and final.get("verdict") != "INVALID_TRANSFER_TEST":
            errors.append("baseline replay separation broken but final verdict is not INVALID_TRANSFER_TEST")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_post_seasoning_transfer.py <proof_dir>", file=sys.stderr)
        return 2

    errors = validate_post_seasoning_transfer(Path(argv[1]))
    if errors:
        print("POST_SEASONING_TRANSFER_INVALID")
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("POST_SEASONING_TRANSFER_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
