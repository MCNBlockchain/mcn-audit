# Node launch scripts

`run-geth.sh` records the current Geth startup command supplied by the operator. It enables discovery v4, configures four bootnodes and loads `execution/peers.toml` when present.

`run-beacon.sh` and `run-validator.sh` are Prysm launch references.

The scripts use the node deployment layout: `scripts/` alongside `bin/`, `execution/`, `consensus/` and `node.env`. Runtime credentials, wallets and databases are not included in this repository.
