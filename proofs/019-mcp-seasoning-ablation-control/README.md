# Proof 019: MCP-Seasoning Ablation and Blind Transfer Control

This proof runs a blinded and ablated transfer comparison across four held-out operational tasks. It compares visible-only baseline solving, seasoned pond-backed solving with MCP-seasoned candidate refs enabled, and an ablated pond-backed control where the seasoned candidate source family is removed before recall.

## Result

Verdict: `SEASONING_TRANSFER_ADVANTAGE_CONFIRMED`.

| Metric | Value |
| --- | ---: |
| baseline total | 136 |
| seasoned total | 172 |
| ablated total | 156 |
| seasoned vs baseline | +36 |
| seasoned vs ablated | +16 |
| tasks where seasoned won | 4/4 |
| tasks where ablation reduced quality | 4/4 |
| seasoned responses with MCP-seasoned refs | 4/4 |
| ablated responses with MCP-seasoned refs | 0/4 |

The finding is bounded to these four local held-out tasks, the captured runtime responses, and the declared scoring rubric. It does not make a promotion claim, generalized cognition claim, AGI claim, consciousness claim, black-box-solved claim, or broad capability claim.
