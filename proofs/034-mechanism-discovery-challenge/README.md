# Proof 034 - Mechanism Discovery Challenge

## Objective

Proof 034 tests whether observation-only cases can produce ranked candidate pathways only after a mandatory consult step.

## Phase Boundary

The observation file contains only `case_id` and `observations`. Candidate generation is written after `mcp/discovery_consults.jsonl` exists, and candidate rows emit `candidate_pathways` only, with no final answer field.

## MCP Boundary

Proof 034 is currently classified as:

`INVALID_AS_POND_BACKED`

because MCP returned `placeholder`. It may remain as a scaffold proof only until the consult artifacts pass `tools/validate_mcp_consults.py` with lineage and motif requirements.

## Results

- Candidate diversity improved: True
- Baseline-eliminated pathways preserved: False
- Ranking quality improved: False
- Premature convergence reduced: True

## Hostile Verdict

WEAK_SIGNAL: diversity and single-candidate convergence improved inside the deterministic harness, but evidence-top preservation and ranking did not improve; the live adapter was not pond-backed in this run and local motif rules remain a full explanation.

The surviving claim is bounded: consult-first pathway generation improved diversity and reduced single-candidate convergence inside this deterministic harness. The proof does not establish independent open-world mechanism discovery.
