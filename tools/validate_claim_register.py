#!/usr/bin/env python3
"""Validate a public claim register for an Operational Cognition proof."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

ALLOWED_CLAIM_LEVELS = {"observed", "inferred", "hypothesis", "unresolved"}
TOP_LEVEL_KEYS = {"analysis_id", "claims", "proof_id"}
CLAIM_KEYS = {
    "appears_in",
    "claim",
    "claim_id",
    "claim_level",
    "evidence_refs",
    "risk_if_overstated",
    "safe_public_wording",
}
DISALLOWED_PATTERNS = {
    "AGI": re.compile(r"\bAGI\b", re.IGNORECASE),
    "consciousness": re.compile(r"\bconsciousness\b", re.IGNORECASE),
    "superintelligence": re.compile(r"\bsuperintelligence\b", re.IGNORECASE),
    "black_box_solved": re.compile(r"\bblack[_ -]?box[_ -]?solved\b", re.IGNORECASE),
    "substrate_disclosure": re.compile(r"\bsubstrate[_ -]?disclosure\b", re.IGNORECASE),
    "hidden_chain_of_thought": re.compile(
        r"\bhidden[_ -]?chain(?:[_ -]?of)?[_ -]?thought\b", re.IGNORECASE
    ),
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def evidence_ids(evidence_manifest: Any) -> set[str]:
    if not isinstance(evidence_manifest, dict):
        return set()
    sources = evidence_manifest.get("sources")
    if not isinstance(sources, list):
        return set()
    return {source.get("id") for source in sources if isinstance(source, dict) and source.get("id")}


def iter_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        strings: list[str] = []
        for item in value:
            strings.extend(iter_strings(item))
        return strings
    if isinstance(value, dict):
        strings = []
        for item in value.values():
            strings.extend(iter_strings(item))
        return strings
    return []


def validate_disallowed_text(value: Any, path: str, errors: list[str]) -> None:
    for text in iter_strings(value):
        for label, pattern in DISALLOWED_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{path}: disallowed claim text {label}")


def validate_string_list(value: Any, path: str, errors: list[str], *, allow_empty: bool) -> None:
    if not isinstance(value, list):
        errors.append(f"{path}: expected array")
        return
    if not allow_empty and not value:
        errors.append(f"{path}: expected non-empty array")
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item:
            errors.append(f"{path}[{index}]: expected non-empty string")


def validate_claim(
    claim: Any,
    index: int,
    known_evidence_ids: set[str],
    seen_ids: set[str],
    errors: list[str],
) -> None:
    path = f"$.claims[{index}]"
    if not isinstance(claim, dict):
        errors.append(f"{path}: expected object")
        return

    missing = CLAIM_KEYS - set(claim)
    unexpected = set(claim) - CLAIM_KEYS
    for field in sorted(missing):
        errors.append(f"{path}: missing required field {field}")
    for field in sorted(unexpected):
        errors.append(f"{path}: unexpected field {field}")
    if missing:
        return

    claim_id = claim.get("claim_id")
    if not isinstance(claim_id, str) or not claim_id:
        errors.append(f"{path}.claim_id: expected non-empty string")
    elif claim_id in seen_ids:
        errors.append(f"{path}.claim_id: duplicate claim ID {claim_id}")
    else:
        seen_ids.add(claim_id)

    if claim.get("claim_level") not in ALLOWED_CLAIM_LEVELS:
        errors.append(f"{path}.claim_level: expected one of {sorted(ALLOWED_CLAIM_LEVELS)}")

    for field in ("claim", "risk_if_overstated", "safe_public_wording"):
        if not isinstance(claim.get(field), str) or not claim[field]:
            errors.append(f"{path}.{field}: expected non-empty string")

    validate_string_list(claim.get("appears_in"), f"{path}.appears_in", errors, allow_empty=False)
    validate_string_list(claim.get("evidence_refs"), f"{path}.evidence_refs", errors, allow_empty=True)

    evidence_refs = claim.get("evidence_refs")
    if isinstance(evidence_refs, list):
        for ref in evidence_refs:
            if isinstance(ref, str) and ref not in known_evidence_ids:
                errors.append(f"{path}.evidence_refs: unknown evidence_ref {ref}")

    claim_level = claim.get("claim_level")
    if claim_level == "observed" and not evidence_refs:
        errors.append(f"{path}.evidence_refs: observed claims require evidence_refs")
    if claim_level == "inferred":
        if not evidence_refs:
            errors.append(f"{path}.evidence_refs: inferred claims require evidence_refs")
        if not claim.get("safe_public_wording"):
            errors.append(f"{path}.safe_public_wording: inferred claims require safe_public_wording")

    validate_disallowed_text(claim, path, errors)


def validate_register_data(register: Any, evidence_manifest: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(register, dict):
        return ["$: expected object"]

    missing = TOP_LEVEL_KEYS - set(register)
    unexpected = set(register) - TOP_LEVEL_KEYS
    for field in sorted(missing):
        errors.append(f"$: missing required field {field}")
    for field in sorted(unexpected):
        errors.append(f"$: unexpected field {field}")
    if missing:
        return errors

    for field in ("proof_id", "analysis_id"):
        if not isinstance(register.get(field), str) or not register[field]:
            errors.append(f"$.{field}: expected non-empty string")

    claims = register.get("claims")
    if not isinstance(claims, list) or not claims:
        errors.append("$.claims: expected non-empty array")
        return errors

    known_evidence_ids = evidence_ids(evidence_manifest)
    seen_ids: set[str] = set()
    for index, claim in enumerate(claims):
        validate_claim(claim, index, known_evidence_ids, seen_ids, errors)

    return errors


def validate_register(register_path: Path, evidence_manifest_path: Path) -> list[str]:
    try:
        register = load_json(register_path)
        evidence_manifest = load_json(evidence_manifest_path)
    except (OSError, json.JSONDecodeError) as exc:
        return [str(exc)]
    return validate_register_data(register, evidence_manifest)


def resolve_path(path_arg: str) -> Path:
    path = Path(path_arg)
    if not path.is_absolute():
        path = ROOT / path
    return path


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "usage: validate_claim_register.py <claim_register.json> <evidence_manifest.json>",
            file=sys.stderr,
        )
        return 2

    errors = validate_register(resolve_path(argv[1]), resolve_path(argv[2]))
    if errors:
        print("CLAIM_REGISTER_INVALID")
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("CLAIM_REGISTER_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
