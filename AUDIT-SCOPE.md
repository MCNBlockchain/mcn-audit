# Audit scope and evidence gaps

## Changes recorded by the recovered bundle

- Deposit contract minimum changes from 1 ether to 250 ether, according to PROVENANCE.md.
- Custom consensus balances and network/fork configuration.
- Genesis allocation and system-contract storage initialization.
- Client code modifications, if any, have not yet been established.

## Evidence required

- [ ] Owner-confirmed repository and access policy.
- [ ] Exact Geth and Prysm commit SHAs, build instructions and binary hashes.
- [ ] Diff against upstream for all client and contract changes.
- [ ] Running network execution genesis, consensus genesis and their hashes.
- [ ] Sanitized deployment configuration reconciled with this bundle.
- [ ] Reproducible deposit-contract compilation and artifact comparison.
- [ ] Confirmed current validator topology and public parameters.

## Required behavior checks

- [ ] Deposit signatures, invalid data, minimum amounts and repeat deposits.
- [ ] Activation and effective-balance accounting.
- [ ] New validator voluntary exit and receipt by the withdrawal address.
- [ ] Partial withdrawals and compounding credentials 0x02.
- [ ] Rewards, penalties, slashing and supply accounting.
- [ ] Fork transitions and execution/consensus agreement.
- [ ] Loss of finality, node recovery and slashing-protection recovery.
- [ ] Investigation of the previously discussed chain divergence.
- [ ] RPC exposure and administrative endpoint restrictions.

No completed check is asserted by this file. Historical validation notes are in
`network/VALIDATION.md`; they do not establish present deployment correctness.
