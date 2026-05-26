# Reconstruction Gap Taxonomy

Each category below is an initial taxonomy, subject to evidence validation. These are possible reconstruction limitations, not conclusions about either target system.

## Visible replay without causal replay

Visible replay may show transcript turns, browser actions, or event timelines while leaving the causal chain unresolved. This category applies only when public evidence shows visible replay surfaces but not enough lineage to reconstruct why the path occurred.

## Missing environment provenance

Operational state may depend on workspace files, sandbox configuration, runtime versions, container images, external services, ports, permissions, or browser/session state. Public replay artifacts may omit some of that provenance or expose only high-level references.

## Memory reconstruction gaps

Memory surfaces may include durable files, recall operations, indexes, summaries, or flush boundaries. Reconstruction remains limited when public artifacts do not preserve what memory existed, what was recalled, what was omitted, and how memory affected later action.

## Omitted-range ambiguity

Compaction, condensation, truncation, redaction, or summary generation can replace detailed ranges with shorter representations. Reconstruction is ambiguous when omitted ranges lack stable IDs, hashes, source references, or boundary metadata.

## Contradiction flattening

Summaries and replay views can present a single coherent path while losing conflicts, stale assumptions, rejected alternatives, corrections, or uncertainty markers. This category is a hypothesis until validated against specific evidence.

## Replay provenance loss

Replay may be viewable while capture method, source integrity, retrieval time, artifact version, redaction policy, and omitted content are not fully reconstructable. Provenance loss limits how strongly replay can support causal claims.

## Recovery-loop reconstruction gaps

Retries, fallback models, restarts, resumptions, aborts, stuck detection, and cleanup behavior can shape outcomes. Reconstruction remains limited when recovery events are not linked to prior state, new state, errors, and timeline boundaries.

## Temporal ambiguity

Causal explanation can fail when ordering, timestamps, insertion points, before/after boundaries, latency, or restart timing are missing or summarized away. Visible ordering alone may not establish decision ordering.

## Intent reconstruction drift

The active task intent can drift when summaries or memories simplify goals, omit constraints, or lose authority and timing. Reconstruction remains limited when public artifacts cannot distinguish user-stated intent from inferred or summary-derived intent.

## Partial replay survivability

Some dimensions may survive replay while others do not. A replay can preserve transcript and event order while leaving memory, environment, configuration, contradiction, or recovery-loop reconstruction unresolved.
