# Fixture Pressure Report

## Did visible-only really fail?

For the synthetic fixture, yes. Proof 010 records zero fully reconstructed visible-only probes, three partially reconstructed probes, and three unresolved probes.

Boundary: this is a fixture-local result. It does not prove visible-only replay fails in every trace.

## Did full-lineage really reconstruct?

For the synthetic fixture, yes. Proof 010 records all six full-lineage probes as reconstructed.

Boundary: this is an observed fixture result, not global sufficiency.

## Was the fixture too easy?

Possibly. The fixture was designed around the same lineage dimensions the corpus was testing: tool results, contradiction refs, memory authority, omitted ranges, environment state, recovery trace, and provenance. That makes it useful as a first fixture but weak as external validation.

## Did the expected result bake in the answer?

Partly. Proof 009 defined expected results before Proof 010 execution, and those expectations align with the survivable-lineage thesis. Proof 010 is still useful because it verifies the fixture mechanics, but it cannot carry the stronger claim that survivable lineage is externally necessary.

## What would make the fixture stronger?

- Add adversarial distractor lineage fields that are present but irrelevant.
- Add missing or inconsistent lineage fields and require the replay to mark them unresolved.
- Include at least one probe where full-lineage replay should fail.
- Include at least one trace where visible-only replay is sufficient for a narrow claim.
- Randomize or independently author probe questions before scoring.
- Separate fixture authorship from replay scoring.
- Add negative controls for memory, contradiction, environment, and recovery dimensions.
- Require provenance hashes for every fixture artifact and every derived score.
- Run the same method on an eligible public or redacted-real trace.

## What would falsify the survivable lineage claim?

- A real or redacted trace where visible-only replay reconstructs all causal, authority, contradiction, environment, recovery, and provenance claims as well as full-lineage replay.
- A full-lineage trace that preserves the proposed lineage bundle but still cannot reconstruct the targeted claims.
- Independent traces where a smaller non-lineage mechanism consistently provides audit-grade reconstruction.
- Evidence that the recurring corpus convergence disappears when proof vocabulary and probe design are independently authored.

## Fixture Hardening Requirements

1. Include positive and negative controls.
2. Include at least one full-lineage expected failure.
3. Include at least one visible-only expected success.
4. Add adversarial irrelevant lineage fields.
5. Add incomplete lineage cases that must remain unresolved.
6. Use independent probe authorship or randomized probe ordering.
7. Preserve exact scoring criteria before replay execution.
8. Record provenance for every artifact, score, and downgrade.
9. Run the hardened method on a public or redacted-real trace.
