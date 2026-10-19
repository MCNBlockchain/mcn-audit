# Requested audit scope

## In scope

- Modified deposit contract, ABI, compiler reproducibility, genesis preallocation code/storage, deposit tree and amount boundaries.
- EL/CL genesis agreement, chain/fork identifiers, fork activation timing, consensus configuration overrides, genesis supply and validator initialization.
- Interaction of minimum deposit (250), activation threshold (10,000), effective-balance cap (100,000), compounding credentials, churn, exits, withdrawals and penalties.
- Integration of the reported unmodified Geth 1.17.6 and Prysm 7.2.0 with custom network parameters. Review source/binary provenance and any actual deployment delta. Full upstream client audits are a separate scope/budget decision.
- Fork-choice recovery and signing safety across restart/recovery.
- Validator key custody, slashing protection, backup/restore, service configuration, network exposure and RPC/archive trust boundaries once runtime evidence is supplied.
- Realistic 10-second-slot / 60M-gas load and failure tests; operational decentralization claims and correlated outage assumptions.

## Explicit exclusions unless separately commissioned

- Stablecoin contract: not supplied for review; no stablecoin security assertion is possible.
- Existing MCN BEP-20 on BNB Chain, bridges, exchange custody and backing/reserves.
- Comprehensive audits of Blockscout, beacon-explorer source, WalletConnect or third-party price providers. Their deployments, exposed API surfaces and display assumptions may still be assessed operationally.

## Questions that need written answers

1. Does every genesis allocation and CL premine reconcile, and are all system-contract constructors represented correctly?
2. Does this exact fork/configuration combination execute deposits, activation, reward accounting, partial/full withdrawals and reorgs correctly?
3. How does genesis effective balance 10,000 transition toward the configured Electra cap, and do reward/penalty estimates use the actual state?
4. Are public RPC APIs bounded, and are Engine/debug/signing interfaces isolated?
5. Can an operator recover from a server outage without losing slashing protection or duplicating signing keys?

A positive result for one item must not be generalized to the others. Findings should identify code/configuration revision, reproduction, impact, mitigation and retest evidence.
