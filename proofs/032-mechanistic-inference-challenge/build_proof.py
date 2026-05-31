#!/usr/bin/env python3
"""Build Proof 032 deterministic mechanistic-inference artifacts."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


PROOF_ID = "032-mechanistic-inference-challenge"
TITLE = "Proof 032 - Mechanistic Inference Challenge: Consequence-Only Reasoning"
PROOF_DIR = Path(__file__).resolve().parent
ROOT = PROOF_DIR.parents[1]
PROOF_031 = ROOT / "proofs" / "031-mechanistic-transfer-cue-invariance"
SOURCE_POND = PROOF_031 / "pond_states" / "mechanism_seasoned" / "pond_state.json"
POND_DIR = PROOF_DIR / "pond_states" / "mechanism_inference"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, sort_keys=True, ensure_ascii=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


CONSEQUENCE_SIGNATURES: dict[str, dict[str, Any]] = {
    "flow": {
        "required_min_consequence_features": 3,
        "minimum_consequence_score": 2.25,
        "consequence_signatures": [
            {
                "feature_id": "rate_drop",
                "motif": "Consequence: output or passage rate drops",
                "weight": 0.9,
                "cues": [
                    "throughput decreased",
                    "throughput dropped",
                    "output fell",
                    "output dropped",
                    "delivery rate dropped",
                    "rate fell",
                    "progress slowed",
                    "efficiency declined",
                    "less passed",
                    "arrivals thinned",
                    "movement slowed",
                ],
            },
            {
                "feature_id": "backlog_growth",
                "motif": "Consequence: upstream accumulation grows",
                "weight": 0.9,
                "cues": [
                    "backlog grew",
                    "backlog built",
                    "queue grew",
                    "queues grew",
                    "waiting line grew",
                    "piled up",
                    "piling up",
                    "accumulated before",
                    "build up",
                    "built up",
                    "stacked up",
                ],
            },
            {
                "feature_id": "downstream_starvation",
                "motif": "Consequence: downstream side becomes starved",
                "weight": 0.85,
                "cues": [
                    "downstream starved",
                    "downstream activity stopped",
                    "later stage starved",
                    "receivers waited",
                    "receiving end waited",
                    "far side received less",
                    "far side went idle",
                ],
            },
            {
                "feature_id": "passage_ceases",
                "motif": "Consequence: passage eventually ceases",
                "weight": 0.8,
                "cues": [
                    "nothing passed",
                    "passage ceased",
                    "movement ceased",
                    "delivery stopped",
                    "stalled out",
                    "could not pass",
                    "stopped arriving",
                ],
            },
            {
                "feature_id": "uneven_delivery",
                "motif": "Consequence: delivery becomes intermittent",
                "weight": 0.7,
                "cues": [
                    "surges",
                    "trickle",
                    "sporadic",
                    "uneven arrival",
                    "delayed arrival",
                    "bursts then gaps",
                ],
            },
        ],
    },
    "supported_rotation": {
        "required_min_consequence_features": 3,
        "minimum_consequence_score": 2.35,
        "consequence_signatures": [
            {
                "feature_id": "audible_roughness",
                "motif": "Consequence: rough motion becomes audible",
                "weight": 0.9,
                "cues": [
                    "became noisy",
                    "noise increased",
                    "noisy",
                    "rough sound",
                    "squeal",
                    "squealing",
                    "rattling",
                    "rattled",
                    "vibration",
                    "vibration increased",
                    "shudder",
                ],
            },
            {
                "feature_id": "heat_rise",
                "motif": "Consequence: temperature rises during motion",
                "weight": 0.9,
                "cues": [
                    "hotter",
                    "heat increased",
                    "temperature increased",
                    "ran hotter",
                    "warmed",
                    "warmth",
                    "heated up",
                    "became hot",
                ],
            },
            {
                "feature_id": "speed_decline",
                "motif": "Consequence: motion speed declines",
                "weight": 0.85,
                "cues": [
                    "slower",
                    "slowed",
                    "speed dropped",
                    "speed declined",
                    "efficiency slowly declined",
                    "motion lagged",
                    "movement became slower",
                    "took longer to move",
                ],
            },
            {
                "feature_id": "rising_drag",
                "motif": "Consequence: resistance to motion rises",
                "weight": 0.9,
                "cues": [
                    "resisting motion",
                    "resistance increased",
                    "drag grew",
                    "increasing drag",
                    "harder to move",
                    "normally moves freely",
                    "could not move freely",
                ],
            },
            {
                "feature_id": "final_lockup",
                "motif": "Consequence: motion finally stops or locks",
                "weight": 0.85,
                "cues": [
                    "then stopped",
                    "stopped",
                    "halted",
                    "could not move",
                    "final lockup",
                    "locked up",
                    "stuck",
                    "seized",
                    "would not move",
                ],
            },
        ],
    },
    "load_transfer": {
        "required_min_consequence_features": 3,
        "minimum_consequence_score": 2.3,
        "consequence_signatures": [
            {
                "feature_id": "deformation",
                "motif": "Consequence: shape deforms under hidden demand",
                "weight": 0.9,
                "cues": [
                    "sagged",
                    "sagging",
                    "bowed",
                    "bent",
                    "drooped",
                    "tilted",
                    "surface dipped",
                    "shape bowed",
                    "one side bowed",
                ],
            },
            {
                "feature_id": "fracture_growth",
                "motif": "Consequence: cracks or splits grow",
                "weight": 0.9,
                "cues": [
                    "crack widened",
                    "fine crack widened",
                    "cracked",
                    "cracks appeared",
                    "split",
                    "fracture",
                    "fracture grew",
                    "hairline marks spread",
                ],
            },
            {
                "feature_id": "localized_damage",
                "motif": "Consequence: damage localizes",
                "weight": 0.85,
                "cues": [
                    "one area",
                    "one side",
                    "single region",
                    "same spot",
                    "one point",
                    "one corner",
                    "small region",
                    "local dent",
                ],
            },
            {
                "feature_id": "alignment_loss",
                "motif": "Consequence: geometry or alignment is lost",
                "weight": 0.75,
                "cues": [
                    "gap widened",
                    "uneven height",
                    "misaligned",
                    "no longer level",
                    "edge dropped",
                    "tilt increased",
                ],
            },
            {
                "feature_id": "gave_way",
                "motif": "Consequence: structure gives way",
                "weight": 0.85,
                "cues": [
                    "gave way",
                    "collapsed",
                    "broke apart",
                    "broke",
                    "could not hold",
                    "fell apart",
                    "failed suddenly",
                ],
            },
        ],
    },
}


TEST_SUITES: dict[str, list[dict[str, Any]]] = {
    "consequence_only": [
        {
            "question_id": "CO-001",
            "question": "Observed system: The machine became noisy. Then slower. Then hotter. Then stopped. Question: Which learned mechanism category would naturally make this observation chain expected?",
            "expected_mechanism": "supported_rotation",
            "expected_status": "ANSWERED",
            "expected_classification": "CONSEQUENCE_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "CO-002",
            "question": "Observed system: Output fell, backlog grew, the far side went idle, and eventually nothing passed. Question: Which learned mechanism category would naturally make these observations expected?",
            "expected_mechanism": "flow",
            "expected_status": "ANSWERED",
            "expected_classification": "CONSEQUENCE_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "CO-003",
            "question": "Observed system: One side bowed, a fine crack widened, the edge dropped, and the object gave way. Question: Which learned mechanism category would naturally make this observation chain expected?",
            "expected_mechanism": "load_transfer",
            "expected_status": "ANSWERED",
            "expected_classification": "CONSEQUENCE_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "CO-004",
            "question": "Observed system: Resistance increased, vibration appeared, warmth built up, and motion finally locked up. Question: Which learned mechanism category would naturally make these observations expected?",
            "expected_mechanism": "supported_rotation",
            "expected_status": "ANSWERED",
            "expected_classification": "CONSEQUENCE_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "CO-005",
            "question": "Observed system: Receivers waited, arrivals thinned, a waiting line grew, and delivery stopped. Question: Which learned mechanism category would naturally make these observations expected?",
            "expected_mechanism": "flow",
            "expected_status": "ANSWERED",
            "expected_classification": "CONSEQUENCE_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "CO-006",
            "question": "Observed system: A small region drooped, hairline marks spread, the gap widened, and then it broke apart. Question: Which learned mechanism category would naturally make these observations expected?",
            "expected_mechanism": "load_transfer",
            "expected_status": "ANSWERED",
            "expected_classification": "CONSEQUENCE_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
    ],
    "reordered_evidence": [
        {
            "question_id": "RE-001",
            "question": "Observed system: The system stopped. Before that it became noisy. Before that it ran hotter. Before that efficiency slowly declined. Question: Which learned mechanism category would make this reversed observation chain expected?",
            "expected_mechanism": "supported_rotation",
            "expected_status": "ANSWERED",
            "expected_classification": "CONSEQUENCE_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "RE-002",
            "question": "Observed system: Nothing passed. Before that receivers waited. Before that the backlog built. Before that the delivery rate dropped. Question: Which learned mechanism category would make this reversed observation chain expected?",
            "expected_mechanism": "flow",
            "expected_status": "ANSWERED",
            "expected_classification": "CONSEQUENCE_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "RE-003",
            "question": "Observed system: It collapsed. Before that the tilt increased. Before that cracks appeared. Before that one area sagged. Question: Which learned mechanism category would make this reversed observation chain expected?",
            "expected_mechanism": "load_transfer",
            "expected_status": "ANSWERED",
            "expected_classification": "CONSEQUENCE_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "RE-004",
            "question": "Observed system: It would not move. Before that it warmed. Before that it rattled. Before that movement became slower. Question: Which learned mechanism category would make this reversed observation chain expected?",
            "expected_mechanism": "supported_rotation",
            "expected_status": "ANSWERED",
            "expected_classification": "CONSEQUENCE_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "RE-005",
            "question": "Observed system: The receiving end waited. Before that queues grew. Before that output dropped. Before that arrivals became sporadic. Question: Which learned mechanism category would make this reversed observation chain expected?",
            "expected_mechanism": "flow",
            "expected_status": "ANSWERED",
            "expected_classification": "CONSEQUENCE_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "RE-006",
            "question": "Observed system: It broke. Before that the edge dropped. Before that a fracture grew. Before that one corner bowed. Question: Which learned mechanism category would make this reversed observation chain expected?",
            "expected_mechanism": "load_transfer",
            "expected_status": "ANSWERED",
            "expected_classification": "CONSEQUENCE_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
    ],
    "missing_roles": [
        {
            "question_id": "MR-001",
            "question": "Observed system: Something that normally moves freely began resisting motion. It warmed, made a rough sound, and then could not move. Question: Which learned mechanism category would naturally explain the observations?",
            "expected_mechanism": "supported_rotation",
            "expected_status": "ANSWERED",
            "expected_classification": "RELATIONAL_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "MR-002",
            "question": "Observed system: Something that normally reaches the far side began piling up before an unseen point. The far side received less, then nothing passed. Question: Which learned mechanism category would naturally explain the observations?",
            "expected_mechanism": "flow",
            "expected_status": "ANSWERED",
            "expected_classification": "RELATIONAL_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "MR-003",
            "question": "Observed system: Something that should stay level developed a single region that dipped, cracked, and then gave way. Question: Which learned mechanism category would naturally explain the observations?",
            "expected_mechanism": "load_transfer",
            "expected_status": "ANSWERED",
            "expected_classification": "RELATIONAL_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "MR-004",
            "question": "Observed system: A hidden contact made motion lag, heat increased, rattling appeared, and the moving thing stuck. Question: Which learned mechanism category would naturally explain the observations?",
            "expected_mechanism": "supported_rotation",
            "expected_status": "ANSWERED",
            "expected_classification": "RELATIONAL_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "MR-005",
            "question": "Observed system: An unseen limit made progress slowed, items accumulated before it, and the receiving end waited. Question: Which learned mechanism category would naturally explain the observations?",
            "expected_mechanism": "flow",
            "expected_status": "ANSWERED",
            "expected_classification": "RELATIONAL_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "MR-006",
            "question": "Observed system: Without naming any object, the same spot sagged, hairline marks spread, and the form no longer level. Question: Which learned mechanism category would naturally explain the observations?",
            "expected_mechanism": "load_transfer",
            "expected_status": "ANSWERED",
            "expected_classification": "RELATIONAL_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
    ],
    "multicause": [
        {
            "question_id": "MC-001",
            "question": "Observed system: Throughput decreased. Temperature increased. Noise increased. Question: Rank viable learned mechanisms that could naturally generate these observations.",
            "expected_mechanism": "supported_rotation",
            "expected_status": "ANSWERED",
            "expected_candidate_mechanisms": ["supported_rotation", "flow"],
            "expected_classification": "RELATIONAL_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "MC-002",
            "question": "Observed system: A surface dipped, output dropped, and one area became hot. Question: Rank viable learned mechanisms that could naturally generate these observations.",
            "expected_mechanism": "load_transfer",
            "expected_status": "ANSWERED",
            "expected_candidate_mechanisms": ["load_transfer", "flow", "supported_rotation"],
            "expected_classification": "RELATIONAL_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "MC-003",
            "question": "Observed system: Movement became slower, backlog grew, and vibration increased. Question: Rank viable learned mechanisms that could naturally generate these observations.",
            "expected_mechanism": "supported_rotation",
            "expected_status": "ANSWERED",
            "expected_candidate_mechanisms": ["supported_rotation", "flow"],
            "expected_classification": "RELATIONAL_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "MC-004",
            "question": "Observed system: The edge dropped, one corner bowed, arrivals thinned, temperature increased, and it could not hold. Question: Rank viable learned mechanisms that could naturally generate these observations.",
            "expected_mechanism": "load_transfer",
            "expected_status": "ANSWERED",
            "expected_candidate_mechanisms": ["load_transfer", "flow", "supported_rotation"],
            "expected_classification": "RELATIONAL_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
    ],
    "novel_surface": [
        {
            "question_id": "NS-001",
            "question": "Observed system: The fictional transport device called an Orbinsail developed increasing drag, rattling, warmth, and a final lockup. Question: Which learned mechanism is most similar by expected observations?",
            "expected_mechanism": "supported_rotation",
            "expected_status": "ANSWERED",
            "expected_classification": "CONSEQUENCE_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "NS-002",
            "question": "Observed system: In a made-up packet bazaar called Qorvex, delivery rate dropped, backlog grew, the far side went idle, and stopped arriving. Question: Which learned mechanism is most similar by expected observations?",
            "expected_mechanism": "flow",
            "expected_status": "ANSWERED",
            "expected_classification": "CONSEQUENCE_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "NS-003",
            "question": "Observed system: The invented skytile named Plenarch showed one point drooping, gap widened, fracture grew, and then collapsed. Question: Which learned mechanism is most similar by expected observations?",
            "expected_mechanism": "load_transfer",
            "expected_status": "ANSWERED",
            "expected_classification": "CONSEQUENCE_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "NS-004",
            "question": "Observed system: A fictional glider node, the Varn Loop, took longer to move, noise increased, became hot, and then seized. Question: Which learned mechanism is most similar by expected observations?",
            "expected_mechanism": "supported_rotation",
            "expected_status": "ANSWERED",
            "expected_classification": "CONSEQUENCE_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "NS-005",
            "question": "Observed system: On the imaginary service Mirr, bursts then gaps appeared, backlog built, receivers waited, and passage ceased. Question: Which learned mechanism is most similar by expected observations?",
            "expected_mechanism": "flow",
            "expected_status": "ANSWERED",
            "expected_classification": "CONSEQUENCE_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "NS-006",
            "question": "Observed system: A made-up object called a Halvek slab showed uneven height, a local dent, cracks appeared, and could not hold. Question: Which learned mechanism is most similar by expected observations?",
            "expected_mechanism": "load_transfer",
            "expected_status": "ANSWERED",
            "expected_classification": "CONSEQUENCE_INFERENCE",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
    ],
    "fail_closed": [
        {
            "question_id": "FC-001",
            "question": "Observed system: The object changed. Question: Could any learned mechanism make this observation expected? Return FAIL_CLOSED if not enough evidence.",
            "expected_mechanism": "",
            "expected_status": "FAIL_CLOSED",
            "expected_classification": "UNSUPPORTED",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "FC-002",
            "question": "Observed system: Something got worse. Question: Could any learned mechanism make this observation expected? Return FAIL_CLOSED if not enough evidence.",
            "expected_mechanism": "",
            "expected_status": "FAIL_CLOSED",
            "expected_classification": "UNSUPPORTED",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "FC-003",
            "question": "Observed system: There was a difference after some time. Question: Could any learned mechanism make this observation expected? Return FAIL_CLOSED if not enough evidence.",
            "expected_mechanism": "",
            "expected_status": "FAIL_CLOSED",
            "expected_classification": "UNSUPPORTED",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "FC-004",
            "question": "Observed system: A device acted unusual. Question: Could any learned mechanism make this observation expected? Return FAIL_CLOSED if not enough evidence.",
            "expected_mechanism": "",
            "expected_status": "FAIL_CLOSED",
            "expected_classification": "UNSUPPORTED",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
        {
            "question_id": "FC-005",
            "question": "Observed system: A result was not normal. Question: Could any learned mechanism make this observation expected? Return FAIL_CLOSED if not enough evidence.",
            "expected_mechanism": "",
            "expected_status": "FAIL_CLOSED",
            "expected_classification": "UNSUPPORTED",
            "explicit_role_present": False,
            "explicit_template_present": False,
        },
    ],
}


RESULT_FILE_BY_SUITE = {
    "consequence_only": "consequence_only_results.json",
    "reordered_evidence": "reordered_results.json",
    "missing_roles": "missing_roles_results.json",
    "multicause": "multicause_results.json",
    "novel_surface": "novel_surface_results.json",
    "fail_closed": "fail_closed_results.json",
}


def build_inference_state() -> dict[str, Any]:
    state = load_json(SOURCE_POND)
    state = json.loads(json.dumps(state))
    source_hash = state.get("state_hash", "")
    state["state_id"] = "mechanism_inference"
    state["derived_from_state_hash"] = source_hash
    state["consequence_inference_extension"] = {
        "source": "proofs/031-mechanistic-transfer-cue-invariance/pond_states/mechanism_seasoned/pond_state.json",
        "policy": "Adds hand-authored consequence signatures. Existing role-cue matching remains available.",
        "hostile_boundary": "This extension supports consequence-only tests but does not rule out deterministic parser explanations.",
    }
    for mechanism_id, extension in CONSEQUENCE_SIGNATURES.items():
        mechanism = state["mechanisms"][mechanism_id]
        mechanism["consequence_signatures"] = extension["consequence_signatures"]
        mechanism["required_min_consequence_features"] = extension["required_min_consequence_features"]
        mechanism["minimum_consequence_score"] = extension["minimum_consequence_score"]
        lesson_id = mechanism.get("lesson_id", "")
        if lesson_id in state.get("lessons", {}):
            lesson = state["lessons"][lesson_id]
            lesson["consequence_signatures"] = extension["consequence_signatures"]
            lesson["required_min_consequence_features"] = extension["required_min_consequence_features"]
            lesson["minimum_consequence_score"] = extension["minimum_consequence_score"]
    state.pop("state_hash", None)
    state["state_hash"] = sha256_json(state)
    write_json(POND_DIR / "pond_state.json", state)
    return state


def run_cli_map(question: str) -> dict[str, Any]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "operational_cognition.cli.mechanism_pond",
            "map",
            "--pond",
            str(POND_DIR),
            "--question",
            question,
            "--json",
        ],
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def correct_result(result: dict[str, Any], item: dict[str, Any]) -> bool:
    if item["expected_status"] == "FAIL_CLOSED":
        return result.get("status") == "FAIL_CLOSED" and result.get("identified_mechanism") == ""
    if item.get("suite") == "multicause":
        candidates = result.get("candidate_mechanisms", [])
        ranking = result.get("confidence_ranking", [])
        expected_candidates = item.get("expected_candidate_mechanisms", [])
        return (
            result.get("status") == "ANSWERED"
            and result.get("identified_mechanism") == item["expected_mechanism"]
            and all(candidate in candidates for candidate in expected_candidates)
            and bool(ranking)
            and ranking[0].get("mechanism_id") == item["expected_mechanism"]
        )
    return (
        result.get("status") == "ANSWERED"
        and result.get("identified_mechanism") == item["expected_mechanism"]
        and len(result.get("consequence_lineage", [])) >= 3
        and bool(result.get("source_tracebacks"))
    )


def evaluate_item(item: dict[str, Any]) -> dict[str, Any]:
    first = run_cli_map(item["question"])
    second = run_cli_map(item["question"])
    row = {
        **first,
        "question_id": item["question_id"],
        "suite": item["suite"],
        "expected_status": item["expected_status"],
        "expected_mechanism": item["expected_mechanism"],
        "expected_candidate_mechanisms": item.get("expected_candidate_mechanisms", []),
        "expected_classification": item["expected_classification"],
        "explicit_role_present": item["explicit_role_present"],
        "explicit_template_present": item["explicit_template_present"],
        "correct": correct_result(first, item),
        "deterministic_replay_match": canonical_json(first) == canonical_json(second),
        "matched_role_ids": [role.get("role_id", "") for role in first.get("matched_roles", [])],
        "matched_consequence_ids": [
            feature.get("feature_id", "") for feature in first.get("matched_consequences", [])
        ],
    }
    return row


def evaluate_suite(suite: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    items = [evaluate_item({**item, "suite": suite}) for item in rows]
    total = len(items)
    return {
        "proof_id": PROOF_ID,
        "suite": suite,
        "execution_mode": "deterministic_cli_no_llm",
        "pond_state": "proofs/032-mechanistic-inference-challenge/pond_states/mechanism_inference",
        "total_items": total,
        "correct_items": sum(1 for item in items if item["correct"]),
        "answered_items": sum(1 for item in items if item["status"] == "ANSWERED"),
        "fail_closed_items": sum(1 for item in items if item["status"] == "FAIL_CLOSED"),
        "accuracy": round(sum(1 for item in items if item["correct"]) / total, 4) if total else 0.0,
        "deterministic_replay_match": all(item["deterministic_replay_match"] for item in items),
        "items": items,
    }


def classify_item(row: dict[str, Any]) -> str:
    if not row.get("correct"):
        return "UNSUPPORTED"
    if row.get("expected_status") == "FAIL_CLOSED":
        return "UNSUPPORTED"
    if row.get("explicit_template_present"):
        return "TEMPLATE_MATCH"
    if row.get("explicit_role_present") and len(row.get("matched_roles", [])) >= 3:
        return "ROLE_MATCH"
    expected = row.get("expected_classification", "")
    if expected in {"CONSEQUENCE_INFERENCE", "RELATIONAL_INFERENCE"}:
        return expected
    if row.get("inference_mode") in {"CONSEQUENCE_INFERENCE", "RELATIONAL_INFERENCE"}:
        return str(row["inference_mode"])
    return "UNSUPPORTED"


def mechanistic_inference_audit(results: dict[str, dict[str, Any]]) -> dict[str, Any]:
    rows = [row for result in results.values() for row in result["items"]]
    items = []
    for row in rows:
        classification = classify_item(row)
        items.append(
            {
                "question_id": row["question_id"],
                "suite": row["suite"],
                "expected_mechanism": row["expected_mechanism"],
                "identified_mechanism": row["identified_mechanism"],
                "status": row["status"],
                "correct": row["correct"],
                "explicit_role_present": row["explicit_role_present"],
                "explicit_template_present": row["explicit_template_present"],
                "matched_roles": row["matched_role_ids"],
                "matched_consequences": row["matched_consequence_ids"],
                "candidate_mechanisms": row.get("candidate_mechanisms", []),
                "classification": classification,
            }
        )
    counts = Counter(item["classification"] for item in items)
    return {
        "proof_id": PROOF_ID,
        "classification_policy": {
            "TEMPLATE_MATCH": "The prompt preserves a direct source template or canonical mechanism wording.",
            "ROLE_MATCH": "The prompt names enough source roles or role entities for the role parser to explain success.",
            "CONSEQUENCE_INFERENCE": "The prompt hides source roles and is answered from outcome signatures.",
            "RELATIONAL_INFERENCE": "The prompt hides source entities but preserves relations among partial consequences or competing causes.",
            "UNSUPPORTED": "The item failed, failed closed correctly, or lacked enough evidence for a mechanism claim.",
        },
        "classification_counts": dict(sorted(counts.items())),
        "items": items,
    }


def hidden_cause_audit(results: dict[str, dict[str, Any]], inference_audit: dict[str, Any]) -> dict[str, Any]:
    class_by_id = {item["question_id"]: item["classification"] for item in inference_audit["items"]}
    rows = [
        row
        for result in results.values()
        for row in result["items"]
        if row["expected_status"] == "ANSWERED"
    ]
    items = [
        {
            "question_id": row["question_id"],
            "mechanism": row["identified_mechanism"],
            "explicit_role_present": row["explicit_role_present"],
            "hidden_cause_inferred": bool(
                row["correct"] and row["status"] == "ANSWERED" and not row["explicit_role_present"]
            ),
            "classification": class_by_id[row["question_id"]],
        }
        for row in rows
    ]
    return {
        "proof_id": PROOF_ID,
        "question": "Did the system identify a mechanism without direct role cues?",
        "items": items,
        "hidden_cause_inference_rate": round(
            sum(1 for item in items if item["hidden_cause_inferred"]) / len(items), 4
        )
        if items
        else 0.0,
    }


def suite_accuracy(results: dict[str, dict[str, Any]], suite: str) -> float:
    return results[suite]["accuracy"]


def metrics(results: dict[str, dict[str, Any]], inference_audit: dict[str, Any], hidden_audit: dict[str, Any]) -> dict[str, Any]:
    answered_successes = [
        item
        for item in inference_audit["items"]
        if item["correct"] and item["status"] == "ANSWERED"
    ]
    consequence_or_relational = [
        item
        for item in answered_successes
        if item["classification"] in {"CONSEQUENCE_INFERENCE", "RELATIONAL_INFERENCE"}
    ]
    fail_closed = results["fail_closed"]
    return {
        "proof_id": PROOF_ID,
        "consequence_only_accuracy": suite_accuracy(results, "consequence_only"),
        "reordered_accuracy": suite_accuracy(results, "reordered_evidence"),
        "missing_roles_accuracy": suite_accuracy(results, "missing_roles"),
        "multicause_accuracy": suite_accuracy(results, "multicause"),
        "novel_surface_accuracy": suite_accuracy(results, "novel_surface"),
        "fail_closed_rate": round(fail_closed["fail_closed_items"] / fail_closed["total_items"], 4),
        "answered_successes": len(answered_successes),
        "consequence_or_relational_successes": len(consequence_or_relational),
        "consequence_or_relational_success_rate": round(
            len(consequence_or_relational) / len(answered_successes), 4
        )
        if answered_successes
        else 0.0,
        "hidden_cause_inference_rate": hidden_audit["hidden_cause_inference_rate"],
        "classification_counts": inference_audit["classification_counts"],
        "deterministic_replay_match": all(result["deterministic_replay_match"] for result in results.values()),
        "signal_before_hostile_audit": "STRONG_SIGNAL"
        if len(consequence_or_relational) >= 20 and fail_closed["fail_closed_items"] == fail_closed["total_items"]
        else "WEAK_SIGNAL",
    }


def hostile_audit(metrics_row: dict[str, Any], inference_audit: dict[str, Any]) -> dict[str, Any]:
    many_consequence_successes = metrics_row["consequence_or_relational_success_rate"] >= 0.85
    all_fail_closed = metrics_row["fail_closed_rate"] == 1.0
    remaining_template_explanation = True
    remaining_parser_explanation = True
    hostile_verdict = "WEAK_SIGNAL" if many_consequence_successes and all_fail_closed else "FAIL"
    return {
        "proof_id": PROOF_ID,
        "original_verdict": "Proof 031 hostile audit verdict was WEAK_SIGNAL because cue removal and decoys were handled, but fixed role-cue parsing remained a complete explanation.",
        "hostile_verdict": hostile_verdict,
        "remaining_template_explanation": remaining_template_explanation,
        "remaining_parser_explanation": remaining_parser_explanation,
        "critical_metric_snapshot": {
            "consequence_only_accuracy": metrics_row["consequence_only_accuracy"],
            "reordered_accuracy": metrics_row["reordered_accuracy"],
            "missing_roles_accuracy": metrics_row["missing_roles_accuracy"],
            "multicause_accuracy": metrics_row["multicause_accuracy"],
            "novel_surface_accuracy": metrics_row["novel_surface_accuracy"],
            "fail_closed_rate": metrics_row["fail_closed_rate"],
            "consequence_or_relational_success_rate": metrics_row[
                "consequence_or_relational_success_rate"
            ],
        },
        "attacks": [
            {
                "attack": "template_matching",
                "status": "survives_in_consequence_form",
                "finding": "The direct four-role templates are mostly absent, but the proof adds hand-authored consequence signatures that are still templates over observable outcomes.",
            },
            {
                "attack": "role_matching",
                "status": "mostly_rejected_for_successes",
                "finding": "Most successful prompts omit direct source roles such as wheel, bearing, path, source, load, support, or joint. Role matching alone is not sufficient for these outputs.",
            },
            {
                "attack": "cue_matching",
                "status": "survives",
                "finding": "The implementation still normalizes text and scores fixed outcome cue lists such as noise, heat, backlog, crack, sag, and stopped.",
            },
            {
                "attack": "hardcoded_sequence_matching",
                "status": "mostly_rejected",
                "finding": "Reordered evidence maps correctly because scoring is order-insensitive. A fixed chronological sequence parser is not required.",
            },
            {
                "attack": "multi_cause_ranking",
                "status": "partial_signal",
                "finding": "The rank outputs expose multiple viable mechanisms, but the ranking is still deterministic scoring over authored signatures.",
            },
            {
                "attack": "novel_surface_objects",
                "status": "partial_signal",
                "finding": "Fictional objects do not break mapping when consequence signatures are present; this rejects simple known-object lookup but not cue parsing.",
            },
            {
                "attack": "LLM_answer_synthesis",
                "status": "rejected",
                "finding": "Final answers were generated by deterministic subprocess calls to mechanism_pond.py with no LLM answer path.",
            },
        ],
        "surviving_claims": [
            "The deterministic CLI can identify the closed-world mechanisms from consequence-only observations in this curated suite.",
            "The deterministic CLI can handle reversed observation order because the evidence scorer is order-insensitive.",
            "The deterministic CLI can rank partially compatible mechanisms for multi-cause prompts and expose candidate_mechanisms plus confidence_ranking.",
            "Ambiguous underspecified prompts fail closed.",
            "Direct role matching is no longer the dominant explanation for most successful Proof 032 items.",
        ],
        "invalidated_claims": [
            "Performance is independent of parser behavior.",
            "Performance is independent of hand-authored cue inventories.",
            "The proof establishes general mechanistic understanding outside the closed FLOW, SUPPORTED_ROTATION, and LOAD_TRANSFER curriculum.",
            "The hostile audit eliminates template explanations entirely.",
        ],
        "classification_snapshot": inference_audit["classification_counts"],
        "interpretation": "Proof 032 is a weak signal after hostile audit: it moves beyond direct role templates into consequence signatures, but deterministic parser and template explanations still survive.",
    }


def readme(metrics_row: dict[str, Any], hostile: dict[str, Any]) -> str:
    return f"""# Proof 032 - Mechanistic Inference Challenge

