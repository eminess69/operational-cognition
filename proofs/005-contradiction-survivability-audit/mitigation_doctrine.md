# Contradiction Survivability Doctrine

This doctrine defines public, implementation-neutral practices for preserving contradictions and uncertainty through compression, replay, memory promotion, and operational reconstruction. It does not expose private implementation details or target-system internals.

## Compression can reduce contradiction visibility

Compression should be treated as a lossy evidence transformation unless it preserves source refs, omitted ranges, contradiction refs, uncertainty markers, and temporal validity metadata. A shorter context can remain operationally useful while becoming less reliable as a contradiction record.

## Replay without ambiguity retention can distort operational reconstruction

Replay surfaces should avoid implying that a visible sequence is a complete causal explanation. Replay artifacts are stronger when they preserve ambiguity markers, omitted ranges, source authority, tool/action provenance, memory state, and uncertainty boundaries.

## Contradiction lineage matters for causal replay

Operational reconstruction should preserve where a contradiction entered, which evidence supported each side, whether it was resolved, and what later actions depended on it. Without contradiction lineage, a later replay can explain what happened while losing why the evidence state was contested.

## Operational cognition requires uncertainty survivability

Long-horizon systems need durable uncertainty boundaries. Unknowns, caveats, stale assumptions, rejected alternatives, and unresolved conflicts should survive context compression as first-class metadata rather than prose that can be simplified away.

## Public proofs require contradiction preservation

Public operational proofs should identify which claims are observed, inferred, hypothesis-level, or unresolved. Evidence-backed findings should cite source refs and preserve contradiction or uncertainty markers instead of silently converting ambiguity into a clean narrative.

## Candidate Contradiction-Preserving Metadata

- contradiction refs
- rejected-alternative refs
- source authority refs
- temporal validity refs
- uncertainty markers
- omitted-range refs
- stale-assumption refs

## Conservative Use Rules

- do not treat a summary as contradiction-preserving unless source refs and omitted ranges remain recoverable
- do not treat visible replay as causal replay unless ambiguity and provenance survive
- do not promote memory-derived claims without source authority and temporal validity boundaries
- do not collapse observed evidence, inference, hypothesis, and unresolved questions into a single claim type
- do not publish raw internal consultation responses or private implementation details
