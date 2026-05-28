# Seasoned Solution: Partial Provenance Recovery

The consult response was `inside_voice_consults/task_003_seasoned_response.json`. It returned `adapter_status: pond_backed`, empty `gate_failures`, pressure rankings `pressure:7ba41d8ba5ef3698`, `pressure:44eeb320a80c1c5f`, `pressure:cf4e82e380cf1a94`, and runtime hashes corpus `9dc990b92a07a9c77beafae5036894225983ce47f5fd2c6650266d29afc81b15`, request `fe62f838ce98b7ed2cde576c3b14172cdf287380c18c840746686e58f1d4038b`, response `06d3b3fdfd4b13668ea95e0b549991fe0d0d35bd7388db1607c4a89328b282a3`.

Visible MCP-seasoned refs used as bounded guidance:

- `request_visible_ref:proofs/018-post-seasoning-transfer-test/mcp_seasoned_visibility_report.json`
- `artifacts/pond/mcp_seasoned_first_principles_admitted.jsonl#21`
- `artifacts/pond/mcp_seasoned_first_principles_admitted.jsonl#49`


        ## Operational Plan

        1. Preserve immutable evidence first: deployment log, repository object IDs, artifact hashes, backup snapshot, ticket edit history, and observability tags.
        2. Separate recovery-safe provenance from actor attribution. Recovery only needs a bounded chain from config state to deploy artifact; compliance attribution needs stronger evidence.
        3. Rebuild the missing mirror commits from the primary repository or deployment artifact hash. If not possible, mark the gap and use a reviewed repair commit.
        4. Treat edited approval as a conditional authority. It can support timeline reconstruction but cannot prove who caused the change.
        5. Restore or patch only after the config state is tied to a replayable artifact; document unresolved actor certainty separately.


## Boundary

The candidate refs are advisory and local to this held-out task. The solution preserves uncertainty, does not mutate the reusable lineage pool, and keeps the result bounded to operational planning under the provided evidence.
