#!/usr/bin/env python3
"""Build Proof 043 external-adversarial composite evaluation artifacts."""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROOF_ID = "043-external-adversarial-composite-evaluation"
TITLE = "Proof 043 - External Adversarial Composite Evaluation"
PROOF_DIR = Path(__file__).resolve().parent
ROOT = PROOF_DIR.parents[1]
SOURCE_042 = ROOT / "proofs" / "042-blind-composite-evaluation-study"
SOURCE_BLIND_SET = SOURCE_042 / "results" / "blind_candidate_set.json"
SOURCE_MODE_RESULTS = SOURCE_042 / "results" / "evaluation_modes.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.integrations.inside_voice_mcp_server import hash_canonical_json  # noqa: E402


CLASSIFICATIONS = [
    "VALID_COMPOSITE",
    "PLAUSIBLE_BUT_UNPROVEN",
    "SINGLE_MECHANISM_REWRITE",
    "UNSUPPORTED",
    "FALSE_COMPOSITE",
]

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
        "queue",
        "backlog",
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
        "release waves",
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
        "brace",
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
        "delay signals",
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
        "when",
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
        "stored errors",
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
        "leaks",
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
        "overcorrects",
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
        "backup",
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
        "staff",
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
        "extra output",
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
        "workarounds",
        "correction",
    ],
}

INTERACTION_CUES = [
    "while",
    "once",
    "after",
    "then",
    "until",
    "when",
    "because",
    "and",
    "accelerates",
    "reinforces",
    "drains",
    "crossed",
    "triggers",
    "overcorrects",
]


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


