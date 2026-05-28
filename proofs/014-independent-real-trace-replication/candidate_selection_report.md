# Candidate Selection Report

| Trace | Candidate Class | Selection | Independence |
|---|---|---|---|
| trace_001 | malformed request recovery trace | accepted | Request-shape failure and schema-cap correction; independent from Proof 013 and from runtime listener verification. |
| trace_002 | runtime/server checkout mismatch trace | accepted | Runtime/server state recovery; independent from request-shape repair and claim-boundary language repair. |
| trace_003 | claim-boundary false-positive trace | accepted | Claim-boundary language repair; independent from schema cap recovery and runtime listener verification. |

Rejected candidates: direct duplication of Proof 013 and candidates without tool/action evidence, correction or recovery behavior, or replay-mode separation.

Selection risk was checked with pond-backed Inside Voice before fixture conversion. The selected traces are not all the same failure mode.
