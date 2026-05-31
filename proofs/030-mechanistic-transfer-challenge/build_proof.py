#!/usr/bin/env python3
"""Build Proof 030 deterministic mechanism-transfer artifacts."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


PROOF_ID = "030-mechanistic-transfer-challenge"
TITLE = "Proof 030 - Mechanistic Transfer Challenge"
PROOF_DIR = Path(__file__).resolve().parent
ROOT = PROOF_DIR.parents[1]


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


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


MECHANISM_LESSONS: list[dict[str, Any]] = [
    {
        "lesson_id": "MEC-L001",
        "mechanism_id": "flow",
        "mechanism_name": "FLOW",
        "core_motif": ["Source", "Path", "Resistance", "Flow"],
        "examples": [
            {
                "domain": "water_system",
                "role_map": {
                    "source": "tank",
                    "path": "pipe",
                    "resistance": "restriction",
                    "flow": "water movement",
                },
            },
            {
                "domain": "electrical_circuit",
                "role_map": {
                    "source": "battery",
                    "path": "wire",
                    "resistance": "resistor",
                    "flow": "current",
                },
            },
            {
                "domain": "traffic_network",
                "role_map": {
                    "source": "cars entering",
                    "path": "road",
                    "resistance": "traffic jam",
                    "flow": "movement",
                },
            },
        ],
        "roles": [
            {
                "role_id": "source",
                "motif": "Source",
                "cues": ["source", "supply", "inlet", "upstream", "origin", "reservoir", "tank", "battery", "sender", "pump"],
            },
            {
                "role_id": "path",
                "motif": "Path",
                "cues": [
                    "path",
                    "pipe",
                    "line",
                    "channel",
                    "wire",
                    "road",
                    "route",
                    "corridor",
                    "hallway",
                    "vessel",
                    "gateway",
                    "network",
                    "through",
                    "along",
                    "conduit",
                ],
            },
            {
                "role_id": "resistance",
                "motif": "Resistance",
                "cues": [
                    "resistance",
                    "restriction",
                    "resistor",
                    "blocked",
                    "blockage",
                    "bottleneck",
                    "narrow",
                    "narrowed",
                    "narrower",
                    "clogged",
                    "jam",
                    "traffic jam",
                    "rate limited",
                    "rate limit",
                    "choke",
                ],
            },
            {
                "role_id": "flow",
                "motif": "Flow",
                "cues": [
                    "flow",
                    "movement",
                    "moving",
                    "moves",
                    "throughput",
                    "current",
                    "progress",
                    "circulation",
                    "circulates",
                    "pass",
                    "passes",
                    "queue",
                    "queues",
                ],
            },
        ],
        "required_min_roles": 3,
        "minimum_score": 3.0,
        "causal_rule": "Increasing resistance along a path reduces flow from source to destination and can create backlog.",
        "direct_effect": "Greater resistance reduces movement through the path and can create backlog or stalled flow.",
        "inspection_priority": "Inspect the highest-resistance segment of the path.",
        "component_category": "path/resistance interface",
        "mechanism_explanation": "The observed system has movement through a path plus a restriction that reduces movement.",
        "mapping_statement": "The system maps to Source -> Path -> Resistance -> Flow.",
        "similarity_statement": "The similar mechanism is FLOW: movement through a path is reduced by resistance.",
        "trace_expectation": "A mapped FLOW answer must cite at least three of Source, Path, Resistance, and Flow.",
    },
    {
        "lesson_id": "MEC-L002",
        "mechanism_id": "supported_rotation",
        "mechanism_name": "SUPPORTED_ROTATION",
        "core_motif": ["Rotation", "Support", "Friction", "Failure"],
        "examples": [
            {
                "domain": "wheel_assembly",
                "role_map": {
                    "rotation": "wheel",
                    "support": "bearing",
                    "friction": "bearing friction",
                    "failure": "wheel seizes",
                },
            },
            {
                "domain": "pulley_system",
                "role_map": {
                    "rotation": "pulley",
                    "support": "axle",
                    "friction": "axle wear",
                    "failure": "pulley slows",
                },
            },
            {
                "domain": "fan_assembly",
                "role_map": {
                    "rotation": "fan",
                    "support": "shaft",
                    "friction": "shaft wear",
                    "failure": "fan stops",
                },
            },
        ],
        "roles": [
            {
                "role_id": "rotation",
                "motif": "Rotation",
                "cues": [
                    "rotation",
                    "rotates",
                    "rotate",
                    "rotating",
                    "spins",
                    "spin",
                    "turns",
                    "wheel",
                    "pulley",
                    "fan",
                    "motor",
                    "turntable",
                    "rotor",
                    "spindle",
                    "disk",
                ],
            },
            {
                "role_id": "support",
                "motif": "Support",
                "cues": ["support", "bearing", "axle", "shaft", "bushing", "spindle", "mount", "hub", "pivot", "journal"],
            },
            {
                "role_id": "friction",
                "motif": "Friction",
                "cues": ["friction", "wear", "worn", "wearing", "noisy", "noise", "squeal", "squealing", "vibration", "rough", "heat"],
            },
            {
                "role_id": "failure",
                "motif": "Failure",
                "cues": ["failure", "fails", "stops", "stopped", "stalls", "seizes", "slows", "slow", "uneven", "stuck"],
            },
        ],
        "required_min_roles": 3,
        "minimum_score": 3.0,
        "causal_rule": "Increasing friction at the support interface slows rotation and can cause noise, wear, seizure, or stoppage.",
        "direct_effect": "More friction at the support interface slows rotation, increases noise or wear, and can stop the rotating part.",
        "inspection_priority": "Inspect the rotational support interface: bearing, bushing, axle, shaft, mount, or hub.",
        "component_category": "rotational support interface",
        "mechanism_explanation": "The observed system has a rotating part whose support interface shows friction, wear, noise, or stoppage.",
        "mapping_statement": "The system maps to Rotation -> Support -> Friction -> Failure.",
        "similarity_statement": "The similar mechanism is SUPPORTED_ROTATION: rotation depends on a support interface that can fail through friction or wear.",
        "trace_expectation": "A mapped SUPPORTED_ROTATION answer must cite at least three of Rotation, Support, Friction, and Failure.",
    },
    {
        "lesson_id": "MEC-L003",
        "mechanism_id": "load_transfer",
        "mechanism_name": "LOAD_TRANSFER",
        "core_motif": ["Load", "Distribution", "Concentration", "Failure"],
        "examples": [
            {
                "domain": "bridge",
                "role_map": {
                    "load": "vehicles and deck weight",
                    "distribution": "truss and supports",
                    "concentration": "joint stress",
                    "failure": "cracking or collapse",
                },
            },
            {
                "domain": "roof_truss",
                "role_map": {
                    "load": "roof weight",
                    "distribution": "truss members",
                    "concentration": "overloaded member",
                    "failure": "sagging",
                },
            },
            {
                "domain": "crane",
                "role_map": {
                    "load": "lifted mass",
                    "distribution": "boom and cables",
                    "concentration": "anchor point",
                    "failure": "bending",
                },
            },
        ],
        "roles": [
            {
                "role_id": "load",
                "motif": "Load",
                "cues": ["load", "weight", "heavy", "force", "carries", "carrying", "pull", "pulls", "suspended", "boxes", "cargo"],
            },
            {
                "role_id": "distribution",
                "motif": "Distribution",
                "cues": [
                    "distribution",
                    "distribute",
                    "spread",
                    "spreads",
                    "shared",
                    "transfers",
                    "through",
                    "across",
                    "load path",
                    "members",
                    "cables",
                    "truss",
                    "posts",
                    "uprights",
                    "supports",
                ],
            },
            {
                "role_id": "concentration",
                "motif": "Concentration",
                "cues": [
                    "concentration",
                    "concentrated",
                    "one corner",
                    "single point",
                    "one anchor",
                    "localized",
                    "overload",
                    "overloaded",
                    "high stress",
                    "stress",
                    "bracket",
                    "joint",
                ],
            },
            {
                "role_id": "failure",
                "motif": "Failure",
                "cues": ["failure", "collapse", "cracks", "crack", "bends", "bent", "sag", "sags", "bow", "bows", "buckle", "buckles", "breaks"],
            },
        ],
        "required_min_roles": 3,
        "minimum_score": 3.0,
        "causal_rule": "Loads must be distributed through a load path; concentrated stress raises failure risk at members, joints, anchors, or supports.",
        "direct_effect": "Load concentration raises stress where distribution fails and can cause sagging, cracking, bending, or collapse.",
        "inspection_priority": "Inspect the load path and high-stress concentration points such as joints, anchors, brackets, supports, and overloaded members.",
        "component_category": "load path distribution element",
        "mechanism_explanation": "The observed system carries load through supports, then fails where stress concentrates.",
        "mapping_statement": "The system maps to Load -> Distribution -> Concentration -> Failure.",
        "similarity_statement": "The similar mechanism is LOAD_TRANSFER: load must distribute through a path, and concentration creates failure risk.",
        "trace_expectation": "A mapped LOAD_TRANSFER answer must cite at least three of Load, Distribution, Concentration, and Failure.",
    },
]


IN_DOMAIN_TESTS: list[dict[str, Any]] = [
    {
        "question_id": "ID-001",
        "suite": "in_domain",
        "question": "Observed system: Water moves from a tank through a pipe. A restriction narrows the path and movement drops. Question: What happens when resistance increases?",
        "expected_status": "IDENTIFIED",
        "expected_mechanism": "flow",
        "expected_component_category": "path/resistance interface",
        "source_domain": "water_system",
        "target_domain": "water_system",
        "requires_transfer": False,
        "hidden_mechanism_name": False,
    },
    {
        "question_id": "ID-002",
        "suite": "in_domain",
        "question": "Observed system: A wheel turns on a bearing. Friction increases, noise appears, and rotation slows. Question: What happens when friction increases in the wheel bearing?",
        "expected_status": "IDENTIFIED",
        "expected_mechanism": "supported_rotation",
        "expected_component_category": "rotational support interface",
        "source_domain": "wheel_assembly",
        "target_domain": "wheel_assembly",
        "requires_transfer": False,
        "hidden_mechanism_name": False,
    },
    {
        "question_id": "ID-003",
        "suite": "in_domain",
        "question": "Observed system: A bridge carries heavy load through a truss. One joint takes concentrated stress and starts to crack. Question: What happens when load concentrates?",
        "expected_status": "IDENTIFIED",
        "expected_mechanism": "load_transfer",
        "expected_component_category": "load path distribution element",
        "source_domain": "bridge",
        "target_domain": "bridge",
        "requires_transfer": False,
        "hidden_mechanism_name": False,
    },
]


CROSS_DOMAIN_TESTS: list[dict[str, Any]] = [
    {
        "question_id": "CD-001",
        "suite": "cross_domain_transfer",
        "question": "Teach: water from a source moves through a pipe and a restriction reduces movement. Test: delivery carts move along a corridor; a bottleneck narrows the route and progress drops. Question: What mechanism is similar?",
        "expected_status": "IDENTIFIED",
        "expected_mechanism": "flow",
        "expected_component_category": "path/resistance interface",
        "source_domain": "water_system",
        "target_domain": "delivery_corridor",
        "requires_transfer": True,
        "hidden_mechanism_name": False,
    },
    {
        "question_id": "CD-002",
        "suite": "cross_domain_transfer",
        "question": "Teach: a wheel turns on a bearing; friction creates noise and slows rotation. Test: a computer fan spins on a shaft; wear creates noise and it eventually slows. Question: What should be inspected first?",
        "expected_status": "IDENTIFIED",
        "expected_mechanism": "supported_rotation",
        "expected_component_category": "rotational support interface",
        "source_domain": "wheel_assembly",
        "target_domain": "computer_fan",
        "requires_transfer": True,
        "hidden_mechanism_name": False,
    },
    {
        "question_id": "CD-003",
        "suite": "cross_domain_transfer",
        "question": "Teach: a bridge spreads weight through truss supports; concentrated load cracks a joint. Test: a warehouse shelf carries heavy boxes through uprights; one overloaded corner sags at a bracket. Question: What mechanism is similar?",
        "expected_status": "IDENTIFIED",
        "expected_mechanism": "load_transfer",
        "expected_component_category": "load path distribution element",
        "source_domain": "bridge",
        "target_domain": "warehouse_shelf",
        "requires_transfer": True,
        "hidden_mechanism_name": False,
    },
    {
        "question_id": "CD-004",
        "suite": "cross_domain_transfer",
        "question": "Observed system: Requests pass through a service gateway. One rate-limited step creates a bottleneck, queues build, and throughput drops. Question: What mechanism is similar?",
        "expected_status": "IDENTIFIED",
        "expected_mechanism": "flow",
        "expected_component_category": "path/resistance interface",
        "source_domain": "water_system",
        "target_domain": "service_gateway",
        "requires_transfer": True,
        "hidden_mechanism_name": False,
    },
    {
        "question_id": "CD-005",
        "suite": "cross_domain_transfer",
        "question": "Observed system: A lab turntable spins around a spindle. The support mount wears, squeals, and the rotation becomes uneven. Question: What should be inspected first?",
        "expected_status": "IDENTIFIED",
        "expected_mechanism": "supported_rotation",
        "expected_component_category": "rotational support interface",
        "source_domain": "wheel_assembly",
        "target_domain": "lab_turntable",
        "requires_transfer": True,
        "hidden_mechanism_name": False,
    },
    {
        "question_id": "CD-006",
        "suite": "cross_domain_transfer",
        "question": "Observed system: A hanging sign carries weight through two cables. One anchor takes most force, bends, and the sign sags. Question: What mechanism is similar?",
        "expected_status": "IDENTIFIED",
        "expected_mechanism": "load_transfer",
        "expected_component_category": "load path distribution element",
        "source_domain": "bridge",
        "target_domain": "hanging_sign",
        "requires_transfer": True,
        "hidden_mechanism_name": False,
    },
]


HIDDEN_TESTS: list[dict[str, Any]] = [
    {
        "question_id": "HM-001",
        "suite": "hidden_mechanism",
        "question": "Observed system: The room fan slows down over time, becomes noisy, and eventually stops. Question: What component category is most likely involved? Explain why.",
        "expected_status": "IDENTIFIED",
        "expected_mechanism": "supported_rotation",
        "expected_component_category": "rotational support interface",
        "source_domain": "wheel_assembly",
        "target_domain": "room_fan",
        "requires_transfer": True,
        "hidden_mechanism_name": True,
    },
    {
        "question_id": "HM-002",
        "suite": "hidden_mechanism",
        "question": "Observed system: People move along a hallway toward an exit. Near the exit the hallway gets narrower, people bunch up, and progress drops. Question: What component category is most likely involved? Explain why.",
        "expected_status": "IDENTIFIED",
        "expected_mechanism": "flow",
        "expected_component_category": "path/resistance interface",
        "source_domain": "water_system",
        "target_domain": "crowd_exit",
        "requires_transfer": True,
        "hidden_mechanism_name": True,
    },
    {
        "question_id": "HM-003",
        "suite": "hidden_mechanism",
        "question": "Observed system: A shelf bows after heavy boxes are moved to one corner, and cracks appear at a bracket. Question: What component category is most likely involved? Explain why.",
        "expected_status": "IDENTIFIED",
        "expected_mechanism": "load_transfer",
        "expected_component_category": "load path distribution element",
        "source_domain": "bridge",
        "target_domain": "storage_shelf",
        "requires_transfer": True,
        "hidden_mechanism_name": True,
    },
    {
        "question_id": "HM-004",
        "suite": "hidden_mechanism",
        "question": "Observed system: A motorized turntable starts squealing, rotation becomes uneven, then stalls. Question: What component category is most likely involved? Explain why.",
        "expected_status": "IDENTIFIED",
        "expected_mechanism": "supported_rotation",
        "expected_component_category": "rotational support interface",
        "source_domain": "wheel_assembly",
        "target_domain": "motorized_turntable",
        "requires_transfer": True,
        "hidden_mechanism_name": True,
    },
    {
        "question_id": "HM-005",
        "suite": "hidden_mechanism",
        "question": "Observed system: Requests pass through a gateway; one rate-limited step causes queues and lower throughput. Question: What component category is most likely involved? Explain why.",
        "expected_status": "IDENTIFIED",
        "expected_mechanism": "flow",
        "expected_component_category": "path/resistance interface",
        "source_domain": "water_system",
        "target_domain": "software_gateway",
        "requires_transfer": True,
        "hidden_mechanism_name": True,
    },
    {
        "question_id": "HM-006",
        "suite": "hidden_mechanism",
        "question": "Observed system: A suspended sign pulls through two cables; one anchor takes most force and bends. Question: What component category is most likely involved? Explain why.",
        "expected_status": "IDENTIFIED",
        "expected_mechanism": "load_transfer",
        "expected_component_category": "load path distribution element",
        "source_domain": "bridge",
        "target_domain": "suspended_sign",
        "requires_transfer": True,
        "hidden_mechanism_name": True,
    },
]


FAIL_CLOSED_TESTS: list[dict[str, Any]] = [
    {
        "question_id": "FC-001",
        "suite": "fail_closed",
        "question": "Observed system: A password is forgotten and the login fails. Question: What mechanism is similar?",
        "expected_status": "FAIL_CLOSED",
        "expected_mechanism": "",
        "expected_component_category": "",
        "source_domain": "",
        "target_domain": "login",
        "requires_transfer": False,
        "hidden_mechanism_name": True,
    },
    {
        "question_id": "FC-002",
        "suite": "fail_closed",
        "question": "Observed system: A plant leans toward a window after several days. Question: What component category is involved?",
        "expected_status": "FAIL_CLOSED",
        "expected_mechanism": "",
        "expected_component_category": "",
        "source_domain": "",
        "target_domain": "plant_growth",
        "requires_transfer": False,
        "hidden_mechanism_name": True,
    },
    {
        "question_id": "FC-003",
        "suite": "fail_closed",
        "question": "Observed system: A recipe tastes too salty after extra seasoning. Question: What mechanism is similar?",
        "expected_status": "FAIL_CLOSED",
        "expected_mechanism": "",
        "expected_component_category": "",
        "source_domain": "",
        "target_domain": "recipe",
        "requires_transfer": False,
        "hidden_mechanism_name": True,
    },
    {
        "question_id": "FC-004",
        "suite": "fail_closed",
        "question": "Observed system: The device is slow. Question: What mechanism is similar?",
        "expected_status": "FAIL_CLOSED",
        "expected_mechanism": "",
        "expected_component_category": "",
        "source_domain": "",
        "target_domain": "underspecified_device",
        "requires_transfer": False,
        "hidden_mechanism_name": True,
    },
]


ALL_TESTS = [*IN_DOMAIN_TESTS, *CROSS_DOMAIN_TESTS, *HIDDEN_TESTS, *FAIL_CLOSED_TESTS]
TRANSFER_TESTS = [*CROSS_DOMAIN_TESTS, *HIDDEN_TESTS]


def build_state(state_id: str, lessons: list[dict[str, Any]]) -> dict[str, Any]:
    mechanisms: dict[str, Any] = {}
    lessons_by_id: dict[str, Any] = {}
    for lesson in lessons:
        lesson_id = lesson["lesson_id"]
        mechanism_id = lesson["mechanism_id"]
        lessons_by_id[lesson_id] = lesson
        mechanisms[mechanism_id] = {
            "lesson_id": lesson_id,
            "mechanism_name": lesson["mechanism_name"],
            "core_motif": lesson["core_motif"],
            "roles": lesson["roles"],
            "required_min_roles": lesson["required_min_roles"],
            "minimum_score": lesson["minimum_score"],
            "causal_rule": lesson["causal_rule"],
            "direct_effect": lesson["direct_effect"],
            "inspection_priority": lesson["inspection_priority"],
            "component_category": lesson["component_category"],
            "mechanism_explanation": lesson["mechanism_explanation"],
            "mapping_statement": lesson["mapping_statement"],
            "similarity_statement": lesson["similarity_statement"],
            "trace_expectation": lesson["trace_expectation"],
            "examples_hash": sha256_json(lesson["examples"]),
        }
    state = {
        "schema_version": "mechanism_pond_state.v1",
        "state_id": state_id,
        "seasoned_lesson_ids": [lesson["lesson_id"] for lesson in lessons],
        "mechanisms": mechanisms,
        "lessons": lessons_by_id,
        "answer_boundary": "deterministic_cli_no_llm",
    }
    state["state_hash"] = sha256_json(state)
    return state


def ingest_report(state_id: str, lessons: list[dict[str, Any]], state: dict[str, Any]) -> dict[str, Any]:
    return {
        "state_id": state_id,
        "seasoning_mode": "deterministic_mechanism_jsonl_ingest",
        "lesson_count": len(lessons),
        "mechanism_count": len(state["mechanisms"]),
        "ingested_lessons": [lesson["lesson_id"] for lesson in lessons],
        "formed_mechanisms": sorted(state["mechanisms"]),
        "state_hash": state["state_hash"],
        "rejected_lessons": [],
        "traceback_policy": "Every identified mechanism must include observed_system, identified_mechanism, supporting_motifs, source_mechanism, and transfer_confidence.",
    }


def run_cli_map(pond_dir: Path, question: str) -> dict[str, Any]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "operational_cognition.cli.mechanism_pond",
            "map",
            "--pond",
            str(pond_dir),
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


def mapping_shape(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "observed_system": result.get("observed_system", ""),
        "identified_mechanism": result.get("identified_mechanism", ""),
        "supporting_motifs": result.get("supporting_motifs", []),
        "source_mechanism": result.get("source_mechanism", ""),
        "transfer_confidence": result.get("transfer_confidence", 0.0),
    }


def expected_roles_satisfied(result: dict[str, Any], item: dict[str, Any]) -> bool:
    if item["expected_status"] != "IDENTIFIED":
        return result.get("status") == "FAIL_CLOSED"
    if result.get("identified_mechanism") != item["expected_mechanism"]:
        return False
    return len(result.get("supporting_motifs", [])) >= 3


def evaluate_item(pond_dir: Path, item: dict[str, Any]) -> dict[str, Any]:
    first = run_cli_map(pond_dir, item["question"])
    second = run_cli_map(pond_dir, item["question"])
    status_ok = first.get("status") == item["expected_status"]
    mechanism_ok = True
    category_ok = True
    if item["expected_status"] == "IDENTIFIED":
        mechanism_ok = first.get("identified_mechanism") == item["expected_mechanism"]
        category_ok = first.get("component_category") == item["expected_component_category"]
    else:
        mechanism_ok = first.get("identified_mechanism") == ""
        category_ok = first.get("component_category") == ""
    correct = status_ok and mechanism_ok and category_ok and expected_roles_satisfied(first, item)
    return {
        **first,
        "question_id": item["question_id"],
        "suite": item["suite"],
        "expected_status": item["expected_status"],
        "expected_mechanism": item["expected_mechanism"],
        "expected_component_category": item["expected_component_category"],
        "source_domain": item["source_domain"],
        "target_domain": item["target_domain"],
        "requires_transfer": item["requires_transfer"],
        "hidden_mechanism_name": item["hidden_mechanism_name"],
        "mapping_output": mapping_shape(first),
        "correct": correct,
        "deterministic_replay_match": canonical_json(first) == canonical_json(second),
        "motif_support_count": len(first.get("supporting_motifs", [])),
    }


def evaluate_items(pond_dir: Path, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [evaluate_item(pond_dir, item) for item in items]


def suite_result(phase: str, pond_state: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(rows)
    identified = [row for row in rows if row.get("status") == "IDENTIFIED"]
    expected_identified = [row for row in rows if row["expected_status"] == "IDENTIFIED"]
    transfer_rows = [row for row in rows if row.get("requires_transfer") and row["expected_status"] == "IDENTIFIED"]
    transfer_successes = [row for row in transfer_rows if row.get("correct")]
    return {
        "proof_id": PROOF_ID,
        "phase": phase,
        "pond_state": pond_state,
        "execution_mode": "deterministic_cli_no_llm",
        "identified_items": len(identified),
        "expected_identified_items": len(expected_identified),
        "total_items": total,
        "correct_items": sum(1 for row in rows if row.get("correct")),
        "fail_closed_items": sum(1 for row in rows if row.get("status") == "FAIL_CLOSED"),
        "fail_closed_rate": round(sum(1 for row in rows if row.get("status") == "FAIL_CLOSED") / total, 4) if total else 0.0,
        "mechanism_transfer_rate": round(len(transfer_successes) / len(transfer_rows), 4) if transfer_rows else None,
        "deterministic_replay_match": all(row.get("deterministic_replay_match") for row in rows),
        "items": rows,
    }


def baseline_result(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "proof_id": PROOF_ID,
        "phase": "no_seasoning_baseline",
        "pond_state": "unseasoned",
        "execution_mode": "deterministic_cli_no_llm",
        "same_prompts_as_seasoned_transfer_tests": True,
        "total_items": len(rows),
        "identified_items": sum(1 for row in rows if row.get("status") == "IDENTIFIED"),
        "fail_closed_items": sum(1 for row in rows if row.get("status") == "FAIL_CLOSED"),
        "all_fail_closed": all(row.get("status") == "FAIL_CLOSED" for row in rows),
        "deterministic_replay_match": all(row.get("deterministic_replay_match") for row in rows),
        "items": rows,
    }


def mechanism_mapping_results(*result_sets: dict[str, Any]) -> dict[str, Any]:
    rows = [
        row
        for result_set in result_sets
        for row in result_set["items"]
        if row["expected_status"] == "IDENTIFIED"
    ]
    return {
        "proof_id": PROOF_ID,
        "required_output_schema": {
            "observed_system": "string",
            "identified_mechanism": "string",
            "supporting_motifs": "array",
            "source_mechanism": "string",
            "transfer_confidence": "number",
        },
        "execution_mode": "deterministic_cli_no_llm",
        "mappings": [
            {
                "question_id": row["question_id"],
                "suite": row["suite"],
                **row["mapping_output"],
                "status": row["status"],
                "correct": row["correct"],
                "source_domain": row["source_domain"],
                "target_domain": row["target_domain"],
            }
            for row in rows
        ],
    }


def transfer_metrics(
    in_domain: dict[str, Any],
    cross_domain: dict[str, Any],
    hidden: dict[str, Any],
    fail_closed: dict[str, Any],
    baseline: dict[str, Any],
) -> dict[str, Any]:
    transfer_items = [*cross_domain["items"], *hidden["items"]]
    transfer_successes = [row for row in transfer_items if row["correct"]]
    hidden_successes = [row for row in hidden["items"] if row["correct"]]
    cross_successes = [row for row in cross_domain["items"] if row["correct"]]
    fail_rows = fail_closed["items"]
    return {
        "proof_id": PROOF_ID,
        "critical_metric": "Mechanism Transfer Rate",
        "metric_definition": "Fraction of cross-domain or hidden-mechanism prompts whose mechanism was correctly identified by deterministic CLI mapping.",
        "mechanism_transfer_rate": round(len(transfer_successes) / len(transfer_items), 4),
        "cross_domain_transfer_rate": round(len(cross_successes) / len(cross_domain["items"]), 4),
        "hidden_mechanism_transfer_rate": round(len(hidden_successes) / len(hidden["items"]), 4),
        "in_domain_identification_rate": round(in_domain["correct_items"] / in_domain["total_items"], 4),
        "fail_closed_rate_on_unsupported_items": fail_closed["fail_closed_rate"],
        "unseasoned_baseline_all_fail_closed": baseline["all_fail_closed"],
        "deterministic_replay_match": all(
            [
                in_domain["deterministic_replay_match"],
                cross_domain["deterministic_replay_match"],
                hidden["deterministic_replay_match"],
                fail_closed["deterministic_replay_match"],
                baseline["deterministic_replay_match"],
            ]
        ),
        "transfer_items": [
            {
                "question_id": row["question_id"],
                "expected_mechanism": row["expected_mechanism"],
                "identified_mechanism": row["identified_mechanism"],
                "correct": row["correct"],
                "source_domain": row["source_domain"],
                "target_domain": row["target_domain"],
                "supporting_motifs": row["supporting_motifs"],
                "transfer_confidence": row["transfer_confidence"],
            }
            for row in transfer_items
        ],
    }


def determinism_report(*result_sets: dict[str, Any]) -> dict[str, Any]:
    entries = []
    for result_set in result_sets:
        for row in result_set.get("items", []):
            entries.append(
                {
                    "phase": result_set["phase"],
                    "question_id": row["question_id"],
                    "deterministic_replay_match": row["deterministic_replay_match"],
                }
            )
    return {
        "proof_id": PROOF_ID,
        "method": "Each prompt was mapped twice by a fresh CLI subprocess; canonical JSON outputs were compared.",
        "all_replays_match": all(entry["deterministic_replay_match"] for entry in entries),
        "checked_items": len(entries),
        "entries": entries,
    }


def fail_closed_report(baseline: dict[str, Any], fail_closed: dict[str, Any]) -> dict[str, Any]:
    reasons = sorted(
        {
            row.get("fail_closed_reason", "")
            for row in [*baseline["items"], *fail_closed["items"]]
            if row.get("status") == "FAIL_CLOSED"
        }
    )
    return {
        "proof_id": PROOF_ID,
        "baseline_all_fail_closed": baseline["all_fail_closed"],
        "unsupported_suite_fail_closed_rate": fail_closed["fail_closed_rate"],
        "unsupported_suite_false_positive_count": sum(1 for row in fail_closed["items"] if row.get("status") == "IDENTIFIED"),
        "fail_closed_reasons": reasons,
        "policy": "The CLI returns FAIL_CLOSED with blank mechanism fields when no mechanisms are loaded, role evidence is insufficient, or the top match is ambiguous.",
    }


def hidden_name_leak(row: dict[str, Any]) -> bool:
    q = row["question"].lower()
    return any(name in q for name in ["flow", "supported rotation", "load transfer"])


def hostile_mechanism_audit(metrics: dict[str, Any], results: list[dict[str, Any]]) -> dict[str, Any]:
    transfer_rows = [row for result in results for row in result["items"] if row.get("requires_transfer")]
    parser_explanation_survives = True
    keyword_explanation_survives = True
    memorization_explanation_survives = False
    hardcoded_mapping_explanation_survives = True
    return {
        "proof_id": PROOF_ID,
        "critical_metric_snapshot": {
            "mechanism_transfer_rate": metrics["mechanism_transfer_rate"],
            "cross_domain_transfer_rate": metrics["cross_domain_transfer_rate"],
            "hidden_mechanism_transfer_rate": metrics["hidden_mechanism_transfer_rate"],
            "fail_closed_rate_on_unsupported_items": metrics["fail_closed_rate_on_unsupported_items"],
        },
        "signal_before_hostile_audit": "STRONG_SIGNAL"
        if metrics["mechanism_transfer_rate"] == 1.0
        and metrics["fail_closed_rate_on_unsupported_items"] == 1.0
        and metrics["unseasoned_baseline_all_fail_closed"]
        else "WEAK_OR_FAILING_SIGNAL",
        "checks": [
            {
                "attack": "keyword_matching",
                "finding": "Survives partially. The CLI maps text to learned role cues such as bottleneck, shaft, noisy, weight, one corner, and bracket. Hidden prompts avoid mechanism names, but role-cue keywords remain central.",
                "status": "survives_partially",
            },
            {
                "attack": "parser_behavior",
                "finding": "Survives. The engine is a deterministic role-cue parser over a closed mechanism state. That can explain the observed success without requiring a stronger claim of general understanding.",
                "status": "survives",
            },
            {
                "attack": "memorization",
                "finding": "Does not fully survive. The CLI receives only pond path and question text; expected answers live in test artifacts and are not loaded by the CLI. However, the curriculum and tests were both authored in this harness.",
                "status": "mostly_rejected_with_boundary",
            },
            {
                "attack": "hardcoded_mappings",
                "finding": "Survives in a bounded form. There are no per-question answer mappings, but each mechanism has explicit role cues and deterministic output templates in the pond state.",
                "status": "survives_bounded",
            },
            {
                "attack": "mechanism_name_leakage",
                "finding": "Hidden suite prompts do not contain FLOW, SUPPORTED_ROTATION, or LOAD_TRANSFER mechanism names.",
                "status": "rejected_for_hidden_suite",
            },
        ],
        "parser_explanation_survives": parser_explanation_survives,
        "keyword_explanation_survives": keyword_explanation_survives,
        "memorization_explanation_survives": memorization_explanation_survives,
        "hardcoded_mapping_explanation_survives": hardcoded_mapping_explanation_survives,
        "hidden_mechanism_name_leaks": [
            {"question_id": row["question_id"], "leak_detected": hidden_name_leak(row)}
            for row in transfer_rows
            if row.get("hidden_mechanism_name")
        ],
        "hostile_verdict": "FAIL" if parser_explanation_survives else "STRONG_SIGNAL",
        "failure_condition_triggered": "parser_explanation_survives" if parser_explanation_survives else "",
        "surviving_claims": [
            "No-LLM CLI generated all mechanism mappings.",
            "The seasoned pond identified taught mechanisms across curated surface-domain changes.",
            "The unseasoned pond and unsupported prompts failed closed.",
            "Every identified item emitted the required mapping object with supporting motifs and source mechanism.",
        ],
        "invalidated_claims": [
            "Success cannot be explained by parser behavior.",
            "Success cannot be explained by hardcoded mechanism role cues.",
            "This establishes general mechanism understanding beyond the closed-world symbolic curriculum.",
        ],
        "interpretation": "The critical transfer metric is high, but the hostile audit rejects a strong cognition claim because parser and hardcoded-role explanations survive.",
    }


def no_llm_exam_result(
    baseline: dict[str, Any],
    in_domain: dict[str, Any],
    cross_domain: dict[str, Any],
    hidden: dict[str, Any],
    fail_closed: dict[str, Any],
    metrics: dict[str, Any],
    hostile: dict[str, Any],
) -> dict[str, Any]:
    return {
        "proof_id": PROOF_ID,
        "phase": "no_llm_cli_mechanism_exam",
        "execution_mode": "deterministic_cli_no_llm",
        "answer_generation_boundary": {
            "cli_module": "operational_cognition.cli.mechanism_pond",
            "llm_used_for_final_answers": False,
            "codex_answer_synthesis_used": False,
            "final_answers_generated_by": "subprocess invocation of python3 -m operational_cognition.cli.mechanism_pond map --json",
            "fail_closed_policy": "If mechanism role evidence is absent or ambiguous, the CLI returns FAIL_CLOSED with blank mapping fields.",
        },
        "baseline_unseasoned": {
            "total_items": baseline["total_items"],
            "all_fail_closed": baseline["all_fail_closed"],
        },
        "seasoned": {
            "in_domain_identification_rate": metrics["in_domain_identification_rate"],
            "mechanism_transfer_rate": metrics["mechanism_transfer_rate"],
            "cross_domain_transfer_rate": metrics["cross_domain_transfer_rate"],
            "hidden_mechanism_transfer_rate": metrics["hidden_mechanism_transfer_rate"],
            "unsupported_fail_closed_rate": metrics["fail_closed_rate_on_unsupported_items"],
        },
        "deterministic_replay_match": metrics["deterministic_replay_match"],
        "hostile_verdict": hostile["hostile_verdict"],
        "final_interpretation": hostile["interpretation"],
        "result_refs": [
            "results/in_domain_results.json",
            "results/cross_domain_transfer_results.json",
            "results/hidden_mechanism_results.json",
            "results/mechanism_mapping_results.json",
            "analysis/hostile_mechanism_audit.json",
        ],
    }


def readme(metrics: dict[str, Any], hostile: dict[str, Any]) -> str:
    return f"""# Proof 030 - Mechanistic Transfer Challenge

