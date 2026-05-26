# Recursive Consultation Log

## Boundary

The local Inside Voice MCP bridge was consulted three times for Proof 008. The adapter status reported by each response was `placeholder`, so the consultations are advisory lineage only and do not provide evidence for target-system behavior. Evidence basis: `docs/PROOF_STANDARD.md`; `docs/PUBLIC_PRIVATE_BOUNDARY.md`; `proofs/007-cross-proof-convergence/convergence_analysis.md`.

Raw request and response artifacts are stored only under ignored `internal/inside_voice/proof_008_recursive_deep_audit/`. Public material below contains only sanitized summaries and hashes. Evidence basis: `docs/PROOF_STANDARD.md`.

## Consultation Hashes

| Pass | Mode | Request hash | Response hash | Sanitized summary |
| --- | --- | --- | --- | --- |
| synthesis | `synthesis` | `f1f0d3ac63e7f69d998235c42439cfc298c64bf298b70d0e0d99e1fe8a9a99ab` | `7ac2a86ec1cc40154c50218df8277c851b834b45636609d8afaa4dd2ea169438` | Bounded advisory pass over Proofs 001-007 for recurring operational requirements; public claims remain supported by proof artifacts, not MCP output. |
| adversarial | `review` | `43ba0bc6013f6fbcabe9608466984f7a3aca121cf234e47cebdd898d99c8af82` | `4be552d3d56a28a8d4039cc577fa5d48a4c7919c7a1f00d548d3fe5922ec4d9e` | Bounded advisory pass for overclaim and evidence-gap pressure; unresolved target-system preservation remains unresolved. |
| validation | `proof_planning` | `d268b19d5bc649e9a72ef40edc911d473dfa517b362943fc4da55e934cac3cf3` | `c909694c39825014f7f918cb7f5dde7bd4b30c7361568046bb9215cba93c289b` | Bounded advisory pass for fixture completeness; the resulting fixture plan remains a candidate validation design. |

## Raw Body File Hashes

| Internal artifact kind | SHA-256 |
| --- | --- |
| synthesis request body | `7860e37df8643958ec07456ba9910ba07c646774db5ac77ef0bb85fdcc4d2706` |
| synthesis response body | `48a2207d35b9097b3b3f258294c6f11adb210683b9150182992a7257d4e0cd28` |
| adversarial request body | `502240a71f67ae97aad0bfc816e4e7c832932ac2d6ca716cab56a03b8ff56624` |
| adversarial response body | `87f52ea05cbffeb2403397416aa1899bf9abc6615df08707c377ad528b4fc8fe` |
| validation request body | `b430f898a5cca778d448597e4c5fefb0165417e3d1a193feeb58a894a8e88109` |
| validation response body | `fc375bd5530aeeed336a41a01aced7af188bfd499247f45c6bc3dfe78cf4be69` |
| capabilities response body | `cd2602821aba6b2d59b88f0b01a3a898951351dd7ef5ea6d7cf5527b2ce934d5` |
| schema response body | `17a2f78000609684555f4d99f4223faff0a25ad0617f177e0aaab838decc485b` |

## Public Use

Proof 008 uses the consultations only as bounded review pressure. The substantive audit claims cite public proof artifacts, especially `proofs/007-cross-proof-convergence/cross_proof_claim_register.json`, `proofs/007-cross-proof-convergence/minimum_operational_replay_bundle.md`, and the cited source proof artifacts from Proofs 001-006.
