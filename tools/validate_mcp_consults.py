#!/usr/bin/env python3
"""Validate MCP consult artifacts against the pond-backed proof boundary."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from operational_cognition.mcp.proof_gate import MCPConsultBoundaryError, assert_pond_backed_consult


def load_consults(path: Path) -> list[tuple[int, dict[str, Any]]]:
    if path.suffix == ".json":
        return [(1, json.loads(path.read_text(encoding="utf-8")))]

    rows: list[tuple[int, dict[str, Any]]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        rows.append((line_number, json.loads(line)))
    return rows


def validate_paths(paths: list[Path], *, require_lineage: bool, require_motifs: bool) -> list[str]:
    errors: list[str] = []
    for path in paths:
        if not path.exists():
            errors.append(f"{path}: missing consult artifact")
            continue
        try:
            rows = load_consults(path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path}: cannot read consult artifact: {exc}")
            continue
        if not rows:
            errors.append(f"{path}: no consult rows found")
            continue
        for line_number, row in rows:
            try:
                assert_pond_backed_consult(
                    row,
                    require_lineage=require_lineage,
                    require_motifs=require_motifs,
                )
            except MCPConsultBoundaryError as exc:
                errors.append(f"{path}:{line_number}: {exc}")
    return errors


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="MCP consult .jsonl or .json artifacts")
    parser.add_argument("--require-lineage", action="store_true", help="Require lineage hashes or refs")
    parser.add_argument("--require-motifs", action="store_true", help="Require returned/recalled/activated motifs")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    errors = validate_paths(
        args.paths,
        require_lineage=args.require_lineage,
        require_motifs=args.require_motifs,
    )
    if errors:
        print("MCP_CONSULTS_INVALID")
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("MCP_CONSULTS_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
