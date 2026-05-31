# Inside Voice Behavior Protocol

This protocol exposes observable pond behavior through explicit `/consult` modes.
Successful responses are pond-backed only when they carry traceable motifs,
lineages, and lineage hashes from the local Inside Voice pond state.

## Common Request Shape

```json
{
  "request_id": "behavior-probe-001",
  "task": "Observation:\nOutput stayed stable until a threshold, then feedback accelerated decline.\nRequired: return behavior fields for the requested mode.",
  "context": {
    "summary": "Behavior protocol probe.",
    "files": [],
    "constraints": ["No placeholder fallback.", "Fail closed if pond recall is unavailable."],
    "desired_artifacts": ["raw_response"]
  },
  "mode": "activation_only",
  "max_output_chars": 8000,
  "require_lineage": true
}
```

Unknown modes are not routed implicitly. They fail closed with:

```json
{
  "adapter_status": "error",
  "verdict": "fail_closed",
  "fail_closed_reason": "unknown_mode"
}
```

## Common Successful Response Fields

Every successful response must include:

```json
{
  "adapter_status": "pond_backed",
  "response_source": "inside_voice_pond",
  "mode": "",
  "returned_motifs": [],
  "returned_lineages": [],
  "lineage_hashes": [],
  "fail_closed_reason": null
}
```

Validation rule:

```bash
python3 tools/validate_mcp_consults.py <consult-log.jsonl> --require-lineage --require-motifs
```

## Modes

### recall

Purpose: return relevant pond-backed motifs and lineages without activation-field
inspection.

Additional output:

```json
{
  "recall_summary": "Returned traceable pond records ranked by motif/cue overlap.",
  "findings": []
}
```

Fail closed when the pond is unavailable, empty, or no relevant record matches.

### activation_only

Purpose: return all activated mechanisms before ranking or elimination.

Additional output:

```json
{
  "activated_mechanisms": [
    {
      "mechanism": "THRESHOLD",
      "activation_weight": 0.42,
      "supporting_motifs": ["Accumulation", "Limit", "Trigger", "StateChange"],
      "supporting_lineages": ["pond:threshold:..."],
      "supporting_lineage_hashes": ["..."]
    }
  ],
  "activation_weights": {
    "THRESHOLD": 0.42
  }
}
```

Fail closed when no mechanism receives relevant motif/cue support.

### field_interaction

Purpose: form pair and triple mechanism interactions before collapse.

Additional output:

```json
{
  "field_interactions": [
    {
      "pathway_id": "pathway:...",
      "pathway": "THRESHOLD + FEEDBACK",
      "mechanisms": ["THRESHOLD", "FEEDBACK"],
      "combination_depth": 2,
      "interaction_weight": 0.75,
      "supporting_motifs": [],
      "shared_motifs": [],
      "supporting_lineages": [],
      "supporting_lineage_hashes": []
    }
  ],
  "interaction_window": {
    "ranking_deferred": true,
    "pairwise_pathways": 0,
    "triple_pathways": 0
  }
}
```

Fail closed when activation cannot return pond-backed motifs and lineages.

### delayed_ranking

Purpose: rank only after the interaction window forms composite pathway
candidates.

Additional output:

```json
{
  "ranked_pathways": [
    {
      "rank": 1,
      "pathway": "THRESHOLD + FEEDBACK + RESOURCE_DEPLETION",
      "mechanisms": ["THRESHOLD", "FEEDBACK", "RESOURCE_DEPLETION"],
      "combination_depth": 3,
      "weight": 0.91
    }
  ]
}
```

Fail closed when activation cannot return pond-backed motifs and lineages.

### collapse_trace

Purpose: show which interaction pathways survived collapse and which were
eliminated.

Additional output:

```json
{
  "collapse_trace": {
    "activated_before_collapse": ["THRESHOLD", "FEEDBACK"],
    "survived_after_collapse": [],
    "eliminated_pathways": [],
    "collapse_reason": "Delayed-ranking collapse selected the highest supported interaction pathway."
  }
}
```

Fail closed when activation cannot return pond-backed motifs and lineages.

### perturbation

Purpose: rerun field behavior after suppressing, removing, or injecting
mechanisms or motifs.

Additional output:

```json
{
  "perturbations": [
    {
      "perturbation": "remove_top_activated",
      "activated_mechanisms": [],
      "field_size": 0,
      "ranked_pathways": [],
      "valid_pathway_count": 0
    }
  ],
  "perturbation_summary": {
    "top_mechanism_removed": "",
    "top_two_mechanisms_removed": [],
    "injected_irrelevant_mechanism": "",
    "suppressed_shared_motif": "",
    "ranking_forced_off": true
  }
}
```

Fail closed when activation cannot return pond-backed motifs and lineages.

## Example Probe Command

```bash
python3 tools/integrations/run_inside_voice_behavior_probe.py \
  --mode activation_only \
  --observation "Output stayed stable until a threshold, then feedback accelerated decline." \
  --out artifacts/inside_voice_behavior_probe
```
