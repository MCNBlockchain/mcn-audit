# Provenance and evidence conventions

- Network inputs: user-supplied `genesis.json`, `genesis.ssz` and `config.yaml`, copied without editing from the current network's package.
- Public seeds: user-supplied peer identities from the ready RPC package.
- Deposit source/artifact/system allocations: existing MCN five-validator launch package. Source baseline compared to the cached Prysm v7.2.0 source; compiler reproduction completed locally.
- Upstream reference: [Prysm v7.2.0](https://github.com/OffchainLabs/prysm/tree/v7.2.0) and [Geth v1.17.6](https://github.com/ethereum/go-ethereum/tree/v1.17.6). Source excerpts are included for parameter/bytecode inspection.
- Client versions recorded in the deployment: Geth `1.17.6-stable-3d84c6b2`; Prysm 7.2.0.
- Original operational templates and discovery patch are reference artifacts.
- `evidence/local/` records checks performed against committed inputs on the preparation workstation. They establish artifact consistency within their stated limits.

Upstream source licenses and SPDX notices are preserved. No blanket relicensing of MCN files is asserted.
