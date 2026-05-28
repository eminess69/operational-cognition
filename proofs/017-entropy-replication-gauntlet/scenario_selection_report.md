# Scenario Selection Report

        The five scenarios were selected to avoid sharing a single operational domain. They reuse the same scoring probes but vary the artifact surface, failure mode, authority conflict, and recovery pressure.

        | Scenario | Domain | Contradictions | Redacted-real trace | External/blind pack |
        | --- | --- | ---: | --- | --- |
        | scenario_001 | proof/validator repair | 3 | False | False |
| scenario_002 | config/runtime migration | 2 | False | False |
| scenario_003 | redaction/provenance audit | 4 | True | False |
| scenario_004 | fixture minimization or compression recovery | 2 | False | False |
| scenario_005 | external evaluator or blinded pack preparation | 3 | False | True |

        Independence controls:

        - No scenario shares the same primary domain key.
        - At least two scenarios contain three or more linked contradictions.
        - One scenario uses a redacted-real operational trace.
        - One scenario is designed as an external blinded evaluation pack.

