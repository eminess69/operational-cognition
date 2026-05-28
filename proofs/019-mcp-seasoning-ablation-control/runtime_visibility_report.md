# Runtime Visibility Report

## Required Answers

Did seasoned mode expose MCP-seasoned refs? Yes. Every seasoned response exposes MCP-seasoned refs in `retrieved_artifact_refs` and related lineage fields.

Did ablated mode suppress MCP-seasoned refs? Yes. Every ablated response excludes the seasoned candidate source family before recall and has zero MCP-seasoned refs in retrieved refs, lineage refs, and pressure rankings.

Did runtime hashes differ across modes? Yes. Seasoned responses use the default corpus hash, while ablated responses use a filtered corpus hash. Runtime request and response hashes also differ by task.

Did pressure rankings change? Yes. Seasoned responses were compacted to the top three pressure rankings with MCP-seasoned refs visible elsewhere; ablated responses retained eight non-seasoned pressure rankings.

Did contradiction arbitration change? Yes. Both modes retained contradiction pressure, but ablated mode relied on continuity arbitration and proof-boundary refs without candidate-family guidance.

## Classifications

- `SEASONED_VISIBLE`: all four seasoned responses expose MCP-seasoned refs.
- `ABLATION_CONFIRMED`: all four ablated responses suppress MCP-seasoned refs while retaining runtime pressure evidence.
- `VISIBILITY_GAP`: not observed.
- `UNEXPECTED_SEASONED_LEAK`: not observed.

## Per-Task Audit

### task_001

- Seasoned exposed MCP-seasoned refs: `True`.
- Ablated suppressed MCP-seasoned refs: `True`.
- Runtime hashes differ: `True`.
- Pressure ranking counts changed: seasoned `3`, ablated `8`.
- Classification: `SEASONED_VISIBLE`, `ABLATION_CONFIRMED`.

### task_002

- Seasoned exposed MCP-seasoned refs: `True`.
- Ablated suppressed MCP-seasoned refs: `True`.
- Runtime hashes differ: `True`.
- Pressure ranking counts changed: seasoned `3`, ablated `8`.
- Classification: `SEASONED_VISIBLE`, `ABLATION_CONFIRMED`.

### task_003

- Seasoned exposed MCP-seasoned refs: `True`.
- Ablated suppressed MCP-seasoned refs: `True`.
- Runtime hashes differ: `True`.
- Pressure ranking counts changed: seasoned `3`, ablated `8`.
- Classification: `SEASONED_VISIBLE`, `ABLATION_CONFIRMED`.

### task_004

- Seasoned exposed MCP-seasoned refs: `True`.
- Ablated suppressed MCP-seasoned refs: `True`.
- Runtime hashes differ: `True`.
- Pressure ranking counts changed: seasoned `3`, ablated `8`.
- Classification: `SEASONED_VISIBLE`, `ABLATION_CONFIRMED`.
