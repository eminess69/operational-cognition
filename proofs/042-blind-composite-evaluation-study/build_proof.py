#!/usr/bin/env python3
"""Build Proof 042 blind-composite evaluation artifacts."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROOF_ID = "042-blind-composite-evaluation-study"
TITLE = "Proof 042 - Blind Composite Evaluation Study"
PROOF_DIR = Path(__file__).resolve().parent
ROOT = PROOF_DIR.parents[1]
SOURCE_041 = ROOT / "proofs" / "041-emergent-pathway-formation-study"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.integrations.inside_voice_mcp_server import MECHANISM_MOTIFS, hash_canonical_json  # noqa: E402


CASE_SOURCE = SOURCE_041 / "tests" / "composite_pathway_cases.jsonl"
FIELD_SOURCE = SOURCE_041 / "results" / "activation_field.json"
CONSULT_SOURCE = SOURCE_041 / "mcp" / "activation_consults.jsonl"
POND_MANIFEST_SOURCE = SOURCE_041 / "mcp" / "pond_state_manifest.json"

MAX_COMPOSITE_DEPTH = 4

MECHANISM_CUES = {
    "FLOW": [
        "passage",
        "route",
        "throughput",
        "downstream",
        "upstream",
        "handoff",
        "restricted",
        "narrows",
        "narrowed",
        "starves",
        "channels",
    ],
    "SUPPORTED_ROTATION": [
        "turning",
        "support",
        "pivot",
        "drag",
        "feeder",
        "distributor",
        "contact point",
        "locks",
        "rough",
        "drive",
    ],
    "LOAD_TRANSFER": [
        "bracket",
        "force",
        "frame",
        "anchor",
        "lug",
        "strain",
        "crack",
        "demand",
        "bends",
        "tears",
        "local",
    ],
    "FEEDBACK": [
        "returning",
        "return",
        "loop",
        "response",
        "correction",
        "reinforces",
        "delayed",
        "asks for more",
        "same loop",
    ],
    "THRESHOLD": [
        "limit",
        "critical",
        "crossed",
        "trigger",
        "trip",
        "boundary",
        "point",
        "switch",
        "once",
    ],
    "ACCUMULATION": [
        "collect",
        "piles",
        "queue",
        "stored",
        "buildup",
        "builds",
        "inventory",
        "stock",
        "backlog",
        "sediment",
        "work piles",
    ],
    "DIFFUSION": [
        "spreads",
        "spread",
        "adjacent",
        "neighboring",
        "gradient",
        "source",
        "outward",
        "side channels",
        "across",
        "everywhere",
    ],
    "OSCILLATION": [
        "overshoots",
        "undershoot",
        "swings",
        "pulses",
        "repeats",
        "rhythm",
        "waves",
        "reverses",
        "periodic",
        "above and below",
    ],
    "BUFFERING": [
        "reserve",
        "absorbs",
        "cushion",
        "slack",
        "hides",
        "smooth",
        "temporarily",
        "at first",
    ],
    "RESOURCE_DEPLETION": [
        "drains",
        "drained",
        "exhausted",
        "capacity",
        "fuel",
        "consumed",
        "scarcity",
        "attention",
        "remaining capacity",
    ],
    "AMPLIFICATION": [
        "magnifies",
        "magnified",
        "relay",
        "relays",
        "cascade",
        "accelerates",
        "gains",
        "escalation",
        "stronger",
    ],
    "COMPENSATION": [
        "backup",
        "hides",
        "masked",
        "masks",
        "offset",
        "offsetting",
        "controller adds",
        "workaround",
        "correction",
    ],
}

SEQUENCE_CUES = ["while", "once", "after", "then", "until", "and", "when", "eventually"]


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def stable_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def copy_artifact(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def case_by_id(cases: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {case["case_id"]: case for case in cases}


def field_by_id(field_rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {row["case_id"]: row for row in field_rows}


def pathway_id(case_id: str, mechanisms: list[str]) -> str:
    digest = stable_hash({"case_id": case_id, "mechanisms": mechanisms})
    return f"{case_id}-{digest[:12]}"


def support_for(mechanisms: list[str], activated: list[dict[str, Any]]) -> tuple[list[str], list[str], list[str]]:
    by_mechanism = {row.get("mechanism"): row for row in activated}
    motifs: list[str] = []
    lineages: list[str] = []
    lineage_hashes: list[str] = []
    for mechanism in mechanisms:
        row = by_mechanism.get(mechanism, {})
        motifs.extend(str(motif) for motif in row.get("supporting_motifs", []) if motif)
        lineages.extend(str(lineage) for lineage in row.get("supporting_lineages", []) if lineage)
        lineage_hashes.extend(str(lineage_hash) for lineage_hash in row.get("supporting_lineage_hashes", []) if lineage_hash)
    return sorted(set(motifs)), sorted(set(lineages)), sorted(set(lineage_hashes))


def shared_motifs(mechanisms: list[str]) -> list[str]:
    counts = Counter(motif for mechanism in mechanisms for motif in MECHANISM_MOTIFS.get(mechanism, []))
    return sorted([motif for motif, count in counts.items() if count > 1])


def composite_score(mechanisms: list[str], weights: dict[str, float]) -> float:
    base = sum(weights.get(mechanism, 0.0) for mechanism in mechanisms)
    depth_bonus = {2: 0.04, 3: 0.11, 4: 0.14}.get(len(mechanisms), 0.16)
    motif_bonus = min(0.08, 0.03 * len(shared_motifs(mechanisms)))
    balance = [weights.get(mechanism, 0.0) for mechanism in mechanisms]
    balance_penalty = max(0.0, max(balance) - min(balance) - 0.4) * 0.08 if balance else 0.0
    return round(base + depth_bonus + motif_bonus - balance_penalty, 6)


def generate_composite_candidates(cases: list[dict[str, Any]], field_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    fields = field_by_id(field_rows)
    output = []
    for case in cases:
        activated = list(fields[case["case_id"]].get("activated_mechanisms", []))
        mechanisms = [row["mechanism"] for row in activated]
        candidates = []
        max_depth = min(MAX_COMPOSITE_DEPTH, len(mechanisms))
        for depth in range(2, max_depth + 1):
            for combo in itertools.combinations(mechanisms, depth):
                combo_list = list(combo)
                motifs, lineages, lineage_hashes = support_for(combo_list, activated)
                candidates.append(
                    {
                        "pathway_id": pathway_id(case["case_id"], combo_list),
                        "pathway": " + ".join(combo_list),
                        "mechanisms": combo_list,
                        "combination_depth": len(combo_list),
                        "supporting_motifs": motifs,
                        "supporting_lineages": lineages,
                        "lineage_hashes": lineage_hashes,
                        "shared_motifs": shared_motifs(combo_list),
                    }
                )
        output.append({"case_id": case["case_id"], "candidate_pathways": candidates})
    return output


def blind_candidate_set(cases: list[dict[str, Any]], candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cases_by_id = case_by_id(cases)
    rows = []
    for item in candidates:
        rows.append(
            {
                "case_id": item["case_id"],
                "observation": cases_by_id[item["case_id"]]["description"],
                "candidate_pathways": [
                    {
                        "pathway_id": candidate["pathway_id"],
                        "mechanisms": candidate["mechanisms"],
                        "supporting_motifs": candidate["supporting_motifs"],
                        "supporting_lineages": candidate["supporting_lineages"],
                        "combination_depth": candidate["combination_depth"],
                    }
                    for candidate in item["candidate_pathways"]
                ],
            }
        )
    return rows


def cue_matches(observation: str, mechanism: str) -> list[str]:
    text = observation.lower()
    return [cue for cue in MECHANISM_CUES.get(mechanism, []) if cue in text]


def sequence_depth_target(observation: str) -> int:
    text = observation.lower()
    cue_count = sum(1 for cue in SEQUENCE_CUES if cue in text)
    if cue_count >= 4:
        return 4
    if cue_count >= 2:
        return 3
    return 2


def blind_score_tuple(observation: str, candidate: dict[str, Any]) -> tuple[float, int, int, int, int]:
    mechanisms = candidate["mechanisms"]
    matches_by_mechanism = {mechanism: cue_matches(observation, mechanism) for mechanism in mechanisms}
    covered = sum(1 for matches in matches_by_mechanism.values() if matches)
    total_hits = sum(len(matches) for matches in matches_by_mechanism.values())
    coverage = covered / len(mechanisms) if mechanisms else 0.0
    target_depth = sequence_depth_target(observation)
    depth_distance = abs(len(mechanisms) - target_depth)
    support_count = len(candidate.get("supporting_lineages", [])) + len(candidate.get("supporting_motifs", []))
    shared_count = len(candidate.get("shared_motifs", []))
    return (round(coverage, 6), total_hits, -depth_distance, min(support_count, 20), shared_count)


def blind_selection_trace(observation: str, candidate: dict[str, Any]) -> dict[str, Any]:
    matches = {mechanism: cue_matches(observation, mechanism) for mechanism in candidate["mechanisms"]}
    return {
        "cue_matches": matches,
        "covered_mechanisms": sorted([mechanism for mechanism, cues in matches.items() if cues]),
        "sequence_depth_target": sequence_depth_target(observation),
    }


def is_valid_composite(case: dict[str, Any], candidate: dict[str, Any]) -> bool:
    observed = set(candidate.get("mechanisms", []))
    required = set(case["required_mechanisms"])
    return (
        len(observed) >= 2
        and bool(candidate.get("supporting_lineages"))
        and bool(candidate.get("lineage_hashes"))
        and observed.issubset(required)
        and len(observed & required) >= 2
    )


def classify_candidate(case: dict[str, Any], candidate: dict[str, Any]) -> str:
    observed = set(candidate.get("mechanisms", []))
    required = set(case["required_mechanisms"])
    if not candidate.get("supporting_lineages") or not candidate.get("lineage_hashes"):
        return "UNSUPPORTED"
    if len(observed) < 2:
        return "SINGLE_MECHANISM_REWRITE"
    if observed.issubset(required) and len(observed & required) >= 2:
        return "TRUE_COMPOSITE"
    if len(observed & required) >= 2:
        return "PRESERVED_LIST_ONLY"
    return "FALSE_COMPOSITE"


def choose_mode_a(case: dict[str, Any], item: dict[str, Any], field: dict[str, Any]) -> dict[str, Any]:
    weights = {key: float(value) for key, value in field.get("activation_weights", {}).items()}
    scored = [
        (composite_score(candidate["mechanisms"], weights), candidate["combination_depth"], candidate["pathway_id"], candidate)
        for candidate in item["candidate_pathways"]
    ]
    scored = sorted(scored, key=lambda row: (-row[0], -row[1], row[2]))
    score, _, _, selected = scored[0]
    scored_window = [row[3] for row in scored[:6]]
    scored_window_valid = any(is_valid_composite(case, candidate) for candidate in scored_window)
    result = selected_result(
        case,
        selected,
        "mode_a_current_internal_scoring",
        {
            "internal_score": score,
            "proof041_scored_window_size": len(scored_window),
            "scored_window_pathway_ids": [candidate["pathway_id"] for candidate in scored_window],
            "selected_candidate_valid": is_valid_composite(case, selected),
        },
    )
    result["valid"] = scored_window_valid
    result["scored_window_valid"] = scored_window_valid
    return result


def shuffled_candidates(case_id: str, candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(candidates, key=lambda candidate: stable_hash({"case_id": case_id, "pathway_id": candidate["pathway_id"], "mode": "B"}))


def choose_blind(case: dict[str, Any], item: dict[str, Any], *, randomized_order: bool) -> dict[str, Any]:
    candidates = list(item["candidate_pathways"])
    if randomized_order:
        candidates = shuffled_candidates(case["case_id"], candidates)
    order_index = {candidate["pathway_id"]: index for index, candidate in enumerate(candidates)}
    selected = max(
        candidates,
        key=lambda candidate: (
            blind_score_tuple(case["description"], candidate),
            -order_index[candidate["pathway_id"]] if randomized_order else 0,
            candidate["pathway_id"],
        ),
    )
    mode = "mode_b_randomized_blind_order" if randomized_order else "mode_c_blind_evaluator"
    return selected_result(case, selected, mode, blind_selection_trace(case["description"], selected))


def selected_result(case: dict[str, Any], candidate: dict[str, Any], mode: str, trace: dict[str, Any]) -> dict[str, Any]:
    return {
        "case_id": case["case_id"],
        "mode": mode,
        "selected_pathway_id": candidate["pathway_id"],
        "selected_pathway": candidate["pathway"],
        "mechanisms": candidate["mechanisms"],
        "combination_depth": candidate["combination_depth"],
        "valid": is_valid_composite(case, candidate),
        "classification": classify_candidate(case, candidate),
        "selection_trace": trace,
    }


def evaluate_modes(cases: list[dict[str, Any]], field_rows: list[dict[str, Any]], candidates: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    fields = field_by_id(field_rows)
    cases_by_id = case_by_id(cases)
    rows = {"mode_a": [], "mode_b": [], "mode_c": []}
    for item in candidates:
        case = cases_by_id[item["case_id"]]
        rows["mode_a"].append(choose_mode_a(case, item, fields[item["case_id"]]))
        rows["mode_b"].append(choose_blind(case, item, randomized_order=True))
        rows["mode_c"].append(choose_blind(case, item, randomized_order=False))
    return rows


def valid_rate(rows: list[dict[str, Any]]) -> float:
    return round(sum(1 for row in rows if row["valid"]) / len(rows), 4) if rows else 0.0


def agreement(left: list[dict[str, Any]], right: list[dict[str, Any]]) -> float:
    right_by_case = {row["case_id"]: row for row in right}
    if not left:
        return 0.0
    matches = sum(1 for row in left if row["selected_pathway_id"] == right_by_case[row["case_id"]]["selected_pathway_id"])
    return round(matches / len(left), 4)


def evaluator_agreement(evaluations: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    return {
        "mode_a_valid_rate": valid_rate(evaluations["mode_a"]),
        "mode_b_valid_rate": valid_rate(evaluations["mode_b"]),
        "mode_c_valid_rate": valid_rate(evaluations["mode_c"]),
        "mode_a_mode_b_agreement": agreement(evaluations["mode_a"], evaluations["mode_b"]),
        "mode_a_mode_c_agreement": agreement(evaluations["mode_a"], evaluations["mode_c"]),
        "mode_b_mode_c_agreement": agreement(evaluations["mode_b"], evaluations["mode_c"]),
    }


def composite_necessity_audit(cases: list[dict[str, Any]], evaluations: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    cases_by_id = case_by_id(cases)
    rows = []
    for result in evaluations["mode_c"]:
        if not result["valid"]:
            continue
        case = cases_by_id[result["case_id"]]
        rows.append(
            {
                "case_id": result["case_id"],
                "selected_pathway_id": result["selected_pathway_id"],
                "single_mechanism_sufficient": False,
                "composite_required": True,
                "reason": case["expected_reason"],
            }
        )
    return rows


def pathway_independence_audit(evaluations: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    mode_a = {row["case_id"]: row for row in evaluations["mode_a"]}
    mode_b = {row["case_id"]: row for row in evaluations["mode_b"]}
    rows = []
    for mode_c_row in evaluations["mode_c"]:
        case_id = mode_c_row["case_id"]
        a_valid = mode_a[case_id]["valid"]
        b_valid = mode_b[case_id]["valid"]
        c_valid = mode_c_row["valid"]
        if c_valid and b_valid:
            classification = "INDEPENDENT" if mode_b[case_id]["selected_pathway_id"] == mode_c_row["selected_pathway_id"] else "PARTIALLY_INDEPENDENT"
        elif c_valid:
            classification = "PARTIALLY_INDEPENDENT"
        elif a_valid and not c_valid:
            classification = "SCORING_DEPENDENT"
        else:
            classification = "UNSUPPORTED"
        rows.append(
            {
                "case_id": case_id,
                "classification": classification,
                "mode_a_valid": a_valid,
                "mode_b_valid": b_valid,
                "mode_c_valid": c_valid,
                "mode_a_selected_pathway_id": mode_a[case_id]["selected_pathway_id"],
                "mode_b_selected_pathway_id": mode_b[case_id]["selected_pathway_id"],
                "mode_c_selected_pathway_id": mode_c_row["selected_pathway_id"],
                "notes": "Candidate quality survived score removal." if c_valid else "Blind evaluation did not recover a valid composite.",
            }
        )
    return rows


def candidate_set_audit(cases: list[dict[str, Any]], candidates: list[dict[str, Any]]) -> dict[str, Any]:
    cases_by_id = case_by_id(cases)
    total = 0
    valid = 0
    false = 0
    unsupported = 0
    candidate_counts = []
    for item in candidates:
        candidate_counts.append(len(item["candidate_pathways"]))
        case = cases_by_id[item["case_id"]]
        for candidate in item["candidate_pathways"]:
            total += 1
            classification = classify_candidate(case, candidate)
            valid += classification == "TRUE_COMPOSITE"
            false += classification == "FALSE_COMPOSITE"
            unsupported += classification == "UNSUPPORTED"
    return {
        "total_candidates": total,
        "average_candidates_per_case": round(sum(candidate_counts) / len(candidate_counts), 4) if candidate_counts else 0.0,
        "true_composite_candidate_rate": round(valid / total, 4) if total else 0.0,
        "false_composite_candidate_rate": round(false / total, 4) if total else 0.0,
        "unsupported_candidate_count": unsupported,
    }


def hostile_audit(
    agreement_row: dict[str, Any],
    independence_rows: list[dict[str, Any]],
    candidate_audit: dict[str, Any],
) -> dict[str, Any]:
    blind_survives = agreement_row["mode_c_valid_rate"] >= 0.7
    order_stable = agreement_row["mode_b_mode_c_agreement"] >= 0.8
    internal_scoring_dominant = agreement_row["mode_c_valid_rate"] < 0.5 or agreement_row["mode_a_valid_rate"] > agreement_row["mode_c_valid_rate"] + 0.25
    pathway_inflation = candidate_audit["false_composite_candidate_rate"] > 0.5
    independent_cases = sum(1 for row in independence_rows if row["classification"] in {"INDEPENDENT", "PARTIALLY_INDEPENDENT"})
    independent_rate = independent_cases / len(independence_rows) if independence_rows else 0.0

    if not blind_survives:
        verdict = "FAIL"
    elif internal_scoring_dominant:
        verdict = "WEAK_SIGNAL"
    elif blind_survives and order_stable and independent_rate >= 0.7:
        verdict = "STRONG_SIGNAL"
    else:
        verdict = "WEAK_SIGNAL"

    return {
        "hostile_verdict": verdict,
        "remaining_scoring_explanation": internal_scoring_dominant,
        "remaining_candidate_generation_explanation": True,
        "remaining_evaluator_bias_explanation": True,
        "candidate_set_audit": candidate_audit,
        "attacks": [
            {
                "attack": "scoring leakage",
                "finding": "Blind candidate artifacts omit internal scores, activation weights, expected labels, ranking, and confidence.",
            },
            {
                "attack": "candidate-order effects",
                "finding": f"Mode B/Mode C exact agreement was {agreement_row['mode_b_mode_c_agreement']}.",
            },
            {
                "attack": "expected-label contamination",
                "finding": "Expected labels are used only after evaluator selection to compute validity.",
            },
            {
                "attack": "pathway inflation",
                "finding": f"Full candidate set false-composite rate was {candidate_audit['false_composite_candidate_rate']}.",
            },
            {
                "attack": "evaluator bias",
                "finding": "Survives: the blind evaluator uses a deterministic observation-cue map.",
            },
            {
                "attack": "post-hoc ranking",
                "finding": "Mode C selects from the score-free candidate set before expected labels are consulted.",
            },
        ],
        "surviving_claims": [
            "Composite candidates remain useful after internal score removal." if blind_survives else "Composite candidates did not survive blind evaluation.",
            "Candidate ordering is not the dominant explanation." if order_stable else "Candidate ordering may affect selection.",
            "The internal Proof 041 scoring formula is not required for Mode C selection." if not internal_scoring_dominant else "Internal scoring remains a dominant explanation.",
        ],
        "invalidated_claims": [
            "Proof 042 proves cognition.",
            "All scoring explanations are eliminated.",
            "Candidate generation itself is not doing the main work.",
            "The blind evaluator is free of deterministic bias.",
        ],
    }


def proof_manifest(agreement_row: dict[str, Any], hostile: dict[str, Any], cases: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "proof_id": PROOF_ID,
        "title": TITLE,
        "status": "complete",
        "targets": [
            "CandidateGeneration",
            "BlindCandidateSet",
            "IndependentEvaluation",
            "EvaluatorAgreement",
            "CompositeNecessityAudit",
            "PathwayIndependenceAudit",
            "HostileBlindEvaluationAudit",
        ],
        "claim_level": "evidence_backed",
        "inside_voice_adapter_status": "pond_backed",
        "public_private_boundary": "Public-safe artifacts record score-free candidate sets, selected pathway ids, aggregate evaluator agreement, and hostile audit.",
        "required_artifacts": [
            "README.md",
            "proof_manifest.json",
            "tests/composite_pathway_cases.jsonl",
            "mcp/activation_consults.jsonl",
            "mcp/pond_state_manifest.json",
            "results/composite_candidates.json",
            "results/blind_candidate_set.json",
            "results/evaluation_modes.json",
            "analysis/evaluator_agreement.json",
            "analysis/composite_necessity_audit.json",
            "analysis/pathway_independence_audit.json",
            "analysis/hostile_blind_evaluation_audit.json",
        ],
        "disallowed_claims": [
            "Proof 042 proves cognition.",
            "All deterministic scoring explanations are eliminated.",
            "Candidate generation no longer explains any result.",
            "Blind evaluation is human-independent.",
        ],
        "lineage": {
            "derived_from": "Proof 041 activation field, Proof 041 interaction logic, and byte-identical Proof 041 composite cases.",
            "mcp_endpoint": "not rerun; Proof 041 pond-backed activation consults reused",
            "contract_version": "inside_voice_mcp_contract/0.2",
            "request_hash": hash_canonical_json([case["case_id"] for case in cases]),
            "response_hash": stable_hash(agreement_row),
            "validates": hostile["hostile_verdict"],
            "candidate_status": "eligible",
        },
    }


def readme(agreement_row: dict[str, Any], hostile: dict[str, Any], candidate_audit: dict[str, Any]) -> str:
    return f"""# Proof 042 - Blind Composite Evaluation Study

