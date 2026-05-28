# Solution B

Do not decide from the 45-day scanner baseline. Open a same-day evidence refresh and split the decision into three branches: block, patch with partner mitigation, or short risk-accepted extension.

Authority order:

- Security owns vulnerability closure criteria and exploit relevance.
- Product owns verified partner breakage and patch feasibility.
- Audit owns acceptance evidence requirements.
- Commercial stakeholders provide impact timing, not risk acceptance.

Replay plan:

1. Run a fresh scan or targeted component check.
2. Ask security to classify exploit relevance as applicable, not applicable, or unresolved.
3. Require product to demonstrate the partner workflow break with logs or a test case.
4. Draft compensating controls: limited exposure window, monitoring, rollback, owner, and expiry.
5. Convene a risk acceptance decision with named accountable owner.

Stop release if applicable exploit evidence exists without a patch or compensating controls, if no accountable owner accepts risk, or if partner breakage cannot be verified. If an extension is granted, it must be short, dated, and tied to refreshed evidence rather than the stale scan.
