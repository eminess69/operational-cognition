# Contradiction Injection Report

Primary contradiction: C-001

- Source A: S-004 records that strict hash checking is required under `validator-v2.1`.
- Source B: S-006 compressed summary states that v2.0 was sufficient and hash checking was optional.
- Entropy injection: E-001.
- Baseline result: unresolved.
- Full-lineage result: reconstructed.

Secondary authority conflict: C-002

- Source A: S-011 says the repair was simple.
- Source B: A-002, T-002, and R-001 show that success depended on authority ranking, temporal invalidation, and retry recovery.
- Entropy injections: E-004 and E-007.
- Baseline result: unresolved.
- Full-lineage result: reconstructed.

Inside Voice evidence:

- `inside_voice_consults/contradiction_arbitration_response.json`
- adapter_status: `pond_backed`
- contribution_grade: `bounded`
- gate_failures: `[]`

The contradiction was not resolved by trusting a summary. It was resolved by preserving the conflict and ranking the current runtime authority above stale text.
