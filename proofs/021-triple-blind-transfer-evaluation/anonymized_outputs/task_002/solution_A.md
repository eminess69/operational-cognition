# Solution A

Contain first by locking the invoice flag and pausing automation that can edit it. Pull canary logs, tenant request traces, and the available ledger export into a shared incident record. The missing six-hour ledger range should stay unresolved until a fresh export or direct ledger query closes it.

The billing owner can say no charge is currently shown, but that is not enough to close the exposure because the warehouse lag and export gap weaken the evidence. Support tickets should be linked to tenant IDs and compared with canary log entries.

Decision branches:

- If no tenant has posted charges after the direct ledger query and delayed warehouse data arrive, close as no confirmed charge impact.
- If any posted charge appears, move to refund review and customer notice drafting.
- If the automation edit cannot be explained, keep the flag locked and require manual owner approval for reenablement.

Sales can receive internal status language, but external language should wait for exposure and charge-impact boundaries.
