"""Deterministic grade-ladder math pond CLI.

The answer engine is intentionally small and closed-world. It answers only
when a question matches a supported arithmetic form and the loaded pond state
contains every required concept motif. Otherwise it fails closed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


STATE_FILE = "pond_state.json"


def load_pond(path: Path) -> dict[str, Any]:
    state_path = path / STATE_FILE if path.is_dir() else path
    try:
        with state_path.open("r", encoding="utf-8") as handle:
            state = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return {
            "schema_version": "math_pond_state.v1",
            "state_id": "missing_or_invalid",
            "concepts": {},
            "motifs": {},
            "lessons": {},
        }
    if not isinstance(state, dict):
        return {
            "schema_version": "math_pond_state.v1",
            "state_id": "invalid_type",
            "concepts": {},
            "motifs": {},
            "lessons": {},
        }
    return state


def normalize(question: str) -> str:
    lowered = question.strip().lower()
    lowered = lowered.replace("?", "")
    lowered = lowered.replace(",", " ")
    lowered = lowered.replace(":", " ")
    lowered = lowered.replace(".", " ")
    lowered = re.sub(r"\s+", " ", lowered).strip()
    return lowered


def no_carry(a: int, b: int) -> bool:
    return a % 10 + b % 10 < 10


def no_borrow(a: int, b: int) -> bool:
    return a >= b and a % 10 >= b % 10


def learned(state: dict[str, Any], concept: str) -> bool:
    concepts = state.get("concepts", {})
    return isinstance(concepts, dict) and concept in concepts


def motifs_for(state: dict[str, Any], concepts: list[str]) -> list[dict[str, Any]]:
    motifs = state.get("motifs", {})
    concept_rows = state.get("concepts", {})
    if not isinstance(motifs, dict) or not isinstance(concept_rows, dict):
        return []

    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for concept in concepts:
        concept_row = concept_rows.get(concept, {})
        motif_ids = concept_row.get("motifs", []) if isinstance(concept_row, dict) else []
        for motif_id in motif_ids:
            if motif_id in seen:
                continue
            motif = motifs.get(motif_id, {})
            if isinstance(motif, dict):
                rows.append(
                    {
                        "motif_id": motif_id,
                        "concept": motif.get("concept", concept),
                        "grade": motif.get("grade"),
                        "lesson_id": motif.get("lesson_id"),
                    }
                )
                seen.add(motif_id)
    return rows


def tracebacks_for(state: dict[str, Any], concepts: list[str]) -> list[dict[str, Any]]:
    lessons = state.get("lessons", {})
    concept_rows = state.get("concepts", {})
    if not isinstance(lessons, dict) or not isinstance(concept_rows, dict):
        return []

    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for concept in concepts:
        concept_row = concept_rows.get(concept, {})
        lesson_ids = concept_row.get("lesson_ids", []) if isinstance(concept_row, dict) else []
        for lesson_id in lesson_ids:
            if lesson_id in seen:
                continue
            lesson = lessons.get(lesson_id, {})
            if isinstance(lesson, dict):
                rows.append(
                    {
                        "lesson_id": lesson_id,
                        "concept": lesson.get("concept", concept),
                        "rule": lesson.get("rule", ""),
                        "trace_expectation": lesson.get("trace_expectation", ""),
                        "expected_motif": lesson.get("expected_motif", ""),
                    }
                )
                seen.add(lesson_id)
    return rows


def fail_closed(question: str, reason: str, pathway: list[str] | None = None) -> dict[str, Any]:
    return {
        "question": question,
        "answer": "",
        "status": "FAIL_CLOSED",
        "concept_pathway": pathway or [],
        "motif_lineage": [],
        "source_tracebacks": [],
        "confidence": 0.0,
        "fail_closed_reason": reason,
    }


def answered(
    question: str,
    answer: int | str | bool,
    concepts: list[str],
    state: dict[str, Any],
) -> dict[str, Any]:
    missing = [concept for concept in concepts if not learned(state, concept)]
    if missing:
        return fail_closed(question, "missing_required_motifs:" + ",".join(missing), concepts)

    motif_lineage = motifs_for(state, concepts)
    source_tracebacks = tracebacks_for(state, concepts)
    if len(source_tracebacks) < len(set(concepts)):
        return fail_closed(question, "incomplete_source_tracebacks", concepts)

    if isinstance(answer, bool):
        rendered = "true" if answer else "false"
    else:
        rendered = str(answer)

    confidence = min(0.95, 0.55 + 0.08 * len(set(concepts)))
    return {
        "question": question,
        "answer": rendered,
        "status": "ANSWERED",
        "concept_pathway": concepts,
        "motif_lineage": motif_lineage,
        "source_tracebacks": source_tracebacks,
        "confidence": round(confidence, 2),
    }


def addition_concepts(a: int, b: int, word_problem: bool = False) -> list[str] | None:
    if a < 10 and b < 10:
        concepts = ["counting", "one_digit_addition"]
    elif a < 100 and b < 100 and no_carry(a, b):
        concepts = [
            "counting",
            "one_digit_addition",
            "place_value",
            "two_digit_addition_without_carrying",
        ]
    else:
        return None
    if word_problem:
        concepts.append("simple_word_problems")
    return concepts


def subtraction_concepts(a: int, b: int, word_problem: bool = False) -> list[str] | None:
    if a < b:
        return None
    if a < 10 and b < 10:
        concepts = ["counting", "one_digit_subtraction"]
    elif a < 100 and b < 100 and no_borrow(a, b):
        concepts = [
            "counting",
            "one_digit_subtraction",
            "place_value",
            "two_digit_subtraction_without_borrowing",
        ]
    else:
        return None
    if word_problem:
        concepts.append("simple_word_problems")
    return concepts


def comparison_concepts(a: int, b: int) -> list[str]:
    if max(a, b) < 10:
        return ["counting", "number_comparison"]
    return ["counting", "number_comparison", "place_value"]


def multiplication_concepts(groups: int, size: int, word_problem: bool = False) -> list[str] | None:
    if groups <= 0 or size <= 0 or groups > 6 or size > 6:
        return None
    concepts = ["counting", "one_digit_addition", "multiplication_as_repeated_addition"]
    if word_problem:
        concepts.append("simple_word_problems")
    return concepts


def merge_concepts(*concept_lists: list[str] | None) -> list[str] | None:
    merged: list[str] = []
    for concept_list in concept_lists:
        if concept_list is None:
            return None
        for concept in concept_list:
            if concept not in merged:
                merged.append(concept)
    return merged


def answer_question(question: str, state: dict[str, Any]) -> dict[str, Any]:
    q = normalize(question)

    match = re.fullmatch(r"what number comes after (\d+)", q)
    if match:
        n = int(match.group(1))
        return answered(question, n + 1, ["counting"], state)

    match = re.fullmatch(r"what is (\d+) \+ (\d+)", q) or re.fullmatch(r"(\d+) \+ (\d+)", q)
    if match:
        a, b = int(match.group(1)), int(match.group(2))
        concepts = addition_concepts(a, b)
        if concepts is None:
            return fail_closed(question, "addition_form_not_seasoned")
        return answered(question, a + b, concepts, state)

    match = re.fullmatch(r"what do you get when you put (\d+) and (\d+) together", q)
    if match:
        a, b = int(match.group(1)), int(match.group(2))
        concepts = addition_concepts(a, b)
        if concepts is None:
            return fail_closed(question, "addition_form_not_seasoned")
        return answered(question, a + b, concepts, state)

    match = re.fullmatch(r"start with (\d+) add (\d+) what number do you land on", q)
    if match:
        a, b = int(match.group(1)), int(match.group(2))
        concepts = addition_concepts(a, b)
        if concepts is None:
            return fail_closed(question, "addition_form_not_seasoned")
        return answered(question, a + b, concepts, state)

    match = re.fullmatch(r"what is (\d+) - (\d+)", q) or re.fullmatch(r"(\d+) - (\d+)", q)
    if match:
        a, b = int(match.group(1)), int(match.group(2))
        concepts = subtraction_concepts(a, b)
        if concepts is None:
            return fail_closed(question, "subtraction_form_not_seasoned")
        return answered(question, a - b, concepts, state)

    match = re.fullmatch(r"take (\d+) away from (\d+)", q)
    if match:
        b, a = int(match.group(1)), int(match.group(2))
        concepts = subtraction_concepts(a, b)
        if concepts is None:
            return fail_closed(question, "subtraction_form_not_seasoned")
        return answered(question, a - b, concepts, state)

    match = re.fullmatch(r"does (\d+) \+ (\d+) = (\d+)", q)
    if match:
        a, b, c = int(match.group(1)), int(match.group(2)), int(match.group(3))
        concepts = addition_concepts(a, b)
        if concepts is None:
            return fail_closed(question, "equality_addition_form_not_seasoned")
        return answered(question, a + b == c, concepts + ["equality"], state)

    match = re.fullmatch(r"is (\d+) = (\d+)", q)
    if match:
        a, b = int(match.group(1)), int(match.group(2))
        return answered(question, a == b, ["equality"], state)

    match = re.fullmatch(r"which is larger (\d+) or (\d+)", q)
    if match:
        a, b = int(match.group(1)), int(match.group(2))
        return answered(question, max(a, b), comparison_concepts(a, b), state)

    match = re.fullmatch(r"which is smaller (\d+) or (\d+)", q)
    if match:
        a, b = int(match.group(1)), int(match.group(2))
        return answered(question, min(a, b), comparison_concepts(a, b), state)

    match = re.fullmatch(r"which number is smaller (\d+) or (\d+)", q)
    if match:
        a, b = int(match.group(1)), int(match.group(2))
        return answered(question, min(a, b), comparison_concepts(a, b), state)

    match = re.fullmatch(r"which number is greater (\d+) or (\d+)", q)
    if match:
        a, b = int(match.group(1)), int(match.group(2))
        return answered(question, max(a, b), comparison_concepts(a, b), state)

    match = re.fullmatch(r"is (\d+) greater than (\d+)", q)
    if match:
        a, b = int(match.group(1)), int(match.group(2))
        return answered(question, a > b, comparison_concepts(a, b), state)

    match = re.fullmatch(r"how many tens and ones are in (\d+)", q)
    if match:
        n = int(match.group(1))
        if not 10 <= n <= 99:
            return fail_closed(question, "place_value_range_not_seasoned")
        return answered(question, f"{n // 10} tens and {n % 10} ones", ["counting", "place_value"], state)

    match = re.fullmatch(r"break (\d+) into tens and ones", q)
    if match:
        n = int(match.group(1))
        if not 10 <= n <= 99:
            return fail_closed(question, "place_value_range_not_seasoned")
        return answered(question, f"{n // 10} tens and {n % 10} ones", ["counting", "place_value"], state)

    match = re.fullmatch(r"count by (\d+)s what comes after (\d+)", q)
    if match:
        step, n = int(match.group(1)), int(match.group(2))
        if step <= 0:
            return fail_closed(question, "invalid_skip_count_step")
        concepts = ["counting", "one_digit_addition", "skip_counting"]
        return answered(question, n + step, concepts, state)

    match = re.fullmatch(r"if you count by (\d+)s what comes after (\d+)", q)
    if match:
        step, n = int(match.group(1)), int(match.group(2))
        if step <= 0:
            return fail_closed(question, "invalid_skip_count_step")
        concepts = ["counting", "one_digit_addition", "skip_counting"]
        return answered(question, n + step, concepts, state)

    match = re.fullmatch(r"what number is (\d+) more than (\d+)", q)
    if match:
        delta, n = int(match.group(1)), int(match.group(2))
        concepts = addition_concepts(n, delta)
        if concepts is None:
            return fail_closed(question, "more_than_form_not_seasoned")
        if n >= 10 or delta >= 10:
            concepts = [
                "counting",
                "one_digit_addition",
                "place_value",
                "two_digit_addition_without_carrying",
            ]
        return answered(question, n + delta, concepts, state)

    match = re.fullmatch(r"what is (\d+) groups of (\d+)", q)
    if match:
        groups, size = int(match.group(1)), int(match.group(2))
        concepts = multiplication_concepts(groups, size)
        if concepts is None:
            return fail_closed(question, "multiplication_factor_range_not_seasoned")
        return answered(question, groups * size, concepts, state)

    match = re.fullmatch(r"what is (\d+) times (\d+)", q) or re.fullmatch(r"what is (\d+) x (\d+)", q)
    if match:
        a, b = int(match.group(1)), int(match.group(2))
        concepts = multiplication_concepts(a, b)
        if concepts is None:
            return fail_closed(question, "multiplication_factor_range_not_seasoned")
        return answered(question, a * b, concepts, state)

    match = re.fullmatch(r"if there are (\d+) bags with (\d+) apples each how many apples", q)
    if match:
        groups, size = int(match.group(1)), int(match.group(2))
        concepts = multiplication_concepts(groups, size, word_problem=True)
        if concepts is None:
            return fail_closed(question, "multiplication_factor_range_not_seasoned")
        return answered(question, groups * size, concepts, state)

    match = re.fullmatch(r"share (\d+) \w+ equally into (\d+) groups how many in each group", q)
    if match:
        total, groups = int(match.group(1)), int(match.group(2))
        if groups == 0 or total % groups != 0:
            return fail_closed(question, "division_remainder_not_seasoned")
        concepts = ["counting", "one_digit_subtraction", "division_as_grouping"]
        return answered(question, total // groups, concepts, state)

    match = re.fullmatch(r"how many groups of (\d+) can be made from (\d+)", q)
    if match:
        size, total = int(match.group(1)), int(match.group(2))
        if size == 0 or total % size != 0:
            return fail_closed(question, "division_remainder_not_seasoned")
        concepts = ["counting", "one_digit_subtraction", "division_as_grouping"]
        return answered(question, total // size, concepts, state)

    match = re.fullmatch(r"what is (\d+) divided by (\d+)", q)
    if match:
        total, groups = int(match.group(1)), int(match.group(2))
        if groups == 0 or total % groups != 0:
            return fail_closed(question, "division_remainder_not_seasoned")
        concepts = ["counting", "one_digit_subtraction", "division_as_grouping"]
        return answered(question, total // groups, concepts, state)

    match = re.fullmatch(r"\w+ has (\d+) \w+ and finds (\d+) more how many \w+ now", q)
    if match:
        a, b = int(match.group(1)), int(match.group(2))
        concepts = addition_concepts(a, b, word_problem=True)
        if concepts is None:
            return fail_closed(question, "word_addition_form_not_seasoned")
        return answered(question, a + b, concepts, state)

    match = re.fullmatch(r"\w+ has (\d+) \w+ and gets (\d+) more how many \w+ now", q)
    if match:
        a, b = int(match.group(1)), int(match.group(2))
        concepts = addition_concepts(a, b, word_problem=True)
        if concepts is None:
            return fail_closed(question, "word_addition_form_not_seasoned")
        return answered(question, a + b, concepts, state)

    match = re.fullmatch(r"\w+ has (\d+) \w+ and gives away (\d+) how many \w+ remain", q)
    if match:
        a, b = int(match.group(1)), int(match.group(2))
        concepts = subtraction_concepts(a, b, word_problem=True)
        if concepts is None:
            return fail_closed(question, "word_subtraction_form_not_seasoned")
        return answered(question, a - b, concepts, state)

    match = re.fullmatch(r"what number must be added to (\d+) to make (\d+)", q)
    if match:
        addend, total = int(match.group(1)), int(match.group(2))
        missing = total - addend
        if missing < 0:
            return fail_closed(question, "reverse_addition_form_not_seasoned")
        concepts = merge_concepts(addition_concepts(addend, missing), ["equality"])
        if concepts is None:
            return fail_closed(question, "reverse_addition_form_not_seasoned")
        return answered(question, missing, concepts, state)

    match = re.fullmatch(r"after losing (\d+) \w+ \w+ has (\d+) left how many did \w+ have before", q)
    if match:
        lost, remaining = int(match.group(1)), int(match.group(2))
        concepts = merge_concepts(
            addition_concepts(remaining, lost, word_problem=True),
            ["one_digit_subtraction", "equality"],
        )
        if concepts is None:
            return fail_closed(question, "reverse_subtraction_form_not_seasoned")
        return answered(question, remaining + lost, concepts, state)

    match = re.fullmatch(r"what must be taken from (\d+) to leave (\d+)", q)
    if match:
        start, remaining = int(match.group(1)), int(match.group(2))
        taken = start - remaining
        if taken < 0:
            return fail_closed(question, "reverse_subtraction_form_not_seasoned")
        concepts = merge_concepts(subtraction_concepts(start, taken), ["equality"])
        if concepts is None:
            return fail_closed(question, "reverse_subtraction_form_not_seasoned")
        return answered(question, taken, concepts, state)

    match = re.fullmatch(r"there are (\d+) red (\w+) (\d+) green \w+ and (\d+) empty \w+ how many \w+ are there", q)
    if match:
        red, green = int(match.group(1)), int(match.group(3))
        concepts = addition_concepts(red, green, word_problem=True)
        if concepts is None:
            return fail_closed(question, "distractor_addition_form_not_seasoned")
        return answered(question, red + green, concepts, state)

    match = re.fullmatch(r"a class has (\d+) pencils (\d+) erasers and (\d+) rulers how many pencils and erasers together", q)
    if match:
        pencils, erasers = int(match.group(1)), int(match.group(2))
        concepts = addition_concepts(pencils, erasers, word_problem=True)
        if concepts is None:
            return fail_closed(question, "distractor_addition_form_not_seasoned")
        return answered(question, pencils + erasers, concepts, state)

    match = re.fullmatch(r"there are (\d+) blue cars (\d+) red cars and (\d+) bikes how many cars are there", q)
    if match:
        blue, red = int(match.group(1)), int(match.group(2))
        concepts = addition_concepts(blue, red, word_problem=True)
        if concepts is None:
            return fail_closed(question, "distractor_addition_form_not_seasoned")
        return answered(question, blue + red, concepts, state)

    match = re.fullmatch(r"\w+ has (\d+) stickers gives (\d+) stickers to \w+ and sees (\d+) stamps how many stickers does \w+ have now", q)
    if match:
        start, given = int(match.group(1)), int(match.group(2))
        concepts = subtraction_concepts(start, given, word_problem=True)
        if concepts is None:
            return fail_closed(question, "distractor_subtraction_form_not_seasoned")
        return answered(question, start - given, concepts, state)

    match = re.fullmatch(r"a shelf has (\d+) boxes with (\d+) books each and (\d+) empty boxes how many books are on the shelf", q)
    if match:
        groups, size = int(match.group(1)), int(match.group(2))
        concepts = multiplication_concepts(groups, size, word_problem=True)
        if concepts is None:
            return fail_closed(question, "multiplication_factor_range_not_seasoned")
        return answered(question, groups * size, concepts, state)

    match = re.fullmatch(r"there are (\d+) bags with (\d+) apples each then (\d+) apples are eaten how many remain", q)
    if match:
        groups, size, eaten = int(match.group(1)), int(match.group(2)), int(match.group(3))
        total = groups * size
        concepts = merge_concepts(
            multiplication_concepts(groups, size, word_problem=True),
            subtraction_concepts(total, eaten, word_problem=True),
        )
        if concepts is None:
            return fail_closed(question, "multistep_form_not_seasoned")
        return answered(question, total - eaten, concepts, state)

    match = re.fullmatch(r"start at (\d+) add (\d+) then take away (\d+)", q)
    if match:
        start, added, taken = int(match.group(1)), int(match.group(2)), int(match.group(3))
        subtotal = start + added
        concepts = merge_concepts(addition_concepts(start, added), subtraction_concepts(subtotal, taken))
        if concepts is None:
            return fail_closed(question, "multistep_form_not_seasoned")
        return answered(question, subtotal - taken, concepts, state)

    match = re.fullmatch(r"(\d+) groups of (\d+) \w+ join (\d+) more \w+ how many \w+", q)
    if match:
        groups, size, extra = int(match.group(1)), int(match.group(2)), int(match.group(3))
        subtotal = groups * size
        concepts = merge_concepts(
            multiplication_concepts(groups, size, word_problem=True),
            addition_concepts(subtotal, extra, word_problem=True),
        )
        if concepts is None:
            return fail_closed(question, "multistep_form_not_seasoned")
        return answered(question, subtotal + extra, concepts, state)

    match = re.fullmatch(r"a class has (\d+) pencils and gets (\d+) more then gives away (\d+) pencils how many pencils remain", q)
    if match:
        start, added, given = int(match.group(1)), int(match.group(2)), int(match.group(3))
        subtotal = start + added
        concepts = merge_concepts(
            addition_concepts(start, added, word_problem=True),
            subtraction_concepts(subtotal, given, word_problem=True),
        )
        if concepts is None:
            return fail_closed(question, "multistep_form_not_seasoned")
        return answered(question, subtotal - given, concepts, state)

    match = re.fullmatch(r"count by (\d+)s after (\d+) then add (\d+) what number is it", q)
    if match:
        step, start, added = int(match.group(1)), int(match.group(2)), int(match.group(3))
        subtotal = start + step
        concepts = merge_concepts(["counting", "one_digit_addition", "skip_counting"], addition_concepts(subtotal, added))
        if concepts is None:
            return fail_closed(question, "multistep_form_not_seasoned")
        return answered(question, subtotal + added, concepts, state)

    match = re.fullmatch(r"if (\d+) \w+ are on a \w+ and (\d+) fly away how many remain", q)
    if match:
        a, b = int(match.group(1)), int(match.group(2))
        concepts = subtraction_concepts(a, b, word_problem=True)
        if concepts is None:
            return fail_closed(question, "word_subtraction_form_not_seasoned")
        return answered(question, a - b, concepts, state)

    return fail_closed(question, "unrecognized_question_form")


def run_answer(args: argparse.Namespace) -> int:
    state = load_pond(Path(args.pond))
    result = answer_question(args.question, state)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=True))
    else:
        print(result["answer"] if result["status"] == "ANSWERED" else result["status"])
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python3 -m operational_cognition.cli.math_pond")
    subparsers = parser.add_subparsers(dest="command", required=True)
    answer_parser = subparsers.add_parser("answer", help="Answer one math question from a pond state.")
    answer_parser.add_argument("--pond", required=True, help="Path to a pond directory or pond_state.json file.")
    answer_parser.add_argument("--question", required=True, help="Question to answer.")
    answer_parser.add_argument("--json", action="store_true", help="Emit JSON.")
    answer_parser.set_defaults(func=run_answer)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
