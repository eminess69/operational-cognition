#!/usr/bin/env python3
"""Score Proof 017 blind-pack key reconstruction without reading narrative claims."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_json(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def score_case(submitted: list[str], expected: list[str]) -> dict:
    submitted_set = set(submitted)
    expected_set = set(expected)
    reconstructed = sorted(submitted_set & expected_set)
    missing = sorted(expected_set - submitted_set)
    extra = sorted(submitted_set - expected_set)
    return {
        "reconstructed": len(reconstructed),
        "missing": len(missing),
        "extra": len(extra),
        "reconstructed_keys": reconstructed,
        "missing_keys": missing,
        "extra_keys": extra,
    }


def main() -> int:
    inputs = load_json("blind_inputs.json")
    hidden = load_json("blind_expected_hidden.json")
    hidden_by_case = {case["case_id"]: case["expected_reconstruction_keys"] for case in hidden["cases"]}
    results = []
    totals = {
        "baseline_reconstructed": 0,
        "pond_reconstructed": 0,
        "delta": 0,
    }
    for case in inputs["cases"]:
        expected = hidden_by_case[case["case_id"]]
        baseline = score_case(case["baseline_submission_keys"], expected)
        pond = score_case(case["pond_backed_submission_keys"], expected)
        delta = pond["reconstructed"] - baseline["reconstructed"]
        totals["baseline_reconstructed"] += baseline["reconstructed"]
        totals["pond_reconstructed"] += pond["reconstructed"]
        totals["delta"] += delta
        results.append(
            {
                "case_id": case["case_id"],
                "baseline": baseline,
                "pond_backed": pond,
                "delta": delta,
            }
        )
    output = {
        "proof_id": "017-entropy-replication-gauntlet",
        "scoring_input_kind": inputs["scoring_input_kind"],
        "narrative_claims_read": False,
        "case_results": results,
        "totals": totals,
        "verdict": "BLIND_RECONSTRUCTION_DELTA_OBSERVED" if totals["delta"] > 0 else "NO_BLIND_RECONSTRUCTION_DELTA",
    }
    (HERE / "blind_results.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output["verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

