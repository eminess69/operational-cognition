# Baseline Solution

Mode: baseline operational solving.

No candidate lineage refs or runtime pressure rankings were used for this solution.

## Validation Plan

1. Freeze the evidence set.
   Record the proof directory path, list all required artifacts, and record the current hash of the external reusable pool before any validation. If the proof directory changes during validation, restart from this step.

2. Validate structural completeness.
   Check that the root required files exist, the three task folders exist, and each task folder has a description, two solutions, two score files, a refs file, a comparison, and a verdict. Missing task artifacts stop the test because comparison would be incomplete.

3. Validate mode separation.
   Scan baseline solutions and baseline score files for seasoned-candidate identifiers, candidate refs, or consult response-derived pressure rankings. Any baseline leak invalidates the transfer comparison.

4. Validate pond-backed evidence.
   For each task, inspect the consult response for `adapter_status`, empty `gate_failures`, runtime hashes, and visible candidate refs. Missing refs or hashes invalidate that task.

5. Resolve authority conflicts.
   Rank authority in this order: live consult response JSON, runtime log entry by matching request hash, proof-local task files, then summary prose. If a summary contradicts JSON evidence, mark the summary stale and require correction.

6. Validate score math.
   Recompute task totals from the eight rubric fields. Recompute aggregate baseline and pond-backed totals, improved counts, unchanged counts, degraded counts, and final verdict eligibility.

7. Validate runtime visibility.
   Compare response refs with runtime log contents. If responses expose refs but the log exposes only hashes and counts, record the visibility gap instead of treating it as a full logging pass.

8. Validate claim boundaries.
   Search proof prose and JSON for positive broad capability, promotion, target-defect, or black-box claims. Negated boundary language may remain, but positive claims stop the test.

9. Emit the final validation result.
   Only after the structural, separation, runtime, scoring, mutation, and claim-boundary checks pass should the proof receive a valid final verdict.

## Stop Conditions

- Baseline artifacts cite candidate refs.
- Pond-backed task artifacts lack candidate refs.
- Runtime hashes are missing.
- Score totals do not match component scores.
- The reusable pool hash changes.
- The final verdict exceeds the aggregate rules.

## Residual Weakness

This baseline plan is serviceable, but it treats validation steps mostly as a checklist. It does not explicitly model dependency direction between validation stages or design cheap invariant-bypass probes before running broader checks.
