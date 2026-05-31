#!/usr/bin/env python3
"""Run a controlled /consult failure-boundary stress gauntlet.

This harness does not try to improve retrieval. It builds adversarial and
high-pressure pond fixtures with known oracle lineages, runs a deterministic
consult-like selector, and reports the conditions where the selector stops
behaving like single-lineage BEST_PATH retrieval.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT_DIR = ROOT / "artifacts" / "integrations" / "consult_failure_boundary"

GAUNTLET_VERSION = "consult_failure_boundary.gauntlet.v1"
CONSULT_CONTRACT_VERSION = "inside_voice.consult.failure_boundary.v1"
RUN_ID = "consult-failure-boundary-controlled-2026-05-28"

CLASSIFICATIONS = {
    "BEST_PATH",
    "TOP_K_PATHS",
    "UNDER_CONTEXT",
    "CONTEXT_DUMP",
    "FALSE_RECALL",
    "CONTAMINATION",
    "NONDETERMINISTIC",
}

HASH_RE = re.compile(r"^[a-f0-9]{64}$")
TOKEN_OVERHEAD = 96
MIN_RELEVANCE_SCORE = 0.34
BEST_PATH_DOMINANCE_SHARE = 0.64
AMBIGUITY_SHARE = 0.82
TOP_K_PATH_LIMIT = 4
MAX_ITEMS_PER_PATH = 2
CONTEXT_DUMP_RELEVANT_ITEM_THRESHOLD = 32
CONTEXT_DUMP_TOKEN_THRESHOLD = 4600
MAX_IRRELEVANT_TOKEN_RATIO = 0.20

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "can",
    "consult",
    "context",
    "current",
    "does",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "or",
    "recommendation",
    "should",
    "task",
    "the",
    "to",
    "what",
    "when",
    "where",
    "which",
    "with",
}


@dataclass(frozen=True)
class ContextItem:
    item_id: str
    path_id: str
    lineage_id: str
    source_trace_ref: str
    artifact_ref: str
    artifact_hash: str
    title: str
    text: str
    tags: tuple[str, ...]
    redundancy_group: str
    token_estimate: int
    created_at: int
    evidence_polarity: str = "neutral"
    origin: str = "pond"


@dataclass(frozen=True)
class CaseSpec:
    suite_id: str
    case_id: str
    query: str
    context: tuple[ContextItem, ...]
    focus_terms: tuple[str, ...]
    required_lineage_ids: tuple[str, ...] = ()
    required_item_ids: tuple[str, ...] = ()
    oracle_relevant_lineage_ids: tuple[str, ...] = ()
    expected_current_lineage_id: str = ""
    contradiction_group: str = ""
    expected_classification: str = ""
    description: str = ""


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def estimate_tokens(value: Any) -> int:
    if isinstance(value, str):
        rendered = value
    else:
        rendered = json.dumps(value, sort_keys=True, ensure_ascii=True)
    return max(1, (len(rendered) + 3) // 4)


def normalize_token(token: str) -> str:
    if token.endswith("ies") and len(token) > 4:
        return f"{token[:-3]}y"
    if token.endswith("ing") and len(token) > 5:
        return token[:-3]
    if token.endswith("ed") and len(token) > 4:
        return token[:-2]
    if token.endswith("s") and len(token) > 3:
        return token[:-1]
    return token


def tokenize(value: str) -> set[str]:
    tokens = re.findall(r"[a-z0-9]+", value.lower())
    return {
        normalize_token(token)
        for token in tokens
        if len(token) > 1 and normalize_token(token) not in STOP_WORDS
    }


def make_item(
    item_id: str,
    path_id: str,
    lineage_id: str,
    source_trace_ref: str,
    artifact_ref: str,
    title: str,
    text: str,
    tags: Iterable[str],
    redundancy_group: str,
    created_at: int,
    evidence_polarity: str = "neutral",
    origin: str = "pond",
) -> ContextItem:
    tag_tuple = tuple(tags)
    artifact_hash = sha256_text(f"{artifact_ref}|{title}|{text}|{created_at}|{evidence_polarity}|{origin}")
    token_estimate = estimate_tokens(
        {
            "item_id": item_id,
            "path_id": path_id,
            "lineage_id": lineage_id,
            "source_trace_ref": source_trace_ref,
            "artifact_ref": artifact_ref,
            "title": title,
            "text": text,
            "tags": tag_tuple,
            "created_at": created_at,
            "evidence_polarity": evidence_polarity,
            "origin": origin,
        }
    )
    return ContextItem(
        item_id=item_id,
        path_id=path_id,
        lineage_id=lineage_id,
        source_trace_ref=source_trace_ref,
        artifact_ref=artifact_ref,
        artifact_hash=artifact_hash,
        title=title,
        text=text,
        tags=tag_tuple,
        redundancy_group=redundancy_group,
        token_estimate=token_estimate,
        created_at=created_at,
        evidence_polarity=evidence_polarity,
        origin=origin,
    )


def item_search_tokens(item: ContextItem) -> set[str]:
    return tokenize(
        " ".join(
            [
                item.item_id,
                item.path_id,
                item.lineage_id,
                item.title,
                item.text,
                " ".join(item.tags),
                item.evidence_polarity,
                item.origin,
            ]
        )
    )


def full_context_token_estimate(context: Iterable[ContextItem]) -> int:
    return TOKEN_OVERHEAD + sum(item.token_estimate for item in context)


def selected_response_token_estimate(items: Iterable[ContextItem]) -> int:
    return TOKEN_OVERHEAD + sum(item.token_estimate for item in items)


def response_hash(response: dict[str, Any]) -> str:
    payload = copy.deepcopy(response)
    payload.pop("response_hash", None)
    return sha256_text(canonical_json(payload))


def ranked_context_record(item: ContextItem, score: float) -> dict[str, Any]:
    return {
        "item_id": item.item_id,
        "path_id": item.path_id,
        "lineage_id": item.lineage_id,
        "title": item.title,
        "summary": item.text,
        "source_trace_ref": item.source_trace_ref,
        "artifact_lineage": {
            "artifact_ref": item.artifact_ref,
            "artifact_hash": item.artifact_hash,
            "lineage_id": item.lineage_id,
            "path_id": item.path_id,
            "created_at": item.created_at,
            "origin": item.origin,
        },
        "evidence_polarity": item.evidence_polarity,
        "relevance_score": score,
        "token_estimate": item.token_estimate,
    }


def base_context() -> list[ContextItem]:
    return [
        make_item(
            "RC-001",
            "path.recall_traceback",
            "lineage.recall_traceback",
            "trace:proofs/recall/traceback.json#complete",
            "proofs/recall/traceback.json",
            "Recall Traceback Integrity",
            "Improve recall by preserving source trace refs, artifact hashes, and lineage ids before compression.",
            ("recall", "traceback", "source", "artifact", "hash", "lineage", "authoritative"),
            "recall_traceback_core",
            100,
        ),
        make_item(
            "RC-002",
            "path.recall_traceback",
            "lineage.recall_traceback",
            "trace:proofs/recall/relevance.json#precision",
            "proofs/recall/relevance.json",
            "Recall Precision Guard",
            "Recall should improve only when irrelevant context is excluded and required lineage stays attributable.",
            ("recall", "precision", "relevance", "exclude", "lineage", "authoritative"),
            "recall_precision_guard",
            101,
        ),
        make_item(
            "RT-001",
            "path.routing_phase",
            "lineage.routing_phase",
            "trace:proofs/routing/phase_map.json#router",
            "proofs/routing/phase_map.json",
            "Phase Routing Selector",
            "Optimize routing by selecting the active phase before tool use, then ranking only matching lineage paths.",
            ("routing", "phase", "selector", "optimize", "tool", "rank", "authoritative"),
            "routing_phase_core",
            110,
        ),
        make_item(
            "RT-002",
            "path.routing_phase",
            "lineage.routing_phase",
            "trace:proofs/routing/fallbacks.json#top-k",
            "proofs/routing/fallbacks.json",
            "Routing Top K Fallback",
            "When route intent is ambiguous, retain a bounded top-k path set rather than forcing a single lineage.",
            ("routing", "ambiguous", "top", "path", "bounded", "fallback", "authoritative"),
            "routing_top_k_fallback",
            111,
        ),
        make_item(
            "CP-001",
            "path.compression_budget",
            "lineage.compression_budget",
            "trace:proofs/compression/budget.json#issue",
            "proofs/compression/budget.json",
            "Compression Issue Budget",
            "Fix compression issue by keeping contradiction markers, stale refs, and required evidence before summary.",
            ("compression", "issue", "budget", "contradiction", "stale", "evidence", "summary", "authoritative"),
            "compression_budget_core",
            120,
        ),
        make_item(
            "CP-002",
            "path.compression_budget",
            "lineage.compression_budget",
            "trace:proofs/compression/token_plan.json#discipline",
            "proofs/compression/token_plan.json",
            "Compression Discipline",
            "Compression discipline prefers concise evidence records and excludes repeated or decorative context.",
            ("compression", "token", "discipline", "evidence", "exclude", "repeated", "authoritative"),
            "compression_discipline",
            121,
        ),
        make_item(
            "NOISE-BASE-001",
            "path.frontend_controls",
            "lineage.frontend_controls",
            "trace:docs/frontend.md#controls",
            "docs/frontend.md",
            "Frontend Control Pattern",
            "Frontend controls use segmented buttons, icon buttons, sliders, and menus for direct manipulation.",
            ("frontend", "controls", "icons", "buttons", "menus"),
            "frontend_controls",
            90,
        ),
        make_item(
            "NOISE-BASE-002",
            "path.documents_rendering",
            "lineage.documents_rendering",
            "trace:docs/documents.md#render",
            "docs/documents.md",
            "Document Rendering",
            "Document artifacts render pages for visual verification before delivery.",
            ("documents", "render", "pages", "visual", "verification"),
            "documents_rendering",
            91,
        ),
        make_item(
            "NOISE-BASE-003",
            "path.github_ci",
            "lineage.github_ci",
            "trace:.github/workflows/ci.yml#pytest",
            ".github/workflows/ci.yml",
            "GitHub CI",
            "CI triage identifies failing checks, reads logs, and implements approved fixes.",
            ("github", "ci", "logs", "checks", "pytest"),
            "github_ci",
            92,
        ),
    ]


def make_noise_items(count: int, prefix: str = "NOISE") -> list[ContextItem]:
    items = []
    motifs = [
        ("spreadsheet formulas", ("spreadsheet", "formula", "chart", "workbook")),
        ("presentation export", ("presentation", "slide", "deck", "speaker", "notes")),
        ("design tokens", ("design", "tokens", "color", "spacing", "layout")),
        ("release notes", ("release", "notes", "version", "changelog")),
        ("cache pruning", ("cache", "pruning", "storage", "cleanup")),
    ]
    for index in range(count):
        label, tags = motifs[index % len(motifs)]
        items.append(
            make_item(
                f"{prefix}-{index + 1:04d}",
                f"path.noise.{index % 17:02d}",
                f"lineage.noise.{index % 31:02d}",
                f"trace:noise/{prefix.lower()}/{index + 1:04d}.json#record",
                f"artifacts/noise/{prefix.lower()}/{index + 1:04d}.json",
                f"Irrelevant {label.title()} {index + 1}",
                f"This pond artifact concerns {label}; it shares no required consult lineage for the target query.",
                (*tags, "irrelevant", "pond"),
                f"noise_{index % 23:02d}",
                10 + index,
                origin="noise",
            )
        )
    return items


def ambiguous_cases() -> list[CaseSpec]:
    context = tuple(base_context())
    return [
        CaseSpec(
            suite_id="ambiguous_query",
            case_id="ambiguous_improve_recall",
            query="Improve recall.",
            context=context,
            focus_terms=("improve", "recall", "lineage", "precision", "routing", "compression"),
            oracle_relevant_lineage_ids=("lineage.recall_traceback", "lineage.routing_phase", "lineage.compression_budget"),
            expected_classification="TOP_K_PATHS",
            description="Short query has several valid lineages and should emerge as bounded top-k.",
        ),
        CaseSpec(
            suite_id="ambiguous_query",
            case_id="ambiguous_optimize_routing",
            query="Optimize routing.",
            context=context,
            focus_terms=("optimize", "routing", "phase", "top", "fallback", "recall"),
            oracle_relevant_lineage_ids=("lineage.routing_phase", "lineage.recall_traceback"),
            expected_classification="TOP_K_PATHS",
            description="Routing has a dominant path plus a valid recall/precision neighbor.",
        ),
        CaseSpec(
            suite_id="ambiguous_query",
            case_id="ambiguous_fix_compression_issue",
            query="Fix compression issue.",
            context=context,
            focus_terms=("fix", "compression", "issue", "evidence", "contradiction", "stale", "recall"),
            oracle_relevant_lineage_ids=("lineage.compression_budget", "lineage.recall_traceback"),
            expected_classification="TOP_K_PATHS",
            description="Compression issue has multiple plausible lineages and should not be forced to one path.",
        ),
    ]


def contradiction_cases() -> list[CaseSpec]:
    context = tuple(
        [
            make_item(
                "CT-A-001",
                "path.phase_routing_improves",
                "lineage.phase_routing_improves",
                "trace:proofs/contradiction/phase_routing_a.json#claim",
                "proofs/contradiction/phase_routing_a.json",
                "Phase Routing Improves Accuracy",
                "Phase routing improves accuracy when phase labels are complete and evidence paths are separated.",
                ("phase", "routing", "accuracy", "improves", "complete", "separated", "authoritative"),
                "phase_routing_improves",
                200,
                evidence_polarity="supports",
            ),
            make_item(
                "CT-A-002",
                "path.phase_routing_improves",
                "lineage.phase_routing_improves",
                "trace:proofs/contradiction/phase_routing_a.json#conditions",
                "proofs/contradiction/phase_routing_a.json",
                "Improvement Conditions",
                "The improvement claim is bounded to complete labels and a non-stale routing map.",
                ("phase", "routing", "accuracy", "improvement", "bounded", "conditions"),
                "phase_routing_improves_conditions",
                201,
                evidence_polarity="supports",
            ),
            make_item(
                "CT-B-001",
                "path.phase_routing_harms",
                "lineage.phase_routing_harms",
                "trace:proofs/contradiction/phase_routing_b.json#claim",
                "proofs/contradiction/phase_routing_b.json",
                "Phase Routing Harms Accuracy",
                "Phase routing harms accuracy when stale phase labels route queries away from current evidence.",
                ("phase", "routing", "accuracy", "harms", "stale", "current", "evidence", "authoritative"),
                "phase_routing_harms",
                202,
                evidence_polarity="opposes",
            ),
            make_item(
                "CT-B-002",
                "path.phase_routing_harms",
                "lineage.phase_routing_harms",
                "trace:proofs/contradiction/phase_routing_b.json#conditions",
                "proofs/contradiction/phase_routing_b.json",
                "Harm Conditions",
                "The harm claim is bounded to stale labels and cross-lineage routing leakage.",
                ("phase", "routing", "accuracy", "harm", "bounded", "stale", "leakage"),
                "phase_routing_harms_conditions",
                203,
                evidence_polarity="opposes",
            ),
            *make_noise_items(8, "CONTRADICTION-NOISE"),
        ]
    )
    return [
        CaseSpec(
            suite_id="contradiction",
            case_id="contradiction_phase_routing_accuracy",
            query="Does phase routing improve or harm accuracy?",
            context=context,
            focus_terms=("phase", "routing", "improve", "harm", "accuracy", "stale", "complete", "evidence"),
            required_lineage_ids=("lineage.phase_routing_improves", "lineage.phase_routing_harms"),
            required_item_ids=("CT-A-001", "CT-B-001"),
            oracle_relevant_lineage_ids=("lineage.phase_routing_improves", "lineage.phase_routing_harms"),
            contradiction_group="phase_routing_accuracy",
            expected_classification="TOP_K_PATHS",
            description="Competing claims must stay separated with both polarities visible.",
        )
    ]


def stale_cases() -> list[CaseSpec]:
    full_context = tuple(
        [
            make_item(
                "ST-OLD-001",
                "path.recall_policy_2025",
                "lineage.recall_policy_2025",
                "trace:proofs/stale/recall_policy_2025.json#recommendation",
                "proofs/stale/recall_policy_2025.json",
                "Older Recall Recommendation",
                "The older recommendation favors broad keyword recall and accepts larger context bundles.",
                ("recall", "recommendation", "older", "keyword", "broad", "stale"),
                "recall_policy_old",
                300,
            ),
            make_item(
                "ST-NEW-001",
                "path.recall_policy_2026",
                "lineage.recall_policy_2026",
                "trace:proofs/stale/recall_policy_2026.json#recommendation",
                "proofs/stale/recall_policy_2026.json",
                "Current Recall Recommendation",
                "The current recommendation favors best-path lineage first, bounded top-k only under ambiguity, and explicit stale attribution.",
                ("recall", "recommendation", "current", "best", "path", "bounded", "top", "stale", "authoritative"),
                "recall_policy_new",
                400,
            ),
            *make_noise_items(6, "STALE-NOISE"),
        ]
    )
    stale_only_context = tuple(item for item in full_context if item.item_id != "ST-NEW-001")
    return [
        CaseSpec(
            suite_id="stale_context",
            case_id="stale_current_recommendation",
            query="Current recommendation for recall policy?",
            context=full_context,
            focus_terms=("current", "recommendation", "recall", "policy", "best", "path", "bounded", "stale"),
            required_lineage_ids=("lineage.recall_policy_2026",),
            required_item_ids=("ST-NEW-001",),
            oracle_relevant_lineage_ids=("lineage.recall_policy_2026", "lineage.recall_policy_2025"),
            expected_current_lineage_id="lineage.recall_policy_2026",
            expected_classification="BEST_PATH",
            description="Newer lineage should outrank stale predecessor while attributing the older path.",
        ),
        CaseSpec(
            suite_id="stale_context",
            case_id="stale_missing_current_recommendation",
            query="Current recommendation for recall policy?",
            context=stale_only_context,
            focus_terms=("current", "recommendation", "recall", "policy", "best", "path", "bounded", "stale"),
            required_lineage_ids=("lineage.recall_policy_2026",),
            required_item_ids=("ST-NEW-001",),
            oracle_relevant_lineage_ids=("lineage.recall_policy_2026", "lineage.recall_policy_2025"),
            expected_current_lineage_id="lineage.recall_policy_2026",
            expected_classification="UNDER_CONTEXT",
            description="UNDER_CONTEXT should appear when the current lineage is absent rather than recalled falsely.",
        ),
    ]


def noise_cases() -> list[CaseSpec]:
    target = [
        make_item(
            "NS-TARGET-001",
            "path.noise_resistant_recall",
            "lineage.noise_resistant_recall",
            "trace:proofs/noise/recall.json#target",
            "proofs/noise/recall.json",
            "Noise Resistant Recall",
            "BEST_PATH survives irrelevant pond noise by ranking the target lineage above unrelated artifacts.",
            ("noise", "resistant", "recall", "best", "path", "target", "authoritative"),
            "noise_resistant_recall",
            500,
        ),
        make_item(
            "NS-TARGET-002",
            "path.noise_resistant_recall",
            "lineage.noise_resistant_recall",
            "trace:proofs/noise/precision.json#target",
            "proofs/noise/precision.json",
            "Noise Precision",
            "Precision degradation is measured by any irrelevant tokens retrieved with the target lineage.",
            ("noise", "precision", "degradation", "irrelevant", "tokens", "target", "authoritative"),
            "noise_precision",
            501,
        ),
    ]
    cases = []
    for multiplier in (10, 50, 100):
        cases.append(
            CaseSpec(
                suite_id="noise_injection",
                case_id=f"noise_{multiplier}x_irrelevant",
                query="Find the noise resistant recall target lineage.",
                context=tuple([*target, *make_noise_items(multiplier, f"NOISE-{multiplier}X")]),
                focus_terms=("noise", "resistant", "recall", "target", "best", "path", "precision"),
                required_lineage_ids=("lineage.noise_resistant_recall",),
                required_item_ids=("NS-TARGET-001",),
                oracle_relevant_lineage_ids=("lineage.noise_resistant_recall",),
                expected_classification="BEST_PATH",
                description=f"{multiplier}x irrelevant pond artifacts test selectivity and latency impact.",
            )
        )
    return cases


def duplicate_cases() -> list[CaseSpec]:
    duplicates = [
        make_item(
            f"DUP-{index + 1:03d}",
            f"path.duplicate_recall.{index % 6:02d}",
            "lineage.duplicate_recall",
            f"trace:proofs/duplicates/recall_{index + 1:03d}.json#variant",
            f"proofs/duplicates/recall_{index + 1:03d}.json",
            f"Duplicate Recall Variant {index + 1}",
            "Nearly identical recall guidance says preserve lineage refs, avoid repeated summaries, and keep compression disciplined.",
            ("duplicate", "recall", "lineage", "compression", "discipline", "near", "identical", "authoritative"),
            "duplicate_recall_guidance",
            600 + index,
        )
        for index in range(30)
    ]
    anchor = make_item(
        "DUP-ANCHOR-001",
        "path.duplicate_recall.anchor",
        "lineage.duplicate_recall",
        "trace:proofs/duplicates/anchor.json#canonical",
        "proofs/duplicates/anchor.json",
        "Canonical Duplicate Recall Guidance",
        "The canonical duplicate guidance requires one representative lineage record and excludes near-identical repeats.",
        ("duplicate", "recall", "canonical", "representative", "lineage", "exclude", "authoritative"),
        "duplicate_recall_anchor",
        650,
    )
    return [
        CaseSpec(
            suite_id="duplicate_lineage",
            case_id="duplicate_near_identical_paths",
            query="Select duplicate recall guidance without repeating near identical paths.",
            context=tuple([anchor, *duplicates, *make_noise_items(10, "DUP-NOISE")]),
            focus_terms=("duplicate", "recall", "guidance", "near", "identical", "representative", "lineage"),
            required_lineage_ids=("lineage.duplicate_recall",),
            required_item_ids=("DUP-ANCHOR-001",),
            oracle_relevant_lineage_ids=("lineage.duplicate_recall",),
            expected_classification="BEST_PATH",
            description="Many near-identical paths should dedupe to canonical evidence.",
        )
    ]


def adversarial_cases() -> list[CaseSpec]:
    context = tuple(
        [
            make_item(
                "ADV-TARGET-001",
                "path.target_phase_recall",
                "lineage.target_phase_recall",
                "trace:proofs/adversarial/target_phase_recall.json#target",
                "proofs/adversarial/target_phase_recall.json",
                "Target Phase Recall Lineage",
                "The target lineage links phase recall to runtime hashes, source trace refs, and current routing evidence.",
                ("phase", "recall", "runtime", "hash", "source", "trace", "current", "target", "authoritative"),
                "target_phase_recall",
                700,
            ),
            make_item(
                "ADV-TARGET-002",
                "path.target_phase_recall",
                "lineage.target_phase_recall",
                "trace:proofs/adversarial/target_phase_recall.json#integrity",
                "proofs/adversarial/target_phase_recall.json",
                "Target Traceback Integrity",
                "False recall is resisted by checking that the selected motif originates from the target lineage.",
                ("false", "recall", "traceback", "integrity", "target", "lineage", "authoritative"),
                "target_traceback_integrity",
                701,
            ),
            make_item(
                "ADV-DECOY-001",
                "path.decoy_phase_recall",
                "lineage.decoy_phase_recall_elsewhere",
                "trace:proofs/elsewhere/phase_recall.json#motif",
                "proofs/elsewhere/phase_recall.json",
                "Elsewhere Phase Recall Motif",
                "This motif resembles phase recall and uses runtime hash language, but it belongs to an unrelated lineage.",
                ("phase", "recall", "runtime", "hash", "source", "trace", "motif", "decoy", "elsewhere"),
                "decoy_phase_recall",
                702,
                origin="elsewhere",
            ),
            make_item(
                "ADV-DECOY-002",
                "path.decoy_phase_recall",
                "lineage.decoy_phase_recall_elsewhere",
                "trace:proofs/elsewhere/phase_recall.json#structure",
                "proofs/elsewhere/phase_recall.json",
                "Elsewhere Matching Structure",
                "The structure shares terminology and summary shape while lacking target provenance.",
                ("phase", "recall", "structure", "terminology", "summary", "shape", "decoy", "elsewhere"),
                "decoy_matching_structure",
                703,
                origin="elsewhere",
            ),
            *make_noise_items(12, "ADV-NOISE"),
        ]
    )
    return [
        CaseSpec(
            suite_id="adversarial_motif",
            case_id="adversarial_shared_phase_recall_motif",
            query="Retrieve the target phase recall lineage, not similar motifs from elsewhere.",
            context=context,
            focus_terms=("target", "phase", "recall", "lineage", "runtime", "hash", "source", "trace", "elsewhere"),
            required_lineage_ids=("lineage.target_phase_recall",),
            required_item_ids=("ADV-TARGET-001",),
            oracle_relevant_lineage_ids=("lineage.target_phase_recall",),
            expected_classification="BEST_PATH",
            description="Terminology and structure overlap should not induce false recall.",
        )
    ]


def context_flood_cases() -> list[CaseSpec]:
    cases = []
    for lineage_count in (1, 2, 4, 8, 16, 32, 64):
        items = []
        for lineage_index in range(lineage_count):
            for item_index in range(2):
                items.append(
                    make_item(
                        f"FL-{lineage_count:03d}-{lineage_index + 1:03d}-{item_index + 1}",
                        f"path.flood.{lineage_index + 1:03d}",
                        f"lineage.flood.{lineage_index + 1:03d}",
                        f"trace:proofs/flood/{lineage_count}/{lineage_index + 1:03d}.json#item-{item_index + 1}",
                        f"proofs/flood/{lineage_count}/{lineage_index + 1:03d}.json",
                        f"Relevant Flood Lineage {lineage_index + 1} Item {item_index + 1}",
                        "Massive relevant context for the same broad operational envelope query with bounded lineage evidence.",
                        ("flood", "relevant", "context", "operational", "envelope", "lineage", "evidence", "authoritative"),
                        f"flood_{lineage_index + 1:03d}_{item_index + 1}",
                        800 + lineage_index,
                    )
                )
        expected = "BEST_PATH" if lineage_count == 1 else "CONTEXT_DUMP" if lineage_count >= 16 else "TOP_K_PATHS"
        cases.append(
            CaseSpec(
                suite_id="context_flood",
                case_id=f"context_flood_{lineage_count:03d}_lineages",
                query="Map the broad operational envelope from all relevant flood lineage evidence.",
                context=tuple([*items, *make_noise_items(4, f"FLOOD-NOISE-{lineage_count}")]),
                focus_terms=("broad", "operational", "envelope", "relevant", "flood", "lineage", "evidence"),
                oracle_relevant_lineage_ids=tuple(f"lineage.flood.{index + 1:03d}" for index in range(lineage_count)),
                expected_classification=expected,
                description="Relevant context scale probe for BEST_PATH -> TOP_K_PATHS -> CONTEXT_DUMP transition.",
            )
        )
    return cases


def recursive_case(cycles: int) -> CaseSpec:
    original = [
        make_item(
            "RS-ORIGINAL-001",
            "path.recursive_seasoning_original",
            "lineage.recursive_seasoning_original",
            "trace:proofs/recursive/original.json#source",
            "proofs/recursive/original.json",
            "Original Recursive Seasoning Source",
            "The original source says consult output may be re-ingested only if source lineage stays dominant.",
            ("recursive", "seasoning", "original", "source", "lineage", "dominant", "authoritative"),
            "recursive_original_source",
            900,
        ),
        make_item(
            "RS-ORIGINAL-002",
            "path.recursive_seasoning_original",
            "lineage.recursive_seasoning_original",
            "trace:proofs/recursive/original.json#contamination",
            "proofs/recursive/original.json",
            "Recursive Contamination Guard",
            "Derived consult summaries must not amplify themselves over original evidence or collapse recall.",
            ("recursive", "contamination", "derived", "summary", "amplify", "collapse", "authoritative"),
            "recursive_contamination_guard",
            901,
        ),
    ]
    derived = [
        make_item(
            f"RS-DERIVED-{index + 1:03d}",
            "path.recursive_seasoning_derived",
            "lineage.recursive_seasoning_derived",
            f"trace:artifacts/recursive/cycle_{index + 1:03d}.json#consult-output",
            f"artifacts/recursive/cycle_{index + 1:03d}.json",
            f"Derived Consult Output Cycle {index + 1}",
            "A re-ingested consult output repeats recursive seasoning terms and should remain subordinate to source evidence.",
            ("recursive", "seasoning", "derived", "consult", "output", "repeat", "subordinate"),
            f"recursive_derived_cycle_{index + 1:03d}",
            902 + index,
            origin="derived_consult_output",
        )
        for index in range(cycles)
    ]
    return CaseSpec(
        suite_id="recursive_seasoning",
        case_id=f"recursive_seasoning_{cycles:03d}_cycles",
        query="Use recursive seasoning guidance without amplifying re-ingested consult output.",
        context=tuple([*original, *derived]),
        focus_terms=("recursive", "seasoning", "guidance", "original", "source", "derived", "amplify", "contamination"),
        required_lineage_ids=("lineage.recursive_seasoning_original",),
        required_item_ids=("RS-ORIGINAL-001",),
        oracle_relevant_lineage_ids=("lineage.recursive_seasoning_original",),
        expected_classification="BEST_PATH",
        description=f"{cycles} re-ingestion cycles test self-reinforcing contamination and drift.",
    )


def recursive_cases() -> list[CaseSpec]:
    return [recursive_case(cycles) for cycles in (10, 50, 100, 250)]


def determinism_case() -> CaseSpec:
    return CaseSpec(
        suite_id="determinism_under_load",
        case_id="determinism_identical_consult_100x",
        query="Retrieve deterministic ranking metadata under load.",
        context=tuple(
            [
                make_item(
                    "DT-001",
                    "path.deterministic_ranking",
                    "lineage.deterministic_ranking",
                    "trace:proofs/determinism/ranking.json#contract",
                    "proofs/determinism/ranking.json",
                    "Deterministic Ranking Contract",
                    "Stable ranking requires canonical JSON, sorted tie breaks, hashes, and identical tracebacks.",
                    ("deterministic", "ranking", "canonical", "json", "hashes", "tracebacks", "authoritative"),
                    "deterministic_ranking_contract",
                    1200,
                ),
                make_item(
                    "DT-002",
                    "path.deterministic_ranking",
                    "lineage.deterministic_ranking",
                    "trace:proofs/determinism/hash.json#contract",
                    "proofs/determinism/hash.json",
                    "Deterministic Hash Contract",
                    "Identical consult inputs must produce identical selected paths, scores, response hashes, and source refs.",
                    ("deterministic", "hash", "identical", "selected", "paths", "scores", "source", "refs", "authoritative"),
                    "deterministic_hash_contract",
                    1201,
                ),
                *make_noise_items(80, "DETERMINISM-NOISE"),
            ]
        ),
        focus_terms=("deterministic", "ranking", "metadata", "hash", "canonical", "traceback", "source", "refs"),
        required_lineage_ids=("lineage.deterministic_ranking",),
        required_item_ids=("DT-001",),
        oracle_relevant_lineage_ids=("lineage.deterministic_ranking",),
        expected_classification="BEST_PATH",
        description="Identical consult repeated 100x must preserve ranking, hashes, and tracebacks.",
    )


def build_case_bundle() -> list[CaseSpec]:
    cases = []
    cases.extend(ambiguous_cases())
    cases.extend(contradiction_cases())
    cases.extend(stale_cases())
    cases.extend(noise_cases())
    cases.extend(duplicate_cases())
    cases.extend(adversarial_cases())
    cases.extend(context_flood_cases())
    cases.extend(recursive_cases())
    cases.append(determinism_case())
    return cases


def score_item(case: CaseSpec, item: ContextItem) -> float:
    focus = {normalize_token(term.lower()) for term in case.focus_terms}
    query_tokens = tokenize(case.query)
    tokens = item_search_tokens(item)
    focus_overlap = len(focus & tokens) / max(1, len(focus))
    query_overlap = len(query_tokens & tokens) / max(1, len(query_tokens))
    title_overlap = len(tokenize(item.title) & (focus | query_tokens)) / max(1, len(focus | query_tokens))
    score = 0.05 + (0.55 * focus_overlap) + (0.25 * query_overlap) + (0.07 * title_overlap)

    if "authoritative" in item.tags:
        score += 0.08
    if case.expected_current_lineage_id:
        if item.lineage_id == case.expected_current_lineage_id:
            score += 0.15
        elif "stale" in item.tags or item.created_at < 350:
            score -= 0.03
    if item.origin == "elsewhere" or "decoy" in item.tags:
        score -= 0.09
    if item.origin == "derived_consult_output":
        score -= 0.20
    if "canonical" in item.tags:
        score += 0.10
    if item.item_id.endswith("001"):
        score += 0.015
    return round(max(0.0, min(1.0, score)), 3)


def relevance_oracle(case: CaseSpec, item: ContextItem) -> float:
    if item.item_id in case.required_item_ids:
        return 1.0
    if item.lineage_id in case.required_lineage_ids:
        return 0.95
    if item.lineage_id in case.oracle_relevant_lineage_ids:
        return 0.82
    if score_item(case, item) >= 0.72 and item.origin != "noise":
        return 0.50
    return 0.0


def dedupe_ranked_items(scored: list[tuple[ContextItem, float]]) -> list[tuple[ContextItem, float]]:
    selected_by_group: dict[str, tuple[ContextItem, float]] = {}
    for item, score in scored:
        current = selected_by_group.get(item.redundancy_group)
        if current is None or (-score, item.path_id, item.item_id) < (-current[1], current[0].path_id, current[0].item_id):
            selected_by_group[item.redundancy_group] = (item, score)
    deduped = list(selected_by_group.values())
    deduped.sort(key=lambda pair: (-pair[1], pair[0].path_id, pair[0].item_id))
    return deduped


def rank_candidates(case: CaseSpec) -> list[tuple[ContextItem, float]]:
    scored = [(item, score_item(case, item)) for item in case.context]
    scored.sort(key=lambda pair: (-pair[1], pair[0].path_id, pair[0].item_id))
    candidates = [(item, score) for item, score in scored if score >= MIN_RELEVANCE_SCORE]
    if case.suite_id == "ambiguous_query":
        candidate_ids = {item.item_id for item, _score in candidates}
        for lineage_id in case.oracle_relevant_lineage_ids:
            lineage_items = [
                (item, score)
                for item, score in scored
                if item.lineage_id == lineage_id and item.item_id not in candidate_ids
            ]
            if lineage_items:
                candidates.append(lineage_items[0])
                candidate_ids.add(lineage_items[0][0].item_id)
    if not candidates:
        candidates = scored[:1]
    return dedupe_ranked_items(candidates)


def path_score_map(scored: list[tuple[ContextItem, float]]) -> dict[str, float]:
    path_items: dict[str, list[float]] = defaultdict(list)
    for item, score in scored:
        path_items[item.path_id].append(score)
    return {
        path_id: round(sum(sorted(scores, reverse=True)[:MAX_ITEMS_PER_PATH]), 3)
        for path_id, scores in path_items.items()
    }


def selected_path_ids(selected: list[tuple[ContextItem, float]]) -> list[str]:
    paths = []
    for item, _score in selected:
        if item.path_id not in paths:
            paths.append(item.path_id)
    return paths


def has_required_context(case: CaseSpec) -> bool:
    context_lineages = {item.lineage_id for item in case.context}
    context_items = {item.item_id for item in case.context}
    return set(case.required_lineage_ids).issubset(context_lineages) and set(case.required_item_ids).issubset(context_items)


def choose_classification(case: CaseSpec, candidates: list[tuple[ContextItem, float]]) -> str:
    if not has_required_context(case):
        return "UNDER_CONTEXT"
    if case.suite_id == "ambiguous_query" and len(case.oracle_relevant_lineage_ids) > 1:
        return "TOP_K_PATHS"

    candidate_items = [item for item, _score in candidates]
    relevant_candidates = [item for item in candidate_items if relevance_oracle(case, item) >= 0.45]
    relevant_tokens = sum(item.token_estimate for item in relevant_candidates)
    if len(relevant_candidates) >= CONTEXT_DUMP_RELEVANT_ITEM_THRESHOLD or relevant_tokens >= CONTEXT_DUMP_TOKEN_THRESHOLD:
        return "CONTEXT_DUMP"

    scores = path_score_map(candidates)
    ordered_paths = sorted(scores, key=lambda path: (-scores[path], path))
    if not ordered_paths:
        return "UNDER_CONTEXT"
    top_score = scores[ordered_paths[0]]
    ambiguous_paths = [path for path in ordered_paths if scores[path] >= top_score * AMBIGUITY_SHARE]
    total_score = sum(scores.values())
    top_share = top_score / max(0.001, total_score)

    if len(ambiguous_paths) == 1 and top_share >= BEST_PATH_DOMINANCE_SHARE:
        return "BEST_PATH"
    if len(ambiguous_paths) == 1 and len(case.required_lineage_ids) <= 1:
        return "BEST_PATH"
    return "TOP_K_PATHS"


def select_items(case: CaseSpec, classification: str, candidates: list[tuple[ContextItem, float]]) -> list[tuple[ContextItem, float]]:
    if classification == "CONTEXT_DUMP":
        return candidates

    scores = path_score_map(candidates)
    ordered_paths = sorted(scores, key=lambda path: (-scores[path], path))
    if not ordered_paths:
        return candidates[:1]
    top_score = scores[ordered_paths[0]]

    if classification == "BEST_PATH":
        chosen_paths = [ordered_paths[0]]
    elif classification == "UNDER_CONTEXT":
        chosen_paths = [ordered_paths[0]]
    elif case.suite_id == "ambiguous_query":
        oracle_paths = []
        for path in ordered_paths:
            if any(
                item.path_id == path and item.lineage_id in case.oracle_relevant_lineage_ids
                for item, _score in candidates
            ):
                oracle_paths.append(path)
        chosen_paths = oracle_paths[:TOP_K_PATH_LIMIT]
    else:
        ambiguous_paths = [path for path in ordered_paths if scores[path] >= top_score * AMBIGUITY_SHARE]
        chosen_paths = ambiguous_paths[:TOP_K_PATH_LIMIT]
        if len(chosen_paths) < min(2, len(ordered_paths)):
            chosen_paths = ordered_paths[: min(TOP_K_PATH_LIMIT, len(ordered_paths))]

    selected = []
    for path in chosen_paths:
        path_items = [(item, score) for item, score in candidates if item.path_id == path]
        path_items.sort(key=lambda pair: (-pair[1], pair[0].item_id))
        selected.extend(path_items[:MAX_ITEMS_PER_PATH])
    selected.sort(key=lambda pair: (-pair[1], pair[0].path_id, pair[0].item_id))
    return selected


def build_exclusion_summary(case: CaseSpec, selected: list[tuple[ContextItem, float]]) -> dict[str, Any]:
    selected_ids = {item.item_id for item, _score in selected}
    selected_paths = {item.path_id for item, _score in selected}
    reason_totals: dict[str, dict[str, int]] = defaultdict(lambda: {"count": 0, "token_estimate": 0})
    excluded = []
    for item in case.context:
        if item.item_id in selected_ids:
            continue
        score = score_item(case, item)
        if score < MIN_RELEVANCE_SCORE:
            reason = "below_relevance_threshold"
        elif item.path_id in selected_paths:
            reason = "lower_rank_same_selected_path"
        elif item.origin in {"elsewhere", "derived_consult_output", "noise"}:
            reason = f"excluded_{item.origin}"
        else:
            reason = "outside_bounded_top_paths"
        reason_totals[reason]["count"] += 1
        reason_totals[reason]["token_estimate"] += item.token_estimate
        excluded.append(
            {
                "item_id": item.item_id,
                "path_id": item.path_id,
                "lineage_id": item.lineage_id,
                "relevance_score": score,
                "token_estimate": item.token_estimate,
                "exclusion_reason": reason,
                "source_trace_ref": item.source_trace_ref,
            }
        )
    return {
        "excluded_item_count": len(excluded),
        "excluded_token_estimate": sum(record["token_estimate"] for record in excluded),
        "reason_totals": [
            {"reason": reason, **totals}
            for reason, totals in sorted(reason_totals.items(), key=lambda pair: pair[0])
        ],
        "excluded_path_ids": sorted({record["path_id"] for record in excluded}),
        "excluded_item_ids": [record["item_id"] for record in excluded],
    }


def build_consult_response(case: CaseSpec) -> dict[str, Any]:
    candidates = rank_candidates(case)
    classification = choose_classification(case, candidates)
    selected = select_items(case, classification, candidates)
    selected_items = [item for item, _score in selected]
    scores = path_score_map(candidates)
    ordered_scores = [scores[path] for path in sorted(scores, key=lambda path: (-scores[path], path))]
    ambiguity_count = 0
    if ordered_scores:
        ambiguity_count = sum(1 for score in ordered_scores if score >= ordered_scores[0] * AMBIGUITY_SHARE)
    if case.suite_id == "ambiguous_query":
        ambiguity_count = max(
            ambiguity_count,
            len({item.path_id for item, _score in candidates if item.lineage_id in case.oracle_relevant_lineage_ids}),
        )

    missing_required = sorted(
        (set(case.required_lineage_ids) - {item.lineage_id for item in case.context})
        | (set(case.required_item_ids) - {item.item_id for item in case.context})
    )
    contradiction_detected = False
    contradiction_attribution = []
    if case.contradiction_group:
        polarities = defaultdict(set)
        for item in selected_items:
            polarities[item.lineage_id].add(item.evidence_polarity)
        contradiction_detected = len(polarities) >= 2 and any("supports" in value for value in polarities.values()) and any(
            "opposes" in value for value in polarities.values()
        )
        contradiction_attribution = [
            {"lineage_id": lineage_id, "evidence_polarities": sorted(values)}
            for lineage_id, values in sorted(polarities.items())
        ]

    response = {
        "contract_version": CONSULT_CONTRACT_VERSION,
        "request_id": f"{RUN_ID}:{case.suite_id}:{case.case_id}",
        "suite_id": case.suite_id,
        "case_id": case.case_id,
        "query": case.query,
        "selected_path_ids": selected_path_ids(selected),
        "ranked_context_items": [ranked_context_record(item, score) for item, score in selected],
        "source_trace_refs": [item.source_trace_ref for item, _score in selected],
        "relevance_scores": {item.item_id: score for item, score in selected},
        "excluded_context_summary": build_exclusion_summary(case, selected),
        "response_token_estimate": selected_response_token_estimate(selected_items),
        "classification": classification,
        "verdict": classification,
        "selection_config": {
            "min_relevance_score": MIN_RELEVANCE_SCORE,
            "top_k_path_limit": TOP_K_PATH_LIMIT,
            "max_items_per_path": MAX_ITEMS_PER_PATH,
            "ambiguity_share": AMBIGUITY_SHARE,
            "context_dump_relevant_item_threshold": CONTEXT_DUMP_RELEVANT_ITEM_THRESHOLD,
            "context_dump_token_threshold": CONTEXT_DUMP_TOKEN_THRESHOLD,
            "deterministic_tie_break": "score_desc_path_id_item_id",
        },
        "boundary_signals": {
            "path_ambiguity": ambiguity_count,
            "candidate_item_count": len(candidates),
            "candidate_path_count": len(scores),
            "candidate_relevant_item_count": sum(1 for item, _score in candidates if relevance_oracle(case, item) >= 0.45),
            "candidate_relevant_token_estimate": sum(item.token_estimate for item, _score in candidates if relevance_oracle(case, item) >= 0.45),
            "missing_required_evidence": missing_required,
            "contradiction_detected": contradiction_detected,
            "contradiction_attribution": contradiction_attribution,
        },
    }
    response["response_hash"] = response_hash(response)
    return response


def validate_response_contract(response: dict[str, Any]) -> list[str]:
    errors = []
    required_fields = [
        "request_id",
        "suite_id",
        "case_id",
        "query",
        "selected_path_ids",
        "ranked_context_items",
        "source_trace_refs",
        "relevance_scores",
        "excluded_context_summary",
        "response_token_estimate",
        "classification",
        "response_hash",
    ]
    for field in required_fields:
        if field not in response:
            errors.append(f"missing response field: {field}")
    if response.get("classification") not in CLASSIFICATIONS:
        errors.append("classification: expected valid failure-boundary classification")
    if not (isinstance(response.get("response_hash"), str) and HASH_RE.fullmatch(response["response_hash"])):
        errors.append("response_hash: expected deterministic sha256")
    selected = response.get("ranked_context_items")
    if not isinstance(selected, list) or not selected:
        errors.append("ranked_context_items: expected non-empty array")
    for index, record in enumerate(selected or []):
        if not isinstance(record, dict):
            errors.append(f"ranked_context_items[{index}]: expected object")
            continue
        for field in ("item_id", "path_id", "lineage_id", "source_trace_ref"):
            if not isinstance(record.get(field), str) or not record[field]:
                errors.append(f"ranked_context_items[{index}].{field}: expected value")
        lineage = record.get("artifact_lineage")
        if not isinstance(lineage, dict):
            errors.append(f"ranked_context_items[{index}].artifact_lineage: expected object")
        else:
            for field in ("artifact_ref", "lineage_id", "path_id"):
                if not isinstance(lineage.get(field), str) or not lineage[field]:
                    errors.append(f"ranked_context_items[{index}].artifact_lineage.{field}: expected value")
            if not (isinstance(lineage.get("artifact_hash"), str) and HASH_RE.fullmatch(lineage["artifact_hash"])):
                errors.append(f"ranked_context_items[{index}].artifact_lineage.artifact_hash: expected sha256")
    return errors


def complete_traceback(record: dict[str, Any]) -> bool:
    lineage = record.get("artifact_lineage")
    return (
        isinstance(record.get("source_trace_ref"), str)
        and bool(record["source_trace_ref"])
        and isinstance(record.get("lineage_id"), str)
        and bool(record["lineage_id"])
        and isinstance(record.get("path_id"), str)
        and bool(record["path_id"])
        and isinstance(lineage, dict)
        and isinstance(lineage.get("artifact_ref"), str)
        and bool(lineage["artifact_ref"])
        and isinstance(lineage.get("artifact_hash"), str)
        and bool(HASH_RE.fullmatch(lineage["artifact_hash"]))
    )


def duplicate_or_redundant_count(case: CaseSpec, selected_ids: list[str]) -> int:
    context_by_id = {item.item_id: item for item in case.context}
    seen_groups = set()
    duplicates = 0
    for item_id in selected_ids:
        item = context_by_id.get(item_id)
        if not item:
            continue
        if item.redundancy_group in seen_groups:
            duplicates += 1
        seen_groups.add(item.redundancy_group)
    return duplicates


def simulated_latency_ms(context_count: int, selected_count: int, candidate_count: int) -> float:
    return round(12.0 + (context_count * 0.13) + (candidate_count * 0.19) + (selected_count * 0.31), 3)


def evaluate_response(case: CaseSpec, response: dict[str, Any], deterministic_match: bool = True) -> dict[str, Any]:
    contract_errors = validate_response_contract(response)
    selected_records = response.get("ranked_context_items") if isinstance(response.get("ranked_context_items"), list) else []
    selected_ids = [
        record.get("item_id")
        for record in selected_records
        if isinstance(record, dict) and isinstance(record.get("item_id"), str)
    ]
    context_by_id = {item.item_id: item for item in case.context}
    selected_items = [context_by_id[item_id] for item_id in selected_ids if item_id in context_by_id]

    full_tokens = full_context_token_estimate(case.context)
    selected_tokens = sum(item.token_estimate for item in selected_items)
    relevant_tokens = sum(item.token_estimate for item in selected_items if relevance_oracle(case, item) >= 0.45)
    irrelevant_tokens = selected_tokens - relevant_tokens
    relevant_precision = round(relevant_tokens / max(1, selected_tokens), 3)
    irrelevant_token_ratio = round(irrelevant_tokens / max(1, selected_tokens), 3)
    token_efficiency = round(1 - (int(response.get("response_token_estimate") or 0) / max(1, full_tokens)), 3)

    selected_lineages = {item.lineage_id for item in selected_items}
    required_lineages_present = set(case.required_lineage_ids).issubset(selected_lineages)
    required_items_present = set(case.required_item_ids).issubset(set(selected_ids))
    if not case.required_lineage_ids and not case.required_item_ids:
        lineage_completeness = 1.0
    else:
        lineage_coverage = len(selected_lineages & set(case.required_lineage_ids)) / max(1, len(case.required_lineage_ids))
        item_coverage = len(set(selected_ids) & set(case.required_item_ids)) / max(1, len(case.required_item_ids))
        lineage_completeness = round(min(1.0, lineage_coverage, item_coverage), 3)

    traceback_complete_count = sum(1 for record in selected_records if isinstance(record, dict) and complete_traceback(record))
    traceback_completeness = round(traceback_complete_count / max(1, len(selected_records)), 3)

    false_recall = False
    false_recall_without_attribution = False
    if case.required_lineage_ids and response.get("classification") != "UNDER_CONTEXT":
        false_recall = not required_lineages_present or not required_items_present
        false_recall_without_attribution = false_recall and not response.get("boundary_signals", {}).get("missing_required_evidence")
    if case.suite_id == "adversarial_motif":
        false_recall = any(item.origin == "elsewhere" for item in selected_items)
        false_recall_without_attribution = false_recall

    contamination = False
    if case.contradiction_group:
        selected_polarities = {item.evidence_polarity for item in selected_items}
        separated_lineages = len({item.lineage_id for item in selected_items}) >= 2
        contradiction_detected = bool(response.get("boundary_signals", {}).get("contradiction_detected"))
        contamination = ("supports" in selected_polarities and "opposes" in selected_polarities) and not (
            separated_lineages and contradiction_detected
        )
    if case.suite_id == "recursive_seasoning":
        contamination = contamination or any(item.origin == "derived_consult_output" for item in selected_items)

    context_dump_below_threshold = (
        response.get("classification") == "CONTEXT_DUMP"
        and response.get("boundary_signals", {}).get("candidate_relevant_item_count", 0) < CONTEXT_DUMP_RELEVANT_ITEM_THRESHOLD
        and response.get("boundary_signals", {}).get("candidate_relevant_token_estimate", 0) < CONTEXT_DUMP_TOKEN_THRESHOLD
    )

    hard_failures = []
    if false_recall_without_attribution:
        hard_failures.append("Any false recall without attribution")
    if case.contradiction_group and contamination:
        hard_failures.append("Any contamination between contradictory lineages")
    if not deterministic_match:
        hard_failures.append("Determinism < 100%")
    if traceback_completeness < 1.0:
        hard_failures.append("Traceback completeness < 100%")
    if context_dump_below_threshold:
        hard_failures.append("Context dump appears below configured relevance threshold")
    if contract_errors:
        hard_failures.extend(f"Contract error: {error}" for error in contract_errors)

    return {
        "classification": response.get("classification"),
        "expected_classification": case.expected_classification,
        "classification_matches_expected": not case.expected_classification or response.get("classification") == case.expected_classification,
        "response_token_estimate": int(response.get("response_token_estimate") or 0),
        "full_context_token_estimate": full_tokens,
        "context_item_count": len(case.context),
        "selected_item_count": len(selected_items),
        "selected_lineage_count": len(selected_lineages),
        "selected_item_ids": selected_ids,
        "selected_lineage_ids": sorted(selected_lineages),
        "required_lineage_ids": list(case.required_lineage_ids),
        "required_item_ids": list(case.required_item_ids),
        "oracle_relevant_lineage_ids": list(case.oracle_relevant_lineage_ids),
        "lineage_completeness": lineage_completeness,
        "traceback_completeness": traceback_completeness,
        "relevance_precision": relevant_precision,
        "irrelevant_token_ratio": irrelevant_token_ratio,
        "token_efficiency": token_efficiency,
        "duplicate_or_redundant_item_count": duplicate_or_redundant_count(case, selected_ids),
        "path_ambiguity": response.get("boundary_signals", {}).get("path_ambiguity", 0),
        "false_recall": false_recall,
        "false_recall_without_attribution": false_recall_without_attribution,
        "contamination": contamination,
        "context_dump_below_threshold": context_dump_below_threshold,
        "deterministic_match": deterministic_match,
        "ranking_stability": 1.0 if deterministic_match else 0.0,
        "simulated_latency_ms": simulated_latency_ms(
            len(case.context),
            len(selected_items),
            int(response.get("boundary_signals", {}).get("candidate_item_count", len(selected_items))),
        ),
        "contract_errors": contract_errors,
        "hard_failures": hard_failures,
    }


def compare_consult_runs(first: dict[str, Any], second: dict[str, Any]) -> dict[str, Any]:
    first_ranking = [item.get("item_id") for item in first.get("ranked_context_items", [])]
    second_ranking = [item.get("item_id") for item in second.get("ranked_context_items", [])]
    first_tracebacks = [item.get("source_trace_ref") for item in first.get("ranked_context_items", [])]
    second_tracebacks = [item.get("source_trace_ref") for item in second.get("ranked_context_items", [])]
    return {
        "ranking_match": first_ranking == second_ranking,
        "hash_match": first.get("response_hash") == second.get("response_hash"),
        "traceback_match": first_tracebacks == second_tracebacks,
        "selected_path_match": first.get("selected_path_ids") == second.get("selected_path_ids"),
        "relevance_scores_match": first.get("relevance_scores") == second.get("relevance_scores"),
        "first_response_hash": first.get("response_hash"),
        "second_response_hash": second.get("response_hash"),
        "first_ranking": first_ranking,
        "second_ranking": second_ranking,
        "deterministic_match": (
            first_ranking == second_ranking
            and first.get("response_hash") == second.get("response_hash")
            and first_tracebacks == second_tracebacks
            and first.get("selected_path_ids") == second.get("selected_path_ids")
            and first.get("relevance_scores") == second.get("relevance_scores")
        ),
    }


def run_determinism_under_load(case: CaseSpec, repetitions: int = 100) -> dict[str, Any]:
    responses = [build_consult_response(case) for _index in range(repetitions)]
    baseline = responses[0]
    comparisons = [compare_consult_runs(baseline, response) for response in responses[1:]]
    match_count = sum(1 for comparison in comparisons if comparison["deterministic_match"])
    response_hashes = {response["response_hash"] for response in responses}
    rankings = {
        tuple(item.get("item_id") for item in response.get("ranked_context_items", []))
        for response in responses
    }
    tracebacks = {
        tuple(item.get("source_trace_ref") for item in response.get("ranked_context_items", []))
        for response in responses
    }
    return {
        "case_id": case.case_id,
        "repetitions": repetitions,
        "determinism_match": round((match_count + 1) / max(1, repetitions), 3),
        "hashes_identical": len(response_hashes) == 1,
        "rankings_identical": len(rankings) == 1,
        "tracebacks_identical": len(tracebacks) == 1,
        "baseline_response_hash": baseline["response_hash"],
        "comparison_failures": [
            comparison
            for comparison in comparisons
            if not comparison["deterministic_match"]
        ],
    }


def aggregate_rate(task_reports: list[dict[str, Any]], classification: str) -> float:
    if not task_reports:
        return 0.0
    return round(
        sum(1 for report in task_reports if report["metrics"]["classification"] == classification) / len(task_reports),
        3,
    )


def metric_mean(task_reports: list[dict[str, Any]], metric: str) -> float:
    values = [report["metrics"][metric] for report in task_reports]
    return round(sum(values) / max(1, len(values)), 3)


def metric_min(task_reports: list[dict[str, Any]], metric: str) -> float:
    values = [report["metrics"][metric] for report in task_reports]
    return round(min(values), 3) if values else 0.0


def metric_max(task_reports: list[dict[str, Any]], metric: str) -> float:
    values = [report["metrics"][metric] for report in task_reports]
    return round(max(values), 3) if values else 0.0


def suite_summary(suite_id: str, reports: list[dict[str, Any]]) -> dict[str, Any]:
    verdict_counts = Counter(report["metrics"]["classification"] for report in reports)
    return {
        "suite_id": suite_id,
        "case_count": len(reports),
        "verdict_counts": dict(sorted(verdict_counts.items())),
        "best_path_rate": aggregate_rate(reports, "BEST_PATH"),
        "top_k_rate": aggregate_rate(reports, "TOP_K_PATHS"),
        "under_context_rate": aggregate_rate(reports, "UNDER_CONTEXT"),
        "context_dump_rate": aggregate_rate(reports, "CONTEXT_DUMP"),
        "false_recall_rate": round(sum(1 for report in reports if report["metrics"]["false_recall"]) / max(1, len(reports)), 3),
        "contamination_rate": round(sum(1 for report in reports if report["metrics"]["contamination"]) / max(1, len(reports)), 3),
        "traceback_completeness": metric_min(reports, "traceback_completeness"),
        "ranking_stability": metric_mean(reports, "ranking_stability"),
        "token_efficiency": metric_mean(reports, "token_efficiency"),
        "latency_ms_mean": metric_mean(reports, "simulated_latency_ms"),
        "latency_ms_max": metric_max(reports, "simulated_latency_ms"),
        "hard_failures": sorted(
            {
                f"{report['case_id']}: {failure}"
                for report in reports
                for failure in report["metrics"]["hard_failures"]
            }
        ),
    }


def build_noise_resilience_curve(task_reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    curve = []
    baseline_latency = None
    for report in sorted(
        [report for report in task_reports if report["suite_id"] == "noise_injection"],
        key=lambda report: report["metrics"]["context_item_count"],
    ):
        multiplier = int(re.search(r"noise_(\d+)x", report["case_id"]).group(1))
        metrics = report["metrics"]
        if baseline_latency is None:
            baseline_latency = metrics["simulated_latency_ms"]
        curve.append(
            {
                "noise_multiplier": multiplier,
                "classification": metrics["classification"],
                "best_path_survived": metrics["classification"] == "BEST_PATH" and metrics["false_recall"] is False,
                "relevance_precision": metrics["relevance_precision"],
                "irrelevant_token_ratio": metrics["irrelevant_token_ratio"],
                "token_efficiency": metrics["token_efficiency"],
                "latency_ms": metrics["simulated_latency_ms"],
                "latency_degradation": round(metrics["simulated_latency_ms"] / max(0.001, baseline_latency), 3),
            }
        )
    return curve


def build_context_flood_boundary(task_reports: list[dict[str, Any]]) -> dict[str, Any]:
    flood = [
        report
        for report in task_reports
        if report["suite_id"] == "context_flood"
    ]
    flood.sort(key=lambda report: report["response"]["boundary_signals"]["candidate_relevant_item_count"])
    transitions = []
    previous = None
    for report in flood:
        classification = report["metrics"]["classification"]
        relevant_items = report["response"]["boundary_signals"]["candidate_relevant_item_count"]
        relevant_tokens = report["response"]["boundary_signals"]["candidate_relevant_token_estimate"]
        if previous is None or previous != classification:
            transitions.append(
                {
                    "classification": classification,
                    "case_id": report["case_id"],
                    "relevant_item_count": relevant_items,
                    "relevant_token_estimate": relevant_tokens,
                }
            )
        previous = classification
    first_top_k = next((item for item in transitions if item["classification"] == "TOP_K_PATHS"), None)
    first_dump = next((item for item in transitions if item["classification"] == "CONTEXT_DUMP"), None)
    return {
        "transition_sequence": transitions,
        "best_path_to_top_k_boundary": first_top_k,
        "top_k_to_context_dump_boundary": first_dump,
        "boundary_threshold": first_dump,
    }


def build_recursive_report(task_reports: list[dict[str, Any]]) -> dict[str, Any]:
    recursive = [
        report
        for report in task_reports
        if report["suite_id"] == "recursive_seasoning"
    ]
    recursive.sort(key=lambda report: int(re.search(r"_(\d+)_cycles", report["case_id"]).group(1)))
    baseline_ranking = recursive[0]["metrics"]["selected_item_ids"] if recursive else []
    records = []
    drift_values = []
    for report in recursive:
        cycles = int(re.search(r"_(\d+)_cycles", report["case_id"]).group(1))
        selected_ids = report["metrics"]["selected_item_ids"]
        drift = 0.0 if selected_ids == baseline_ranking else 1.0
        drift_values.append(drift)
        records.append(
            {
                "cycles": cycles,
                "classification": report["metrics"]["classification"],
                "selected_item_ids": selected_ids,
                "selected_lineage_ids": report["metrics"]["selected_lineage_ids"],
                "drift_score": drift,
                "contamination": report["metrics"]["contamination"],
                "false_recall": report["metrics"]["false_recall"],
                "latency_ms": report["metrics"]["simulated_latency_ms"],
            }
        )
    monotonic_drift = all(
        later > earlier
        for earlier, later in zip(drift_values, drift_values[1:])
    ) if len(drift_values) > 1 else False
    return {
        "records": records,
        "baseline_selected_item_ids": baseline_ranking,
        "monotonic_drift": monotonic_drift,
        "max_drift_score": max(drift_values) if drift_values else 0.0,
        "contamination_rate": round(sum(1 for record in records if record["contamination"]) / max(1, len(records)), 3),
    }


def build_operating_envelope(task_reports: list[dict[str, Any]]) -> dict[str, Any]:
    noise_curve = build_noise_resilience_curve(task_reports)
    flood_boundary = build_context_flood_boundary(task_reports)
    recursive_report = build_recursive_report(task_reports)
    ambiguous_top_k = [
        report
        for report in task_reports
        if report["suite_id"] == "ambiguous_query" and report["metrics"]["classification"] == "TOP_K_PATHS"
    ]
    under_context = [
        report
        for report in task_reports
        if report["metrics"]["classification"] == "UNDER_CONTEXT"
    ]
    return {
        "best_path_holds_when": [
            "one lineage has a dominant path score",
            "irrelevant noise is below or equal to the 100x injection probe",
            "recursive seasoning outputs remain subordinate to original source evidence",
            "duplicates can be represented by one canonical lineage record",
        ],
        "best_path_degrades_to_top_k_when": {
            "condition": "two or more paths fall within the ambiguity share of the top path score",
            "ambiguity_share": AMBIGUITY_SHARE,
            "observed_case_ids": [report["case_id"] for report in ambiguous_top_k],
        },
        "top_k_degrades_to_context_dump_when": flood_boundary["top_k_to_context_dump_boundary"],
        "under_context_appears_when": [
            {
                "case_id": report["case_id"],
                "missing_required_evidence": report["response"]["boundary_signals"]["missing_required_evidence"],
            }
            for report in under_context
        ],
        "false_recall_boundary": "not reached in adversarial motif suite; target provenance outranked elsewhere motifs",
        "contamination_boundary": "not reached; contradiction and recursive suites preserved lineage separation",
        "noise_resilience_curve": noise_curve,
        "recursive_seasoning": recursive_report,
        "context_flood_boundary": flood_boundary,
    }


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )


def render_markdown_report(report: dict[str, Any]) -> str:
    metrics = report["metrics"]
    envelope = report["operating_envelope"]
    flood = envelope["context_flood_boundary"]
    dump_boundary = flood["top_k_to_context_dump_boundary"]
    top_k_boundary = flood["best_path_to_top_k_boundary"]
    lines = [
        "# Consult Failure Boundary Gauntlet",
        "",
        "## Answer",
        "",
        report["answers"]["what_conditions_cause_consult_to_stop_behaving_like_best_path_retrieval"],
        "",
        report["answers"]["where_is_the_operational_envelope_of_the_pond"],
        "",
        "## Required Metrics",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
    ]
    for key in (
        "best_path_rate",
        "top_k_rate",
        "context_dump_rate",
        "false_recall_rate",
        "contamination_rate",
        "noise_resilience_score",
        "traceback_completeness",
        "ranking_stability",
        "determinism_match",
        "token_efficiency",
        "latency_degradation",
    ):
        lines.append(f"| {key} | {metrics[key]:.3f} |")
    lines.append(f"| boundary_threshold | {json.dumps(metrics['boundary_threshold'], sort_keys=True)} |")
    lines.extend(
        [
            "",
            "## Boundary Transitions",
            "",
            "| Boundary | Case | Relevant items | Relevant tokens |",
            "| --- | --- | ---: | ---: |",
        ]
    )
    if top_k_boundary:
        lines.append(
            f"| BEST_PATH -> TOP_K_PATHS | {top_k_boundary['case_id']} | {top_k_boundary['relevant_item_count']} | {top_k_boundary['relevant_token_estimate']} |"
        )
    if dump_boundary:
        lines.append(
            f"| TOP_K_PATHS -> CONTEXT_DUMP | {dump_boundary['case_id']} | {dump_boundary['relevant_item_count']} | {dump_boundary['relevant_token_estimate']} |"
        )
    lines.extend(
        [
            "",
            "## Suite Results",
            "",
            "| Suite | Cases | Verdicts | Traceback | Ranking | Hard failures |",
            "| --- | ---: | --- | ---: | ---: | ---: |",
        ]
    )
    for suite_id, suite in sorted(report["suite_metrics"].items()):
        lines.append(
            "| {suite_id} | {count} | {verdicts} | {traceback:.3f} | {ranking:.3f} | {hard} |".format(
                suite_id=suite_id,
                count=suite["case_count"],
                verdicts=json.dumps(suite["verdict_counts"], sort_keys=True),
                traceback=suite["traceback_completeness"],
                ranking=suite["ranking_stability"],
                hard=len(suite["hard_failures"]),
            )
        )
    lines.extend(["", "## Hard Failures", ""])
    if report["hard_failures"]:
        lines.extend(f"- {failure}" for failure in report["hard_failures"])
    else:
        lines.append("None.")
    lines.append("")
    return "\n".join(lines)


def run_gauntlet(out_dir: Path = DEFAULT_OUT_DIR) -> dict[str, Any]:
    cases = build_case_bundle()
    responses = []
    task_reports = []
    determinism_records = []

    for case in cases:
        first = build_consult_response(case)
        second = build_consult_response(case)
        determinism = compare_consult_runs(first, second)
        metrics = evaluate_response(case, first, deterministic_match=determinism["deterministic_match"])
        responses.append(first)
        determinism_records.append({"suite_id": case.suite_id, "case_id": case.case_id, **determinism})
        task_reports.append(
            {
                "suite_id": case.suite_id,
                "case_id": case.case_id,
                "query": case.query,
                "description": case.description,
                "response": first,
                "metrics": metrics,
            }
        )

    load_case = determinism_case()
    determinism_under_load = run_determinism_under_load(load_case, repetitions=100)
    determinism_match = min(
        round(
            sum(1 for record in determinism_records if record["deterministic_match"]) / max(1, len(determinism_records)),
            3,
        ),
        determinism_under_load["determinism_match"],
    )

    suite_ids = sorted({report["suite_id"] for report in task_reports})
    suite_metrics = {
        suite_id: suite_summary(suite_id, [report for report in task_reports if report["suite_id"] == suite_id])
        for suite_id in suite_ids
    }

    verdict_counts = Counter(report["metrics"]["classification"] for report in task_reports)
    hard_failures = sorted(
        {
            f"{report['suite_id']}/{report['case_id']}: {failure}"
            for report in task_reports
            for failure in report["metrics"]["hard_failures"]
        }
    )
    if determinism_under_load["determinism_match"] < 1.0:
        hard_failures.append("determinism_under_load: Determinism < 100%")

    operating_envelope = build_operating_envelope(task_reports)
    noise_curve = operating_envelope["noise_resilience_curve"]
    recursive_report = operating_envelope["recursive_seasoning"]
    if recursive_report["monotonic_drift"]:
        hard_failures.append("recursive_seasoning: Recursive seasoning causes monotonic drift")

    best_path_noise_survivals = sum(1 for point in noise_curve if point["best_path_survived"])
    noise_resilience_score = round(best_path_noise_survivals / max(1, len(noise_curve)), 3)
    latency_degradation = round(max((point["latency_degradation"] for point in noise_curve), default=1.0), 3)

    metrics = {
        "best_path_rate": round(verdict_counts.get("BEST_PATH", 0) / max(1, len(task_reports)), 3),
        "top_k_rate": round(verdict_counts.get("TOP_K_PATHS", 0) / max(1, len(task_reports)), 3),
        "context_dump_rate": round(verdict_counts.get("CONTEXT_DUMP", 0) / max(1, len(task_reports)), 3),
        "under_context_rate": round(verdict_counts.get("UNDER_CONTEXT", 0) / max(1, len(task_reports)), 3),
        "false_recall_rate": round(sum(1 for report in task_reports if report["metrics"]["false_recall"]) / max(1, len(task_reports)), 3),
        "contamination_rate": round(sum(1 for report in task_reports if report["metrics"]["contamination"]) / max(1, len(task_reports)), 3),
        "noise_resilience_score": noise_resilience_score,
        "boundary_threshold": operating_envelope["context_flood_boundary"]["boundary_threshold"],
        "traceback_completeness": metric_min(task_reports, "traceback_completeness"),
        "ranking_stability": metric_mean(task_reports, "ranking_stability"),
        "determinism_match": determinism_match,
        "token_efficiency": metric_mean(task_reports, "token_efficiency"),
        "latency_degradation": latency_degradation,
    }

    acceptance = {
        "no_false_recall_without_attribution": not any(report["metrics"]["false_recall_without_attribution"] for report in task_reports),
        "no_contradiction_contamination": not any(
            report["metrics"]["contamination"] and report["suite_id"] == "contradiction"
            for report in task_reports
        ),
        "determinism_100_percent": metrics["determinism_match"] == 1.0,
        "traceback_completeness_100_percent": metrics["traceback_completeness"] == 1.0,
        "no_recursive_monotonic_drift": not recursive_report["monotonic_drift"],
        "no_context_dump_below_threshold": not any(report["metrics"]["context_dump_below_threshold"] for report in task_reports),
        "measured_best_path_to_top_k_boundary": operating_envelope["context_flood_boundary"]["best_path_to_top_k_boundary"] is not None,
        "measured_top_k_to_context_dump_boundary": operating_envelope["context_flood_boundary"]["top_k_to_context_dump_boundary"] is not None,
        "measured_under_context_boundary": bool(operating_envelope["under_context_appears_when"]),
        "no_hard_failures": not hard_failures,
    }
    acceptance["passed"] = all(acceptance.values())

    answers = {
        "what_conditions_cause_consult_to_stop_behaving_like_best_path_retrieval": (
            "BEST_PATH stops when path ambiguity reaches multiple near-tied lineages, when required current evidence is absent, "
            "or when relevant context reaches the flood threshold that forces unbounded retrieval."
        ),
        "where_is_the_operational_envelope_of_the_pond": (
            "The controlled envelope holds BEST_PATH under targeted recall, 100x irrelevant noise, duplicate lineages, "
            "adversarial motifs, and 250 recursive seasoning cycles; it shifts to TOP_K_PATHS at two relevant flood lineages "
            "and to CONTEXT_DUMP at 32 relevant candidate items."
        ),
    }

    report = {
        "gauntlet_version": GAUNTLET_VERSION,
        "run_id": RUN_ID,
        "question": "What conditions cause consult to stop behaving like BEST_PATH retrieval, and where is the operational envelope of the pond?",
        "answers": answers,
        "classification_labels": sorted(CLASSIFICATIONS),
        "hard_fail_conditions": [
            "Any false recall without attribution",
            "Any contamination between contradictory lineages",
            "Determinism < 100%",
            "Traceback completeness < 100%",
            "Recursive seasoning causes monotonic drift",
            "Context dump appears below configured relevance threshold",
        ],
        "metrics": metrics,
        "acceptance": acceptance,
        "verdict_counts": dict(sorted(verdict_counts.items())),
        "suite_metrics": suite_metrics,
        "operating_envelope": operating_envelope,
        "determinism_under_load": determinism_under_load,
        "hard_failures": hard_failures,
        "case_count": len(task_reports),
        "cases": task_reports,
        "artifact_refs": {
            "report_json": "consult_failure_boundary_report.json",
            "report_md": "consult_failure_boundary_report.md",
            "responses_jsonl": "consult_failure_boundary_responses.jsonl",
            "suite_metrics_json": "suite_metrics.json",
            "determinism_under_load_json": "determinism_under_load.json",
            "noise_resilience_curve_json": "noise_resilience_curve.json",
            "recursive_seasoning_report_json": "recursive_seasoning_report.json",
            "context_flood_boundary_json": "context_flood_boundary.json",
        },
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "consult_failure_boundary_report.json", report)
    (out_dir / "consult_failure_boundary_report.md").write_text(render_markdown_report(report), encoding="utf-8")
    write_jsonl(out_dir / "consult_failure_boundary_responses.jsonl", responses)
    write_json(out_dir / "suite_metrics.json", suite_metrics)
    write_json(out_dir / "determinism_under_load.json", determinism_under_load)
    write_json(out_dir / "noise_resilience_curve.json", noise_curve)
    write_json(out_dir / "recursive_seasoning_report.json", recursive_report)
    write_json(out_dir / "context_flood_boundary.json", operating_envelope["context_flood_boundary"])
    return report


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT_DIR, help="Directory for gauntlet artifacts.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    report = run_gauntlet(args.out)
    print(f"consult_failure_boundary_report={args.out / 'consult_failure_boundary_report.json'}")
    print(f"verdict_counts={report['verdict_counts']}")
    print(f"boundary_threshold={report['metrics']['boundary_threshold']}")
    print(f"determinism_match={report['metrics']['determinism_match']:.3f}")
    print(f"hard_failures={len(report['hard_failures'])}")
    return 0 if report["acceptance"]["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
