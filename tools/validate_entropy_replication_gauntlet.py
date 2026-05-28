#!/usr/bin/env python3
"""Validate Proof 017 entropy replication gauntlet artifacts."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROOF_ID = "017-entropy-replication-gauntlet"

PROBES = [
    "contradiction preservation",
    "stale assumption correction",
    "authority reconstruction",
    "omitted-range recovery",
    "recovery-loop reconstruction",
    "temporal validity reconstruction",
    "environment dependency reconstruction",
    "replay adequacy",
    "operational continuity",
    "hallucination prevention",
    "reconstruction drift",
    "provenance completeness",
]

REQUIRED_ROOT_FILES = [
    "README.md",
    "gauntlet_design.md",
    "scenario_selection_report.md",
    "blind_pack_design.md",
    "external_replication_plan.md",
    "aggregate_results.json",
    "comparative_entropy_report.md",
    "blinded_evaluation_report.md",
    "claim_register.json",
    "public_lineage_summary.md",
    "final_verdict.json",
    "proof_manifest.json",
]

REQUIRED_SCENARIO_FILES = [
    "entropy_scenario.md",
    "baseline_visible_only_results.json",
    "pond_backed_results.json",
    "entropy_event_log.jsonl",
    "contradiction_chain.json",
    "recovery_trace.jsonl",
    "environment_refs.json",
    "replay_integrity_results.json",
    "scenario_verdict.json",
    "public_lineage_summary.md",
]

REQUIRED_BLIND_FILES = [
    "blind_inputs.json",
    "blind_expected_hidden.json",
    "blind_scorer.py",
    "blind_results.json",
    "README.md",
]

REQUIRED_CONSULT_RESPONSES = [
    "hard_gate_response.json",
    "scenario_selection_response.json",
    "contradiction_arbitration_response.json",
    "stale_assumption_detection_response.json",
    "recovery_reconstruction_response.json",
    "replay_adequacy_response.json",
    "final_claim_boundary_audit_response.json",
]

REQUIRED_DOMAINS = {
    "proof/validator repair",
    "config/runtime migration",
    "redaction/provenance audit",
    "fixture minimization or compression recovery",
    "external evaluator or blinded pack preparation",
}

REQUIRED_CLAIM_IDS = {
    "claim.pond_backed_runtime_participated",
    "claim.five_entropy_scenarios_tested",
    "claim.scenario_independence_preserved",
    "claim.replay_modes_separated",
    "claim.blinded_pack_created",
    "claim.aggregate_verdict_bounded",
    "claim.no_global_superiority_claim",
    "claim.no_agi_consciousness_black_box_claim",
    "claim.no_target_system_defect_claim",
    "claim.unresolved_questions_preserved",
}

VALID_STATUSES = {"reconstructed", "partially_reconstructed", "unresolved"}
VALID_SCENARIO_VERDICTS = {
    "ENTROPY_SCENARIO_ADVANTAGE",
    "PARTIAL_ENTROPY_SCENARIO_ADVANTAGE",
    "NO_ENTROPY_SCENARIO_ADVANTAGE",
    "INVALID_SCENARIO",
}
VALID_FINAL_VERDICTS = {
    "ENTROPY_REPLICATION_ADVANTAGE_OBSERVED",
    "PARTIAL_ENTROPY_REPLICATION_ADVANTAGE",
    "NO_ENTROPY_REPLICATION_ADVANTAGE",
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
STATUS_RANK = {"unresolved": 0, "partially_reconstructed": 1, "reconstructed": 2}
HASH_RE = re.compile(r"^[a-f0-9]{64}$")

OVERCLAIM_PATTERNS = [
    re.compile(r"\bglobally superior\b", re.IGNORECASE),
    re.compile(r"\buniversal superiority\b", re.IGNORECASE),
    re.compile(
        r"\b(validates|validated|proves|proven|demonstrates|demonstrated|confirms|confirmed|observes|observed|shows|showed|is)\b"
        r".{0,80}\bglobal[-_ ]superiority\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bglobal[-_ ]superiority\b.{0,80}"
        r"\b(validates|validated|proves|proven|demonstrates|demonstrated|confirms|confirmed|observes|observed|shown|true|made)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(validates|validated|proves|proven|demonstrates|demonstrated|confirms|confirmed|achieves|achieved)\b"
        r".{0,90}\b(agi|artificial general intelligence|consciousness|universal cognition|autonomous intelligence|black[-_ ]box[-_ ]solv(?:ed|ing))\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(agi|artificial general intelligence|consciousness|universal cognition|autonomous intelligence|black[-_ ]box[-_ ]solv(?:ed|ing))\b"
        r".{0,90}\b(validates|validated|proves|proven|demonstrates|demonstrated|confirms|confirmed|achieves|achieved)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(validates|validated|proves|proven|demonstrates|demonstrated|confirms|confirmed|observes|observed|diagnoses|diagnosed)\b"
        r".{0,90}\btarget[-_ ]system[-_ ]defect\b",
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
    "excludes",
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
    records = []
    for index, line in enumerate(read_text(path, errors).splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{path}:{index}: invalid JSON: {exc}")
            continue
        if not isinstance(record, dict):
            errors.append(f"{path}:{index}: expected object")
            continue
        records.append(record)
    return records


def is_hash(value: Any) -> bool:
    return isinstance(value, str) and bool(HASH_RE.fullmatch(value))


def counts_from_results(results: dict[str, str], prefix: str) -> dict[str, int]:
    return {
        f"{prefix}_reconstructed": sum(1 for value in results.values() if value == "reconstructed"),
        f"{prefix}_partial": sum(1 for value in results.values() if value == "partially_reconstructed"),
        f"{prefix}_unresolved": sum(1 for value in results.values() if value == "unresolved"),
    }


def improvement_count(baseline: dict[str, str], pond: dict[str, str]) -> int:
    return sum(1 for probe in PROBES if STATUS_RANK[pond[probe]] > STATUS_RANK[baseline[probe]])


def probe_improved(baseline: dict[str, str], pond: dict[str, str], probe: str) -> bool:
    return STATUS_RANK[pond[probe]] > STATUS_RANK[baseline[probe]]


def positive_overclaim(text: str) -> str | None:
    for pattern in OVERCLAIM_PATTERNS:
        for match in pattern.finditer(text):
            prefix_window = text[max(0, match.start() - 160) : match.start()].lower()
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


def check_required_files(proof_dir: Path, errors: list[str]) -> None:
    for relative in REQUIRED_ROOT_FILES:
        if not (proof_dir / relative).is_file():
            errors.append(f"missing required artifact: {relative}")
    if (proof_dir / "FAIL_CLOSED.md").exists():
        errors.append("FAIL_CLOSED.md present after passing gate")

    scenario_root = proof_dir / "scenarios"
    expected = {f"scenario_{index:03d}" for index in range(1, 6)}
    found = {path.name for path in scenario_root.iterdir() if path.is_dir()} if scenario_root.is_dir() else set()
    if found != expected:
        errors.append(f"scenario folders: expected {sorted(expected)}, got {sorted(found)}")
        return
    for scenario_id in sorted(expected):
        for relative in REQUIRED_SCENARIO_FILES:
            if not (scenario_root / scenario_id / relative).is_file():
                errors.append(f"missing scenario artifact: scenarios/{scenario_id}/{relative}")

    blind_dir = proof_dir / "blind_pack"
    for relative in REQUIRED_BLIND_FILES:
        if not (blind_dir / relative).is_file():
            errors.append(f"missing blind pack artifact: blind_pack/{relative}")


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
    if "BROAD_UNSUPPORTED_CLAIM_BLOCKED" in json.dumps(doc, sort_keys=True):
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
    for response in REQUIRED_CONSULT_RESPONSES:
        path = consult_dir / response
        if not path.is_file():
            errors.append(f"missing Inside Voice response artifact: inside_voice_consults/{response}")
            continue
        check_consult_response(load_json(path, errors), response, errors)


def parse_probe_results(doc: Any, prefix: str, scenario_id: str, errors: list[str]) -> dict[str, str]:
    if not isinstance(doc, dict):
        errors.append(f"{scenario_id}.{prefix}: expected object")
        return {}
    rows = doc.get("probe_results")
    if not isinstance(rows, list):
        errors.append(f"{scenario_id}.{prefix}.probe_results: expected array")
        return {}
    results: dict[str, str] = {}
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"{scenario_id}.{prefix}.probe_results[{index}]: expected object")
            continue
        probe = row.get("probe")
        status = row.get("status")
        if probe not in PROBES:
            errors.append(f"{scenario_id}.{prefix}.probe_results[{index}].probe: invalid {probe}")
            continue
        if status not in VALID_STATUSES:
            errors.append(f"{scenario_id}.{prefix}.probe_results[{index}].status: invalid {status}")
            continue
        if probe in results:
            errors.append(f"{scenario_id}.{prefix}.probe_results: duplicate probe {probe}")
        results[probe] = status
    missing = set(PROBES) - set(results)
    if missing:
        errors.append(f"{scenario_id}.{prefix}.probe_results: missing probes {sorted(missing)}")
    return results


def check_mode_separation(baseline: Any, pond: Any, scenario_id: str, errors: list[str]) -> None:
    if isinstance(baseline, dict):
        if baseline.get("mode") != "visible_only":
            errors.append(f"{scenario_id}.baseline.mode: expected visible_only")
        false_fields = [
            "lineage_refs_used",
            "runtime_hashes_used",
            "pressure_rankings_used",
            "contradiction_refs_used",
            "authority_refs_used",
            "omitted_range_refs_used",
            "recovery_refs_used",
            "inside_voice_guidance_used",
        ]
        for field in false_fields:
            if baseline.get(field) is not False:
                errors.append(f"{scenario_id}.baseline.{field}: expected false")
    if isinstance(pond, dict):
        if pond.get("mode") != "pond_backed_full_lineage":
            errors.append(f"{scenario_id}.pond.mode: expected pond_backed_full_lineage")
        true_fields = [
            "lineage_refs_used",
            "runtime_hashes_used",
            "pressure_rankings_used",
            "contradiction_refs_used",
            "authority_refs_used",
            "temporal_refs_used",
            "omitted_range_refs_used",
            "recovery_refs_used",
            "inside_voice_guidance_used",
            "stage_reports_used",
            "provenance_manifests_used",
        ]
        for field in true_fields:
            if pond.get(field) is not True:
                errors.append(f"{scenario_id}.pond.{field}: expected true")


def check_entropy_event_log(path: Path, scenario_id: str, errors: list[str]) -> None:
    records = load_jsonl(path, errors)
    if len(records) < 16:
        errors.append(f"{scenario_id}.entropy_event_log: expected at least 16 events")
    pressures = {str(record.get("entropy_pressure", "")) for record in records}
    event_types = {str(record.get("event_type", "")) for record in records}
    required_pressures = {
        "long_horizon_sequence",
        "compressed_context_boundary",
        "omitted_range",
        "stale_assumption",
        "contradiction_chain",
        "retry_recovery_loop",
        "environment_runtime_dependency",
        "partial_lineage_loss",
        "competing_authority_sources",
        "summary_degradation_pressure",
        "replay_reconstruction_challenge",
    }
    missing = {pressure for pressure in required_pressures if pressure not in pressures}
    if missing:
        errors.append(f"{scenario_id}.entropy_event_log: missing entropy pressures {sorted(missing)}")
    if sum(1 for record in records if record.get("event_type") == "contradiction") < 2:
        errors.append(f"{scenario_id}.entropy_event_log: expected at least two contradiction events")
    if "retry_recovery_loop" not in event_types:
        errors.append(f"{scenario_id}.entropy_event_log: missing retry_recovery_loop event")


def expected_scenario_verdict(baseline: dict[str, str], pond: dict[str, str]) -> str:
    improved = improvement_count(baseline, pond)
    required = [
        "contradiction preservation",
        "recovery-loop reconstruction",
        "replay adequacy",
    ]
    if improved >= 6 and all(probe_improved(baseline, pond, probe) for probe in required):
        if counts_from_results(pond, "pond")["pond_reconstructed"] > counts_from_results(baseline, "baseline")["baseline_reconstructed"]:
            return "ENTROPY_SCENARIO_ADVANTAGE"
        return "PARTIAL_ENTROPY_SCENARIO_ADVANTAGE"
    if improved:
        return "PARTIAL_ENTROPY_SCENARIO_ADVANTAGE"
    return "NO_ENTROPY_SCENARIO_ADVANTAGE"


def check_scenario(path: Path, errors: list[str]) -> dict[str, Any] | None:
    scenario_id = path.name
    baseline_doc = load_json(path / "baseline_visible_only_results.json", errors)
    pond_doc = load_json(path / "pond_backed_results.json", errors)
    chain_doc = load_json(path / "contradiction_chain.json", errors)
    env_doc = load_json(path / "environment_refs.json", errors)
    integrity_doc = load_json(path / "replay_integrity_results.json", errors)
    verdict_doc = load_json(path / "scenario_verdict.json", errors)

    check_entropy_event_log(path / "entropy_event_log.jsonl", scenario_id, errors)
    recovery_records = load_jsonl(path / "recovery_trace.jsonl", errors)
    if len(recovery_records) < 3:
        errors.append(f"{scenario_id}.recovery_trace: expected retry/recovery records")

    baseline = parse_probe_results(baseline_doc, "baseline", scenario_id, errors)
    pond = parse_probe_results(pond_doc, "pond", scenario_id, errors)
    check_mode_separation(baseline_doc, pond_doc, scenario_id, errors)
    if set(baseline) != set(PROBES) or set(pond) != set(PROBES):
        return None

    if not isinstance(chain_doc, dict):
        errors.append(f"{scenario_id}.contradiction_chain: expected object")
    else:
        contradictions = chain_doc.get("contradictions")
        if not isinstance(contradictions, list) or len(contradictions) < 2:
            errors.append(f"{scenario_id}.contradiction_chain.contradictions: expected at least two")
        if chain_doc.get("contradiction_count") != len(contradictions or []):
            errors.append(f"{scenario_id}.contradiction_chain.contradiction_count: mismatch")

    if not isinstance(env_doc, dict):
        errors.append(f"{scenario_id}.environment_refs: expected object")
    else:
        for field in ("environment_dependency", "partial_lineage_loss", "deterministic_hash"):
            if not env_doc.get(field):
                errors.append(f"{scenario_id}.environment_refs.{field}: expected value")
        if not is_hash(env_doc.get("deterministic_hash")):
            errors.append(f"{scenario_id}.environment_refs.deterministic_hash: expected sha256")
        if not isinstance(env_doc.get("competing_authority_sources"), list) or len(env_doc["competing_authority_sources"]) < 2:
            errors.append(f"{scenario_id}.environment_refs.competing_authority_sources: expected at least two")
        if env_doc.get("runtime_dependency") is not True:
            errors.append(f"{scenario_id}.environment_refs.runtime_dependency: expected true")

    expected_counts = {**counts_from_results(baseline, "baseline"), **counts_from_results(pond, "pond")}
    improved = improvement_count(baseline, pond)
    if not isinstance(verdict_doc, dict):
        errors.append(f"{scenario_id}.scenario_verdict: expected object")
        return None
    for key, value in expected_counts.items():
        if verdict_doc.get(key) != value:
            errors.append(f"{scenario_id}.scenario_verdict.{key}: expected {value}, got {verdict_doc.get(key)}")
    if verdict_doc.get("improvement_count") != improved:
        errors.append(f"{scenario_id}.scenario_verdict.improvement_count: expected {improved}")
    if verdict_doc.get("scenario_verdict") not in VALID_SCENARIO_VERDICTS:
        errors.append(f"{scenario_id}.scenario_verdict.scenario_verdict: invalid")
    else:
        expected = expected_scenario_verdict(baseline, pond)
        if verdict_doc["scenario_verdict"] != expected:
            errors.append(f"{scenario_id}.scenario_verdict.scenario_verdict: expected {expected}")

    if not isinstance(integrity_doc, dict):
        errors.append(f"{scenario_id}.replay_integrity_results: expected object")
    else:
        if integrity_doc.get("probe_count") != len(PROBES):
            errors.append(f"{scenario_id}.replay_integrity_results.probe_count: expected {len(PROBES)}")
        if integrity_doc.get("improvement_count") != improved:
            errors.append(f"{scenario_id}.replay_integrity_results.improvement_count: expected {improved}")

    return {
        "scenario_id": scenario_id,
        "domain": verdict_doc.get("domain"),
        "verdict": verdict_doc.get("scenario_verdict"),
        "counts": expected_counts,
        "improvement_count": improved,
        "contradiction_count": len(chain_doc.get("contradictions", [])) if isinstance(chain_doc, dict) else 0,
        "contradiction_improved": probe_improved(baseline, pond, "contradiction preservation"),
        "recovery_improved": probe_improved(baseline, pond, "recovery-loop reconstruction"),
        "redacted_real_trace": bool(verdict_doc.get("redacted_real_trace")),
        "external_blind_pack": bool(verdict_doc.get("external_blind_pack")),
        "valid": verdict_doc.get("scenario_verdict") != "INVALID_SCENARIO",
    }


def check_scenarios(proof_dir: Path, errors: list[str]) -> list[dict[str, Any]]:
    scenario_infos = []
    scenario_root = proof_dir / "scenarios"
    for index in range(1, 6):
        info = check_scenario(scenario_root / f"scenario_{index:03d}", errors)
        if info:
            scenario_infos.append(info)
    domains = {info["domain"] for info in scenario_infos}
    if domains != REQUIRED_DOMAINS:
        errors.append(f"scenario domains: expected {sorted(REQUIRED_DOMAINS)}, got {sorted(domains)}")
    if len(domains) != len(scenario_infos):
        errors.append("scenario domains: expected unique domains")
    if sum(1 for info in scenario_infos if info["contradiction_count"] >= 3) < 2:
        errors.append("scenario contradiction chains: expected at least two scenarios with 3+ linked contradictions")
    if not any(info["redacted_real_trace"] for info in scenario_infos):
        errors.append("scenario requirements: expected at least one redacted-real operational trace")
    if not any(info["external_blind_pack"] for info in scenario_infos):
        errors.append("scenario requirements: expected at least one external/blinded evaluation pack")
    return scenario_infos


def visible_contains_hidden_expected(value: Any) -> bool:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"expected_outcomes", "expected_reconstruction_keys", "hidden_expected"}:
                return True
            if visible_contains_hidden_expected(child):
                return True
    elif isinstance(value, list):
        return any(visible_contains_hidden_expected(item) for item in value)
    return False


def check_blind_pack(proof_dir: Path, aggregate_counts: dict[str, int], errors: list[str]) -> None:
    blind_dir = proof_dir / "blind_pack"
    inputs = load_json(blind_dir / "blind_inputs.json", errors)
    hidden = load_json(blind_dir / "blind_expected_hidden.json", errors)
    if isinstance(inputs, dict):
        if inputs.get("contains_expected_outcomes") is not False:
            errors.append("blind_inputs.contains_expected_outcomes: expected false")
        if visible_contains_hidden_expected(inputs):
            errors.append("blind_inputs.json: visible input contains hidden expected outcome keys")
    if isinstance(hidden, dict) and hidden.get("visible_to_replay_path") is not False:
        errors.append("blind_expected_hidden.visible_to_replay_path: expected false")

    scorer = blind_dir / "blind_scorer.py"
    result = subprocess.run(
        [sys.executable, str(scorer)],
        cwd=blind_dir,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        errors.append(f"blind_scorer.py failed: {result.stderr.strip() or result.stdout.strip()}")
        return
    blind_results = load_json(blind_dir / "blind_results.json", errors)
    if not isinstance(blind_results, dict):
        errors.append("blind_results.json: expected object")
        return
    if blind_results.get("narrative_claims_read") is not False:
        errors.append("blind_results.narrative_claims_read: expected false")
    totals = blind_results.get("totals")
    if not isinstance(totals, dict):
        errors.append("blind_results.totals: expected object")
        return
    if totals.get("baseline_reconstructed") != aggregate_counts.get("baseline_reconstructed"):
        errors.append("blind_results.totals.baseline_reconstructed: mismatch")
    if totals.get("pond_reconstructed") != aggregate_counts.get("pond_reconstructed"):
        errors.append("blind_results.totals.pond_reconstructed: mismatch")
    if not isinstance(totals.get("delta"), int) or totals["delta"] <= 0:
        errors.append("blind_results.totals.delta: expected positive integer")


def expected_final_verdict(scenarios: list[dict[str, Any]], counts: dict[str, int], overclaim: bool) -> str:
    valid_count = sum(1 for info in scenarios if info["valid"])
    if overclaim:
        return "INVALID_GAUNTLET"
    if valid_count < 4:
        return "INVALID_GAUNTLET"
    advantage_count = sum(1 for info in scenarios if info["verdict"] == "ENTROPY_SCENARIO_ADVANTAGE")
    contradiction_improved = sum(1 for info in scenarios if info["contradiction_improved"])
    recovery_improved = sum(1 for info in scenarios if info["recovery_improved"])
    if (
        advantage_count >= 4
        and counts.get("pond_reconstructed", 0) >= counts.get("baseline_reconstructed", 0) * 2
        and counts.get("pond_reconstructed", 0) > counts.get("baseline_reconstructed", 0)
        and contradiction_improved >= 4
        and recovery_improved >= 4
    ):
        return "ENTROPY_REPLICATION_ADVANTAGE_OBSERVED"
    if advantage_count >= 2:
        return "PARTIAL_ENTROPY_REPLICATION_ADVANTAGE"
    return "NO_ENTROPY_REPLICATION_ADVANTAGE"


def check_aggregate_and_verdict(
    proof_dir: Path,
    scenarios: list[dict[str, Any]],
    overclaim: bool,
    errors: list[str],
) -> dict[str, int]:
    aggregate = load_json(proof_dir / "aggregate_results.json", errors)
    final = load_json(proof_dir / "final_verdict.json", errors)
    totals = {key: 0 for key in COUNT_KEYS}
    for info in scenarios:
        for key in totals:
            totals[key] += info["counts"][key]

    if not isinstance(aggregate, dict):
        errors.append("aggregate_results.json: expected object")
        return totals
    if aggregate.get("proof_id") != PROOF_ID:
        errors.append(f"aggregate_results.proof_id: expected {PROOF_ID}")
    if aggregate.get("scenario_count") != 5:
        errors.append("aggregate_results.scenario_count: expected 5")
    if aggregate.get("valid_scenarios") != sum(1 for info in scenarios if info["valid"]):
        errors.append("aggregate_results.valid_scenarios: mismatch")
    if aggregate.get("scenario_advantage_count") != sum(
        1 for info in scenarios if info["verdict"] == "ENTROPY_SCENARIO_ADVANTAGE"
    ):
        errors.append("aggregate_results.scenario_advantage_count: mismatch")
    if aggregate.get("aggregate_counts") != totals:
        errors.append("aggregate_results.aggregate_counts: mismatch")
    if aggregate.get("contradiction_preservation_improved_scenarios") != sum(
        1 for info in scenarios if info["contradiction_improved"]
    ):
        errors.append("aggregate_results.contradiction_preservation_improved_scenarios: mismatch")
    if aggregate.get("recovery_reconstruction_improved_scenarios") != sum(
        1 for info in scenarios if info["recovery_improved"]
    ):
        errors.append("aggregate_results.recovery_reconstruction_improved_scenarios: mismatch")

    expected = expected_final_verdict(scenarios, totals, overclaim)
    if aggregate.get("aggregate_verdict") != expected:
        errors.append(f"aggregate_results.aggregate_verdict: expected {expected}, got {aggregate.get('aggregate_verdict')}")

    if not isinstance(final, dict):
        errors.append("final_verdict.json: expected object")
        return totals
    verdict = final.get("verdict")
    if verdict not in VALID_FINAL_VERDICTS:
        errors.append("final_verdict.verdict: invalid")
    elif verdict != expected:
        errors.append(f"final_verdict.verdict: expected {expected}, got {verdict}")
    if final.get("adapter_status") != "pond_backed":
        errors.append("final_verdict.adapter_status: expected pond_backed")
    if final.get("aggregate_counts") != totals:
        errors.append("final_verdict.aggregate_counts: mismatch")
    flags = final.get("overclaim_flags")
    if not isinstance(flags, dict):
        errors.append("final_verdict.overclaim_flags: expected object")
    else:
        for key, value in flags.items():
            if value is not False:
                errors.append(f"final_verdict.overclaim_flags.{key}: expected false")
    return totals


def check_claim_register(proof_dir: Path, errors: list[str]) -> None:
    doc = load_json(proof_dir / "claim_register.json", errors)
    if not isinstance(doc, dict):
        errors.append("claim_register.json: expected object")
        return
    claims = doc.get("claims")
    if not isinstance(claims, list):
        errors.append("claim_register.claims: expected array")
        return
    seen = set()
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            errors.append(f"claim_register.claims[{index}]: expected object")
            continue
        seen.add(claim.get("id"))
        for field in ("claim_level", "evidence_refs", "safe_public_wording", "risk_if_overstated"):
            if field not in claim:
                errors.append(f"claim_register.claims[{index}].{field}: missing")
        if not isinstance(claim.get("evidence_refs"), list) or not claim["evidence_refs"]:
            errors.append(f"claim_register.claims[{index}].evidence_refs: expected non-empty array")
    missing = REQUIRED_CLAIM_IDS - seen
    if missing:
        errors.append(f"claim_register.claims: missing required claims {sorted(missing)}")
    if not isinstance(doc.get("unresolved_questions"), list) or not doc["unresolved_questions"]:
        errors.append("claim_register.unresolved_questions: expected non-empty array")


def check_manifest(proof_dir: Path, errors: list[str]) -> None:
    manifest = load_json(proof_dir / "proof_manifest.json", errors)
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
    for relative in REQUIRED_ROOT_FILES:
        if relative not in required:
            errors.append(f"proof_manifest.required_artifacts: missing {relative}")
    for response in REQUIRED_CONSULT_RESPONSES:
        if f"inside_voice_consults/{response}" not in required:
            errors.append(f"proof_manifest.required_artifacts: missing inside_voice_consults/{response}")
    for index in range(1, 6):
        for relative in REQUIRED_SCENARIO_FILES:
            entry = f"scenarios/scenario_{index:03d}/{relative}"
            if entry not in required:
                errors.append(f"proof_manifest.required_artifacts: missing {entry}")


def validate_entropy_replication_gauntlet(proof_dir: Path | str) -> list[str]:
    proof_dir = Path(proof_dir)
    if not proof_dir.is_absolute():
        proof_dir = ROOT / proof_dir

    errors: list[str] = []
    check_required_files(proof_dir, errors)
    if errors:
        return errors

    check_consults(proof_dir, errors)
    scenarios = check_scenarios(proof_dir, errors)
    overclaim = check_text_boundaries(proof_dir, errors)
    aggregate_counts = check_aggregate_and_verdict(proof_dir, scenarios, overclaim, errors)
    check_blind_pack(proof_dir, aggregate_counts, errors)
    check_claim_register(proof_dir, errors)
    check_manifest(proof_dir, errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_entropy_replication_gauntlet.py <proof_dir>", file=sys.stderr)
        return 2

    errors = validate_entropy_replication_gauntlet(Path(argv[1]))
    if errors:
        print("ENTROPY_REPLICATION_GAUNTLET_INVALID")
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("ENTROPY_REPLICATION_GAUNTLET_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
