# Public Lineage Summary

The source backbone is NASA's public Rogers Commission HTML corpus:

- Volume I chapters on the accident, physical cause, contributing cause, historical root causes, safety program, schedule pressure, and recommendations.
- Volume II appendices on reliability observations, flight readiness review treatment of O-ring problems, prelaunch activities, mission planning, development/production, accident analysis, and Morton Thiokol comments.
- Volume IV and V hearing records containing NASA, Thiokol, and engineering testimony.

All major conclusions in this proof pack trace through evidence IDs in `evidence_graph.json`. Conclusion-level paths are recorded in `harmonic_traceback_report.json`; causal ordering is recorded in `causal_chain.json`; conflicts are preserved in `contradiction_map.json`.

The pack uses public source references and short paraphrased evidence summaries. It does not publish hidden reasoning traces or private Inside Voice internals.

## Inside Voice MCP Audit

After the public-corpus reconstruction, a bounded Inside Voice MCP audit was run against the proof pack:

- request: `inside_voice_consults/traceback_audit_request.json`
- response: `inside_voice_consults/traceback_audit_response.json`
- consultation record: `inside_voice_consults/mcp_consultation_record.json`

The MCP response reported `adapter_status=pond_backed` and `verdict=ok`, but its contribution grade was `minimal` and it blocked broad unsupported public-claim language. The consult is therefore recorded as a claim-boundary audit, not as a replacement for the NASA/Rogers historical source lineage.
