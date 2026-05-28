# Gauntlet Design

The gauntlet uses five independent domains and applies the same reconstruction probes to both replay modes. Visible-only replay may use visible transcript order and summaries. Pond-backed replay may use consult refs, pressure rankings, contradiction refs, authority refs, temporal refs, omitted-range refs, recovery refs, runtime hashes, stage reports, and provenance manifests.

Each scenario contains a long horizon sequence, compressed context boundary, omitted range, stale assumption, at least two contradictions, retry/recovery loop, environment dependency, partial lineage loss, competing authority sources, summary degradation pressure, and replay reconstruction challenge.

The scoring unit is a probe status, not a narrative claim. Allowed probe statuses are `reconstructed`, `partially_reconstructed`, and `unresolved`.

