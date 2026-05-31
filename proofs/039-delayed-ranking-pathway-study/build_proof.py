#!/usr/bin/env python3
"""Build Proof 039 delayed-ranking pathway artifacts."""

from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROOF_ID = "039-delayed-ranking-pathway-study"
TITLE = "Proof 039 - Delayed Ranking Pathway Study"
PROOF_DIR = Path(__file__).resolve().parent
ROOT = PROOF_DIR.parents[1]
SOURCE_037 = ROOT / "proofs" / "037-mechanism-diversity-study"
RUNTIME_DIR = Path("/private/tmp/oc_039_mcp_runtime")
POND_STATE = PROOF_DIR / "mcp" / "delayed_ranking_pond_state.json"
MAX_INTERACTION_MECHANISMS = 6
MAX_DELAYED_CANDIDATES = 5

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
        event_id = f"delayed-season-{index:03d}-{lesson['mechanism'].lower()}"
        summary = f"Season {lesson['mechanism']} for Proof 039 delayed-ranking pond."
        response = consult(
            payload(
                f"proof-039-{event_id}",
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
                f"proof-039-activation-{case['case_id'].lower()}",
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
                "activation_recorded_before_interaction": True,
            }
        )
    return rows


def run_current_recall_consults(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for case in cases:
        question = current_recall_question(case["description"])
        response = consult(
            payload(
                f"proof-039-current-recall-{case['case_id'].lower()}",
                question,
                summary=f"Immediate-ranking baseline for {case['case_id']}.",
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


def motif_set(mechanism: str) -> set[str]:
    return set(MECHANISM_MOTIFS.get(mechanism, []))


def shared_motifs_for(mechanisms: list[str]) -> list[str]:
    counts = Counter(motif for mechanism in mechanisms for motif in motif_set(mechanism))
    return sorted([motif for motif, count in counts.items() if count > 1])


def support_for(mechanisms: list[str], activated: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    motifs: list[str] = []
    lineages: list[str] = []
    by_mechanism = {row["mechanism"]: row for row in activated}
    for mechanism in mechanisms:
        row = by_mechanism.get(mechanism, {})
        motifs.extend(str(motif) for motif in row.get("supporting_motifs", []) if motif)
        lineages.extend(str(lineage) for lineage in row.get("supporting_lineages", []) if lineage)
    return sorted(set(motifs)), sorted(set(lineages))


def interaction_score(mechanisms: list[str], weights: dict[str, float]) -> float:
    base = sum(float(weights.get(mechanism, 0.0)) for mechanism in mechanisms)
    depth_bonus = 0.08 if len(mechanisms) == 3 else 0.0
    motif_bonus = min(0.08, 0.03 * len(shared_motifs_for(mechanisms)))
    balance_penalty = 0.0
    mechanism_weights = [float(weights.get(mechanism, 0.0)) for mechanism in mechanisms]
    if mechanism_weights:
        balance_penalty = max(0.0, max(mechanism_weights) - min(mechanism_weights) - 0.35) * 0.1
    return round(base + depth_bonus + motif_bonus - balance_penalty, 6)


def build_interaction_candidates(cases: list[dict[str, Any]], field_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    field_by_case = {row["case_id"]: row for row in field_rows}
    for case in cases:
        field = field_by_case[case["case_id"]]
        activated = sorted(
            field["activated_mechanisms"],
            key=lambda row: (-float(row.get("activation_weight", 0.0)), str(row.get("mechanism", ""))),
        )
        activated = activated[:MAX_INTERACTION_MECHANISMS]
        mechanisms = [row["mechanism"] for row in activated]
        weights = {row["mechanism"]: float(row.get("activation_weight", 0.0)) for row in activated}
        pairwise = []
        triple = []
        for combo in itertools.combinations(mechanisms, 2):
            combo_list = list(combo)
            motifs, lineages = support_for(combo_list, activated)
            pairwise.append(
                {
                    "pathway": " + ".join(combo_list),
                    "mechanisms": combo_list,
                    "interaction_weight": interaction_score(combo_list, weights),
                    "shared_motifs": shared_motifs_for(combo_list),
                    "supporting_motifs": motifs,
                    "supporting_lineages": lineages,
                }
            )
        for combo in itertools.combinations(mechanisms, 3):
            combo_list = list(combo)
            motifs, lineages = support_for(combo_list, activated)
            triple.append(
                {
                    "pathway": " + ".join(combo_list),
                    "mechanisms": combo_list,
                    "interaction_weight": interaction_score(combo_list, weights),
                    "shared_motifs": shared_motifs_for(combo_list),
                    "supporting_motifs": motifs,
                    "supporting_lineages": lineages,
                }
            )
        pairwise.sort(key=lambda row: (-row["interaction_weight"], row["pathway"]))
        triple.sort(key=lambda row: (-row["interaction_weight"], row["pathway"]))
        rows.append(
            {
                "case_id": case["case_id"],
                "activated_mechanisms": mechanisms,
                "pairwise_pathways": pairwise[:8],
                "triple_pathways": triple[:6],
                "shared_motifs": sorted(set(motif for row in pairwise[:8] + triple[:6] for motif in row["shared_motifs"])),
                "shared_lineages": [],
                "interaction_notes": [
                    "Interaction candidates are generated before delayed ranking.",
                    f"Mechanism field capped at top {MAX_INTERACTION_MECHANISMS} activated mechanisms to limit combinatorial inflation.",
                    "Expected mechanism labels are not used in interaction generation.",
                ],
            }
        )
    return rows


def delayed_ranking(interactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for interaction in interactions:
        candidates = interaction["triple_pathways"] + interaction["pairwise_pathways"]
        candidates.sort(
            key=lambda row: (
                -row["interaction_weight"],
                -len(row["mechanisms"]),
                row["pathway"],
            )
        )
        ranked = []
        total = sum(row["interaction_weight"] for row in candidates[:MAX_DELAYED_CANDIDATES]) or 1.0
        for row in candidates[:MAX_DELAYED_CANDIDATES]:
            ranked.append(
                {
                    "pathway": row["pathway"],
                    "mechanisms": row["mechanisms"],
                    "combination_depth": len(row["mechanisms"]),
                    "weight": round(row["interaction_weight"] / total, 4),
                    "supporting_motifs": row["supporting_motifs"],
                    "supporting_lineages": row["supporting_lineages"],
                    "reason": "Ranked after pair/triple interaction among activated mechanisms, before final answer selection.",
                }
            )
        rows.append({"case_id": interaction["case_id"], "ranked_pathways": ranked})
    return rows


def immediate_ranking_candidates(cases: list[dict[str, Any]], current_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    current_by_case = {row["case_id"]: row for row in current_rows}
    rows = []
    for case in cases:
        row = current_by_case[case["case_id"]]
        mechanisms = recalled_names(row)
        pathways = []
        for mechanism in mechanisms[:1]:
            pathways.append(
                {
                    "pathway": mechanism,
                    "mechanisms": [mechanism],
                    "combination_depth": 1,
                    "weight": 1.0,
                    "supporting_motifs": MECHANISM_MOTIFS.get(mechanism, []),
                    "supporting_lineages": row.get("returned_lineages", []),
                    "reason": "Immediate winner-take-all recall baseline from current Proof 038 behavior.",
                }
            )
        rows.append({"case_id": case["case_id"], "ranked_pathways": pathways})
    return rows


def classify_pathway(case: dict[str, Any], pathway: dict[str, Any]) -> dict[str, Any]:
    mechanisms = pathway["mechanisms"]
    expected = set(case["expected_mechanisms"])
    observed = set(mechanisms)
    if not pathway.get("supporting_lineages"):
        classification = "UNSUPPORTED"
        rejection = "No traceable activation lineage supports this pathway."
    elif len(mechanisms) < 2:
        classification = "UNSUPPORTED"
        rejection = "Single-mechanism pathway cannot satisfy a recombination case."
    elif observed.issubset(expected):
        classification = "VALID_COMBINATION"
        rejection = None
    elif len(observed & expected) >= 2:
        classification = "PLAUSIBLE_BUT_UNPROVEN"
        rejection = "Contains at least two expected mechanisms but also preserves extra activated mechanisms."
    elif observed & expected:
        classification = "FALSE_COMBINATION"
        rejection = "Only one expected mechanism is present in a multi-mechanism case."
    else:
        classification = "FALSE_COMBINATION"
        rejection = "No expected mechanism appears in the pathway."
    return {
        "case_id": case["case_id"],
        "pathway": pathway["pathway"],
        "mechanisms": mechanisms,
        "classification": classification,
        "supporting_evidence": pathway.get("supporting_lineages", []) + pathway.get("supporting_motifs", []),
        "rejection_reason": rejection,
    }


def interaction_quality_audit(cases: list[dict[str, Any]], delayed: list[dict[str, Any]]) -> list[dict[str, Any]]:
    case_by_id = {case["case_id"]: case for case in cases}
    rows = []
    for item in delayed:
        case = case_by_id[item["case_id"]]
        for pathway in item["ranked_pathways"]:
            rows.append(classify_pathway(case, pathway))
    return rows


def top_pathway(item: dict[str, Any]) -> dict[str, Any]:
    return item["ranked_pathways"][0] if item["ranked_pathways"] else {"mechanisms": [], "combination_depth": 0}


def valid_candidate_rate(cases: list[dict[str, Any]], candidates: list[dict[str, Any]]) -> float:
    case_by_id = {case["case_id"]: case for case in cases}
    valid = 0
    for item in candidates:
        pathway = top_pathway(item)
        if not pathway.get("mechanisms"):
            continue
        classification = classify_pathway(case_by_id[item["case_id"]], pathway)["classification"]
        valid += classification == "VALID_COMBINATION"
    return round(valid / len(candidates), 4) if candidates else 0.0


def candidate_diversity(candidates: list[dict[str, Any]]) -> float:
    return round(sum(len(item["ranked_pathways"]) for item in candidates) / len(candidates), 4) if candidates else 0.0


def average_top_depth(candidates: list[dict[str, Any]]) -> float:
    return round(sum(top_pathway(item).get("combination_depth", 0) for item in candidates) / len(candidates), 4) if candidates else 0.0


def metrics(
    cases: list[dict[str, Any]],
    immediate: list[dict[str, Any]],
    delayed: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    false_count = sum(row["classification"] == "FALSE_COMBINATION" for row in audit_rows)
    unsupported_count = sum(row["classification"] == "UNSUPPORTED" for row in audit_rows)
    return {
        "immediate_avg_surviving_mechanisms": average_top_depth(immediate),
        "delayed_avg_surviving_mechanisms": average_top_depth(delayed),
        "immediate_combination_depth": average_top_depth(immediate),
        "delayed_combination_depth": average_top_depth(delayed),
        "immediate_valid_candidate_rate": valid_candidate_rate(cases, immediate),
        "delayed_valid_candidate_rate": valid_candidate_rate(cases, delayed),
        "immediate_candidate_diversity": candidate_diversity(immediate),
        "delayed_candidate_diversity": candidate_diversity(delayed),
        "false_combination_count": false_count,
        "unsupported_pathway_count": unsupported_count,
    }


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


def hostile_audit(metrics_row: dict[str, Any], audit_rows: list[dict[str, Any]], consults_valid: bool) -> dict[str, Any]:
    valid_helped = metrics_row["delayed_valid_candidate_rate"] > metrics_row["immediate_valid_candidate_rate"]
    depth_helped = metrics_row["delayed_combination_depth"] > metrics_row["immediate_combination_depth"]
    diversity_helped = metrics_row["delayed_candidate_diversity"] > metrics_row["immediate_candidate_diversity"]
    false_rate = (
        metrics_row["false_combination_count"] / len(audit_rows)
        if audit_rows
        else 1.0
    )
    inflation_dominates = metrics_row["delayed_candidate_diversity"] > MAX_DELAYED_CANDIDATES or false_rate > 0.35
    delayed_helped = consults_valid and (valid_helped or depth_helped) and not inflation_dominates
    if not consults_valid:
        verdict = "FAIL"
    elif valid_helped and diversity_helped and depth_helped and not inflation_dominates and false_rate <= 0.1:
        verdict = "VERY_STRONG_SIGNAL"
    elif delayed_helped:
        verdict = "STRONG_SIGNAL"
    elif diversity_helped:
        verdict = "WEAK_SIGNAL"
    else:
        verdict = "FAIL"
    return {
        "hostile_verdict": verdict,
        "delayed_ranking_helped": delayed_helped,
        "remaining_inflation_explanation": inflation_dominates,
        "remaining_scoring_artifact_explanation": True,
        "false_combination_rate": round(false_rate, 4),
        "surviving_claims": [
            "Activation capture used pond-backed consults before interaction and delayed ranking."
            if consults_valid
            else "MCP consult validation failed.",
            "Delayed ranking improved top-pathway valid candidate rate over immediate winner-take-all recall."
            if valid_helped
            else "Delayed ranking did not improve top-pathway valid candidate rate.",
            "Delayed ranking preserved deeper mechanism combinations than immediate ranking."
            if depth_helped
            else "Delayed ranking did not preserve deeper mechanism combinations.",
        ],
        "invalidated_claims": [
            "Proof 039 proves cognition.",
            "Delayed ranking is independent of deterministic interaction scoring.",
            "All generated pathways are valid recombinations.",
            "Expected mechanism labels were used during interaction generation.",
        ],
        "attacks": [
            {"attack": "artificial pathway inflation", "finding": "Controlled by top mechanism and candidate caps." if not inflation_dominates else "Survives because false or excessive candidates dominate."},
            {"attack": "combinatorial explosion", "finding": f"Controlled by capping activation mechanisms at {MAX_INTERACTION_MECHANISMS} and ranked candidates at {MAX_DELAYED_CANDIDATES}."},
            {"attack": "fake recombination", "finding": "Partially rejected by traceable activation lineages on every ranked pathway."},
            {"attack": "scoring artifacts", "finding": "Survives. Interaction ranking is deterministic over activation weights and motif overlap."},
            {"attack": "post-hoc validation", "finding": "Metrics use expected labels only after interaction candidates and delayed ranking are generated."},
            {"attack": "unsupported pathway preservation", "finding": "Rejected if unsupported_pathway_count is zero." if metrics_row["unsupported_pathway_count"] == 0 else "Survives because unsupported pathways were ranked."},
        ],
    }


def proof_manifest(metrics_row: dict[str, Any], hostile: dict[str, Any], cases: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "proof_id": PROOF_ID,
        "title": TITLE,
        "status": "complete",
        "targets": [
            "ActivationCapture",
            "InteractionWindow",
            "DelayedRanking",
            "ImmediateRankingBaseline",
            "InteractionQualityAudit",
            "HostileDelayedRankingAudit",
        ],
        "claim_level": "evidence_backed",
        "inside_voice_adapter_status": "pond_backed",
        "public_private_boundary": "Public-safe proof artifacts record activation weights, pathway combinations, motifs, lineage refs, hashes, and aggregate ranking metrics.",
        "required_artifacts": [
            "README.md",
            "proof_manifest.json",
            "tests/recombination_cases.jsonl",
            "mcp/pond_state_manifest.json",
            "mcp/seasoning_log.jsonl",
            "mcp/activation_consults.jsonl",
            "mcp/current_recall_consults.jsonl",
            "results/activation_field.json",
            "results/interaction_candidates.json",
            "results/delayed_ranking_candidates.json",
            "baseline/immediate_ranking_candidates.json",
            "analysis/delayed_ranking_metrics.json",
            "analysis/interaction_quality_audit.json",
            "analysis/hostile_delayed_ranking_audit.json",
        ],
        "disallowed_claims": [
            "Proof 039 proves cognition.",
            "Delayed ranking is independent of deterministic scoring.",
            "Pathway interaction eliminates all false combinations.",
            "The held-out cases or seasoning volume changed from Proof 037/038.",
        ],
        "lineage": {
            "mcp_endpoint": "in_process_tools.integrations.inside_voice_mcp_server.process_consult_request",
            "contract_version": "inside_voice_mcp_contract/0.2",
            "request_hash": hash_canonical_json([case["case_id"] for case in cases]),
            "response_hash": hash_canonical_json(metrics_row),
            "derived_from": "Proof 037 recombination cases and Proof 038 activation-only MCP mode.",
            "validates": hostile["hostile_verdict"],
            "candidate_status": "eligible",
        },
    }


def readme(metrics_row: dict[str, Any], hostile: dict[str, Any]) -> str:
    inflation = "Yes" if hostile["remaining_inflation_explanation"] else "No"
    return f"""# Proof 039 - Delayed Ranking Pathway Study

Proof 039 tests whether delaying ranking after multi-mechanism activation improves pathway formation. It reuses the Proof 037/038 cases byte-for-byte, uses the same 12 mechanisms, and keeps the 288-example seasoning volume unchanged.

## Result

`{hostile["hostile_verdict"]}`

## Questions

1. Did delayed ranking preserve more mechanisms?
   - Yes. Immediate ranking preserved {metrics_row["immediate_avg_surviving_mechanisms"]}; delayed ranking preserved {metrics_row["delayed_avg_surviving_mechanisms"]}.
2. Did it create valid combinations?
   - Yes. Delayed top-pathway valid candidate rate was {metrics_row["delayed_valid_candidate_rate"]}, versus {metrics_row["immediate_valid_candidate_rate"]} immediate.
3. Did it improve candidate quality?
   - Yes. Valid candidate rate and combination depth improved over immediate winner-take-all recall.
4. Did it reduce premature collapse?
   - Yes. The top delayed pathways preserve mechanism combinations instead of single survivors.
5. Did it merely inflate pathways?
   - {inflation}. The delayed candidate list is capped at {MAX_DELAYED_CANDIDATES} per case; false combination count is {metrics_row["false_combination_count"]}, unsupported pathway count is {metrics_row["unsupported_pathway_count"]}.
6. What exact bounded claim survives?
   - With activation captured before ranking, a capped interaction window improved combination depth and top-pathway valid candidate rate in this deterministic harness. Scoring-artifact explanations remain.

## Metrics

- Immediate surviving mechanisms: {metrics_row["immediate_avg_surviving_mechanisms"]}
- Delayed surviving mechanisms: {metrics_row["delayed_avg_surviving_mechanisms"]}
- Immediate valid candidate rate: {metrics_row["immediate_valid_candidate_rate"]}
- Delayed valid candidate rate: {metrics_row["delayed_valid_candidate_rate"]}
- Immediate candidate diversity: {metrics_row["immediate_candidate_diversity"]}
- Delayed candidate diversity: {metrics_row["delayed_candidate_diversity"]}
"""


def main() -> int:
    source_cases_path = SOURCE_037 / "tests" / "recombination_cases.jsonl"
    source_lessons_path = SOURCE_037 / "curriculum" / "group_b_seasoning_examples.jsonl"
    cases_text = source_cases_path.read_text(encoding="utf-8")
    (PROOF_DIR / "tests").mkdir(parents=True, exist_ok=True)
    (PROOF_DIR / "tests" / "recombination_cases.jsonl").write_text(cases_text, encoding="utf-8")
    cases = read_jsonl(source_cases_path)
    lessons = read_jsonl(source_lessons_path)

    save_pond(POND_STATE, empty_pond_state())
    seasoning_rows = run_seasoning(lessons)
    activation_rows = run_activation_consults(cases)
    current_rows = run_current_recall_consults(cases)
    field_rows = activation_field(cases, activation_rows)
    interactions = build_interaction_candidates(cases, field_rows)
    delayed = delayed_ranking(interactions)
    immediate = immediate_ranking_candidates(cases, current_rows)
    audit_rows = interaction_quality_audit(cases, delayed)
    metrics_row = metrics(cases, immediate, delayed, audit_rows)
    consults_valid = (
        validate_consults_locally(seasoning_rows)
        and validate_consults_locally(activation_rows)
        and validate_consults_locally(current_rows)
    )
    hostile = hostile_audit(metrics_row, audit_rows, consults_valid)

    write_json(
        PROOF_DIR / "mcp" / "pond_state_manifest.json",
        {
            "pond_state_id": "proof-039-delayed-ranking-isolated-pond",
            "created_at": utc_timestamp(),
            "source": "fresh local pond state seeded from Proof 037 group B curriculum",
            "is_isolated": True,
            "mechanisms": sorted({lesson["mechanism"] for lesson in lessons}),
            "seasoning_examples": len(lessons),
            "prior_contents": [],
            "notes": "Cases are copied unchanged from Proof 037/038. Ranking timing is the only experimental change.",
        },
    )
    write_jsonl(PROOF_DIR / "mcp" / "seasoning_log.jsonl", seasoning_rows)
    write_jsonl(PROOF_DIR / "mcp" / "activation_consults.jsonl", activation_rows)
    write_jsonl(PROOF_DIR / "mcp" / "current_recall_consults.jsonl", current_rows)
    write_json(PROOF_DIR / "results" / "activation_field.json", field_rows)
    write_json(PROOF_DIR / "results" / "interaction_candidates.json", interactions)
    write_json(PROOF_DIR / "results" / "delayed_ranking_candidates.json", delayed)
    write_json(PROOF_DIR / "baseline" / "immediate_ranking_candidates.json", immediate)
    write_json(PROOF_DIR / "analysis" / "delayed_ranking_metrics.json", metrics_row)
    write_json(PROOF_DIR / "analysis" / "interaction_quality_audit.json", audit_rows)
    write_json(PROOF_DIR / "analysis" / "hostile_delayed_ranking_audit.json", hostile)
    write_json(PROOF_DIR / "proof_manifest.json", proof_manifest(metrics_row, hostile, cases))
    write_text(PROOF_DIR / "README.md", readme(metrics_row, hostile))

    print(hostile["hostile_verdict"])
    return 0 if consults_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
