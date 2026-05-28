#!/usr/bin/env python3
"""Validate Proof 019 MCP-seasoning ablation artifacts."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROOF_ID = "019-mcp-seasoning-ablation-control"

TASK_IDS = ["task_001", "task_002", "task_003", "task_004"]
MODES = ["baseline", "seasoned", "ablated"]
SOLUTION_LABELS = ["solution_A", "solution_B", "solution_C"]
SCORE_KEYS = [
    "contradiction_handling",
    "authority_handling",
    "replayability",
    "prioritization_quality",
    "operational_continuity",
    "uncertainty_discipline",
    "hallucination_prevention",
    "actionability",
    "boundary_discipline",
]

REQUIRED_ROOT_FILES = [
    "README.md",
    "blind_protocol.md",
    "task_selection_report.md",
    "ablation_design.md",
    "aggregate_results.json",
    "comparative_ablation_report.md",
    "runtime_visibility_report.md",
    "claim_register.json",
    "public_lineage_summary.md",
    "final_verdict.json",
    "proof_manifest.json",
]

REQUIRED_CONSULT_FILES = [
    "hard_gate_request.json",
    "hard_gate_response.json",
    *[f"{task_id}_{mode}_request.json" for task_id in TASK_IDS for mode in ("seasoned", "ablated")],
    *[f"{task_id}_{mode}_response.json" for task_id in TASK_IDS for mode in ("seasoned", "ablated")],
]

REQUIRED_TASK_FILES = [
    "task_description.md",
    "baseline_solution.md",
    "seasoned_solution.md",
    "ablated_solution.md",
    "blind_scoring_results.json",
    "task_comparison.md",
    "task_verdict.json",
]

VALID_FINAL_VERDICTS = {
    "SEASONING_TRANSFER_ADVANTAGE_CONFIRMED",
    "PARTIAL_SEASONING_TRANSFER_ADVANTAGE",
    "NO_SEASONING_TRANSFER_ADVANTAGE",
    "INVALID_ABLATION_TEST",
    "FAIL_CLOSED",
}

HASH_RE = re.compile(r"^[a-f0-9]{64}$")
MCP_REF_RE = re.compile(
    r"(MCP_SEASONED_CANDIDATE|artifacts/pond/mcp_seasoned_[^\\s\"']+|mcp_seasoned_[a-z0-9_./#-]+)",
    re.IGNORECASE,
)
BASELINE_FORBIDDEN_RE = re.compile(
    r"(MCP_SEASONED_CANDIDATE|artifacts/pond/mcp_seasoned_[^\\s\"']+|inside_voice_consults/.+response\\.json|pressure:[a-f0-9])",
    re.IGNORECASE,
)

OVERCLAIM_PATTERNS = [
    re.compile(r"\bglobally superior\b", re.IGNORECASE),
    re.compile(r"\buniversal superiority\b", re.IGNORECASE),
    re.compile(
        r"\b(validates|validated|proves|proven|demonstrates|demonstrated|confirms|confirmed|shows|showed|is)\b"
        r".{0,90}\b(global[-_ ]superiority|system[-_ ]wide superiority|universal superiority|broad capability|generalized cognition)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(global[-_ ]superiority|system[-_ ]wide superiority|universal superiority|broad capability|generalized cognition)\b"
        r".{0,90}\b(validates|validated|proves|proven|demonstrates|demonstrated|confirms|confirmed|shown|true|made)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(validates|validated|proves|proven|demonstrates|demonstrated|confirms|confirmed|achieves|achieved)\b"
        r".{0,90}\b(agi|artificial general intelligence|consciousness|black[-_ ]box[-_ ]solv(?:ed|ing))\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(agi|artificial general intelligence|consciousness|black[-_ ]box[-_ ]solv(?:ed|ing))\b"
        r".{0,90}\b(validates|validated|proves|proven|demonstrates|demonstrated|confirms|confirmed|achieves|achieved|true)\b",
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
    "bounded",
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


def runtime_lineage(response: dict[str, Any]) -> dict[str, Any]:
    lineage = response.get("lineage") if isinstance(response.get("lineage"), dict) else {}
    runtime = lineage.get("runtime")
    return runtime if isinstance(runtime, dict) else lineage


def has_mcp_ref(value: Any) -> bool:
    rendered = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    return bool(MCP_REF_RE.search(rendered))


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


def check_runtime_hashes(response: dict[str, Any], label: str, errors: list[str]) -> None:
    runtime = runtime_lineage(response)
    if not isinstance(runtime, dict):
        errors.append(f"{label}: missing runtime hashes")
        return
    for field in ("corpus_hash", "runtime_request_hash", "runtime_response_hash"):
        if not is_hash(runtime.get(field)):
            errors.append(f"{label}: missing or invalid {field}")
    if not runtime.get("schema_version"):
        errors.append(f"{label}: missing schema_version")


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
    audit_text = json.dumps(response.get("claim_boundary_audit"), sort_keys=True)
    if "SAFE_NEGATED_CLAIM_LANGUAGE" not in audit_text and "safe_negated" not in audit_text.lower():
        errors.append("hard gate missing safe-negated boundary audit")
    check_runtime_hashes(response, "hard gate", errors)


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


def check_blind_scores(proof_dir: Path, errors: list[str]) -> dict[str, dict[str, int]]:
    mode_totals: dict[str, dict[str, int]] = {}
    for task_id in TASK_IDS:
        task_dir = proof_dir / "tasks" / task_id
        blind = load_json(task_dir / "blind_scoring_results.json", errors)
        verdict = load_json(task_dir / "task_verdict.json", errors)
        if not isinstance(blind, dict) or not isinstance(verdict, dict):
            continue

        blind_text = json.dumps(blind, sort_keys=True).lower()
        if any(mode in blind_text for mode in MODES):
            errors.append(f"{task_id}: blind scoring file contains mode-identifying text")
        if blind.get("labels_scored") != SOLUTION_LABELS:
            errors.append(f"{task_id}: blind scoring labels must be solution_A/B/C")
        if blind.get("mode_mapping_included") is not False:
            errors.append(f"{task_id}: blind scoring must not include mode mapping")

        results = blind.get("results")
        if not isinstance(results, dict):
            errors.append(f"{task_id}: blind scoring missing results")
            continue
        mapping = verdict.get("reveal_mapping")
        if not isinstance(mapping, dict):
            errors.append(f"{task_id}: missing reveal mapping")
            continue
        if set(mapping) != set(SOLUTION_LABELS) or set(mapping.values()) != set(MODES):
            errors.append(f"{task_id}: invalid reveal mapping")
            continue

        totals: dict[str, int] = {}
        for label in SOLUTION_LABELS:
            entry = results.get(label)
            if not isinstance(entry, dict) or not isinstance(entry.get("scores"), dict):
                errors.append(f"{task_id}: missing blind score for {label}")
                continue
            merged = dict(entry["scores"])
            merged["total_score"] = entry.get("total_score")
            total = score_total(merged, task_dir / "blind_scoring_results.json", errors)
            if total is not None:
                totals[mapping[label]] = total

        if set(totals) == set(MODES):
            recorded = verdict.get("mode_totals")
            if recorded != totals:
                errors.append(f"{task_id}: task_verdict mode_totals mismatch")
            mode_totals[task_id] = totals

    return mode_totals


def check_mode_artifacts(proof_dir: Path, errors: list[str]) -> dict[str, Any]:
    visibility = {
        "seasoned_visible": 0,
        "ablated_visible": 0,
        "runtime_hashes_differ": True,
    }
    for task_id in TASK_IDS:
        task_dir = proof_dir / "tasks" / task_id
        baseline_text = read_text(task_dir / "baseline_solution.md", errors)
        if BASELINE_FORBIDDEN_RE.search(baseline_text):
            errors.append(f"{task_id}: baseline mode cites forbidden consult or MCP-seasoned material")

        seasoned = load_json(proof_dir / "inside_voice_consults" / f"{task_id}_seasoned_response.json", errors)
        ablated = load_json(proof_dir / "inside_voice_consults" / f"{task_id}_ablated_response.json", errors)
        if not isinstance(seasoned, dict) or not isinstance(ablated, dict):
            continue

        for label, response in ((f"{task_id} seasoned", seasoned), (f"{task_id} ablated", ablated)):
            if response.get("adapter_status") != "pond_backed":
                errors.append(f"{label}: adapter_status expected pond_backed")
            if response.get("gate_failures") != []:
                errors.append(f"{label}: gate_failures not empty")
            if not response.get("pressure_rankings"):
                errors.append(f"{label}: pressure_rankings empty")
            check_runtime_hashes(response, label, errors)

        seasoned_visible = has_mcp_ref(
            {
                "retrieved_artifact_refs": seasoned.get("retrieved_artifact_refs"),
                "lineage_refs": seasoned.get("lineage_refs"),
                "relevant_lineage_refs": seasoned.get("relevant_lineage_refs"),
                "solution": read_text(task_dir / "seasoned_solution.md", errors),
            }
        )
        ablated_visible = has_mcp_ref(
            {
                "retrieved_artifact_refs": ablated.get("retrieved_artifact_refs"),
                "lineage_refs": ablated.get("lineage_refs"),
                "relevant_lineage_refs": ablated.get("relevant_lineage_refs"),
                "pressure_rankings": ablated.get("pressure_rankings"),
                "solution": read_text(task_dir / "ablated_solution.md", errors),
            }
        )
        if not seasoned_visible:
            errors.append(f"{task_id}: seasoned mode lacks MCP-seasoned refs")
        if ablated_visible:
            errors.append(f"{task_id}: seasoned refs leaked into ablated mode")
        visibility["seasoned_visible"] += int(seasoned_visible)
        visibility["ablated_visible"] += int(ablated_visible)

        sr = runtime_lineage(seasoned)
        ar = runtime_lineage(ablated)
        if sr.get("runtime_response_hash") == ar.get("runtime_response_hash") and sr.get("corpus_hash") == ar.get("corpus_hash"):
            errors.append(f"{task_id}: seasoned and ablated runtime hashes did not differ")
            visibility["runtime_hashes_differ"] = False

    return visibility


def expected_verdict(aggregate: dict[str, Any], visibility: dict[str, Any], overclaiming: bool) -> str:
    if overclaiming:
        return "INVALID_ABLATION_TEST"
    if visibility["ablated_visible"] > 0 or visibility["seasoned_visible"] < 4 or not visibility["runtime_hashes_differ"]:
        return "INVALID_ABLATION_TEST"
    if (
        aggregate["seasoned_total"] > aggregate["baseline_total"]
        and aggregate["seasoned_total"] > aggregate["ablated_total"]
        and aggregate["tasks_where_seasoned_won"] >= 3
        and aggregate["tasks_where_ablation_reduced_quality"] >= 2
    ):
        return "SEASONING_TRANSFER_ADVANTAGE_CONFIRMED"
    if aggregate["seasoned_total"] > aggregate["baseline_total"] or aggregate["seasoned_total"] > aggregate["ablated_total"]:
        return "PARTIAL_SEASONING_TRANSFER_ADVANTAGE"
    return "NO_SEASONING_TRANSFER_ADVANTAGE"


def check_final_math(proof_dir: Path, mode_totals: dict[str, dict[str, int]], visibility: dict[str, Any], errors: list[str]) -> None:
    aggregate = load_json(proof_dir / "aggregate_results.json", errors)
    final = load_json(proof_dir / "final_verdict.json", errors)
    if not isinstance(aggregate, dict) or not isinstance(final, dict):
        return

    computed = {
        "baseline_total": sum(totals.get("baseline", 0) for totals in mode_totals.values()),
        "seasoned_total": sum(totals.get("seasoned", 0) for totals in mode_totals.values()),
        "ablated_total": sum(totals.get("ablated", 0) for totals in mode_totals.values()),
        "tasks_where_seasoned_won": 0,
        "tasks_where_ablation_reduced_quality": 0,
        "mcp_refs_visible_in_seasoned": visibility["seasoned_visible"],
        "mcp_refs_visible_in_ablated": visibility["ablated_visible"],
    }
    for totals in mode_totals.values():
        if totals.get("seasoned", -1) > max(totals.get("baseline", -1), totals.get("ablated", -1)):
            computed["tasks_where_seasoned_won"] += 1
        if totals.get("seasoned", -1) > totals.get("ablated", -1):
            computed["tasks_where_ablation_reduced_quality"] += 1
    computed["seasoned_vs_baseline_delta"] = computed["seasoned_total"] - computed["baseline_total"]
    computed["seasoned_vs_ablated_delta"] = computed["seasoned_total"] - computed["ablated_total"]

    for field, expected in computed.items():
        if aggregate.get(field) != expected:
            errors.append(f"aggregate_results.{field}: expected {expected}, got {aggregate.get(field)}")
        if final.get("aggregate_metrics", {}).get(field) != expected:
            errors.append(f"final_verdict.aggregate_metrics.{field}: expected {expected}, got {final.get('aggregate_metrics', {}).get(field)}")

    verdict = final.get("verdict")
    if verdict not in VALID_FINAL_VERDICTS:
        errors.append(f"final_verdict.verdict: invalid {verdict}")
        return
    overclaiming = positive_overclaim(json.dumps(final, sort_keys=True)) is not None
    expected = expected_verdict(computed, visibility, overclaiming)
    if verdict != expected:
        errors.append(f"final_verdict.verdict: expected {expected}, got {verdict}")


def check_reusable_pool(proof_dir: Path, errors: list[str]) -> None:
    aggregate = load_json(proof_dir / "aggregate_results.json", errors)
    pool = aggregate.get("reusable_lineage_pool") if isinstance(aggregate, dict) else None
    if not isinstance(pool, dict):
        errors.append("aggregate_results missing reusable_lineage_pool")
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


def check_claim_register(proof_dir: Path, errors: list[str]) -> None:
    required_claims = {
        "mcp_seasoned_refs_participated_in_seasoned_mode",
        "ablation_mode_suppressed_mcp_seasoned_refs",
        "seasoned_mode_improved_held_out_tasks",
        "ablation_reduced_quality_on_some_tasks",
        "runtime_visibility_audited",
        "no_promotion_claim",
        "no_generalized_cognition_claim",
        "no_agi_consciousness_or_black_box_solved_claim",
        "reusable_lineage_pool_remained_unchanged",
    }
    register = load_json(proof_dir / "claim_register.json", errors)
    claims = register.get("claims") if isinstance(register, dict) else None
    if not isinstance(claims, list):
        errors.append("claim_register missing claims list")
        return
    seen = {claim.get("id") for claim in claims if isinstance(claim, dict)}
    missing = sorted(required_claims - seen)
    if missing:
        errors.append(f"claim_register missing required claims: {missing}")
    for claim in claims:
        if not isinstance(claim, dict):
            errors.append("claim_register contains non-object claim")
            continue
        for field in ("claim_level", "evidence_refs", "safe_public_wording", "risk_if_overstated"):
            if field not in claim:
                errors.append(f"claim_register.{claim.get('id')}: missing {field}")


def check_text_boundaries(proof_dir: Path, errors: list[str]) -> None:
    combined = ""
    for path in sorted(proof_dir.rglob("*")):
        if path.is_file() and path.suffix in {".md", ".json", ".jsonl"}:
            combined += "\n" + read_text(path, errors)
    overclaim = positive_overclaim(combined)
    if overclaim:
        errors.append(f"positive overclaim detected: {overclaim}")


def validate_mcp_seasoning_ablation(proof_dir: Path) -> list[str]:
    if not proof_dir.is_absolute():
        proof_dir = ROOT / proof_dir

    errors: list[str] = []
    if not proof_dir.is_dir():
        return [f"proof directory not found: {proof_dir}"]

    check_required_files(proof_dir, errors)
    check_hard_gate(proof_dir, errors)
    mode_totals = check_blind_scores(proof_dir, errors)
    visibility = check_mode_artifacts(proof_dir, errors)
    check_final_math(proof_dir, mode_totals, visibility, errors)
    check_reusable_pool(proof_dir, errors)
    check_claim_register(proof_dir, errors)
    check_text_boundaries(proof_dir, errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_mcp_seasoning_ablation.py <proof_dir>", file=sys.stderr)
        return 2

    errors = validate_mcp_seasoning_ablation(Path(argv[1]))
    if errors:
        print("MCP_SEASONING_ABLATION_INVALID")
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("MCP_SEASONING_ABLATION_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
