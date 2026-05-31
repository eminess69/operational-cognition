# Proof 029 - Surface-Form Robustness and Structure Reuse

## Result

1. Did surface variation break the system? No for the curated reworded suite: accuracy was 1.0.
2. Did distractors break the system? No for the curated distractor suite: accuracy was 1.0.
3. Did reversed phrasing break the system? No for the curated reversed suite: accuracy was 1.0.
4. Did multi-step composition work? Yes inside the frozen Grade 1/Grade 2 boundary: accuracy was 1.0.
5. Did out-of-scope items fail closed? Yes: fail-closed rate was 1.0.
6. Did hostile audit classify the result as structure reuse or parser matching? The original metrics reached VERY_STRONG_SIGNAL, but the hostile verdict is WEAK_SIGNAL because the implementation is still a narrow deterministic parser with explicit surface templates.
7. What should be tested next? Use a blinded question generator and lock the CLI before test creation, then test paraphrases not visible to the harness builder.

## Boundary

This proof does not add math concepts beyond Proof 028. It tests whether the existing Grade 1/Grade 2 motifs can be reused across curated wording variation. The hostile audit rejects broad claims because success can still be explained by deterministic regex and keyword parsing.

## CLI Boundary

Final answers were produced through:

```bash
python3 -m operational_cognition.cli.math_pond answer --pond proofs/028-developmental-learning-grade-ladder/pond_states/grade_2 --question "<question>" --json
```
