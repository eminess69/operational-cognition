#!/usr/bin/env python3
"""Build public evidence snapshots and manifests for proof packs."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import ssl
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import request as urlrequest


ROOT = Path(__file__).resolve().parents[1]
MAX_ISSUE_BODY_CHARS = 12000

PROOF_001_SOURCES: list[dict[str, Any]] = [
    {
        "id": "openclaw-doc-compaction",
        "system": "OpenClaw",
        "type": "doc",
        "title": "OpenClaw Compaction",
        "url": "https://docs.openclaw.ai/concepts/compaction",
        "fetch_url": "https://docs.openclaw.ai/concepts/compaction.md",
        "capture_method": "markdown",
        "tags": ["long-horizon-execution", "memory-persistence", "replayability"],
        "notes": "Public documentation describes compaction behavior; included as architecture evidence, not a validated failure claim.",
    },
    {
        "id": "openclaw-doc-memory-overview",
        "system": "OpenClaw",
        "type": "doc",
        "title": "OpenClaw Memory overview",
        "url": "https://docs.openclaw.ai/concepts/memory",
        "fetch_url": "https://docs.openclaw.ai/concepts/memory.md",
        "capture_method": "markdown",
        "tags": ["memory-persistence", "multi-session-coordination"],
        "notes": "Public documentation describes memory persistence mechanisms and limits; no continuity finding is inferred.",
    },
    {
        "id": "openclaw-doc-trajectory-bundles",
        "system": "OpenClaw",
        "type": "doc",
        "title": "OpenClaw Trajectory bundles",
        "url": "https://docs.openclaw.ai/tools/trajectory",
        "fetch_url": "https://docs.openclaw.ai/tools/trajectory.md",
        "capture_method": "markdown",
        "tags": ["replayability", "tool-action-lineage"],
        "notes": "Public documentation describes trajectory export as an audit/debugging surface; included for lineage baseline only.",
    },
    {
        "id": "openclaw-issue-41216",
        "system": "OpenClaw",
        "type": "issue",
        "title": "Feature request: memory flush before /new and /restart session reset",
        "url": "https://github.com/openclaw/openclaw/issues/41216",
        "fetch_url": "https://api.github.com/repos/openclaw/openclaw/issues/41216",
        "capture_method": "github_issue",
        "tags": ["memory-persistence", "session-reset"],
        "notes": "Public issue reports a requested memory-flush behavior before reset; preserved as reported evidence only.",
    },
    {
        "id": "openclaw-issue-45981",
        "system": "OpenClaw",
        "type": "issue",
        "title": "Session memory index silently dropped on gateway restart",
        "url": "https://github.com/openclaw/openclaw/issues/45981",
        "fetch_url": "https://api.github.com/repos/openclaw/openclaw/issues/45981",
        "capture_method": "github_issue",
        "tags": ["memory-persistence", "multi-session-coordination", "recovery-loop"],
        "notes": "Public bug report about session memory indexing after restart; included as reported evidence, not independent validation.",
    },
    {
        "id": "openclaw-issue-48217",
        "system": "OpenClaw",
        "type": "issue",
        "title": "/new starts sessions as if no prior history existed",
        "url": "https://github.com/openclaw/openclaw/issues/48217",
        "fetch_url": "https://api.github.com/repos/openclaw/openclaw/issues/48217",
        "capture_method": "github_issue",
        "tags": ["cross-session-consistency", "memory-persistence", "session-reset"],
        "notes": "Public feature request reports perceived continuity loss across /new sessions; uncertainty is preserved.",
    },
    {
        "id": "openclaw-issue-58802",
        "system": "OpenClaw",
        "type": "issue",
        "title": "SessionManager.fileEntries grows unbounded in memory",
        "url": "https://github.com/openclaw/openclaw/issues/58802",
        "fetch_url": "https://api.github.com/repos/openclaw/openclaw/issues/58802",
        "capture_method": "github_issue",
        "tags": ["environmental-state", "long-horizon-execution", "recovery-loop"],
        "notes": "Public bug report about long-running session resource growth; included as reported evidence only.",
    },
    {
        "id": "openhands-cli-roadmap-147",
        "system": "OpenHands",
        "type": "roadmap",
        "title": "OpenHands CLI non-interactive mode PRD",
        "url": "https://github.com/OpenHands/OpenHands-CLI/issues/147",
        "fetch_url": "https://api.github.com/repos/OpenHands/OpenHands-CLI/issues/147",
        "capture_method": "github_issue",
        "tags": ["long-horizon-execution", "multi-session-coordination"],
        "notes": "Public PRD-style issue includes resume and non-interactive CLI requirements; not evidence of failure by itself.",
    },
    {
        "id": "openhands-doc-agent-architecture",
        "system": "OpenHands",
        "type": "doc",
        "title": "OpenHands SDK Agent architecture",
        "url": "https://docs.openhands.dev/sdk/arch/agent",
        "fetch_url": "https://docs.openhands.dev/sdk/arch/agent.md",
        "capture_method": "markdown",
        "tags": ["long-horizon-execution", "tool-action-lineage"],
        "notes": "Public architecture documentation describes a stateless event-driven reasoning-action loop.",
    },
    {
        "id": "openhands-doc-browser-session-recording",
        "system": "OpenHands",
        "type": "doc",
        "title": "OpenHands Browser Session Recording",
        "url": "https://docs.openhands.dev/sdk/guides/browser-session-recording",
        "fetch_url": "https://docs.openhands.dev/sdk/guides/browser-session-recording.md",
        "capture_method": "markdown",
        "tags": ["replayability", "tool-action-lineage"],
        "notes": "Public documentation describes browser session recording and replay support.",
    },
    {
        "id": "openhands-doc-condenser-architecture",
        "system": "OpenHands",
        "type": "doc",
        "title": "OpenHands SDK Condenser architecture",
        "url": "https://docs.openhands.dev/sdk/arch/condenser",
        "fetch_url": "https://docs.openhands.dev/sdk/arch/condenser.md",
        "capture_method": "markdown",
        "tags": ["architectural-drift", "memory-persistence"],
        "notes": "Public architecture documentation describes conversation history compression and forgotten event IDs.",
    },
    {
        "id": "openhands-doc-conversation-architecture",
        "system": "OpenHands",
        "type": "doc",
        "title": "OpenHands SDK Conversation architecture",
        "url": "https://docs.openhands.dev/sdk/arch/conversation",
        "fetch_url": "https://docs.openhands.dev/sdk/arch/conversation.md",
        "capture_method": "markdown",
        "tags": ["environmental-state", "multi-session-coordination", "tool-action-lineage"],
        "notes": "Public architecture documentation describes conversation state, event logs, persistence, and execution modes.",
    },
    {
        "id": "openhands-issue-11432",
        "system": "OpenHands",
        "type": "issue",
        "title": "Deadlock after TaskTrackingAction in headless mode",
        "url": "https://github.com/OpenHands/OpenHands/issues/11432",
        "fetch_url": "https://api.github.com/repos/OpenHands/OpenHands/issues/11432",
        "capture_method": "github_issue",
        "tags": ["long-horizon-execution", "recovery-loop", "tool-action-lineage"],
        "notes": "Public bug report describes a stalled headless run after task tracking; included as reported evidence.",
    },
    {
        "id": "openhands-issue-13109",
        "system": "OpenHands",
        "type": "issue",
        "title": "Workspace directory cannot be created when starting tasks",
        "url": "https://github.com/OpenHands/OpenHands/issues/13109",
        "fetch_url": "https://api.github.com/repos/OpenHands/OpenHands/issues/13109",
        "capture_method": "github_issue",
        "tags": ["environmental-state", "long-horizon-execution"],
        "notes": "Public bug report describes sandbox workspace initialization divergence; included as reported evidence.",
    },
    {
        "id": "openhands-issue-14287",
        "system": "OpenHands",
        "type": "issue",
        "title": "RecallAction produces two consecutive USER turns",
        "url": "https://github.com/OpenHands/OpenHands/issues/14287",
        "fetch_url": "https://api.github.com/repos/OpenHands/OpenHands/issues/14287",
        "capture_method": "github_issue",
        "tags": ["memory-persistence", "tool-action-lineage"],
        "notes": "Public issue reports role-order interaction between recall actions and strict-alternation backends; unresolved at retrieval.",
    },
]

PROOF_002_SOURCES: list[dict[str, Any]] = [
    {
        "id": "openclaw-doc-compaction",
        "system": "OpenClaw",
        "type": "doc",
        "title": "OpenClaw Compaction",
        "url": "https://docs.openclaw.ai/concepts/compaction",
        "fetch_url": "https://docs.openclaw.ai/concepts/compaction.md",
        "capture_method": "markdown",
        "tags": ["compressed-context", "memory-state", "session-state"],
        "notes": "Public documentation describes compaction, successor transcripts, and memory flush interactions relevant to replay reconstruction.",
    },
    {
        "id": "openclaw-doc-memory-overview",
        "system": "OpenClaw",
        "type": "doc",
        "title": "OpenClaw Memory overview",
        "url": "https://docs.openclaw.ai/concepts/memory",
        "fetch_url": "https://docs.openclaw.ai/concepts/memory.md",
        "capture_method": "markdown",
        "tags": ["cross-session-replay", "memory-state"],
        "notes": "Public documentation describes disk based memory files and recall mechanisms that may affect replay adequacy.",
    },
    {
        "id": "openclaw-doc-trajectory-bundles",
        "system": "OpenClaw",
        "type": "doc",
        "title": "OpenClaw Trajectory bundles",
        "url": "https://docs.openclaw.ai/tools/trajectory",
        "fetch_url": "https://docs.openclaw.ai/tools/trajectory.md",
        "capture_method": "markdown",
        "tags": ["runtime-artifacts", "tool-action-lineage", "visible-replay"],
        "notes": "Public documentation describes exported runtime and transcript timelines; included to evaluate visible versus causal replay coverage.",
    },
    {
        "id": "openhands-doc-agent-server-architecture",
        "system": "OpenHands",
        "type": "doc",
        "title": "OpenHands SDK Agent Server architecture",
        "url": "https://docs.openhands.dev/sdk/arch/agent-server",
        "fetch_url": "https://docs.openhands.dev/sdk/arch/agent-server.md",
        "capture_method": "markdown",
        "tags": ["configuration-runtime", "environment-state"],
        "notes": "Public architecture documentation describes remote execution, workspace isolation, and container orchestration surfaces relevant to replay state.",
    },
    {
        "id": "openhands-doc-browser-session-recording",
        "system": "OpenHands",
        "type": "doc",
        "title": "OpenHands Browser Session Recording",
        "url": "https://docs.openhands.dev/sdk/guides/browser-session-recording",
        "fetch_url": "https://docs.openhands.dev/sdk/guides/browser-session-recording.md",
        "capture_method": "markdown",
        "tags": ["browser-ui-state", "visible-replay"],
        "notes": "Public documentation describes browser recording and replay support through rrweb.",
    },
    {
        "id": "openhands-doc-condenser-architecture",
        "system": "OpenHands",
        "type": "doc",
        "title": "OpenHands SDK Condenser architecture",
        "url": "https://docs.openhands.dev/sdk/arch/condenser",
        "fetch_url": "https://docs.openhands.dev/sdk/arch/condenser.md",
        "capture_method": "markdown",
        "tags": ["compressed-context", "memory-state"],
        "notes": "Public architecture documentation describes history compression, summaries, and forgotten event IDs relevant to compressed-context replay.",
    },
    {
        "id": "openhands-doc-conversation-architecture",
        "system": "OpenHands",
        "type": "doc",
        "title": "OpenHands SDK Conversation architecture",
        "url": "https://docs.openhands.dev/sdk/arch/conversation",
        "fetch_url": "https://docs.openhands.dev/sdk/arch/conversation.md",
        "capture_method": "markdown",
        "tags": ["event-log", "state-management", "tool-action-lineage"],
        "notes": "Public architecture documentation describes event logs, persistence, conversation state, and local/remote execution models.",
    },
    {
        "id": "openhands-doc-events-architecture",
        "system": "OpenHands",
        "type": "doc",
        "title": "OpenHands SDK Events architecture",
        "url": "https://docs.openhands.dev/sdk/arch/events",
        "fetch_url": "https://docs.openhands.dev/sdk/arch/events.md",
        "capture_method": "markdown",
        "tags": ["causal-lineage", "event-log", "tool-action-lineage"],
        "notes": "Public architecture documentation describes typed events and event flows relevant to replay lineage.",
    },
    {
        "id": "shared-rrweb-readme",
        "system": "Shared",
        "type": "doc",
        "title": "rrweb README",
        "url": "https://github.com/rrweb-io/rrweb",
        "fetch_url": "https://raw.githubusercontent.com/rrweb-io/rrweb/master/README.md",
        "capture_method": "markdown",
        "tags": ["browser-ui-state", "visible-replay"],
        "notes": "Public upstream replay library documentation is included only as shared context for browser/UI replay semantics.",
    },
]

PROOF_003_SOURCES: list[dict[str, Any]] = [
    {
        "id": "openclaw-doc-compaction",
        "system": "OpenClaw",
        "type": "doc",
        "title": "OpenClaw Compaction",
        "url": "https://docs.openclaw.ai/concepts/compaction",
        "fetch_url": "https://docs.openclaw.ai/concepts/compaction.md",
        "capture_method": "markdown",
        "tags": ["causal-lineage", "compressed-context", "replayability", "summarization-boundary"],
        "notes": "Public documentation describes compaction, summaries, successor transcripts, memory flush behavior, and preserved recent context relevant to continuity survivability.",
    },
    {
        "id": "openclaw-doc-memory-overview",
        "system": "OpenClaw",
        "type": "doc",
        "title": "OpenClaw Memory overview",
        "url": "https://docs.openclaw.ai/concepts/memory",
        "fetch_url": "https://docs.openclaw.ai/concepts/memory.md",
        "capture_method": "markdown",
        "tags": ["cross-session-continuity", "memory-continuity"],
        "notes": "Public documentation describes memory files, recall surfaces, truncation signals, and compaction memory flush interactions.",
    },
    {
        "id": "openclaw-doc-trajectory-bundles",
        "system": "OpenClaw",
        "type": "doc",
        "title": "OpenClaw Trajectory bundles",
        "url": "https://docs.openclaw.ai/tools/trajectory",
        "fetch_url": "https://docs.openclaw.ai/tools/trajectory.md",
        "capture_method": "markdown",
        "tags": ["replay-lineage", "temporal-ordering", "tool-action-continuity"],
        "notes": "Public documentation describes trajectory export surfaces that may support post-compression reconstruction of visible transcript and tool/action lineage.",
    },
    {
        "id": "openhands-doc-agent-server-architecture",
        "system": "OpenHands",
        "type": "doc",
        "title": "OpenHands SDK Agent Server architecture",
        "url": "https://docs.openhands.dev/sdk/arch/agent-server",
        "fetch_url": "https://docs.openhands.dev/sdk/arch/agent-server.md",
        "capture_method": "markdown",
        "tags": ["environment-continuity", "runtime-state"],
        "notes": "Public architecture documentation describes remote execution and workspace surfaces relevant to environment continuity under compressed context.",
    },
    {
        "id": "openhands-doc-browser-session-recording",
        "system": "OpenHands",
        "type": "doc",
        "title": "OpenHands Browser Session Recording",
        "url": "https://docs.openhands.dev/sdk/guides/browser-session-recording",
        "fetch_url": "https://docs.openhands.dev/sdk/guides/browser-session-recording.md",
        "capture_method": "markdown",
        "tags": ["replayability", "visible-state"],
        "notes": "Public documentation describes browser recording and replay support used only as shared context for visible replay boundaries.",
    },
    {
        "id": "openhands-doc-condenser-architecture",
        "system": "OpenHands",
        "type": "doc",
        "title": "OpenHands SDK Condenser architecture",
        "url": "https://docs.openhands.dev/sdk/arch/condenser",
        "fetch_url": "https://docs.openhands.dev/sdk/arch/condenser.md",
        "capture_method": "markdown",
        "tags": ["compressed-context", "history-condensation", "omitted-event-lineage"],
        "notes": "Public architecture documentation describes history compression, summaries, kept head/tail events, forgotten event IDs, and condensed LLM-ready views.",
    },
    {
        "id": "openhands-doc-conversation-architecture",
        "system": "OpenHands",
        "type": "doc",
        "title": "OpenHands SDK Conversation architecture",
        "url": "https://docs.openhands.dev/sdk/arch/conversation",
        "fetch_url": "https://docs.openhands.dev/sdk/arch/conversation.md",
        "capture_method": "markdown",
        "tags": ["event-log", "session-state", "temporal-ordering"],
        "notes": "Public architecture documentation describes conversation state, event logs, persistence, and execution status relevant to continuity reconstruction.",
    },
    {
        "id": "openhands-doc-events-architecture",
        "system": "OpenHands",
        "type": "doc",
        "title": "OpenHands SDK Events architecture",
        "url": "https://docs.openhands.dev/sdk/arch/events",
        "fetch_url": "https://docs.openhands.dev/sdk/arch/events.md",
        "capture_method": "markdown",
        "tags": ["causal-lineage", "event-lineage", "tool-action-continuity"],
        "notes": "Public architecture documentation describes typed events and event flows relevant to continuity lineage before and after condensation.",
    },
    {
        "id": "shared-rrweb-readme",
        "system": "Shared",
        "type": "doc",
        "title": "rrweb README",
        "url": "https://github.com/rrweb-io/rrweb",
        "fetch_url": "https://raw.githubusercontent.com/rrweb-io/rrweb/master/README.md",
        "capture_method": "markdown",
        "tags": ["browser-ui-state", "visible-replay"],
        "notes": "Public upstream replay library documentation is included only as shared context for visible browser replay semantics.",
    },
]

PROOF_CONFIGS: dict[str, dict[str, Any]] = {
    "001-agent-continuity-audit": {
        "internal_consult_path": ROOT / "internal" / "inside_voice" / "evidence_collection_consult.json",
        "sources": PROOF_001_SOURCES,
    },
    "002-replayability-gap-audit": {
        "internal_consult_path": ROOT / "internal" / "inside_voice" / "proof_002_mcp_consult_response.json",
        "sources": PROOF_002_SOURCES,
    },
    "003-continuity-compression-audit": {
        "internal_consult_path": ROOT / "internal" / "inside_voice" / "proof_003_mcp_consult_response.json",
        "sources": PROOF_003_SOURCES,
    },
}


def ssl_context() -> ssl.SSLContext:
    cafile = Path("/etc/ssl/cert.pem")
    if cafile.exists():
        return ssl.create_default_context(cafile=str(cafile))
    return ssl.create_default_context()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_content(content: str) -> str:
    """Normalize whitespace before hashing captured evidence content."""
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    return " ".join(content.split()).strip()


def stable_content_hash(content: str) -> str:
    return hashlib.sha256(normalize_content(content).encode("utf-8")).hexdigest()


def canonical_json_hash(value: dict[str, Any]) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def fetch_text(url: str, capture_method: str) -> str:
    accept = "application/vnd.github+json" if capture_method == "github_issue" else "text/markdown,*/*"
    req = urlrequest.Request(
        url,
        headers={
            "Accept": accept,
            "User-Agent": "operational-cognition-evidence-builder/0.1",
        },
    )
    with urlrequest.urlopen(req, timeout=30, context=ssl_context()) as response:
        return response.read().decode("utf-8")


def issue_snapshot_content(issue: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    labels = sorted(label.get("name", "") for label in issue.get("labels", []) if isinstance(label, dict))
    body = str(issue.get("body") or "")
    body_excerpt = body[:MAX_ISSUE_BODY_CHARS]
    body_truncated = len(body) > len(body_excerpt)
    metadata = {
        "author_association": issue.get("author_association"),
        "body_full_sha256": stable_content_hash(body),
        "body_length": len(body),
        "body_truncated": body_truncated,
        "closed_at": issue.get("closed_at"),
        "comments": issue.get("comments"),
        "created_at": issue.get("created_at"),
        "labels": labels,
        "number": issue.get("number"),
        "state": issue.get("state"),
        "state_reason": issue.get("state_reason"),
        "updated_at": issue.get("updated_at"),
    }
    parts = [
        f"GitHub issue: {issue.get('title', '')}",
        f"URL: {issue.get('html_url', '')}",
        f"Number: {issue.get('number', '')}",
        f"State: {issue.get('state', '')}",
        f"State reason: {issue.get('state_reason', '')}",
        f"Created at: {issue.get('created_at', '')}",
        f"Updated at: {issue.get('updated_at', '')}",
        f"Closed at: {issue.get('closed_at', '')}",
        f"Labels: {', '.join(labels)}",
        "Body:",
        body_excerpt,
    ]
    if body_truncated:
        parts.append(f"[body truncated at {MAX_ISSUE_BODY_CHARS} characters]")
    return "\n".join(parts), metadata


def markdown_snapshot_content(raw_text: str) -> tuple[str, dict[str, Any]]:
    return raw_text, {
        "body_full_sha256": stable_content_hash(raw_text),
        "body_length": len(raw_text),
        "body_truncated": False,
    }


def capture_source(definition: dict[str, Any], retrieved_at: str) -> dict[str, Any]:
    raw_text = fetch_text(definition["fetch_url"], definition["capture_method"])
    if definition["capture_method"] == "github_issue":
        content, raw_metadata = issue_snapshot_content(json.loads(raw_text))
    elif definition["capture_method"] == "markdown":
        content, raw_metadata = markdown_snapshot_content(raw_text)
    else:
        raise ValueError(f"unsupported capture method: {definition['capture_method']}")

    normalized_content = normalize_content(content)
    content_hash = hashlib.sha256(normalized_content.encode("utf-8")).hexdigest()
    return {
        "capture_method": definition["capture_method"],
        "content_format": "normalized_text_v1",
        "content_hash": content_hash,
        "fetch_url": definition["fetch_url"],
        "id": definition["id"],
        "normalized_content": normalized_content,
        "raw_metadata": raw_metadata,
        "retrieved_at": retrieved_at,
        "system": definition["system"],
        "title": definition["title"],
        "type": definition["type"],
        "url": definition["url"],
    }


def manifest_source(definition: dict[str, Any], snapshot: dict[str, Any]) -> dict[str, Any]:
    snapshot_path = f"evidence/snapshots/{definition['id']}.json"
    return {
        "content_hash": snapshot["content_hash"],
        "id": definition["id"],
        "notes": definition["notes"],
        "retrieved_at": snapshot["retrieved_at"],
        "snapshot_path": snapshot_path,
        "system": definition["system"],
        "tags": sorted(definition["tags"]),
        "title": definition["title"],
        "type": definition["type"],
        "url": definition["url"],
    }


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def investigation_record(
    step_id: str,
    timestamp: str,
    action: str,
    source_ref: str,
    notes: str,
) -> dict[str, str]:
    record = {
        "action": action,
        "notes": notes,
        "source_ref": source_ref,
        "step_id": step_id,
        "timestamp": timestamp,
    }
    record["lineage_hash"] = canonical_json_hash(record)
    return record


def build_investigation_records(
    manifest: dict[str, Any],
    internal_consult_path: Path,
    consult_source_ref: str,
) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []

    if internal_consult_path.exists():
        consult = json.loads(internal_consult_path.read_text(encoding="utf-8"))
        hashes = consult.get("hashes", {})
        adapter_status = consult.get("adapter_status", "placeholder")
        notes = (
            "Bounded local MCP consultation recorded in ignored internal artifact; "
            f"adapter_status={adapter_status}; "
            f"request_hash={hashes.get('request_hash', '')}; "
            f"response_hash={hashes.get('response_hash', '')}."
        )
        records.append(
            investigation_record(
                "000-consult-mcp",
                str(consult.get("created_at") or utc_now()),
                "consult_mcp",
                consult_source_ref,
                notes,
            )
        )

    for index, source in enumerate(manifest["sources"], start=1):
        prefix = f"{index:03d}-{source['id']}"
        timestamp = source["retrieved_at"]
        records.extend(
            [
                investigation_record(
                    f"{prefix}-collect",
                    timestamp,
                    "collect_source",
                    source["id"],
                    f"Collected public {source['type']} from {source['url']} into {source['snapshot_path']}.",
                ),
                investigation_record(
                    f"{prefix}-normalize",
                    timestamp,
                    "normalize",
                    source["id"],
                    "Normalized whitespace before hashing captured snapshot content.",
                ),
                investigation_record(
                    f"{prefix}-hash",
                    timestamp,
                    "hash",
                    source["id"],
                    f"Computed sha256 content_hash={source['content_hash']}.",
                ),
                investigation_record(
                    f"{prefix}-classify",
                    timestamp,
                    "classify",
                    source["id"],
                    f"Assigned tags: {', '.join(source['tags'])}.",
                ),
            ]
        )
    return records


def write_investigation_log_once(
    manifest: dict[str, Any],
    investigation_log_path: Path,
    internal_consult_path: Path,
    consult_source_ref: str,
) -> bool:
    if investigation_log_path.exists():
        return False

    records = build_investigation_records(manifest, internal_consult_path, consult_source_ref)
    investigation_log_path.parent.mkdir(parents=True, exist_ok=True)
    with investigation_log_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    return True


def resolve_proof_dir(proof_dir_arg: str) -> Path:
    proof_dir = Path(proof_dir_arg)
    if not proof_dir.is_absolute():
        proof_dir = ROOT / proof_dir
    return proof_dir.resolve()


def proof_config_for(proof_id: str) -> dict[str, Any]:
    if proof_id not in PROOF_CONFIGS:
        known = ", ".join(sorted(PROOF_CONFIGS))
        raise ValueError(f"unsupported proof id {proof_id!r}; known proofs: {known}")
    return PROOF_CONFIGS[proof_id]


def build_manifest(proof_dir: Path, retrieved_at: str | None = None) -> dict[str, Any]:
    retrieved_at = retrieved_at or utc_now()
    proof_id = proof_dir.name
    config = proof_config_for(proof_id)
    evidence_dir = proof_dir / "evidence"
    snapshot_dir = evidence_dir / "snapshots"
    manifest_path = proof_dir / "evidence_manifest.json"
    investigation_log_path = proof_dir / "investigation_log.jsonl"
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    sources: list[dict[str, Any]] = []
    for definition in sorted(config["sources"], key=lambda item: item["id"]):
        snapshot = capture_source(definition, retrieved_at)
        write_json(snapshot_dir / f"{definition['id']}.json", snapshot)
        sources.append(manifest_source(definition, snapshot))

    manifest = {
        "proof_id": proof_id,
        "sources": sorted(sources, key=lambda item: item["id"]),
        "status": "evidence_collection",
    }
    write_json(manifest_path, manifest)
    wrote_log = write_investigation_log_once(
        manifest,
        investigation_log_path,
        config["internal_consult_path"],
        f"inside_voice:{proof_id}",
    )

    print(f"Wrote {manifest_path.relative_to(ROOT)}")
    print(f"Wrote {len(sources)} snapshots under {snapshot_dir.relative_to(ROOT)}")
    if wrote_log:
        print(f"Wrote {investigation_log_path.relative_to(ROOT)}")
    else:
        print(f"Preserved existing append-only {investigation_log_path.relative_to(ROOT)}")
    return manifest


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--proof-dir",
        default="proofs/001-agent-continuity-audit",
        help="Proof directory to build. Defaults to Proof 001.",
    )
    parser.add_argument(
        "--retrieved-at",
        help="ISO8601 timestamp to stamp all source retrievals. Defaults to current UTC time.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.retrieved_at and not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", args.retrieved_at):
        print("--retrieved-at must use YYYY-MM-DDTHH:MM:SSZ", file=sys.stderr)
        return 2
    try:
        proof_dir = resolve_proof_dir(args.proof_dir)
        build_manifest(proof_dir, args.retrieved_at)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
