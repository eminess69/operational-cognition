# Baseline Solution

Mode: baseline operational solving.

No candidate lineage refs or runtime pressure rankings were used for this solution.

## Decision

Choose Design B.

The task explicitly forbids endpoint expansion. Design A would satisfy log verbosity more directly, but it violates a hard constraint and would change the runtime surface during a transfer-utility test. Design B preserves the runtime contract and records the visibility limitation in proof-local artifacts.

## Rationale

1. Treat the no-endpoint-expansion rule as binding.
   A design that changes the endpoint cannot be selected for this proof, even if it would produce a cleaner logging result.

2. Split response visibility from log verbosity.
   Response artifacts can show detailed refs. Runtime logs can show request hashes, response hashes, corpus hashes, counts, and synthesis text. The proof should report both facts separately.

3. Preserve replayability.
   Use request and response JSON files as replayable evidence. Match them to runtime log entries by request hash and response hash.

4. Avoid overclaiming.
   The design can claim response-visible refs when present. It cannot claim that the runtime log exposes detailed refs if the log omits them.

5. Keep mutation boundaries.
   Do not modify the reusable pool or promote candidate refs as part of architecture arbitration.

## Residual Weakness

This baseline decision respects the hard constraint, but it does not include an explicit adversarial check for surface-valid but invariant-invalid evidence. It also does not formalize nondeterminism boundaries beyond matching hashes.
