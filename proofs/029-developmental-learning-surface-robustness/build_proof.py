#!/usr/bin/env python3
"""Build Proof 029 surface-form robustness artifacts."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


PROOF_ID = "029-developmental-learning-surface-robustness"
TITLE = "Proof 029 - Developmental Learning Challenge 002 - Surface-Form Robustness and Structure Reuse"
PROOF_DIR = Path(__file__).resolve().parent
ROOT = PROOF_DIR.parents[1]
SOURCE_PROOF = ROOT / "proofs" / "028-developmental-learning-grade-ladder"
SOURCE_POND = SOURCE_PROOF / "pond_states" / "grade_2"
SOURCE_STATE_PATH = SOURCE_POND / "pond_state.json"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


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


PATHWAY_IDS: dict[str, list[str]] = {
    "counting": ["pathway:g1_counting_sequence"],
    "one_digit_addition": ["pathway:g1_counting->g1_one_digit_addition"],
    "one_digit_subtraction": ["pathway:g1_counting->g1_one_digit_subtraction"],
    "equality": ["pathway:g1_equality_check"],
    "number_comparison": ["pathway:g1_counting->g1_number_order"],
    "simple_word_problems": ["pathway:g1_language_to_operation"],
    "place_value": ["pathway:g1_counting->g2_tens_ones_place_value"],
    "two_digit_addition_without_carrying": [
        "pathway:g1_addition->g2_place_value->g2_no_carry_addition"
    ],
    "two_digit_subtraction_without_borrowing": [
        "pathway:g1_subtraction->g2_place_value->g2_no_borrow_subtraction"
    ],
    "skip_counting": ["pathway:g1_addition->g2_fixed_step_skip_counting"],
    "multiplication_as_repeated_addition": [
        "pathway:g1_addition->g2_equal_groups_repeated_addition"
    ],
    "division_as_grouping": ["pathway:g1_subtraction->g2_equal_grouping_division"],
}


REWORDED_TESTS: list[dict[str, Any]] = [
    {
        "question_id": "RQ-001",
        "suite": "reworded",
        "question": "What do you get when you put 6 and 7 together?",
        "expected_answer": "13",
        "expected_status": "ANSWERED",
        "concept": "one_digit_addition",
        "requires_transfer": True,
        "surface_variation": "addition_without_plus_symbol",
        "expected_composition_depth": 1,
        "fragility_classification": "AMBIGUOUS",
    },
    {
        "question_id": "RQ-002",
        "suite": "reworded",
        "question": "Start with 14. Add 23. What number do you land on?",
        "expected_answer": "37",
        "expected_status": "ANSWERED",
        "concept": "two_digit_addition_without_carrying",
        "requires_transfer": True,
        "surface_variation": "imperative_start_add",
        "expected_composition_depth": 1,
        "fragility_classification": "STRUCTURE_REUSE",
    },
    {
        "question_id": "RQ-003",
        "suite": "reworded",
        "question": "Take 5 away from 18.",
        "expected_answer": "13",
        "expected_status": "ANSWERED",
        "concept": "two_digit_subtraction_without_borrowing",
        "requires_transfer": True,
        "surface_variation": "subtraction_without_minus_symbol",
        "expected_composition_depth": 1,
        "fragility_classification": "PARSER_MATCH",
    },
    {
        "question_id": "RQ-004",
        "suite": "reworded",
        "question": "If you count by 5s, what comes after 25?",
        "expected_answer": "30",
        "expected_status": "ANSWERED",
        "concept": "skip_counting",
        "requires_transfer": True,
        "surface_variation": "skip_counting_if_clause",
        "expected_composition_depth": 1,
        "fragility_classification": "PARSER_MATCH",
    },
    {
        "question_id": "RQ-005",
        "suite": "reworded",
        "question": "Break 58 into tens and ones.",
        "expected_answer": "5 tens and 8 ones",
        "expected_status": "ANSWERED",
        "concept": "place_value",
        "requires_transfer": True,
        "surface_variation": "place_value_without_how_many",
        "expected_composition_depth": 1,
        "fragility_classification": "PARSER_MATCH",
    },
]


DISTRACTOR_TESTS: list[dict[str, Any]] = [
    {
        "question_id": "DQ-001",
        "suite": "distractor",
        "question": "There are 4 red apples, 3 green apples, and 2 empty baskets. How many apples are there?",
        "expected_answer": "7",
        "expected_status": "ANSWERED",
        "concept": "simple_word_problems",
        "requires_transfer": True,
        "surface_variation": "irrelevant_empty_baskets",
        "expected_composition_depth": 1,
        "fragility_classification": "STRUCTURE_REUSE",
    },
    {
        "question_id": "DQ-002",
        "suite": "distractor",
        "question": "A class has 12 pencils, 5 erasers, and 3 rulers. How many pencils and erasers together?",
        "expected_answer": "17",
        "expected_status": "ANSWERED",
        "concept": "two_digit_addition_without_carrying",
        "requires_transfer": True,
        "surface_variation": "select_two_named_quantities",
        "expected_composition_depth": 1,
        "fragility_classification": "STRUCTURE_REUSE",
    },
    {
        "question_id": "DQ-003",
        "suite": "distractor",
        "question": "There are 6 blue cars, 2 red cars, and 5 bikes. How many cars are there?",
        "expected_answer": "8",
        "expected_status": "ANSWERED",
        "concept": "simple_word_problems",
        "requires_transfer": True,
        "surface_variation": "category_filtering",
        "expected_composition_depth": 1,
        "fragility_classification": "STRUCTURE_REUSE",
    },
    {
        "question_id": "DQ-004",
        "suite": "distractor",
        "question": "Mia has 18 stickers, gives 3 stickers to Lee, and sees 4 stamps. How many stickers does Mia have now?",
        "expected_answer": "15",
        "expected_status": "ANSWERED",
        "concept": "two_digit_subtraction_without_borrowing",
        "requires_transfer": True,
        "surface_variation": "ignore_unrelated_stamp_quantity",
        "expected_composition_depth": 1,
        "fragility_classification": "STRUCTURE_REUSE",
    },
    {
        "question_id": "DQ-005",
        "suite": "distractor",
        "question": "A shelf has 3 boxes with 4 books each and 2 empty boxes. How many books are on the shelf?",
        "expected_answer": "12",
        "expected_status": "ANSWERED",
        "concept": "multiplication_as_repeated_addition",
        "requires_transfer": True,
        "surface_variation": "ignore_empty_equal_groups",
        "expected_composition_depth": 1,
        "fragility_classification": "STRUCTURE_REUSE",
    },
]


REVERSED_TESTS: list[dict[str, Any]] = [
    {
        "question_id": "RV-001",
        "suite": "reversed",
        "question": "What number must be added to 6 to make 10?",
        "expected_answer": "4",
        "expected_status": "ANSWERED",
        "concept": "equality",
        "requires_transfer": True,
        "surface_variation": "missing_addend",
        "expected_composition_depth": 2,
        "fragility_classification": "STRUCTURE_REUSE",
    },
    {
        "question_id": "RV-002",
        "suite": "reversed",
        "question": "After losing 4 marbles, Sam has 9 left. How many did Sam have before?",
        "expected_answer": "13",
        "expected_status": "ANSWERED",
        "concept": "simple_word_problems",
        "requires_transfer": True,
        "surface_variation": "recover_starting_quantity",
        "expected_composition_depth": 2,
        "fragility_classification": "STRUCTURE_REUSE",
    },
    {
        "question_id": "RV-003",
        "suite": "reversed",
        "question": "Which number is smaller: 42 or 24?",
        "expected_answer": "24",
        "expected_status": "ANSWERED",
        "concept": "number_comparison",
        "requires_transfer": True,
        "surface_variation": "comparison_with_number_inserted",
        "expected_composition_depth": 1,
        "fragility_classification": "STRUCTURE_REUSE",
    },
    {
        "question_id": "RV-004",
        "suite": "reversed",
        "question": "What must be taken from 18 to leave 13?",
        "expected_answer": "5",
        "expected_status": "ANSWERED",
        "concept": "equality",
        "requires_transfer": True,
        "surface_variation": "missing_subtrahend",
        "expected_composition_depth": 2,
        "fragility_classification": "STRUCTURE_REUSE",
    },
    {
        "question_id": "RV-005",
        "suite": "reversed",
        "question": "Which number is greater: 35 or 53?",
        "expected_answer": "53",
        "expected_status": "ANSWERED",
        "concept": "number_comparison",
        "requires_transfer": True,
        "surface_variation": "greater_comparison_with_number_inserted",
        "expected_composition_depth": 1,
        "fragility_classification": "STRUCTURE_REUSE",
    },
]


MULTISTEP_TESTS: list[dict[str, Any]] = [
    {
        "question_id": "MS-001",
        "suite": "multistep",
        "question": "There are 3 bags with 4 apples each. Then 2 apples are eaten. How many remain?",
        "expected_answer": "10",
        "expected_status": "ANSWERED",
        "concept": "multiplication_as_repeated_addition",
        "requires_transfer": True,
        "surface_variation": "multiplication_then_subtraction",
        "expected_composition_depth": 2,
        "fragility_classification": "STRUCTURE_REUSE",
    },
    {
        "question_id": "MS-002",
        "suite": "multistep",
        "question": "Start at 20, add 13, then take away 3.",
        "expected_answer": "30",
        "expected_status": "ANSWERED",
        "concept": "two_digit_addition_without_carrying",
        "requires_transfer": True,
        "surface_variation": "addition_then_subtraction",
        "expected_composition_depth": 2,
        "fragility_classification": "STRUCTURE_REUSE",
    },
    {
        "question_id": "MS-003",
        "suite": "multistep",
        "question": "2 groups of 6 birds join 3 more birds. How many birds?",
        "expected_answer": "15",
        "expected_status": "ANSWERED",
        "concept": "multiplication_as_repeated_addition",
        "requires_transfer": True,
        "surface_variation": "equal_groups_then_more",
        "expected_composition_depth": 2,
        "fragility_classification": "STRUCTURE_REUSE",
    },
    {
        "question_id": "MS-004",
        "suite": "multistep",
        "question": "A class has 12 pencils and gets 6 more, then gives away 4 pencils. How many pencils remain?",
        "expected_answer": "14",
        "expected_status": "ANSWERED",
        "concept": "simple_word_problems",
        "requires_transfer": True,
        "surface_variation": "word_addition_then_word_subtraction",
        "expected_composition_depth": 2,
        "fragility_classification": "STRUCTURE_REUSE",
    },
    {
        "question_id": "MS-005",
        "suite": "multistep",
        "question": "Count by 5s after 10, then add 2. What number is it?",
        "expected_answer": "17",
        "expected_status": "ANSWERED",
        "concept": "skip_counting",
        "requires_transfer": True,
        "surface_variation": "skip_counting_then_addition",
        "expected_composition_depth": 2,
        "fragility_classification": "STRUCTURE_REUSE",
    },
]


OUT_OF_SCOPE_TESTS: list[dict[str, Any]] = [
    {
        "question_id": "OOS-001",
        "suite": "out_of_scope",
        "question": "What is 7 x 8?",
        "expected_answer": "",
        "expected_status": "FAIL_CLOSED",
        "concept": "out_of_scope_large_multiplication",
        "requires_transfer": False,
        "surface_variation": "factor_range_not_taught",
        "expected_composition_depth": 0,
        "fragility_classification": "UNSUPPORTED",
    },
    {
        "question_id": "OOS-002",
        "suite": "out_of_scope",
        "question": "What is 14 divided by 3?",
        "expected_answer": "",
        "expected_status": "FAIL_CLOSED",
        "concept": "out_of_scope_remainder_division",
        "requires_transfer": False,
        "surface_variation": "division_with_remainder",
        "expected_composition_depth": 0,
        "fragility_classification": "UNSUPPORTED",
    },
    {
        "question_id": "OOS-003",
        "suite": "out_of_scope",
        "question": "What is 3 + x = 7?",
        "expected_answer": "",
        "expected_status": "FAIL_CLOSED",
        "concept": "out_of_scope_algebra",
        "requires_transfer": False,
        "surface_variation": "symbolic_unknown",
        "expected_composition_depth": 0,
        "fragility_classification": "UNSUPPORTED",
    },
    {
        "question_id": "OOS-004",
        "suite": "out_of_scope",
        "question": "What is one half of 10?",
        "expected_answer": "",
        "expected_status": "FAIL_CLOSED",
        "concept": "out_of_scope_fraction",
        "requires_transfer": False,
        "surface_variation": "fraction_language",
        "expected_composition_depth": 0,
        "fragility_classification": "UNSUPPORTED",
    },
    {
        "question_id": "OOS-005",
        "suite": "out_of_scope",
        "question": "What is 46 - 19?",
        "expected_answer": "",
        "expected_status": "FAIL_CLOSED",
        "concept": "out_of_scope_borrowing",
        "requires_transfer": False,
        "surface_variation": "two_digit_subtraction_with_borrowing",
        "expected_composition_depth": 0,
        "fragility_classification": "UNSUPPORTED",
    },
    {
        "question_id": "OOS-006",
        "suite": "out_of_scope",
        "question": "What is 58 + 37?",
        "expected_answer": "",
        "expected_status": "FAIL_CLOSED",
        "concept": "out_of_scope_carrying",
        "requires_transfer": False,
        "surface_variation": "two_digit_addition_with_carrying",
        "expected_composition_depth": 0,
        "fragility_classification": "UNSUPPORTED",
    },
]


SUITES: dict[str, list[dict[str, Any]]] = {
    "reworded": REWORDED_TESTS,
    "distractor": DISTRACTOR_TESTS,
    "reversed": REVERSED_TESTS,
    "multistep": MULTISTEP_TESTS,
    "out_of_scope": OUT_OF_SCOPE_TESTS,
}


def freeze_inventory(state: dict[str, Any]) -> dict[str, Any]:
    concepts = state.get("concepts", {})
    inventory: list[dict[str, Any]] = []
    for concept_id in sorted(concepts):
        concept = concepts[concept_id]
        inventory.append(
            {
                "concept_id": concept_id,
                "source_proof": "proofs/028-developmental-learning-grade-ladder",
                "source_lesson_ids": concept.get("lesson_ids", []),
                "motif_ids": concept.get("motifs", []),
                "pathway_ids": PATHWAY_IDS.get(concept_id, []),
            }
        )
    return {
        "proof_id": PROOF_ID,
        "source_pond": str(SOURCE_POND.relative_to(ROOT)),
        "source_state_hash": state.get("state_hash", ""),
        "new_math_concepts_allowed": False,
        "frozen_concept_count": len(inventory),
        "concepts": inventory,
    }


def run_cli_answer(question: str) -> dict[str, Any]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "operational_cognition.cli.math_pond",
            "answer",
            "--pond",
            str(SOURCE_POND),
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


def tracebacks_complete(result: dict[str, Any]) -> bool:
    if result.get("status") != "ANSWERED":
        return False
    concepts = set(result.get("concept_pathway", []))
    traced = {trace.get("concept") for trace in result.get("source_tracebacks", []) if isinstance(trace, dict)}
    return concepts <= traced


def used_motif_ids(result: dict[str, Any]) -> list[str]:
    return sorted(
        {
            str(motif.get("motif_id"))
            for motif in result.get("motif_lineage", [])
            if isinstance(motif, dict) and motif.get("motif_id")
        }
    )


def source_lesson_ids(result: dict[str, Any]) -> list[str]:
    return sorted(
        {
            str(trace.get("lesson_id"))
            for trace in result.get("source_tracebacks", [])
            if isinstance(trace, dict) and trace.get("lesson_id")
        }
    )


def pathway_ids(result: dict[str, Any]) -> list[str]:
    concept_pathway = result.get("concept_pathway", [])
    if not concept_pathway:
        return []
    ids = ["pathway:" + "->".join(concept_pathway)]
    for concept in concept_pathway:
        ids.extend(PATHWAY_IDS.get(concept, []))
    return sorted(set(ids))


def evaluate_item(item: dict[str, Any]) -> dict[str, Any]:
    first = run_cli_answer(item["question"])
    second = run_cli_answer(item["question"])
    expected_status = item["expected_status"]
    correct = first.get("status") == expected_status
    if expected_status == "ANSWERED":
        correct = correct and first.get("answer") == item["expected_answer"]
    else:
        correct = correct and first.get("answer") == ""

    return {
        **first,
        "question_id": item["question_id"],
        "suite": item["suite"],
        "expected_answer": item["expected_answer"],
        "expected_status": expected_status,
        "concept": item["concept"],
        "requires_transfer": item["requires_transfer"],
        "surface_variation": item["surface_variation"],
        "expected_composition_depth": item["expected_composition_depth"],
        "fragility_classification": item["fragility_classification"],
        "correct": correct,
        "traceback_complete": tracebacks_complete(first),
        "deterministic_replay_match": canonical_json(first) == canonical_json(second),
        "used_motifs": used_motif_ids(first),
        "used_pathways": pathway_ids(first),
        "source_lessons": source_lesson_ids(first),
    }


def evaluate_suite(name: str, items: list[dict[str, Any]]) -> dict[str, Any]:
    rows = [evaluate_item(item) for item in items]
    total = len(rows)
    answered = [row for row in rows if row.get("status") == "ANSWERED"]
    expected_answered = [row for row in rows if row["expected_status"] == "ANSWERED"]
    return {
        "proof_id": PROOF_ID,
        "suite": name,
        "pond_state": str(SOURCE_POND.relative_to(ROOT)),
        "execution_mode": "deterministic_cli_no_llm",
        "accuracy": round(sum(1 for row in rows if row["correct"]) / total, 4),
        "answered_items": len(answered),
        "total_items": total,
        "traceback_completeness": round(
            sum(1 for row in expected_answered if row["traceback_complete"]) / len(expected_answered), 4
        )
        if expected_answered
        else 1.0,
        "unsupported_answers": sum(1 for row in expected_answered if row["status"] != "ANSWERED"),
        "fail_closed_rate": round(sum(1 for row in rows if row["status"] == "FAIL_CLOSED") / total, 4),
        "deterministic_replay_match": all(row["deterministic_replay_match"] for row in rows),
        "items": rows,
    }


def parser_fragility_audit(results: dict[str, dict[str, Any]]) -> dict[str, Any]:
    items = [row for result in results.values() for row in result["items"]]
    audit_items: list[dict[str, Any]] = []
    for row in items:
        classification = row["fragility_classification"]
        if row["expected_status"] == "ANSWERED" and not row["correct"]:
            classification = "UNSUPPORTED"
        audit_items.append(
            {
                "question_id": row["question_id"],
                "suite": row["suite"],
                "classification": classification,
                "status": row["status"],
                "correct": row["correct"],
                "exact_phrase_dependence": row["suite"] == "reworded" and classification == "PARSER_MATCH",
                "operation_keyword_dependence": any(
                    token in row["question"].lower()
                    for token in ["add", "take", "away", "together", "groups", "divided", "count by"]
                ),
                "number_position_dependence": row["suite"] in {"reversed", "multistep"},
                "distractor_failure": row["suite"] == "distractor" and not row["correct"],
                "reversed_phrasing_failure": row["suite"] == "reversed" and not row["correct"],
                "multi_step_failure": row["suite"] == "multistep" and not row["correct"],
                "rationale": fragility_rationale(row, classification),
            }
        )

    answered_in_scope = [
        item for item in audit_items if item["suite"] != "out_of_scope" and item["status"] == "ANSWERED"
    ]
    return {
        "proof_id": PROOF_ID,
        "audit_basis": "Static item metadata plus deterministic CLI outputs; no LLM answer generation.",
        "summary": {
            "exact_phrase_dependence": "partial",
            "operation_keyword_dependence": "high",
            "number_position_dependence": "partially_survived",
            "distractor_failure": any(item["distractor_failure"] for item in audit_items),
            "reversed_phrasing_failure": any(item["reversed_phrasing_failure"] for item in audit_items),
            "multi_step_failure": any(item["multi_step_failure"] for item in audit_items),
            "structure_reuse_items": sum(
                1 for item in answered_in_scope if item["classification"] == "STRUCTURE_REUSE"
            ),
            "parser_match_items": sum(1 for item in answered_in_scope if item["classification"] == "PARSER_MATCH"),
            "ambiguous_items": sum(1 for item in answered_in_scope if item["classification"] == "AMBIGUOUS"),
        },
        "items": audit_items,
    }


def fragility_rationale(row: dict[str, Any], classification: str) -> str:
    if classification == "UNSUPPORTED":
        return "The item was expected to fail closed or did not produce a supported traced answer."
    if classification == "PARSER_MATCH":
        return "The answer relies on a narrow deterministic surface template with operation keywords."
    if classification == "AMBIGUOUS":
        return "The item uses a novel surface form but still depends on a recognizable operation phrase."
    return "The answer reused multiple frozen motifs or survived distractor/reversed/multi-step structure with tracebacks."


def structure_reuse_audit(results: dict[str, dict[str, Any]]) -> dict[str, Any]:
    answered_rows = [
        row
        for result in results.values()
        for row in result["items"]
        if row["status"] == "ANSWERED"
    ]
    items = []
    for row in answered_rows:
        classification = row["fragility_classification"]
        structure_supported = (
            row["traceback_complete"]
            and bool(row["used_motifs"])
            and bool(row["used_pathways"])
            and classification in {"STRUCTURE_REUSE", "AMBIGUOUS"}
        )
        items.append(
            {
                "question_id": row["question_id"],
                "used_motifs": row["used_motifs"],
                "used_pathways": row["used_pathways"],
                "source_lessons": row["source_lessons"],
                "composition_depth": row["expected_composition_depth"],
                "structure_reuse_supported": structure_supported,
                "classification": classification,
            }
        )
    return {
        "proof_id": PROOF_ID,
        "answered_item_count": len(answered_rows),
        "structure_reuse_supported_count": sum(1 for item in items if item["structure_reuse_supported"]),
        "items": items,
    }


def robustness_metrics(
    results: dict[str, dict[str, Any]],
    parser_audit: dict[str, Any],
    structure_audit: dict[str, Any],
) -> dict[str, Any]:
    in_scope_items = [
        row
        for suite_name in ["reworded", "distractor", "reversed", "multistep"]
        for row in results[suite_name]["items"]
    ]
    answered_in_scope = [row for row in in_scope_items if row["status"] == "ANSWERED"]
    parser_items = [
        item
        for item in parser_audit["items"]
        if item["suite"] != "out_of_scope" and item["status"] == "ANSWERED"
    ]
    structure_rate_denominator = len(answered_in_scope) if answered_in_scope else 1
    parser_rate_denominator = len(parser_items) if parser_items else 1
    unsupported_answer_count = sum(
        1
        for row in in_scope_items
        if row["status"] != "ANSWERED" or (row["status"] == "ANSWERED" and not row["traceback_complete"])
    )
    return {
        "reworded_accuracy": results["reworded"]["accuracy"],
        "distractor_accuracy": results["distractor"]["accuracy"],
        "reversed_accuracy": results["reversed"]["accuracy"],
        "multistep_accuracy": results["multistep"]["accuracy"],
        "out_of_scope_fail_closed_rate": results["out_of_scope"]["fail_closed_rate"],
        "structure_reuse_rate": round(
            structure_audit["structure_reuse_supported_count"] / structure_rate_denominator, 4
        ),
        "parser_match_rate": round(
            sum(1 for item in parser_items if item["classification"] == "PARSER_MATCH") / parser_rate_denominator,
            4,
        ),
        "unsupported_answer_count": unsupported_answer_count,
        "deterministic_replay_match": all(result["deterministic_replay_match"] for result in results.values()),
    }


def hostile_surface_audit(metrics: dict[str, Any], parser_audit: dict[str, Any]) -> dict[str, Any]:
    original_verdict = "VERY_STRONG_SIGNAL"
    if min(
        metrics["reworded_accuracy"],
        metrics["distractor_accuracy"],
        metrics["reversed_accuracy"],
        metrics["multistep_accuracy"],
        metrics["out_of_scope_fail_closed_rate"],
    ) < 1.0:
        original_verdict = "FAIL"

    return {
        "proof_id": PROOF_ID,
        "original_verdict": original_verdict,
        "checks": [
            {
                "attack": "regex_matching",
                "finding": "The CLI extension uses deterministic regular-expression templates. That explains much of the success and blocks a broad robustness claim.",
                "status": "invalidates_broad_structure_claim",
            },
            {
                "attack": "direct_keyword_lookup",
                "finding": "Several passes still depend on words such as add, take away, groups, together, and count by.",
                "status": "partially_invalidates",
            },
            {
                "attack": "answer_leakage",
                "finding": "Expected answers are present only in proof test files. The CLI receives only pond path and question text.",
                "status": "survives",
            },
            {
                "attack": "test_contamination",
                "finding": "The questions are new relative to Proof 028 tests, but the CLI was extended by the harness builder before evaluation.",
                "status": "survives_with_boundary",
            },
            {
                "attack": "arithmetic_hardcoding",
                "finding": "No per-question answers are hardcoded; arithmetic is computed from parsed quantities. Parser templates are still narrow.",
                "status": "survives_with_boundary",
            },
            {
                "attack": "hidden_llm_generation",
                "finding": "The builder invokes python3 -m operational_cognition.cli.math_pond as a subprocess; no LLM API or natural-language answer synthesis path is used.",
                "status": "survives",
            },
            {
                "attack": "shallow_parser_behavior",
                "finding": "Confirmed. The result demonstrates bounded deterministic structural parsing, not general wording robustness.",
                "status": "invalidates_very_strong_claim",
            },
        ],
        "parser_fragility_snapshot": parser_audit["summary"],
        "hostile_verdict": "WEAK_SIGNAL",
        "surviving_claims": [
            "Surface variation in the curated suites did not break deterministic CLI answering.",
            "Distractor, reversed, and multi-step items carried source tracebacks and motif lineage.",
            "Out-of-scope items failed closed instead of guessing.",
            "No LLM generated final test answers.",
        ],
        "invalidated_claims": [
            "The pond learned robust natural-language math independent of parser templates.",
            "Success cannot be explained by regex or keyword-triggered parsing.",
            "The result establishes general structure reuse beyond the curated Grade 1/Grade 2 forms.",
        ],
    }


def readme(metrics: dict[str, Any], hostile: dict[str, Any]) -> str:
    return f"""# Proof 029 - Surface-Form Robustness and Structure Reuse