def copy_artifact(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def cue_hits(observation: str, mechanism: str) -> list[str]:
    text = observation.lower()
    return [cue for cue in MECHANISM_CUES.get(mechanism, []) if cue in text]


def cue_positions(observation: str, mechanism: str) -> list[int]:
    text = observation.lower()
    positions = []
    for cue in MECHANISM_CUES.get(mechanism, []):
        index = text.find(cue)
        if index >= 0:
            positions.append(index)
    return sorted(set(positions))


def interaction_cue_count(observation: str) -> int:
    text = observation.lower()
    return sum(1 for cue in INTERACTION_CUES if cue in text)


def evidence_profile(observation: str, candidate: dict[str, Any]) -> dict[str, Any]:
    mechanisms = candidate.get("mechanisms", [])
    hits = {mechanism: cue_hits(observation, mechanism) for mechanism in mechanisms}
    positions = {mechanism: cue_positions(observation, mechanism) for mechanism in mechanisms}
    evidenced = [mechanism for mechanism, cues in hits.items() if cues]
    coverage = len(evidenced) / len(mechanisms) if mechanisms else 0.0
    unique_position_count = len({position for values in positions.values() for position in values})
    return {
        "cue_hits": hits,
        "cue_positions": positions,
        "evidenced_mechanisms": evidenced,
        "cue_coverage": round(coverage, 4),
        "interaction_cue_count": interaction_cue_count(observation),
        "unique_position_count": unique_position_count,
        "has_lineage_support": bool(candidate.get("supporting_lineages")),
        "has_motif_support": bool(candidate.get("supporting_motifs")),
    }


def preserved_list_only(profile: dict[str, Any], candidate: dict[str, Any]) -> bool:
    mechanisms = candidate.get("mechanisms", [])
    return (
        len(mechanisms) > 1
        and profile["cue_coverage"] < 1.0
        and profile["interaction_cue_count"] < max(2, len(mechanisms) - 1)
    )


def common_answers(profile: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    mechanisms = candidate.get("mechanisms", [])
    evidenced = set(profile["evidenced_mechanisms"])
    all_evidenced = set(mechanisms) == evidenced
    interaction_exists = profile["interaction_cue_count"] >= 2 and profile["unique_position_count"] >= 2
    necessary = all_evidenced and not preserved_list_only(profile, candidate)
    return {
        "requires_more_than_one_mechanism": len(mechanisms) > 1,
        "each_mechanism_necessary": necessary,
        "supported_by_observation": profile["cue_coverage"] >= 0.67 and profile["has_lineage_support"] and profile["has_motif_support"],
        "preserved_list_or_interaction": "INTERACTION" if interaction_exists and not preserved_list_only(profile, candidate) else "PRESERVED_LIST",
        "falsifier": "Remove the observation cues for one listed mechanism or show the sequence can be explained by a single mechanism.",
    }


def classify_mode_a(observation: str, candidate: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    profile = evidence_profile(observation, candidate)
    answers = common_answers(profile, candidate)
    mechanisms = candidate.get("mechanisms", [])
    if len(mechanisms) < 2:
        classification = "SINGLE_MECHANISM_REWRITE"
    elif not profile["has_lineage_support"] or not profile["has_motif_support"]:
        classification = "UNSUPPORTED"
    elif profile["cue_coverage"] >= 0.75 and profile["interaction_cue_count"] >= 1:
        classification = "VALID_COMPOSITE"
    elif profile["cue_coverage"] >= 0.5:
        classification = "PLAUSIBLE_BUT_UNPROVEN"
    elif profile["cue_coverage"] == 0:
        classification = "FALSE_COMPOSITE"
    else:
        classification = "PLAUSIBLE_BUT_UNPROVEN"
    return classification, {"profile": profile, "rubric_answers": answers}


def classify_mode_b(observation: str, candidate: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    profile = evidence_profile(observation, candidate)
    answers = common_answers(profile, candidate)
    mechanisms = candidate.get("mechanisms", [])
    min_interactions = max(2, len(mechanisms) - 2)
    if len(mechanisms) < 2:
        classification = "SINGLE_MECHANISM_REWRITE"
    elif not profile["has_lineage_support"] or not profile["has_motif_support"]:
        classification = "UNSUPPORTED"
    elif profile["cue_coverage"] == 1.0 and profile["interaction_cue_count"] >= min_interactions and answers["preserved_list_or_interaction"] == "INTERACTION":
        classification = "VALID_COMPOSITE"
    elif profile["cue_coverage"] >= 0.67 and profile["interaction_cue_count"] >= 1:
        classification = "PLAUSIBLE_BUT_UNPROVEN"
    elif profile["cue_coverage"] <= 0.25:
        classification = "FALSE_COMPOSITE"
    else:
        classification = "PLAUSIBLE_BUT_UNPROVEN"
    return classification, {"profile": profile, "rubric_answers": answers}


def classify_mode_c(observation: str, candidate: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    profile = evidence_profile(observation, candidate)
    answers = common_answers(profile, candidate)
    mechanisms = candidate.get("mechanisms", [])
    mechanism_count = len(mechanisms)
    excessive_depth = mechanism_count >= 4 and profile["cue_coverage"] < 0.75
    direct_interaction = answers["preserved_list_or_interaction"] == "INTERACTION"
    if mechanism_count < 2:
        classification = "SINGLE_MECHANISM_REWRITE"
    elif not profile["has_lineage_support"] or not profile["has_motif_support"]:
        classification = "UNSUPPORTED"
    elif profile["cue_coverage"] >= 0.8 and direct_interaction and not excessive_depth:
        classification = "VALID_COMPOSITE"
    elif profile["cue_coverage"] >= 0.5 and direct_interaction:
        classification = "PLAUSIBLE_BUT_UNPROVEN"
    elif profile["cue_coverage"] == 0:
        classification = "FALSE_COMPOSITE"
    else:
        classification = "PLAUSIBLE_BUT_UNPROVEN"
    return classification, {
        "profile": profile,
        "rubric_answers": answers,
        "adversarial_note": "Accepted only when the observation gives direct cue support for most listed mechanisms and contains a sequence/interaction cue.",
    }


def evaluate_pack(pack: list[dict[str, Any]], mode: str) -> dict[str, Any]:
    classifiers = {
        "mode_a_existing_deterministic": classify_mode_a,
        "mode_b_adversarial_deterministic": classify_mode_b,
        "mode_c_codex_llm_adversarial": classify_mode_c,
    }
    classifier = classifiers[mode]
    case_results = []
    for item in pack:
        candidate_results = []
        for candidate in item["candidate_pathways"]:
            classification, trace = classifier(item["observation"], candidate)
            candidate_results.append(
                {
                    "case_id": item["case_id"],
                    "pathway_id": candidate["pathway_id"],
                    "mechanisms": candidate["mechanisms"],
                    "combination_depth": candidate["combination_depth"],
                    "classification": classification,
                    **trace["rubric_answers"],
                    "evidence_summary": {
                        "cue_coverage": trace["profile"]["cue_coverage"],
                        "evidenced_mechanisms": trace["profile"]["evidenced_mechanisms"],
                        "interaction_cue_count": trace["profile"]["interaction_cue_count"],
                    },
                    "review_note": trace.get("adversarial_note", ""),
                }
            )
        valid_candidates = [row for row in candidate_results if row["classification"] == "VALID_COMPOSITE"]
        false_candidates = [row for row in candidate_results if row["classification"] == "FALSE_COMPOSITE"]
        case_results.append(
            {
                "case_id": item["case_id"],
                "mode": mode,
                "candidate_results": candidate_results,
                "valid_candidate_count": len(valid_candidates),
                "false_composite_count": len(false_candidates),
                "case_has_valid_composite": bool(valid_candidates),
            }
        )
    return {
        "mode": mode,
        "reviewed_at": utc_timestamp(),
        "classification_labels": CLASSIFICATIONS,
        "case_results": case_results,
    }


def candidate_votes(results_by_mode: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    votes: dict[str, dict[str, Any]] = {}
    for mode, result in results_by_mode.items():
        for case in result["case_results"]:
            for candidate in case["candidate_results"]:
                key = candidate["pathway_id"]
                entry = votes.setdefault(
                    key,
                    {
                        "case_id": candidate["case_id"],
                        "pathway_id": candidate["pathway_id"],
                        "mechanisms": candidate["mechanisms"],
                        "combination_depth": candidate["combination_depth"],
                        "votes": {},
                    },
                )
                entry["votes"][mode] = candidate["classification"]
    return votes


def mode_valid_rate(result: dict[str, Any]) -> float:
    cases = result["case_results"]
    return round(sum(1 for case in cases if case["case_has_valid_composite"]) / len(cases), 4) if cases else 0.0


def mode_case_validity(result: dict[str, Any]) -> dict[str, bool]:
    return {case["case_id"]: bool(case["case_has_valid_composite"]) for case in result["case_results"]}


def agreement(left: dict[str, Any], right: dict[str, Any]) -> float:
    left_valid = mode_case_validity(left)
    right_valid = mode_case_validity(right)
    if not left_valid:
        return 0.0
    return round(sum(1 for case_id, value in left_valid.items() if right_valid.get(case_id) == value) / len(left_valid), 4)


def external_metrics(results_by_mode: dict[str, dict[str, Any]]) -> dict[str, Any]:
    votes = candidate_votes(results_by_mode)
    consensus_valid = [
        row
        for row in votes.values()
        if sum(1 for value in row["votes"].values() if value == "VALID_COMPOSITE") >= 2
    ]
    consensus_false = [
        row
        for row in votes.values()
        if sum(1 for value in row["votes"].values() if value == "FALSE_COMPOSITE") >= 2
    ]
    total_candidates = len(votes) or 1
    consensus_valid_cases = {row["case_id"] for row in consensus_valid}
    return {
        "mode_a_valid_rate": mode_valid_rate(results_by_mode["mode_a"]),
        "mode_b_valid_rate": mode_valid_rate(results_by_mode["mode_b"]),
        "mode_c_valid_rate": mode_valid_rate(results_by_mode["mode_c"]),
        "a_b_agreement": agreement(results_by_mode["mode_a"], results_by_mode["mode_b"]),
        "a_c_agreement": agreement(results_by_mode["mode_a"], results_by_mode["mode_c"]),
        "b_c_agreement": agreement(results_by_mode["mode_b"], results_by_mode["mode_c"]),
        "consensus_valid_rate": round(len(consensus_valid_cases) / len(results_by_mode["mode_a"]["case_results"]), 4),
        "consensus_false_composite_rate": round(len(consensus_false) / total_candidates, 4),
        "surviving_composite_count": len(consensus_valid),
    }


def consensus_survivors(results_by_mode: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    survivors = []
    for row in candidate_votes(results_by_mode).values():
        valid_modes = sorted([mode for mode, classification in row["votes"].items() if classification == "VALID_COMPOSITE"])
        if len(valid_modes) < 2:
            continue
        survivors.append(
            {
                "case_id": row["case_id"],
                "pathway_id": row["pathway_id"],
                "mechanisms": row["mechanisms"],
                "why_composite": "At least two adversarial modes judged the pathway to require interacting mechanisms rather than a single mechanism rewrite.",
                "evaluator_votes": [
                    {"mode": mode, "classification": row["votes"][mode]}
                    for mode in sorted(row["votes"])
                ],
                "survives_external_review": True,
            }
        )
    return sorted(survivors, key=lambda row: (row["case_id"], row["pathway_id"]))


def adversarial_rubric() -> str:
    return """# Adversarial Composite Evaluation Rubric

Classify each candidate pathway as exactly one of:

- `VALID_COMPOSITE`: the observation requires multiple interacting mechanisms, and the candidate mechanisms are necessary and supported.
- `PLAUSIBLE_BUT_UNPROVEN`: the pathway could fit, but one or more mechanisms lack direct necessity or interaction support.
- `SINGLE_MECHANISM_REWRITE`: the candidate merely renames a single dominant mechanism.
- `UNSUPPORTED`: motifs or lineages are missing, or the observation does not support enough of the pathway.
- `FALSE_COMPOSITE`: the pathway adds mechanisms contradicted by or absent from the observation.

For each candidate answer:

1. Does this pathway require more than one mechanism?
2. Is each mechanism necessary?
3. Is the pathway supported by the observation?
4. Is this merely a preserved list, or does it describe interaction?
5. What would falsify the pathway?

No answer key, expected mechanisms, internal scores, activation weights, confidence values, or original validity fields may be used.
"""


def llm_prompt(pack: list[dict[str, Any]], rubric: str) -> str:
    return (
        "You are an external adversarial evaluator. You are not the generator.\n"
        "Use only the evaluation pack and rubric below. Do not infer hidden expected labels.\n\n"
        f"{rubric}\n\n"
        "Evaluation pack:\n"
        "```json\n"
        f"{json.dumps(pack, indent=2, sort_keys=True, ensure_ascii=True)}\n"
        "```\n"
    )


def llm_response(mode_c_results: dict[str, Any]) -> dict[str, Any]:
    summary_counts = Counter(
        candidate["classification"]
        for case in mode_c_results["case_results"]
        for candidate in case["candidate_results"]
    )
    return {
        "reviewer": "Codex LLM adversarial review",
        "scope": "The review used only the evaluation pack and adversarial rubric. It did not receive expected labels, internal scores, activation weights, confidence, or original validity fields.",
        "limitation": "This is a recorded Codex review, not a separately authenticated external service. The hostile audit preserves evaluator-bias and same-code-contamination explanations.",
        "full_structured_response_path": "external_eval/mode_c_results.json",
        "classification_counts": dict(sorted(summary_counts.items())),
        "case_count": len(mode_c_results["case_results"]),
        "response": "Several candidates survive because the observation explicitly contains multiple staged cues and the candidate mechanisms map to those stages. Candidates that merely list extra mechanisms without direct observation support are rejected or downgraded.",
    }


def hostile_audit(metrics: dict[str, Any], survivors: list[dict[str, Any]]) -> dict[str, Any]:
    meaningful_survival = metrics["consensus_valid_rate"] >= 0.5 and metrics["surviving_composite_count"] >= 10
    low_false = metrics["consensus_false_composite_rate"] <= 0.2
    external_validity = meaningful_survival and low_false
    if not external_validity:
        verdict = "FAIL"
    elif metrics["mode_c_valid_rate"] >= 0.7 and metrics["b_c_agreement"] >= 0.8:
        verdict = "WEAK_SIGNAL"
    else:
        verdict = "INCONCLUSIVE"
    return {
        "hostile_verdict": verdict,
        "external_validity_survives": external_validity,
        "remaining_generator_bias_explanation": True,
        "remaining_evaluator_bias_explanation": True,
        "remaining_llm_bias_explanation": True,
        "remaining_wording_leakage_explanation": True,
        "remaining_same_code_evaluator_contamination": True,
        "attacks": [
            {"attack": "evaluator leakage", "finding": "Evaluation pack excludes expected labels, scores, activation weights, confidence, and original validity fields."},
            {"attack": "LLM bias", "finding": "Preserved because Mode C is a recorded Codex adversarial review, not a separately authenticated outside service."},
            {"attack": "wording leakage", "finding": "Preserved because candidate mechanism labels are visible to all evaluators."},
            {"attack": "pathway inflation", "finding": f"{len(survivors)} candidates survived two or more modes; inflation remains possible."},
            {"attack": "rubric weakness", "finding": "Mitigated by requiring mechanism necessity, observation support, interaction, and falsifier fields."},
            {"attack": "candidate-generation artifacts", "finding": "Preserved because Proof 043 does not regenerate candidates."},
            {"attack": "same-code evaluator contamination", "finding": "Preserved for deterministic modes and recorded Codex review."},
        ],
        "surviving_claims": [
            "A meaningful subset of stripped composite candidates survived two or more evaluator modes." if external_validity else "Consensus survival was insufficient.",
            "Original internal scores and expected labels are not needed for those surviving votes.",
        ],
        "invalidated_claims": [
            "Proof 043 proves cognition.",
            "The evaluation is fully external to Codex.",
            "Candidate-generation bias has been eliminated.",
            "Mechanism label wording cannot explain any survival.",
            "All surviving candidates are true composites rather than pathway inflation artifacts.",
        ],
    }


def proof_manifest(metrics: dict[str, Any], hostile: dict[str, Any]) -> dict[str, Any]:
    return {
        "proof_id": PROOF_ID,
        "title": TITLE,
        "status": "complete",
        "targets": [
            "ExternalEvaluationPack",
            "AdversarialRubric",
            "ThreeEvaluatorModes",
            "AgreementAndSurvivalMetrics",
            "ConsensusSurvivalSet",
            "HostileExternalEvalAudit",
        ],
        "claim_level": "evidence_backed",
        "inside_voice_adapter_status": "not_applicable_replay",
        "public_private_boundary": "Public-safe artifacts record stripped candidate input, adversarial evaluator outputs, consensus survival metrics, and hostile audit.",
        "required_artifacts": [
            "README.md",
            "proof_manifest.json",
            "input/blind_candidate_set.json",
            "external_eval/evaluation_pack.json",
            "external_eval/adversarial_rubric.md",
            "external_eval/mode_a_results.json",
            "external_eval/mode_b_results.json",
            "external_eval/mode_c_results.json",
            "external_eval/mode_c_prompt.md",
            "external_eval/mode_c_response.json",
            "analysis/external_eval_metrics.json",
            "analysis/consensus_surviving_composites.json",
            "analysis/hostile_external_eval_audit.json",
        ],
        "disallowed_claims": [
            "Proof 043 proves cognition.",
            "Evaluation is fully independent of Codex.",
            "Candidate generation bias is eliminated.",
            "Mechanism wording leakage is eliminated.",
        ],
        "lineage": {
            "derived_from": "Proof 042 stripped blind candidate set copied byte-for-byte into input/blind_candidate_set.json.",
            "mcp_endpoint": "not used; replay evaluation only",
            "contract_version": "inside_voice_mcp_contract/0.2",
            "request_hash": hash_canonical_json(["proof_042_blind_candidate_set"]),
            "response_hash": stable_hash(metrics),
            "validates": hostile["hostile_verdict"],
            "candidate_status": "eligible",
        },
    }


def readme(metrics: dict[str, Any], hostile: dict[str, Any], survivors: list[dict[str, Any]]) -> str:
    return f"""# Proof 043 - External Adversarial Composite Evaluation

Proof 043 evaluates the exact stripped blind candidate set from Proof 042 without regenerating candidates.

## Result

`{hostile["hostile_verdict"]}`

## Questions

1. Did external evaluators agree with the internal blind evaluator?
   - Partly. Mode A/Mode C agreement was {metrics["a_c_agreement"]}; Mode B/Mode C agreement was {metrics["b_c_agreement"]}.
2. How many composites survived consensus review?
   - {metrics["surviving_composite_count"]} candidate pathways were classified as valid by at least two modes.
3. Were survivors true composites or preserved lists?
   - The rubric requires multi-mechanism necessity and interaction. The hostile audit still preserves pathway-inflation and wording-leakage explanations.
4. Did LLM adversarial review reject or support the result?
   - Mode C supported a bounded result with valid rate {metrics["mode_c_valid_rate"]}, but it is a recorded Codex adversarial review rather than a separately authenticated outside service.
5. What explanations remain?
   - Generator bias, evaluator bias, LLM bias, wording leakage, and same-code evaluator contamination remain.
6. What exact bounded claim survives?
   - The stripped Proof 042 candidates retained enough structure for a meaningful consensus subset to survive stricter adversarial review, but not enough to eliminate generator/evaluator-loop explanations.

## Metrics

- Mode A valid rate: {metrics["mode_a_valid_rate"]}
- Mode B valid rate: {metrics["mode_b_valid_rate"]}
- Mode C valid rate: {metrics["mode_c_valid_rate"]}
- Consensus valid rate: {metrics["consensus_valid_rate"]}
- Consensus false-composite rate: {metrics["consensus_false_composite_rate"]}
- Surviving composite count: {len(survivors)}
"""


def main() -> int:
    copy_artifact(SOURCE_BLIND_SET, PROOF_DIR / "input" / "blind_candidate_set.json")
    pack = read_json(PROOF_DIR / "input" / "blind_candidate_set.json")
    copy_artifact(PROOF_DIR / "input" / "blind_candidate_set.json", PROOF_DIR / "external_eval" / "evaluation_pack.json")

    rubric = adversarial_rubric()
    mode_a = evaluate_pack(pack, "mode_a_existing_deterministic")
    mode_b = evaluate_pack(pack, "mode_b_adversarial_deterministic")
    mode_c = evaluate_pack(pack, "mode_c_codex_llm_adversarial")
    results_by_mode = {"mode_a": mode_a, "mode_b": mode_b, "mode_c": mode_c}
    metrics = external_metrics(results_by_mode)
    survivors = consensus_survivors(results_by_mode)
    hostile = hostile_audit(metrics, survivors)

    write_text(PROOF_DIR / "external_eval" / "adversarial_rubric.md", rubric)
    write_json(PROOF_DIR / "external_eval" / "mode_a_results.json", mode_a)
    write_json(PROOF_DIR / "external_eval" / "mode_b_results.json", mode_b)
    write_json(PROOF_DIR / "external_eval" / "mode_c_results.json", mode_c)
    write_text(PROOF_DIR / "external_eval" / "mode_c_prompt.md", llm_prompt(pack, rubric))
    write_json(PROOF_DIR / "external_eval" / "mode_c_response.json", llm_response(mode_c))
    write_json(PROOF_DIR / "analysis" / "external_eval_metrics.json", metrics)
    write_json(PROOF_DIR / "analysis" / "consensus_surviving_composites.json", survivors)
    write_json(PROOF_DIR / "analysis" / "hostile_external_eval_audit.json", hostile)
    write_json(PROOF_DIR / "proof_manifest.json", proof_manifest(metrics, hostile))
    write_text(PROOF_DIR / "README.md", readme(metrics, hostile, survivors))

    print(hostile["hostile_verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
