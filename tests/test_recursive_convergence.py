from __future__ import annotations

import json
import shutil
from pathlib import Path

from tools.validate_recursive_convergence import validate_recursive_convergence


ROOT = Path(__file__).resolve().parents[1]
PROOF_DIR = ROOT / "proofs" / "012-recursive-convergence-proof-run"


def copy_proof(tmp_path: Path) -> Path:
    destination = tmp_path / "proof-012-copy"
    shutil.copytree(PROOF_DIR, destination)
    return destination


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def test_valid_proof_passes() -> None:
    assert validate_recursive_convergence(PROOF_DIR) == []


def test_fewer_than_seven_passes_fails(tmp_path: Path) -> None:
    proof_dir = copy_proof(tmp_path)
    log_path = proof_dir / "recursive_depth_log.jsonl"
    lines = log_path.read_text(encoding="utf-8").splitlines()
    log_path.write_text("\n".join(lines[:6]) + "\n", encoding="utf-8")

    errors = validate_recursive_convergence(proof_dir)

    assert any("expected at least 7 passes" in error for error in errors)


def test_global_proof_claim_fails(tmp_path: Path) -> None:
    proof_dir = copy_proof(tmp_path)
    readme_path = proof_dir / "README.md"
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8")
        + "\nProof 010 validates survivable lineage globally.\n",
        encoding="utf-8",
    )

    errors = validate_recursive_convergence(proof_dir)

    assert any("forbidden public assertion" in error for error in errors)


def test_hidden_private_phrase_fails(tmp_path: Path) -> None:
    proof_dir = copy_proof(tmp_path)
    readme_path = proof_dir / "README.md"
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8")
        + "\nhidden chain-of-thought\n",
        encoding="utf-8",
    )

    errors = validate_recursive_convergence(proof_dir)

    assert any("private marker appears" in error for error in errors)


def test_missing_limitation_fails(tmp_path: Path) -> None:
    proof_dir = copy_proof(tmp_path)
    laws_path = proof_dir / "surviving_laws.md"
    laws = laws_path.read_text(encoding="utf-8").replace("Limitation:", "Boundary:", 1)
    laws_path.write_text(laws, encoding="utf-8")

    errors = validate_recursive_convergence(proof_dir)

    assert any("missing limitation" in error for error in errors)


def test_invalid_verdict_fails(tmp_path: Path) -> None:
    proof_dir = copy_proof(tmp_path)
    verdict_path = proof_dir / "final_convergence_verdict.json"
    verdict = load_json(verdict_path)
    verdict["verdict"] = "CONVERGENCE_CERTAIN"
    write_json(verdict_path, verdict)

    errors = validate_recursive_convergence(proof_dir)

    assert any("final_convergence_verdict.json.verdict: invalid" in error for error in errors)


def test_missing_next_validation_fails(tmp_path: Path) -> None:
    proof_dir = copy_proof(tmp_path)
    laws_path = proof_dir / "surviving_laws.md"
    laws = laws_path.read_text(encoding="utf-8").replace(
        "Next validation needed:",
        "Validation pending:",
        1,
    )
    laws_path.write_text(laws, encoding="utf-8")

    errors = validate_recursive_convergence(proof_dir)

    assert any("missing next validation needed" in error for error in errors)
