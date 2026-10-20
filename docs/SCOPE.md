# Audit scope

- Modified deposit contract: source, ABI, reproducible compilation, genesis code/storage, deposit tree and amount checks.
- Execution/consensus genesis consistency, network identifiers, fork schedule, supply allocation and validator initialization.
- MCN consensus parameters: 10-second slots, 32 slots per epoch, 60,000,000 genesis gas limit, activation threshold and effective-balance cap.
- Integration with Geth 1.17.6 and Prysm 7.2.0: deposits, activation, rewards, penalties, exits and withdrawals.

The current deployment is a test network for the audit. Mainnet infrastructure and independent-validator onboarding are planned after the audit.

The stablecoin, existing BNB Chain token, bridges and third-party explorer software are outside this submission's contract scope unless separately agreed with the auditor.
