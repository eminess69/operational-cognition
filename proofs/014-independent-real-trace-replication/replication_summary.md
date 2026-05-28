# Replication Summary

Traces selected: 3.

Trace independence: trace_001 is malformed request recovery, trace_002 is runtime/server checkout verification, and trace_003 is claim-boundary audit repair. These are independent operational failure modes and are not Proof 013 duplicated.

Per-trace verdicts: trace_001 TRACE_ADVANTAGE_OBSERVED; trace_002 TRACE_ADVANTAGE_OBSERVED; trace_003 TRACE_ADVANTAGE_OBSERVED.

Aggregate verdict: REPLICATION_ADVANTAGE_OBSERVED.

Visible-only vs full-lineage counts: visible-only reconstructed 2 of 24 probes and left 22 partial or unresolved. Full-lineage reconstructed 24 of 24 probes. Improvement count was 22.

Repeated across traces: visible-only replay could preserve event order but not enough deterministic lineage to resolve tool-result, authority, omitted-range, environment, and recovery-loop probes. Full-lineage replay reconstructed those probes from public-safe hashes and refs.

What did not repeat: the triggering failure mode differed by trace; one was request schema repair, one was runtime listener verification, and one was claim-boundary language repair.

Remaining unresolved questions: public-only traces with less tool lineage remain untested; other runtime deployments remain untested; this proof does not evaluate target-system defects or broad public claims.

Next validation step: run additional independent redacted-real traces with the same replay-mode separation and a predeclared fixture schema.

Focused validation only: full-suite validation remains outside this proof due unrelated failures outside the Proof 014 scope.