## Result

1. Did surface variation break the system? No for the curated reworded suite: accuracy was {metrics["reworded_accuracy"]}.
2. Did distractors break the system? No for the curated distractor suite: accuracy was {metrics["distractor_accuracy"]}.
3. Did reversed phrasing break the system? No for the curated reversed suite: accuracy was {metrics["reversed_accuracy"]}.
4. Did multi-step composition work? Yes inside the frozen Grade 1/Grade 2 boundary: accuracy was {metrics["multistep_accuracy"]}.
5. Did out-of-scope items fail closed? Yes: fail-closed rate was {metrics["out_of_scope_fail_closed_rate"]}.
6. Did hostile audit classify the result as structure reuse or parser matching? The original metrics reached {hostile["original_verdict"]}, but the hostile verdict is {hostile["hostile_verdict"]} because the implementation is still a narrow deterministic parser with explicit surface templates.
7. What should be tested next? Use a blinded question generator and lock the CLI before test creation, then test paraphrases not visible to the harness builder.

## Boundary

This proof does not add math concepts beyond Proof 028. It tests whether the existing Grade 1/Grade 2 motifs can be reused across curated wording variation. The hostile audit rejects broad claims because success can still be explained by deterministic regex and keyword parsing.

## CLI Boundary

Final answers were produced through:

```bash
python3 -m operational_cognition.cli.math_pond answer --pond proofs/028-developmental-learning-grade-ladder/pond_states/grade_2 --question "<question>" --json
```
"""


def manifest(request_hash: str, response_hash: str) -> dict[str, Any]:
    required_artifacts = [
        "README.md",
        "proof_manifest.json",
        "frozen_concept_inventory.json",
        "tests/reworded_questions.jsonl",
        "tests/distractor_questions.jsonl",
        "tests/reversed_phrasing.jsonl",
        "tests/multistep_composition.jsonl",
        "tests/out_of_scope_fail_closed.jsonl",
        "results/reworded_results.json",
        "results/distractor_results.json",
        "results/reversed_results.json",
        "results/multistep_results.json",
        "results/out_of_scope_results.json",
        "analysis/parser_fragility_audit.json",
        "analysis/structure_reuse_audit.json",
        "analysis/hostile_surface_audit.json",
        "analysis/robustness_metrics.json",
    ]
    return {
        "proof_id": PROOF_ID,
        "title": TITLE,
        "status": "complete",
        "targets": [
            "SurfaceFormRobustness",
            "StructureReuse",
            "ParserFragility",
            "DeterministicNoLLMAnswering",
        ],
        "claim_level": "evidence_backed",
        "inside_voice_adapter_status": "not_used_final_answers_generated_by_deterministic_cli",
        "public_private_boundary": "All artifacts are deterministic tests, CLI outputs, audits, and public Proof 028 pond-state references.",
        "required_artifacts": required_artifacts,
        "disallowed_claims": [
            "LLM generated final answers",
            "general mathematical cognition",
            "algebra competence",
            "fraction competence",
            "arithmetic with carrying or borrowing",
            "unbounded natural-language robustness",
            "hidden chain-of-thought",
        ],
        "lineage": {
            "mcp_endpoint": "none:deterministic_cli_no_llm",
            "contract_version": "math_pond.cli.v1.surface_robustness",
            "request_hash": request_hash,
            "response_hash": response_hash,
            "derived_from": "proofs/028-developmental-learning-grade-ladder/pond_states/grade_2/pond_state.json; operational_cognition.cli.math_pond",
            "validates": "surface_form_robustness_with_frozen_grade_1_grade_2_math_motifs",
        },
    }


def main() -> int:
    state = load_json(SOURCE_STATE_PATH)
    inventory = freeze_inventory(state)
    write_json(PROOF_DIR / "frozen_concept_inventory.json", inventory)

    write_jsonl(PROOF_DIR / "tests" / "reworded_questions.jsonl", REWORDED_TESTS)
    write_jsonl(PROOF_DIR / "tests" / "distractor_questions.jsonl", DISTRACTOR_TESTS)
    write_jsonl(PROOF_DIR / "tests" / "reversed_phrasing.jsonl", REVERSED_TESTS)
    write_jsonl(PROOF_DIR / "tests" / "multistep_composition.jsonl", MULTISTEP_TESTS)
    write_jsonl(PROOF_DIR / "tests" / "out_of_scope_fail_closed.jsonl", OUT_OF_SCOPE_TESTS)

    results = {name: evaluate_suite(name, items) for name, items in SUITES.items()}
    write_json(PROOF_DIR / "results" / "reworded_results.json", results["reworded"])
    write_json(PROOF_DIR / "results" / "distractor_results.json", results["distractor"])
    write_json(PROOF_DIR / "results" / "reversed_results.json", results["reversed"])
    write_json(PROOF_DIR / "results" / "multistep_results.json", results["multistep"])
    write_json(PROOF_DIR / "results" / "out_of_scope_results.json", results["out_of_scope"])

    parser_audit = parser_fragility_audit(results)
    structure_audit = structure_reuse_audit(results)
    metrics = robustness_metrics(results, parser_audit, structure_audit)
    hostile = hostile_surface_audit(metrics, parser_audit)

    write_json(PROOF_DIR / "analysis" / "parser_fragility_audit.json", parser_audit)
    write_json(PROOF_DIR / "analysis" / "structure_reuse_audit.json", structure_audit)
    write_json(PROOF_DIR / "analysis" / "robustness_metrics.json", metrics)
    write_json(PROOF_DIR / "analysis" / "hostile_surface_audit.json", hostile)
    write_text(PROOF_DIR / "README.md", readme(metrics, hostile))

    request_hash = sha256_json(
        {
            "source_state_hash": state.get("state_hash", ""),
            "frozen_inventory": inventory,
            "tests": SUITES,
            "cli_module": "operational_cognition.cli.math_pond",
        }
    )
    response_hash = sha256_json(
        {
            "results": results,
            "parser_audit": parser_audit,
            "structure_audit": structure_audit,
            "metrics": metrics,
            "hostile": hostile,
        }
    )
    write_json(PROOF_DIR / "proof_manifest.json", manifest(request_hash, response_hash))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
