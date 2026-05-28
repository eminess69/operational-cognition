# Comparative Entropy Report

        | Scenario | Domain | Baseline reconstructed | Pond reconstructed | Improved probes | Verdict |
        | --- | --- | ---: | ---: | ---: | --- |
        | scenario_001 | proof/validator repair | 2 | 11 | 10 | ENTROPY_SCENARIO_ADVANTAGE |
| scenario_002 | config/runtime migration | 1 | 10 | 11 | ENTROPY_SCENARIO_ADVANTAGE |
| scenario_003 | redaction/provenance audit | 1 | 10 | 11 | ENTROPY_SCENARIO_ADVANTAGE |
| scenario_004 | fixture minimization or compression recovery | 3 | 9 | 9 | ENTROPY_SCENARIO_ADVANTAGE |
| scenario_005 | external evaluator or blinded pack preparation | 2 | 10 | 9 | ENTROPY_SCENARIO_ADVANTAGE |

        Aggregate baseline reconstructed count: `9`

        Aggregate pond-backed reconstructed count: `50`

        Contradiction preservation improved in `5` scenarios. Recovery-loop reconstruction improved in `5` scenarios.

        The comparison is bounded to these five local scenario artifacts and does not assert behavior outside this gauntlet.

