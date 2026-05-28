# Baseline Solution: Conflicting Architecture Migration Plan

Visible-only solution. No pond-backed consult or candidate refs were used.

        ## Decision

        Choose a staged migration only after rollback, lineage, vendor, and capacity gates are refreshed. Do not treat council approval as sufficient while SRE and governance risks remain open.

        ## Authority Order

        1. Current security deadline and production rollback constraints.
        2. SRE failover evidence and capacity forecast.
        3. Architecture approval and prototype evidence.
        4. Procurement and governance readiness.

        ## Plan

        1. Refresh capacity using post-rollout traffic before selecting the migration window.
        2. Test dual-write failover lag with replay and rollback criteria. Stop if lag amplification recurs.
        3. Secure governance approval for lineage fields before production writes.
        4. Build a credential-expiry fallback: extend old credentials only if security accepts the residual risk, otherwise run read-only shadow traffic until broker contract is final.

        ## Uncertainty and Recovery

        The unsigned broker contract and stale traffic forecast are blockers for irreversible migration. The fallback is shadow mode plus credential-extension decision, not unbounded dual-write.
