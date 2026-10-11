# Audit scope

## Components

- Deposit contract: amount validation, deposit data root and Merkle tree.
- Consensus configuration: balances, churn, fork schedule, rewards and penalties.
- Genesis: execution allocation, validator balances and system-contract storage.
- Genesis tools: deposit signatures, withdrawal credentials and allocation logic.

## Outstanding requirements

- Exact Geth and Prysm commit SHAs and any client patches.
- Reproducible client builds and deployed binary checksums.
- Reproduction of the deposit contract artifact with the documented compiler settings.
- Full decoding and validation of the consensus genesis state.
- Confirmation that committed configuration and genesis match the deployed network.
- Tests covering deposits, activation, withdrawals, exits, slashing and fork transitions.
- Finality and recovery tests, including investigation of chain divergence.

The referenced client releases are Geth 1.17.6 and Prysm 7.2.0.
Client source trees and original genesis deposit inputs are not included.
