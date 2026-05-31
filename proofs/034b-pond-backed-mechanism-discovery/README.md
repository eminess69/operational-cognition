# Proof 034b - Pond-Backed Mechanism Discovery Challenge

Proof 034b reruns the Proof 034 observation-to-candidate challenge with the repaired pond-backed MCP consult path. It does not overwrite Proof 034.

## Boundary

Required MCP logs are validator-clean:

```bash
python3 tools/validate_mcp_consults.py proofs/034b-pond-backed-mechanism-discovery/mcp/discovery_consults.jsonl --require-lineage --require-motifs
python3 tools/validate_mcp_consults.py proofs/034b-pond-backed-mechanism-discovery/mcp/seasoning_log.jsonl --require-lineage --require-motifs
```

## Metrics

- No-pond valid candidate rate: 0.4333
- Generic-consult valid candidate rate: 0.7
- Pond-backed valid candidate rate: 0.7333
- No-pond premature single-candidate rate: 0.8182
- Pond-backed premature single-candidate rate: 0.9286

## Hostile Verdict

`STRONG_SIGNAL`

The surviving claim is bounded: pond-backed recall supplied traceable motifs and lineages before candidate generation and improved measured discovery behavior in this deterministic harness. Local deterministic scoring and generic-consult pressure remain partial explanations.
