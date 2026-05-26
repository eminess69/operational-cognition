# Operational Cognition Thesis

Operational Cognition investigates how long-horizon AI systems preserve or lose operational continuity through replay, compression, memory promotion, reconstruction, and recovery.

The repository focuses on:

- replayability
- continuity survivability
- operational reconstruction
- contradiction preservation
- memory authority
- evidence lineage
- bounded public proof generation

It does not claim:

- AGI
- consciousness
- mechanistic interpretability
- solved black-box understanding
- private substrate disclosure

## Why this matters

Modern long-horizon AI systems increasingly depend on:

- summarization
- memory systems
- replay tooling
- event systems
- compaction
- condensation
- recovery flows
- reconstruction tooling

These mechanisms are operationally useful. They allow systems to continue across long contexts, recover from context pressure, expose some visible history, and preserve selected state across sessions or compressed views.

They also introduce a harder audit problem. As systems scale across longer horizons, the distinction between visible replay, operational continuity, causal reconstruction, contradiction survivability, and authority preservation becomes increasingly important.

A transcript can remain readable while the model-visible context has changed. A replay can show browser or event activity while omitting the memory, environment, recovery, or authority state that shaped the trajectory. A summary can keep work moving while weakening the evidence lineage needed to reconstruct why a later action happened. A remembered belief can survive as text while losing source authority, temporal validity, contradiction state, or supersession status.

This repository investigates those distinctions through bounded public proof packs. The goal is not to claim hidden access to model internals. The goal is to define and test public operational evidence requirements for continuity, replay, reconstruction, and survivability.

## Proof progression

| Proof | Focus |
| --- | --- |
| 001 | continuity evidence |
| 002 | replayability adequacy |
| 003 | compression survivability |
| 004 | operational reconstruction |
| 005 | contradiction survivability |
| 006 | memory authority survivability |

Proofs 003 and 004 currently contain evidence-backed analysis v0.1. Proofs 001, 002, 005, and 006 remain planning or evidence-collection scaffolds unless later proof updates promote specific claims through the repository claim discipline.

## Emerging operational findings

The findings below are limited to what current public proof artifacts support. Where a proof is still a scaffold, the thesis treats its contribution as a public audit dimension, taxonomy, or conservative survivability question, not as a validated target-system conclusion.

### Compression is not equivalent to continuity preservation

Reference: Proof 003.

Proof 003 supports the inferred claim that compression may preserve task utility while reducing replay fidelity unless survivable lineage metadata is retained. Public evidence describes mechanisms that preserve summaries, recent context, tool/action surfaces, temporal ordering surfaces, memory surfaces, and recovery-loop compression triggers. The same evidence does not establish complete transcript reconstructability, full causal lineage continuity, contradiction continuity, or complete environment continuity after compression.

The operational distinction is important: a system may continue functioning after compaction or condensation while still losing enough lineage to make later audit-grade replay incomplete. This is an inferred adequacy concern, not a measured benchmark and not a defect claim against the target systems.

### Visible replay is not equivalent to causal replay

Reference: Proof 004.

Proof 004 supports the inferred claim that visible replay and event logs can support partial reconstruction, but causal operational reconstruction requires survivable lineage across memory, environment, tool results, recovery loops, intent, and provenance. Public evidence describes transcript and history surfaces, typed event histories, tool/action reconstruction surfaces, temporal reconstruction surfaces, recovery-loop surfaces, and replay provenance surfaces.

Those surfaces matter, but they do not by themselves establish complete causal replay. Causal reconstruction remains bounded by what public artifacts preserve about omitted ranges, memory writes and recalls, tool result provenance, environment state, runtime configuration, recovery behavior, contradictions, and intent-bearing context.

### Memory survival is not equivalent to authority preservation

Reference: Proof 006.

Proof 006 is currently an evidence-collection scaffold. It does not claim that either target system preserves or loses memory authority. It defines the authority question that later evidence must answer: when a remembered belief survives, what makes it operationally authoritative?

The scaffold identifies a conservative audit risk. Remembered beliefs can survive as content while losing source authority, temporal validity, contradiction lineage, or supersession state. Authority-aware replay requires enough provenance to recover where a belief came from, whether it was current, whether it had been superseded, whether it was contradicted, and whether it was promoted, summarized, or recalled before use.

### Contradiction survivability matters

Reference: Proof 005.

Proof 005 is currently an evidence-collection scaffold. It does not claim that either target system preserves or loses contradiction lineage. It defines a public audit surface for checking whether contradictions, uncertainty, stale assumptions, rejected alternatives, source authority, temporal conflicts, replay ambiguity, memory conflicts, summary conflicts, and operational truth boundaries survive compression, replay, memory promotion, and reconstruction.

The conservative operational concern is that compression and replay may preserve usefulness while flattening uncertainty, rejected alternatives, stale assumptions, and contradiction lineage. Current public artifacts do not establish contradiction-preserving replay guarantees. That unresolved state is itself part of the claim boundary.

## Operational cognition dimensions

- continuity survivability: Whether the operational state needed for an audit survives compression, replay, recovery, and session boundaries. This includes transcript, tool/action, memory, environment, temporal, recovery, intent, and causal lineage dimensions.

- replay fidelity: Whether replay artifacts preserve enough detail to reconstruct what was visible and what state was available at the time. Fidelity can be useful but bounded when summaries, redactions, omitted ranges, or external state dependencies are not fully linked.

