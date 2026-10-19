# Provenance and evidence conventions

- Network inputs: user-supplied `genesis.json`, `genesis.ssz` and `config.yaml`, copied without editing from the current network's package. Historical October 5 genesis and tests are excluded.
- Public seeds: user-supplied peer identities from the ready RPC package. Identities/endpoints may change; live reachability is not attested.
- Deposit source/artifact/system allocations: existing MCN five-validator launch package. Source baseline compared to the cached Prysm v7.2.0 source; compiler reproduction completed locally.
- Upstream reference: [Prysm v7.2.0](https://github.com/OffchainLabs/prysm/tree/v7.2.0) and [Geth v1.17.6](https://github.com/ethereum/go-ethereum/tree/v1.17.6). Source excerpts are included for parameter/bytecode inspection; full sources and release signatures should be acquired independently.
- Reported server Geth version: `1.17.6-stable-3d84c6b2`; Prysm 7.2.0. Installed binary hashes/signatures and the claim of no local client changes are **pending runtime evidence**, not established by a version string.
- Original operational templates and discovery patch are reference artifacts. No remote service files were read during this preparation.
- `evidence/local/` records checks performed against committed inputs on the preparation workstation. They establish artifact consistency within their stated limits.

SHA256SUMS detects accidental changes relative to this snapshot. A committer can regenerate it; it is not an authentication signature. Record the Git commit and independently verify reviewed release/package checksums before deployment. No top-level license is imposed on all MCN files; preserve upstream licenses and have the project owner specify distribution terms for original operational material if publishing publicly.
