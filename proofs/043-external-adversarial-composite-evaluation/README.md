# Proof 043 - External Adversarial Composite Evaluation

Proof 043 evaluates the exact stripped blind candidate set from Proof 042 without regenerating candidates.

## Result

`WEAK_SIGNAL`

## Questions

1. Did external evaluators agree with the internal blind evaluator?
   - Partly. Mode A/Mode C agreement was 0.8; Mode B/Mode C agreement was 1.0.
2. How many composites survived consensus review?
   - 181 candidate pathways were classified as valid by at least two modes.
3. Were survivors true composites or preserved lists?
   - The rubric requires multi-mechanism necessity and interaction. The hostile audit still preserves pathway-inflation and wording-leakage explanations.
4. Did LLM adversarial review reject or support the result?
   - Mode C supported a bounded result with valid rate 0.8, but it is a recorded Codex adversarial review rather than a separately authenticated outside service.
5. What explanations remain?
   - Generator bias, evaluator bias, LLM bias, wording leakage, and same-code evaluator contamination remain.
6. What exact bounded claim survives?
   - The stripped Proof 042 candidates retained enough structure for a meaningful consensus subset to survive stricter adversarial review, but not enough to eliminate generator/evaluator-loop explanations.

## Metrics

- Mode A valid rate: 1.0
- Mode B valid rate: 0.8
- Mode C valid rate: 0.8
- Consensus valid rate: 0.8
- Consensus false-composite rate: 0.0218
- Surviving composite count: 181
