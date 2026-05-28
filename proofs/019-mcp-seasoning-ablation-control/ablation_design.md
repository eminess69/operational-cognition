# Ablation Design

## Modes

Mode A, baseline, uses only visible task text. It does not use pond-backed consults, pressure rankings, runtime hashes, or candidate refs.

Mode B, seasoned, calls `/consult` through the live Belief Ledger MCP server at `http://127.0.0.1:8766` with MCP-seasoned first-principles candidate recall enabled.

Mode C, ablated, uses the same pond-backed Belief Ledger runtime but removes only the seasoned candidate source specs before recall. Ordinary replay, contradiction, authority, unresolved-tension, claim-pressure, proof, and doctrine sources remain available.

## Disabled Sources In Mode C

The ablated runtime excludes the seasoned candidate source family and the seasoning summary source before recall. It keeps reusable lineage fragments, pattern overlap clusters, claim-pressure records, proof corpora, continuity arbitration, epistemic gaps, and doctrine docs.

## Validity Cautions

Ablation is valid only if the ablated response exposes no MCP-seasoned candidate refs while retaining runtime hashes and pressure rankings. If candidate refs appear in ablated response artifacts, the verdict must become `INVALID_ABLATION_TEST`.

## Claim Boundary

This design tests local transfer under a bounded replay condition. It does not promote candidates, mutate the reusable lineage pool, or support broader capability claims.
