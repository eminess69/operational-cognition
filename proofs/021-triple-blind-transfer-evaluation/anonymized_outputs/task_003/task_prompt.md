# Task 003: Support Queue SLA Rebalance

A support operations lead must rebalance queues under stale service data. The evidence is mixed:

- The SLA dashboard is green, but its export is 18 hours old.
- Frontline tickets show aging in one enterprise queue.
- A manager wants immediate reassignment from the onboarding queue.
- The workforce owner says new hires are not trained for enterprise cases.
- The VIP account list changed after the dashboard export.
- Product says a fix reduced ticket volume, but support cannot yet verify that.

Produce a bounded queue plan with decision gates and replayable evidence.
