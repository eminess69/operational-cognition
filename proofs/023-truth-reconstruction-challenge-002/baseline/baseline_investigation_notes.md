# Baseline Investigation Notes

No Inside Voice consultation was used in this phase.

Target selected: `kubernetes/kubernetes`.

Repository qualification:

- GitHub repository page observed `138190` commits, open issues, and open pull requests.
- The project is older than two years, has many contributors, and has a visible public trail of KEPs, issues, pull requests, release docs, old docs, and archived design proposals.
- Documentation drift is visible in old ThirdPartyResource documentation, current CRD docs, archived design proposals, and versioned Kubernetes docs.

Baseline top-three ranking:

1. Container Runtime Interface / runtime-neutral kubelet.
2. CustomResourceDefinitions / API extensibility.
3. Server-Side Apply / field ownership in the API server.

Baseline missed-risk:

The pass did not deeply investigate Container Storage Interface. It treated CSI as a storage subsystem concern rather than a repository-wide architectural decision. This is the primary candidate for consult-phase recovery.
