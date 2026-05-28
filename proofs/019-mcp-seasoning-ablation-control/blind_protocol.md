# Blind Protocol

## Separation Rule

Scoring occurs before reveal. Each task is scored using anonymized labels only: `solution_A`, `solution_B`, and `solution_C`.

## Scoring Packet

The scoring packet contains task prompt, anonymous solution text, and the rubric. It does not include filenames, runtime response paths, consult refs, mode labels, or narrative clues that identify baseline, seasoned, or ablated mode.

## Reveal Rule

The reveal mapping is written only after `blind_scoring_results.json` is complete. Reveal mappings are stored in `task_verdict.json`, not in blind scoring files.

## Rubric

Each anonymous solution receives 0-5 points for contradiction handling, authority handling, replayability, prioritization quality, operational continuity, uncertainty discipline, hallucination prevention, actionability, and boundary discipline.
