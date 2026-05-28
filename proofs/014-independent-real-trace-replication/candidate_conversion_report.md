# Candidate Conversion Report

Each selected candidate was converted into a fixture folder with transcript, events, tool actions, tool result manifest, memory log, compressed context summary, omitted ranges, contradiction refs, authority refs, temporal validity refs, environment snapshot, runtime config, recovery trace, provenance manifest, and public lineage summary.

Conversion preserves replay-mode separation: visible-only inputs are intentionally insufficient for several probes, while full-lineage inputs carry deterministic refs needed to reconstruct those probes.
