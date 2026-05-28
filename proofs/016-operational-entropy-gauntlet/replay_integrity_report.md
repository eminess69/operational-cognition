# Replay Integrity Report

## Replay Separation

Mode A used visible transcript facts, visible ordering, and visible compressed summaries only.

Mode B used the same visible facts plus full-lineage refs, pond-backed consult responses, pressure rankings, unresolved tensions, and runtime hashes.

The baseline result was written before using pond-backed consult guidance for replay reconstruction. Consult responses are only cited in `pond_backed_results.md` and downstream comparison artifacts.

## Integrity Checks

| Check | Baseline | Full-lineage |
| --- | --- | --- |
| Runtime dependency bound to result | partial | reconstructed |
| Contradiction preserved | unresolved | reconstructed |
| Stale assumption corrected | unresolved | reconstructed |
| Omitted range reconstructed | unresolved | reconstructed |
| Recovery continuity preserved | unresolved | reconstructed |
| Missing raw body boundary preserved | partial | partial |

The full-lineage replay did not fill every missing raw detail. It preserved the boundary between reconstructed operational facts and unavailable raw event bodies.
