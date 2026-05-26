#!/usr/bin/env python3
"""Validate a public evidence manifest."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

TOP_LEVEL_KEYS = {"proof_id", "status", "sources"}
SOURCE_KEYS = {
    "content_hash",
    "id",
    "notes",
    "retrieved_at",
    "snapshot_path",
    "system",
    "tags",
    "title",
    "type",
    "url",
}
SNAPSHOT_KEYS = {
    "capture_method",
    "content_format",
    "content_hash",
    "fetch_url",
    "id",
    "normalized_content",
    "raw_metadata",
    "retrieved_at",
    "system",
    "title",
    "type",
    "url",
}
ALLOWED_SYSTEMS = {"OpenClaw", "OpenHands", "Shared"}
ALLOWED_TYPES = {"repo", "issue", "discussion", "doc", "benchmark", "roadmap"}
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def normalize_content(content: str) -> str:
    content = content.replace("\r\n", "\n").replace("\r", "\n")
    return " ".join(content.split()).strip()


def stable_content_hash(content: str) -> str:
    import hashlib

    return hashlib.sha256(normalize_content(content).encode("utf-8")).hexdigest()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_timestamp(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, str):
        errors.append(f"{path}: expected ISO8601 string")
        return
    if not value.endswith("Z"):
        errors.append(f"{path}: expected UTC timestamp ending in Z")
        return
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{path}: malformed ISO8601 timestamp")


def validate_source_shape(source: Any, index: int, errors: list[str]) -> None:
    path = f"$.sources[{index}]"
    if not isinstance(source, dict):
        errors.append(f"{path}: expected object")
        return
    unexpected = set(source) - SOURCE_KEYS
    missing = SOURCE_KEYS - set(source)
    for field in sorted(missing):
        errors.append(f"{path}: missing required field {field}")
    for field in sorted(unexpected):
        errors.append(f"{path}: unexpected field {field}")
    if missing:
        return

    if not isinstance(source["id"], str) or not ID_RE.match(source["id"]):
        errors.append(f"{path}.id: expected stable lowercase id")
    if source["system"] not in ALLOWED_SYSTEMS:
        errors.append(f"{path}.system: expected one of {sorted(ALLOWED_SYSTEMS)}")
    if source["type"] not in ALLOWED_TYPES:
        errors.append(f"{path}.type: expected one of {sorted(ALLOWED_TYPES)}")
    for field in ("title", "url", "notes", "snapshot_path", "content_hash"):
        if not isinstance(source[field], str) or not source[field]:
            errors.append(f"{path}.{field}: expected non-empty string")
    if isinstance(source.get("url"), str) and not source["url"].startswith("https://"):
        errors.append(f"{path}.url: expected https URL")
    if isinstance(source.get("content_hash"), str) and not HASH_RE.match(source["content_hash"]):
        errors.append(f"{path}.content_hash: expected sha256 hex digest")
    validate_timestamp(source.get("retrieved_at"), f"{path}.retrieved_at", errors)

    tags = source.get("tags")
    if not isinstance(tags, list) or not tags:
        errors.append(f"{path}.tags: expected non-empty array")
    elif any(not isinstance(tag, str) or not tag for tag in tags):
        errors.append(f"{path}.tags: expected non-empty string tags")
    elif tags != sorted(tags):
        errors.append(f"{path}.tags: expected deterministic sorted order")
    elif len(tags) != len(set(tags)):
        errors.append(f"{path}.tags: duplicate tags")


def resolve_snapshot_path(manifest_dir: Path, snapshot_path: str) -> Path | None:
    path = Path(snapshot_path)
    if path.is_absolute() or ".." in path.parts:
        return None
    return manifest_dir / path


def validate_snapshot(source: dict[str, Any], manifest_dir: Path, index: int, errors: list[str]) -> None:
    path = f"$.sources[{index}]"
    snapshot_path = resolve_snapshot_path(manifest_dir, source["snapshot_path"])
    if snapshot_path is None:
        errors.append(f"{path}.snapshot_path: must be relative and stay within proof directory")
        return
    if not snapshot_path.exists():
        errors.append(f"{path}.snapshot_path: missing snapshot file {source['snapshot_path']}")
        return
    try:
        snapshot = load_json(snapshot_path)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path}.snapshot_path: invalid snapshot JSON: {exc}")
        return

    if not isinstance(snapshot, dict):
        errors.append(f"{path}.snapshot_path: expected snapshot object")
        return
    missing = SNAPSHOT_KEYS - set(snapshot)
    for field in sorted(missing):
        errors.append(f"{path}.snapshot_path: snapshot missing field {field}")
    if missing:
        return

    for field in ("id", "system", "type", "title", "url", "retrieved_at"):
        if snapshot.get(field) != source.get(field):
            errors.append(f"{path}.snapshot_path: snapshot {field} does not match manifest")

    content = snapshot.get("normalized_content")
    if not isinstance(content, str) or not content:
        errors.append(f"{path}.snapshot_path: normalized_content must be non-empty string")
        return
    expected_hash = stable_content_hash(content)
    if snapshot.get("content_hash") != expected_hash:
        errors.append(f"{path}.snapshot_path: snapshot content_hash does not match normalized_content")
    if source.get("content_hash") != expected_hash:
        errors.append(f"{path}.content_hash: manifest hash does not match snapshot content")


def validate_manifest_data(manifest: Any, manifest_dir: Path) -> list[str]:
    errors: list[str] = []
    if not isinstance(manifest, dict):
        return ["$: expected object"]

    unexpected = set(manifest) - TOP_LEVEL_KEYS
    missing = TOP_LEVEL_KEYS - set(manifest)
    for field in sorted(missing):
        errors.append(f"$: missing required field {field}")
    for field in sorted(unexpected):
        errors.append(f"$: unexpected field {field}")
    if missing:
        return errors

    expected_proof_id = manifest_dir.name
    if manifest.get("proof_id") != expected_proof_id:
        errors.append(f"$.proof_id: expected {expected_proof_id}")
    if manifest.get("status") != "evidence_collection":
        errors.append("$.status: expected evidence_collection")

    sources = manifest.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("$.sources: expected non-empty array")
        return errors

    ids: list[str] = []
    for index, source in enumerate(sources):
        validate_source_shape(source, index, errors)
        if isinstance(source, dict) and isinstance(source.get("id"), str):
            ids.append(source["id"])

    if ids != sorted(ids):
        errors.append("$.sources: expected deterministic id ordering")
    duplicates = sorted({source_id for source_id in ids if ids.count(source_id) > 1})
    for source_id in duplicates:
        errors.append(f"$.sources: duplicate source id {source_id}")

    for index, source in enumerate(sources):
        if isinstance(source, dict) and not (SOURCE_KEYS - set(source)):
            validate_snapshot(source, manifest_dir, index, errors)

    return errors


def validate_manifest(path: Path) -> list[str]:
    try:
        manifest = load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        return [str(exc)]
    return validate_manifest_data(manifest, path.parent)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_evidence_manifest.py <evidence_manifest.json>", file=sys.stderr)
        return 2

    manifest_path = Path(argv[1])
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path

    errors = validate_manifest(manifest_path)
    if errors:
        print("EVIDENCE_MANIFEST_INVALID")
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("EVIDENCE_MANIFEST_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
