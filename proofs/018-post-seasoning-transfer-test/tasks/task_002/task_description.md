# Task 002: Resource Allocation

## Held-out Domain

Resource allocation.

This task was selected as a held-out operational task because it asks for triage across validation risks, not prior trace repair, repair-gate replay, entropy scenario reconstruction, or candidate seasoning.

## Prompt

Prioritize limited validation time across competing failure reports, stale artifacts, and high-risk proof gaps.

Assume a 120-minute validation window and this mixed evidence:

- One report says all required artifacts exist.
- A stale failure report says a consult response failed contract validation before corrected responses were created.
- Runtime responses contain hashes and visible refs, but the runtime consultation log does not expose the refs.
- The final verdict depends on score math, visibility, cross-family combination, and mutation checks.

## Required Pressures

- Contradiction pressure: failure reports and corrected response artifacts disagree.
- Stale or partial information: older failed attempts coexist with newer successful responses.
- Authority conflict: newest response artifacts and older summaries carry different implications.
- Replayable justification: time allocation must be reconstructable from risk and dependency.
- Overclaim possibility: improved local scores could be overstated.
- Operational prioritization: scarce validation time must be spent on the checks most likely to invalidate the result.

## Evaluation Target

A good solution should allocate time to stop-the-line checks first, explain why lower-risk review is deferred, and preserve enough evidence for replay.
