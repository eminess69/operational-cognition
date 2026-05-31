# Adversarial Composite Evaluation Rubric

Classify each candidate pathway as exactly one of:

- `VALID_COMPOSITE`: the observation requires multiple interacting mechanisms, and the candidate mechanisms are necessary and supported.
- `PLAUSIBLE_BUT_UNPROVEN`: the pathway could fit, but one or more mechanisms lack direct necessity or interaction support.
- `SINGLE_MECHANISM_REWRITE`: the candidate merely renames a single dominant mechanism.
- `UNSUPPORTED`: motifs or lineages are missing, or the observation does not support enough of the pathway.
- `FALSE_COMPOSITE`: the pathway adds mechanisms contradicted by or absent from the observation.

For each candidate answer:

1. Does this pathway require more than one mechanism?
2. Is each mechanism necessary?
3. Is the pathway supported by the observation?
4. Is this merely a preserved list, or does it describe interaction?
5. What would falsify the pathway?

No answer key, expected mechanisms, internal scores, activation weights, confidence values, or original validity fields may be used.
