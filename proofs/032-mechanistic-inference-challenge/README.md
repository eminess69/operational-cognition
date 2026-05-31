# Proof 032 - Mechanistic Inference Challenge

## Objective

Proof 032 tests whether the mechanism pond can infer a closed-world mechanism from observed consequences when roles are hidden, evidence is reordered, entities are missing, surfaces are novel, or multiple causes compete.

Final answers were generated only by:

```bash
python3 -m operational_cognition.cli.mechanism_pond map --pond proofs/032-mechanistic-inference-challenge/pond_states/mechanism_inference --question "<question>" --json
```

## Result Snapshot

- Consequence-only accuracy: 1.0
- Reordered-evidence accuracy: 1.0
- Missing-roles accuracy: 1.0
- Multi-cause ranking accuracy: 1.0
- Novel-surface accuracy: 1.0
- Fail-closed rate: 1.0
- Consequence or relational success rate: 1.0
- Hidden-cause inference rate: 1.0
- Deterministic replay match: true
- Signal before hostile audit: STRONG_SIGNAL
- Hostile verdict: WEAK_SIGNAL

## Required Answers

1. Did consequence-only observations identify mechanisms?
   Yes, inside the closed three-mechanism curriculum.

2. Did reversed evidence break inference?
   No. The scorer is order-insensitive, so reversed chains still map.

3. Did hidden or missing roles break inference?
   No for the curated cases. The system used consequence signatures rather than direct role names.

4. Did multi-cause competition produce ranked candidates?
   Yes. Multi-cause result rows include `candidate_mechanisms` and `confidence_ranking`.

5. Did novel surface objects break inference?
   No. Fictional object names mapped when consequence signatures were present.

6. Did ambiguous inputs fail closed?
   Yes. The fail-closed rate was 1.0.

7. What survives hostile audit?
   A bounded deterministic CLI can infer closed-world mechanisms from consequence signatures without direct role labels. The stronger claim that this defeats parser or template explanations does not survive.