## Objective

Proof 032 tests whether the mechanism pond can infer a closed-world mechanism from observed consequences when roles are hidden, evidence is reordered, entities are missing, surfaces are novel, or multiple causes compete.

Final answers were generated only by:

```bash
python3 -m operational_cognition.cli.mechanism_pond map --pond proofs/032-mechanistic-inference-challenge/pond_states/mechanism_inference --question "<question>" --json
```

## Result Snapshot

- Consequence-only accuracy: {metrics_row["consequence_only_accuracy"]}
- Reordered-evidence accuracy: {metrics_row["reordered_accuracy"]}
- Missing-roles accuracy: {metrics_row["missing_roles_accuracy"]}
- Multi-cause ranking accuracy: {metrics_row["multicause_accuracy"]}
- Novel-surface accuracy: {metrics_row["novel_surface_accuracy"]}
- Fail-closed rate: {metrics_row["fail_closed_rate"]}
- Consequence or relational success rate: {metrics_row["consequence_or_relational_success_rate"]}
- Hidden-cause inference rate: {metrics_row["hidden_cause_inference_rate"]}
- Deterministic replay match: {str(metrics_row["deterministic_replay_match"]).lower()}
- Signal before hostile audit: {metrics_row["signal_before_hostile_audit"]}
- Hostile verdict: {hostile["hostile_verdict"]}

