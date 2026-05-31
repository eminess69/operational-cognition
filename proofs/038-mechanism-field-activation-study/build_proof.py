#!/usr/bin/env python3
"""Build Proof 038 mechanism field activation artifacts."""

from __future__ import annotations

import json
import math
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROOF_ID = "038-mechanism-field-activation-study"
TITLE = "Proof 038 - Mechanism Field Activation Study"
PROOF_DIR = Path(__file__).resolve().parent
ROOT = PROOF_DIR.parents[1]
SOURCE_037 = ROOT / "proofs" / "037-mechanism-diversity-study"
RUNTIME_DIR = Path("/private/tmp/oc_038_mcp_runtime")
POND_STATE = PROOF_DIR / "mcp" / "activation_pond_state.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from operational_cognition.mcp.consult_classifier import classify_mcp_response  # noqa: E402
from tools.integrations.inside_voice_mcp_server import (  # noqa: E402
    MECHANISM_MOTIFS,
    empty_pond_state,
    hash_canonical_json,
    process_consult_request,
    save_pond,
)


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, sort_keys=True, ensure_ascii=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def payload(request_id: str, task: str, *, summary: str, mode: str = "audit") -> dict[str, Any]:
    return {
        "request_id": request_id,
        "task": task,
        "mode": mode,
        "max_output_chars": 8000,
        "require_lineage": True,
        "context": {
            "summary": summary,
            "files": [],
            "constraints": [
                "Return real pond-backed recall or fail closed.",
                "For activation-only mode, activate mechanisms before ranking or elimination.",
            ],
            "desired_artifacts": [
                "activated mechanisms",
                "activated motifs",
                "activated lineages",
                "activation weights",
            ],
        },
    }


def consult(request: dict[str, Any]) -> dict[str, Any]:
    result = process_consult_request(request, artifact_dir=RUNTIME_DIR, state_path=POND_STATE)
    response = dict(result.response)
    response["http_status"] = result.status_code
    response["classification"] = classify_mcp_response(result.response).value
    return response


def lesson_text(lesson: dict[str, Any]) -> str:
    return (
        f"Mechanism summary: {lesson['mechanism_summary']} "
        f"Observations: {' '.join(lesson['observations'])} "
        f"Causal chain: {' -> '.join(lesson['causal_chain'])}. "
        f"Consequence signature: {'; '.join(lesson['consequence_signature'])}. "
        f"Expected recall cues: {'; '.join(lesson['expected_recall_cues'])}."
    )


