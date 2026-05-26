# Redaction Policy

## Secrets and Credentials

Credentials, authentication material, session identifiers, signing keys, and access-bearing values must not be committed. Replace them with explicit redaction markers and record only the fact that redaction occurred.

## Local Paths

Local filesystem paths must be generalized unless the path is already public and necessary for replay. Preserve only path structure needed to map the trace into fixture fields.

## Personal Data

Personal names, email addresses, account identifiers, and other person-linked data must be removed or generalized unless the data is already intentionally public and required for provenance.

## Private Client Data

Client names, client artifacts, client source material, business data, and client-specific operational details must not be included. A redacted-real candidate that depends on client material is not eligible for this proof.

## Private Substrate Internals

Private substrate internals must not be disclosed. Public lineage should describe observable artifact boundaries, not internal substrate mechanisms.

## Target-System Private Internals

Do not include non-public target-system internals. The proof may cite public issue, PR, CI, replay, trajectory, or bug-report material, but it must not infer or expose private implementation details.

## Hashes and References

Use hashes, stable IDs, and public references to preserve provenance when raw material cannot be safely included. Hashes must not be used to imply that omitted content is known or stronger than the visible evidence permits.

## Unresolved Markers

Unknown, omitted, or redacted evidence must remain marked as unresolved. Redaction must not convert unknown evidence into stronger claims.
