# Solution B

Check whether the feature flag is off now, then ask the billing owner to verify that no charges were posted. If the owner confirms no charges, keep the flow disabled and monitor the support tickets for any further customer reports. The data warehouse delay means the team should check again after 12 hours.

The canary logs should be reviewed to see whether the tenants actually completed the new invoice path or only loaded it. If they only loaded it, this can be treated as a low-impact exposure. If they completed it, notify support and prepare a customer response.

The rollback automation should be reviewed before the flag is reenabled. Do not make a public statement until the charge status is clearer.
