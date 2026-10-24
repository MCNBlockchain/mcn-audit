# Architecture

Current audit test network:

| Role | Host | Function |
|---|---|---|
| A | 2.29.106.179 | Geth + Prysm beacon + genesis validator 0 |
| B | 103.228.169.164 | Geth + Prysm beacon + genesis validator 1 |
| C | 38.180.143.231 | Geth + Prysm beacon + genesis validator 2 |
| D | 195.35.29.253 | Geth + Prysm beacon + genesis validator 3 |
| E | 77.73.20.222 | Geth + Prysm beacon + genesis validator 4 |
| scan | 187.126.3.145 | Independent archive Geth/beacon; Docker Blockscout; explorer |
| rpc | 159.195.129.170 | Independent non-signing full node and public RPC proxy |

The five validators are operated by the project on separate servers. The scan and RPC nodes do not run validators. Geth runs with discovery v4 enabled and four bootnodes; `execution/peers.toml` supplies its peer configuration.

Mainnet is planned after the audit, on upgraded servers. The operator reports 100 independent validators ready to join after the audit, each with 100,000 MCN.

## Interfaces

Validator hosts use `~/mcn-launch` and systemd units `mcn-geth`, `mcn-beacon`, `mcn-validator`. Geth's Engine API is configured on loopback with JWT authentication.

Scan archive: `~/mcnscan-archive`, units `mcnscan-archive-geth` and `mcnscan-archive-beacon`. Geth HTTP `172.30.232.1:28545`, beacon REST `172.30.232.1:23500`, Engine `127.0.0.1:28551`. Blockscout uses this local archive node. Historical `eth_getBalance` at block 362 was demonstrated in the deployment records.

Public RPC: `~/mcn-rpc`, units `mcn-rpc-geth`/`mcn-rpc-beacon`, upstream HTTP on loopback behind the HTTPS proxy at rpc.mcnblockchain.com. Public modules: eth/net/web3.

Blockscout versions previously reported: backend 9.0.2, frontend 2.3.5. The beacon explorer at beacon.mcnscan.org runs Dora v1.25.0 with MCN branding (`mcn-dora:v1.25.0-mcn1`). Dora listens on `127.0.0.1:18090` behind Nginx and connects to the local archive beacon REST (`172.30.232.1:23500`) and execution RPC (`172.30.232.1:28545`).

## Reference scripts

[run-geth.sh](../operations/reference/run-geth.sh) records the current Geth startup command: full sync, path state scheme, network ID 2325, discovery v4 and four bootnodes. Public JSON-RPC modules are eth/net/web3 on loopback port 8545; the JWT-authenticated Engine API uses loopback port 8551. The same directory includes Prysm launch references.
