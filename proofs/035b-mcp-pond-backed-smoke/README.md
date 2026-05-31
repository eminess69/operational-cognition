# Proof 035b - MCP Pond-Backed Smoke

This is an instrument smoke proof, not a cognition proof.

## Result

- Positive consult classified as: POND_BACKED
- Positive consult has motifs: True
- Positive consult has lineages: True
- Positive consult has lineage hashes: True
- Unsupported consult failed closed: True

## Validator

```bash
python3 tools/validate_mcp_consults.py proofs/035b-mcp-pond-backed-smoke/consult_log.jsonl --require-lineage --require-motifs
```

`consult_log.jsonl` intentionally contains only successful pond-backed recall rows. Unsupported recall is recorded separately in `negative_consult_log.jsonl` because fail-closed rows are not positive proof evidence.
