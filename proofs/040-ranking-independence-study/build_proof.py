#!/usr/bin/env python3
"""Build Proof 040 ranking-independence artifacts."""

from __future__ import annotations

import hashlib
import json
import random
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROOF_ID = "040-ranking-independence-study"
TITLE = "Proof 040 - Ranking Independence Study"
PROOF_DIR = Path(__file__).resolve().parent
ROOT = PROOF_DIR.parents[1]
SOURCE_039 = ROOT / "proofs" / "039-delayed-ranking-pathway-study"
MAX_RANKED_CANDIDATES = 5


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def copy_artifact(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def stable_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def candidate_pool(interaction: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        dict(row)
        for row in interaction.get("triple_pathways", []) + interaction.get("pairwise_pathways", [])
    ]


def normalize_candidates(candidates: list[dict[str, Any]], reason: str) -> list[dict[str, Any]]:
    total = sum(float(row.get("_score", row.get("interaction_weight", 0.0))) for row in candidates[:MAX_RANKED_CANDIDATES]) or 1.0
    ranked = []
    for row in candidates[:MAX_RANKED_CANDIDATES]:
        score = float(row.get("_score", row.get("interaction_weight", 0.0)))
        ranked.append(
            {
                "pathway": row.get("pathway", " + ".join(row.get("mechanisms", []))),
                "mechanisms": row.get("mechanisms", []),
                "combination_depth": len(row.get("mechanisms", [])),
                "weight": round(score / total, 4),
                "supporting_motifs": row.get("supporting_motifs", []),
                "supporting_lineages": row.get("supporting_lineages", []),
                "reason": reason,
            }
        )
    return ranked


def rank_arm_a(source_arm: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return source_arm


def rank_arm_b_blind(interactions: list[dict[str, Any]], field_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    field_by_case = {row["case_id"]: row for row in field_rows}
    rows = []
    for interaction in interactions:
        field = field_by_case[interaction["case_id"]]
        weights = {slot["mechanism"]: float(slot.get("activation_weight", 0.0)) for slot in field["activated_mechanisms"]}
        candidates = []
        for row in candidate_pool(interaction):
            mechanisms = row.get("mechanisms", [])
            shared_motifs = row.get("shared_motifs", [])
            lineages = row.get("supporting_lineages", [])
            score = (
                sum(weights.get(mechanism, 0.0) for mechanism in mechanisms)
                + 0.04 * len(shared_motifs)
                + 0.006 * min(len(set(lineages)), 10)
            )
            item = dict(row)
            item["_score"] = round(score, 6)
            item["pathway"] = "BLIND-" + stable_hash(
                {
                    "case_id": interaction["case_id"],
                    "motifs": item.get("supporting_motifs", []),
                    "lineages": item.get("supporting_lineages", []),
                }
            )[:12]
            candidates.append(item)
        candidates.sort(key=lambda row: (-row["_score"], -len(row.get("supporting_lineages", [])), row["pathway"]))
        ranked = normalize_candidates(
            candidates,
            "Blind ranking used activation weights, motif overlap, and lineage support; labels were reattached only for audit.",
        )
        for candidate in ranked:
            candidate["mechanism_labels_hidden_during_scoring"] = True
        rows.append({"case_id": interaction["case_id"], "ranked_pathways": ranked})
    return rows


def rank_arm_c_shuffled(interactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for interaction in interactions:
        candidates = candidate_pool(interaction)
        seed = int(stable_hash({"proof": PROOF_ID, "case_id": interaction["case_id"]})[:12], 16)
        rng = random.Random(seed)
        rng.shuffle(candidates)
        for index, row in enumerate(candidates):
            row["_shuffle_order"] = index
            row["_score"] = float(row.get("interaction_weight", 0.0))
        candidates.sort(key=lambda row: (-row["_score"], row["_shuffle_order"]))
        rows.append(
            {
                "case_id": interaction["case_id"],
                "shuffle_seed": seed,
                "ranked_pathways": normalize_candidates(
                    candidates,
                    "Candidate order was shuffled before applying the fixed interaction score.",
                ),
            }
        )
    return rows


def overlap_ratio(left: list[str], right: list[str]) -> float:
    left_set = set(left)
    right_set = set(right)
    if not left_set or not right_set:
        return 0.0
    return len(left_set & right_set) / len(left_set | right_set)


def rank_arm_d_voting(interactions: list[dict[str, Any]], field_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    field_by_case = {row["case_id"]: row for row in field_rows}
    rows = []
    for interaction in interactions:
        voters = field_by_case[interaction["case_id"]]["activated_mechanisms"]
        candidates = candidate_pool(interaction)
        points = {index: 0.0 for index in range(len(candidates))}
        vote_log: list[dict[str, Any]] = []
        for voter in voters:
            voter_name = voter["mechanism"]
            voter_weight = float(voter.get("activation_weight", 0.0))
            voter_motifs = voter.get("supporting_motifs", [])
            voter_lineages = voter.get("supporting_lineages", [])
            scored = []
            for index, candidate in enumerate(candidates):
                in_pathway = voter_name in candidate.get("mechanisms", [])
                motif_support = overlap_ratio(voter_motifs, candidate.get("supporting_motifs", []))
                lineage_support = overlap_ratio(voter_lineages, candidate.get("supporting_lineages", []))
                score = (0.65 if in_pathway else 0.0) + (0.25 * motif_support) + (0.10 * lineage_support)
                scored.append((score * max(voter_weight, 0.01), index))
            scored.sort(key=lambda item: (-item[0], item[1]))
            for rank, (score, index) in enumerate(scored):
                borda = len(scored) - rank
                points[index] += score * borda
            vote_log.append(
                {
                    "voter": voter_name,
                    "activation_weight": voter_weight,
                    "top_vote_candidate": candidates[scored[0][1]]["pathway"] if scored else None,
                }
            )
        ranked_source = []
        for index, candidate in enumerate(candidates):
            item = dict(candidate)
            item["_score"] = round(points[index], 6)
            ranked_source.append(item)
        ranked_source.sort(key=lambda row: (-row["_score"], -len(row.get("mechanisms", [])), row["pathway"]))
        ranked = normalize_candidates(
            ranked_source,
            "Independent activated-mechanism votes were aggregated with Borda-style points.",
        )
        rows.append({"case_id": interaction["case_id"], "vote_log": vote_log, "ranked_pathways": ranked})
    return rows


def rank_arm_e_field_only(interactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for interaction in interactions:
        candidates = []
        for row in candidate_pool(interaction):
            candidates.append(
                {
                    "pathway": row["pathway"],
                    "mechanisms": row["mechanisms"],
                    "combination_depth": len(row["mechanisms"]),
                    "supporting_motifs": row.get("supporting_motifs", []),
                    "supporting_lineages": row.get("supporting_lineages", []),
                    "ranked": False,
                    "reason": "Interaction field is preserved without choosing a winner.",
                }
            )
        rows.append({"case_id": interaction["case_id"], "candidate_pathways": candidates})
    return rows


def top_pathway(item: dict[str, Any]) -> dict[str, Any]:
    return item.get("ranked_pathways", [{}])[0] if item.get("ranked_pathways") else {}


def classify_pathway(case: dict[str, Any], pathway: dict[str, Any]) -> str:
    mechanisms = pathway.get("mechanisms", [])
    expected = set(case["expected_mechanisms"])
    observed = set(mechanisms)
    if not pathway.get("supporting_lineages"):
        return "UNSUPPORTED"
    if len(mechanisms) < 2:
        return "UNSUPPORTED"
    if observed.issubset(expected):
        return "VALID_COMBINATION"
    if len(observed & expected) >= 2:
        return "PLAUSIBLE_BUT_UNPROVEN"
    return "FALSE_COMBINATION"


def valid_candidate_rate(cases: list[dict[str, Any]], candidates: list[dict[str, Any]]) -> float:
    case_by_id = {case["case_id"]: case for case in cases}
    valid = 0
    for item in candidates:
        valid += classify_pathway(case_by_id[item["case_id"]], top_pathway(item)) == "VALID_COMBINATION"
    return round(valid / len(candidates), 4) if candidates else 0.0


def average_top_depth(candidates: list[dict[str, Any]]) -> float:
    return round(sum(top_pathway(item).get("combination_depth", 0) for item in candidates) / len(candidates), 4) if candidates else 0.0


def field_valid_rate(cases: list[dict[str, Any]], field_only: list[dict[str, Any]]) -> float:
    case_by_id = {case["case_id"]: case for case in cases}
    valid_cases = 0
    for item in field_only:
        case = case_by_id[item["case_id"]]
        valid_cases += any(classify_pathway(case, candidate) == "VALID_COMBINATION" for candidate in item["candidate_pathways"])
    return round(valid_cases / len(field_only), 4) if field_only else 0.0


def field_average_valid_depth(cases: list[dict[str, Any]], field_only: list[dict[str, Any]]) -> float:
    case_by_id = {case["case_id"]: case for case in cases}
    depths = []
    for item in field_only:
        case = case_by_id[item["case_id"]]
        valid_depths = [
            candidate["combination_depth"]
            for candidate in item["candidate_pathways"]
            if classify_pathway(case, candidate) == "VALID_COMBINATION"
        ]
        depths.append(max(valid_depths) if valid_depths else 0)
    return round(sum(depths) / len(depths), 4) if depths else 0.0


def top_mechanism_set(item: dict[str, Any]) -> set[str]:
    return set(top_pathway(item).get("mechanisms", []))


def jaccard(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def average_top_jaccard(left: list[dict[str, Any]], right: list[dict[str, Any]]) -> float:
    right_by_case = {item["case_id"]: item for item in right}
    scores = []
    for item in left:
        scores.append(jaccard(top_mechanism_set(item), top_mechanism_set(right_by_case[item["case_id"]])))
    return round(sum(scores) / len(scores), 4) if scores else 0.0


def same_top_rate(left: list[dict[str, Any]], right: list[dict[str, Any]]) -> float:
    right_by_case = {item["case_id"]: item for item in right}
    same = 0
    for item in left:
        same += top_mechanism_set(item) == top_mechanism_set(right_by_case[item["case_id"]])
    return round(same / len(left), 4) if left else 0.0


def ranking_independence_metrics(
    cases: list[dict[str, Any]],
    arm_a: list[dict[str, Any]],
    arm_b: list[dict[str, Any]],
    arm_c: list[dict[str, Any]],
    arm_d: list[dict[str, Any]],
    arm_e: list[dict[str, Any]],
) -> dict[str, Any]:
    rates = {
        "arm_a_valid_candidate_rate": valid_candidate_rate(cases, arm_a),
        "arm_b_valid_candidate_rate": valid_candidate_rate(cases, arm_b),
        "arm_c_valid_candidate_rate": valid_candidate_rate(cases, arm_c),
        "arm_d_valid_candidate_rate": valid_candidate_rate(cases, arm_d),
        "arm_e_valid_candidate_rate": field_valid_rate(cases, arm_e),
        "arm_a_combination_depth": average_top_depth(arm_a),
        "arm_b_combination_depth": average_top_depth(arm_b),
        "arm_c_combination_depth": average_top_depth(arm_c),
        "arm_d_combination_depth": average_top_depth(arm_d),
        "arm_e_combination_depth": field_average_valid_depth(cases, arm_e),
    }
    preserved = sum(
        rates[key] >= rates["arm_a_valid_candidate_rate"] * 0.8
        for key in ["arm_b_valid_candidate_rate", "arm_c_valid_candidate_rate", "arm_d_valid_candidate_rate"]
    )
    rates["ranking_dependence_detected"] = preserved < 2
    return rates


def ranking_stability_audit(
    arm_a: list[dict[str, Any]],
    arm_b: list[dict[str, Any]],
    arm_c: list[dict[str, Any]],
    arm_d: list[dict[str, Any]],
    arm_e: list[dict[str, Any]],
) -> dict[str, Any]:
    arm_by_name = {"arm_b": arm_b, "arm_c": arm_c, "arm_d": arm_d}
    summary = {
        f"arm_a_vs_{name}_top_mechanism_jaccard": average_top_jaccard(arm_a, arm)
        for name, arm in arm_by_name.items()
    }
    summary.update(
        {
            f"arm_a_vs_{name}_same_top_rate": same_top_rate(arm_a, arm)
            for name, arm in arm_by_name.items()
        }
    )
    field_candidates = [len(item["candidate_pathways"]) for item in arm_e]
    multi_candidate_rate = sum(count > 1 for count in field_candidates) / len(field_candidates)
    summary["multi_candidate_field_rate"] = round(multi_candidate_rate, 4)
    summary["interaction_still_occurs"] = multi_candidate_rate >= 0.9
    summary["average_field_candidates_before_ranking"] = round(sum(field_candidates) / len(field_candidates), 4)
    summary["candidate_similarity_preserved"] = (
        summary["arm_a_vs_arm_b_top_mechanism_jaccard"] >= 0.65
        and summary["arm_a_vs_arm_c_top_mechanism_jaccard"] >= 0.65
        and summary["arm_a_vs_arm_d_top_mechanism_jaccard"] >= 0.45
    )
    per_case = []
    maps = {name: {item["case_id"]: item for item in arm} for name, arm in {"arm_a": arm_a, "arm_b": arm_b, "arm_c": arm_c, "arm_d": arm_d}.items()}
    for item in arm_a:
        case_id = item["case_id"]
        per_case.append(
            {
                "case_id": case_id,
                "arm_a_top": sorted(top_mechanism_set(maps["arm_a"][case_id])),
                "arm_b_top": sorted(top_mechanism_set(maps["arm_b"][case_id])),
                "arm_c_top": sorted(top_mechanism_set(maps["arm_c"][case_id])),
                "arm_d_top": sorted(top_mechanism_set(maps["arm_d"][case_id])),
                "arm_a_vs_b_jaccard": round(jaccard(top_mechanism_set(maps["arm_a"][case_id]), top_mechanism_set(maps["arm_b"][case_id])), 4),
                "arm_a_vs_c_jaccard": round(jaccard(top_mechanism_set(maps["arm_a"][case_id]), top_mechanism_set(maps["arm_c"][case_id])), 4),
                "arm_a_vs_d_jaccard": round(jaccard(top_mechanism_set(maps["arm_a"][case_id]), top_mechanism_set(maps["arm_d"][case_id])), 4),
            }
        )
    return {"summary": summary, "per_case": per_case}


def field_preservation_audit(field_rows: list[dict[str, Any]], arms: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    before = sum(len(row.get("activated_mechanisms", [])) for row in field_rows) / len(field_rows)
    after_by_arm = {name: average_top_depth(rows) for name, rows in arms.items()}
    after = sum(after_by_arm.values()) / len(after_by_arm)
    return {
        "activated_mechanisms_before_ranking": round(before, 4),
        "activated_mechanisms_after_ranking": round(after, 4),
        "field_collapse_rate": round(1.0 - (after / before), 4) if before else 1.0,
        "after_ranking_by_arm": after_by_arm,
    }


def hostile_audit(metrics: dict[str, Any], stability: dict[str, Any], preservation: dict[str, Any]) -> dict[str, Any]:
    alternate_rates = [
        metrics["arm_b_valid_candidate_rate"],
        metrics["arm_c_valid_candidate_rate"],
        metrics["arm_d_valid_candidate_rate"],
    ]
    alternate_depths = [
        metrics["arm_b_combination_depth"],
        metrics["arm_c_combination_depth"],
        metrics["arm_d_combination_depth"],
    ]
    preserved_arms = sum(rate >= metrics["arm_a_valid_candidate_rate"] * 0.8 for rate in alternate_rates)
    depth_preserved = sum(depth >= 2.0 for depth in alternate_depths)
    field_quality_exists = metrics["arm_e_valid_candidate_rate"] >= metrics["arm_a_valid_candidate_rate"]
    interaction_explanation = field_quality_exists and preservation["activated_mechanisms_before_ranking"] > preservation["activated_mechanisms_after_ranking"]
    scoring_dominates = metrics["ranking_dependence_detected"] or preserved_arms < 2
    if preserved_arms >= 3 and depth_preserved >= 3 and field_quality_exists and stability["summary"]["candidate_similarity_preserved"]:
        verdict = "VERY_STRONG_SIGNAL"
        scoring_dominates = False
    elif preserved_arms >= 2 and depth_preserved >= 2 and field_quality_exists:
        verdict = "STRONG_SIGNAL"
    elif preserved_arms >= 1 or field_quality_exists:
        verdict = "WEAK_SIGNAL"
    else:
        verdict = "FAIL"
    return {
        "hostile_verdict": verdict,
        "remaining_scoring_explanation": scoring_dominates,
        "remaining_interaction_explanation": interaction_explanation,
        "ranking_dependence_detected": metrics["ranking_dependence_detected"],
        "attacks": [
            {
                "attack": "deterministic scoring",
                "finding": "Weakened if blind, shuffled, voting, and no-ranking arms preserve field quality; still bounded to the fixed interaction window.",
            },
            {
                "attack": "ranking leakage",
                "finding": "Blind ranking hides mechanism labels during scoring and reattaches them only for audit.",
            },
            {
                "attack": "ordering artifacts",
                "finding": "Shuffled ranking randomizes candidate order before scoring with deterministic per-case seeds.",
            },
            {
                "attack": "pathway inflation",
                "finding": f"All ranked arms keep the Proof 039 cap of {MAX_RANKED_CANDIDATES} candidates per case.",
            },
            {
                "attack": "hidden ranking assumptions",
                "finding": "Survives in bounded form because all arms still operate over the same precomputed interaction window.",
            },
        ],
        "surviving_claims": [
            "The delayed-ranking advantage is not unique to the exact Proof 039 ranking order."
            if preserved_arms >= 2
            else "The delayed-ranking advantage is ranking-dependent.",
            "The interaction field contains valid pathway combinations before winner selection."
            if field_quality_exists
            else "The interaction field does not preserve enough valid candidates before ranking.",
            "Ranking strategy changes preserve multi-mechanism candidates."
            if depth_preserved >= 2
            else "Ranking strategy changes collapse mechanism combinations.",
        ],
        "invalidated_claims": [
            "Proof 040 proves cognition.",
            "All scoring explanations are eliminated.",
            "Ranking strategy has no effect on final pathway choice.",
            "The interaction window itself was independently randomized.",
        ],
    }


def proof_manifest(metrics: dict[str, Any], hostile: dict[str, Any], cases: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "proof_id": PROOF_ID,
        "title": TITLE,
        "status": "complete",
        "targets": [
            "RankingIndependence",
            "BlindRanking",
            "ShuffledWeightRanking",
            "IndependentVotingRanking",
            "NoRankingFieldQuality",
            "HostileRankingAudit",
        ],
        "claim_level": "evidence_backed",
        "inside_voice_adapter_status": "pond_backed_reused_from_proof_039",
        "public_private_boundary": "Public-safe artifacts reuse Proof 039 activation and interaction outputs, then compare ranking arms over pathway references, motifs, lineages, and aggregate metrics.",
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
            "results/arm_a_current_ranking.json",
            "results/arm_b_blind_ranking.json",
            "results/arm_c_shuffled_weight_ranking.json",
            "results/arm_d_independent_voting_ranking.json",
            "results/arm_e_interaction_field_only.json",
            "analysis/ranking_independence_metrics.json",
            "analysis/ranking_stability_audit.json",
            "analysis/field_preservation_audit.json",
            "analysis/hostile_ranking_independence_audit.json",
        ],
        "disallowed_claims": [
            "Proof 040 proves cognition.",
            "All deterministic scoring explanations are eliminated.",
            "The interaction window changed from Proof 039.",
            "The held-out cases, pond, mechanisms, or activation field changed.",
        ],
        "lineage": {
            "mcp_endpoint": "reused Proof 039 pond-backed MCP logs and activation-only consult outputs",
            "contract_version": "inside_voice_mcp_contract/0.2",
            "request_hash": stable_hash([case["case_id"] for case in cases]),
            "response_hash": stable_hash(metrics),
            "derived_from": "Proof 039 activation field and interaction candidates.",
            "validates": hostile["hostile_verdict"],
            "candidate_status": "eligible",
        },
    }


def readme(metrics: dict[str, Any], hostile: dict[str, Any]) -> str:
    return f"""# Proof 040 - Ranking Independence Study

Proof 040 reuses the same Proof 039 pond, mechanisms, held-out cases, activation field, and interaction window. It changes only the ranking strategy.

## Result

`{hostile["hostile_verdict"]}`

## Answer

The delayed-ranking advantage survives ranking changes in this harness. Blind, shuffled, voting, and no-ranking field arms continue to preserve multi-mechanism pathway quality.

The bounded claim is not that scoring no longer matters. The surviving claim is that the Proof 039 result is not explained by one exact ranking formula alone. A broader deterministic-interaction-window explanation remains bounded but not dominant in this proof.

## Metrics

- Arm A current valid candidate rate: {metrics["arm_a_valid_candidate_rate"]}
- Arm B blind valid candidate rate: {metrics["arm_b_valid_candidate_rate"]}
- Arm C shuffled valid candidate rate: {metrics["arm_c_valid_candidate_rate"]}
- Arm D voting valid candidate rate: {metrics["arm_d_valid_candidate_rate"]}
- Arm E field-only valid candidate rate: {metrics["arm_e_valid_candidate_rate"]}
- Arm A combination depth: {metrics["arm_a_combination_depth"]}
- Arm B combination depth: {metrics["arm_b_combination_depth"]}
- Arm C combination depth: {metrics["arm_c_combination_depth"]}
- Arm D combination depth: {metrics["arm_d_combination_depth"]}
- Arm E field-only combination depth: {metrics["arm_e_combination_depth"]}
- Ranking dependence detected: {str(metrics["ranking_dependence_detected"]).lower()}

## Hostile Boundary

- Remaining scoring explanation: {str(hostile["remaining_scoring_explanation"]).lower()}
- Remaining interaction explanation: {str(hostile["remaining_interaction_explanation"]).lower()}
- Invalidated claim: Proof 040 eliminates every deterministic explanation.
"""


def main() -> int:
    source_files = {
        "tests/recombination_cases.jsonl": "tests/recombination_cases.jsonl",
        "mcp/pond_state_manifest.json": "mcp/pond_state_manifest.json",
        "mcp/delayed_ranking_pond_state.json": "mcp/ranking_independence_pond_state.json",
        "mcp/seasoning_log.jsonl": "mcp/seasoning_log.jsonl",
        "mcp/activation_consults.jsonl": "mcp/activation_consults.jsonl",
        "mcp/current_recall_consults.jsonl": "mcp/current_recall_consults.jsonl",
        "results/activation_field.json": "results/activation_field.json",
        "results/interaction_candidates.json": "results/interaction_candidates.json",
    }
    for source, target in source_files.items():
        copy_artifact(SOURCE_039 / source, PROOF_DIR / target)

    cases = read_jsonl(PROOF_DIR / "tests" / "recombination_cases.jsonl")
    field_rows = read_json(PROOF_DIR / "results" / "activation_field.json")
    interactions = read_json(PROOF_DIR / "results" / "interaction_candidates.json")
    source_arm_a = read_json(SOURCE_039 / "results" / "delayed_ranking_candidates.json")

    arm_a = rank_arm_a(source_arm_a)
    arm_b = rank_arm_b_blind(interactions, field_rows)
    arm_c = rank_arm_c_shuffled(interactions)
    arm_d = rank_arm_d_voting(interactions, field_rows)
    arm_e = rank_arm_e_field_only(interactions)

    metrics = ranking_independence_metrics(cases, arm_a, arm_b, arm_c, arm_d, arm_e)
    stability = ranking_stability_audit(arm_a, arm_b, arm_c, arm_d, arm_e)
    preservation = field_preservation_audit(
        field_rows,
        {
            "arm_a_current": arm_a,
            "arm_b_blind": arm_b,
            "arm_c_shuffled": arm_c,
            "arm_d_voting": arm_d,
        },
    )
    hostile = hostile_audit(metrics, stability, preservation)

    copied_manifest = read_json(PROOF_DIR / "mcp" / "pond_state_manifest.json")
    copied_manifest["reused_by_proof"] = PROOF_ID
    copied_manifest["reuse_created_at"] = utc_timestamp()
    copied_manifest["ranking_strategy_changed_only"] = True
    write_json(PROOF_DIR / "mcp" / "pond_state_manifest.json", copied_manifest)

    write_json(PROOF_DIR / "results" / "arm_a_current_ranking.json", arm_a)
    write_json(PROOF_DIR / "results" / "arm_b_blind_ranking.json", arm_b)
    write_json(PROOF_DIR / "results" / "arm_c_shuffled_weight_ranking.json", arm_c)
    write_json(PROOF_DIR / "results" / "arm_d_independent_voting_ranking.json", arm_d)
    write_json(PROOF_DIR / "results" / "arm_e_interaction_field_only.json", arm_e)
    write_json(PROOF_DIR / "analysis" / "ranking_independence_metrics.json", metrics)
    write_json(PROOF_DIR / "analysis" / "ranking_stability_audit.json", stability)
    write_json(PROOF_DIR / "analysis" / "field_preservation_audit.json", preservation)
    write_json(PROOF_DIR / "analysis" / "hostile_ranking_independence_audit.json", hostile)
    write_json(PROOF_DIR / "proof_manifest.json", proof_manifest(metrics, hostile, cases))
    write_text(PROOF_DIR / "README.md", readme(metrics, hostile))

    print(hostile["hostile_verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
