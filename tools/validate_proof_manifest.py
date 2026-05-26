#!/usr/bin/env python3
"""Validate an Operational Cognition proof manifest."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "proof_manifest.schema.json"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def type_name(value: Any) -> str:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    if isinstance(value, str):
        return "string"
    if isinstance(value, int) and not isinstance(value, bool):
        return "integer"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return "number"
    if value is None:
        return "null"
    return type(value).__name__


def validate_node(value: Any, schema: dict[str, Any], path: str, errors: list[str]) -> None:
    expected_type = schema.get("type")
    if expected_type and type_name(value) != expected_type:
        errors.append(f"{path}: expected {expected_type}, got {type_name(value)}")
        return

    if "enum" in schema and value not in schema["enum"]:
        allowed = ", ".join(str(item) for item in schema["enum"])
        errors.append(f"{path}: expected one of {allowed}")

    if isinstance(value, str):
        min_length = schema.get("minLength")
        if min_length is not None and len(value) < min_length:
            errors.append(f"{path}: shorter than minLength {min_length}")

    if isinstance(value, list):
        min_items = schema.get("minItems")
        if min_items is not None and len(value) < min_items:
            errors.append(f"{path}: fewer than minItems {min_items}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                validate_node(item, item_schema, f"{path}[{index}]", errors)

    if isinstance(value, dict):
        required = schema.get("required", [])
        for field in required:
            if field not in value:
                errors.append(f"{path}: missing required field {field}")

        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            allowed = set(properties)
            for field in value:
                if field not in allowed:
                    errors.append(f"{path}: unexpected field {field}")

        for field, field_schema in properties.items():
            if field in value:
                validate_node(value[field], field_schema, f"{path}.{field}", errors)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_proof_manifest.py <proof_manifest.json>", file=sys.stderr)
        return 2

    manifest_path = Path(argv[1])
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path

    try:
        schema = load_json(SCHEMA_PATH)
        manifest = load_json(manifest_path)
    except (OSError, json.JSONDecodeError) as exc:
        print("PROOF_MANIFEST_INVALID")
        print(str(exc), file=sys.stderr)
        return 1

    errors: list[str] = []
    validate_node(manifest, schema, "$", errors)

    if errors:
        print("PROOF_MANIFEST_INVALID")
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("PROOF_MANIFEST_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
