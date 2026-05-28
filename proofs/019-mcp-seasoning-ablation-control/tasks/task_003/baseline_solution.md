# Baseline Solution: Partial Provenance Recovery

Visible-only solution. No pond-backed consult or candidate refs were used.

        ## Decision

        Recover enough provenance to restore safe configuration first, then separate actor certainty from recovery certainty. Do not infer a definitive actor from an edited approval comment.

        ## Authority Order

        1. Immutable deploy log and repository object IDs.
        2. Backup snapshot, adjusted for stale timestamp limits.
        3. Ticket approval history, with edited fields treated as conditional.
        4. Human recollection and compliance requests.

        ## Plan

        1. Preserve the automation-account deploy record, ticket history, backup snapshot, observability tags, and mirror gap metadata.
        2. Reconstruct the missing two commits from primary repository refs or deployment artifact hashes.
        3. Restore the last known safe config only if the snapshot can be tied to the deploy window; otherwise create a reviewed patch from current service owner input.
        4. Report actor attribution as unresolved unless immutable evidence links the human approval to the automation execution.

        ## Uncertainty and Recovery

        The edited approval and mirror gap remain open. The recovery claim can be bounded to config state and evidence custody without assigning intent.
