# Pond-Backed Consult Contract

`/consult` responses that claim pond-backed behavior must return real recall artifacts from pond memory/state. Placeholder, mock, scaffold, or generic request-echo responses are invalid for proof evidence.

## Required Success Shape

```json
{
  "adapter_status": "pond_backed",
  "verdict": "ok",
  "response_source": "inside_voice_pond",
  "returned_motifs": [],
  "returned_lineages": [],
  "lineage_hashes": [],
  "recall_summary": "",
  "fail_closed_reason": null
}
```

Additional public-safe fields such as `request_id`, `mode`, `summary`, `findings`, `recommendations`, `uncertainty`, `lineage`, and `lineage_payloads` may be present.

## Hard Requirements

- `returned_lineages` must contain traceable pond records.
- `lineage_hashes` must hash actual lineage payloads from those pond records.
- `returned_motifs` must come from pond memory/state, not static placeholder text.
- Empty recall is allowed only with `verdict="fail_closed"` and a non-empty `fail_closed_reason`.
- If the pond is unavailable, `/consult` must return:

```json
{
  "adapter_status": "error",
  "verdict": "fail_closed",
  "fail_closed_reason": "pond_unavailable"
}
```

## Proof Gate

Any proof claiming pond-backed MCP behavior must pass:

```bash
python3 tools/validate_mcp_consults.py <proof>/mcp/*.jsonl --require-lineage
```

Mechanism recall or mechanism discovery proofs must also pass:

```bash
python3 tools/validate_mcp_consults.py <proof>/mcp/*.jsonl --require-lineage --require-motifs
```

Fail-closed rows are valid adapter behavior, but they are not positive pond-backed evidence and must not be included in the validator target for successful recall evidence.
