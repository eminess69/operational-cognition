# Candidate Selection Policy

## Allowed Candidate Types

Proof 011 may use only one of the following candidate classes.

### Fully Public Trace

The source trace may be selected if all source material is public before inclusion:

- public issue
- public pull request
- public CI log
- public replay artifact
- public trajectory
- public bug report
- public agent trace

Public availability alone is not sufficient. The selected source must also contain enough lineage to map into the Proof 009 fixture fields and must not require target-system private internals to interpret the result.

### Redacted-Real Local Trace

The source trace may be selected if it was created by the operator and has been redacted before commit. It must contain no credentials, no private client data, no private substrate internals, and no target-system private internals.

## Current Candidate State

No safe candidate has been selected. The framework therefore records:

- `candidate_status`: `not_selected`
- `candidate_type`: `none`
- `eligible_for_execution`: `false`

## Selection Requirements

A candidate can move from `not_selected` to `selected` only when the source description and source references are sufficient for review. It can move to `eligible` only when all required lineage categories are present, redaction is complete, provenance is established, and the candidate can support both visible-only and full-lineage replay modes.

## Rejection Rule

Incomplete or ambiguous candidates fail closed. If the evidence cannot establish provenance, cannot separate visible-only from full-lineage replay, or cannot preserve the public/private boundary, the candidate status must be `rejected` or remain `not_selected`.

## Non-Fabrication Rule

No real trace may be fabricated to satisfy this proof. Synthetic examples belong in Proof 009; Proof 011 is only for candidate preparation.
