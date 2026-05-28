#!/usr/bin/env python3
"""Validate Proof 020 extreme operational breakdown gauntlet artifacts."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROOF_ID = "020-extreme-operational-breakdown-gauntlet"

SCENARIO_IDS = [f"scenario_{index:03d}" for index in range(1, 7)]
PROBES = [
    "contradiction preservation",
    "stale authority correction",
    "authority arbitration",
    "omitted-range recovery",
    "replay continuity",
    "recovery stability",
    "temporal validity reconstruction",
    "operational prioritization",
    "hallucination prevention",
    "retry stabilization",
    "replay adequacy",
    "causal continuity",
    "provenance preservation",
    "recovery branch reconstruction",
]
VALID_STATUSES = {"reconstructed", "partially_reconstructed", "unresolved", "unstable"}
STATUS_RANK = {"unstable": 0, "unresolved": 1, "partially_reconstructed": 2, "reconstructed": 3}

REQUIRED_ROOT_FILES = [
    "README.md",
    "gauntlet_design.md",
    "breakdown_taxonomy.md",
    "aggregate_results.json",
    "comparative_breakdown_report.md",
    "recovery_stability_report.md",
    "replay_continuity_report.md",
    "cross_family_operational_patterns.md",
    "claim_register.json",
    "public_lineage_summary.md",
    "final_verdict.json",
    "proof_manifest.json",
]
REQUIRED_SCENARIO_FILES = [
    "scenario_description.md",
    "entropy_event_log.jsonl",
    "baseline_results.json",
    "pond_backed_results.json",
    "contradiction_chain.json",
    "authority_conflicts.json",
    "recovery_trace.jsonl",
    "replay_integrity_results.json",
    "scenario_verdict.json",
    "public_lineage_summary.md",
]
REQUIRED_CONSULT_FILES = [
    "hard_gate_request.json",
    "hard_gate_response.json",
    *[f"{scenario_id}_pond_request.json" for scenario_id in SCENARIO_IDS],
    *[f"{scenario_id}_pond_response.json" for scenario_id in SCENARIO_IDS],
]
REQUIRED_EVENT_TYPES = {
    "long_horizon_operational_sequence",
    "omitted_range_loss",
    "stale_authority_source",
    "contradictory_summaries",
    "retry_divergence",
    "replay_ambiguity",
    "environment_runtime_drift",
    "incomplete_recovery_trace",
    "partial_lineage_corruption",
    "compressed_context_degradation",
    "temporal_validity_conflict",
}
REQUIRED_CONDITIONS = {
    "long-horizon operational sequence",
    "omitted-range loss",
    "stale authority source",
    "contradictory summaries",
    "retry divergence",
    "replay ambiguity",
    "environment/runtime drift",
    "incomplete recovery trace",
    "partial lineage corruption",
    "compressed context degradation",
    "temporal validity conflict",
}
VALID_FINAL_VERDICTS = {
    "EXTREME_OPERATIONAL_ADVANTAGE_OBSERVED",
    "PARTIAL_EXTREME_OPERATIONAL_ADVANTAGE",
    "NO_EXTREME_OPERATIONAL_ADVANTAGE",
    "INVALID_GAUNTLET",
    "FAIL_CLOSED",
}
VALID_SCENARIO_VERDICTS = {
    "EXTREME_SCENARIO_ADVANTAGE",
    "PARTIAL_EXTREME_SCENARIO_ADVANTAGE",
    "NO_EXTREME_SCENARIO_ADVANTAGE",
    "INVALID_SCENARIO",
}
REQUIRED_CLAIM_IDS = {
    "bounded_operational_degradation_scenarios_executed",
    "replay_modes_separated",
    "mcp_seasoned_refs_visible_only_pond",
    "full_lineage_replay_preserved_recovery_structure_bounded",
    "runtime_hashes_recorded",
    "reusable_lineage_pool_unchanged",
    "no_promotion",
    "no_global_superiority",
    "no_agi_consciousness_or_black_box_claim",
    "no_target_system_defect_claim",
}

HASH_RE = re.compile(r"^[a-f0-9]{64}$")
MCP_REF_RE = re.compile(
    r"(artifacts/pond/mcp_seasoned_|MCP_SEASONED_CANDIDATE|fp_lineage_candidate_)",
    re.IGNORECASE,
)
BASELINE_FORBIDDEN_RE = re.compile(
    r"(artifacts/pond/mcp_seasoned_|MCP_SEASONED_CANDIDATE|fp_lineage_candidate_|pressure:[a-f0-9])",
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
    "disallowed",
    "blocked",
    "avoid",
    "forbidden",
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


def load_jsonl(path: Path, errors: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, line in enumerate(read_text(path, errors).splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}:{index}: invalid JSON: {exc}")
            continue
        if not isinstance(value, dict):
            errors.append(f"{path}:{index}: expected object")
            continue
        rows.append(value)
    return rows


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_hash(value: Any) -> bool:
    return isinstance(value, str) and bool(HASH_RE.fullmatch(value))


def has_mcp_ref(value: Any) -> bool:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    return bool(MCP_REF_RE.search(text))


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


def check_runtime_hashes(runtime: Any, label: str, errors: list[str]) -> None:
    if not isinstance(runtime, dict):
        errors.append(f"{label}: missing runtime hashes")
        return
    for field in ("corpus_hash", "runtime_request_hash", "runtime_response_hash"):
        if not is_hash(runtime.get(field)):
            errors.append(f"{label}: missing or invalid {field}")
    if not runtime.get("schema_version"):
        errors.append(f"{label}: missing schema_version")


def probe_statuses(result: dict[str, Any], label: str, errors: list[str]) -> dict[str, str]:
    rows = result.get("probe_results")
    if not isinstance(rows, list):
        errors.append(f"{label}: missing probe_results")
        return {}
    statuses: dict[str, str] = {}
    for row in rows:
        if not isinstance(row, dict):
            errors.append(f"{label}: probe_results contains non-object")
            continue
        probe = row.get("probe")
        status = row.get("status")
        if probe not in PROBES:
            errors.append(f"{label}: unexpected probe {probe}")
            continue
        if status not in VALID_STATUSES:
            errors.append(f"{label}: invalid status for {probe}: {status}")
            continue
        statuses[probe] = status
    missing = [probe for probe in PROBES if probe not in statuses]
    if missing:
        errors.append(f"{label}: missing probes {missing}")
    return statuses


def counts_from_statuses(statuses: dict[str, str], prefix: str) -> dict[str, int]:
    return {
        f"{prefix}_reconstructed": sum(1 for status in statuses.values() if status == "reconstructed"),
        f"{prefix}_partial": sum(1 for status in statuses.values() if status == "partially_reconstructed"),
        f"{prefix}_unresolved": sum(1 for status in statuses.values() if status == "unresolved"),
        f"{prefix}_unstable": sum(1 for status in statuses.values() if status == "unstable"),
    }


def improved(baseline: dict[str, str], pond: dict[str, str], probe: str) -> bool:
    return STATUS_RANK[pond[probe]] > STATUS_RANK[baseline[probe]]


def improvement_count(baseline: dict[str, str], pond: dict[str, str]) -> int:
    return sum(1 for probe in PROBES if STATUS_RANK[pond[probe]] > STATUS_RANK[baseline[probe]])


def check_required_files(proof_dir: Path, errors: list[str]) -> None:
    for relative in REQUIRED_ROOT_FILES:
        if not (proof_dir / relative).is_file():
            errors.append(f"missing required artifact: {relative}")
    if (proof_dir / "FAIL_CLOSED.md").exists():
        errors.append("FAIL_CLOSED.md present after neutral gate pass")

    consult_dir = proof_dir / "inside_voice_consults"
    for relative in REQUIRED_CONSULT_FILES:
        if not (consult_dir / relative).is_file():
            errors.append(f"missing consult artifact: inside_voice_consults/{relative}")

    scenario_root = proof_dir / "scenarios"
    found = {path.name for path in scenario_root.iterdir() if path.is_dir()} if scenario_root.is_dir() else set()
    expected = set(SCENARIO_IDS)
    if found != expected:
        errors.append(f"scenario folders: expected {sorted(expected)}, got {sorted(found)}")
        return
    for scenario_id in SCENARIO_IDS:
        for relative in REQUIRED_SCENARIO_FILES:
            if not (scenario_root / scenario_id / relative).is_file():
                errors.append(f"missing scenario artifact: scenarios/{scenario_id}/{relative}")


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
    if "audit.safe_negated_claim_boundary" not in audit_text:
        errors.append("hard gate missing audit.safe_negated_claim_boundary")
    check_runtime_hashes(response.get("lineage", {}).get("runtime"), "hard gate", errors)


def check_scenarios(proof_dir: Path, errors: list[str]) -> dict[str, Any]:
    metrics: dict[str, Any] = {
        "counts": {
            "baseline_reconstructed": 0,
            "baseline_partial": 0,
            "baseline_unresolved": 0,
            "baseline_unstable": 0,
            "pond_reconstructed": 0,
            "pond_partial": 0,
            "pond_unresolved": 0,
            "pond_unstable": 0,
        },
        "scenario_advantage_count": 0,
        "recovery_stability_improved_scenarios": 0,
        "contradiction_handling_improved_scenarios": 0,
        "authority_arbitration_improved_scenarios": 0,
        "mcp_refs_visible_in_pond_scenarios": 0,
        "mcp_refs_visible_in_baseline_scenarios": 0,
        "misleading_summary_scenarios": 0,
        "stale_runtime_assumption_scenarios": 0,
        "replay_trap_scenarios": 0,
        "fixture_corruption_recovery_scenarios": 0,
    }

    for scenario_id in SCENARIO_IDS:
        sdir = proof_dir / "scenarios" / scenario_id
        baseline = load_json(sdir / "baseline_results.json", errors)
        pond = load_json(sdir / "pond_backed_results.json", errors)
        verdict = load_json(sdir / "scenario_verdict.json", errors)
        chain = load_json(sdir / "contradiction_chain.json", errors)
        conflicts = load_json(sdir / "authority_conflicts.json", errors)
        replay = load_json(sdir / "replay_integrity_results.json", errors)
        consult = load_json(proof_dir / "inside_voice_consults" / f"{scenario_id}_pond_response.json", errors)
        events = load_jsonl(sdir / "entropy_event_log.jsonl", errors)
        recovery_rows = load_jsonl(sdir / "recovery_trace.jsonl", errors)
        if not all(isinstance(item, dict) for item in (baseline, pond, verdict, chain, conflicts, replay, consult)):
            continue

        event_types = {row.get("event_type") for row in events}
        missing_events = sorted(REQUIRED_EVENT_TYPES - event_types)
        if missing_events:
            errors.append(f"{scenario_id}: missing severe event types {missing_events}")

        chains = chain.get("chains")
        if not isinstance(chains, list) or len(chains) < 3:
            errors.append(f"{scenario_id}: expected at least 3 linked contradiction chains")
        elif not all(item.get("linked_to") for item in chains if isinstance(item, dict)):
            errors.append(f"{scenario_id}: contradiction chains must include linked_to")

        authority_conflicts = conflicts.get("conflicts")
        if not isinstance(authority_conflicts, list) or len(authority_conflicts) < 2:
            errors.append(f"{scenario_id}: expected at least 2 authority conflicts")

        failed_branches = [row for row in recovery_rows if row.get("branch_status") == "failed"]
        if not failed_branches:
            errors.append(f"{scenario_id}: expected at least 1 failed recovery branch")

        conditions = verdict.get("breakdown_conditions")
        if not isinstance(conditions, dict) or not REQUIRED_CONDITIONS.issubset({key for key, value in conditions.items() if value is True}):
            errors.append(f"{scenario_id}: missing severe breakdown conditions")
        special = verdict.get("special_conditions", [])
        if "intentionally misleading summaries" in special:
            metrics["misleading_summary_scenarios"] += 1
        if "stale runtime assumptions" in special:
            metrics["stale_runtime_assumption_scenarios"] += 1
        if "replay reconstruction traps" in special:
            metrics["replay_trap_scenarios"] += 1
        if "partial fixture corruption" in special and "recovery after invalid replay attempt" in special:
            metrics["fixture_corruption_recovery_scenarios"] += 1

        baseline_text = json.dumps(baseline, sort_keys=True)
        if BASELINE_FORBIDDEN_RE.search(baseline_text):
            errors.append(f"{scenario_id}: baseline mode cites forbidden MCP-seasoned or pressure ref")
        if baseline.get("mcp_seasoned_refs_visible") is not False:
            errors.append(f"{scenario_id}: baseline mcp_seasoned_refs_visible must be false")
        if has_mcp_ref(baseline):
            metrics["mcp_refs_visible_in_baseline_scenarios"] += 1

        if pond.get("mcp_seasoned_refs_visible") is not True or not has_mcp_ref(pond.get("mcp_seasoned_refs", [])):
            errors.append(f"{scenario_id}: pond-backed mode lacks MCP-seasoned refs")
        else:
            metrics["mcp_refs_visible_in_pond_scenarios"] += 1
        check_runtime_hashes(pond.get("runtime_hashes"), f"{scenario_id} pond results", errors)
        if not pond.get("pressure_ranking_ids"):
            errors.append(f"{scenario_id}: pond-backed pressure rankings missing")

        if consult.get("adapter_status") != "pond_backed":
            errors.append(f"{scenario_id}: consult adapter_status expected pond_backed")
        if consult.get("gate_failures") != []:
            errors.append(f"{scenario_id}: consult gate_failures not empty")
        check_runtime_hashes(consult.get("lineage", {}).get("runtime"), f"{scenario_id} consult", errors)
        if not has_mcp_ref(consult.get("retrieved_artifact_refs", [])):
            errors.append(f"{scenario_id}: consult lacks MCP-seasoned refs")

        baseline_statuses = probe_statuses(baseline, f"{scenario_id} baseline", errors)
        pond_statuses = probe_statuses(pond, f"{scenario_id} pond", errors)
        if set(baseline_statuses) != set(PROBES) or set(pond_statuses) != set(PROBES):
            continue
        baseline_counts = counts_from_statuses(baseline_statuses, "baseline")
        pond_counts = counts_from_statuses(pond_statuses, "pond")
        if baseline.get("counts") != baseline_counts:
            errors.append(f"{scenario_id}: baseline counts mismatch")
        if pond.get("counts") != pond_counts:
            errors.append(f"{scenario_id}: pond counts mismatch")
        for key, value in {**baseline_counts, **pond_counts}.items():
            metrics["counts"][key] += value

        severe = verdict.get("severe_stress_metrics")
        expected_severe = {
            **baseline_counts,
            **pond_counts,
            "recovery_stability_delta": STATUS_RANK[pond_statuses["recovery stability"]]
            - STATUS_RANK[baseline_statuses["recovery stability"]],
            "contradiction_resolution_delta": STATUS_RANK[pond_statuses["contradiction preservation"]]
            - STATUS_RANK[baseline_statuses["contradiction preservation"]],
            "authority_arbitration_delta": STATUS_RANK[pond_statuses["authority arbitration"]]
            - STATUS_RANK[baseline_statuses["authority arbitration"]],
        }
        if severe != expected_severe:
            errors.append(f"{scenario_id}: severe stress metrics mismatch")
        if verdict.get("verdict") not in VALID_SCENARIO_VERDICTS:
            errors.append(f"{scenario_id}: invalid scenario verdict {verdict.get('verdict')}")
        if verdict.get("improvement_count") != improvement_count(baseline_statuses, pond_statuses):
            errors.append(f"{scenario_id}: improvement_count mismatch")
        if improvement_count(baseline_statuses, pond_statuses) > 0:
            metrics["scenario_advantage_count"] += 1
        if improved(baseline_statuses, pond_statuses, "recovery stability"):
            metrics["recovery_stability_improved_scenarios"] += 1
        if improved(baseline_statuses, pond_statuses, "contradiction preservation"):
            metrics["contradiction_handling_improved_scenarios"] += 1
        if improved(baseline_statuses, pond_statuses, "authority arbitration"):
            metrics["authority_arbitration_improved_scenarios"] += 1

        if replay.get("baseline_mcp_ref_leak") is not False:
            errors.append(f"{scenario_id}: replay integrity reports baseline MCP leak")
        if replay.get("pond_mcp_refs_visible") is not True:
            errors.append(f"{scenario_id}: replay integrity missing pond MCP visibility")
        check_runtime_hashes(replay.get("runtime_hashes"), f"{scenario_id} replay integrity", errors)

    if metrics["misleading_summary_scenarios"] < 2:
        errors.append("expected at least 2 scenarios with intentionally misleading summaries")
    if metrics["stale_runtime_assumption_scenarios"] < 2:
        errors.append("expected at least 2 scenarios with stale runtime assumptions")
    if metrics["replay_trap_scenarios"] < 2:
        errors.append("expected at least 2 scenarios with replay reconstruction traps")
    if metrics["fixture_corruption_recovery_scenarios"] < 1:
        errors.append("expected at least 1 scenario with fixture corruption and invalid replay recovery")
    return metrics


def expected_final_verdict(metrics: dict[str, Any], overclaiming: bool) -> str:
    counts = metrics["counts"]
    if overclaiming:
        return "INVALID_GAUNTLET"
    if (
        metrics["scenario_advantage_count"] >= 5
        and counts["pond_reconstructed"] > counts["baseline_reconstructed"] * 2
        and metrics["recovery_stability_improved_scenarios"] >= 5
        and metrics["contradiction_handling_improved_scenarios"] >= 5
        and metrics["authority_arbitration_improved_scenarios"] >= 5
        and metrics["mcp_refs_visible_in_pond_scenarios"] == 6
        and metrics["mcp_refs_visible_in_baseline_scenarios"] == 0
    ):
        return "EXTREME_OPERATIONAL_ADVANTAGE_OBSERVED"
    if metrics["scenario_advantage_count"] > 0:
        return "PARTIAL_EXTREME_OPERATIONAL_ADVANTAGE"
    return "NO_EXTREME_OPERATIONAL_ADVANTAGE"


def check_aggregate_and_final(proof_dir: Path, metrics: dict[str, Any], overclaiming: bool, errors: list[str]) -> None:
    aggregate = load_json(proof_dir / "aggregate_results.json", errors)
    final = load_json(proof_dir / "final_verdict.json", errors)
    if not isinstance(aggregate, dict) or not isinstance(final, dict):
        return
    if aggregate.get("aggregate_counts") != metrics["counts"]:
        errors.append("aggregate_results aggregate_counts mismatch")
    for field in (
        "scenario_advantage_count",
        "recovery_stability_improved_scenarios",
        "contradiction_handling_improved_scenarios",
        "authority_arbitration_improved_scenarios",
        "mcp_refs_visible_in_pond_scenarios",
        "mcp_refs_visible_in_baseline_scenarios",
    ):
        if aggregate.get(field) != metrics[field]:
            errors.append(f"aggregate_results.{field}: expected {metrics[field]}, got {aggregate.get(field)}")
    expected_2x = metrics["counts"]["pond_reconstructed"] > metrics["counts"]["baseline_reconstructed"] * 2
    if aggregate.get("pond_reconstructed_at_least_2x_baseline") != expected_2x:
        errors.append("aggregate_results pond 2x flag mismatch")

    final_metrics = final.get("aggregate_metrics", {})
    expected_final_metrics = {
        **metrics["counts"],
        "scenario_advantage_count": metrics["scenario_advantage_count"],
        "recovery_stability_improved_scenarios": metrics["recovery_stability_improved_scenarios"],
        "contradiction_handling_improved_scenarios": metrics["contradiction_handling_improved_scenarios"],
        "authority_arbitration_improved_scenarios": metrics["authority_arbitration_improved_scenarios"],
        "mcp_refs_visible_in_pond_scenarios": metrics["mcp_refs_visible_in_pond_scenarios"],
        "mcp_refs_visible_in_baseline_scenarios": metrics["mcp_refs_visible_in_baseline_scenarios"],
        "pond_reconstructed_at_least_2x_baseline": expected_2x,
    }
    for key, expected in expected_final_metrics.items():
        if final_metrics.get(key) != expected:
            errors.append(f"final_verdict.aggregate_metrics.{key}: expected {expected}, got {final_metrics.get(key)}")

    verdict = final.get("verdict")
    if verdict not in VALID_FINAL_VERDICTS:
        errors.append(f"final_verdict.verdict: invalid {verdict}")
        return
    expected_verdict = expected_final_verdict(metrics, overclaiming)
    if verdict != expected_verdict:
        errors.append(f"final_verdict.verdict: expected {expected_verdict}, got {verdict}")


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
        if pool_path.exists() and sha256_file(pool_path) != pre_hash:
            errors.append("reusable_lineage_pool current hash differs from recorded proof hash")


def check_claim_register(proof_dir: Path, errors: list[str]) -> None:
    register = load_json(proof_dir / "claim_register.json", errors)
    claims = register.get("claims") if isinstance(register, dict) else None
    if not isinstance(claims, list):
        errors.append("claim_register missing claims list")
        return
    seen = {claim.get("id") for claim in claims if isinstance(claim, dict)}
    missing = sorted(REQUIRED_CLAIM_IDS - seen)
    if missing:
        errors.append(f"claim_register missing required claims: {missing}")
    for claim in claims:
        if not isinstance(claim, dict):
            errors.append("claim_register contains non-object claim")
            continue
        for field in ("claim_level", "evidence_refs", "safe_public_wording", "risk_if_overstated"):
            if field not in claim:
                errors.append(f"claim_register.{claim.get('id')}: missing {field}")


def check_reports(proof_dir: Path, errors: list[str]) -> None:
    replay_report = read_text(proof_dir / "replay_continuity_report.md", errors)
    for phrase in (
        "Were MCP-seasoned refs visible in pond-backed responses?",
        "Were they absent from baseline mode?",
        "Did pressure rankings change under severe entropy?",
        "Did runtime hashes remain deterministic?",
        "Did runtime logs expose seasoned refs?",
        "Did recovery continuity improve?",
        "Visibility classification: `SEASONED_VISIBLE`",
    ):
        if phrase not in replay_report:
            errors.append(f"replay_continuity_report.md missing answer: {phrase}")
    patterns = read_text(proof_dir / "cross_family_operational_patterns.md", errors)
    if "strong_cross_family_pattern" not in patterns:
        errors.append("cross_family_operational_patterns.md missing strong_cross_family_pattern")


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


def validate_extreme_operational_breakdown_gauntlet(proof_dir: Path) -> list[str]:
    if not proof_dir.is_absolute():
        proof_dir = ROOT / proof_dir

    errors: list[str] = []
    if not proof_dir.is_dir():
        return [f"proof directory not found: {proof_dir}"]

    check_required_files(proof_dir, errors)
    check_hard_gate(proof_dir, errors)
    metrics = check_scenarios(proof_dir, errors)
    overclaiming = check_text_boundaries(proof_dir, errors)
    check_aggregate_and_final(proof_dir, metrics, overclaiming, errors)
    check_reusable_pool(proof_dir, errors)
    check_claim_register(proof_dir, errors)
    check_reports(proof_dir, errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_extreme_operational_breakdown_gauntlet.py <proof_dir>", file=sys.stderr)
        return 2

    errors = validate_extreme_operational_breakdown_gauntlet(Path(argv[1]))
    if errors:
        print("EXTREME_OPERATIONAL_BREAKDOWN_INVALID")
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("EXTREME_OPERATIONAL_BREAKDOWN_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
