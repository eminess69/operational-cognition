"""Deterministic mechanism-transfer pond CLI.

The engine is intentionally closed-world. It identifies a mechanism only when
the loaded pond state provides enough role evidence to map an observed system
to one taught core motif. Otherwise it returns FAIL_CLOSED.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


STATE_FILE = "pond_state.json"
MECHANISM_ALIASES = {
    "flow": "flow",
    "supported_rotation": "supported_rotation",
    "load_transfer": "load_transfer",
    "FLOW": "flow",
    "SUPPORTED_ROTATION": "supported_rotation",
    "LOAD_TRANSFER": "load_transfer",
}


def empty_state(state_id: str) -> dict[str, Any]:
    return {
        "schema_version": "mechanism_pond_state.v1",
        "state_id": state_id,
        "mechanisms": {},
        "lessons": {},
    }


def load_pond(path: Path) -> dict[str, Any]:
    state_path = path / STATE_FILE if path.is_dir() else path
    try:
        with state_path.open("r", encoding="utf-8") as handle:
            state = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return empty_state("missing_or_invalid")
    if not isinstance(state, dict):
        return empty_state("invalid_type")
    return state


def load_recall(path: Path) -> dict[str, Any]:
    try:
        recall = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return recall if isinstance(recall, dict) else {}


def normalize(text: str) -> str:
    lowered = text.strip().lower()
    lowered = re.sub(r"[^a-z0-9]+", " ", lowered)
    return re.sub(r"\s+", " ", lowered).strip()


def token_set(text: str) -> set[str]:
    tokens = set(normalize(text).split())
    expanded = set(tokens)
    for token in tokens:
        if token.endswith("ies") and len(token) > 3:
            expanded.add(token[:-3] + "y")
        if token.endswith("s") and len(token) > 3:
            expanded.add(token[:-1])
        if token.endswith("ing") and len(token) > 5:
            expanded.add(token[:-3])
        if token.endswith("ed") and len(token) > 4:
            expanded.add(token[:-2])
    return expanded


def normalize_mechanism_id(value: Any) -> str:
    raw = str(value).strip()
    if raw in MECHANISM_ALIASES:
        return MECHANISM_ALIASES[raw]
    normalized = normalize(raw).replace(" ", "_")
    return MECHANISM_ALIASES.get(normalized, normalized)


def recall_candidates(recall: dict[str, Any]) -> list[str]:
    raw_candidates = recall.get("returned_mechanism_candidates", recall.get("mechanism_candidates", []))
    if not isinstance(raw_candidates, list):
        return []
    candidates: list[str] = []
    seen: set[str] = set()
    for candidate in raw_candidates:
        mechanism_id = normalize_mechanism_id(candidate)
        if mechanism_id and mechanism_id not in seen:
            seen.add(mechanism_id)
            candidates.append(mechanism_id)
    return candidates


def recall_list(recall: dict[str, Any], *keys: str) -> list[Any]:
    for key in keys:
        value = recall.get(key, [])
        if isinstance(value, list):
            return value
    return []


def recall_traceable(recall: dict[str, Any]) -> bool:
    lineages = recall_list(recall, "returned_lineages", "lineage_refs", "selected_path_ids")
    lineage_hashes = recall_list(recall, "lineage_hashes")
    motifs = recall_list(recall, "returned_motifs", "recalled_motifs")
    return bool(lineages or lineage_hashes) and bool(motifs)


def state_with_recalled_candidates(state: dict[str, Any], candidates: list[str]) -> dict[str, Any]:
    if not candidates:
        return state
    mechanisms = state.get("mechanisms", {})
    if not isinstance(mechanisms, dict):
        return state
    filtered = {
        mechanism_id: mechanism
        for mechanism_id, mechanism in mechanisms.items()
        if normalize_mechanism_id(mechanism_id) in candidates
    }
    narrowed = dict(state)
    narrowed["mechanisms"] = filtered
    return narrowed


def cue_present(cue: str, normalized_question: str, tokens: set[str]) -> bool:
    normalized_cue = normalize(cue)
    if not normalized_cue:
        return False
    if " " in normalized_cue:
        return normalized_cue in normalized_question
    return normalized_cue in tokens


def observed_system(question: str) -> str:
    patterns = [
        r"observed system:\s*(.+?)(?:\s+question:|$)",
        r"test:\s*(.+?)(?:\s+question:|$)",
        r"target:\s*(.+?)(?:\s+question:|$)",
    ]
    for pattern in patterns:
        match = re.search(pattern, question, flags=re.IGNORECASE | re.DOTALL)
        if match:
            return re.sub(r"\s+", " ", match.group(1)).strip()
    return re.sub(r"\s+", " ", question).strip()[:220]


def question_intent(question: str) -> str:
    q = normalize(question)
    if "rank" in q or "viable mechanism" in q or "candidate mechanism" in q or "confidence ranking" in q:
        return "ranking"
    if "inspect" in q or "inspected first" in q:
        return "inspection"
    if "component category" in q or "category" in q:
        return "component_category"
    if "what happens" in q or "happens when" in q:
        return "effect"
    if "what mechanism" in q or "mechanism is similar" in q or "similar" in q:
        return "similarity"
    return "mapping"


def score_role(role: dict[str, Any], normalized_question: str, tokens: set[str]) -> dict[str, Any] | None:
    cues = role.get("cues", [])
    if not isinstance(cues, list):
        return None
    matched = [str(cue) for cue in cues if cue_present(str(cue), normalized_question, tokens)]
    minimum = role.get("minimum_cues", 1)
    if not isinstance(minimum, int) or minimum < 1:
        minimum = 1
    if len(matched) < minimum:
        return None
    role_id = str(role.get("role_id", ""))
    motif = str(role.get("motif", role_id))
    weight = role.get("weight", 1.0)
    if not isinstance(weight, (int, float)):
        weight = 1.0
    return {
        "role_id": role_id,
        "motif": motif,
        "matched_cues": matched,
        "weight": float(weight),
    }


def score_consequence_feature(
    feature: dict[str, Any], normalized_question: str, tokens: set[str]
) -> dict[str, Any] | None:
    cues = feature.get("cues", [])
    if not isinstance(cues, list):
        return None
    matched = [str(cue) for cue in cues if cue_present(str(cue), normalized_question, tokens)]
    minimum = feature.get("minimum_cues", 1)
    if not isinstance(minimum, int) or minimum < 1:
        minimum = 1
    if len(matched) < minimum:
        return None
    feature_id = str(feature.get("feature_id", ""))
    motif = str(feature.get("motif", feature_id))
    weight = feature.get("weight", 0.8)
    if not isinstance(weight, (int, float)):
        weight = 0.8
    return {
        "feature_id": feature_id,
        "motif": motif,
        "matched_cues": matched,
        "weight": float(weight),
    }


def score_mechanism(mechanism_id: str, mechanism: dict[str, Any], question: str) -> dict[str, Any]:
    normalized_question = normalize(question)
    tokens = token_set(question)
    roles = mechanism.get("roles", [])
    matched_roles: list[dict[str, Any]] = []
    if isinstance(roles, list):
        for role in roles:
            if not isinstance(role, dict):
                continue
            role_match = score_role(role, normalized_question, tokens)
            if role_match:
                matched_roles.append(role_match)

    cue_count = sum(len(role["matched_cues"]) for role in matched_roles)
    role_score = sum(role["weight"] for role in matched_roles) + min(cue_count, 8) * 0.05

    consequence_signatures = mechanism.get("consequence_signatures", [])
    matched_consequences: list[dict[str, Any]] = []
    if isinstance(consequence_signatures, list):
        for feature in consequence_signatures:
            if not isinstance(feature, dict):
                continue
            feature_match = score_consequence_feature(feature, normalized_question, tokens)
            if feature_match:
                matched_consequences.append(feature_match)

    consequence_cue_count = sum(len(feature["matched_cues"]) for feature in matched_consequences)
    consequence_score = sum(feature["weight"] for feature in matched_consequences) + min(consequence_cue_count, 10) * 0.04
    score = role_score + consequence_score
    return {
        "mechanism_id": mechanism_id,
        "mechanism": mechanism,
        "matched_roles": matched_roles,
        "matched_role_count": len(matched_roles),
        "matched_cue_count": cue_count,
        "role_score": round(role_score, 4),
        "matched_consequences": matched_consequences,
        "matched_consequence_count": len(matched_consequences),
        "matched_consequence_cue_count": consequence_cue_count,
        "consequence_score": round(consequence_score, 4),
        "score": round(score, 4),
    }


def source_tracebacks(mechanism_id: str, mechanism: dict[str, Any]) -> list[dict[str, Any]]:
    trace = {
        "lesson_id": mechanism.get("lesson_id", ""),
        "mechanism_id": mechanism_id,
        "mechanism_name": mechanism.get("mechanism_name", mechanism_id),
        "core_motif": mechanism.get("core_motif", []),
        "trace_expectation": mechanism.get("trace_expectation", ""),
    }
    return [trace] if trace["lesson_id"] else []


def evidence_features(matched_roles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "role_id": role["role_id"],
            "motif": role["motif"],
            "matched_cues": role["matched_cues"],
        }
        for role in matched_roles
    ]


def consequence_features(matched_consequences: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "feature_id": feature["feature_id"],
            "motif": feature["motif"],
            "matched_cues": feature["matched_cues"],
        }
        for feature in matched_consequences
    ]


def motif_lineage(mechanism_id: str, mechanism: dict[str, Any], matched_roles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lesson_id = str(mechanism.get("lesson_id", ""))
    mechanism_name = str(mechanism.get("mechanism_name", mechanism_id))
    return [
        {
            "lesson_id": lesson_id,
            "mechanism_id": mechanism_id,
            "mechanism_name": mechanism_name,
            "role_id": role["role_id"],
            "motif": role["motif"],
            "matched_cues": role["matched_cues"],
        }
        for role in matched_roles
    ]


def consequence_lineage(
    mechanism_id: str, mechanism: dict[str, Any], matched_consequences: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    lesson_id = str(mechanism.get("lesson_id", ""))
    mechanism_name = str(mechanism.get("mechanism_name", mechanism_id))
    return [
        {
            "lesson_id": lesson_id,
            "mechanism_id": mechanism_id,
            "mechanism_name": mechanism_name,
            "feature_id": feature["feature_id"],
            "motif": feature["motif"],
            "matched_cues": feature["matched_cues"],
        }
        for feature in matched_consequences
    ]


def viable_candidate_rows(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        candidate
        for candidate in candidates
        if candidate.get("score", 0.0) > 0.0
        and (
            candidate.get("matched_role_count", 0) > 0
            or candidate.get("matched_consequence_count", 0) > 0
        )
    ]


def candidate_mechanisms(candidates: list[dict[str, Any]]) -> list[str]:
    return [str(candidate.get("mechanism_id", "")) for candidate in viable_candidate_rows(candidates)]


def confidence_ranking(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    viable = viable_candidate_rows(candidates)
    if not viable:
        return []
    top_score = max(float(candidate.get("score", 0.0)) for candidate in viable) or 1.0
    ranking = []
    for rank, candidate in enumerate(viable, start=1):
        score = float(candidate.get("score", 0.0))
        ranking.append(
            {
                "rank": rank,
                "mechanism_id": candidate.get("mechanism_id", ""),
                "score": round(score, 4),
                "relative_confidence": round(min(0.95, max(0.05, score / top_score)), 4),
                "matched_role_count": candidate.get("matched_role_count", 0),
                "matched_consequence_count": candidate.get("matched_consequence_count", 0),
                "matched_roles": candidate.get("matched_roles", []),
                "matched_consequences": candidate.get("matched_consequences", []),
            }
        )
    return ranking


def rejected_mechanisms(
    candidates: list[dict[str, Any]],
    selected_mechanism_id: str = "",
    reason: str = "lower_ranked_candidate",
) -> list[dict[str, Any]]:
    rows = []
    for candidate in candidates:
        if candidate["mechanism_id"] == selected_mechanism_id:
            continue
        rows.append(
            {
                "mechanism_id": candidate["mechanism_id"],
                "score": candidate["score"],
                "matched_role_count": candidate["matched_role_count"],
                "matched_cue_count": candidate["matched_cue_count"],
                "matched_consequence_count": candidate.get("matched_consequence_count", 0),
                "matched_consequence_cue_count": candidate.get("matched_consequence_cue_count", 0),
                "matched_roles": [role["role_id"] for role in candidate["matched_roles"]],
                "matched_consequences": [
                    feature["feature_id"] for feature in candidate.get("matched_consequences", [])
                ],
                "rejection_reason": reason,
            }
        )
    return rows


def fail_closed(question: str, reason: str, evidence: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    candidate_evidence = evidence or []
    return {
        "question": question,
        "observed_system": observed_system(question),
        "identified_mechanism": "",
        "evidence_features": [],
        "rejected_mechanisms": [
            {
                "mechanism_id": row.get("mechanism_id", ""),
                "score": row.get("score", 0.0),
                "matched_role_count": row.get("matched_role_count", 0),
                "matched_cue_count": row.get("matched_cue_count", 0),
                "matched_consequence_count": row.get("matched_consequence_count", 0),
                "matched_consequence_cue_count": row.get("matched_consequence_cue_count", 0),
                "matched_roles": row.get("matched_roles", []),
                "matched_consequences": row.get("matched_consequences", []),
                "rejection_reason": reason,
            }
            for row in candidate_evidence
        ],
        "motif_lineage": [],
        "confidence": 0.0,
        "supporting_motifs": [],
        "source_mechanism": "",
        "transfer_confidence": 0.0,
        "answer": "",
        "status": "FAIL_CLOSED",
        "component_category": "",
        "inspection_priority": "",
        "mechanism_explanation": "",
        "matched_roles": [],
        "consequence_features": [],
        "consequence_lineage": [],
        "matched_consequences": [],
        "candidate_mechanisms": candidate_mechanisms(candidate_evidence),
        "confidence_ranking": confidence_ranking(candidate_evidence),
        "inference_mode": "UNSUPPORTED",
        "source_tracebacks": [],
        "candidate_evidence": candidate_evidence,
        "fail_closed_reason": reason,
    }


def render_answer(mechanism: dict[str, Any], intent: str) -> str:
    if intent == "ranking":
        return str(mechanism.get("similarity_statement", mechanism.get("mechanism_name", "")))
    if intent == "inspection":
        return str(mechanism.get("inspection_priority", ""))
    if intent == "component_category":
        return str(mechanism.get("component_category", ""))
    if intent == "effect":
        return str(mechanism.get("direct_effect", ""))
    if intent == "similarity":
        return str(mechanism.get("similarity_statement", mechanism.get("mechanism_name", "")))
    return str(mechanism.get("mapping_statement", mechanism.get("mechanism_name", "")))


def choose_candidate(question: str, state: dict[str, Any]) -> dict[str, Any]:
    mechanisms = state.get("mechanisms", {})
    if not isinstance(mechanisms, dict) or not mechanisms:
        return fail_closed(question, "no_mechanisms_loaded")

    analysis_text = observed_system(question)
    candidates = [
        score_mechanism(str(mechanism_id), mechanism, analysis_text)
        for mechanism_id, mechanism in mechanisms.items()
        if isinstance(mechanism, dict)
    ]
    if not candidates:
        return fail_closed(question, "no_valid_mechanisms_loaded")

    candidates.sort(key=lambda row: (-row["score"], -row["matched_role_count"], row["mechanism_id"]))
    compact_evidence = [
        {
            "mechanism_id": row["mechanism_id"],
            "score": row["score"],
            "matched_role_count": row["matched_role_count"],
            "matched_cue_count": row["matched_cue_count"],
            "matched_consequence_count": row.get("matched_consequence_count", 0),
            "matched_consequence_cue_count": row.get("matched_consequence_cue_count", 0),
            "matched_roles": [role["role_id"] for role in row["matched_roles"]],
            "matched_consequences": [
                feature["feature_id"] for feature in row.get("matched_consequences", [])
            ],
        }
        for row in candidates
    ]
    top = candidates[0]
    mechanism = top["mechanism"]
    minimum_roles = mechanism.get("required_min_roles", 3)
    if not isinstance(minimum_roles, int) or minimum_roles < 1:
        minimum_roles = 3
    minimum_score = mechanism.get("minimum_score", float(minimum_roles))
    if not isinstance(minimum_score, (int, float)):
        minimum_score = float(minimum_roles)

    role_supported = top["matched_role_count"] >= minimum_roles and top["role_score"] >= float(minimum_score)

    minimum_consequence_features = mechanism.get("required_min_consequence_features", 10**6)
    if not isinstance(minimum_consequence_features, int) or minimum_consequence_features < 1:
        minimum_consequence_features = 10**6
    minimum_consequence_score = mechanism.get("minimum_consequence_score", float(minimum_consequence_features))
    if not isinstance(minimum_consequence_score, (int, float)):
        minimum_consequence_score = float(minimum_consequence_features)
    consequence_supported = (
        top["matched_consequence_count"] >= minimum_consequence_features
        and top["consequence_score"] >= float(minimum_consequence_score)
    )

    intent = question_intent(question)
    ranking_supported = (
        intent == "ranking"
        and top["score"] > 0.0
        and top["matched_role_count"] + top["matched_consequence_count"] >= 2
    )

    if not role_supported and not consequence_supported and not ranking_supported:
        return fail_closed(question, "insufficient_motif_support", compact_evidence)

    if len(candidates) > 1:
        runner_up = candidates[1]
        if top.get("matched_consequence_count", 0) or runner_up.get("matched_consequence_count", 0):
            top_evidence_count = top["matched_role_count"] + top.get("matched_consequence_count", 0)
            runner_evidence_count = runner_up["matched_role_count"] + runner_up.get("matched_consequence_count", 0)
            ambiguous_role_tie = runner_evidence_count == top_evidence_count
        else:
            ambiguous_role_tie = runner_up["matched_role_count"] == top["matched_role_count"]
        ambiguous_score_gap = top["score"] - runner_up["score"] < 0.35
        if intent != "ranking" and ambiguous_role_tie and ambiguous_score_gap:
            return fail_closed(question, "ambiguous_mechanism_match", compact_evidence)

    matched_roles = top["matched_roles"]
    matched_consequences = top.get("matched_consequences", [])
    role_count = len(matched_roles)
    cue_count = top["matched_cue_count"]
    consequence_count = len(matched_consequences)
    consequence_cue_count = top.get("matched_consequence_cue_count", 0)
    if consequence_count:
        confidence = min(
            0.95,
            0.28
            + 0.1 * role_count
            + 0.09 * consequence_count
            + 0.018 * min(cue_count + consequence_cue_count, 10),
        )
    else:
        confidence = min(0.95, 0.32 + 0.12 * role_count + 0.025 * min(cue_count, 8))
    mechanism_name = str(mechanism.get("mechanism_name", top["mechanism_id"]))
    if ranking_supported and not role_supported and not consequence_supported:
        inference_mode = "RELATIONAL_INFERENCE"
    elif consequence_supported and not role_supported:
        inference_mode = "CONSEQUENCE_INFERENCE"
    elif consequence_supported and consequence_count >= 2:
        inference_mode = "RELATIONAL_INFERENCE"
    else:
        inference_mode = "ROLE_MATCH"
    return {
        "question": question,
        "observed_system": observed_system(question),
        "identified_mechanism": top["mechanism_id"],
        "evidence_features": evidence_features(matched_roles),
        "rejected_mechanisms": rejected_mechanisms(candidates, top["mechanism_id"]),
        "motif_lineage": motif_lineage(top["mechanism_id"], mechanism, matched_roles),
        "confidence": round(confidence, 2),
        "supporting_motifs": [role["motif"] for role in matched_roles]
        + [feature["motif"] for feature in matched_consequences],
        "source_mechanism": mechanism_name,
        "transfer_confidence": round(confidence, 2),
        "answer": render_answer(mechanism, intent),
        "status": "ANSWERED",
        "component_category": str(mechanism.get("component_category", "")),
        "inspection_priority": str(mechanism.get("inspection_priority", "")),
        "mechanism_explanation": str(mechanism.get("mechanism_explanation", "")),
        "matched_roles": matched_roles,
        "consequence_features": consequence_features(matched_consequences),
        "consequence_lineage": consequence_lineage(top["mechanism_id"], mechanism, matched_consequences),
        "matched_consequences": matched_consequences,
        "candidate_mechanisms": candidate_mechanisms(compact_evidence),
        "confidence_ranking": confidence_ranking(compact_evidence),
        "inference_mode": inference_mode,
        "source_tracebacks": source_tracebacks(top["mechanism_id"], mechanism),
        "candidate_evidence": compact_evidence,
        "fail_closed_reason": "",
    }


def answer_question(question: str, state: dict[str, Any]) -> dict[str, Any]:
    return choose_candidate(question, state)


def recall_rank_rows(result: dict[str, Any], candidates: list[str]) -> list[dict[str, Any]]:
    ranking = result.get("confidence_ranking", [])
    if isinstance(ranking, list) and ranking:
        return [
            {
                "rank": row.get("rank", index),
                "mechanism_id": row.get("mechanism_id", ""),
                "score": row.get("score", 0.0),
                "relative_confidence": row.get("relative_confidence", 0.0),
                "source": "local_state_scoring_with_pond_recall_filter",
            }
            for index, row in enumerate(ranking, start=1)
            if isinstance(row, dict)
        ]
    return [
        {
            "rank": index,
            "mechanism_id": mechanism_id,
            "score": 0.0,
            "relative_confidence": 0.0,
            "source": "pond_recall_candidate_only",
        }
        for index, mechanism_id in enumerate(candidates, start=1)
    ]


def recall_supported_answer(
    question: str,
    state: dict[str, Any],
    recall: dict[str, Any],
    candidates: list[str],
    reason: str,
) -> dict[str, Any]:
    mechanism_id = candidates[0] if candidates else ""
    mechanisms = state.get("mechanisms", {})
    mechanism = mechanisms.get(mechanism_id, {}) if isinstance(mechanisms, dict) else {}
    if not mechanism_id or not isinstance(mechanism, dict) or not mechanism:
        result = fail_closed(question, "recalled_candidate_not_in_local_state")
    else:
        mechanism_name = str(mechanism.get("mechanism_name", mechanism_id))
        motifs = [str(motif) for motif in recall_list(recall, "returned_motifs", "recalled_motifs")]
        lineages = [str(lineage) for lineage in recall_list(recall, "returned_lineages", "lineage_refs", "selected_path_ids")]
        lineage_hashes = [str(lineage_hash) for lineage_hash in recall_list(recall, "lineage_hashes")]
        core_motifs = mechanism.get("core_motif", [])
        if not isinstance(core_motifs, list):
            core_motifs = []
        result = {
            "question": question,
            "observed_system": observed_system(question),
            "identified_mechanism": mechanism_id,
            "evidence_features": [
                {
                    "role_id": f"recalled_motif_{index:02d}",
                    "motif": motif,
                    "matched_cues": [],
                    "evidence_source": "pond_recall",
                }
                for index, motif in enumerate(motifs, start=1)
            ],
            "rejected_mechanisms": [
                {
                    "mechanism_id": other,
                    "score": 0.0,
                    "matched_role_count": 0,
                    "matched_cue_count": 0,
                    "matched_consequence_count": 0,
                    "matched_consequence_cue_count": 0,
                    "matched_roles": [],
                    "matched_consequences": [],
                    "rejection_reason": "not_top_recalled_candidate",
                }
                for other in candidates[1:]
            ],
            "motif_lineage": [
                {
                    "lesson_id": str(mechanism.get("lesson_id", "")),
                    "mechanism_id": mechanism_id,
                    "mechanism_name": mechanism_name,
                    "role_id": f"recalled_motif_{index:02d}",
                    "motif": motif,
                    "matched_cues": [],
                    "lineage_refs": lineages,
                    "lineage_hashes": lineage_hashes,
                }
                for index, motif in enumerate(motifs, start=1)
            ],
            "confidence": 0.62,
            "supporting_motifs": motifs or [str(motif) for motif in core_motifs],
            "source_mechanism": mechanism_name,
            "transfer_confidence": 0.62,
            "answer": render_answer(mechanism, question_intent(question)),
            "status": "ANSWERED",
            "component_category": str(mechanism.get("component_category", "")),
            "inspection_priority": str(mechanism.get("inspection_priority", "")),
            "mechanism_explanation": str(mechanism.get("mechanism_explanation", "")),
            "matched_roles": [],
            "consequence_features": [],
            "consequence_lineage": [],
            "matched_consequences": [],
            "candidate_mechanisms": candidates,
            "confidence_ranking": recall_rank_rows({"confidence_ranking": []}, candidates),
            "inference_mode": "POND_RECALL",
            "source_tracebacks": source_tracebacks(mechanism_id, mechanism),
            "candidate_evidence": [],
            "fail_closed_reason": "",
            "recall_support_reason": reason,
        }
    return attach_recall_metadata(result, recall, candidates)


def attach_recall_metadata(result: dict[str, Any], recall: dict[str, Any], candidates: list[str]) -> dict[str, Any]:
    output = dict(result)
    used_lineages = recall_list(recall, "returned_lineages", "lineage_refs", "selected_path_ids")
    used_motifs = recall_list(recall, "returned_motifs", "recalled_motifs")
    output.update(
        {
            "case_id": str(recall.get("case_id", "")),
            "ranked_candidates": recall_rank_rows(output, candidates),
            "used_pond_recall": True,
            "used_recalled_lineages": used_lineages,
            "used_recalled_motifs": used_motifs,
            "used_recalled_lineage_hashes": recall_list(recall, "lineage_hashes"),
            "recall_used_by_cli": True,
            "pond_recall_status": str(recall.get("mcp_status", recall.get("adapter_status", ""))),
            "pond_recall_reason": str(recall.get("reason", "")),
        }
    )
    return output


def answer_question_with_recall(question: str, state: dict[str, Any], recall: dict[str, Any]) -> dict[str, Any]:
    candidates = recall_candidates(recall)
    if not candidates:
        return attach_recall_metadata(
            fail_closed(question, "no_recalled_mechanism_candidates"),
            recall,
            candidates,
        )
    if not recall_traceable(recall):
        return attach_recall_metadata(
            fail_closed(question, "pond_recall_not_traceable"),
            recall,
            candidates,
        )

    narrowed_state = state_with_recalled_candidates(state, candidates)
    result = choose_candidate(question, narrowed_state)
    if result.get("status") == "ANSWERED":
        return attach_recall_metadata(result, recall, candidates)

    if len(candidates) == 1:
        return recall_supported_answer(
            question,
            narrowed_state,
            recall,
            candidates,
            "single_traceable_recalled_candidate_with_local_mechanism_state",
        )
    return attach_recall_metadata(result, recall, candidates)


def run_map(args: argparse.Namespace) -> int:
    recall = load_recall(Path(args.pond_recall)) if args.pond_recall else {}
    pond_path = args.pond or recall.get("pond_state_path", "")
    state = load_pond(Path(pond_path)) if pond_path else empty_state("missing_pond")
    if recall:
        result = answer_question_with_recall(args.question, state, recall)
    else:
        result = answer_question(args.question, state)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=True))
    else:
        if result["status"] == "ANSWERED":
            print(result["identified_mechanism"])
        else:
            print(result["status"])
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python3 -m operational_cognition.cli.mechanism_pond")
    subparsers = parser.add_subparsers(dest="command", required=True)
    map_parser = subparsers.add_parser("map", help="Map an observed system to a learned mechanism.")
    map_parser.add_argument("--pond", required=False, help="Path to a pond directory or pond_state.json file.")
    map_parser.add_argument("--pond-recall", required=False, help="Path to per-case pond recall JSON.")
    map_parser.add_argument("--question", required=True, help="Question or observed-system prompt.")
    map_parser.add_argument("--json", action="store_true", help="Emit JSON.")
    map_parser.set_defaults(func=run_map)

    answer_parser = subparsers.add_parser("answer", help="Alias for map.")
    answer_parser.add_argument("--pond", required=False, help="Path to a pond directory or pond_state.json file.")
    answer_parser.add_argument("--pond-recall", required=False, help="Path to per-case pond recall JSON.")
    answer_parser.add_argument("--question", required=True, help="Question or observed-system prompt.")
    answer_parser.add_argument("--json", action="store_true", help="Emit JSON.")
    answer_parser.set_defaults(func=run_map)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
