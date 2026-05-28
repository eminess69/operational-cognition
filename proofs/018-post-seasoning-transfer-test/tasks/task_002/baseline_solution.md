# Baseline Solution

Mode: baseline operational solving.

No candidate lineage refs or runtime pressure rankings were used for this solution.

## Time Budget

Total budget: 120 minutes.

1. Structural completeness: 15 minutes.
   Confirm required root files, task folders, request files, response files, score files, and manifest entries. Missing required files invalidate the test immediately.

2. Mode separation: 20 minutes.
   Inspect baseline artifacts for forbidden candidate identifiers or consult-derived pressure. This check receives early time because a leak invalidates the comparison even if later scoring looks good.

3. Pond-backed response validity: 20 minutes.
   Confirm each task response is pond-backed, has runtime hashes, exposes refs, and has no gate failures.

4. Score recomputation: 15 minutes.
   Recompute each task total and aggregate totals. Compare improved, unchanged, and degraded counts against final verdict rules.

5. Runtime visibility: 15 minutes.
   Check whether detailed refs appear in response artifacts and whether the runtime log exposes the same detail. Record partial visibility if the log only has hashes and counts.

6. Reusable-pool mutation check: 10 minutes.
   Compare the pre-test and post-test reusable pool hashes. Any mismatch invalidates the test.

7. Claim-boundary scan: 15 minutes.
   Search for positive promotion, broad capability, target-defect, or black-box claims.

8. Report cleanup: 10 minutes.
   Only after the validity gates pass, tighten the reports for consistency.

## Triage Rules

- Stop immediately on separation failure, missing runtime hashes, missing refs, pool hash drift, or invalid final verdict math.
- Defer prose polish until all blocking checks pass.
- Treat older failed reports as stale if corrected response artifacts have matching runtime hashes.

## Residual Weakness

This baseline allocation ranks the main risks, but it does not design targeted bypass probes for the gates. It also treats replay checks as one block instead of separating stable-input evidence from nondeterminism boundaries.
