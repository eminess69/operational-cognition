You are an external adversarial evaluator. You are not the generator.
Use only the evaluation pack and rubric below. Do not infer hidden expected labels.

# Adversarial Composite Evaluation Rubric

Classify each candidate pathway as exactly one of:

- `VALID_COMPOSITE`: the observation requires multiple interacting mechanisms, and the candidate mechanisms are necessary and supported.
- `PLAUSIBLE_BUT_UNPROVEN`: the pathway could fit, but one or more mechanisms lack direct necessity or interaction support.
- `SINGLE_MECHANISM_REWRITE`: the candidate merely renames a single dominant mechanism.
- `UNSUPPORTED`: motifs or lineages are missing, or the observation does not support enough of the pathway.
- `FALSE_COMPOSITE`: the pathway adds mechanisms contradicted by or absent from the observation.

For each candidate answer:

1. Does this pathway require more than one mechanism?
2. Is each mechanism necessary?
3. Is the pathway supported by the observation?
4. Is this merely a preserved list, or does it describe interaction?
5. What would falsify the pathway?

No answer key, expected mechanisms, internal scores, activation weights, confidence values, or original validity fields may be used.


Evaluation pack:
```json
[
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION"
        ],
        "pathway_id": "P041-CP-001-9764ad0a2465",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Escalation",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING"
        ],
        "pathway_id": "P041-CP-001-bcc8c7c0de8a",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Input",
          "Overflow",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-001-b18d70bce3a3",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Input",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Response",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-001-eba9e4c2e35e",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-696d72e11d55",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Exhaustion",
          "Input",
          "Overflow",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-99f7916c9ad4",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Input",
          "Limit",
          "Overflow",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING"
        ],
        "pathway_id": "P041-CP-001-2672f7936fed",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Propagation"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-001-bae9d1030c7c",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-001-564ab5dad2ed",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0"
        ],
        "supporting_motifs": [
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-e27d75943c95",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Propagation",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-d0ad686b00d8",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Propagation",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-001-984a0de00b8f",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Input",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-001-03a1994e8058",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Flow",
          "Input",
          "Path",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-3a0befc094ed",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-ecd65dfba512",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Input",
          "Limit",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-001-2574e1f540ad",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0"
        ],
        "supporting_motifs": [
          "Flow",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-8af61037d990",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Exhaustion",
          "Loop",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-79a62c6bf455",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Limit",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-febd7aa30fe8",
        "supporting_lineages": [
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Exhaustion",
          "Flow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-5d98b7977387",
        "supporting_lineages": [
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Flow",
          "Limit",
          "Path",
          "Resistance",
          "Source",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-0227bd6d4e40",
        "supporting_lineages": [
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Consumption",
          "Exhaustion",
          "Limit",
          "Resource",
          "Scarcity",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "BUFFERING"
        ],
        "pathway_id": "P041-CP-001-e5040c5190b7",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-001-7b69a8100abd",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Overflow",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-001-c7ece90c1591",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Overflow",
          "Path",
          "Propagation",
          "Resistance",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-91e205cd9b87",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-a8d924146495",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Overflow",
          "Propagation",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-001-a2ff847c0b43",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Input",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Response",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-001-b22593c508fe",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-6cbd151d918f",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Overflow",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-63c743f46453",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "BuildUp",
          "Delay",
          "Input",
          "Limit",
          "Overflow",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-001-cdc39d6c268c",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Flow",
          "Input",
          "Loop",
          "Overflow",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-249514ca5b3b",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Exhaustion",
          "Input",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-9caa18f7b623",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Input",
          "Limit",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Response",
          "Signal",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-1367a99bf404",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Exhaustion",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-7a4aaa1b9bf0",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Flow",
          "Input",
          "Limit",
          "Overflow",
          "Path",
          "Resistance",
          "Source",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-ae5e485d9b41",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Consumption",
          "Exhaustion",
          "Input",
          "Limit",
          "Overflow",
          "Resource",
          "Scarcity",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-001-d47ef1855319",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-001-1e623772aec4",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-659342396c54",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Propagation",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-ca5a5215c4e9",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Propagation",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-001-e8a8f80341a5",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0"
        ],
        "supporting_motifs": [
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Loop",
          "Path",
          "Propagation",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-19fbc6a27f97",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-eafb58a57b24",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-bb4f31e9697e",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-ad36c27f1ca8",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Limit",
          "Path",
          "Propagation",
          "Resistance",
          "Source",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-757999c6f067",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Limit",
          "Propagation",
          "Resource",
          "Scarcity",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-001-f66093bf8b33",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Flow",
          "Input",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-48ab3b7b6e8d",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Loop",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-8b1ea10e5883",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Input",
          "Limit",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-c418d015905f",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Flow",
          "Input",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-14f55ae67b27",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Flow",
          "Input",
          "Limit",
          "Path",
          "Resistance",
          "Source",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-b8f5d6e9a3bb",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Limit",
          "Resource",
          "Scarcity",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "FEEDBACK",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-a59e23b59e64",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Exhaustion",
          "Flow",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "FEEDBACK",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-a7370da05288",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Flow",
          "Limit",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "FEEDBACK",
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-8530be9be464",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Consumption",
          "Exhaustion",
          "Limit",
          "Loop",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "FLOW",
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-483acd243403",
        "supporting_lineages": [
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Consumption",
          "Exhaustion",
          "Flow",
          "Limit",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-001-dd9561731ecf",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Overflow",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-001-b3a9b3cc0697",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Overflow",
          "Path",
          "Propagation",
          "Resistance",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-34b8a02ff637",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "BUFFERING",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-a3875d77944e",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "BuildUp",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Overflow",
          "Propagation",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-001-cc645c3fec70",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Loop",
          "Overflow",
          "Path",
          "Propagation",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-61396609d7f5",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Loop",
          "Overflow",
          "Propagation",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-8574c26207e9",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Loop",
          "Overflow",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-26c13be2cd87",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Flow",
          "Gain",
          "Input",
          "Overflow",
          "Path",
          "Propagation",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-f34904a1fa8b",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Limit",
          "Overflow",
          "Path",
          "Propagation",
          "Resistance",
          "Source",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-7618bc899ece",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Limit",
          "Overflow",
          "Propagation",
          "Resource",
          "Scarcity",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-001-a6d47999c1dd",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Flow",
          "Input",
          "Loop",
          "Overflow",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-2bbfac6f1608",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-111021e48646",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "BuildUp",
          "Delay",
          "Input",
          "Limit",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Response",
          "Signal",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-b590a42ed3a1",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-a32ecbd7829d",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "BuildUp",
          "Delay",
          "Flow",
          "Input",
          "Limit",
          "Overflow",
          "Path",
          "Resistance",
          "Source",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-1d87c1abee01",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Limit",
          "Overflow",
          "Resource",
          "Scarcity",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-859574e7fa7b",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Exhaustion",
          "Flow",
          "Input",
          "Loop",
          "Overflow",
          "Path",
          "Reinforcement",
          "Resistance",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-10ba9578c8e6",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Flow",
          "Input",
          "Limit",
          "Loop",
          "Overflow",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK",
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-acd846546293",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Consumption",
          "Exhaustion",
          "Input",
          "Limit",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "FLOW",
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-2f3bbc54761a",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Consumption",
          "Exhaustion",
          "Flow",
          "Input",
          "Limit",
          "Overflow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-001-dfd511b3c3ae",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Loop",
          "Path",
          "Propagation",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-f67a833b07ee",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-e77794632801",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-8dcac48c5abe",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Escalation",
          "Exhaustion",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-7ca09c5305bf",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Limit",
          "Path",
          "Propagation",
          "Resistance",
          "Source",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-c12fc793f681",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Consumption",
          "Delay",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Limit",
          "Propagation",
          "Resource",
          "Scarcity",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-adda801a8208",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Flow",
          "Gain",
          "Input",
          "Loop",
          "Path",
          "Propagation",
          "Reinforcement",
          "Resistance",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-17907e8a8fc6",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Limit",
          "Loop",
          "Path",
          "Propagation",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-c9ad23b44c1b",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Limit",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "FLOW",
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-a2c1f31f5394",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Flow",
          "Gain",
          "Input",
          "Limit",
          "Path",
          "Propagation",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-001-ddca78486424",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Flow",
          "Input",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-b2f91282086a",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Flow",
          "Input",
          "Limit",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-f89cab7ed68a",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Limit",
          "Loop",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "FLOW",
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-f84ef7cb4f35",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Flow",
          "Input",
          "Limit",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "FEEDBACK",
          "FLOW",
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-001-f27f223a6935",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Consumption",
          "Exhaustion",
          "Flow",
          "Limit",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Source",
          "StateChange",
          "Trigger"
        ]
      }
    ],
    "case_id": "P041-CP-001",
    "observation": "Output stays steady while a reserve absorbs variation. Once a limit is crossed, a returning signal reinforces decline and remaining capacity drains."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "COMPENSATION"
        ],
        "pathway_id": "P041-CP-002-f9325ea67cb0",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Counteraction",
          "Deviation",
          "Input",
          "Overflow",
          "Stabilization",
          "Storage",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-002-2adf054d509e",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Input",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Response",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-002-f71b344ed49f",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Cycle",
          "Delay",
          "Input",
          "Overflow",
          "Overshoot",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-002-cd420b735f22",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Input",
          "Limit",
          "Overflow",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-002-b7aea6e67d3e",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Deviation",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-002-e142b95c0716",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Cycle",
          "Delay",
          "Deviation",
          "Overshoot",
          "Stabilization",
          "State",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-002-438a9116b38c",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Counteraction",
          "Deviation",
          "Limit",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-002-34a33631e942",
        "supporting_lineages": [
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-002-caed32c89c94",
        "supporting_lineages": [
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Limit",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-002-56af625fd9f4",
        "supporting_lineages": [
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Cycle",
          "Delay",
          "Limit",
          "Overshoot",
          "State",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "COMPENSATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-002-23995635cb06",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Counteraction",
          "Deviation",
          "Input",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "Storage",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "COMPENSATION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-002-79a6cdef7522",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Counteraction",
          "Cycle",
          "Delay",
          "Deviation",
          "Input",
          "Overflow",
          "Overshoot",
          "Stabilization",
          "State",
          "Storage",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "COMPENSATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-002-c61298c5204e",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Counteraction",
          "Deviation",
          "Input",
          "Limit",
          "Overflow",
          "Stabilization",
          "StateChange",
          "Storage",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-002-0ca4d7553453",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Cycle",
          "Delay",
          "Input",
          "Loop",
          "Overflow",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-002-e65df9622104",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Input",
          "Limit",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Response",
          "Signal",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-002-94726b3cca98",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Cycle",
          "Delay",
          "Input",
          "Limit",
          "Overflow",
          "Overshoot",
          "State",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-002-dce6249bf4fa",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Cycle",
          "Delay",
          "Deviation",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "State",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-002-3e97b07ac656",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Counteraction",
          "Deviation",
          "Limit",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-002-0a16359faf4c",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Counteraction",
          "Cycle",
          "Delay",
          "Deviation",
          "Limit",
          "Overshoot",
          "Stabilization",
          "State",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "FEEDBACK",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-002-b31cb9ce64a0",
        "supporting_lineages": [
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Cycle",
          "Delay",
          "Limit",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "State",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "COMPENSATION",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-002-d68af4d5f809",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Counteraction",
          "Cycle",
          "Delay",
          "Deviation",
          "Input",
          "Loop",
          "Overflow",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "State",
          "Storage",
          "Substitution"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "COMPENSATION",
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-002-2e13bdf4d5d9",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Counteraction",
          "Deviation",
          "Input",
          "Limit",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "StateChange",
          "Storage",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "COMPENSATION",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-002-6eb0ce53eb03",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Counteraction",
          "Cycle",
          "Delay",
          "Deviation",
          "Input",
          "Limit",
          "Overflow",
          "Overshoot",
          "Stabilization",
          "State",
          "StateChange",
          "Storage",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-002-55e891cb01eb",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Cycle",
          "Delay",
          "Input",
          "Limit",
          "Loop",
          "Overflow",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "State",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "COMPENSATION",
          "FEEDBACK",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-002-5f5d8100d1f2",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Counteraction",
          "Cycle",
          "Delay",
          "Deviation",
          "Limit",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "State",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      }
    ],
    "case_id": "P041-CP-002",
    "observation": "Small errors collect quietly. At a critical point the controller flips state, correction overshoots, and the process swings above and below target."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "DIFFUSION"
        ],
        "pathway_id": "P041-CP-003-6efad7887a39",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8"
        ],
        "supporting_motifs": [
          "Dilution",
          "Escalation",
          "Gain",
          "Gradient",
          "Input",
          "Propagation",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-003-2d716d677035",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "DIFFUSION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-003-316084eae898",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Dilution",
          "Gradient",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "DIFFUSION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-003-cc36447d7946",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Dilution",
          "Escalation",
          "Gain",
          "Gradient",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "Source",
          "Spread"
        ]
      }
    ],
    "case_id": "P041-CP-003",
    "observation": "A faint signal spreads through adjacent groups, each relay magnifies it, and the returning response makes the next relay stronger."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION"
        ],
        "pathway_id": "P041-CP-004-0551747a8017",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Escalation",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING"
        ],
        "pathway_id": "P041-CP-004-7664623720a6",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Input",
          "Overflow",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "COMPENSATION"
        ],
        "pathway_id": "P041-CP-004-002498b667cc",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Counteraction",
          "Deviation",
          "Input",
          "Overflow",
          "Stabilization",
          "Storage",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-004-de2d35fcc28c",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-2c3d0184f747",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Exhaustion",
          "Input",
          "Overflow",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING"
        ],
        "pathway_id": "P041-CP-004-d44d1766ecf3",
        "supporting_lineages": [
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Propagation"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "COMPENSATION"
        ],
        "pathway_id": "P041-CP-004-b62a56dac013",
        "supporting_lineages": [
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Deviation",
          "Escalation",
          "Gain",
          "Input",
          "Propagation",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-004-b6bdb1987d3f",
        "supporting_lineages": [
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-16a8961303f1",
        "supporting_lineages": [
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Propagation",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION"
        ],
        "pathway_id": "P041-CP-004-d3eba22e1955",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Input",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-004-f7de4d5ddaa3",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Flow",
          "Input",
          "Path",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-9556c70444e9",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-004-31d767755cad",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Deviation",
          "Flow",
          "Path",
          "Resistance",
          "Source",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-0f86bf865d10",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Counteraction",
          "Deviation",
          "Exhaustion",
          "Resource",
          "Scarcity",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-39ab15256fe1",
        "supporting_lineages": [
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Exhaustion",
          "Flow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "BUFFERING"
        ],
        "pathway_id": "P041-CP-004-41ebe5ef3dc8",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "COMPENSATION"
        ],
        "pathway_id": "P041-CP-004-a2e588e0217e",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Counteraction",
          "Deviation",
          "Escalation",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Stabilization",
          "Storage",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-004-8760e4185376",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Overflow",
          "Path",
          "Propagation",
          "Resistance",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-9b4f01a34b6a",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "COMPENSATION"
        ],
        "pathway_id": "P041-CP-004-cf55e7799a16",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Counteraction",
          "Delay",
          "Deviation",
          "Input",
          "Overflow",
          "Stabilization",
          "Storage",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-004-cafa44006680",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-8102782680e2",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Overflow",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "COMPENSATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-004-495aab4031df",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Counteraction",
          "Deviation",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Source",
          "Stabilization",
          "Storage",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "COMPENSATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-c9318a61bcf5",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Counteraction",
          "Deviation",
          "Exhaustion",
          "Input",
          "Overflow",
          "Resource",
          "Scarcity",
          "Stabilization",
          "Storage",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-bcfab6fe4643",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Exhaustion",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "COMPENSATION"
        ],
        "pathway_id": "P041-CP-004-b50f1be2b760",
        "supporting_lineages": [
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Escalation",
          "Gain",
          "Input",
          "Propagation",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-004-e79113e5ce39",
        "supporting_lineages": [
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-91ecf331795d",
        "supporting_lineages": [
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Propagation",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "COMPENSATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-004-a80e8c87d4ec",
        "supporting_lineages": [
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Deviation",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Source",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "COMPENSATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-6143cad50367",
        "supporting_lineages": [
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Counteraction",
          "Deviation",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Propagation",
          "Resource",
          "Scarcity",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-6781fba3789f",
        "supporting_lineages": [
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-004-bbdde7a87290",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Flow",
          "Input",
          "Path",
          "Resistance",
          "Source",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-3d72436ee0ae",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Counteraction",
          "Delay",
          "Deviation",
          "Exhaustion",
          "Input",
          "Resource",
          "Scarcity",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-6b59884ad7b6",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Flow",
          "Input",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-65a3de6dc490",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Counteraction",
          "Deviation",
          "Exhaustion",
          "Flow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "BUFFERING",
          "COMPENSATION"
        ],
        "pathway_id": "P041-CP-004-cf84866d38f8",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Counteraction",
          "Delay",
          "Deviation",
          "Escalation",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Stabilization",
          "Storage",
          "Substitution"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-004-e91a1fc5c823",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Overflow",
          "Path",
          "Propagation",
          "Resistance",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-24fa88d565e5",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "COMPENSATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-004-884e2fabf8e5",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Counteraction",
          "Deviation",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Overflow",
          "Path",
          "Propagation",
          "Resistance",
          "Source",
          "Stabilization",
          "Storage",
          "Substitution"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "COMPENSATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-fc902787e7b5",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Counteraction",
          "Deviation",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Resource",
          "Scarcity",
          "Stabilization",
          "Storage",
          "Substitution"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-8d7287bed821",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Flow",
          "Gain",
          "Input",
          "Overflow",
          "Path",
          "Propagation",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "COMPENSATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-004-80aed7bb4dbe",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Counteraction",
          "Delay",
          "Deviation",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Source",
          "Stabilization",
          "Storage",
          "Substitution"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "COMPENSATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-38ff201501f4",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Counteraction",
          "Delay",
          "Deviation",
          "Exhaustion",
          "Input",
          "Overflow",
          "Resource",
          "Scarcity",
          "Stabilization",
          "Storage",
          "Substitution"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-3e3eb1a747e8",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "COMPENSATION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-5d04acc70c91",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:2f351cd2b5c75d68",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Counteraction",
          "Deviation",
          "Exhaustion",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Stabilization",
          "Storage",
          "Substitution"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "COMPENSATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-004-030394569572",
        "supporting_lineages": [
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Source",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "COMPENSATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-29ebf4b33de9",
        "supporting_lineages": [
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Counteraction",
          "Delay",
          "Deviation",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Propagation",
          "Resource",
          "Scarcity",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-2d701a95f5f3",
        "supporting_lineages": [
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Escalation",
          "Exhaustion",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "COMPENSATION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-488da83e8421",
        "supporting_lineages": [
          "pond:amplification:3206405517eb80fb",
          "pond:amplification:822274423d90b909",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Counteraction",
          "Deviation",
          "Escalation",
          "Exhaustion",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-004-f6d186a49a50",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Counteraction",
          "Delay",
          "Deviation",
          "Exhaustion",
          "Flow",
          "Input",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Stabilization",
          "Substitution"
        ]
      }
    ],
    "case_id": "P041-CP-004",
    "observation": "A backup routine hides demand growth. Stored work piles up behind it, then spare capacity drains and output falls sharply."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING"
        ],
        "pathway_id": "P041-CP-005-072beaafe5b3",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Input",
          "Overflow",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-005-c1532d22cf9a",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-005-c0380c0656ae",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Exhaustion",
          "Input",
          "Overflow",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-005-7526fca85bc2",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Flow",
          "Input",
          "Path",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-005-140a4dcd164e",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-005-6dbae6cf9ff1",
        "supporting_lineages": [
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Exhaustion",
          "Flow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-005-664b8f3a49c3",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-005-a88a9331ea62",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Overflow",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-005-a03dc19a7106",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Exhaustion",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-005-71ed57f4e493",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Flow",
          "Input",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-005-4e1e59e811e1",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Storage"
        ]
      }
    ],
    "case_id": "P041-CP-005",
    "observation": "A passage narrows while an upstream reserve absorbs arrivals. After the reserve fills, backlog grows and downstream output starves."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "LOAD_TRANSFER"
        ],
        "pathway_id": "P041-CP-006-c3c5b7471b47",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044"
        ],
        "supporting_motifs": [
          "Concentration",
          "Counteraction",
          "Deviation",
          "Distribution",
          "Failure",
          "Load",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-006-dc50c7efbc20",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Deviation",
          "Failure",
          "Friction",
          "Rotation",
          "Stabilization",
          "Substitution",
          "Support"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-006-48c8a35c9891",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Counteraction",
          "Deviation",
          "Limit",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "LOAD_TRANSFER",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-006-10b61fedbf4c",
        "supporting_lineages": [
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Concentration",
          "Distribution",
          "Failure",
          "Friction",
          "Load",
          "Rotation",
          "Support"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "LOAD_TRANSFER",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-006-637f50759c33",
        "supporting_lineages": [
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Distribution",
          "Failure",
          "Limit",
          "Load",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "SUPPORTED_ROTATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-006-316eca5d9830",
        "supporting_lineages": [
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Failure",
          "Friction",
          "Limit",
          "Rotation",
          "StateChange",
          "Support",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "LOAD_TRANSFER",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-006-1c0ceb6cc7b5",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Concentration",
          "Counteraction",
          "Deviation",
          "Distribution",
          "Failure",
          "Friction",
          "Load",
          "Rotation",
          "Stabilization",
          "Substitution",
          "Support"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "LOAD_TRANSFER",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-006-3f51b7c89841",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Counteraction",
          "Deviation",
          "Distribution",
          "Failure",
          "Limit",
          "Load",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "SUPPORTED_ROTATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-006-1317a7a5c978",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Counteraction",
          "Deviation",
          "Failure",
          "Friction",
          "Limit",
          "Rotation",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Support",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "LOAD_TRANSFER",
          "SUPPORTED_ROTATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-006-5da9e75c7181",
        "supporting_lineages": [
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Distribution",
          "Failure",
          "Friction",
          "Limit",
          "Load",
          "Rotation",
          "StateChange",
          "Support",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "COMPENSATION",
          "LOAD_TRANSFER",
          "SUPPORTED_ROTATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-006-7edf743726e1",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Counteraction",
          "Deviation",
          "Distribution",
          "Failure",
          "Friction",
          "Limit",
          "Load",
          "Rotation",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Support",
          "Trigger"
        ]
      }
    ],
    "case_id": "P041-CP-006",
    "observation": "A turning support grows rough. The controller adds drive to offset drag, heat rises, and a critical point is crossed."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "LOAD_TRANSFER"
        ],
        "pathway_id": "P041-CP-007-2365b5c1a4b3",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Concentration",
          "Distribution",
          "Failure",
          "Input",
          "Load",
          "Overflow",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-007-ad7d099fbfdc",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Input",
          "Limit",
          "Overflow",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "LOAD_TRANSFER",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-007-07872d2ae5d2",
        "supporting_lineages": [
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Distribution",
          "Failure",
          "Limit",
          "Load",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "LOAD_TRANSFER",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-007-984c68270e55",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Concentration",
          "Distribution",
          "Failure",
          "Input",
          "Limit",
          "Load",
          "Overflow",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      }
    ],
    "case_id": "P041-CP-007",
    "observation": "A bracket takes extra demand. Tiny cracks collect, force shifts to one point, and a final limit crossing starts collapse."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION"
        ],
        "pathway_id": "P041-CP-008-7eb13faf0d9a",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Escalation",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING"
        ],
        "pathway_id": "P041-CP-008-187556411bd4",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Input",
          "Overflow",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-008-28b5fa8c0805",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Input",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Response",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-008-08884cf08ba3",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-1901b78e513c",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Exhaustion",
          "Input",
          "Overflow",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING"
        ],
        "pathway_id": "P041-CP-008-f3e294d2b4c9",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Propagation"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-008-d9569622a51e",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-008-a3d3ac30e0cf",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-5c3f7bb260d2",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Propagation",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-008-ba16d523de36",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Input",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-008-0bf1fd6f7499",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Flow",
          "Input",
          "Path",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-676641d7b218",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-008-a4125cf90e9a",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Flow",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-4252ffb95444",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Exhaustion",
          "Loop",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-32a9359d9ec1",
        "supporting_lineages": [
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Exhaustion",
          "Flow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "BUFFERING"
        ],
        "pathway_id": "P041-CP-008-9df603d08e87",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-008-838d4d721ea5",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Overflow",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-008-43c340f4db4a",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Overflow",
          "Path",
          "Propagation",
          "Resistance",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-ebd983fad837",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-008-3ce886354b02",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Input",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Response",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-008-75f441090c55",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-e7978380f3da",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Overflow",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-008-004ca87deff4",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Flow",
          "Input",
          "Loop",
          "Overflow",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-6a7dcb058814",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Exhaustion",
          "Input",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-81242f340efa",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Exhaustion",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-008-98aa1374f03e",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-008-9b5dafe229aa",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-0fa09eb4853c",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Propagation",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-008-cff38e5d9628",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Loop",
          "Path",
          "Propagation",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-d2b5be1eeca7",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-7b3cc59b55f5",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-008-53dbdd363781",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Flow",
          "Input",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-c68a2022d5f7",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Loop",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-72195418069c",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Flow",
          "Input",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "FEEDBACK",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-18e4cad7cfe4",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Exhaustion",
          "Flow",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-008-12184d73a55b",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Overflow",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-008-95a1a5cde168",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Overflow",
          "Path",
          "Propagation",
          "Resistance",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-8e92a48b4934",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-008-908da61ebe3b",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Loop",
          "Overflow",
          "Path",
          "Propagation",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-a574cc64a41c",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Loop",
          "Overflow",
          "Propagation",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-cbb0ac6f0fc9",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Flow",
          "Gain",
          "Input",
          "Overflow",
          "Path",
          "Propagation",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-008-b725f3dc9c9c",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Flow",
          "Input",
          "Loop",
          "Overflow",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-dc150e555421",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-fd6454ea6cb7",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-bcbaa6528096",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Exhaustion",
          "Flow",
          "Input",
          "Loop",
          "Overflow",
          "Path",
          "Reinforcement",
          "Resistance",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-008-ca2d920a3670",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Loop",
          "Path",
          "Propagation",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-2be320b1d049",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-148d96e68166",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Escalation",
          "Exhaustion",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-928bd097827f",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Flow",
          "Gain",
          "Input",
          "Loop",
          "Path",
          "Propagation",
          "Reinforcement",
          "Resistance",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-008-ec23d3948e36",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Flow",
          "Input",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Source"
        ]
      }
    ],
    "case_id": "P041-CP-008",
    "observation": "A reserve drains while a return signal asks for more output. The extra output accelerates use and magnifies the final drop."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION"
        ],
        "pathway_id": "P041-CP-009-3101bc5d2049",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Input",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-009-f027b2401612",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Input",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-009-88b3e4d35495",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Input",
          "Overshoot",
          "State"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-009-d5e0bda18270",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Deviation",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-009-7a435930216e",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Cycle",
          "Delay",
          "Deviation",
          "Overshoot",
          "Stabilization",
          "State",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-009-c5fc98e04147",
        "supporting_lineages": [
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-009-6a2a13cbe979",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Input",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-009-8b028e3077d0",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Cycle",
          "Delay",
          "Deviation",
          "Input",
          "Overshoot",
          "Stabilization",
          "State",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-009-222f8c7c1988",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Input",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-009-875cf6ddc17a",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Cycle",
          "Delay",
          "Deviation",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "State",
          "Substitution"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-009-a067fad4336a",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Cycle",
          "Delay",
          "Deviation",
          "Input",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "State",
          "Substitution"
        ]
      }
    ],
    "case_id": "P041-CP-009",
    "observation": "Delay in a correction loop makes each adjustment arrive late. The response overshoots, reverses, and repeats in a rhythm."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING"
        ],
        "pathway_id": "P041-CP-010-fc63ac8e529d",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Input",
          "Overflow",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "DIFFUSION"
        ],
        "pathway_id": "P041-CP-010-32df7475c402",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:diffusion:1e1929a4abb9bd0d",
          "pond:diffusion:5fceeaf81812122f"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Dilution",
          "Gradient",
          "Input",
          "Overflow",
          "Source",
          "Spread",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-010-afb6478fe70e",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-010-7135842539da",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:resource_depletion:55d78a46424150c9",
          "pond:resource_depletion:772a8746b40af786"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Exhaustion",
          "Input",
          "Overflow",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "DIFFUSION"
        ],
        "pathway_id": "P041-CP-010-dd19c83500f4",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:1e1929a4abb9bd0d",
          "pond:diffusion:5fceeaf81812122f"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Dilution",
          "Gradient",
          "Input",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-010-e926ca859619",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Flow",
          "Input",
          "Path",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-010-46e73a830b9a",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:55d78a46424150c9",
          "pond:resource_depletion:772a8746b40af786"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "DIFFUSION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-010-a9d3851553f7",
        "supporting_lineages": [
          "pond:diffusion:1e1929a4abb9bd0d",
          "pond:diffusion:5fceeaf81812122f",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Dilution",
          "Flow",
          "Gradient",
          "Path",
          "Resistance",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "DIFFUSION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-010-721e6b0e8c5c",
        "supporting_lineages": [
          "pond:diffusion:1e1929a4abb9bd0d",
          "pond:diffusion:5fceeaf81812122f",
          "pond:resource_depletion:55d78a46424150c9",
          "pond:resource_depletion:772a8746b40af786"
        ],
        "supporting_motifs": [
          "Consumption",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Resource",
          "Scarcity",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-010-55734f298ca0",
        "supporting_lineages": [
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:55d78a46424150c9",
          "pond:resource_depletion:772a8746b40af786"
        ],
        "supporting_motifs": [
          "Consumption",
          "Exhaustion",
          "Flow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "DIFFUSION"
        ],
        "pathway_id": "P041-CP-010-96b06bd77394",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:1e1929a4abb9bd0d",
          "pond:diffusion:5fceeaf81812122f"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Dilution",
          "Gradient",
          "Input",
          "Overflow",
          "Source",
          "Spread",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-010-f06e2fc1575e",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-010-219bb11888d9",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:55d78a46424150c9",
          "pond:resource_depletion:772a8746b40af786"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Overflow",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "DIFFUSION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-010-d8bbc53be019",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:diffusion:1e1929a4abb9bd0d",
          "pond:diffusion:5fceeaf81812122f",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Dilution",
          "Flow",
          "Gradient",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Source",
          "Spread",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "DIFFUSION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-010-a33679c84e12",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:diffusion:1e1929a4abb9bd0d",
          "pond:diffusion:5fceeaf81812122f",
          "pond:resource_depletion:55d78a46424150c9",
          "pond:resource_depletion:772a8746b40af786"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Input",
          "Overflow",
          "Resource",
          "Scarcity",
          "Source",
          "Spread",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-010-9d701b3e8a8b",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:55d78a46424150c9",
          "pond:resource_depletion:772a8746b40af786"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Exhaustion",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "DIFFUSION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-010-238e4f10f6ba",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:1e1929a4abb9bd0d",
          "pond:diffusion:5fceeaf81812122f",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Dilution",
          "Flow",
          "Gradient",
          "Input",
          "Path",
          "Resistance",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "DIFFUSION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-010-c9905c137959",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:1e1929a4abb9bd0d",
          "pond:diffusion:5fceeaf81812122f",
          "pond:resource_depletion:55d78a46424150c9",
          "pond:resource_depletion:772a8746b40af786"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Input",
          "Resource",
          "Scarcity",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-010-46ba8e92ee5b",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:55d78a46424150c9",
          "pond:resource_depletion:772a8746b40af786"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Flow",
          "Input",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "DIFFUSION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-010-b8ede0cadffc",
        "supporting_lineages": [
          "pond:diffusion:1e1929a4abb9bd0d",
          "pond:diffusion:5fceeaf81812122f",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:55d78a46424150c9",
          "pond:resource_depletion:772a8746b40af786"
        ],
        "supporting_motifs": [
          "Consumption",
          "Dilution",
          "Exhaustion",
          "Flow",
          "Gradient",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "DIFFUSION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-010-abe6baccf311",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:1e1929a4abb9bd0d",
          "pond:diffusion:5fceeaf81812122f",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Dilution",
          "Flow",
          "Gradient",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Source",
          "Spread",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "DIFFUSION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-010-5f3645cb90ed",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:1e1929a4abb9bd0d",
          "pond:diffusion:5fceeaf81812122f",
          "pond:resource_depletion:55d78a46424150c9",
          "pond:resource_depletion:772a8746b40af786"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Input",
          "Overflow",
          "Resource",
          "Scarcity",
          "Source",
          "Spread",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-010-9b739af7179c",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:55d78a46424150c9",
          "pond:resource_depletion:772a8746b40af786"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "DIFFUSION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-010-c58a861c15e0",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:diffusion:1e1929a4abb9bd0d",
          "pond:diffusion:5fceeaf81812122f",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:55d78a46424150c9",
          "pond:resource_depletion:772a8746b40af786"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Dilution",
          "Exhaustion",
          "Flow",
          "Gradient",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Spread",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "DIFFUSION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-010-700bb01ac9d5",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:1e1929a4abb9bd0d",
          "pond:diffusion:5fceeaf81812122f",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:55d78a46424150c9",
          "pond:resource_depletion:772a8746b40af786"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Dilution",
          "Exhaustion",
          "Flow",
          "Gradient",
          "Input",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Spread"
        ]
      }
    ],
    "case_id": "P041-CP-010",
    "observation": "A contaminant leaks from one source and spreads down a gradient. A cleanup reserve absorbs it at first, then capacity is exhausted and traces appear everywhere."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING"
        ],
        "pathway_id": "P041-CP-011-aa5e9f5561de",
        "supporting_lineages": [
          "pond:amplification:49a80c094f40fa16",
          "pond:amplification:669bc533991b7e59",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Propagation"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-011-319c0de28c86",
        "supporting_lineages": [
          "pond:amplification:49a80c094f40fa16",
          "pond:amplification:669bc533991b7e59",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-011-760658f9b46f",
        "supporting_lineages": [
          "pond:amplification:49a80c094f40fa16",
          "pond:amplification:669bc533991b7e59",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550"
        ],
        "supporting_motifs": [
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-011-bc7d4c79e4f4",
        "supporting_lineages": [
          "pond:amplification:49a80c094f40fa16",
          "pond:amplification:669bc533991b7e59",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Overshoot",
          "Propagation",
          "State"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-011-bf032b5375f8",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Input",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-011-2acbddb3e940",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Flow",
          "Input",
          "Path",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-011-9898faa07ee8",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Input",
          "Overshoot",
          "State"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-011-2d7fe327309d",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550"
        ],
        "supporting_motifs": [
          "Flow",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-011-4dfc29ce56e6",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FLOW",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-011-0099d957b32d",
        "supporting_lineages": [
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Flow",
          "Overshoot",
          "Path",
          "Resistance",
          "Source",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-011-4e68d174f821",
        "supporting_lineages": [
          "pond:amplification:49a80c094f40fa16",
          "pond:amplification:669bc533991b7e59",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-011-27b95824e4ae",
        "supporting_lineages": [
          "pond:amplification:49a80c094f40fa16",
          "pond:amplification:669bc533991b7e59",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-011-991a282f30ca",
        "supporting_lineages": [
          "pond:amplification:49a80c094f40fa16",
          "pond:amplification:669bc533991b7e59",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Overshoot",
          "Propagation",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-011-3afd59d6d1c2",
        "supporting_lineages": [
          "pond:amplification:49a80c094f40fa16",
          "pond:amplification:669bc533991b7e59",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550"
        ],
        "supporting_motifs": [
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Loop",
          "Path",
          "Propagation",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-011-c43f379498ae",
        "supporting_lineages": [
          "pond:amplification:49a80c094f40fa16",
          "pond:amplification:669bc533991b7e59",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Overshoot",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FLOW",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-011-f2fcfc9f8506",
        "supporting_lineages": [
          "pond:amplification:49a80c094f40fa16",
          "pond:amplification:669bc533991b7e59",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Overshoot",
          "Path",
          "Propagation",
          "Resistance",
          "Source",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-011-d314980a55c3",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Flow",
          "Input",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-011-707a65273ba2",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Input",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FLOW",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-011-d393ab414c37",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Flow",
          "Input",
          "Overshoot",
          "Path",
          "Resistance",
          "Source",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "FEEDBACK",
          "FLOW",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-011-2a9c28fda2e9",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Flow",
          "Loop",
          "Overshoot",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "State"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-011-21be353127c5",
        "supporting_lineages": [
          "pond:amplification:49a80c094f40fa16",
          "pond:amplification:669bc533991b7e59",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Loop",
          "Path",
          "Propagation",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-011-0cd2f4a5f8cb",
        "supporting_lineages": [
          "pond:amplification:49a80c094f40fa16",
          "pond:amplification:669bc533991b7e59",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Overshoot",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FLOW",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-011-6b065bc8a9f7",
        "supporting_lineages": [
          "pond:amplification:49a80c094f40fa16",
          "pond:amplification:669bc533991b7e59",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Overshoot",
          "Path",
          "Propagation",
          "Resistance",
          "Source",
          "State"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "FLOW",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-011-385cd8a2e58e",
        "supporting_lineages": [
          "pond:amplification:49a80c094f40fa16",
          "pond:amplification:669bc533991b7e59",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Loop",
          "Overshoot",
          "Path",
          "Propagation",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "State"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "FLOW",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-011-1ed4c2419521",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Flow",
          "Input",
          "Loop",
          "Overshoot",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "State"
        ]
      }
    ],
    "case_id": "P041-CP-011",
    "observation": "A queue surge is cushioned by slack. Once slack is gone, the narrowed route creates backlog and returning delay signals push more arrivals into the same route."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "DIFFUSION",
          "LOAD_TRANSFER"
        ],
        "pathway_id": "P041-CP-012-90e7f02f0cdc",
        "supporting_lineages": [
          "pond:diffusion:1295d8896f93fcd8",
          "pond:diffusion:558b4378784d5a7f",
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044"
        ],
        "supporting_motifs": [
          "Concentration",
          "Dilution",
          "Distribution",
          "Failure",
          "Gradient",
          "Load",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "DIFFUSION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-012-baf90a470320",
        "supporting_lineages": [
          "pond:diffusion:1295d8896f93fcd8",
          "pond:diffusion:558b4378784d5a7f",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Dilution",
          "Failure",
          "Friction",
          "Gradient",
          "Rotation",
          "Source",
          "Spread",
          "Support"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "DIFFUSION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-012-870c770a9a60",
        "supporting_lineages": [
          "pond:diffusion:1295d8896f93fcd8",
          "pond:diffusion:558b4378784d5a7f",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Dilution",
          "Gradient",
          "Limit",
          "Source",
          "Spread",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "LOAD_TRANSFER",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-012-513913249e65",
        "supporting_lineages": [
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Concentration",
          "Distribution",
          "Failure",
          "Friction",
          "Load",
          "Rotation",
          "Support"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "LOAD_TRANSFER",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-012-af2756a80a53",
        "supporting_lineages": [
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Distribution",
          "Failure",
          "Limit",
          "Load",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "SUPPORTED_ROTATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-012-73655ad7e12c",
        "supporting_lineages": [
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Failure",
          "Friction",
          "Limit",
          "Rotation",
          "StateChange",
          "Support",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "DIFFUSION",
          "LOAD_TRANSFER",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-012-683fa94a25e1",
        "supporting_lineages": [
          "pond:diffusion:1295d8896f93fcd8",
          "pond:diffusion:558b4378784d5a7f",
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Concentration",
          "Dilution",
          "Distribution",
          "Failure",
          "Friction",
          "Gradient",
          "Load",
          "Rotation",
          "Source",
          "Spread",
          "Support"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "DIFFUSION",
          "LOAD_TRANSFER",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-012-88bbfec4ad5d",
        "supporting_lineages": [
          "pond:diffusion:1295d8896f93fcd8",
          "pond:diffusion:558b4378784d5a7f",
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Dilution",
          "Distribution",
          "Failure",
          "Gradient",
          "Limit",
          "Load",
          "Source",
          "Spread",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "DIFFUSION",
          "SUPPORTED_ROTATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-012-9bc737692be6",
        "supporting_lineages": [
          "pond:diffusion:1295d8896f93fcd8",
          "pond:diffusion:558b4378784d5a7f",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Dilution",
          "Failure",
          "Friction",
          "Gradient",
          "Limit",
          "Rotation",
          "Source",
          "Spread",
          "StateChange",
          "Support",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "LOAD_TRANSFER",
          "SUPPORTED_ROTATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-012-ee88c90f2fca",
        "supporting_lineages": [
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Distribution",
          "Failure",
          "Friction",
          "Limit",
          "Load",
          "Rotation",
          "StateChange",
          "Support",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "DIFFUSION",
          "LOAD_TRANSFER",
          "SUPPORTED_ROTATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-012-e57a6db4a72d",
        "supporting_lineages": [
          "pond:diffusion:1295d8896f93fcd8",
          "pond:diffusion:558b4378784d5a7f",
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Dilution",
          "Distribution",
          "Failure",
          "Friction",
          "Gradient",
          "Limit",
          "Load",
          "Rotation",
          "Source",
          "Spread",
          "StateChange",
          "Support",
          "Trigger"
        ]
      }
    ],
    "case_id": "P041-CP-012",
    "observation": "Heat spreads from one contact point. Drag in the turning support rises, a critical point is crossed, and the part locks."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "COMPENSATION"
        ],
        "pathway_id": "P041-CP-013-345f5b7e4218",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Counteraction",
          "Deviation",
          "Input",
          "Overflow",
          "Stabilization",
          "Storage",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "LOAD_TRANSFER"
        ],
        "pathway_id": "P041-CP-013-2a2105a2684c",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:load_transfer:100c18cc1d1c2bf9",
          "pond:load_transfer:38ae4961e6268ecd"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Concentration",
          "Distribution",
          "Failure",
          "Input",
          "Load",
          "Overflow",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-013-580127338632",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Input",
          "Limit",
          "Overflow",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "LOAD_TRANSFER"
        ],
        "pathway_id": "P041-CP-013-4c1479e828fd",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:load_transfer:100c18cc1d1c2bf9",
          "pond:load_transfer:38ae4961e6268ecd"
        ],
        "supporting_motifs": [
          "Concentration",
          "Counteraction",
          "Deviation",
          "Distribution",
          "Failure",
          "Load",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-013-a7c4eb322998",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Counteraction",
          "Deviation",
          "Limit",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "LOAD_TRANSFER",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-013-5aa9d28c0ea4",
        "supporting_lineages": [
          "pond:load_transfer:100c18cc1d1c2bf9",
          "pond:load_transfer:38ae4961e6268ecd",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Distribution",
          "Failure",
          "Limit",
          "Load",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "COMPENSATION",
          "LOAD_TRANSFER"
        ],
        "pathway_id": "P041-CP-013-89fdd5c8c823",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:load_transfer:100c18cc1d1c2bf9",
          "pond:load_transfer:38ae4961e6268ecd"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Concentration",
          "Counteraction",
          "Deviation",
          "Distribution",
          "Failure",
          "Input",
          "Load",
          "Overflow",
          "Stabilization",
          "Storage",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "COMPENSATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-013-c10c93aefbea",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Counteraction",
          "Deviation",
          "Input",
          "Limit",
          "Overflow",
          "Stabilization",
          "StateChange",
          "Storage",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "LOAD_TRANSFER",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-013-4f6a662d87ce",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:load_transfer:100c18cc1d1c2bf9",
          "pond:load_transfer:38ae4961e6268ecd",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Concentration",
          "Distribution",
          "Failure",
          "Input",
          "Limit",
          "Load",
          "Overflow",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "LOAD_TRANSFER",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-013-c34c107f6211",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:load_transfer:100c18cc1d1c2bf9",
          "pond:load_transfer:38ae4961e6268ecd",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Counteraction",
          "Deviation",
          "Distribution",
          "Failure",
          "Limit",
          "Load",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "COMPENSATION",
          "LOAD_TRANSFER",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-013-3a24c94768aa",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:load_transfer:100c18cc1d1c2bf9",
          "pond:load_transfer:38ae4961e6268ecd",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Concentration",
          "Counteraction",
          "Deviation",
          "Distribution",
          "Failure",
          "Input",
          "Limit",
          "Load",
          "Overflow",
          "Stabilization",
          "StateChange",
          "Storage",
          "Substitution",
          "Trigger"
        ]
      }
    ],
    "case_id": "P041-CP-013",
    "observation": "Tiny demand shifts are masked by an offsetting brace. Strain still collects at one lug until the bracket tears from a local point."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-014-84b508e6ce34",
        "supporting_lineages": [
          "pond:amplification:4f7102b33900c26a",
          "pond:amplification:7a741fe9eb0dd270",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-014-0897cb26dd68",
        "supporting_lineages": [
          "pond:amplification:4f7102b33900c26a",
          "pond:amplification:7a741fe9eb0dd270",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Propagation",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-014-df94268b9d2a",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Limit",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-014-0f0e36a495c0",
        "supporting_lineages": [
          "pond:amplification:4f7102b33900c26a",
          "pond:amplification:7a741fe9eb0dd270",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "StateChange",
          "Trigger"
        ]
      }
    ],
    "case_id": "P041-CP-014",
    "observation": "A weak alarm signal is magnified through repeated relays. Once it crosses a trip point, the returning response reinforces further escalation."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING"
        ],
        "pathway_id": "P041-CP-015-2277e0d9fc94",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Input",
          "Overflow",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-015-91ed56421f8c",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Cycle",
          "Delay",
          "Input",
          "Overflow",
          "Overshoot",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-015-4f8061103720",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Input",
          "Overshoot",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-015-677d38164f64",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Cycle",
          "Delay",
          "Input",
          "Overflow",
          "Overshoot",
          "State",
          "Storage"
        ]
      }
    ],
    "case_id": "P041-CP-015",
    "observation": "Inventory builds while demand is cushioned by slack. Delayed replenishment overshoots, stock swings from shortage to excess, and the pattern repeats."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "DIFFUSION"
        ],
        "pathway_id": "P041-CP-016-e3442c71fc2b",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:diffusion:1e1929a4abb9bd0d",
          "pond:diffusion:5fceeaf81812122f"
        ],
        "supporting_motifs": [
          "Dilution",
          "Escalation",
          "Gain",
          "Gradient",
          "Input",
          "Propagation",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-016-ad7911341a24",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-016-f637b04f0db5",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:resource_depletion:55d78a46424150c9",
          "pond:resource_depletion:772a8746b40af786"
        ],
        "supporting_motifs": [
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Propagation",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "DIFFUSION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-016-1673cf909782",
        "supporting_lineages": [
          "pond:diffusion:1e1929a4abb9bd0d",
          "pond:diffusion:5fceeaf81812122f",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Dilution",
          "Flow",
          "Gradient",
          "Path",
          "Resistance",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "DIFFUSION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-016-495f0858ad50",
        "supporting_lineages": [
          "pond:diffusion:1e1929a4abb9bd0d",
          "pond:diffusion:5fceeaf81812122f",
          "pond:resource_depletion:55d78a46424150c9",
          "pond:resource_depletion:772a8746b40af786"
        ],
        "supporting_motifs": [
          "Consumption",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Resource",
          "Scarcity",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-016-ea0245437de3",
        "supporting_lineages": [
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:55d78a46424150c9",
          "pond:resource_depletion:772a8746b40af786"
        ],
        "supporting_motifs": [
          "Consumption",
          "Exhaustion",
          "Flow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "DIFFUSION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-016-73c8b22c9bbd",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:diffusion:1e1929a4abb9bd0d",
          "pond:diffusion:5fceeaf81812122f",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Dilution",
          "Escalation",
          "Flow",
          "Gain",
          "Gradient",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "DIFFUSION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-016-cf72af247d8a",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:diffusion:1e1929a4abb9bd0d",
          "pond:diffusion:5fceeaf81812122f",
          "pond:resource_depletion:55d78a46424150c9",
          "pond:resource_depletion:772a8746b40af786"
        ],
        "supporting_motifs": [
          "Consumption",
          "Dilution",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Gradient",
          "Input",
          "Propagation",
          "Resource",
          "Scarcity",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-016-21a5c33a1cfd",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:55d78a46424150c9",
          "pond:resource_depletion:772a8746b40af786"
        ],
        "supporting_motifs": [
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "DIFFUSION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-016-fd8752d7b144",
        "supporting_lineages": [
          "pond:diffusion:1e1929a4abb9bd0d",
          "pond:diffusion:5fceeaf81812122f",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:55d78a46424150c9",
          "pond:resource_depletion:772a8746b40af786"
        ],
        "supporting_motifs": [
          "Consumption",
          "Dilution",
          "Exhaustion",
          "Flow",
          "Gradient",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "DIFFUSION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-016-18e479776872",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:diffusion:1e1929a4abb9bd0d",
          "pond:diffusion:5fceeaf81812122f",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:resource_depletion:55d78a46424150c9",
          "pond:resource_depletion:772a8746b40af786"
        ],
        "supporting_motifs": [
          "Consumption",
          "Dilution",
          "Escalation",
          "Exhaustion",
          "Flow",
          "Gain",
          "Gradient",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Spread"
        ]
      }
    ],
    "case_id": "P041-CP-016",
    "observation": "A rumor starts at one source, spreads outward, gains strength through each relay, and eventually drains attention from the original task."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-017-b46779220aa4",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Flow",
          "Input",
          "Path",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-017-d51fc5314f6a",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-017-5226bdf1d365",
        "supporting_lineages": [
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Exhaustion",
          "Flow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-017-f050a176c913",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Flow",
          "Input",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      }
    ],
    "case_id": "P041-CP-017",
    "observation": "Manual workarounds hide a queue. Workaround capacity drains, then throughput drops through a restricted handoff."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION"
        ],
        "pathway_id": "P041-CP-018-bf6e480d423a",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Escalation",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-018-713e83341679",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Input",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Response",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-018-7f39c2039e4a",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:oscillation:375bfcf0455750c7",
          "pond:oscillation:4fbec22bb8891daa"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Cycle",
          "Delay",
          "Input",
          "Overflow",
          "Overshoot",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-018-27613d1defe7",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Failure",
          "Friction",
          "Input",
          "Overflow",
          "Rotation",
          "Storage",
          "Support"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-018-0097f9e51738",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-018-1221a223232a",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:oscillation:375bfcf0455750c7",
          "pond:oscillation:4fbec22bb8891daa"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Overshoot",
          "Propagation",
          "State"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-018-e4dc49de6c85",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Escalation",
          "Failure",
          "Friction",
          "Gain",
          "Input",
          "Propagation",
          "Rotation",
          "Support"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-018-638ca220ae4a",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:375bfcf0455750c7",
          "pond:oscillation:4fbec22bb8891daa"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FEEDBACK",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-018-94bd561c79e5",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Failure",
          "Friction",
          "Loop",
          "Reinforcement",
          "Response",
          "Rotation",
          "Signal",
          "Support"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "OSCILLATION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-018-1065a011f57b",
        "supporting_lineages": [
          "pond:oscillation:375bfcf0455750c7",
          "pond:oscillation:4fbec22bb8891daa",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Failure",
          "Friction",
          "Overshoot",
          "Rotation",
          "State",
          "Support"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-018-828fc56c5710",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Overflow",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-018-c21cde11cedc",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:oscillation:375bfcf0455750c7",
          "pond:oscillation:4fbec22bb8891daa"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Overflow",
          "Overshoot",
          "Propagation",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-018-a22e9f19032a",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Escalation",
          "Failure",
          "Friction",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Rotation",
          "Storage",
          "Support"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-018-057a394934c3",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:375bfcf0455750c7",
          "pond:oscillation:4fbec22bb8891daa"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Cycle",
          "Delay",
          "Input",
          "Loop",
          "Overflow",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-018-2b0346d02a4d",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Failure",
          "Friction",
          "Input",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Response",
          "Rotation",
          "Signal",
          "Storage",
          "Support"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "OSCILLATION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-018-7be171d888a4",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:oscillation:375bfcf0455750c7",
          "pond:oscillation:4fbec22bb8891daa",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Cycle",
          "Delay",
          "Failure",
          "Friction",
          "Input",
          "Overflow",
          "Overshoot",
          "Rotation",
          "State",
          "Storage",
          "Support"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-018-cbf48d5e31a9",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:375bfcf0455750c7",
          "pond:oscillation:4fbec22bb8891daa"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Overshoot",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-018-37948de5146d",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Escalation",
          "Failure",
          "Friction",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Rotation",
          "Signal",
          "Support"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "OSCILLATION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-018-ed8b938c712b",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:oscillation:375bfcf0455750c7",
          "pond:oscillation:4fbec22bb8891daa",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Escalation",
          "Failure",
          "Friction",
          "Gain",
          "Input",
          "Overshoot",
          "Propagation",
          "Rotation",
          "State",
          "Support"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "FEEDBACK",
          "OSCILLATION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-018-633545968821",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:375bfcf0455750c7",
          "pond:oscillation:4fbec22bb8891daa",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Failure",
          "Friction",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Rotation",
          "Signal",
          "State",
          "Support"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-018-e5d66753b35d",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:375bfcf0455750c7",
          "pond:oscillation:4fbec22bb8891daa"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Overflow",
          "Overshoot",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "FEEDBACK",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-018-e8d7f7a04ac3",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Escalation",
          "Failure",
          "Friction",
          "Gain",
          "Input",
          "Loop",
          "Overflow",
          "Propagation",
          "Reinforcement",
          "Response",
          "Rotation",
          "Signal",
          "Storage",
          "Support"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "OSCILLATION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-018-e850308d694f",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:oscillation:375bfcf0455750c7",
          "pond:oscillation:4fbec22bb8891daa",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Cycle",
          "Delay",
          "Escalation",
          "Failure",
          "Friction",
          "Gain",
          "Input",
          "Overflow",
          "Overshoot",
          "Propagation",
          "Rotation",
          "State",
          "Storage",
          "Support"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK",
          "OSCILLATION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-018-4f52fc6eafd2",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:375bfcf0455750c7",
          "pond:oscillation:4fbec22bb8891daa",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Cycle",
          "Delay",
          "Failure",
          "Friction",
          "Input",
          "Loop",
          "Overflow",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Rotation",
          "Signal",
          "State",
          "Storage",
          "Support"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "OSCILLATION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-018-4d22cae68c25",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:375bfcf0455750c7",
          "pond:oscillation:4fbec22bb8891daa",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Escalation",
          "Failure",
          "Friction",
          "Gain",
          "Input",
          "Loop",
          "Overshoot",
          "Propagation",
          "Reinforcement",
          "Response",
          "Rotation",
          "Signal",
          "State",
          "Support"
        ]
      }
    ],
    "case_id": "P041-CP-018",
    "observation": "A turning feeder releases material unevenly. Downstream work piles up, a return signal overcorrects, and release pulses repeat."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "DIFFUSION"
        ],
        "pathway_id": "P041-CP-019-4d9f544eb195",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Dilution",
          "Gradient",
          "Input",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "LOAD_TRANSFER"
        ],
        "pathway_id": "P041-CP-019-533a49a2df63",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:load_transfer:100c18cc1d1c2bf9",
          "pond:load_transfer:38ae4961e6268ecd"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Concentration",
          "Delay",
          "Distribution",
          "Failure",
          "Input",
          "Load"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-019-404ddb3267de",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-019-13d8b75613ae",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Input",
          "Limit",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "DIFFUSION",
          "LOAD_TRANSFER"
        ],
        "pathway_id": "P041-CP-019-818f11348f3d",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:load_transfer:100c18cc1d1c2bf9",
          "pond:load_transfer:38ae4961e6268ecd"
        ],
        "supporting_motifs": [
          "Concentration",
          "Dilution",
          "Distribution",
          "Failure",
          "Gradient",
          "Load",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "DIFFUSION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-019-7c6f2579426b",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Resource",
          "Scarcity",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "DIFFUSION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-019-e8ecfa6be27d",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Dilution",
          "Gradient",
          "Limit",
          "Source",
          "Spread",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "LOAD_TRANSFER",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-019-ffd146ba3f94",
        "supporting_lineages": [
          "pond:load_transfer:100c18cc1d1c2bf9",
          "pond:load_transfer:38ae4961e6268ecd",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Concentration",
          "Consumption",
          "Distribution",
          "Exhaustion",
          "Failure",
          "Load",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "LOAD_TRANSFER",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-019-4de026850869",
        "supporting_lineages": [
          "pond:load_transfer:100c18cc1d1c2bf9",
          "pond:load_transfer:38ae4961e6268ecd",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Distribution",
          "Failure",
          "Limit",
          "Load",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-019-45f4b383a58e",
        "supporting_lineages": [
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Consumption",
          "Exhaustion",
          "Limit",
          "Resource",
          "Scarcity",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "DIFFUSION",
          "LOAD_TRANSFER"
        ],
        "pathway_id": "P041-CP-019-9b2f52b889bd",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:load_transfer:100c18cc1d1c2bf9",
          "pond:load_transfer:38ae4961e6268ecd"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Concentration",
          "Delay",
          "Dilution",
          "Distribution",
          "Failure",
          "Gradient",
          "Input",
          "Load",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "DIFFUSION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-019-e3141dfbba55",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Input",
          "Resource",
          "Scarcity",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "DIFFUSION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-019-363ba9bf9d71",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Dilution",
          "Gradient",
          "Input",
          "Limit",
          "Source",
          "Spread",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "LOAD_TRANSFER",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-019-db21084fdc41",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:load_transfer:100c18cc1d1c2bf9",
          "pond:load_transfer:38ae4961e6268ecd",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Concentration",
          "Consumption",
          "Delay",
          "Distribution",
          "Exhaustion",
          "Failure",
          "Input",
          "Load",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "LOAD_TRANSFER",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-019-88530bd7300e",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:load_transfer:100c18cc1d1c2bf9",
          "pond:load_transfer:38ae4961e6268ecd",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Concentration",
          "Delay",
          "Distribution",
          "Failure",
          "Input",
          "Limit",
          "Load",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-019-2bf119d1d7fc",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Limit",
          "Resource",
          "Scarcity",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "DIFFUSION",
          "LOAD_TRANSFER",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-019-d34e0bcc7c8e",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:load_transfer:100c18cc1d1c2bf9",
          "pond:load_transfer:38ae4961e6268ecd",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Concentration",
          "Consumption",
          "Dilution",
          "Distribution",
          "Exhaustion",
          "Failure",
          "Gradient",
          "Load",
          "Resource",
          "Scarcity",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "DIFFUSION",
          "LOAD_TRANSFER",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-019-91165dee33db",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:load_transfer:100c18cc1d1c2bf9",
          "pond:load_transfer:38ae4961e6268ecd",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Dilution",
          "Distribution",
          "Failure",
          "Gradient",
          "Limit",
          "Load",
          "Source",
          "Spread",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "DIFFUSION",
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-019-d78792055f00",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Consumption",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Limit",
          "Resource",
          "Scarcity",
          "Source",
          "Spread",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "LOAD_TRANSFER",
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-019-774b1857fa81",
        "supporting_lineages": [
          "pond:load_transfer:100c18cc1d1c2bf9",
          "pond:load_transfer:38ae4961e6268ecd",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Consumption",
          "Distribution",
          "Exhaustion",
          "Failure",
          "Limit",
          "Load",
          "Resource",
          "Scarcity",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "DIFFUSION",
          "LOAD_TRANSFER",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-019-794e75854459",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:load_transfer:100c18cc1d1c2bf9",
          "pond:load_transfer:38ae4961e6268ecd",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Concentration",
          "Consumption",
          "Delay",
          "Dilution",
          "Distribution",
          "Exhaustion",
          "Failure",
          "Gradient",
          "Input",
          "Load",
          "Resource",
          "Scarcity",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "DIFFUSION",
          "LOAD_TRANSFER",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-019-ab50bd664e95",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:load_transfer:100c18cc1d1c2bf9",
          "pond:load_transfer:38ae4961e6268ecd",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Concentration",
          "Delay",
          "Dilution",
          "Distribution",
          "Failure",
          "Gradient",
          "Input",
          "Limit",
          "Load",
          "Source",
          "Spread",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "DIFFUSION",
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-019-818703993a1d",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Consumption",
          "Delay",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Input",
          "Limit",
          "Resource",
          "Scarcity",
          "Source",
          "Spread",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "LOAD_TRANSFER",
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-019-c9a7ce660e0f",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:load_transfer:100c18cc1d1c2bf9",
          "pond:load_transfer:38ae4961e6268ecd",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Concentration",
          "Consumption",
          "Delay",
          "Distribution",
          "Exhaustion",
          "Failure",
          "Input",
          "Limit",
          "Load",
          "Resource",
          "Scarcity",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "DIFFUSION",
          "LOAD_TRANSFER",
          "RESOURCE_DEPLETION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-019-2eb3239a3187",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:load_transfer:100c18cc1d1c2bf9",
          "pond:load_transfer:38ae4961e6268ecd",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Consumption",
          "Dilution",
          "Distribution",
          "Exhaustion",
          "Failure",
          "Gradient",
          "Limit",
          "Load",
          "Resource",
          "Scarcity",
          "Source",
          "Spread",
          "StateChange",
          "Trigger"
        ]
      }
    ],
    "case_id": "P041-CP-019",
    "observation": "Force shifts across a frame. One region absorbs it temporarily, cracks spread from the stressed point, and local capacity is consumed."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING"
        ],
        "pathway_id": "P041-CP-020-c4482271bc1f",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Propagation"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-020-1df8de60af5c",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-020-bd9d851f635e",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550"
        ],
        "supporting_motifs": [
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-020-4e3691892afb",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Overshoot",
          "Propagation",
          "State"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-9c9fd45cce09",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Propagation",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-020-b4f8972c8075",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Input",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-020-1c66d7b6ef0b",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Flow",
          "Input",
          "Path",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-020-79cdf410ac92",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Input",
          "Overshoot",
          "State"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-b8c5d55ee507",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Input",
          "Limit",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-020-ec30452ddd3b",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550"
        ],
        "supporting_motifs": [
          "Flow",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-020-47236e2b00bf",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-1f60499e32fe",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Limit",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FLOW",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-020-4d4be9854ff3",
        "supporting_lineages": [
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Flow",
          "Overshoot",
          "Path",
          "Resistance",
          "Source",
          "State"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-c5431622202b",
        "supporting_lineages": [
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Flow",
          "Limit",
          "Path",
          "Resistance",
          "Source",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-ac99c9f6d6c3",
        "supporting_lineages": [
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Cycle",
          "Delay",
          "Limit",
          "Overshoot",
          "State",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-020-331a159e49e8",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-020-cc2ce34bce6a",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-020-4a0effae024b",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Overshoot",
          "Propagation",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-8aff7f2e376f",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Propagation",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-020-66aeea5da5cd",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550"
        ],
        "supporting_motifs": [
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Loop",
          "Path",
          "Propagation",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-020-76f130eb9e79",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Overshoot",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-792f39b47321",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FLOW",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-020-c0267ba659b8",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Overshoot",
          "Path",
          "Propagation",
          "Resistance",
          "Source",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-9efd75599665",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Limit",
          "Path",
          "Propagation",
          "Resistance",
          "Source",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-b5ceb733df4b",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Overshoot",
          "Propagation",
          "State",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-020-64eefd496786",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Flow",
          "Input",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-020-f08f59a6d8d8",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Input",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-ade9a90a4296",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Input",
          "Limit",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FLOW",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-020-97b54ce1eb43",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Flow",
          "Input",
          "Overshoot",
          "Path",
          "Resistance",
          "Source",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-4967ed7af374",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Flow",
          "Input",
          "Limit",
          "Path",
          "Resistance",
          "Source",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-dfabd72a3311",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Cycle",
          "Delay",
          "Input",
          "Limit",
          "Overshoot",
          "State",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "FEEDBACK",
          "FLOW",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-020-419644ad9048",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Flow",
          "Loop",
          "Overshoot",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "FEEDBACK",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-36d53aeb56c1",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Flow",
          "Limit",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "FEEDBACK",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-373762f40ed2",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Cycle",
          "Delay",
          "Limit",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "State",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "FLOW",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-f8894e5ec4a1",
        "supporting_lineages": [
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Cycle",
          "Delay",
          "Flow",
          "Limit",
          "Overshoot",
          "Path",
          "Resistance",
          "Source",
          "State",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-020-4a309f513d96",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Loop",
          "Path",
          "Propagation",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-020-2619298ff108",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Overshoot",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-a8a417dd5eea",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FLOW",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-020-9fce8e838768",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Overshoot",
          "Path",
          "Propagation",
          "Resistance",
          "Source",
          "State"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-cb1841a00939",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Limit",
          "Path",
          "Propagation",
          "Resistance",
          "Source",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-4fc2c1aadc9f",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Overshoot",
          "Propagation",
          "State",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "FLOW",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-020-8eeda3049960",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Loop",
          "Overshoot",
          "Path",
          "Propagation",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "State"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-c86939ebdf2d",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Limit",
          "Loop",
          "Path",
          "Propagation",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-07d7ad70b9cf",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Loop",
          "Overshoot",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "State",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "FLOW",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-6e7785584723",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Cycle",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Limit",
          "Overshoot",
          "Path",
          "Propagation",
          "Resistance",
          "Source",
          "State",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "FLOW",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-020-2dca1621e138",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Flow",
          "Input",
          "Loop",
          "Overshoot",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "State"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-c97cc7da78b7",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Flow",
          "Input",
          "Limit",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-42dd1e8257ba",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Cycle",
          "Delay",
          "Input",
          "Limit",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "State",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "FLOW",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-c31516426ed1",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Cycle",
          "Delay",
          "Flow",
          "Input",
          "Limit",
          "Overshoot",
          "Path",
          "Resistance",
          "Source",
          "State",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "FEEDBACK",
          "FLOW",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-020-fe0caa4dc784",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Cycle",
          "Delay",
          "Flow",
          "Limit",
          "Loop",
          "Overshoot",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "State",
          "StateChange",
          "Trigger"
        ]
      }
    ],
    "case_id": "P041-CP-020",
    "observation": "Small route delays are magnified by priority rules. The queue crosses a limit and a returning delay signal sends later batches into the same route."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION"
        ],
        "pathway_id": "P041-CP-021-972f29661e98",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Escalation",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING"
        ],
        "pathway_id": "P041-CP-021-edf32f3dca6c",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Input",
          "Overflow",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-021-7933949a88be",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-021-bc0a9b1188c8",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Exhaustion",
          "Input",
          "Overflow",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING"
        ],
        "pathway_id": "P041-CP-021-3181f8c5ba82",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Propagation"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-021-4b459b7b4990",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0"
        ],
        "supporting_motifs": [
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-021-569a61080db6",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Propagation",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-021-053231c565fe",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Flow",
          "Input",
          "Path",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-021-a0b63f7899a4",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-021-61a99140969c",
        "supporting_lineages": [
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Exhaustion",
          "Flow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "BUFFERING"
        ],
        "pathway_id": "P041-CP-021-fa439e29c03b",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-021-a5d063347328",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Overflow",
          "Path",
          "Propagation",
          "Resistance",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-021-f22712e7b802",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-021-8f32ea0cd5d8",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-021-ebca33839ed5",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Overflow",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-021-c10407bd1ba8",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Exhaustion",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-021-4ffadc03948c",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-021-926a572fe2d6",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Propagation",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-021-675d2e5663e3",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-021-d96bc69b2ae0",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Flow",
          "Input",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-021-8a23fe85c3f6",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Escalation",
          "Flow",
          "Gain",
          "Input",
          "Overflow",
          "Path",
          "Propagation",
          "Resistance",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-021-e54fb846d580",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-021-4ef3231b2411",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Flow",
          "Gain",
          "Input",
          "Overflow",
          "Path",
          "Propagation",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-021-98ba0e857eb1",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FLOW",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-021-8dfc748833e5",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:flow:3e0228bbea0e6e1c",
          "pond:flow:5dac9687957be5f0",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Escalation",
          "Exhaustion",
          "Flow",
          "Gain",
          "Input",
          "Path",
          "Propagation",
          "Resistance",
          "Resource",
          "Scarcity",
          "Source"
        ]
      }
    ],
    "case_id": "P041-CP-021",
    "observation": "A reserve hides falling fuel. Once the reserve is drained, a controller requests more demand and the final decline accelerates."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING"
        ],
        "pathway_id": "P041-CP-022-b9a2272053a1",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Propagation"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "COMPENSATION"
        ],
        "pathway_id": "P041-CP-022-580863259b67",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Deviation",
          "Escalation",
          "Gain",
          "Input",
          "Propagation",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-022-83a2866f9ead",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8"
        ],
        "supporting_motifs": [
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-022-0d797eda37a1",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Overshoot",
          "Propagation",
          "State"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-4951d9ea99d9",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Propagation",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION"
        ],
        "pathway_id": "P041-CP-022-2a6e0cb2b6ad",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Input",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-022-b8ec5bece15c",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Input",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-022-6cd962bc8b74",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Input",
          "Overshoot",
          "State"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-ff4e69c8641b",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Input",
          "Limit",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-022-e5b6511c50f1",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Deviation",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-022-37768d22fdc4",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Cycle",
          "Delay",
          "Deviation",
          "Overshoot",
          "Stabilization",
          "State",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-b77740c8ff10",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Counteraction",
          "Deviation",
          "Limit",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-022-9afcad8c38ce",
        "supporting_lineages": [
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-36b7c26156cb",
        "supporting_lineages": [
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Limit",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-f3acda3cf845",
        "supporting_lineages": [
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Cycle",
          "Delay",
          "Limit",
          "Overshoot",
          "State",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "COMPENSATION"
        ],
        "pathway_id": "P041-CP-022-8928e8049f61",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Escalation",
          "Gain",
          "Input",
          "Propagation",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-022-ab4db2ddebaa",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-022-ca67305e71d3",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Overshoot",
          "Propagation",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-725ebf33e8d0",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Propagation",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "COMPENSATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-022-9cad4229fcdd",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Deviation",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "COMPENSATION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-022-7f38968af9ca",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Cycle",
          "Delay",
          "Deviation",
          "Escalation",
          "Gain",
          "Input",
          "Overshoot",
          "Propagation",
          "Stabilization",
          "State",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "COMPENSATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-1d2901a5ae62",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Counteraction",
          "Deviation",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Propagation",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-022-682878e67b44",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Overshoot",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-02f7d46d76c4",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-c4ffe622d79b",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Overshoot",
          "Propagation",
          "State",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-022-40a5930eb30d",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Input",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-022-bd0fdfb64d7c",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Cycle",
          "Delay",
          "Deviation",
          "Input",
          "Overshoot",
          "Stabilization",
          "State",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-6d1d33dc7d63",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Input",
          "Limit",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-022-a0afdf0e7a3a",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Input",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-76e7790362cc",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Input",
          "Limit",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-4fae988186d9",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Cycle",
          "Delay",
          "Input",
          "Limit",
          "Overshoot",
          "State",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-022-070c8e3cd6e2",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Cycle",
          "Delay",
          "Deviation",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "State",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-2161fc7a46db",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Counteraction",
          "Deviation",
          "Limit",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-c1b5d75b534a",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Counteraction",
          "Cycle",
          "Delay",
          "Deviation",
          "Limit",
          "Overshoot",
          "Stabilization",
          "State",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "FEEDBACK",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-160a9c136e6e",
        "supporting_lineages": [
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Cycle",
          "Delay",
          "Limit",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "State",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "COMPENSATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-022-9b7162a37362",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "COMPENSATION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-022-4fc84cc97422",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Cycle",
          "Delay",
          "Deviation",
          "Escalation",
          "Gain",
          "Input",
          "Overshoot",
          "Propagation",
          "Stabilization",
          "State",
          "Substitution"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "COMPENSATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-3830bc25bb65",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Propagation",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-022-e14bda0f380a",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Overshoot",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-dcae252cd235",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-9d34aa3ddfdc",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Overshoot",
          "Propagation",
          "State",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "COMPENSATION",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-022-98a157ea1bb6",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Cycle",
          "Delay",
          "Deviation",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Overshoot",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "State",
          "Substitution"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "COMPENSATION",
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-635066061f64",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Counteraction",
          "Deviation",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "COMPENSATION",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-3e87784984d9",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Counteraction",
          "Cycle",
          "Delay",
          "Deviation",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Overshoot",
          "Propagation",
          "Stabilization",
          "State",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-530579151dac",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Limit",
          "Loop",
          "Overshoot",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "State",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-022-680e670ccbbc",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Cycle",
          "Delay",
          "Deviation",
          "Input",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "State",
          "Substitution"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-2cad92c22564",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Input",
          "Limit",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-ba88814a9d45",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Counteraction",
          "Cycle",
          "Delay",
          "Deviation",
          "Input",
          "Limit",
          "Overshoot",
          "Stabilization",
          "State",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-320362747cd7",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Cycle",
          "Delay",
          "Input",
          "Limit",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "State",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "COMPENSATION",
          "FEEDBACK",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-022-a92b815c9d60",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:27415f742a6cf086"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Counteraction",
          "Cycle",
          "Delay",
          "Deviation",
          "Limit",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "State",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      }
    ],
    "case_id": "P041-CP-022",
    "observation": "A limit switch triggers late. The offsetting correction overshoots, reverses direction, and repeats because the return signal is delayed."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "DIFFUSION"
        ],
        "pathway_id": "P041-CP-023-3a135e171c46",
        "supporting_lineages": [
          "pond:accumulation:10c2c8ae31c87504",
          "pond:accumulation:15625a03373c9075",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Dilution",
          "Gradient",
          "Input",
          "Overflow",
          "Source",
          "Spread",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-023-5c8822f28859",
        "supporting_lineages": [
          "pond:accumulation:10c2c8ae31c87504",
          "pond:accumulation:15625a03373c9075",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "DIFFUSION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-023-e6e4065d986c",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Dilution",
          "Flow",
          "Gradient",
          "Path",
          "Resistance",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "DIFFUSION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-023-720c0ff24204",
        "supporting_lineages": [
          "pond:accumulation:10c2c8ae31c87504",
          "pond:accumulation:15625a03373c9075",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Dilution",
          "Flow",
          "Gradient",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Source",
          "Spread",
          "Storage"
        ]
      }
    ],
    "case_id": "P041-CP-023",
    "observation": "Sediment builds in a passage and spreads into side channels. After enough buildup, throughput falls and downstream output starves."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "LOAD_TRANSFER",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-024-41d8e8cb8228",
        "supporting_lineages": [
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:threshold:4805330b0343ed45",
          "pond:threshold:7bb27a243a3a432e"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Distribution",
          "Failure",
          "Limit",
          "Load",
          "StateChange",
          "Trigger"
        ]
      }
    ],
    "case_id": "P041-CP-024",
    "observation": "A local crack concentrates demand. Each small deformation magnifies the next, and the bracket crosses a failure limit."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION"
        ],
        "pathway_id": "P041-CP-025-fd00a7b0314d",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Input",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "DIFFUSION"
        ],
        "pathway_id": "P041-CP-025-f9d5134351a5",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:diffusion:558b4378784d5a7f"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Dilution",
          "Gradient",
          "Input",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-025-38a376d12328",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-025-26b57f85b1dd",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:supported_rotation:43b7e46d4526aded"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Failure",
          "Friction",
          "Input",
          "Rotation",
          "Support"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "DIFFUSION"
        ],
        "pathway_id": "P041-CP-025-9d9c43a56baa",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:diffusion:558b4378784d5a7f"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Deviation",
          "Dilution",
          "Gradient",
          "Source",
          "Spread",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-025-24aac706addd",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Counteraction",
          "Deviation",
          "Exhaustion",
          "Resource",
          "Scarcity",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-025-e4a4f69163d6",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:supported_rotation:43b7e46d4526aded"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Deviation",
          "Failure",
          "Friction",
          "Rotation",
          "Stabilization",
          "Substitution",
          "Support"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "DIFFUSION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-025-934dac8d3a15",
        "supporting_lineages": [
          "pond:diffusion:1295d8896f93fcd8",
          "pond:diffusion:558b4378784d5a7f",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Resource",
          "Scarcity",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "DIFFUSION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-025-a3a13a752c8a",
        "supporting_lineages": [
          "pond:diffusion:1295d8896f93fcd8",
          "pond:diffusion:558b4378784d5a7f",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:supported_rotation:43b7e46d4526aded"
        ],
        "supporting_motifs": [
          "Dilution",
          "Failure",
          "Friction",
          "Gradient",
          "Rotation",
          "Source",
          "Spread",
          "Support"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "RESOURCE_DEPLETION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-025-78d657720ea0",
        "supporting_lineages": [
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:supported_rotation:43b7e46d4526aded"
        ],
        "supporting_motifs": [
          "Consumption",
          "Exhaustion",
          "Failure",
          "Friction",
          "Resource",
          "Rotation",
          "Scarcity",
          "Support"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "DIFFUSION"
        ],
        "pathway_id": "P041-CP-025-0d40659bc6a2",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:diffusion:558b4378784d5a7f"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Dilution",
          "Gradient",
          "Input",
          "Source",
          "Spread",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-025-e4ea6adbde1e",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Counteraction",
          "Delay",
          "Deviation",
          "Exhaustion",
          "Input",
          "Resource",
          "Scarcity",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-025-c621800c371b",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:supported_rotation:43b7e46d4526aded"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Failure",
          "Friction",
          "Input",
          "Rotation",
          "Stabilization",
          "Substitution",
          "Support"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "DIFFUSION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-025-3c2e04d5a2a2",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:diffusion:558b4378784d5a7f",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Input",
          "Resource",
          "Scarcity",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "DIFFUSION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-025-f99b75c859b2",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:diffusion:558b4378784d5a7f",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:supported_rotation:43b7e46d4526aded"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Dilution",
          "Failure",
          "Friction",
          "Gradient",
          "Input",
          "Rotation",
          "Source",
          "Spread",
          "Support"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "RESOURCE_DEPLETION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-025-06ad470558fa",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:supported_rotation:43b7e46d4526aded"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Failure",
          "Friction",
          "Input",
          "Resource",
          "Rotation",
          "Scarcity",
          "Support"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "DIFFUSION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-025-ab06394ebe5f",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:diffusion:558b4378784d5a7f",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Counteraction",
          "Deviation",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Resource",
          "Scarcity",
          "Source",
          "Spread",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "DIFFUSION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-025-a68486bc8c75",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:diffusion:558b4378784d5a7f",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:supported_rotation:43b7e46d4526aded"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Deviation",
          "Dilution",
          "Failure",
          "Friction",
          "Gradient",
          "Rotation",
          "Source",
          "Spread",
          "Stabilization",
          "Substitution",
          "Support"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "RESOURCE_DEPLETION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-025-8af243ab427b",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:supported_rotation:43b7e46d4526aded"
        ],
        "supporting_motifs": [
          "Consumption",
          "Counteraction",
          "Deviation",
          "Exhaustion",
          "Failure",
          "Friction",
          "Resource",
          "Rotation",
          "Scarcity",
          "Stabilization",
          "Substitution",
          "Support"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "DIFFUSION",
          "RESOURCE_DEPLETION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-025-625f3eb1eecc",
        "supporting_lineages": [
          "pond:diffusion:1295d8896f93fcd8",
          "pond:diffusion:558b4378784d5a7f",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:supported_rotation:43b7e46d4526aded"
        ],
        "supporting_motifs": [
          "Consumption",
          "Dilution",
          "Exhaustion",
          "Failure",
          "Friction",
          "Gradient",
          "Resource",
          "Rotation",
          "Scarcity",
          "Source",
          "Spread",
          "Support"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "DIFFUSION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-025-6428f2e17789",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:diffusion:558b4378784d5a7f",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Counteraction",
          "Delay",
          "Deviation",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Input",
          "Resource",
          "Scarcity",
          "Source",
          "Spread",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "DIFFUSION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-025-46a3c821bd71",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:diffusion:558b4378784d5a7f",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:supported_rotation:43b7e46d4526aded"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Dilution",
          "Failure",
          "Friction",
          "Gradient",
          "Input",
          "Rotation",
          "Source",
          "Spread",
          "Stabilization",
          "Substitution",
          "Support"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "RESOURCE_DEPLETION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-025-219ff41aa4a8",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:supported_rotation:43b7e46d4526aded"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Counteraction",
          "Delay",
          "Deviation",
          "Exhaustion",
          "Failure",
          "Friction",
          "Input",
          "Resource",
          "Rotation",
          "Scarcity",
          "Stabilization",
          "Substitution",
          "Support"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "DIFFUSION",
          "RESOURCE_DEPLETION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-025-707939318b09",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:diffusion:558b4378784d5a7f",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:supported_rotation:43b7e46d4526aded"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Dilution",
          "Exhaustion",
          "Failure",
          "Friction",
          "Gradient",
          "Input",
          "Resource",
          "Rotation",
          "Scarcity",
          "Source",
          "Spread",
          "Support"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "COMPENSATION",
          "DIFFUSION",
          "RESOURCE_DEPLETION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-025-641607da9660",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:diffusion:558b4378784d5a7f",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:supported_rotation:43b7e46d4526aded"
        ],
        "supporting_motifs": [
          "Consumption",
          "Counteraction",
          "Deviation",
          "Dilution",
          "Exhaustion",
          "Failure",
          "Friction",
          "Gradient",
          "Resource",
          "Rotation",
          "Scarcity",
          "Source",
          "Spread",
          "Stabilization",
          "Substitution",
          "Support"
        ]
      }
    ],
    "case_id": "P041-CP-025",
    "observation": "A spreading heat patch reaches a pivot. Drag rises, the controller adds drive to offset it, and the added drive drains capacity."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING"
        ],
        "pathway_id": "P041-CP-026-76267ccf44a4",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Input",
          "Overflow",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-026-f8ffd0637b91",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:oscillation:375bfcf0455750c7",
          "pond:oscillation:4fbec22bb8891daa"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Cycle",
          "Delay",
          "Input",
          "Overflow",
          "Overshoot",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-026-84ef956747d0",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Exhaustion",
          "Input",
          "Overflow",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-026-051ebb150fda",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:oscillation:375bfcf0455750c7",
          "pond:oscillation:4fbec22bb8891daa"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Input",
          "Overshoot",
          "State"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-026-d542ee55d083",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "OSCILLATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-026-4f7f7b9d6bb8",
        "supporting_lineages": [
          "pond:oscillation:375bfcf0455750c7",
          "pond:oscillation:4fbec22bb8891daa",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Cycle",
          "Delay",
          "Exhaustion",
          "Overshoot",
          "Resource",
          "Scarcity",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-026-618058fb225b",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:oscillation:375bfcf0455750c7",
          "pond:oscillation:4fbec22bb8891daa"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Cycle",
          "Delay",
          "Input",
          "Overflow",
          "Overshoot",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-026-3d30f9b27b2a",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Overflow",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "OSCILLATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-026-ddef4fb0e5d9",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:oscillation:375bfcf0455750c7",
          "pond:oscillation:4fbec22bb8891daa",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Cycle",
          "Delay",
          "Exhaustion",
          "Input",
          "Overflow",
          "Overshoot",
          "Resource",
          "Scarcity",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "OSCILLATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-026-da03dbca6f2e",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:oscillation:375bfcf0455750c7",
          "pond:oscillation:4fbec22bb8891daa",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Cycle",
          "Delay",
          "Exhaustion",
          "Input",
          "Overshoot",
          "Resource",
          "Scarcity",
          "State"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "OSCILLATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-026-ccdffd7213a3",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:oscillation:375bfcf0455750c7",
          "pond:oscillation:4fbec22bb8891daa",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Cycle",
          "Delay",
          "Exhaustion",
          "Input",
          "Overflow",
          "Overshoot",
          "Resource",
          "Scarcity",
          "State",
          "Storage"
        ]
      }
    ],
    "case_id": "P041-CP-026",
    "observation": "Work piles behind a reserve. When the reserve fills, release comes in pulses that overshoot capacity and then undershoot demand."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "DIFFUSION"
        ],
        "pathway_id": "P041-CP-027-0354357c4382",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Deviation",
          "Dilution",
          "Gradient",
          "Source",
          "Spread",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "LOAD_TRANSFER"
        ],
        "pathway_id": "P041-CP-027-1031f2bff505",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044"
        ],
        "supporting_motifs": [
          "Concentration",
          "Counteraction",
          "Deviation",
          "Distribution",
          "Failure",
          "Load",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-027-7af719878b52",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Deviation",
          "Failure",
          "Friction",
          "Rotation",
          "Stabilization",
          "Substitution",
          "Support"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-027-15d442e4d561",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Counteraction",
          "Deviation",
          "Limit",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "DIFFUSION",
          "LOAD_TRANSFER"
        ],
        "pathway_id": "P041-CP-027-c747f3ca3e91",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044"
        ],
        "supporting_motifs": [
          "Concentration",
          "Dilution",
          "Distribution",
          "Failure",
          "Gradient",
          "Load",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "DIFFUSION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-027-688c78d2b107",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Dilution",
          "Failure",
          "Friction",
          "Gradient",
          "Rotation",
          "Source",
          "Spread",
          "Support"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "DIFFUSION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-027-90782613ce34",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Dilution",
          "Gradient",
          "Limit",
          "Source",
          "Spread",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "LOAD_TRANSFER",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-027-ea3f7d9c17df",
        "supporting_lineages": [
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Concentration",
          "Distribution",
          "Failure",
          "Friction",
          "Load",
          "Rotation",
          "Support"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "LOAD_TRANSFER",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-027-63ac101a3e52",
        "supporting_lineages": [
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Distribution",
          "Failure",
          "Limit",
          "Load",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "SUPPORTED_ROTATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-027-58828005d349",
        "supporting_lineages": [
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Failure",
          "Friction",
          "Limit",
          "Rotation",
          "StateChange",
          "Support",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "DIFFUSION",
          "LOAD_TRANSFER"
        ],
        "pathway_id": "P041-CP-027-a4f46eb99060",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044"
        ],
        "supporting_motifs": [
          "Concentration",
          "Counteraction",
          "Deviation",
          "Dilution",
          "Distribution",
          "Failure",
          "Gradient",
          "Load",
          "Source",
          "Spread",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "DIFFUSION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-027-c1395ccafd92",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Deviation",
          "Dilution",
          "Failure",
          "Friction",
          "Gradient",
          "Rotation",
          "Source",
          "Spread",
          "Stabilization",
          "Substitution",
          "Support"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "DIFFUSION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-027-be4caecc2e27",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Counteraction",
          "Deviation",
          "Dilution",
          "Gradient",
          "Limit",
          "Source",
          "Spread",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "LOAD_TRANSFER",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-027-b71ba404ae24",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Concentration",
          "Counteraction",
          "Deviation",
          "Distribution",
          "Failure",
          "Friction",
          "Load",
          "Rotation",
          "Stabilization",
          "Substitution",
          "Support"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "LOAD_TRANSFER",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-027-65248986ab59",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Counteraction",
          "Deviation",
          "Distribution",
          "Failure",
          "Limit",
          "Load",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "SUPPORTED_ROTATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-027-f0d11a9d882a",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Counteraction",
          "Deviation",
          "Failure",
          "Friction",
          "Limit",
          "Rotation",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Support",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "DIFFUSION",
          "LOAD_TRANSFER",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-027-0eb0909f4518",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Concentration",
          "Dilution",
          "Distribution",
          "Failure",
          "Friction",
          "Gradient",
          "Load",
          "Rotation",
          "Source",
          "Spread",
          "Support"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "DIFFUSION",
          "LOAD_TRANSFER",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-027-2ebd8106f070",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Dilution",
          "Distribution",
          "Failure",
          "Gradient",
          "Limit",
          "Load",
          "Source",
          "Spread",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "DIFFUSION",
          "SUPPORTED_ROTATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-027-b296672cf116",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Dilution",
          "Failure",
          "Friction",
          "Gradient",
          "Limit",
          "Rotation",
          "Source",
          "Spread",
          "StateChange",
          "Support",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "LOAD_TRANSFER",
          "SUPPORTED_ROTATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-027-e944777212b8",
        "supporting_lineages": [
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Distribution",
          "Failure",
          "Friction",
          "Limit",
          "Load",
          "Rotation",
          "StateChange",
          "Support",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "COMPENSATION",
          "DIFFUSION",
          "LOAD_TRANSFER",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-027-d66eb703872d",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Concentration",
          "Counteraction",
          "Deviation",
          "Dilution",
          "Distribution",
          "Failure",
          "Friction",
          "Gradient",
          "Load",
          "Rotation",
          "Source",
          "Spread",
          "Stabilization",
          "Substitution",
          "Support"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "COMPENSATION",
          "DIFFUSION",
          "LOAD_TRANSFER",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-027-e8842e1954f6",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Counteraction",
          "Deviation",
          "Dilution",
          "Distribution",
          "Failure",
          "Gradient",
          "Limit",
          "Load",
          "Source",
          "Spread",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "COMPENSATION",
          "DIFFUSION",
          "SUPPORTED_ROTATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-027-f04074f98626",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Counteraction",
          "Deviation",
          "Dilution",
          "Failure",
          "Friction",
          "Gradient",
          "Limit",
          "Rotation",
          "Source",
          "Spread",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Support",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "COMPENSATION",
          "LOAD_TRANSFER",
          "SUPPORTED_ROTATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-027-c0fda56b2883",
        "supporting_lineages": [
          "pond:compensation:0293b4c027834565",
          "pond:compensation:0f554fa27f3ebc01",
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Counteraction",
          "Deviation",
          "Distribution",
          "Failure",
          "Friction",
          "Limit",
          "Load",
          "Rotation",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Support",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "DIFFUSION",
          "LOAD_TRANSFER",
          "SUPPORTED_ROTATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-027-8f0e8e583fab",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:load_transfer:093852f103902af0",
          "pond:load_transfer:100b958307e05044",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Concentration",
          "Dilution",
          "Distribution",
          "Failure",
          "Friction",
          "Gradient",
          "Limit",
          "Load",
          "Rotation",
          "Source",
          "Spread",
          "StateChange",
          "Support",
          "Trigger"
        ]
      }
    ],
    "case_id": "P041-CP-027",
    "observation": "A small imbalance spreads across neighboring supports. Offsetting action masks the tilt until one anchor takes excess demand and bends."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION"
        ],
        "pathway_id": "P041-CP-028-40998d104726",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Input",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-028-58546be84e35",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Input",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "FLOW"
        ],
        "pathway_id": "P041-CP-028-fd031b8cfd1a",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Flow",
          "Input",
          "Path",
          "Resistance",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-028-5359265a14cc",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:threshold:1dbfe551705dbe5c",
          "pond:threshold:32701a3d308b3051"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Input",
          "Limit",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-028-1b7c3c2bb2ba",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Deviation",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-028-1af84c236b0a",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Deviation",
          "Flow",
          "Path",
          "Resistance",
          "Source",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "COMPENSATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-028-bb1997581a7f",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:threshold:1dbfe551705dbe5c",
          "pond:threshold:32701a3d308b3051"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Counteraction",
          "Deviation",
          "Limit",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-028-4b27a5e02731",
        "supporting_lineages": [
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Flow",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-028-e5d9be6198fe",
        "supporting_lineages": [
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:threshold:1dbfe551705dbe5c",
          "pond:threshold:32701a3d308b3051"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Limit",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-028-92b2494dfbbe",
        "supporting_lineages": [
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:threshold:1dbfe551705dbe5c",
          "pond:threshold:32701a3d308b3051"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Flow",
          "Limit",
          "Path",
          "Resistance",
          "Source",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-028-66cd56165e45",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Input",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-028-cb5e6beeb594",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Flow",
          "Input",
          "Path",
          "Resistance",
          "Source",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-028-7fc4ddceabef",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:threshold:1dbfe551705dbe5c",
          "pond:threshold:32701a3d308b3051"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Input",
          "Limit",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-028-13fcdb93341c",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Flow",
          "Input",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-028-bd26a1f60b78",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:threshold:1dbfe551705dbe5c",
          "pond:threshold:32701a3d308b3051"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Input",
          "Limit",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-028-68195a60f61c",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:threshold:1dbfe551705dbe5c",
          "pond:threshold:32701a3d308b3051"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Flow",
          "Input",
          "Limit",
          "Path",
          "Resistance",
          "Source",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-028-a95ef8670aef",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Counteraction",
          "Deviation",
          "Flow",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-028-a8e8413313ff",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:threshold:1dbfe551705dbe5c",
          "pond:threshold:32701a3d308b3051"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Counteraction",
          "Deviation",
          "Limit",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "COMPENSATION",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-028-c1223e253650",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:threshold:1dbfe551705dbe5c",
          "pond:threshold:32701a3d308b3051"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Counteraction",
          "Deviation",
          "Flow",
          "Limit",
          "Path",
          "Resistance",
          "Source",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "FEEDBACK",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-028-b1d99c90ed01",
        "supporting_lineages": [
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:threshold:1dbfe551705dbe5c",
          "pond:threshold:32701a3d308b3051"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Flow",
          "Limit",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "FEEDBACK",
          "FLOW"
        ],
        "pathway_id": "P041-CP-028-f310ffdb3e64",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Flow",
          "Input",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "Stabilization",
          "Substitution"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "FEEDBACK",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-028-d091ead44e13",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:threshold:1dbfe551705dbe5c",
          "pond:threshold:32701a3d308b3051"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Input",
          "Limit",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "COMPENSATION",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-028-995e4c2e82b9",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:threshold:1dbfe551705dbe5c",
          "pond:threshold:32701a3d308b3051"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Counteraction",
          "Delay",
          "Deviation",
          "Flow",
          "Input",
          "Limit",
          "Path",
          "Resistance",
          "Source",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-028-7baa83dd151a",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:2ddfeb5b0f9baf86",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:threshold:1dbfe551705dbe5c",
          "pond:threshold:32701a3d308b3051"
        ],
        "supporting_motifs": [
          "Absorption",
          "Accumulation",
          "Buffer",
          "Delay",
          "Flow",
          "Input",
          "Limit",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "COMPENSATION",
          "FEEDBACK",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-028-0c71eb95cb97",
        "supporting_lineages": [
          "pond:compensation:1b348715597e8587",
          "pond:compensation:29b7f9f7ae556a3b",
          "pond:feedback:29970c37fcd9a815",
          "pond:feedback:639dd439e706d4f8",
          "pond:flow:174e933edaa55697",
          "pond:flow:1b188635f25f4a13",
          "pond:threshold:1dbfe551705dbe5c",
          "pond:threshold:32701a3d308b3051"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Counteraction",
          "Deviation",
          "Flow",
          "Limit",
          "Loop",
          "Path",
          "Reinforcement",
          "Resistance",
          "Response",
          "Signal",
          "Source",
          "Stabilization",
          "StateChange",
          "Substitution",
          "Trigger"
        ]
      }
    ],
    "case_id": "P041-CP-028",
    "observation": "A return loop stabilizes output until stored errors cross a boundary. Then the same loop reinforces the wrong correction and magnifies deviation."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION"
        ],
        "pathway_id": "P041-CP-029-20936cad6272",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Escalation",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING"
        ],
        "pathway_id": "P041-CP-029-9bb3e23707df",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Input",
          "Overflow",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "DIFFUSION"
        ],
        "pathway_id": "P041-CP-029-060dffc83d00",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Dilution",
          "Gradient",
          "Input",
          "Overflow",
          "Source",
          "Spread",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-029-95482dc65c63",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Input",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Response",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-3e6fa00c1441",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Cycle",
          "Delay",
          "Input",
          "Overflow",
          "Overshoot",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-75861d2d5098",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Exhaustion",
          "Input",
          "Overflow",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING"
        ],
        "pathway_id": "P041-CP-029-63798f06ab97",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Propagation"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "DIFFUSION"
        ],
        "pathway_id": "P041-CP-029-683c359eb3d6",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8"
        ],
        "supporting_motifs": [
          "Dilution",
          "Escalation",
          "Gain",
          "Gradient",
          "Input",
          "Propagation",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-029-7d826bdab7d7",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-58cf2d21d101",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Overshoot",
          "Propagation",
          "State"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "AMPLIFICATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-5725b5353f34",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Propagation",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "DIFFUSION"
        ],
        "pathway_id": "P041-CP-029-dce0bd0c4bf2",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Dilution",
          "Gradient",
          "Input",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-029-904d594ecbd7",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Input",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-382848c781e4",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Input",
          "Overshoot",
          "State"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-04801abfb304",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "DIFFUSION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-029-e7835331b7cf",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Dilution",
          "Gradient",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "DIFFUSION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-1d655de272c0",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Dilution",
          "Gradient",
          "Overshoot",
          "Source",
          "Spread",
          "State"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "DIFFUSION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-e1c5fcd69f95",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Resource",
          "Scarcity",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-8ea2a0f76187",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-e0cad76b04de",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Exhaustion",
          "Loop",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "OSCILLATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-1f23e19c9bfc",
        "supporting_lineages": [
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Cycle",
          "Delay",
          "Exhaustion",
          "Overshoot",
          "Resource",
          "Scarcity",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "BUFFERING"
        ],
        "pathway_id": "P041-CP-029-3cfa477c11db",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "DIFFUSION"
        ],
        "pathway_id": "P041-CP-029-d5e90dc961b8",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Dilution",
          "Escalation",
          "Gain",
          "Gradient",
          "Input",
          "Overflow",
          "Propagation",
          "Source",
          "Spread",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-029-369976cd201b",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Overflow",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-b7a5e0f38dd9",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Overflow",
          "Overshoot",
          "Propagation",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-6e43b47ed15b",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "DIFFUSION"
        ],
        "pathway_id": "P041-CP-029-2d9f8e530ed4",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Dilution",
          "Gradient",
          "Input",
          "Overflow",
          "Source",
          "Spread",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-029-7d29ae9ee329",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Input",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Response",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-5b9c8f38c9dd",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Cycle",
          "Delay",
          "Input",
          "Overflow",
          "Overshoot",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-95aafdf05262",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Overflow",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "DIFFUSION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-029-5d8eaf36da9a",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Dilution",
          "Gradient",
          "Input",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Response",
          "Signal",
          "Source",
          "Spread",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "DIFFUSION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-971304188734",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Cycle",
          "Delay",
          "Dilution",
          "Gradient",
          "Input",
          "Overflow",
          "Overshoot",
          "Source",
          "Spread",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "DIFFUSION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-81d1a69cb302",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Input",
          "Overflow",
          "Resource",
          "Scarcity",
          "Source",
          "Spread",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-d406f946d3fe",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Cycle",
          "Delay",
          "Input",
          "Loop",
          "Overflow",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-e56735f99355",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Exhaustion",
          "Input",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "OSCILLATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-7860f1af1c09",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Cycle",
          "Delay",
          "Exhaustion",
          "Input",
          "Overflow",
          "Overshoot",
          "Resource",
          "Scarcity",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "DIFFUSION"
        ],
        "pathway_id": "P041-CP-029-f1954d1443e7",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Dilution",
          "Escalation",
          "Gain",
          "Gradient",
          "Input",
          "Propagation",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-029-5463cfd843e5",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-12f9e09ae234",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Overshoot",
          "Propagation",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-1385319a3b2b",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Propagation",
          "Resource",
          "Scarcity"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "DIFFUSION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-029-8b4dc38d8339",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Dilution",
          "Escalation",
          "Gain",
          "Gradient",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "DIFFUSION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-a2f8d40851cd",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Dilution",
          "Escalation",
          "Gain",
          "Gradient",
          "Input",
          "Overshoot",
          "Propagation",
          "Source",
          "Spread",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "DIFFUSION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-13ef2b6e7e88",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Dilution",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Gradient",
          "Input",
          "Propagation",
          "Resource",
          "Scarcity",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-5d7aad0120f0",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Overshoot",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-e1118bd20f33",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "AMPLIFICATION",
          "OSCILLATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-5c5e686d6939",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Cycle",
          "Delay",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Overshoot",
          "Propagation",
          "Resource",
          "Scarcity",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "DIFFUSION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-029-750885d79694",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Dilution",
          "Gradient",
          "Input",
          "Loop",
          "Reinforcement",
          "Response",
          "Signal",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "DIFFUSION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-d957f729e8d8",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Dilution",
          "Gradient",
          "Input",
          "Overshoot",
          "Source",
          "Spread",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "DIFFUSION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-2a276a5939db",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Input",
          "Resource",
          "Scarcity",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-f06c0d5ef045",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Input",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-fffcc1721011",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Loop",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "BUFFERING",
          "OSCILLATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-ef73bb7466ef",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Cycle",
          "Delay",
          "Exhaustion",
          "Input",
          "Overshoot",
          "Resource",
          "Scarcity",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "DIFFUSION",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-15ca3ea93cb4",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Dilution",
          "Gradient",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "Source",
          "Spread",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "DIFFUSION",
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-b0e77b813728",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Loop",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "DIFFUSION",
          "OSCILLATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-0d6280403c88",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Cycle",
          "Delay",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Overshoot",
          "Resource",
          "Scarcity",
          "Source",
          "Spread",
          "State"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "FEEDBACK",
          "OSCILLATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-57d3d6c8f061",
        "supporting_lineages": [
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Cycle",
          "Delay",
          "Exhaustion",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "BUFFERING",
          "DIFFUSION"
        ],
        "pathway_id": "P041-CP-029-e8a9616306c0",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Dilution",
          "Escalation",
          "Gain",
          "Gradient",
          "Input",
          "Overflow",
          "Propagation",
          "Source",
          "Spread",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-029-e3b6f23599f4",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Overflow",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "BUFFERING",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-fedbab2ddcc1",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Overflow",
          "Overshoot",
          "Propagation",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "BUFFERING",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-872418b0c713",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Overflow",
          "Propagation",
          "Resource",
          "Scarcity",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "DIFFUSION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-029-d3cdc3b4e83b",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Dilution",
          "Escalation",
          "Gain",
          "Gradient",
          "Input",
          "Loop",
          "Overflow",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "Source",
          "Spread",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "DIFFUSION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-43047bb7dd18",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Cycle",
          "Delay",
          "Dilution",
          "Escalation",
          "Gain",
          "Gradient",
          "Input",
          "Overflow",
          "Overshoot",
          "Propagation",
          "Source",
          "Spread",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "DIFFUSION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-10da939a36ef",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Dilution",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Gradient",
          "Input",
          "Overflow",
          "Propagation",
          "Resource",
          "Scarcity",
          "Source",
          "Spread",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-d5b5726783e3",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Overflow",
          "Overshoot",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-573a97816e67",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Loop",
          "Overflow",
          "Propagation",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "AMPLIFICATION",
          "OSCILLATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-5a384e18d8e3",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Cycle",
          "Delay",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Overflow",
          "Overshoot",
          "Propagation",
          "Resource",
          "Scarcity",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "DIFFUSION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-029-4d9c19b30848",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Delay",
          "Dilution",
          "Gradient",
          "Input",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Response",
          "Signal",
          "Source",
          "Spread",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "DIFFUSION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-9ce410b229fe",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Cycle",
          "Delay",
          "Dilution",
          "Gradient",
          "Input",
          "Overflow",
          "Overshoot",
          "Source",
          "Spread",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "DIFFUSION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-62001e1a6f51",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Input",
          "Overflow",
          "Resource",
          "Scarcity",
          "Source",
          "Spread",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-e95f67dd54e1",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Cycle",
          "Delay",
          "Input",
          "Loop",
          "Overflow",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-1a2eecc1c059",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Delay",
          "Exhaustion",
          "Input",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "BUFFERING",
          "OSCILLATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-610a2fda504e",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "BuildUp",
          "Consumption",
          "Cycle",
          "Delay",
          "Exhaustion",
          "Input",
          "Overflow",
          "Overshoot",
          "Resource",
          "Scarcity",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "DIFFUSION",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-5a83ead44e1f",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Cycle",
          "Delay",
          "Dilution",
          "Gradient",
          "Input",
          "Loop",
          "Overflow",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "Source",
          "Spread",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "DIFFUSION",
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-d2652786660e",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Input",
          "Loop",
          "Overflow",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Source",
          "Spread",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "DIFFUSION",
          "OSCILLATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-f60a883c46dc",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Cycle",
          "Delay",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Input",
          "Overflow",
          "Overshoot",
          "Resource",
          "Scarcity",
          "Source",
          "Spread",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "FEEDBACK",
          "OSCILLATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-dfdb79d26b5d",
        "supporting_lineages": [
          "pond:accumulation:16eb311b61f8f6b2",
          "pond:accumulation:42a3759a8f240fdf",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Consumption",
          "Cycle",
          "Delay",
          "Exhaustion",
          "Input",
          "Loop",
          "Overflow",
          "Overshoot",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "DIFFUSION",
          "FEEDBACK"
        ],
        "pathway_id": "P041-CP-029-a490c12617c5",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Delay",
          "Dilution",
          "Escalation",
          "Gain",
          "Gradient",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "DIFFUSION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-25bc6ecee920",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Dilution",
          "Escalation",
          "Gain",
          "Gradient",
          "Input",
          "Overshoot",
          "Propagation",
          "Source",
          "Spread",
          "State"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "DIFFUSION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-2fc5aaff51e9",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Dilution",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Gradient",
          "Input",
          "Propagation",
          "Resource",
          "Scarcity",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-842f434127d5",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Escalation",
          "Gain",
          "Input",
          "Loop",
          "Overshoot",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-23b5059952bb",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "BUFFERING",
          "OSCILLATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-1712b6e2278e",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Cycle",
          "Delay",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Overshoot",
          "Propagation",
          "Resource",
          "Scarcity",
          "State"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "DIFFUSION",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-37c4774b3745",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Dilution",
          "Escalation",
          "Gain",
          "Gradient",
          "Input",
          "Loop",
          "Overshoot",
          "Propagation",
          "Reinforcement",
          "Response",
          "Signal",
          "Source",
          "Spread",
          "State"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "DIFFUSION",
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-709b2f2a2741",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Dilution",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Gradient",
          "Input",
          "Loop",
          "Propagation",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "DIFFUSION",
          "OSCILLATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-f705d44c4d80",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Cycle",
          "Delay",
          "Dilution",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Gradient",
          "Input",
          "Overshoot",
          "Propagation",
          "Resource",
          "Scarcity",
          "Source",
          "Spread",
          "State"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "AMPLIFICATION",
          "FEEDBACK",
          "OSCILLATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-9d58b7b5e9a6",
        "supporting_lineages": [
          "pond:amplification:18f5d2d240960f8d",
          "pond:amplification:1b5b2323489efb04",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Cycle",
          "Delay",
          "Escalation",
          "Exhaustion",
          "Gain",
          "Input",
          "Loop",
          "Overshoot",
          "Propagation",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "DIFFUSION",
          "FEEDBACK",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-029-bca1863ef3a9",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Cycle",
          "Delay",
          "Dilution",
          "Gradient",
          "Input",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Response",
          "Signal",
          "Source",
          "Spread",
          "State"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "DIFFUSION",
          "FEEDBACK",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-7a705d7ea24b",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Delay",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Input",
          "Loop",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Source",
          "Spread"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "DIFFUSION",
          "OSCILLATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-ba37a5adfeba",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Cycle",
          "Delay",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Input",
          "Overshoot",
          "Resource",
          "Scarcity",
          "Source",
          "Spread",
          "State"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "BUFFERING",
          "FEEDBACK",
          "OSCILLATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-d8751c36e6ad",
        "supporting_lineages": [
          "pond:buffering:010a47fc50ece231",
          "pond:buffering:058131c3d6047bc5",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Absorption",
          "Buffer",
          "Consumption",
          "Cycle",
          "Delay",
          "Exhaustion",
          "Input",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "State"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "DIFFUSION",
          "FEEDBACK",
          "OSCILLATION",
          "RESOURCE_DEPLETION"
        ],
        "pathway_id": "P041-CP-029-fb4027b54704",
        "supporting_lineages": [
          "pond:diffusion:0b89588dcc61beff",
          "pond:diffusion:1295d8896f93fcd8",
          "pond:feedback:025e697cd0540aa5",
          "pond:feedback:1ce9e53fa76e84ab",
          "pond:oscillation:019f81b9c8cdc87f",
          "pond:oscillation:361241c5a28eb54e",
          "pond:resource_depletion:02ad5ee5193ae3c9",
          "pond:resource_depletion:1470dfb316e6a70c"
        ],
        "supporting_motifs": [
          "Consumption",
          "Cycle",
          "Delay",
          "Dilution",
          "Exhaustion",
          "Gradient",
          "Loop",
          "Overshoot",
          "Reinforcement",
          "Resource",
          "Response",
          "Scarcity",
          "Signal",
          "Source",
          "Spread",
          "State"
        ]
      }
    ],
    "case_id": "P041-CP-029",
    "observation": "Reserve staff keep service smooth while tickets spread across teams. Once staff capacity drains, returning delay signals increase repeated contacts."
  },
  {
    "candidate_pathways": [
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "FLOW"
        ],
        "pathway_id": "P041-CP-030-52be5efbb22c",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Flow",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Source",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-030-0a5be10abe95",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:oscillation:49eecdfdee1794e8",
          "pond:oscillation:8ca1805f5f03f852"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Cycle",
          "Delay",
          "Input",
          "Overflow",
          "Overshoot",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-030-056266598ca0",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Failure",
          "Friction",
          "Input",
          "Overflow",
          "Rotation",
          "Storage",
          "Support"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "ACCUMULATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-030-a9d5c09794ef",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Input",
          "Limit",
          "Overflow",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FLOW",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-030-79f54471e6e6",
        "supporting_lineages": [
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:49eecdfdee1794e8",
          "pond:oscillation:8ca1805f5f03f852"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Flow",
          "Overshoot",
          "Path",
          "Resistance",
          "Source",
          "State"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FLOW",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-030-6e02c2512547",
        "supporting_lineages": [
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Failure",
          "Flow",
          "Friction",
          "Path",
          "Resistance",
          "Rotation",
          "Source",
          "Support"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-030-760203d9f8a6",
        "supporting_lineages": [
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Flow",
          "Limit",
          "Path",
          "Resistance",
          "Source",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "OSCILLATION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-030-2c09be447fdc",
        "supporting_lineages": [
          "pond:oscillation:49eecdfdee1794e8",
          "pond:oscillation:8ca1805f5f03f852",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Failure",
          "Friction",
          "Overshoot",
          "Rotation",
          "State",
          "Support"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-030-cb0eb66ea763",
        "supporting_lineages": [
          "pond:oscillation:49eecdfdee1794e8",
          "pond:oscillation:8ca1805f5f03f852",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Cycle",
          "Delay",
          "Limit",
          "Overshoot",
          "State",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 2,
        "mechanisms": [
          "SUPPORTED_ROTATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-030-b25b8c1b106f",
        "supporting_lineages": [
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Failure",
          "Friction",
          "Limit",
          "Rotation",
          "StateChange",
          "Support",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "FLOW",
          "OSCILLATION"
        ],
        "pathway_id": "P041-CP-030-407d24ab2957",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:49eecdfdee1794e8",
          "pond:oscillation:8ca1805f5f03f852"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Cycle",
          "Delay",
          "Flow",
          "Input",
          "Overflow",
          "Overshoot",
          "Path",
          "Resistance",
          "Source",
          "State",
          "Storage"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "FLOW",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-030-276c01b1d087",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Failure",
          "Flow",
          "Friction",
          "Input",
          "Overflow",
          "Path",
          "Resistance",
          "Rotation",
          "Source",
          "Storage",
          "Support"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "FLOW",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-030-bbdc06c2b7e8",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Flow",
          "Input",
          "Limit",
          "Overflow",
          "Path",
          "Resistance",
          "Source",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "OSCILLATION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-030-36b49559c4a3",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:oscillation:49eecdfdee1794e8",
          "pond:oscillation:8ca1805f5f03f852",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Cycle",
          "Delay",
          "Failure",
          "Friction",
          "Input",
          "Overflow",
          "Overshoot",
          "Rotation",
          "State",
          "Storage",
          "Support"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-030-5b442c8a295f",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:oscillation:49eecdfdee1794e8",
          "pond:oscillation:8ca1805f5f03f852",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Cycle",
          "Delay",
          "Input",
          "Limit",
          "Overflow",
          "Overshoot",
          "State",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "ACCUMULATION",
          "SUPPORTED_ROTATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-030-b48de55f90bf",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Failure",
          "Friction",
          "Input",
          "Limit",
          "Overflow",
          "Rotation",
          "StateChange",
          "Storage",
          "Support",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "FLOW",
          "OSCILLATION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-030-5c0d217c8108",
        "supporting_lineages": [
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:49eecdfdee1794e8",
          "pond:oscillation:8ca1805f5f03f852",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "Cycle",
          "Delay",
          "Failure",
          "Flow",
          "Friction",
          "Overshoot",
          "Path",
          "Resistance",
          "Rotation",
          "Source",
          "State",
          "Support"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "FLOW",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-030-1932e7ec477e",
        "supporting_lineages": [
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:49eecdfdee1794e8",
          "pond:oscillation:8ca1805f5f03f852",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Cycle",
          "Delay",
          "Flow",
          "Limit",
          "Overshoot",
          "Path",
          "Resistance",
          "Source",
          "State",
          "StateChange",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "FLOW",
          "SUPPORTED_ROTATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-030-5d5ad750ecdc",
        "supporting_lineages": [
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Failure",
          "Flow",
          "Friction",
          "Limit",
          "Path",
          "Resistance",
          "Rotation",
          "Source",
          "StateChange",
          "Support",
          "Trigger"
        ]
      },
      {
        "combination_depth": 3,
        "mechanisms": [
          "OSCILLATION",
          "SUPPORTED_ROTATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-030-b62ff8f03a00",
        "supporting_lineages": [
          "pond:oscillation:49eecdfdee1794e8",
          "pond:oscillation:8ca1805f5f03f852",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Cycle",
          "Delay",
          "Failure",
          "Friction",
          "Limit",
          "Overshoot",
          "Rotation",
          "State",
          "StateChange",
          "Support",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "FLOW",
          "OSCILLATION",
          "SUPPORTED_ROTATION"
        ],
        "pathway_id": "P041-CP-030-cd00f2171f0c",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:49eecdfdee1794e8",
          "pond:oscillation:8ca1805f5f03f852",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af"
        ],
        "supporting_motifs": [
          "BuildUp",
          "Cycle",
          "Delay",
          "Failure",
          "Flow",
          "Friction",
          "Input",
          "Overflow",
          "Overshoot",
          "Path",
          "Resistance",
          "Rotation",
          "Source",
          "State",
          "Storage",
          "Support"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "FLOW",
          "OSCILLATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-030-349d823fb5ff",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:49eecdfdee1794e8",
          "pond:oscillation:8ca1805f5f03f852",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Cycle",
          "Delay",
          "Flow",
          "Input",
          "Limit",
          "Overflow",
          "Overshoot",
          "Path",
          "Resistance",
          "Source",
          "State",
          "StateChange",
          "Storage",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "FLOW",
          "SUPPORTED_ROTATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-030-3e873be4c3d1",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Failure",
          "Flow",
          "Friction",
          "Input",
          "Limit",
          "Overflow",
          "Path",
          "Resistance",
          "Rotation",
          "Source",
          "StateChange",
          "Storage",
          "Support",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "ACCUMULATION",
          "OSCILLATION",
          "SUPPORTED_ROTATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-030-0acd6eaf4133",
        "supporting_lineages": [
          "pond:accumulation:0b8b507e57754286",
          "pond:accumulation:10c2c8ae31c87504",
          "pond:oscillation:49eecdfdee1794e8",
          "pond:oscillation:8ca1805f5f03f852",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "BuildUp",
          "Cycle",
          "Delay",
          "Failure",
          "Friction",
          "Input",
          "Limit",
          "Overflow",
          "Overshoot",
          "Rotation",
          "State",
          "StateChange",
          "Storage",
          "Support",
          "Trigger"
        ]
      },
      {
        "combination_depth": 4,
        "mechanisms": [
          "FLOW",
          "OSCILLATION",
          "SUPPORTED_ROTATION",
          "THRESHOLD"
        ],
        "pathway_id": "P041-CP-030-383de2aafbf9",
        "supporting_lineages": [
          "pond:flow:8725e050fc43ca48",
          "pond:flow:8fb2c710a8e84550",
          "pond:oscillation:49eecdfdee1794e8",
          "pond:oscillation:8ca1805f5f03f852",
          "pond:supported_rotation:18f72fc932ab6180",
          "pond:supported_rotation:1de1ef328a4b75af",
          "pond:threshold:015d065dc2d74199",
          "pond:threshold:1dbfe551705dbe5c"
        ],
        "supporting_motifs": [
          "Accumulation",
          "Cycle",
          "Delay",
          "Failure",
          "Flow",
          "Friction",
          "Limit",
          "Overshoot",
          "Path",
          "Resistance",
          "Rotation",
          "Source",
          "State",
          "StateChange",
          "Support",
          "Trigger"
        ]
      }
    ],
    "case_id": "P041-CP-030",
    "observation": "A turning distributor creates periodic release waves. The waves build a queue at a restricted route, and the queue triggers a limit rule."
  }
]
```