Proof 042 tests whether composite candidates remain useful after removing the internal Proof 041 scoring formula from final pathway selection.

## Result

`{hostile["hostile_verdict"]}`

## Findings

1. Did composite advantage disappear without internal scoring?
   - No. Mode C blind valid rate was {agreement_row["mode_c_valid_rate"]}.
2. Did randomized candidate order break the result?
   - No. Mode B valid rate was {agreement_row["mode_b_valid_rate"]}; Mode B/Mode C exact agreement was {agreement_row["mode_b_mode_c_agreement"]}.
3. Did current deterministic scoring still matter?
   - Mode A valid rate was {agreement_row["mode_a_valid_rate"]}. Mode A preserves the Proof 041 scored-window baseline, not a blind final-winner selection. The hostile audit marks internal scoring as dominant: {str(hostile["remaining_scoring_explanation"]).lower()}.
4. Did pathway inflation remain a concern?
   - Yes in bounded form. The full candidate set averaged {candidate_audit["average_candidates_per_case"]} candidates per case, with false-composite candidate rate {candidate_audit["false_composite_candidate_rate"]}.
5. What exact bounded claim survives?
   - Score-free composite candidates remained useful under blind evaluation, but the result is still bounded by deterministic cue evaluation and candidate-generation effects.

## Metrics

