# Proof 031 - Mechanistic Transfer Cue-Invariance

## Objective

Proof 031 attacks the Proof 030 failure mode directly: the deterministic mechanism mapper might be matching parser cues rather than preserving physical or relational structure.

Final answers were generated only by:

```bash
python3 -m operational_cognition.cli.mechanism_pond map --pond proofs/031-mechanistic-transfer-cue-invariance/pond_states/mechanism_seasoned --question "<question>" --json
```

## Result Snapshot

- Cue-removed accuracy: 1.0
- Cue-swapped accuracy: 1.0
- Decoy-cue accuracy: 1.0
- Neutral-physics accuracy: 1.0
- Ambiguous fail-closed rate: 1.0
- Structure-match rate: 0.875
- Cue-match rate: 0.125
- Decoy failure rate: 0.0
- Deterministic replay match: true
- Hostile verdict: WEAK_SIGNAL

## Required Answers

1. Did cue removal break mechanism mapping?
   No. The curated cue-removed suite mapped correctly, but the audit shows many answers still used non-canonical role cues such as inlet, pivot, channel, stress, and joint.

2. Did cue swapping break mechanism mapping?
   No. The cue-swapped suite mapped correctly because the target structure supplied more complete role support than the misleading words.

3. Did decoys break mechanism mapping?
   No. The decoy resistance rate was 1.0000; obvious wrong-mechanism words did not dominate these cases.

4. Did neutral physical descriptions work?
   Yes, inside the curated closed world. Neutral physical descriptions with enough role structure were answered correctly.

5. Did ambiguous inputs fail closed?
   Yes. The ambiguous fail-closed rate was 1.0.

6. Did hostile audit still preserve a parser explanation?
   Yes. The hostile audit keeps `remaining_parser_explanation` true because every successful answer is still explainable by deterministic role-cue matching over the frozen pond state.

7. What exact claim survives?
   A bounded deterministic CLI can resist simple cue removal, cue swapping, and decoys in curated prompts that preserve the four-role mechanism structures from Proof 030. The stronger claim that this is independent of parser scaffolding does not survive.
