# Replication Plan

Proof 014 tests whether the Proof 013 result repeats across independent redacted-real operational traces.

Mode A, visible-only replay, receives only public transcript, visible event order, and visible action sequence. Mode B, full-lineage replay, receives fixture bundle, tool result refs and hashes, authority refs, omitted-range refs, temporal validity refs, environment refs, runtime config, recovery trace, provenance manifest, and pond-backed runtime hashes.

All traces execute probes P-001 through P-008 and classify each as reconstructed, partially_reconstructed, or unresolved. The aggregate verdict is bounded to these fixtures and preserves Proof 010 synthetic-only and Proof 011/013 real-trace replay boundaries.