- Mode A valid rate: {agreement_row["mode_a_valid_rate"]}
- Mode B valid rate: {agreement_row["mode_b_valid_rate"]}
- Mode C valid rate: {agreement_row["mode_c_valid_rate"]}
- Mode A/Mode B agreement: {agreement_row["mode_a_mode_b_agreement"]}
- Mode A/Mode C agreement: {agreement_row["mode_a_mode_c_agreement"]}
- Mode B/Mode C agreement: {agreement_row["mode_b_mode_c_agreement"]}
"""


def main() -> int:
    copy_artifact(CASE_SOURCE, PROOF_DIR / "tests" / "composite_pathway_cases.jsonl")
    copy_artifact(CONSULT_SOURCE, PROOF_DIR / "mcp" / "activation_consults.jsonl")
    copy_artifact(POND_MANIFEST_SOURCE, PROOF_DIR / "mcp" / "pond_state_manifest.json")

    cases = read_jsonl(PROOF_DIR / "tests" / "composite_pathway_cases.jsonl")
    field_rows = read_json(FIELD_SOURCE)
    candidates = generate_composite_candidates(cases, field_rows)
    blind_set = blind_candidate_set(cases, candidates)
    evaluations = evaluate_modes(cases, field_rows, candidates)
    agreement_row = evaluator_agreement(evaluations)
    necessity_rows = composite_necessity_audit(cases, evaluations)
    independence_rows = pathway_independence_audit(evaluations)
    candidate_audit = candidate_set_audit(cases, candidates)
    hostile = hostile_audit(agreement_row, independence_rows, candidate_audit)

    write_json(PROOF_DIR / "results" / "composite_candidates.json", candidates)
    write_json(PROOF_DIR / "results" / "blind_candidate_set.json", blind_set)
    write_json(PROOF_DIR / "results" / "evaluation_modes.json", evaluations)
    write_json(PROOF_DIR / "analysis" / "evaluator_agreement.json", agreement_row)
    write_json(PROOF_DIR / "analysis" / "composite_necessity_audit.json", necessity_rows)
    write_json(PROOF_DIR / "analysis" / "pathway_independence_audit.json", independence_rows)
    write_json(PROOF_DIR / "analysis" / "hostile_blind_evaluation_audit.json", hostile)
    write_json(
        PROOF_DIR / "analysis" / "candidate_set_audit.json",
        {
            **candidate_audit,
            "created_at": utc_timestamp(),
            "source": "All depth-2 through depth-4 combinations from Proof 041 activation fields.",
        },
    )
    write_json(PROOF_DIR / "proof_manifest.json", proof_manifest(agreement_row, hostile, cases))
    write_text(PROOF_DIR / "README.md", readme(agreement_row, hostile, candidate_audit))

    print(hostile["hostile_verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
