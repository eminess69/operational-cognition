from __future__ import annotations

import copy
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import build_evidence_manifest as builder  # noqa: E402
from tools import validate_evidence_manifest as validator  # noqa: E402


MANIFEST_PATH = ROOT / "proofs" / "001-agent-continuity-audit" / "evidence_manifest.json"


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_manifest_validates() -> None:
    assert validator.validate_manifest(MANIFEST_PATH) == []


def test_hashes_stable() -> None:
    assert builder.stable_content_hash("alpha   beta\n gamma") == builder.stable_content_hash(
        "alpha beta gamma"
    )


def test_ordering_deterministic() -> None:
    manifest = load_manifest()
    ids = [source["id"] for source in manifest["sources"]]
    assert ids == sorted(ids)


def test_duplicate_ids_rejected() -> None:
    manifest = load_manifest()
    mutated = copy.deepcopy(manifest)
    mutated["sources"][1]["id"] = mutated["sources"][0]["id"]

    errors = validator.validate_manifest_data(mutated, MANIFEST_PATH.parent)

    assert any("duplicate source id" in error for error in errors)


def test_missing_snapshot_fails() -> None:
    manifest = load_manifest()
    mutated = copy.deepcopy(manifest)
    mutated["sources"][0]["snapshot_path"] = "evidence/snapshots/does-not-exist.json"

    errors = validator.validate_manifest_data(mutated, MANIFEST_PATH.parent)

    assert any("missing snapshot file" in error for error in errors)


def test_malformed_source_rejected() -> None:
    manifest = load_manifest()
    mutated = copy.deepcopy(manifest)
    del mutated["sources"][0]["url"]

    errors = validator.validate_manifest_data(mutated, MANIFEST_PATH.parent)

    assert any("missing required field url" in error for error in errors)
