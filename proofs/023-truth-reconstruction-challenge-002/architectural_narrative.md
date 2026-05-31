# Architectural Narrative

Target: `kubernetes/kubernetes`.

Final answer: Kubernetes became what it is by repeatedly extracting ecosystem-specific implementation from core Kubernetes into stable extension boundaries, while keeping the Kubernetes API as the common control surface. The three strongest historical decisions in that pattern are CRI, CRDs, and CSI.

## Decision 1: CRI

Kubernetes first had to stop treating Docker as structurally special. The 2016 CRI announcement says the container runtime space was evolving and that users wanted support for more runtimes. It also records that Docker and rkt had been integrated directly into kubelet through internal interfaces, creating high maintenance cost and barriers for new runtimes.

The alternatives were to keep direct integrations, keep Docker/dockershim privileged, or expose a stable runtime boundary. CRI won because kubelet could keep Kubernetes pod lifecycle semantics while runtimes implemented a gRPC/protobuf contract. KEP-2221 later shows the consequence: dockershim was still built into kubelet, tightly coupled to kubelet's lifecycle, and ultimately removed so Docker would no longer be special.

Evidence lineage: CRI blog lines 795-801; KEP-2221 lines 287-300; dockershim FAQ lines 806-809; `consult_002_cri_response.json`.

## Decision 2: CRDs

Kubernetes then had to let users extend the API without turning every extension into a core-code change or a full custom API server. CRDs made custom resources behave like native resources while being served by the main API server. API aggregation remained the flexible option, but the docs state the core tradeoff plainly: CRDs are easier; aggregated APIs are more flexible.

This decision made Kubernetes a platform for operators and domain APIs. KEP-95 shows why GA was not just a label: CRDs were already widely used, but the project had to settle pruning, defaulting, schema restrictions, conversion, subresources, validation, and scale targets. The consequence is that Kubernetes became an API substrate, not only a container orchestrator.

Evidence lineage: custom resource docs lines 983-1003; KEP-95 lines 90-114; archived ThirdPartyResource docs; `consult_003_crd_response.json`.

## Decision 3: CSI

The baseline pass missed CSI and ranked Server-Side Apply third. The consult run changed the search path by forcing a broader motif check: Kubernetes repeatedly moves vendor/runtime/provider implementation out of core behind stable APIs. Under that motif, CSI is more historically central than Server-Side Apply.

The CSI design proposal records the original storage problem: volume plugins were in-tree, release-coupled, risky for core binaries, and hard for maintainers to test. FlexVolume was the predecessor and a real competing path, but it still required filesystem access and did not solve dependency/deployment pain. CSI won because it let storage providers ship out-of-tree, containerized drivers through a standard interface while Kubernetes users kept the storage primitives they already used.

The long-term consequence was not just adding another plugin. CSI migration translated old in-tree storage APIs to CSI drivers so existing PersistentVolume, PersistentVolumeClaim, and StorageClass objects could keep working while implementation moved out of core.

Evidence lineage: CSI design proposal lines 250-268 and 290-295; CSI alpha blog lines 798-805 and 955-960; CSI GA blog lines 796-802; CSI migration blog lines 798-804; `consult_001_top_three_rerank_response.json`; `consult_004_csi_response.json`; `consult_005_final_contradiction_audit_response.json`.

## Why SSA Was Demoted

Server-Side Apply remains an important architectural repair: it moved field ownership and conflict handling into the API server. But compared with CRI and CSI, it does not redefine Kubernetes' boundary with an external implementation ecosystem. Compared with CRDs, it does not turn Kubernetes into an extension substrate. The consult run changed the investigation from "major API features" to "system-shaping architectural boundaries," and the public evidence supported demoting SSA.

## Recovered Context

The key recovered fact is that CSI is part of the same deep pattern as CRI: both remove special in-tree implementation from core Kubernetes and replace it with a stable, external contract. CRDs do the same at the API-extension level. This makes the long arc of Kubernetes less a list of features and more a governance architecture: stable APIs in core, ecosystem implementation outside core, compatibility layers for migration, and a continuous tension between extensibility and operational burden.
