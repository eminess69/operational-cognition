# Proof 030 - Mechanistic Transfer Challenge

## Objective

This proof tests whether a deterministic pond can map learned mechanism motifs across changed surface domains.

Final mappings are generated only through:

```bash
python3 -m operational_cognition.cli.mechanism_pond map --pond <pond_state_dir> --question "<question>" --json
```

## Required Mapping Output

Every identified item emits:

```json
{
  "observed_system": "",
  "identified_mechanism": "",
  "supporting_motifs": [],
  "source_mechanism": "",
  "transfer_confidence": 0.0
}
```

## Result Snapshot

- Mechanism Transfer Rate: 1.0
- Cross-domain transfer rate: 1.0
- Hidden-mechanism transfer rate: 1.0
- Unsupported fail-closed rate: 1.0
- Unseasoned baseline all fail closed: true
- Hostile verdict: FAIL

## Audit Boundary

The transfer metric is high inside the curated closed-world test, but the hostile audit marks the proof as FAIL for strong claims because parser behavior and hardcoded role-cue explanations survive. The surviving claim is bounded: a deterministic no-LLM CLI can reuse explicit mechanism motifs from a proof state on curated cross-domain prompts and fail closed outside that state.