- causal reconstruction: Whether an auditor can reconstruct why a trajectory occurred, not only what appeared on the replay surface. Causal reconstruction depends on lineage across model-visible context, memory, tool results, configuration, environment, recovery paths, and provenance.

- contradiction survivability: Whether conflicts, caveats, rejected alternatives, corrections, and unresolved questions remain reconstructable after compression, replay, or memory promotion. Loss of contradiction lineage can make a replay appear more settled than the original operational state.

- uncertainty retention: Whether public artifacts preserve what was unknown, inferred, incomplete, or unresolved at decision time. Preserving uncertainty prevents weak evidence from becoming stronger than the proof supports.

- authority survivability: Whether source authority survives when beliefs are stored, summarized, recalled, or replayed. User instructions, tool observations, documentation facts, assistant inferences, and memory-derived claims should remain distinguishable where they affect action.

- temporal validity survivability: Whether the time window of a belief, instruction, observation, or correction remains available. A statement can be valid before a correction and stale after it, so operational replay needs before/after boundaries and supersession markers.

- replay provenance: Whether replay artifacts preserve source integrity, artifact identity, capture boundaries, event IDs, omitted ranges, hashes, redaction rules, and retrieval context. Replay provenance controls how strongly a replay can support later claims.

- operational truth survivability: Whether the boundary between observed fact, tool output, source-backed claim, assistant inference, recalled belief, stale assumption, and unresolved question remains reconstructable. Operational truth degrades when useful narrative replaces evidence lineage.

## Operational replay vs visible replay

Operational Cognition treats replay as more than visual playback or transcript recovery. A replay surface can show what happened visibly while still failing to reconstruct why it happened, what state was omitted, which memory was authoritative, which contradictions existed, what assumptions were stale, or what recovery logic changed the trajectory.

Visible replay is the reconstruction of visible sequence: transcript turns, browser interactions, event timelines, tool-call order, or other inspectable activity. Visible replay is valuable because it gives investigators a shared surface for review. It is not sufficient by itself for causal explanation.

Causal replay is the reconstruction of the operational dependencies that made a trajectory possible. It asks whether the replay can recover model-visible context, omitted ranges, tool results, memory writes and recalls, environment state, runtime configuration, recovery behavior, temporal boundaries, source authority, contradictions, and provenance well enough to explain why a later action occurred.

Operational replay adequacy is the degree to which a replay bundle is sufficient for the audit question being asked. Adequacy is not binary. A replay may be adequate for checking visible action order but inadequate for explaining memory influence, authority propagation, environment dependency, recovery behavior, or contradiction preservation.

This distinction anchors the repository. Public replay artifacts and event logs can support partial reconstruction. They become operationally stronger when they preserve lineage across the dimensions that affect causality, authority, temporal validity, and evidentiary status. They remain bounded when those dimensions are absent, summarized, redacted, stale, or unresolved.

## Public/private boundary

The public repository is a proof surface, not a raw cognition dump.

Public artifacts may include:

- proof packs
- evidence manifests
- replayability doctrine
- continuity taxonomies
- evidence-backed findings
- claim registers
- sanitized lineage summaries

Private artifacts and implementation details are not published:

- Belief Ledger internals
- Inside Voice internals
- harmonic traceback implementation
- hidden reasoning traces
- private cognition routing
- substrate scoring internals

This boundary is structural. Public proof packs must stand on public evidence, public summaries, explicit uncertainty, deterministic manifests, and bounded claim registers. Private systems may assist planning or review, but public claims must not require access to private substrate state.

## Claim discipline

Operational Cognition uses a claim hierarchy:

- observed: directly supported by public evidence in the proof pack.
- inferred: conservatively derived from public evidence through an explicit reasoning bridge.
- hypothesis: plausible but not yet validated by sufficient public evidence.
- unresolved: a known evidence gap or open question.

This hierarchy is part of the method. Long-horizon replay and memory systems can make weakly supported narratives look complete. Operational Cognition preserves uncertainty instead of flattening it into stronger claims than the evidence supports.

The project intentionally avoids AGI rhetoric and unsupported interpretability claims. It does not claim consciousness, mechanistic interpretability, solved black-box understanding, hidden substrate access, or target-system defects unless a future public proof pack supports a specific bounded claim.

## Current limitations

- Evidence sets remain bounded.

- Many dimensions remain unresolved, especially contradiction survivability, authority-preserving replay, complete causal lineage, memory reconstruction, recovery-loop reconstruction, and environment reconstruction.

- The current MCP adapter status is `placeholder`. Public proof artifacts may disclose contract-bound hashes or sanitized lineage summaries, but raw private consultation artifacts remain outside the public repository.

- Public evidence may not expose complete operational state. Documentation, issue reports, replay artifacts, trajectory bundles, and event systems can expose useful surfaces while still omitting model-visible context, external state, memory influence, or recovery details.

- Replay adequacy is not yet fully measurable. The repository has not established a minimum sufficient metadata bundle for every replay, compression, memory, contradiction, authority, or reconstruction question.

- Proof packs remain conservative. Several current artifacts are scaffolds or initial analyses, not completed end-to-end reconstructions.

## Future investigation directions

- replay-preserving metadata standards
- contradiction-preserving compression
- authority-aware replay
- survivable lineage requirements
- operational reconstruction adequacy
- recovery-loop reconstruction
- temporal validity preservation
- memory supersession tracking

These directions should remain evidence-first. Each stronger claim needs a proof pack, public evidence references, claim-level classification, and explicit unresolved questions.
