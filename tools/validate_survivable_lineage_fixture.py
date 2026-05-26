#!/usr/bin/env python3
"""Validate the Proof 009 survivable lineage fixture."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PROOF_FILES = [
    "README.md",
    "fixture_design.md",
    "fixture_schema.md",
    "visible_replay_mode.md",
    "full_lineage_replay_mode.md",
    "probe_set.md",
    "expected_results.md",
    "proof_manifest.json",
]

REQUIRED_FIXTURE_FILES = [
    "fixture/README.md",
    "fixture/transcript.jsonl",
    "fixture/events.jsonl",
    "fixture/tool_actions.jsonl",
    "fixture/tool_results_manifest.json",
    "fixture/memory_log.jsonl",
    "fixture/compressed_context_summary.json",
    "fixture/omitted_ranges.json",
    "fixture/contradiction_refs.json",
    "fixture/authority_refs.json",
    "fixture/temporal_validity.json",
    "fixture/environment_snapshot_manifest.json",
    "fixture/runtime_config.json",
    "fixture/recovery_trace.jsonl",
    "fixture/provenance_manifest.json",
    "fixture/public_lineage_summary.md",
]

PROBE_IDS = [f"P-{index:03d}" for index in range(1, 7)]
ID_REF_RE = re.compile(r"`((?:T|E|A|TR|ML|MEM|S|O|C|AUTH|TV|ENV|R)-[A-Z0-9.-]+)`")
ARTIFACT_REF_RE = re.compile(r"`(fixture/[^`]+)`")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class FixtureData(dict[str, Any]):
    pass


def load_json(path: Path, errors: list[str]) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return None


def load_jsonl(path: Path, errors: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    value = json.loads(line)
                except json.JSONDecodeError as exc:
                    errors.append(f"{path}:{line_number}: invalid JSONL: {exc}")
                    continue
                if not isinstance(value, dict):
                    errors.append(f"{path}:{line_number}: expected object")
                    continue
                rows.append(value)
    except OSError as exc:
        errors.append(f"{path}: cannot read JSONL: {exc}")
    return rows


def unique_ids(rows: list[dict[str, Any]], field: str, label: str, errors: list[str]) -> set[str]:
    seen: set[str] = set()
    for row in rows:
        value = row.get(field)
        if not isinstance(value, str) or not value:
            errors.append(f"{label}: missing {field}")
            continue
        if value in seen:
            errors.append(f"{label}: duplicate {field} {value}")
        seen.add(value)
    return seen


def collect_ids(items: list[dict[str, Any]], field: str, label: str, errors: list[str]) -> set[str]:
    return unique_ids(items, field, label, errors)


def ensure_ref(ref: Any, valid: set[str], label: str, errors: list[str]) -> None:
    if ref is None:
        return
    if not isinstance(ref, str) or ref not in valid:
        errors.append(f"{label}: unresolved ref {ref!r}")


def ensure_refs(refs: Any, valid: set[str], label: str, errors: list[str]) -> None:
    if refs is None:
        return
    if isinstance(refs, str):
        ensure_ref(refs, valid, label, errors)
        return
    if not isinstance(refs, list):
        errors.append(f"{label}: expected ref list")
        return
    for ref in refs:
        ensure_ref(ref, valid, label, errors)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_required_files(proof_dir: Path, errors: list[str]) -> None:
    for relative in REQUIRED_PROOF_FILES + REQUIRED_FIXTURE_FILES:
        path = proof_dir / relative
        if not path.is_file():
            errors.append(f"missing required artifact: {relative}")


def load_fixture_data(proof_dir: Path, errors: list[str]) -> FixtureData:
    data = FixtureData()
    fixture_dir = proof_dir / "fixture"
    data["transcript"] = load_jsonl(fixture_dir / "transcript.jsonl", errors)
    data["events"] = load_jsonl(fixture_dir / "events.jsonl", errors)
    data["tool_actions"] = load_jsonl(fixture_dir / "tool_actions.jsonl", errors)
    data["memory_log"] = load_jsonl(fixture_dir / "memory_log.jsonl", errors)
    data["recovery_trace"] = load_jsonl(fixture_dir / "recovery_trace.jsonl", errors)
    data["tool_results_manifest"] = load_json(fixture_dir / "tool_results_manifest.json", errors)
    data["summary"] = load_json(fixture_dir / "compressed_context_summary.json", errors)
    data["omitted_ranges"] = load_json(fixture_dir / "omitted_ranges.json", errors)
    data["contradictions"] = load_json(fixture_dir / "contradiction_refs.json", errors)
    data["authority"] = load_json(fixture_dir / "authority_refs.json", errors)
    data["temporal"] = load_json(fixture_dir / "temporal_validity.json", errors)
    data["environment"] = load_json(fixture_dir / "environment_snapshot_manifest.json", errors)
    data["runtime_config"] = load_json(fixture_dir / "runtime_config.json", errors)
    data["provenance"] = load_json(fixture_dir / "provenance_manifest.json", errors)
    return data


def build_id_sets(data: FixtureData, errors: list[str]) -> dict[str, set[str]]:
    tool_results = []
    if isinstance(data.get("tool_results_manifest"), dict):
        tool_results = data["tool_results_manifest"].get("tool_results", [])
    omitted_ranges = []
    if isinstance(data.get("omitted_ranges"), dict):
        omitted_ranges = data["omitted_ranges"].get("omitted_ranges", [])
    contradictions = []
    if isinstance(data.get("contradictions"), dict):
        contradictions = data["contradictions"].get("contradictions", [])
    authority_refs = []
    if isinstance(data.get("authority"), dict):
        authority_refs = data["authority"].get("authority_refs", [])
    temporal_refs = []
    if isinstance(data.get("temporal"), dict):
        temporal_refs = data["temporal"].get("temporal_refs", [])
    snapshots = []
    if isinstance(data.get("environment"), dict):
        snapshots = data["environment"].get("snapshots", [])

    sets = {
        "turns": unique_ids(data["transcript"], "turn_id", "transcript", errors),
        "events": unique_ids(data["events"], "event_id", "events", errors),
        "actions": unique_ids(data["tool_actions"], "action_id", "tool_actions", errors),
        "memory_events": unique_ids(data["memory_log"], "memory_event_id", "memory_log", errors),
        "memory": unique_ids(data["memory_log"], "memory_id", "memory_log", []),
        "recoveries": unique_ids(data["recovery_trace"], "recovery_event_id", "recovery_trace", errors),
        "tool_results": collect_ids(tool_results, "result_id", "tool_results", errors),
        "omitted_ranges": collect_ids(omitted_ranges, "omitted_range_id", "omitted_ranges", errors),
        "contradictions": collect_ids(contradictions, "contradiction_id", "contradictions", errors),
        "authority": collect_ids(authority_refs, "authority_id", "authority_refs", errors),
        "temporal": collect_ids(temporal_refs, "temporal_id", "temporal_refs", errors),
        "environment": collect_ids(snapshots, "snapshot_id", "environment", errors),
    }
    summary = data.get("summary")
    if isinstance(summary, dict) and isinstance(summary.get("summary_id"), str):
        sets["summaries"] = {summary["summary_id"]}
    else:
        sets["summaries"] = set()
        errors.append("compressed_context_summary: missing summary_id")
    return sets


def check_refs(data: FixtureData, ids: dict[str, set[str]], errors: list[str]) -> None:
    for row in data["transcript"]:
        ensure_ref(row.get("event_id"), ids["events"], f"transcript {row.get('turn_id')}", errors)
        ensure_refs(row.get("omitted_range_refs"), ids["omitted_ranges"], f"transcript {row.get('turn_id')}", errors)

    for row in data["events"]:
        label = f"event {row.get('event_id')}"
        ensure_ref(row.get("turn_id"), ids["turns"], label, errors)
        ensure_ref(row.get("tool_action_id"), ids["actions"], label, errors)
        ensure_ref(row.get("tool_result_id"), ids["tool_results"], label, errors)
        ensure_ref(row.get("memory_event_id"), ids["memory_events"], label, errors)
        ensure_ref(row.get("contradiction_id"), ids["contradictions"], label, errors)
        ensure_ref(row.get("summary_id"), ids["summaries"], label, errors)
        ensure_ref(row.get("recovery_event_id"), ids["recoveries"], label, errors)

    all_decision_refs = (
        ids["contradictions"]
        | ids["environment"]
        | ids["memory"]
        | ids["recoveries"]
        | ids["actions"]
        | ids["tool_results"]
    )
    for row in data["tool_actions"]:
        label = f"tool_action {row.get('action_id')}"
        ensure_ref(row.get("event_id"), ids["events"], label, errors)
        ensure_ref(row.get("result_ref"), ids["tool_results"], label, errors)
        ensure_refs(row.get("decision_claim_refs"), all_decision_refs, label, errors)

    manifest = data.get("tool_results_manifest")
    if isinstance(manifest, dict):
        for row in manifest.get("tool_results", []):
            label = f"tool_result {row.get('result_id')}"
            ensure_ref(row.get("producer_action_id"), ids["actions"], label, errors)
            ensure_ref(row.get("source_event_id"), ids["events"], label, errors)

    for row in data["memory_log"]:
        label = f"memory_log {row.get('memory_event_id')}"
        ensure_ref(row.get("event_id"), ids["events"], label, errors)
        ensure_refs(row.get("source_turn_refs"), ids["turns"], label, errors)
        ensure_refs(row.get("source_event_refs"), ids["events"], label, errors)
        ensure_refs(row.get("authority_refs"), ids["authority"], label, errors)
        ensure_refs(row.get("temporal_validity_refs"), ids["temporal"], label, errors)
        ensure_refs(row.get("contradiction_refs"), ids["contradictions"], label, errors)
        ensure_ref(row.get("insertion_event_id"), ids["events"], label, errors)

    summary = data.get("summary")
    if isinstance(summary, dict):
        ensure_ref(summary.get("event_id"), ids["events"], "summary", errors)
        ensure_refs(summary.get("source_event_range"), ids["events"], "summary", errors)
        ensure_refs(summary.get("source_turn_range"), ids["turns"], "summary", errors)
        ensure_refs(summary.get("retained_head_turn_ids"), ids["turns"], "summary", errors)
        ensure_refs(summary.get("retained_tail_event_ids"), ids["events"], "summary", errors)
        ensure_refs(summary.get("omitted_range_refs"), ids["omitted_ranges"], "summary", errors)
        ensure_refs(summary.get("memory_refs"), ids["memory"], "summary", errors)
        ensure_refs(summary.get("contradiction_refs"), ids["contradictions"], "summary", errors)
        ensure_refs(summary.get("authority_refs"), ids["authority"], "summary", errors)

    omitted = data.get("omitted_ranges")
    if isinstance(omitted, dict):
        for row in omitted.get("omitted_ranges", []):
            label = f"omitted_range {row.get('omitted_range_id')}"
            ensure_ref(row.get("summary_id"), ids["summaries"], label, errors)
            ensure_refs(row.get("source_event_ids"), ids["events"], label, errors)
            ensure_refs(row.get("source_turn_ids"), ids["turns"], label, errors)
            if not isinstance(row.get("content_sha256"), str) or not SHA256_RE.match(row["content_sha256"]):
                errors.append(f"{label}: missing valid content_sha256")

    contradictions = data.get("contradictions")
    if isinstance(contradictions, dict):
        for row in contradictions.get("contradictions", []):
            label = f"contradiction {row.get('contradiction_id')}"
            ensure_ref(row.get("opened_event_id"), ids["events"], label, errors)
            ensure_ref(row.get("resolved_event_id"), ids["events"], label, errors)
            ensure_ref(row.get("resolution_source_ref"), ids["authority"], label, errors)
            ensure_refs(row.get("dependent_action_refs"), ids["actions"], label, errors)
            for claim in row.get("conflicting_claims", []):
                ensure_ref(claim.get("claim_ref"), ids["tool_results"], label, errors)
                ensure_ref(claim.get("authority_ref"), ids["authority"], label, errors)
                ensure_ref(claim.get("temporal_validity_ref"), ids["temporal"], label, errors)

    authority = data.get("authority")
    if isinstance(authority, dict):
        for row in authority.get("authority_refs", []):
            ensure_ref(row.get("source_event_id"), ids["events"], f"authority {row.get('authority_id')}", errors)

    temporal = data.get("temporal")
    if isinstance(temporal, dict):
        for row in temporal.get("temporal_refs", []):
            label = f"temporal {row.get('temporal_id')}"
            ensure_ref(row.get("valid_from_event_id"), ids["events"], label, errors)
            ensure_ref(row.get("valid_until_event_id"), ids["events"], label, errors)

    environment = data.get("environment")
    if isinstance(environment, dict):
        for row in environment.get("snapshots", []):
            label = f"environment {row.get('snapshot_id')}"
            ensure_ref(row.get("captured_event_id"), ids["events"], label, errors)
            ensure_refs(row.get("related_event_ids"), ids["events"], label, errors)
            for hash_field in ("config_sha256", "note_sha256"):
                if hash_field in row and not SHA256_RE.match(str(row[hash_field])):
                    errors.append(f"{label}: invalid {hash_field}")

    for row in data["recovery_trace"]:
        label = f"recovery {row.get('recovery_event_id')}"
        ensure_ref(row.get("event_id"), ids["events"], label, errors)
        ensure_ref(row.get("trigger_action_ref"), ids["actions"], label, errors)
        ensure_ref(row.get("trigger_result_ref"), ids["tool_results"], label, errors)
        ensure_refs(row.get("pre_state_refs"), ids["environment"], label, errors)
        ensure_refs(row.get("post_state_refs"), ids["environment"], label, errors)
        ensure_ref(row.get("next_action_ref"), ids["actions"], label, errors)


def check_probes(proof_dir: Path, all_ids: set[str], errors: list[str]) -> None:
    path = proof_dir / "probe_set.md"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"probe_set.md: cannot read: {exc}")
        return

    for probe_id in PROBE_IDS:
        if f"## {probe_id} " not in text:
            errors.append(f"probe_set.md: missing {probe_id}")

    for artifact_ref in ARTIFACT_REF_RE.findall(text):
        if not (proof_dir / artifact_ref).is_file():
            errors.append(f"probe_set.md: unresolved artifact ref {artifact_ref}")

    for ref in ID_REF_RE.findall(text):
        if ref not in all_ids:
            errors.append(f"probe_set.md: unresolved fixture ref {ref}")


def check_provenance(proof_dir: Path, provenance: Any, errors: list[str]) -> None:
    if not isinstance(provenance, dict):
        errors.append("provenance_manifest: expected object")
        return
    artifact_hashes = provenance.get("artifact_hashes")
    if not isinstance(artifact_hashes, dict) or not artifact_hashes:
        errors.append("provenance_manifest: missing artifact_hashes")
        return
    required_hash_files = [
        relative
        for relative in REQUIRED_FIXTURE_FILES
        if relative != "fixture/provenance_manifest.json"
    ]
    for relative in required_hash_files:
        expected = artifact_hashes.get(relative)
        if not isinstance(expected, str) or not SHA256_RE.match(expected):
            errors.append(f"provenance_manifest: missing valid hash for {relative}")
            continue
        actual = sha256_file(proof_dir / relative)
        if actual != expected:
            errors.append(f"provenance_manifest: hash mismatch for {relative}")


def validate_fixture(proof_dir: Path) -> list[str]:
    if not proof_dir.is_absolute():
        proof_dir = ROOT / proof_dir
    errors: list[str] = []
    check_required_files(proof_dir, errors)
    if errors:
        return errors

    data = load_fixture_data(proof_dir, errors)
    if errors:
        return errors

    ids = build_id_sets(data, errors)
    check_refs(data, ids, errors)
    all_ids = set().union(*ids.values())
    check_probes(proof_dir, all_ids, errors)
    check_provenance(proof_dir, data.get("provenance"), errors)
    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_survivable_lineage_fixture.py <proof_dir>", file=sys.stderr)
        return 2

    errors = validate_fixture(Path(argv[1]))
    if errors:
        print("SURVIVABLE_LINEAGE_FIXTURE_INVALID")
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("SURVIVABLE_LINEAGE_FIXTURE_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
