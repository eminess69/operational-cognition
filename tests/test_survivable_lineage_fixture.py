from __future__ import annotations

import json
import shutil
from pathlib import Path

from tools.validate_survivable_lineage_fixture import validate_fixture


ROOT = Path(__file__).resolve().parents[1]
PROOF_DIR = ROOT / "proofs" / "009-survivable-lineage-fixture"


def copy_fixture(tmp_path: Path) -> Path:
    destination = tmp_path / "proof-009-copy"
    shutil.copytree(PROOF_DIR, destination)
    return destination


def test_valid_fixture_passes() -> None:
    assert validate_fixture(PROOF_DIR) == []


def test_missing_artifact_fails(tmp_path: Path) -> None:
    proof_dir = copy_fixture(tmp_path)
    (proof_dir / "fixture" / "events.jsonl").unlink()

    errors = validate_fixture(proof_dir)

    assert any("missing required artifact: fixture/events.jsonl" in error for error in errors)


def test_malformed_jsonl_fails(tmp_path: Path) -> None:
    proof_dir = copy_fixture(tmp_path)
    transcript = proof_dir / "fixture" / "transcript.jsonl"
    transcript.write_text(transcript.read_text(encoding="utf-8") + "{not-json\n", encoding="utf-8")

    errors = validate_fixture(proof_dir)

    assert any("invalid JSONL" in error for error in errors)


def test_unresolved_probe_refs_fail(tmp_path: Path) -> None:
    proof_dir = copy_fixture(tmp_path)
    probe_set = proof_dir / "probe_set.md"
    probe_set.write_text(
        probe_set.read_text(encoding="utf-8").replace("`TR-002`", "`TR-999`", 1),
        encoding="utf-8",
    )

    errors = validate_fixture(proof_dir)

    assert any("unresolved fixture ref TR-999" in error for error in errors)


def test_provenance_hashes_exist() -> None:
    provenance_path = PROOF_DIR / "fixture" / "provenance_manifest.json"
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))

    artifact_hashes = provenance["artifact_hashes"]

    assert artifact_hashes
    assert "fixture/transcript.jsonl" in artifact_hashes
    assert all(len(value) == 64 for value in artifact_hashes.values())
