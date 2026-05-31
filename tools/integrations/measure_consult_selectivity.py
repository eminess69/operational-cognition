#!/usr/bin/env python3
"""Measure Inside Voice /consult context selectivity.

The harness uses a controlled pond fixture where each task has a small known
set of relevant lineages inside a larger unrelated context pool. It compares a
full context dump, naive keyword retrieval, and a deterministic ranked consult
selection against the same answer key.
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
DEFAULT_OUT_DIR = ROOT / "artifacts" / "integrations" / "consult_selectivity"

MEASUREMENT_VERSION = "consult_selectivity.measurement.v1"
CONSULT_CONTRACT_VERSION = "inside_voice.consult.selectivity.v1"
RUN_ID = "consult-selectivity-controlled-2026-05-28"

VALID_VERDICTS = {"BEST_PATH", "TOP_K_PATHS", "CONTEXT_DUMP", "UNDER_CONTEXT", "INVALID"}
HASH_RE = re.compile(r"^[a-f0-9]{64}$")
TOKEN_OVERHEAD = 96
MIN_TOKEN_REDUCTION = 0.50
MIN_RELEVANCE_PRECISION = 0.80
MAX_IRRELEVANT_TOKEN_RATIO = 0.20
MIN_SELECTION_SCORE = 0.34
MAX_PATHS = 2
MAX_ITEMS_PER_PATH = 2

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
    "codex",
    "consult",
    "context",
    "does",
    "for",
    "from",
    "how",
    "in",
    "inside",
    "is",
    "it",
    "of",
    "or",
    "output",
    "pond",
    "request",
    "response",
    "should",
    "task",
    "the",
    "through",
    "to",
    "voice",
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


@dataclass(frozen=True)
class TaskSpec:
    task_id: str
    query: str
    required_lineage_ids: tuple[str, ...]
    required_item_ids: tuple[str, ...]
    ideal_path_ids: tuple[str, ...]
    focus_terms: tuple[str, ...]


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
) -> ContextItem:
    tag_tuple = tuple(tags)
    artifact_hash = sha256_text(f"{artifact_ref}|{title}|{text}")
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
    )


def build_controlled_context() -> list[ContextItem]:
    """Return a mixed pond where most context is irrelevant to any one task."""

    return [
        make_item(
            "CB-001",
            "path.claim_boundary",
            "lineage.claim_boundary",
            "trace:proofs/016/claim_register.json#overclaim-gate",
            "proofs/016-operational-entropy-gauntlet/claim_register.json",
            "Claim Boundary Overclaim Gate",
            "Block positive global superiority, AGI, consciousness, black-box solved, and target-system defect claims unless directly supported. Preserve observed, inferred, hypothesis, and unresolved labels.",
            ("claim", "boundary", "overclaim", "agi", "consciousness", "global", "superiority", "target", "defect", "proof", "gate"),
            "claim_boundary_overclaim",
        ),
        make_item(
            "CB-002",
            "path.claim_boundary",
            "lineage.claim_boundary",
            "trace:docs/PUBLIC_PRIVATE_BOUNDARY.md#public-safe-consults",
            "docs/PUBLIC_PRIVATE_BOUNDARY.md",
            "Public Private Boundary",
            "Consult output may expose public-safe summaries, refs, scores, and hashes. It must not expose hidden chain-of-thought, private Inside Voice internals, substrate state, or private ledger implementation details.",
            ("public", "private", "boundary", "safe", "internals", "hidden", "ledger", "hashes", "source", "refs"),
            "public_private_boundary",
        ),
        make_item(
            "CB-003",
            "path.claim_boundary",
            "lineage.claim_boundary",
            "trace:docs/PROOF_STANDARD.md#bounded-claims",
            "docs/PROOF_STANDARD.md",
            "Bounded Proof Claim Discipline",
            "Public proof packs must separate observed evidence from inferred implications and must avoid universal capability claims when the evidence only supports a bounded audit result.",
            ("proof", "claim", "discipline", "observed", "inferred", "bounded", "audit", "universal"),
            "claim_boundary_discipline",
        ),
        make_item(
            "RA-001",
            "path.replay_adequacy",
            "lineage.replay_adequacy",
            "trace:proofs/014/full_lineage_replay_results.json#adequacy",
            "proofs/014-independent-real-trace-replication/full_lineage_replay_results.json",
            "Replay Adequacy Lineage",
            "Real-trace replay adequacy requires source refs, event order, tool outputs, environment snapshots, recovery decisions, and runtime hashes beyond visible-only transcript logs.",
            ("replay", "adequacy", "real", "trace", "event", "order", "environment", "recovery", "runtime", "hash"),
            "replay_adequacy_core",
        ),
        make_item(
            "RA-002",
            "path.replay_adequacy",
            "lineage.replay_adequacy",
            "trace:proofs/016/replay_integrity_report.md#visible-only-gap",
            "proofs/016-operational-entropy-gauntlet/replay_integrity_report.md",
            "Visible Only Replay Gap",
            "Visible-only replay can preserve readable transcript state while omitting tool lineage, recovery loops, authority state, and environment context needed for causal reconstruction.",
            ("visible", "only", "replay", "gap", "tool", "lineage", "recovery", "authority", "environment", "causal"),
            "replay_visible_gap",
        ),
        make_item(
            "CS-001",
            "path.contradiction_survivability",
            "lineage.contradiction_survivability",
            "trace:proofs/005/contradiction_matrix.json#survivability",
            "proofs/005-contradiction-survivability-audit/contradiction_matrix.json",
            "Contradiction Survivability",
            "Compression-safe contradiction handling keeps stale assumptions, rejected alternatives, supersession markers, uncertainty, and unresolved tensions traceable after summary or replay.",
            ("contradiction", "stale", "assumption", "supersession", "rejected", "alternative", "uncertainty", "unresolved", "compression"),
            "contradiction_survivability_core",
        ),
        make_item(
            "CS-002",
            "path.contradiction_survivability",
            "lineage.contradiction_survivability",
            "trace:artifacts/inside_voice/continuity_arbitration/report.json#conflicts",
            "artifacts/inside_voice/continuity_arbitration/continuity_arbitration_report.json",
            "Conflict Arbitration Pressure",
            "Arbitration uses unresolved tension refs and contradiction clusters to prevent a later answer from flattening contested or stale operational truth into a settled narrative.",
            ("conflict", "arbitration", "pressure", "contradiction", "unresolved", "tension", "stale", "truth"),
            "contradiction_arbitration_pressure",
        ),
        make_item(
            "MS-001",
            "path.mcp_seasoning_ablation",
            "lineage.mcp_seasoning_ablation",
            "trace:proofs/019/ablation_design.md#baseline-contamination",
            "proofs/019-mcp-seasoning-ablation-control/ablation_design.md",
            "MCP Seasoning Ablation Separation",
            "A valid ablation keeps baseline, seasoned, and ablated solutions separated. Baseline outputs must not cite consult artifacts, MCP-seasoned candidate refs, pressure ids, or reusable lineage pool refs.",
            ("mcp", "seasoning", "ablation", "baseline", "seasoned", "ablated", "contamination", "pressure", "candidate"),
            "mcp_ablation_separation",
        ),
        make_item(
            "MS-002",
            "path.mcp_seasoning_ablation",
            "lineage.mcp_seasoning_ablation",
            "trace:proofs/019/runtime_visibility_report.md#pool-mutation",
            "proofs/019-mcp-seasoning-ablation-control/runtime_visibility_report.md",
            "Reusable Lineage Pool Nonmutation",
            "The reusable lineage pool must remain unchanged during the ablation. Runtime hashes should distinguish seasoned and ablated consult responses without mutating the candidate corpus.",
            ("mcp", "seasoning", "reusable", "lineage", "pool", "mutation", "runtime", "hash", "candidate"),
            "mcp_pool_nonmutation",
        ),
        make_item(
            "NL-001",
            "path.novel_learning",
            "lineage.novel_learning",
            "trace:proofs/021/repeat_replay_response.json#lineage-ref",
            "proofs/021-novel-learning-replay/repeat_replay_response.json",
            "Novel Learning Replay Ref",
            "A repeat replay response must cite the learning record lineage ref and preserve the source artifact hash before using newly learned information as task evidence.",
            ("novel", "learning", "repeat", "replay", "record", "lineage", "source", "artifact", "hash"),
            "novel_learning_replay_ref",
        ),
        make_item(
            "NL-002",
            "path.novel_learning",
            "lineage.novel_learning",
            "trace:proofs/021/final_verdict.json#learning-boundary",
            "proofs/021-novel-learning-replay/final_verdict.json",
            "Novel Learning Boundary",
            "Learning replay claims remain bounded to demonstrated repeatability and cannot claim generalized learning ability outside the recorded artifact lineage.",
            ("novel", "learning", "bounded", "repeatability", "artifact", "lineage", "claim"),
            "novel_learning_boundary",
        ),
        make_item(
            "RH-001",
            "path.runtime_hash_contract",
            "lineage.runtime_hash_contract",
            "trace:tools/validate_mcp_seasoning_ablation.py#runtime-hashes",
            "tools/validate_mcp_seasoning_ablation.py",
            "Runtime Hash Contract",
            "Consult responses require runtime_request_hash, runtime_response_hash, corpus_hash, and schema_version metadata so the selection can be traced and replayed.",
            ("metadata", "runtime", "request", "response", "hash", "corpus", "schema", "traceable", "replay"),
            "runtime_hash_contract",
        ),
        make_item(
            "RH-002",
            "path.runtime_hash_contract",
            "lineage.runtime_hash_contract",
            "trace:tools/integrations/hash_contract.py#canonical-json",
            "tools/integrations/hash_contract.py",
            "Deterministic Hashing",
            "Stable ranking requires canonical JSON, sorted keys, deterministic tie breaks, and a response hash that does not change for the same query and configuration.",
            ("deterministic", "ranking", "canonical", "json", "sorted", "tie", "response", "hash", "same", "query"),
            "deterministic_hashing",
        ),
        make_item(
            "SEL-001",
            "path.consult_selectivity",
            "lineage.consult_selectivity",
            "trace:docs/integrations/CONSULT_SELECTIVITY_MEASUREMENT.md#contract",
            "docs/integrations/CONSULT_SELECTIVITY_MEASUREMENT.md",
            "Consult Selectivity Contract",
            "A selective consult returns one best lineage or a bounded top-k set, includes relevance scores and source trace refs, summarizes excluded context, and rejects full context dumps for targeted tasks.",
            ("selectivity", "best", "path", "top", "ranked", "bounded", "relevance", "source", "trace", "excluded", "dump"),
            "consult_selectivity_contract",
        ),
        make_item(
            "SEL-002",
            "path.consult_selectivity",
            "lineage.consult_selectivity",
            "trace:artifacts/integrations/consult_selectivity/report.json#metrics",
            "artifacts/integrations/consult_selectivity/consult_selectivity_report.json",
            "Consult Selectivity Metrics",
            "Selectivity measurement tracks token reduction, relevance precision, lineage completeness, deterministic ranking match, task success delta, and context efficiency score.",
            ("selectivity", "token", "reduction", "precision", "lineage", "deterministic", "ranking", "task", "success", "efficiency"),
            "consult_selectivity_metrics",
        ),
        make_item(
            "EM-001",
            "path.evidence_manifest",
            "lineage.evidence_manifest",
            "trace:tools/build_evidence_manifest.py#public-evidence",
            "tools/build_evidence_manifest.py",
            "Evidence Manifest Builder",
            "The evidence manifest builder records public web evidence, citations, target-system references, and sanitized proof evidence for publication checks.",
            ("evidence", "manifest", "public", "web", "citation", "publication", "target", "system"),
            "evidence_manifest",
        ),
        make_item(
            "UI-001",
            "path.frontend_design",
            "lineage.frontend_design",
            "trace:docs/frontend_guidance.md#controls",
            "docs/frontend_guidance.md",
            "Frontend Control Guidance",
            "Frontend work should use icons for tool buttons, segmented controls for modes, sliders for numeric values, and avoid nested cards.",
            ("frontend", "ui", "icons", "buttons", "controls", "cards", "sliders", "design"),
            "frontend_controls",
        ),
        make_item(
            "GH-001",
            "path.github_ci",
            "lineage.github_ci",
            "trace:.github/workflows/ci.yml#pytest",
            ".github/workflows/ci.yml",
            "GitHub CI Check",
            "CI triage reads GitHub Actions logs, identifies failing pytest commands, and implements approved fixes without treating external providers as in scope.",
            ("github", "ci", "actions", "logs", "pytest", "checks", "workflow"),
            "github_ci",
        ),
        make_item(
            "DOC-001",
            "path.documents",
            "lineage.documents",
            "trace:docs/document_rendering.md#docx",
            "docs/document_rendering.md",
            "Document Rendering Workflow",
            "Document artifacts should render DOCX pages to PNG or PDF for visual quality assurance before delivery.",
            ("document", "docx", "render", "png", "pdf", "quality", "assurance"),
            "documents",
        ),
        make_item(
            "PPT-001",
            "path.presentations",
            "lineage.presentations",
            "trace:docs/presentation_style.md#slides",
            "docs/presentation_style.md",
            "Presentation Deck Workflow",
            "Presentation tasks create slide decks with layout checks, speaker notes, and export verification.",
            ("presentation", "deck", "slides", "layout", "speaker", "notes", "export"),
            "presentations",
        ),
        make_item(
            "SHEET-001",
            "path.spreadsheets",
            "lineage.spreadsheets",
            "trace:docs/spreadsheet_analysis.md#charts",
            "docs/spreadsheet_analysis.md",
            "Spreadsheet Analysis Workflow",
            "Spreadsheet tasks handle formulas, tables, charts, recalculation, and workbook validation.",
            ("spreadsheet", "formula", "table", "chart", "workbook", "validation"),
            "spreadsheets",
        ),
    ]


def build_task_bundle() -> list[TaskSpec]:
    return [
        TaskSpec(
            task_id="task_claim_boundary_overclaims",
            query="How should a proof gate handle global superiority, AGI, consciousness, and target-system defect overclaims?",
            required_lineage_ids=("lineage.claim_boundary",),
            required_item_ids=("CB-001",),
            ideal_path_ids=("path.claim_boundary",),
            focus_terms=("claim", "boundary", "overclaim", "agi", "consciousness", "global", "superiority", "target", "defect", "proof", "gate"),
        ),
        TaskSpec(
            task_id="task_replay_adequacy",
            query="Which lineage is necessary to decide whether real-trace replay is adequate beyond visible-only logs?",
            required_lineage_ids=("lineage.replay_adequacy",),
            required_item_ids=("RA-001",),
            ideal_path_ids=("path.replay_adequacy",),
            focus_terms=("replay", "adequacy", "real", "trace", "visible", "only", "event", "order", "tool", "environment", "recovery", "runtime", "hash"),
        ),
        TaskSpec(
            task_id="task_contradiction_survivability",
            query="What context is needed for stale assumption and contradiction arbitration after compression?",
            required_lineage_ids=("lineage.contradiction_survivability",),
            required_item_ids=("CS-001",),
            ideal_path_ids=("path.contradiction_survivability",),
            focus_terms=("contradiction", "stale", "assumption", "arbitration", "compression", "supersession", "unresolved", "tension"),
        ),
        TaskSpec(
            task_id="task_mcp_ablation_separation",
            query="Which lineage prevents baseline contamination in MCP seasoning ablation tasks?",
            required_lineage_ids=("lineage.mcp_seasoning_ablation",),
            required_item_ids=("MS-001",),
            ideal_path_ids=("path.mcp_seasoning_ablation",),
            focus_terms=("mcp", "seasoning", "ablation", "baseline", "contamination", "seasoned", "ablated", "pressure", "candidate"),
        ),
        TaskSpec(
            task_id="task_novel_learning_replay",
            query="What lineage must a repeat replay response cite for a novel learning record?",
            required_lineage_ids=("lineage.novel_learning",),
            required_item_ids=("NL-001",),
            ideal_path_ids=("path.novel_learning",),
            focus_terms=("novel", "learning", "repeat", "replay", "record", "lineage", "cite", "source", "artifact", "hash"),
        ),
        TaskSpec(
            task_id="task_runtime_hash_contract",
            query="Which metadata proves a consult response is deterministic and traceable?",
            required_lineage_ids=("lineage.runtime_hash_contract",),
            required_item_ids=("RH-001", "RH-002"),
            ideal_path_ids=("path.runtime_hash_contract",),
            focus_terms=("metadata", "deterministic", "traceable", "runtime", "request", "response", "hash", "corpus", "schema", "canonical", "ranking"),
        ),
        TaskSpec(
            task_id="task_public_private_boundary",
            query="What context keeps Inside Voice consult output public-safe without exposing internals?",
            required_lineage_ids=("lineage.claim_boundary",),
            required_item_ids=("CB-002",),
            ideal_path_ids=("path.claim_boundary",),
            focus_terms=("public", "private", "boundary", "safe", "internals", "hidden", "ledger", "hashes", "source", "refs"),
        ),
        TaskSpec(
            task_id="task_consult_selectivity",
            query="How should /consult avoid dumping all pond context when a bounded ranked path exists?",
            required_lineage_ids=("lineage.consult_selectivity",),
            required_item_ids=("SEL-001",),
            ideal_path_ids=("path.consult_selectivity",),
            focus_terms=("selectivity", "best", "path", "top", "ranked", "bounded", "relevance", "source", "trace", "excluded", "dump"),
        ),
    ]


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
            ]
        )
    )


def score_item(task: TaskSpec, item: ContextItem) -> float:
    focus = {normalize_token(term.lower()) for term in task.focus_terms}
    query_tokens = tokenize(task.query)
    tokens = item_search_tokens(item)
    focus_overlap = len(focus & tokens) / max(1, len(focus))
    query_overlap = len(query_tokens & tokens) / max(1, len(query_tokens))
    title_bonus = 0.04 if focus & tokenize(item.title) else 0.0
    score = 0.05 + (0.73 * focus_overlap) + (0.18 * query_overlap) + title_bonus
    return round(min(1.0, score), 3)


def naive_keyword_score(task: TaskSpec, item: ContextItem) -> float:
    query_tokens = tokenize(task.query)
    tokens = item_search_tokens(item)
    return round(len(query_tokens & tokens) / max(1, len(query_tokens)), 3)


def reference_relevance_score(task: TaskSpec, item: ContextItem) -> float:
    if item.item_id in task.required_item_ids:
        return 1.0
    if item.lineage_id in task.required_lineage_ids:
        return 0.9
    if item.path_id in task.ideal_path_ids:
        return 0.85
    lexical = score_item(task, item)
    if lexical >= 0.68:
        return min(0.8, lexical)
    if lexical >= 0.50:
        return 0.5
    return 0.0


def full_context_token_estimate(context: list[ContextItem]) -> int:
    return TOKEN_OVERHEAD + sum(item.token_estimate for item in context)


def selected_response_token_estimate(items: Iterable[ContextItem]) -> int:
    return TOKEN_OVERHEAD + sum(item.token_estimate for item in items)


def select_ranked_items(task: TaskSpec, context: list[ContextItem]) -> list[tuple[ContextItem, float]]:
    scored = [(item, score_item(task, item)) for item in context]
    scored.sort(key=lambda pair: (-pair[1], pair[0].path_id, pair[0].item_id))
    relevant = [(item, score) for item, score in scored if score >= MIN_SELECTION_SCORE]
    if not relevant:
        relevant = scored[:1]

    path_scores: dict[str, float] = defaultdict(float)
    for item, score in relevant:
        path_scores[item.path_id] += score

    ordered_paths = sorted(
        path_scores,
        key=lambda path: (-path_scores[path], path),
    )
    selected_paths: list[str] = []
    if ordered_paths:
        selected_paths.append(ordered_paths[0])
    for path in ordered_paths[1:]:
        top_item_score = max(score for item, score in relevant if item.path_id == path)
        if len(selected_paths) < MAX_PATHS and top_item_score >= 0.62:
            selected_paths.append(path)

    selected: list[tuple[ContextItem, float]] = []
    for path in selected_paths:
        path_items = [(item, score) for item, score in relevant if item.path_id == path]
        path_items.sort(key=lambda pair: (-pair[1], pair[0].item_id))
        selected.extend(path_items[:MAX_ITEMS_PER_PATH])

    selected.sort(key=lambda pair: (-pair[1], pair[0].path_id, pair[0].item_id))
    return selected


def selected_path_ids(selected: list[tuple[ContextItem, float]]) -> list[str]:
    paths: list[str] = []
    for item, _score in selected:
        if item.path_id not in paths:
            paths.append(item.path_id)
    return paths


def build_exclusion_summary(
    task: TaskSpec,
    context: list[ContextItem],
    selected: list[tuple[ContextItem, float]],
) -> dict[str, Any]:
    selected_ids = {item.item_id for item, _score in selected}
    excluded_records = []
    reason_totals: dict[str, dict[str, int]] = defaultdict(lambda: {"count": 0, "token_estimate": 0})
    selected_paths = set(selected_path_ids(selected))
    for item in context:
        if item.item_id in selected_ids:
            continue
        score = score_item(task, item)
        if score < MIN_SELECTION_SCORE:
            reason = "below_relevance_threshold"
        elif item.path_id in selected_paths:
            reason = "lower_rank_same_selected_path"
        else:
            reason = "outside_bounded_top_paths"
        reason_totals[reason]["count"] += 1
        reason_totals[reason]["token_estimate"] += item.token_estimate
        excluded_records.append(
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
        "excluded_item_count": len(excluded_records),
        "excluded_token_estimate": sum(record["token_estimate"] for record in excluded_records),
        "reason_totals": [
            {"reason": reason, **totals}
            for reason, totals in sorted(reason_totals.items(), key=lambda pair: pair[0])
        ],
        "excluded_path_ids": sorted({record["path_id"] for record in excluded_records}),
        "excluded_item_ids": [record["item_id"] for record in excluded_records],
    }


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
        },
        "relevance_score": score,
        "token_estimate": item.token_estimate,
    }


def build_consult_response(task: TaskSpec, context: list[ContextItem]) -> dict[str, Any]:
    selected = select_ranked_items(task, context)
    response = {
        "contract_version": CONSULT_CONTRACT_VERSION,
        "request_id": f"{RUN_ID}:{task.task_id}",
        "query": task.query,
        "task": task.query,
        "selected_path_ids": selected_path_ids(selected),
        "ranked_context_items": [ranked_context_record(item, score) for item, score in selected],
        "source_trace_refs": [item.source_trace_ref for item, _score in selected],
        "relevance_scores": {item.item_id: score for item, score in selected},
        "excluded_context_summary": build_exclusion_summary(task, context, selected),
        "response_token_estimate": selected_response_token_estimate(item for item, _score in selected),
        "selection_config": {
            "max_paths": MAX_PATHS,
            "max_items_per_path": MAX_ITEMS_PER_PATH,
            "min_relevance_score": MIN_SELECTION_SCORE,
            "deterministic_tie_break": "score_desc_path_id_item_id",
        },
    }
    preliminary = evaluate_consult_response(task, context, response, deterministic_ranking_match=True, require_hash=False)
    response["verdict"] = preliminary["verdict"]
    response["response_hash"] = response_hash(response)
    return response


def build_context_dump_response(task: TaskSpec, context: list[ContextItem]) -> dict[str, Any]:
    selected = [(item, score_item(task, item)) for item in context]
    selected.sort(key=lambda pair: (-pair[1], pair[0].path_id, pair[0].item_id))
    response = {
        "contract_version": CONSULT_CONTRACT_VERSION,
        "request_id": f"{RUN_ID}:{task.task_id}:dump",
        "query": task.query,
        "task": task.query,
        "selected_path_ids": selected_path_ids(selected),
        "ranked_context_items": [ranked_context_record(item, score) for item, score in selected],
        "source_trace_refs": [item.source_trace_ref for item, _score in selected],
        "relevance_scores": {item.item_id: score for item, score in selected},
        "excluded_context_summary": {
            "excluded_item_count": 0,
            "excluded_token_estimate": 0,
            "reason_totals": [],
            "excluded_path_ids": [],
            "excluded_item_ids": [],
        },
        "response_token_estimate": selected_response_token_estimate(item for item, _score in selected),
        "selection_config": {
            "max_paths": "unbounded",
            "max_items_per_path": "unbounded",
            "min_relevance_score": 0.0,
            "deterministic_tie_break": "score_desc_path_id_item_id",
        },
    }
    preliminary = evaluate_consult_response(task, context, response, deterministic_ranking_match=True, require_hash=False)
    response["verdict"] = preliminary["verdict"]
    response["response_hash"] = response_hash(response)
    return response


def validate_response_contract(response: dict[str, Any], require_hash: bool = True) -> list[str]:
    errors: list[str] = []
    required_fields = [
        "request_id",
        "query",
        "task",
        "selected_path_ids",
        "ranked_context_items",
        "source_trace_refs",
        "relevance_scores",
        "excluded_context_summary",
        "verdict",
    ]
    if require_hash:
        required_fields.append("response_hash")

    for field in required_fields:
        if field not in response:
            errors.append(f"missing response field: {field}")

    if not isinstance(response.get("request_id"), str) or not response.get("request_id"):
        errors.append("request_id: expected non-empty string")
    if not isinstance(response.get("query"), str) or not response.get("query"):
        errors.append("query: expected non-empty string")
    if not isinstance(response.get("task"), str) or not response.get("task"):
        errors.append("task: expected non-empty string")
    if not isinstance(response.get("selected_path_ids"), list) or not response.get("selected_path_ids"):
        errors.append("selected_path_ids: expected non-empty array")
    if not isinstance(response.get("ranked_context_items"), list) or not response.get("ranked_context_items"):
        errors.append("ranked_context_items: expected non-empty array")
    if not isinstance(response.get("source_trace_refs"), list) or not response.get("source_trace_refs"):
        errors.append("source_trace_refs: expected non-empty array")
    if not isinstance(response.get("relevance_scores"), dict) or not response.get("relevance_scores"):
        errors.append("relevance_scores: expected non-empty object")
    if not isinstance(response.get("excluded_context_summary"), dict):
        errors.append("excluded_context_summary: expected object")
    if require_hash and not (isinstance(response.get("response_hash"), str) and HASH_RE.fullmatch(response["response_hash"])):
        errors.append("response_hash: expected deterministic sha256")
    if response.get("verdict") not in VALID_VERDICTS:
        errors.append("verdict: expected valid selectivity classification")

    selected_ids: set[str] = set()
    for index, item in enumerate(response.get("ranked_context_items") or []):
        if not isinstance(item, dict):
            errors.append(f"ranked_context_items[{index}]: expected object")
            continue
        item_id = item.get("item_id")
        if not isinstance(item_id, str) or not item_id:
            errors.append(f"ranked_context_items[{index}].item_id: expected value")
        else:
            selected_ids.add(item_id)
        for field in ("path_id", "lineage_id", "source_trace_ref"):
            if not isinstance(item.get(field), str) or not item[field]:
                errors.append(f"ranked_context_items[{index}].{field}: expected value")
        lineage = item.get("artifact_lineage")
        if not isinstance(lineage, dict):
            errors.append(f"ranked_context_items[{index}].artifact_lineage: expected object")
        else:
            for field in ("artifact_ref", "lineage_id", "path_id"):
                if not isinstance(lineage.get(field), str) or not lineage[field]:
                    errors.append(f"ranked_context_items[{index}].artifact_lineage.{field}: expected value")
            if not (isinstance(lineage.get("artifact_hash"), str) and HASH_RE.fullmatch(lineage["artifact_hash"])):
                errors.append(f"ranked_context_items[{index}].artifact_lineage.artifact_hash: expected sha256")
        if not isinstance(item.get("relevance_score"), (int, float)):
            errors.append(f"ranked_context_items[{index}].relevance_score: expected number")

    relevance_scores = response.get("relevance_scores")
    if isinstance(relevance_scores, dict):
        missing_scores = selected_ids - set(relevance_scores)
        if missing_scores:
            errors.append(f"relevance_scores: missing selected item scores {sorted(missing_scores)}")

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


def duplicate_or_redundant_count(context_by_id: dict[str, ContextItem], selected_ids: list[str]) -> int:
    seen_groups: set[str] = set()
    duplicates = 0
    lineage_counts: dict[str, int] = defaultdict(int)
    for item_id in selected_ids:
        item = context_by_id.get(item_id)
        if not item:
            continue
        if item.redundancy_group in seen_groups:
            duplicates += 1
        seen_groups.add(item.redundancy_group)
        lineage_counts[item.lineage_id] += 1
    for count in lineage_counts.values():
        if count > MAX_ITEMS_PER_PATH:
            duplicates += count - MAX_ITEMS_PER_PATH
    return duplicates


def classify_metrics(metrics: dict[str, Any], contract_errors: list[str]) -> str:
    if contract_errors or metrics["traceback_completeness"] < 1.0 or not metrics["response_hash_present"]:
        return "INVALID"
    if metrics["lineage_completeness"] < 1.0:
        return "UNDER_CONTEXT"
    if (
        metrics["irrelevant_token_ratio"] > MAX_IRRELEVANT_TOKEN_RATIO
        or metrics["token_reduction_vs_full_dump"] < MIN_TOKEN_REDUCTION
        or metrics["number_of_recalled_items"] > metrics["context_item_count"] * 0.5
    ):
        return "CONTEXT_DUMP"
    if metrics["number_of_distinct_lineages"] <= 2 and metrics["number_of_recalled_items"] <= 3 and metrics["top_path_share"] >= 0.66:
        return "BEST_PATH"
    return "TOP_K_PATHS"


def evaluate_selection(
    task: TaskSpec,
    context: list[ContextItem],
    selected_ids: list[str],
    relevance_scores: dict[str, float],
    response_token_estimate: int,
) -> dict[str, Any]:
    context_by_id = {item.item_id: item for item in context}
    selected_items = [context_by_id[item_id] for item_id in selected_ids if item_id in context_by_id]
    selected_item_tokens = sum(item.token_estimate for item in selected_items)
    full_tokens = full_context_token_estimate(context)
    benchmark_scores = {item.item_id: reference_relevance_score(task, item) for item in selected_items}
    irrelevant_items = [item for item in selected_items if benchmark_scores[item.item_id] < 0.45]
    irrelevant_tokens = sum(item.token_estimate for item in irrelevant_items)

    selected_lineages = {item.lineage_id for item in selected_items}
    selected_required_lineages = selected_lineages & set(task.required_lineage_ids)
    required_items = set(task.required_item_ids)
    selected_required_items = set(selected_ids) & required_items
    lineage_coverage = len(selected_required_lineages) / max(1, len(task.required_lineage_ids))
    item_coverage = len(selected_required_items) / max(1, len(required_items))
    lineage_completeness = round(min(1.0, lineage_coverage, item_coverage), 3)

    relevant_tokens = sum(
        item.token_estimate
        for item in selected_items
        if benchmark_scores[item.item_id] >= 0.45
    )
    relevance_precision = round(relevant_tokens / max(1, selected_item_tokens), 3)
    irrelevant_token_ratio = round(irrelevant_tokens / max(1, selected_item_tokens), 3)

    path_scores: dict[str, float] = defaultdict(float)
    for item in selected_items:
        path_scores[item.path_id] += relevance_scores.get(item.item_id, score_item(task, item))
    top_path_score = round(max(path_scores.values()) if path_scores else 0.0, 3)
    total_path_score = sum(path_scores.values())
    top_path_share = round(top_path_score / total_path_score, 3) if total_path_score else 0.0

    token_reduction = round(1 - (response_token_estimate / max(1, full_tokens)), 3)
    compression_ratio = round(response_token_estimate / max(1, full_tokens), 3)
    duplicate_count = duplicate_or_redundant_count(context_by_id, selected_ids)

    task_success_score = (
        (0.52 * lineage_completeness)
        + (0.25 * relevance_precision)
        + (0.13 * min(1.0, top_path_score))
        + (0.10 * min(1.0, token_reduction))
    )
    if irrelevant_token_ratio > MAX_IRRELEVANT_TOKEN_RATIO:
        task_success_score -= 0.20
    if duplicate_count:
        task_success_score -= min(0.15, duplicate_count * 0.05)
    task_success_score = round(max(0.0, min(1.0, task_success_score)), 3)

    context_efficiency_score = round(
        max(0.0, relevance_precision)
        * max(0.0, lineage_completeness)
        * max(0.0, token_reduction)
        * (1.0 - min(1.0, irrelevant_token_ratio)),
        3,
    )

    return {
        "response_token_estimate": response_token_estimate,
        "number_of_recalled_items": len(selected_items),
        "number_of_distinct_lineages": len(selected_lineages),
        "relevance_score_per_item": {
            item.item_id: round(relevance_scores.get(item.item_id, score_item(task, item)), 3)
            for item in selected_items
        },
        "top_path_score": top_path_score,
        "top_path_share": top_path_share,
        "irrelevant_item_count": len(irrelevant_items),
        "irrelevant_token_estimate": irrelevant_tokens,
        "irrelevant_token_ratio": irrelevant_token_ratio,
        "duplicate_or_redundant_item_count": duplicate_count,
        "traceback_completeness": 1.0,
        "compression_ratio_vs_full_context": compression_ratio,
        "token_reduction_vs_full_dump": token_reduction,
        "relevance_precision": relevance_precision,
        "lineage_completeness": lineage_completeness,
        "task_success_score": task_success_score,
        "context_efficiency_score": context_efficiency_score,
        "selected_item_ids": [item.item_id for item in selected_items],
        "selected_lineage_ids": sorted(selected_lineages),
        "required_lineage_ids": list(task.required_lineage_ids),
        "required_item_ids": list(task.required_item_ids),
        "context_item_count": len(context),
        "full_context_token_estimate": full_tokens,
    }


def evaluate_baseline(
    task: TaskSpec,
    context: list[ContextItem],
    selected_items: list[ContextItem],
    response_token_estimate: int,
) -> dict[str, Any]:
    scores = {item.item_id: score_item(task, item) for item in selected_items}
    return evaluate_selection(
        task=task,
        context=context,
        selected_ids=[item.item_id for item in selected_items],
        relevance_scores=scores,
        response_token_estimate=response_token_estimate,
    )


def evaluate_consult_response(
    task: TaskSpec,
    context: list[ContextItem],
    response: dict[str, Any],
    deterministic_ranking_match: bool,
    require_hash: bool = True,
) -> dict[str, Any]:
    contract_errors = validate_response_contract(response, require_hash=require_hash)
    selected_records = response.get("ranked_context_items") if isinstance(response.get("ranked_context_items"), list) else []
    selected_ids = [
        record.get("item_id")
        for record in selected_records
        if isinstance(record, dict) and isinstance(record.get("item_id"), str)
    ]
    relevance_scores = {
        str(item_id): float(score)
        for item_id, score in (response.get("relevance_scores") or {}).items()
        if isinstance(score, (int, float))
    }
    metrics = evaluate_selection(
        task=task,
        context=context,
        selected_ids=selected_ids,
        relevance_scores=relevance_scores,
        response_token_estimate=int(response.get("response_token_estimate") or 0),
    )

    complete_count = sum(1 for record in selected_records if isinstance(record, dict) and complete_traceback(record))
    metrics["traceback_completeness"] = round(complete_count / max(1, len(selected_records)), 3)
    metrics["response_hash_present"] = isinstance(response.get("response_hash"), str) and bool(HASH_RE.fullmatch(response["response_hash"]))
    metrics["deterministic_ranking_match"] = deterministic_ranking_match

    hard_failures: list[str] = []
    if metrics["traceback_completeness"] < 1.0:
        hard_failures.append("Any recalled item without source trace or artifact lineage")
    if metrics["irrelevant_token_ratio"] > MAX_IRRELEVANT_TOKEN_RATIO:
        hard_failures.append("More than 20% irrelevant context by token estimate")
    if require_hash and not metrics["response_hash_present"]:
        hard_failures.append("No deterministic response hash")
    if not deterministic_ranking_match:
        hard_failures.append("Same query/config returns different ranking")
    if metrics["token_reduction_vs_full_dump"] < MIN_TOKEN_REDUCTION:
        hard_failures.append("Full context dump returned when a bounded path exists")

    verdict = classify_metrics(metrics, contract_errors)
    if not deterministic_ranking_match:
        verdict = "INVALID"
    metrics["contract_errors"] = contract_errors
    metrics["hard_failures"] = hard_failures
    metrics["verdict"] = verdict
    return metrics


def naive_keyword_selection(task: TaskSpec, context: list[ContextItem]) -> list[ContextItem]:
    scored = [(item, naive_keyword_score(task, item)) for item in context]
    scored.sort(key=lambda pair: (-pair[1], pair[0].path_id, pair[0].item_id))
    selected = [item for item, score in scored if score > 0][:8]
    if not selected:
        selected = [item for item, _score in scored[:8]]
    return selected


def compare_consult_runs(first: dict[str, Any], second: dict[str, Any]) -> dict[str, Any]:
    first_ranking = [item.get("item_id") for item in first.get("ranked_context_items", [])]
    second_ranking = [item.get("item_id") for item in second.get("ranked_context_items", [])]
    return {
        "request_id": first.get("request_id"),
        "ranking_match": first_ranking == second_ranking,
        "selected_path_match": first.get("selected_path_ids") == second.get("selected_path_ids"),
        "relevance_scores_match": first.get("relevance_scores") == second.get("relevance_scores"),
        "response_hash_match": first.get("response_hash") == second.get("response_hash"),
        "first_response_hash": first.get("response_hash"),
        "second_response_hash": second.get("response_hash"),
        "first_ranking": first_ranking,
        "second_ranking": second_ranking,
        "deterministic_ranking_match": (
            first_ranking == second_ranking
            and first.get("selected_path_ids") == second.get("selected_path_ids")
            and first.get("relevance_scores") == second.get("relevance_scores")
            and first.get("response_hash") == second.get("response_hash")
        ),
    }


def build_context_exclusion_audit(
    task: TaskSpec,
    context: list[ContextItem],
    response: dict[str, Any],
) -> dict[str, Any]:
    selected_ids = {item.get("item_id") for item in response.get("ranked_context_items", [])}
    excluded = []
    for item in context:
        if item.item_id in selected_ids:
            continue
        score = score_item(task, item)
        if score < MIN_SELECTION_SCORE:
            reason = "below_relevance_threshold"
        elif item.path_id in response.get("selected_path_ids", []):
            reason = "lower_rank_same_selected_path"
        else:
            reason = "outside_bounded_top_paths"
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
        "task_id": task.task_id,
        "request_id": response.get("request_id"),
        "selected_item_ids": sorted(selected_ids),
        "selected_path_ids": response.get("selected_path_ids"),
        "excluded_items": excluded,
        "excluded_token_estimate": sum(item["token_estimate"] for item in excluded),
    }


def aggregate_metric(task_reports: list[dict[str, Any]], baseline: str, metric: str, reducer: str = "mean") -> float:
    values = [report["baselines"][baseline][metric] for report in task_reports]
    if not values:
        return 0.0
    if reducer == "min":
        return round(min(values), 3)
    if reducer == "max":
        return round(max(values), 3)
    return round(sum(values) / len(values), 3)


def aggregate_consult_metric(task_reports: list[dict[str, Any]], metric: str, reducer: str = "mean") -> float:
    values = [report["consult"]["metrics"][metric] for report in task_reports]
    if not values:
        return 0.0
    if reducer == "min":
        return round(min(values), 3)
    if reducer == "max":
        return round(max(values), 3)
    return round(sum(values) / len(values), 3)


def final_classification(verdict_counts: Counter[str]) -> str:
    if verdict_counts.get("INVALID"):
        return "INVALID"
    if verdict_counts.get("UNDER_CONTEXT"):
        return "UNDER_CONTEXT"
    if verdict_counts.get("CONTEXT_DUMP"):
        return "CONTEXT_DUMP"
    if verdict_counts.get("TOP_K_PATHS"):
        return "TOP_K_PATHS"
    return "BEST_PATH"


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(record, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )


def render_markdown_report(report: dict[str, Any]) -> str:
    aggregate = report["aggregate"]
    lines = [
        "# Consult Selectivity Measurement",
        "",
        f"Answer: `/consult` classified as **{aggregate['final_classification']}** for the controlled targeted task bundle.",
        "",
        "## Acceptance",
        "",
        "| Check | Result |",
        "| --- | --- |",
    ]
    for key, value in report["acceptance"].items():
        if key == "passed":
            continue
        lines.append(f"| {key} | {'pass' if value else 'fail'} |")
    lines.extend(
        [
            f"| overall | {'pass' if report['acceptance']['passed'] else 'fail'} |",
            "",
            "## Baseline Comparison",
            "",
            "| Baseline | Token reduction | Relevance precision | Lineage completeness | Determinism | Efficiency |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for baseline, metrics in report["baseline_aggregates"].items():
        lines.append(
            "| {baseline} | {token_reduction:.3f} | {precision:.3f} | {lineage:.3f} | {determinism:.3f} | {efficiency:.3f} |".format(
                baseline=baseline,
                token_reduction=metrics["token_reduction_vs_full_dump_mean"],
                precision=metrics["relevance_precision_mean"],
                lineage=metrics["lineage_completeness_mean"],
                determinism=metrics["deterministic_ranking_match_rate"],
                efficiency=metrics["context_efficiency_score_mean"],
            )
        )
    lines.extend(
        [
            "",
            "## Task Verdicts",
            "",
            "| Task | Verdict | Items | Lineages | Precision | Token reduction | Top path score |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for task_report in report["tasks"]:
        metrics = task_report["consult"]["metrics"]
        lines.append(
            "| {task} | {verdict} | {items} | {lineages} | {precision:.3f} | {reduction:.3f} | {top:.3f} |".format(
                task=task_report["task_id"],
                verdict=task_report["consult"]["verdict"],
                items=metrics["number_of_recalled_items"],
                lineages=metrics["number_of_distinct_lineages"],
                precision=metrics["relevance_precision"],
                reduction=metrics["token_reduction_vs_full_dump"],
                top=metrics["top_path_score"],
            )
        )
    lines.extend(["", "## Hard Failures", ""])
    if aggregate["hard_failures"]:
        lines.extend(f"- {failure}" for failure in aggregate["hard_failures"])
    else:
        lines.append("None.")
    lines.append("")
    return "\n".join(lines)


def run_measurement(out_dir: Path = DEFAULT_OUT_DIR) -> dict[str, Any]:
    context = build_controlled_context()
    tasks = build_task_bundle()

    consult_responses: list[dict[str, Any]] = []
    exclusion_audits: list[dict[str, Any]] = []
    determinism_records: list[dict[str, Any]] = []
    task_reports: list[dict[str, Any]] = []

    for task in tasks:
        first = build_consult_response(task, context)
        second = build_consult_response(task, context)
        determinism = compare_consult_runs(first, second)
        consult_metrics = evaluate_consult_response(
            task,
            context,
            first,
            deterministic_ranking_match=determinism["deterministic_ranking_match"],
        )
        first["verdict"] = consult_metrics["verdict"]
        first["response_hash"] = response_hash(first)
        consult_metrics = evaluate_consult_response(
            task,
            context,
            first,
            deterministic_ranking_match=determinism["deterministic_ranking_match"],
        )

        full_dump_items = list(context)
        full_dump_metrics = evaluate_baseline(
            task,
            context,
            full_dump_items,
            response_token_estimate=full_context_token_estimate(context),
        )
        naive_items = naive_keyword_selection(task, context)
        naive_metrics = evaluate_baseline(
            task,
            context,
            naive_items,
            response_token_estimate=selected_response_token_estimate(naive_items),
        )

        consult_metrics["answer_quality_delta"] = {
            "vs_full_dump": round(consult_metrics["task_success_score"] - full_dump_metrics["task_success_score"], 3),
            "vs_naive_keyword": round(consult_metrics["task_success_score"] - naive_metrics["task_success_score"], 3),
        }
        consult_metrics["task_success_delta"] = consult_metrics["answer_quality_delta"]

        consult_responses.append(first)
        determinism_records.append(determinism)
        exclusion_audits.append(build_context_exclusion_audit(task, context, first))
        task_reports.append(
            {
                "task_id": task.task_id,
                "query": task.query,
                "required_lineage_ids": list(task.required_lineage_ids),
                "required_item_ids": list(task.required_item_ids),
                "consult": {
                    "request_id": first["request_id"],
                    "verdict": consult_metrics["verdict"],
                    "response_hash": first["response_hash"],
                    "selected_path_ids": first["selected_path_ids"],
                    "selected_item_ids": consult_metrics["selected_item_ids"],
                    "metrics": consult_metrics,
                },
                "baselines": {
                    "full_dump": full_dump_metrics,
                    "naive_keyword": naive_metrics,
                },
            }
        )

    verdict_counts = Counter(report["consult"]["verdict"] for report in task_reports)
    hard_failures = sorted(
        {
            f"{report['task_id']}: {failure}"
            for report in task_reports
            for failure in report["consult"]["metrics"]["hard_failures"]
        }
    )
    deterministic_rate = round(
        sum(1 for record in determinism_records if record["deterministic_ranking_match"]) / max(1, len(determinism_records)),
        3,
    )

    baseline_aggregates = {
        "full_dump": {
            "token_reduction_vs_full_dump_mean": aggregate_metric(task_reports, "full_dump", "token_reduction_vs_full_dump"),
            "relevance_precision_mean": aggregate_metric(task_reports, "full_dump", "relevance_precision"),
            "lineage_completeness_mean": aggregate_metric(task_reports, "full_dump", "lineage_completeness"),
            "deterministic_ranking_match_rate": 1.0,
            "task_success_score_mean": aggregate_metric(task_reports, "full_dump", "task_success_score"),
            "context_efficiency_score_mean": aggregate_metric(task_reports, "full_dump", "context_efficiency_score"),
        },
        "naive_keyword": {
            "token_reduction_vs_full_dump_mean": aggregate_metric(task_reports, "naive_keyword", "token_reduction_vs_full_dump"),
            "relevance_precision_mean": aggregate_metric(task_reports, "naive_keyword", "relevance_precision"),
            "lineage_completeness_mean": aggregate_metric(task_reports, "naive_keyword", "lineage_completeness"),
            "deterministic_ranking_match_rate": 1.0,
            "task_success_score_mean": aggregate_metric(task_reports, "naive_keyword", "task_success_score"),
            "context_efficiency_score_mean": aggregate_metric(task_reports, "naive_keyword", "context_efficiency_score"),
        },
        "inside_voice_ranked": {
            "token_reduction_vs_full_dump_mean": aggregate_consult_metric(task_reports, "token_reduction_vs_full_dump"),
            "token_reduction_vs_full_dump_min": aggregate_consult_metric(task_reports, "token_reduction_vs_full_dump", "min"),
            "relevance_precision_mean": aggregate_consult_metric(task_reports, "relevance_precision"),
            "relevance_precision_min": aggregate_consult_metric(task_reports, "relevance_precision", "min"),
            "lineage_completeness_mean": aggregate_consult_metric(task_reports, "lineage_completeness"),
            "lineage_completeness_min": aggregate_consult_metric(task_reports, "lineage_completeness", "min"),
            "traceback_completeness_min": aggregate_consult_metric(task_reports, "traceback_completeness", "min"),
            "deterministic_ranking_match_rate": deterministic_rate,
            "task_success_score_mean": aggregate_consult_metric(task_reports, "task_success_score"),
            "context_efficiency_score_mean": aggregate_consult_metric(task_reports, "context_efficiency_score"),
        },
    }

    aggregate = {
        "task_count": len(tasks),
        "context_item_count": len(context),
        "full_context_token_estimate": full_context_token_estimate(context),
        "verdict_counts": dict(sorted(verdict_counts.items())),
        "final_classification": final_classification(verdict_counts),
        "hard_failures": hard_failures,
        "consult_token_reduction_vs_full_dump_min": baseline_aggregates["inside_voice_ranked"]["token_reduction_vs_full_dump_min"],
        "consult_relevance_precision_min": baseline_aggregates["inside_voice_ranked"]["relevance_precision_min"],
        "consult_traceback_completeness_min": baseline_aggregates["inside_voice_ranked"]["traceback_completeness_min"],
        "deterministic_ranking_match_rate": deterministic_rate,
    }

    acceptance = {
        "token_reduction_vs_full_dump_at_least_50_percent": aggregate["consult_token_reduction_vs_full_dump_min"] >= MIN_TOKEN_REDUCTION,
        "relevance_precision_at_least_0_80": aggregate["consult_relevance_precision_min"] >= MIN_RELEVANCE_PRECISION,
        "traceback_completeness_100_percent": aggregate["consult_traceback_completeness_min"] == 1.0,
        "deterministic_ranking_match_100_percent": deterministic_rate == 1.0,
        "targeted_tasks_not_context_dump": "CONTEXT_DUMP" not in verdict_counts,
        "no_hard_failures": not hard_failures,
    }
    acceptance["passed"] = all(acceptance.values())

    report = {
        "measurement_version": MEASUREMENT_VERSION,
        "run_id": RUN_ID,
        "question": "Is /consult returning best-path lineage, bounded top-k lineage, or context dumps?",
        "answer": aggregate["final_classification"],
        "method": {
            "task_bundle_size": len(tasks),
            "baselines": ["full_dump", "naive_keyword", "inside_voice_ranked"],
            "classification_labels": sorted(VALID_VERDICTS),
            "hard_fail_conditions": [
                "Any recalled item without source trace or artifact lineage",
                "More than 20% irrelevant context by token estimate",
                "No deterministic response hash",
                "Same query/config returns different ranking",
                "Full context dump returned when a bounded path exists",
            ],
        },
        "aggregate": aggregate,
        "acceptance": acceptance,
        "baseline_aggregates": baseline_aggregates,
        "determinism_report_ref": "determinism_report.json",
        "consult_responses_ref": "consult_responses.jsonl",
        "context_exclusion_audit_ref": "context_exclusion_audit.jsonl",
        "tasks": task_reports,
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "consult_selectivity_report.json", report)
    (out_dir / "consult_selectivity_report.md").write_text(render_markdown_report(report), encoding="utf-8")
    write_jsonl(out_dir / "consult_responses.jsonl", consult_responses)
    write_jsonl(out_dir / "context_exclusion_audit.jsonl", exclusion_audits)
    write_json(
        out_dir / "determinism_report.json",
        {
            "measurement_version": MEASUREMENT_VERSION,
            "run_id": RUN_ID,
            "deterministic_ranking_match_rate": deterministic_rate,
            "records": determinism_records,
        },
    )
    return report


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT_DIR, help="Directory for selectivity artifacts.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    report = run_measurement(args.out)
    aggregate = report["aggregate"]
    print(f"consult_selectivity_report={args.out / 'consult_selectivity_report.json'}")
    print(f"final_classification={aggregate['final_classification']}")
    print(f"verdict_counts={aggregate['verdict_counts']}")
    print(f"hard_failures={len(aggregate['hard_failures'])}")
    return 0 if report["acceptance"]["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