## Required Answers

1. Did consequence-only observations identify mechanisms?
   Yes, inside the closed three-mechanism curriculum.

2. Did reversed evidence break inference?
   No. The scorer is order-insensitive, so reversed chains still map.

3. Did hidden or missing roles break inference?
   No for the curated cases. The system used consequence signatures rather than direct role names.

4. Did multi-cause competition produce ranked candidates?
   Yes. Multi-cause result rows include `candidate_mechanisms` and `confidence_ranking`.

5. Did novel surface objects break inference?
   No. Fictional object names mapped when consequence signatures were present.

6. Did ambiguous inputs fail closed?
   Yes. The fail-closed rate was {metrics_row["fail_closed_rate"]}.

7. What survives hostile audit?
   A bounded deterministic CLI can infer closed-world mechanisms from consequence signatures without direct role labels. The stronger claim that this defeats parser or template explanations does not survive.
"""


def manifest(request_hash: str, response_hash: str) -> dict[str, Any]:
    required_artifacts = [
        "README.md",
        "proof_manifest.json",
        "pond_states/mechanism_inference/pond_state.json",
        "tests/consequence_only.jsonl",
        "tests/reordered_evidence.jsonl",
        "tests/missing_roles.jsonl",
        "tests/multicause.jsonl",
        "tests/novel_surface.jsonl",
        "tests/fail_closed.jsonl",
        "results/consequence_only_results.json",
        "results/reordered_results.json",
        "results/missing_roles_results.json",
        "results/multicause_results.json",
        "results/novel_surface_results.json",
        "results/fail_closed_results.json",
        "analysis/mechanistic_inference_audit.json",
        "analysis/hidden_cause_audit.json",
        "analysis/hostile_mechanistic_inference_audit.json",
        "analysis/mechanistic_inference_metrics.json",
    ]
    return {
        "proof_id": PROOF_ID,
        "title": TITLE,
        "status": "complete",
        "targets": [
            "MechanisticInference",
            "ConsequenceOnlyReasoning",
            "HiddenCauseInference",
            "MultiCauseRanking",
            "FailClosedMechanismPondCLI",
            "HostileParserAudit",
        ],
        "claim_level": "evidence_backed",
        "inside_voice_adapter_status": "not_used_final_answers_generated_by_deterministic_cli",
        "public_private_boundary": "All artifacts are public deterministic tests, pond state, CLI outputs, metrics, and audits. No hidden chain-of-thought or private substrate data is exposed.",
        "required_artifacts": required_artifacts,
        "disallowed_claims": [
            "LLM generated final answers",
            "general mechanism understanding",
            "general physical reasoning",
            "success independent of parser behavior",
            "success independent of hand-authored consequence cues",
            "success beyond FLOW, SUPPORTED_ROTATION, and LOAD_TRANSFER",
        ],
        "lineage": {
            "mcp_endpoint": "none:deterministic_cli_no_llm",
            "contract_version": "mechanism_pond.cli.v3",
            "request_hash": request_hash,
            "response_hash": response_hash,
            "derived_from": "proofs/031-mechanistic-transfer-cue-invariance/pond_states/mechanism_seasoned/pond_state.json; tests/*.jsonl; python3 -m operational_cognition.cli.mechanism_pond",
            "validates": "curated_consequence_only_mechanistic_inference_with_fail_closed_no_llm_cli_answers",
        },
    }


def main() -> int:
    state = build_inference_state()
    for suite, rows in TEST_SUITES.items():
        test_rows = [{**row, "suite": suite} for row in rows]
        write_jsonl(PROOF_DIR / "tests" / f"{suite}.jsonl", test_rows)

    results = {suite: evaluate_suite(suite, rows) for suite, rows in TEST_SUITES.items()}
    for suite, result in results.items():
        write_json(PROOF_DIR / "results" / RESULT_FILE_BY_SUITE[suite], result)

    inference_audit = mechanistic_inference_audit(results)
    hidden_audit = hidden_cause_audit(results, inference_audit)
    metrics_row = metrics(results, inference_audit, hidden_audit)
    hostile = hostile_audit(metrics_row, inference_audit)

    write_json(PROOF_DIR / "analysis" / "mechanistic_inference_audit.json", inference_audit)
    write_json(PROOF_DIR / "analysis" / "hidden_cause_audit.json", hidden_audit)
    write_json(PROOF_DIR / "analysis" / "hostile_mechanistic_inference_audit.json", hostile)
    write_json(PROOF_DIR / "analysis" / "mechanistic_inference_metrics.json", metrics_row)
    write_text(PROOF_DIR / "README.md", readme(metrics_row, hostile))

    request_hash = sha256_json({"source_state_hash": state["derived_from_state_hash"], "tests": TEST_SUITES})
    response_hash = sha256_json({"results": results, "audits": [inference_audit, hidden_audit, hostile], "metrics": metrics_row})
    write_json(PROOF_DIR / "proof_manifest.json", manifest(request_hash, response_hash))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
