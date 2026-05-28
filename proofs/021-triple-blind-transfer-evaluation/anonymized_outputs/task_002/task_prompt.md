# Task 002: Billing Flag Exposure Triage

A billing team must decide whether a multi-tenant invoice-flow exposure occurred. The evidence is mixed:

- The feature flag summary says the new flow is off.
- Canary logs show three tenants reached the new invoice path.
- The billing owner says no charge was posted.
- The ledger export is missing a six-hour range.
- The data warehouse is lagging by 12 hours.
- Sales wants no external incident language, while support has related tickets.
- The rollback flag configuration was edited by automation.

Produce a bounded triage and containment plan.
