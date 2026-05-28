# Baseline Solution: Degraded Validation Pipeline Triage

Visible-only solution. No pond-backed consult or candidate refs were used.

        ## Decision

        Hold release until the failed shard logs and smoke-gate coverage can be replayed. Treat the green rerun as a newer signal, not as authority to erase the earlier failures.

        ## Authority Order

        1. Reproducible validation artifacts with timestamps and shard IDs.
        2. Release policy and rollback capacity confirmation.
        3. Owner statements, only when tied to an artifact or explicit capacity commitment.

        ## Plan

        1. Freeze the dependency update at the candidate build and collect the failed shard logs, rerun summary, linter output, smoke-gate coverage, and cache eviction window.
        2. Re-run only the missing smoke coverage and the two failed shards with cache state pinned. Stop if either shard fails or cannot be replayed.
        3. Ask rollback owner for written capacity before the support freeze. Stop if rollback cannot be staffed.
        4. If replay passes and rollback is staffed, ship behind a narrow flag; otherwise defer.

        ## Uncertainty and Recovery

        The missing cache-eviction range remains unresolved. If it cannot be recovered, the plan must record that the release decision depends on partial evidence and prefer deferment over silent acceptance.
