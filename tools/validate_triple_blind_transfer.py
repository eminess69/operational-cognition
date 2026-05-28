#!/usr/bin/env python3
"""Validate Proof 021 triple-blind transfer evaluation artifacts."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROOF_ID = "021-triple-blind-transfer-evaluation"

TASK_IDS = [f"task_{index:03d}" for index in range(1, 6)]
SOLUTION_LABELS = ["solution_A", "solution_B", "solution_C"]
MODES = ["baseline_visible_only", "pond_backed_ablated", "pond_backed_mcp_seasoned"]
SEASONED_MODE = "pond_backed_mcp_seasoned"
BASELINE_MODE = "baseline_visible_only"
ABLATED_MODE = "pond_backed_ablated"

SCORE_KEYS = [
    "contradiction_preservation",
    "authority_arbitration",
    "operational_prioritization",
    "replayability",
    "uncertainty_discipline",
    "recovery_planning",
    "boundary_control",
    "actionability",
]

REQUIRED_ROOT_FILES = [
    "README.md",
    "blind_protocol.md",
    "task_selection_report.md",
    "mode_mapping_hidden.json",
    "blind_scores.json",
    "revealed_results.json",
    "comparative_blind_report.md",
    "claim_register.json",
    "public_lineage_summary.md",
    "final_verdict.json",
    "proof_manifest.json",
]

VALID_FINAL_VERDICTS = {
    "BLIND_SEASONED_ADVANTAGE_CONFIRMED",
    "PARTIAL_BLIND_SEASONED_ADVANTAGE",
    "NO_BLIND_SEASONED_ADVANTAGE",
    "INVALID_BLIND_TEST",
    "FAIL_CLOSED",
}

REQUIRED_CLAIMS = {
    "five_held_out_tasks_selected",
    "anonymized_solution_labels_used",
    "scorer_had_no_mode_names",
    "blind_scores_written_before_reveal",
    "no_seasoned_refs_in_blind_artifacts",
    "seasoned_first_or_tied_on_at_least_four_tasks",
    "seasoned_aggregate_exceeded_controls",
    "no_overclaiming",
}

REUSED_TASK_TITLES = {
    "planning decomposition",
    "resource allocation",
    "architecture arbitration",
    "degraded validation pipeline triage",
    "conflicting architecture migration plan",
    "partial provenance recovery",
    "constrained operational planning under stale assumptions",
    "validator replay with omitted checkpoint range",
    "runtime migration with misleading visible summary",
    "redaction provenance recovery trap",
    "compressed fixture corruption and invalid replay recovery",
    "external evaluation pack with stale authority",
    "release recovery handoff with runtime drift",
}

HASH_RE = re.compile(r"^[a-f0-9]{64}$")
MCP_REF_RE = re.compile(
    r"(MCP_SEASONED_CANDIDATE|artifacts/pond/mcp_seasoned_|mcp[-_ ]seasoned)",
    re.IGNORECASE,
)
BLIND_SOURCE_LEAK_RE = re.compile(
    r"(baseline_visible_only|pond_backed|pond-backed|pond backed|visible-only|visible only|"
    r"pond_backed_ablated|pond_backed_mcp_seasoned|mcp[-_ ]seasoned|ablated|seasoned|"
    r"MCP_SEASONED_CANDIDATE|artifacts/pond/mcp_seasoned_|inside_voice_consults)",
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
        r".{0,90}\b(agi|artificial general intelligence|consciousness|black[-_ ]box[-_ ]solv(?:ed|ing)|autonomous cognition)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(agi|artificial general intelligence|consciousness|black[-_ ]box[-_ ]solv(?:ed|ing)|autonomous cognition)\b"
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


def parse_timestamp(value: Any, label: str, errors: list[str]) -> datetime | None:
    if not isinstance(value, str):
        errors.append(f"{label}: missing timestamp")
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{label}: invalid timestamp {value!r}")
        return None


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


def check_required_files(proof_dir: Path, errors: list[str]) -> None:
    for relative in REQUIRED_ROOT_FILES:
        if not (proof_dir / relative).is_file():
            errors.append(f"missing required artifact: {relative}")

    anon_root = proof_dir / "anonymized_outputs"
    if not anon_root.is_dir():
        errors.append("missing required artifact: anonymized_outputs/")
        return
    found = {path.name for path in anon_root.iterdir() if path.is_dir()}
    expected = set(TASK_IDS)
    if found != expected:
        errors.append(f"anonymized task folders: expected {sorted(expected)}, got {sorted(found)}")
        return
    for task_id in TASK_IDS:
        task_dir = anon_root / task_id
        for relative in ["task_prompt.md", *[f"{label}.md" for label in SOLUTION_LABELS]]:
            path = task_dir / relative
            if not path.is_file():
                errors.append(f"missing anonymized artifact: anonymized_outputs/{task_id}/{relative}")
            elif not read_text(path, errors).strip():
                errors.append(f"empty anonymized artifact: anonymized_outputs/{task_id}/{relative}")


def check_blind_artifact_leaks(proof_dir: Path, errors: list[str]) -> bool:
    leak_found = False
    blind_paths = [proof_dir / "blind_scores.json", *sorted((proof_dir / "anonymized_outputs").rglob("*.md"))]
    for path in blind_paths:
        if not path.is_file():
            continue
        text = read_text(path, errors)
        match = BLIND_SOURCE_LEAK_RE.search(text)
        if match:
            errors.append(f"{path.relative_to(proof_dir)}: blind artifact contains source-identifying text {match.group(0)!r}")
            leak_found = True
    return leak_found


def score_total(score: dict[str, Any], path: str, errors: list[str]) -> int | None:
    total = 0
    for key in SCORE_KEYS:
        value = score.get(key)
        if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 5:
            errors.append(f"{path}: invalid score field {key}")
            return None
        total += value
    return total


def check_blind_scores(proof_dir: Path, errors: list[str]) -> dict[str, dict[str, int]]:
    blind = load_json(proof_dir / "blind_scores.json", errors)
    label_totals: dict[str, dict[str, int]] = {}
    if not isinstance(blind, dict):
        return label_totals

    if blind.get("proof_id") != PROOF_ID:
        errors.append(f"blind_scores.proof_id: expected {PROOF_ID}, got {blind.get('proof_id')}")
    if blind.get("labels_scored") != SOLUTION_LABELS:
        errors.append("blind_scores.labels_scored: expected solution_A/B/C")
    if blind.get("mode_mapping_included") is not False:
        errors.append("blind_scores.mode_mapping_included: expected false")
    for forbidden_field in ("mode_mapping", "reveal_mapping", "source_modes"):
        if forbidden_field in blind:
            errors.append(f"blind_scores: forbidden field {forbidden_field}")

    tasks = blind.get("tasks")
    if not isinstance(tasks, dict):
        errors.append("blind_scores.tasks: missing object")
        return label_totals
    if set(tasks) != set(TASK_IDS):
        errors.append(f"blind_scores.tasks: expected {TASK_IDS}, got {sorted(tasks)}")
        return label_totals

    for task_id in TASK_IDS:
        task = tasks.get(task_id)
        if not isinstance(task, dict):
            errors.append(f"blind_scores.{task_id}: expected object")
            continue
        results = task.get("results")
        if not isinstance(results, dict) or set(results) != set(SOLUTION_LABELS):
            errors.append(f"blind_scores.{task_id}.results: expected solution_A/B/C")
            continue
        totals: dict[str, int] = {}
        for label in SOLUTION_LABELS:
            entry = results.get(label)
            if not isinstance(entry, dict) or not isinstance(entry.get("scores"), dict):
                errors.append(f"blind_scores.{task_id}.{label}: missing scores")
                continue
            total = score_total(entry["scores"], f"blind_scores.{task_id}.{label}", errors)
            if total is None:
                continue
            if entry.get("total_score") != total:
                errors.append(f"blind_scores.{task_id}.{label}.total_score: expected {total}, got {entry.get('total_score')}")
            totals[label] = total
        if set(totals) == set(SOLUTION_LABELS):
            max_total = max(totals.values())
            for label, total in totals.items():
                greater = {value for value in totals.values() if value > total}
                expected_rank = len(greater) + 1
                rank = results[label].get("rank")
                if rank != expected_rank:
                    errors.append(f"blind_scores.{task_id}.{label}.rank: expected {expected_rank}, got {rank}")
                expected_first = total == max_total
                if results[label].get("first_place_tied") is not expected_first:
                    errors.append(f"blind_scores.{task_id}.{label}.first_place_tied: expected {expected_first}")
            label_totals[task_id] = totals

    return label_totals


def check_mapping(
    proof_dir: Path,
    blind_hash: str,
    label_totals: dict[str, dict[str, int]],
    errors: list[str],
) -> tuple[dict[str, dict[str, str]], bool]:
    mapping_artifact = load_json(proof_dir / "mode_mapping_hidden.json", errors)
    mappings: dict[str, dict[str, str]] = {}
    sequence_valid = False
    if not isinstance(mapping_artifact, dict):
        return mappings, sequence_valid

    if mapping_artifact.get("proof_id") != PROOF_ID:
        errors.append(f"mode_mapping_hidden.proof_id: expected {PROOF_ID}, got {mapping_artifact.get('proof_id')}")
    if mapping_artifact.get("available_to_scorer_before_lock") is not False:
        errors.append("mode_mapping_hidden.available_to_scorer_before_lock: expected false")
    if mapping_artifact.get("blind_scores_sha256") != blind_hash:
        errors.append("mode_mapping_hidden.blind_scores_sha256 mismatch")

    locked_at = parse_timestamp(mapping_artifact.get("blind_scores_locked_at"), "mode_mapping_hidden.blind_scores_locked_at", errors)
    revealed_at = parse_timestamp(mapping_artifact.get("mapping_revealed_at"), "mode_mapping_hidden.mapping_revealed_at", errors)
    if locked_at and revealed_at:
        sequence_valid = revealed_at > locked_at and mapping_artifact.get("mapping_revealed_after_blind_scores") is True
        if not sequence_valid:
            errors.append("mode_mapping_hidden: mapping reveal must be after blind score lock")

    tasks = mapping_artifact.get("tasks")
    if not isinstance(tasks, dict) or set(tasks) != set(TASK_IDS):
        errors.append(f"mode_mapping_hidden.tasks: expected {TASK_IDS}")
        return mappings, sequence_valid

    for task_id in TASK_IDS:
        task = tasks.get(task_id)
        if not isinstance(task, dict):
            errors.append(f"mode_mapping_hidden.{task_id}: expected object")
            continue
        title = task.get("title")
        if not isinstance(title, str) or not title.strip():
            errors.append(f"mode_mapping_hidden.{task_id}.title: missing title")
        elif title.lower().strip() in REUSED_TASK_TITLES:
            errors.append(f"{task_id}: task title reuses Proofs 018-020 task {title!r}")

        mapping = task.get("label_to_mode")
        if not isinstance(mapping, dict) or set(mapping) != set(SOLUTION_LABELS) or set(mapping.values()) != set(MODES):
            errors.append(f"mode_mapping_hidden.{task_id}.label_to_mode: invalid mapping")
            continue
        mappings[task_id] = dict(mapping)

        refs = task.get("source_refs_by_mode")
        if not isinstance(refs, dict):
            errors.append(f"mode_mapping_hidden.{task_id}.source_refs_by_mode: missing object")
            continue
        seasoned_refs = refs.get(SEASONED_MODE)
        ablated_refs = refs.get(ABLATED_MODE)
        baseline_refs = refs.get(BASELINE_MODE)
        if not isinstance(seasoned_refs, list) or not any(MCP_REF_RE.search(str(ref)) for ref in seasoned_refs):
            errors.append(f"mode_mapping_hidden.{task_id}: missing MCP-seasoned refs for seasoned mode")
        if any(MCP_REF_RE.search(str(ref)) for ref in (ablated_refs if isinstance(ablated_refs, list) else [])):
            errors.append(f"mode_mapping_hidden.{task_id}: MCP-seasoned refs present in ablated mode")
        if any(MCP_REF_RE.search(str(ref)) for ref in (baseline_refs if isinstance(baseline_refs, list) else [])):
            errors.append(f"mode_mapping_hidden.{task_id}: MCP-seasoned refs present in baseline mode")

    if set(mappings) == set(label_totals):
        for task_id, totals in label_totals.items():
            mapped_labels = mappings[task_id]
            if set(mapped_labels) != set(totals):
                errors.append(f"{task_id}: blind labels and mapping labels differ")

    return mappings, sequence_valid


def compute_revealed(
    label_totals: dict[str, dict[str, int]],
    mappings: dict[str, dict[str, str]],
) -> tuple[dict[str, dict[str, Any]], dict[str, int]]:
    task_results: dict[str, dict[str, Any]] = {}
    aggregate = {
        "baseline_visible_only_total": 0,
        "pond_backed_ablated_total": 0,
        "pond_backed_mcp_seasoned_total": 0,
        "seasoned_first_or_tied_tasks": 0,
    }
    for task_id in TASK_IDS:
        if task_id not in label_totals or task_id not in mappings:
            continue
        mode_totals = {mode: 0 for mode in MODES}
        label_results: dict[str, dict[str, Any]] = {}
        for label, total in label_totals[task_id].items():
            mode = mappings[task_id][label]
            mode_totals[mode] = total
            label_results[label] = {"mode": mode, "total_score": total}
        max_total = max(mode_totals.values())
        winner_modes = sorted(mode for mode, total in mode_totals.items() if total == max_total)
        if SEASONED_MODE in winner_modes:
            aggregate["seasoned_first_or_tied_tasks"] += 1
        aggregate["baseline_visible_only_total"] += mode_totals[BASELINE_MODE]
        aggregate["pond_backed_ablated_total"] += mode_totals[ABLATED_MODE]
        aggregate["pond_backed_mcp_seasoned_total"] += mode_totals[SEASONED_MODE]
        task_results[task_id] = {
            "labels": label_results,
            "mode_totals": mode_totals,
            "winner_modes": winner_modes,
        }
    aggregate["seasoned_vs_baseline_delta"] = (
        aggregate["pond_backed_mcp_seasoned_total"] - aggregate["baseline_visible_only_total"]
    )
    aggregate["seasoned_vs_ablated_delta"] = (
        aggregate["pond_backed_mcp_seasoned_total"] - aggregate["pond_backed_ablated_total"]
    )
    return task_results, aggregate


def check_revealed_results(
    proof_dir: Path,
    blind_hash: str,
    mapping_hash: str,
    expected_tasks: dict[str, dict[str, Any]],
    expected_aggregate: dict[str, int],
    errors: list[str],
) -> None:
    revealed = load_json(proof_dir / "revealed_results.json", errors)
    if not isinstance(revealed, dict):
        return
    if revealed.get("proof_id") != PROOF_ID:
        errors.append(f"revealed_results.proof_id: expected {PROOF_ID}, got {revealed.get('proof_id')}")
    if revealed.get("blind_scores_sha256") != blind_hash:
        errors.append("revealed_results.blind_scores_sha256 mismatch")
    if revealed.get("mode_mapping_hidden_sha256") != mapping_hash:
        errors.append("revealed_results.mode_mapping_hidden_sha256 mismatch")
    if revealed.get("mapping_revealed_after_blind_scores") is not True:
        errors.append("revealed_results.mapping_revealed_after_blind_scores: expected true")
    if revealed.get("task_results") != expected_tasks:
        errors.append("revealed_results.task_results: does not match blind scores plus mapping")
    if revealed.get("aggregate") != expected_aggregate:
        errors.append("revealed_results.aggregate: does not match blind scores plus mapping")


def expected_verdict(aggregate: dict[str, int], leak_found: bool, sequence_valid: bool, overclaiming: bool) -> str:
    if leak_found or not sequence_valid or overclaiming:
        return "INVALID_BLIND_TEST"
    seasoned_total = aggregate.get("pond_backed_mcp_seasoned_total", 0)
    baseline_total = aggregate.get("baseline_visible_only_total", 0)
    ablated_total = aggregate.get("pond_backed_ablated_total", 0)
    if (
        aggregate.get("seasoned_first_or_tied_tasks", 0) >= 4
        and seasoned_total > baseline_total
        and seasoned_total > ablated_total
    ):
        return "BLIND_SEASONED_ADVANTAGE_CONFIRMED"
    if aggregate.get("seasoned_first_or_tied_tasks", 0) >= 3 or seasoned_total > baseline_total or seasoned_total > ablated_total:
        return "PARTIAL_BLIND_SEASONED_ADVANTAGE"
    return "NO_BLIND_SEASONED_ADVANTAGE"


def check_claim_register(proof_dir: Path, errors: list[str]) -> None:
    register = load_json(proof_dir / "claim_register.json", errors)
    claims = register.get("claims") if isinstance(register, dict) else None
    if not isinstance(claims, list):
        errors.append("claim_register missing claims list")
        return
    seen = {claim.get("id") for claim in claims if isinstance(claim, dict)}
    missing = sorted(REQUIRED_CLAIMS - seen)
    if missing:
        errors.append(f"claim_register missing required claims: {missing}")
    for claim in claims:
        if not isinstance(claim, dict):
            errors.append("claim_register contains non-object claim")
            continue
        for field in ("claim_level", "evidence_refs", "safe_public_wording", "risk_if_overstated"):
            if field not in claim:
                errors.append(f"claim_register.{claim.get('id')}: missing {field}")


def check_final_verdict(
    proof_dir: Path,
    aggregate: dict[str, int],
    leak_found: bool,
    sequence_valid: bool,
    overclaiming: bool,
    errors: list[str],
) -> None:
    final = load_json(proof_dir / "final_verdict.json", errors)
    if not isinstance(final, dict):
        return
    verdict = final.get("verdict")
    if verdict not in VALID_FINAL_VERDICTS:
        errors.append(f"final_verdict.verdict: invalid {verdict}")
        return

    if final.get("allowed_verdicts") != sorted(VALID_FINAL_VERDICTS):
        errors.append("final_verdict.allowed_verdicts: does not match allowed verdict set")
    if final.get("aggregate_metrics") != aggregate:
        errors.append("final_verdict.aggregate_metrics: does not match computed aggregate")

    criteria = final.get("criteria")
    if not isinstance(criteria, dict):
        errors.append("final_verdict.criteria: missing object")
    else:
        expected_criteria = {
            "seasoned_wins_or_ties_first_on_at_least_4_of_5_tasks": aggregate.get("seasoned_first_or_tied_tasks", 0) >= 4,
            "seasoned_aggregate_gt_baseline": aggregate.get("pond_backed_mcp_seasoned_total", 0)
            > aggregate.get("baseline_visible_only_total", 0),
            "seasoned_aggregate_gt_ablated": aggregate.get("pond_backed_mcp_seasoned_total", 0)
            > aggregate.get("pond_backed_ablated_total", 0),
            "no_mcp_seasoned_refs_leaked_into_blind_scoring_files": not leak_found,
            "blind_scores_written_before_mapping_reveal": sequence_valid,
            "no_overclaiming": not overclaiming,
        }
        for key, expected in expected_criteria.items():
            if criteria.get(key) is not expected:
                errors.append(f"final_verdict.criteria.{key}: expected {expected}, got {criteria.get(key)}")

    boundary = final.get("claim_boundary")
    if not isinstance(boundary, str) or "bounded" not in boundary.lower():
        errors.append("final_verdict.claim_boundary must explicitly remain bounded")
    if not isinstance(final.get("scope_limitations"), list) or not final["scope_limitations"]:
        errors.append("final_verdict.scope_limitations: missing non-empty list")

    expected = expected_verdict(aggregate, leak_found, sequence_valid, overclaiming)
    if verdict != expected:
        errors.append(f"final_verdict.verdict: expected {expected}, got {verdict}")


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


def validate_triple_blind_transfer(proof_dir: Path) -> list[str]:
    if not proof_dir.is_absolute():
        proof_dir = ROOT / proof_dir

    errors: list[str] = []
    if not proof_dir.is_dir():
        return [f"proof directory not found: {proof_dir}"]

    check_required_files(proof_dir, errors)
    leak_found = check_blind_artifact_leaks(proof_dir, errors)
    label_totals = check_blind_scores(proof_dir, errors)

    blind_path = proof_dir / "blind_scores.json"
    mapping_path = proof_dir / "mode_mapping_hidden.json"
    blind_hash = sha256_file(blind_path) if blind_path.is_file() else ""
    mapping_hash = sha256_file(mapping_path) if mapping_path.is_file() else ""

    mappings, sequence_valid = check_mapping(proof_dir, blind_hash, label_totals, errors)
    expected_tasks, aggregate = compute_revealed(label_totals, mappings)
    check_revealed_results(proof_dir, blind_hash, mapping_hash, expected_tasks, aggregate, errors)
    overclaiming = check_text_boundaries(proof_dir, errors)
    check_claim_register(proof_dir, errors)
    check_final_verdict(proof_dir, aggregate, leak_found, sequence_valid, overclaiming, errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_triple_blind_transfer.py <proof_dir>", file=sys.stderr)
        return 2

    errors = validate_triple_blind_transfer(Path(argv[1]))
    if errors:
        print("TRIPLE_BLIND_TRANSFER_INVALID")
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("TRIPLE_BLIND_TRANSFER_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
