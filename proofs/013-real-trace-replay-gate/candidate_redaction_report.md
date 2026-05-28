# Candidate Redaction Report

## Redaction Decision

The candidate is a redacted-real local operational trace. Redaction is complete.

## Material Included

- visible task/correction transcript summaries
- deterministic event ids
- public-safe tool/action summaries
- command result summaries and hashes
- local environment refs needed for replay
- pond-backed Inside Voice response hashes and pressure ids

## Material Excluded

- hidden chain-of-thought
- private substrate internals
- credentials or secrets
- raw private implementation state
- target-system private internals
- obsolete fail-closed payload duplication not needed for replay

## Secret Scan

The fixture does not contain credential-like material. The validator scans fixture and proof text for banned secret terms.

## Boundary

Local paths are retained only as environment refs because the proof needs to reconstruct which workspace and Belief Ledger checkout were used. They are not used to infer private substrate behavior.