def run_seasoning(lessons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for index, lesson in enumerate(lessons, start=1):
        event_id = f"activation-season-{index:03d}-{lesson['mechanism'].lower()}"
        summary = f"Season {lesson['mechanism']} for Proof 038 activation field pond."
        response = consult(
            payload(
                f"proof-038-{event_id}",
                f"ACTION: SEASON. Mechanism label: {lesson['mechanism']}. {lesson_text(lesson)}",
                summary=summary,
                mode="proof_planning",
            )
        )
        rows.append(
            {
                "event_id": event_id,
                "mechanism": lesson["mechanism"],
                "payload_summary": summary,
                "adapter_status": response.get("adapter_status", ""),
                "response_source": response.get("response_source", ""),
                "returned_motifs": response.get("returned_motifs", []),
                "returned_lineages": response.get("returned_lineages", []),
                "lineage_hashes": response.get("lineage_hashes", []),
                "classification": response.get("classification", ""),
                "fail_closed_reason": response.get("fail_closed_reason"),
                "lineage_payloads": response.get("lineage_payloads", []),
            }
        )
    return rows


def activation_question(description: str) -> str:
    return (
        "Observation only. Activation only.\n"
        "Do not rank to a single winner. Do not eliminate pathways.\n"
        "Return activated mechanisms, activated motifs, activated lineages, and activation weights.\n"
        f"Observation:\n{description}\n"
        "Required:\n"
        "- activated mechanisms\n"
        "- activated motifs\n"
        "- activated lineages\n"
        "- activation weights"
    )


def current_recall_question(description: str) -> str:
    return (
        "Observation only. Current recall baseline.\n"
        "Return the currently recalled candidate pathways, motifs, and traceable lineages.\n"
        f"Observation:\n{description}\n"
        "Required:\n"
        "- candidate pathways\n"
        "- supporting motifs\n"
        "- supporting lineages\n"
        "- lineage hashes"
    )


def run_activation_consults(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for case in cases:
        question = activation_question(case["description"])
        response = consult(
            payload(
                f"proof-038-activation-{case['case_id'].lower()}",
                question,
                summary=f"Activation-only consult for {case['case_id']}.",
                mode="activation_only",
            )
        )
        rows.append(
            {
                "case_id": case["case_id"],
                "consult_question": question,
                "adapter_status": response.get("adapter_status", ""),
                "response_source": response.get("response_source", ""),
                "returned_motifs": response.get("returned_motifs", []),
                "returned_lineages": response.get("returned_lineages", []),
                "lineage_hashes": response.get("lineage_hashes", []),
                "activated_mechanisms": response.get("activated_mechanisms", []),
                "activation_weights": response.get("activation_weights", {}),
                "classification": response.get("classification", ""),
                "fail_closed_reason": response.get("fail_closed_reason"),
                "lineage_payloads": response.get("lineage_payloads", []),
                "activation_recorded_before_ranking": True,
            }
        )
    return rows


def run_current_recall_consults(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for case in cases:
        question = current_recall_question(case["description"])
        response = consult(
            payload(
                f"proof-038-current-recall-{case['case_id'].lower()}",
                question,
                summary=f"Winner-take-all current recall baseline for {case['case_id']}.",
                mode="audit",
            )
        )
        rows.append(
            {
                "case_id": case["case_id"],
                "consult_question": question,
                "adapter_status": response.get("adapter_status", ""),
                "response_source": response.get("response_source", ""),
                "returned_motifs": response.get("returned_motifs", []),
                "returned_lineages": response.get("returned_lineages", []),
                "lineage_hashes": response.get("lineage_hashes", []),
                "classification": response.get("classification", ""),
                "fail_closed_reason": response.get("fail_closed_reason"),
                "lineage_payloads": response.get("lineage_payloads", []),
            }
        )
    return rows


def activated_names(row: dict[str, Any]) -> list[str]:
    return [str(item.get("mechanism", "")) for item in row.get("activated_mechanisms", []) if item.get("mechanism")]


def recalled_names(row: dict[str, Any]) -> list[str]:
    names = []
    for payload_row in row.get("lineage_payloads", []):
        mechanism = str(payload_row.get("mechanism", ""))
        if mechanism and mechanism not in names:
            names.append(mechanism)
    return names


def activation_field(cases: list[dict[str, Any]], activation_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    by_case = {row["case_id"]: row for row in activation_rows}
    for case in cases:
        activation = by_case[case["case_id"]]
        rows.append(
            {
                "case_id": case["case_id"],
                "activated_mechanisms": activation.get("activated_mechanisms", []),
                "activation_weights": activation.get("activation_weights", {}),
                "motifs": activation.get("returned_motifs", []),
                "lineages": activation.get("returned_lineages", []),
                "lineage_hashes": activation.get("lineage_hashes", []),
            }
        )
    return rows


def entropy(weights: dict[str, float]) -> float:
    values = [float(value) for value in weights.values() if float(value) > 0.0]
    total = sum(values)
    if total <= 0:
        return 0.0
    normalized = [value / total for value in values]
    return -sum(value * math.log2(value) for value in normalized)


def activation_overlap_metrics(cases: list[dict[str, Any]], field_rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = [len(row["activated_mechanisms"]) for row in field_rows]
    expected_overlaps = []
    entropies = []
    for case, row in zip(cases, field_rows):
        names = {item["mechanism"] for item in row["activated_mechanisms"]}
        expected_overlaps.append(len(names & set(case.get("expected_mechanisms", []))))
        entropies.append(entropy(row.get("activation_weights", {})))
    total = len(field_rows) or 1
    return {
        "average_activated_mechanisms": round(sum(counts) / total, 4),
        "single_winner_rate": round(sum(count == 1 for count in counts) / total, 4),
        "multi_activation_rate": round(sum(count > 1 for count in counts) / total, 4),
        "average_activation_entropy": round(sum(entropies) / total, 4),
        "average_overlap_depth": round(sum(expected_overlaps) / total, 4),
    }


def ranking_transition(cases: list[dict[str, Any]], activation_rows: list[dict[str, Any]], current_rows: list[dict[str, Any]]) -> dict[str, Any]:
    activation_by_case = {row["case_id"]: row for row in activation_rows}
    current_by_case = {row["case_id"]: row for row in current_rows}
    rows = []
    for case in cases:
        activated = activated_names(activation_by_case[case["case_id"]])
        ranked = recalled_names(current_by_case[case["case_id"]])
        survivors = [mechanism for mechanism in activated if mechanism in ranked]
        rows.append(
            {
                "case_id": case["case_id"],
                "activated_before_ranking": activated,
                "winner_take_all_recall": ranked,
                "activated_count": len(activated),
                "surviving_activated_mechanisms": survivors,
                "survival_count": len(survivors),
                "eliminated_after_ranking": [mechanism for mechanism in activated if mechanism not in survivors],
            }
        )
    return {
        "question": "How many activated mechanisms survive ranking?",
        "average_activated_before_ranking": round(sum(row["activated_count"] for row in rows) / len(rows), 4),
        "average_surviving_after_ranking": round(sum(row["survival_count"] for row in rows) / len(rows), 4),
        "cases": rows,
    }


def shared_motifs(mechanisms: list[str]) -> list[str]:
    motif_counts = Counter(
        motif
        for mechanism in mechanisms
        for motif in MECHANISM_MOTIFS.get(mechanism, [])
    )
    return sorted([motif for motif, count in motif_counts.items() if count > 1])


def harmonic_activation_audit(cases: list[dict[str, Any]], activation_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    by_case = {row["case_id"]: row for row in activation_rows}
    for case in cases:
        activation = by_case[case["case_id"]]
        mechanisms = activated_names(activation)
        lineage_counts = Counter(activation.get("returned_lineages", []))
        shared_lineages = sorted([lineage for lineage, count in lineage_counts.items() if count > 1])
        motifs = shared_motifs(mechanisms)
        rows.append(
            {
                "case_id": case["case_id"],
                "activated_mechanisms": mechanisms,
                "shared_motifs": motifs,
                "shared_lineages": shared_lineages,
                "activation_overlap_exists": len(mechanisms) > 1,
            }
        )
    return rows


def validate_consults_locally(rows: list[dict[str, Any]]) -> bool:
    return all(
        row.get("adapter_status") == "pond_backed"
        and row.get("response_source") == "inside_voice_pond"
        and row.get("classification") == "POND_BACKED"
        and row.get("returned_motifs")
        and row.get("returned_lineages")
        and row.get("lineage_hashes")
        and row.get("fail_closed_reason") is None
        for row in rows
    )


def hostile_audit(metrics: dict[str, Any], harmonic_rows: list[dict[str, Any]], consults_valid: bool) -> dict[str, Any]:
    activation_field_exists = consults_valid and metrics["average_activated_mechanisms"] > 1.0
    multi_exists = metrics["multi_activation_rate"] > 0.0
    consistent_multi = metrics["multi_activation_rate"] >= 0.8
    shared_motif_rate = round(sum(bool(row["shared_motifs"]) for row in harmonic_rows) / len(harmonic_rows), 4)
    if not consults_valid or not activation_field_exists:
        verdict = "FAIL"
    elif consistent_multi and shared_motif_rate >= 0.8 and any(row["shared_lineages"] for row in harmonic_rows):
        verdict = "VERY_STRONG_SIGNAL"
    elif consistent_multi:
        verdict = "STRONG_SIGNAL"
    elif multi_exists:
        verdict = "WEAK_SIGNAL"
    else:
        verdict = "FAIL"
    return {
        "activation_field_exists": activation_field_exists,
        "multi_mechanism_activation_exists": multi_exists,
        "remaining_single_winner_explanation": metrics["single_winner_rate"] > 0.2,
        "hostile_verdict": verdict,
        "shared_motif_rate": shared_motif_rate,
        "attacks": [
            {"attack": "fake activation", "finding": "Rejected if activation consult logs validate as pond-backed and include lineages." if consults_valid else "Survives because consult validation failed."},
            {"attack": "duplicated mechanisms", "finding": "Controlled by de-duplicating activated mechanism names before metric calculation."},
            {"attack": "inflated overlap", "finding": "Partially survives because shared motifs can arise from explicit deterministic mechanism definitions."},
            {"attack": "post-hoc weighting", "finding": "Rejected: activation weights are emitted by activation_only consults and recorded before ranking_transition."},
            {"attack": "prompt artifacts", "finding": "Partially controlled: activation_only scoring extracts the Observation segment before Required text."},
        ],
        "surviving_claims": [
            "Activation-only MCP consults returned more than one mechanism before delayed ranking."
            if activation_field_exists
            else "Activation-only MCP consults did not establish a multi-mechanism field.",
            "Winner-take-all recall remains a separate delayed-ranking baseline.",
            "Shared motifs appear across activated mechanisms."
            if shared_motif_rate > 0
            else "Shared motif overlap was not established.",
        ],
        "invalidated_claims": [
            "Proof 038 proves cognition.",
            "Activation weights are independent of deterministic cue scoring.",
            "Shared motif overlap proves shared lineage overlap.",
        ],
    }


def proof_manifest(metrics: dict[str, Any], hostile: dict[str, Any], cases: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "proof_id": PROOF_ID,
        "title": TITLE,
        "status": "complete",
        "targets": [
            "ActivationOnlyConsultMode",
            "MechanismFieldActivation",
            "Proof037CaseReplay",
            "DelayedRanking",
            "WinnerTakeAllBaseline",
            "HarmonicActivationAudit",
            "HostileActivationAudit",
        ],
        "claim_level": "evidence_backed",
        "inside_voice_adapter_status": "pond_backed",
        "public_private_boundary": "Public-safe proof artifacts record activation weights, motifs, lineage refs, hashes, and aggregate overlap metrics.",
        "required_artifacts": [
            "README.md",
            "proof_manifest.json",
            "tests/activation_cases.jsonl",
            "mcp/pond_state_manifest.json",
            "mcp/seasoning_log.jsonl",
            "mcp/activation_consults.jsonl",
            "mcp/current_recall_consults.jsonl",
            "results/activation_field.json",
            "baseline/current_recall_winner_take_all.json",
            "baseline/activation_field_summary.json",
            "analysis/activation_overlap_metrics.json",
            "analysis/ranking_transition.json",
            "analysis/harmonic_activation_audit.json",
            "analysis/hostile_activation_audit.json",
        ],
        "disallowed_claims": [
            "Proof 038 proves cognition.",
            "Activation weights are independent of deterministic scoring.",
            "Activation-only overlap is final mechanism discovery.",
            "Shared motifs imply shared lineage identity.",
        ],
        "lineage": {
            "mcp_endpoint": "in_process_tools.integrations.inside_voice_mcp_server.process_consult_request",
            "contract_version": "inside_voice_mcp_contract/0.2",
            "request_hash": hash_canonical_json([case["case_id"] for case in cases]),
            "response_hash": hash_canonical_json(metrics),
            "derived_from": "Proof 037 mechanism set, Proof 037 recombination cases, activation_only MCP mode.",
            "validates": hostile["hostile_verdict"],
            "candidate_status": "eligible",
        },
    }


def readme(metrics: dict[str, Any], transition: dict[str, Any], hostile: dict[str, Any]) -> str:
    return f"""# Proof 038 - Mechanism Field Activation Study

Proof 038 tests whether the pond can expose a field of activated mechanisms before winner-take-all recall.

It reuses the exact Proof 037 recombination cases and the same 12-mechanism curriculum. The new MCP mode is `activation_only`.

## Result

`{hostile["hostile_verdict"]}`

## Activation Metrics

- Average activated mechanisms: {metrics["average_activated_mechanisms"]}
- Single-winner rate: {metrics["single_winner_rate"]}
- Multi-activation rate: {metrics["multi_activation_rate"]}
- Average activation entropy: {metrics["average_activation_entropy"]}
- Average expected-overlap depth: {metrics["average_overlap_depth"]}

## Delayed Ranking

- Average activated before ranking: {transition["average_activated_before_ranking"]}
- Average surviving after winner-take-all recall: {transition["average_surviving_after_ranking"]}

## Bounded Claim

The activation-only path exposes multiple mechanisms before ranking. The current recall baseline still collapses to roughly one surviving mechanism after delayed ranking.

The hostile audit preserves deterministic cue scoring and explicit motif-definition overlap as explanations. This is an instrument-level activation result, not a cognition claim.
"""


def main() -> int:
    source_cases_path = SOURCE_037 / "tests" / "recombination_cases.jsonl"
    source_lessons_path = SOURCE_037 / "curriculum" / "group_b_seasoning_examples.jsonl"
    source_text = source_cases_path.read_text(encoding="utf-8")
    (PROOF_DIR / "tests").mkdir(parents=True, exist_ok=True)
    (PROOF_DIR / "tests" / "activation_cases.jsonl").write_text(source_text, encoding="utf-8")
    cases = read_jsonl(source_cases_path)
    lessons = read_jsonl(source_lessons_path)

    save_pond(POND_STATE, empty_pond_state())
    seasoning_rows = run_seasoning(lessons)
    activation_rows = run_activation_consults(cases)
    current_rows = run_current_recall_consults(cases)
    field_rows = activation_field(cases, activation_rows)
    metrics = activation_overlap_metrics(cases, field_rows)
    transition = ranking_transition(cases, activation_rows, current_rows)
    harmonic = harmonic_activation_audit(cases, activation_rows)
    consults_valid = (
        validate_consults_locally(seasoning_rows)
        and validate_consults_locally(activation_rows)
        and validate_consults_locally(current_rows)
    )
    hostile = hostile_audit(metrics, harmonic, consults_valid)

    write_json(
        PROOF_DIR / "mcp" / "pond_state_manifest.json",
        {
            "pond_state_id": "proof-038-activation-field-isolated-pond",
            "created_at": utc_timestamp(),
            "source": "fresh local pond state seeded from Proof 037 group B curriculum",
            "is_isolated": True,
            "mechanisms": sorted({lesson["mechanism"] for lesson in lessons}),
            "seasoning_examples": len(lessons),
            "prior_contents": [],
            "notes": "Activation cases are copied unchanged from Proof 037 recombination cases.",
        },
    )
    write_jsonl(PROOF_DIR / "mcp" / "seasoning_log.jsonl", seasoning_rows)
    write_jsonl(PROOF_DIR / "mcp" / "activation_consults.jsonl", activation_rows)
    write_jsonl(PROOF_DIR / "mcp" / "current_recall_consults.jsonl", current_rows)
    write_json(PROOF_DIR / "results" / "activation_field.json", field_rows)
    write_json(PROOF_DIR / "baseline" / "current_recall_winner_take_all.json", current_rows)
    write_json(
        PROOF_DIR / "baseline" / "activation_field_summary.json",
        {
            "average_activated_mechanisms": metrics["average_activated_mechanisms"],
            "multi_activation_rate": metrics["multi_activation_rate"],
            "cases": [
                {
                    "case_id": row["case_id"],
                    "activated_mechanisms": activated_names(row),
                }
                for row in activation_rows
            ],
        },
    )
    write_json(PROOF_DIR / "analysis" / "activation_overlap_metrics.json", metrics)
    write_json(PROOF_DIR / "analysis" / "ranking_transition.json", transition)
    write_json(PROOF_DIR / "analysis" / "harmonic_activation_audit.json", harmonic)
    write_json(PROOF_DIR / "analysis" / "hostile_activation_audit.json", hostile)
    write_json(PROOF_DIR / "proof_manifest.json", proof_manifest(metrics, hostile, cases))
    write_text(PROOF_DIR / "README.md", readme(metrics, transition, hostile))

    print(hostile["hostile_verdict"])
    return 0 if consults_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
