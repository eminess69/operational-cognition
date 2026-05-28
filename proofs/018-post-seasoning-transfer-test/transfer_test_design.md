# Transfer Test Design

## Question

Does pond-backed operational solving with MCP-seasoned first-principles candidates available as bounded guidance produce better held-out task outputs than baseline operational solving?

## Modes

Baseline mode:

- Uses the task prompt, visible constraints, normal reasoning, and existing repo files if needed.
- Does not use direct candidate refs.
- Does not use Inside Voice consult responses.
- Does not use runtime pressure rankings.

Pond-backed mode:

- Calls `http://127.0.0.1:8766/consult`.
- Explicitly asks for MCP-seasoned candidate refs when relevant.
- Requires cross-family pressure, contradiction and authority guidance, replayability safeguards, boundary risks, and runtime hashes.
- Treats candidate refs as bounded guidance, not promoted reusable lineage.

## Hard Gate

The proof construction gate used `inside_voice_consults/hard_gate_request.json` and `inside_voice_consults/hard_gate_response.json`.

Gate result:

- `adapter_status`: `pond_backed`
- `contribution_grade`: `bounded`
- `runtime_stage_report_ref`: present
- `pressure_rankings`: non-empty
- `gate_failures`: `[]`
- Safe-negated boundary handling: present in `claim_boundary_audit`
- Runtime hashes: present
- Broad unsupported claim block: absent

## Rubric

Each task is scored on eight fields, each from 0 to 5:

- task completeness
- contradiction handling
- authority handling
- replayability
- prioritization quality
- boundary discipline
- hallucination prevention
- actionability

## Validity Rules

- Baseline artifacts must not cite candidate refs.
- Pond-backed task artifacts must cite at least one MCP-seasoned candidate ref.
- Runtime hashes must be present for each pond-backed consult.
- The runtime visibility report must distinguish response-visible refs from runtime-log verbosity.
- The reusable pool hash must remain unchanged.
- The final verdict must follow aggregate score math and claim-boundary rules.
