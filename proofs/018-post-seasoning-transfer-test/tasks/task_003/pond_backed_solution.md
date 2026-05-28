# Pond-backed Solution

Mode: pond-backed operational solving with MCP-seasoned first-principles candidates available as bounded guidance.

The consult response for this task was `inside_voice_consults/task_003_pond_response.json`. It returned `adapter_status: pond_backed`, empty `gate_failures`, runtime hashes, and these visible MCP-seasoned refs:

- `artifacts/pond/mcp_seasoned_first_principles_admitted.jsonl#49`
- `artifacts/pond/mcp_seasoned_reusable_lineage_candidates.jsonl#49`
- `artifacts/pond/mcp_seasoned_first_principles_admitted.jsonl#19`

## Decision

Choose Design B.

Design A is rejected because endpoint expansion is outside the allowed surface for this proof. Design B keeps the runtime stable, preserves replayable response artifacts, and classifies the log gap directly.

## Arbitration Steps

1. Define the invariant.
   The proof must demonstrate whether refs are visible without expanding the endpoint and without treating candidate guidance as promoted reusable lineage.

2. Test the cheapest bypass.
   A surface-valid report that says "runtime visible" while only response artifacts expose detailed refs violates the invariant. The report must use the narrower classification `RESPONSE_VISIBLE_LOG_NOT_VERBOSE`.

3. Preserve replay evidence.
   Each response has stable runtime request and response hashes. The runtime log can be matched by those hashes even though it omits detailed retrieved refs.

4. Rank authority.
   The stable runtime contract controls endpoint behavior. The proof-local visibility report controls how the observed gap is classified. Response JSON controls which candidate refs were available to the task.

5. Reject forbidden implementation work.
   Do not add fields to the runtime log, do not create a new endpoint, and do not mutate the reusable pool. The transfer test evaluates current runtime behavior.

6. State the bounded outcome.
   The architecture decision supports a valid proof only if response-visible refs satisfy the transfer-test visibility requirement and the log limitation is reported as a limitation.

## Why This Differs From Baseline

The pond-backed decision adds an invariant check for a surface-valid but misleading visibility claim, and it ties replayability to stable hashes rather than to log verbosity alone.
