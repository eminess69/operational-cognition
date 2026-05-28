# Candidate Conversion Report

## Conversion Method

The redacted-real trace was converted into the Proof 009/010-style fixture shape with deterministic refs:

- transcript refs: `T-*`
- event refs: `E-*`
- tool action refs: `A-*`
- tool result refs: `TR-*`
- memory refs: `MEM-*`
- contradiction refs: `C-*`
- authority refs: `AUTH-*`
- temporal refs: `TV-*`
- environment refs: `ENV-*`
- recovery refs: `R-*`

## Fixture Artifacts

The fixture is stored under `proofs/013-real-trace-replay-gate/fixture/` and includes transcript, events, tool actions, result manifest, memory log, compressed context summary, omitted ranges, contradiction refs, authority refs, temporal validity, environment snapshot manifest, runtime config, recovery trace, provenance manifest, and public lineage summary.

## Inside Voice Participation

Pond-backed Inside Voice was used for:

- candidate evaluation: `artifacts/inside_voice/proof_013_candidate_risk_gate_response.json`
- contradiction mapping: `artifacts/inside_voice/proof_013_contradiction_mapping_response.json`
- omitted-range recovery: `artifacts/inside_voice/proof_013_omitted_range_recovery_response.json`
- replay adequacy analysis: `artifacts/inside_voice/proof_013_replay_adequacy_response.json`
- claim-boundary audit: `artifacts/inside_voice/proof_013_claim_boundary_audit_response.json`

The replay-adequacy call returned a boundary warning. The proof records that warning and avoids broad comparative wording.

## Runtime Fields Recorded

- adapter_status: `pond_backed`
- candidate-risk contribution_grade: `strong`
- runtime_stage_report_ref: `artifacts/integrations/inside_voice_runtime/runtime_stage_report.json`
- candidate-risk runtime_response_hash: `90b27799df584e4fb62f05f2feb510d852b890f21ddb8c3ef83fcaacfa67ad0e`
- corpus_hash: `b44a6338242a31cee7792d853979662f31975822d1509b8fca4a0824c38d5a0d`
- recalled motif: `inside_voice_runtime:b52f584c333f5750c031`
- unresolved tension: `inside_voice_runtime:d43e2e09c028b98314e8`
- pressure rankings: `pressure:c3df6614e5a021dd`, `pressure:9b4f9fded2776784`, `pressure:d8573d273ed72157`
- claim-boundary warning: replay-adequacy advisory call reported `BROAD_UNSUPPORTED_CLAIM_BLOCKED`; final wording therefore remains single-trace bounded.