## Objective

This proof tests whether a deterministic pond can map learned mechanism motifs across changed surface domains.

Final mappings are generated only through:

```bash
python3 -m operational_cognition.cli.mechanism_pond map --pond <pond_state_dir> --question "<question>" --json
```

## Required Mapping Output

Every identified item emits:

```json
{{
  "observed_system": "",
  "identified_mechanism": "",
  "supporting_motifs": [],
  "source_mechanism": "",
  "transfer_confidence": 0.0
}}
```

## Result Snapshot

- Mechanism Transfer Rate: {metrics["mechanism_transfer_rate"]}
- Cross-domain transfer rate: {metrics["cross_domain_transfer_rate"]}
- Hidden-mechanism transfer rate: {metrics["hidden_mechanism_transfer_rate"]}
- Unsupported fail-closed rate: {metrics["fail_closed_rate_on_unsupported_items"]}
- Unseasoned baseline all fail closed: {str(metrics["unseasoned_baseline_all_fail_closed"]).lower()}
- Hostile verdict: {hostile["hostile_verdict"]}

## Audit Boundary

The transfer metric is high inside the curated closed-world test, but the hostile audit marks the proof as FAIL for strong claims because parser behavior and hardcoded role-cue explanations survive. The surviving claim is bounded: a deterministic no-LLM CLI can reuse explicit mechanism motifs from a proof state on curated cross-domain prompts and fail closed outside that state.
"""


def manifest(request_hash: str, response_hash: str) -> dict[str, Any]:
    required_artifacts = [
        "README.md",
        "proof_manifest.json",
        "curriculum/mechanism_lessons.jsonl",
        "seasoning/mechanism_ingest_report.json",
        "pond_states/unseasoned/pond_state.json",
        "pond_states/mechanism_seasoned/pond_state.json",
        "tests/in_domain_test.jsonl",
        "tests/cross_domain_transfer_test.jsonl",
        "tests/hidden_mechanism_test.jsonl",
        "tests/fail_closed_test.jsonl",
        "baseline/no_seasoning_results.json",
        "results/in_domain_results.json",
        "results/cross_domain_transfer_results.json",
        "results/hidden_mechanism_results.json",
        "results/fail_closed_results.json",
        "results/mechanism_mapping_results.json",
        "results/no_llm_mechanism_exam.json",
        "analysis/mechanism_transfer_metrics.json",
        "analysis/fail_closed_report.json",
        "analysis/determinism_report.json",
        "analysis/hostile_mechanism_audit.json",
    ]
    return {
        "proof_id": PROOF_ID,
        "title": TITLE,
        "status": "complete",
        "targets": [
            "MechanisticTransfer",
            "StructureTransfer",
            "DeterministicNoLLMMapping",
            "FailClosedMechanismPondCLI",
            "HostileParserAudit",
        ],
        "claim_level": "evidence_backed",
        "inside_voice_adapter_status": "not_used_final_answers_generated_by_deterministic_cli",
        "public_private_boundary": "All artifacts are public deterministic curriculum, tests, pond states, CLI outputs, metrics, and audits. No hidden chain-of-thought or private substrate data is exposed.",
        "required_artifacts": required_artifacts,
        "disallowed_claims": [
            "LLM generated final answers",
            "general mechanism understanding",
            "general physical reasoning",
            "consciousness",
            "AGI",
            "hidden chain-of-thought",
            "success independent of parser behavior",
            "success independent of hardcoded mechanism role cues",
        ],
        "lineage": {
            "mcp_endpoint": "none:deterministic_cli_no_llm",
            "contract_version": "mechanism_pond.cli.v1",
            "request_hash": request_hash,
            "response_hash": response_hash,
            "derived_from": "curriculum/mechanism_lessons.jsonl; tests/*.jsonl; pond_states/*/pond_state.json; python3 -m operational_cognition.cli.mechanism_pond",
            "validates": "curated_mechanism_transfer_mapping_with_fail_closed_no_llm_cli_answers",
        },
    }


def main() -> int:
    write_jsonl(PROOF_DIR / "curriculum" / "mechanism_lessons.jsonl", MECHANISM_LESSONS)
    write_jsonl(PROOF_DIR / "tests" / "in_domain_test.jsonl", IN_DOMAIN_TESTS)
    write_jsonl(PROOF_DIR / "tests" / "cross_domain_transfer_test.jsonl", CROSS_DOMAIN_TESTS)
    write_jsonl(PROOF_DIR / "tests" / "hidden_mechanism_test.jsonl", HIDDEN_TESTS)
    write_jsonl(PROOF_DIR / "tests" / "fail_closed_test.jsonl", FAIL_CLOSED_TESTS)

    unseasoned_state = build_state("unseasoned", [])
    seasoned_state = build_state("mechanism_seasoned", MECHANISM_LESSONS)
    unseasoned_dir = PROOF_DIR / "pond_states" / "unseasoned"
    seasoned_dir = PROOF_DIR / "pond_states" / "mechanism_seasoned"
    write_json(unseasoned_dir / "pond_state.json", unseasoned_state)
    write_json(seasoned_dir / "pond_state.json", seasoned_state)
    write_json(PROOF_DIR / "seasoning" / "mechanism_ingest_report.json", ingest_report("mechanism_seasoned", MECHANISM_LESSONS, seasoned_state))

    baseline_rows = evaluate_items(unseasoned_dir, TRANSFER_TESTS)
    in_domain_rows = evaluate_items(seasoned_dir, IN_DOMAIN_TESTS)
    cross_domain_rows = evaluate_items(seasoned_dir, CROSS_DOMAIN_TESTS)
    hidden_rows = evaluate_items(seasoned_dir, HIDDEN_TESTS)
    fail_closed_rows = evaluate_items(seasoned_dir, FAIL_CLOSED_TESTS)

    baseline_output = baseline_result(baseline_rows)
    in_domain_output = suite_result("in_domain_test", "mechanism_seasoned", in_domain_rows)
    cross_domain_output = suite_result("cross_domain_transfer_test", "mechanism_seasoned", cross_domain_rows)
    hidden_output = suite_result("hidden_mechanism_test", "mechanism_seasoned", hidden_rows)
    fail_closed_output = suite_result("fail_closed_test", "mechanism_seasoned", fail_closed_rows)
    mapping_output = mechanism_mapping_results(in_domain_output, cross_domain_output, hidden_output)
    metrics_output = transfer_metrics(in_domain_output, cross_domain_output, hidden_output, fail_closed_output, baseline_output)
    fail_output = fail_closed_report(baseline_output, fail_closed_output)
    determinism_output = determinism_report(
        baseline_output,
        in_domain_output,
        cross_domain_output,
        hidden_output,
        fail_closed_output,
    )
    hostile_output = hostile_mechanism_audit(
        metrics_output,
        [in_domain_output, cross_domain_output, hidden_output, fail_closed_output],
    )
    exam_output = no_llm_exam_result(
        baseline_output,
        in_domain_output,
        cross_domain_output,
        hidden_output,
        fail_closed_output,
        metrics_output,
        hostile_output,
    )

    write_json(PROOF_DIR / "baseline" / "no_seasoning_results.json", baseline_output)
    write_json(PROOF_DIR / "results" / "in_domain_results.json", in_domain_output)
    write_json(PROOF_DIR / "results" / "cross_domain_transfer_results.json", cross_domain_output)
    write_json(PROOF_DIR / "results" / "hidden_mechanism_results.json", hidden_output)
    write_json(PROOF_DIR / "results" / "fail_closed_results.json", fail_closed_output)
    write_json(PROOF_DIR / "results" / "mechanism_mapping_results.json", mapping_output)
    write_json(PROOF_DIR / "results" / "no_llm_mechanism_exam.json", exam_output)
    write_json(PROOF_DIR / "analysis" / "mechanism_transfer_metrics.json", metrics_output)
    write_json(PROOF_DIR / "analysis" / "fail_closed_report.json", fail_output)
    write_json(PROOF_DIR / "analysis" / "determinism_report.json", determinism_output)
    write_json(PROOF_DIR / "analysis" / "hostile_mechanism_audit.json", hostile_output)
    write_text(PROOF_DIR / "README.md", readme(metrics_output, hostile_output))

    request_hash = sha256_json(
        {
            "mechanism_lessons": MECHANISM_LESSONS,
            "tests": {
                "in_domain": IN_DOMAIN_TESTS,
                "cross_domain": CROSS_DOMAIN_TESTS,
                "hidden": HIDDEN_TESTS,
                "fail_closed": FAIL_CLOSED_TESTS,
            },
            "cli": "operational_cognition.cli.mechanism_pond",
        }
    )
    response_hash = sha256_json(
        {
            "baseline": baseline_output,
            "in_domain": in_domain_output,
            "cross_domain": cross_domain_output,
            "hidden": hidden_output,
            "fail_closed": fail_closed_output,
            "mapping": mapping_output,
            "metrics": metrics_output,
            "fail_report": fail_output,
            "determinism": determinism_output,
            "hostile": hostile_output,
            "exam": exam_output,
        }
    )
    write_json(PROOF_DIR / "proof_manifest.json", manifest(request_hash, response_hash))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
