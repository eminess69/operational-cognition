# Baseline Final Verdict

No consultation used.

The baseline answer converges on **H1: MCAS single-sensor, repeated-authority control-law failure** as the primary failure mechanism. The strongest common evidence across JT610 and ET302 is that erroneous AOA data could activate MCAS, reset after pilot electric-trim use, and command repeated nose-down stabilizer movement. The FAA return-to-service fixes map directly to this mechanism: use both AOA sensors, prevent repeated MCAS movement, limit trim authority, improve procedures/training, restore AOA Disagree behavior, and add monitoring.

This verdict is evidence-backed but vulnerable to premature convergence. It demotes certification/development assurance, program pressure, human-factors assumptions, accident-specific AOA failure paths, and derivative architecture into supporting context. That makes the baseline too certain that the proximate technical failure is also the primary failure mechanism.

Baseline primary metric: `premature_convergence_resistance = 3` viable explanations active immediately before final convergence (`H1`, `H2`, `H4`).
