# Architecture and trust boundaries

Topology below is operator-reported. Validate it against collected service configurations, binary hashes and API responses.

| Role | Host | Function |
|---|---|---|
| A | 2.29.106.179 | Geth + Prysm beacon + genesis validator 0 |
| B | 103.228.169.164 | Geth + Prysm beacon + genesis validator 1 |
| C | 38.180.143.231 | Geth + Prysm beacon + genesis validator 2 |
| D | 195.35.29.253 | Geth + Prysm beacon + genesis validator 3 |
| E | 77.73.20.222 | Geth + Prysm beacon + genesis validator 4 |
| scan | 187.126.3.145 | Independent archive Geth/beacon; Docker Blockscout; explorer |
| rpc | 159.195.129.170 | Independent non-signing full node and public RPC proxy |

Five validator servers currently have a common operator and withdrawal destination. Server diversity improves fault isolation, but does not establish independent operators, independent keys/custody or equal provider risk. At equal active weights, losing one of five leaves 80%; losing two leaves 60%, below the two-thirds finality threshold. Recalculate from **actual effective balances**, including future deposits and activation changes.

The scan and RPC nodes add read capacity and peer diversity, not additional validator votes. Public seed files contain four bootstrap peers and are not an exhaustive network membership list. Dynamic discovery was enabled later; peers must be independently checked for discovery configuration, identity consistency and firewall behavior. Six peers per node was reported, not independently measured in this handoff.

## Interfaces

Validator hosts use `~/mcn-launch` and systemd units `mcn-geth`, `mcn-beacon`, `mcn-validator`. Engine API must remain private and JWT authenticated. Signing keys and slashing databases belong only to the intended signing host; never copy a signing wallet to a second active validator.

Scan archive: `~/mcnscan-archive`, units `mcnscan-archive-geth` and `mcnscan-archive-beacon`. Geth HTTP `172.30.232.1:28545`, beacon REST `172.30.232.1:23500`, Engine `127.0.0.1:28551`. The 172.30.232.1 address is the Docker bridge gateway, not an authentication boundary by itself. Verify host firewall/container exposure. Nonstandard ports organize services; they do not provide access control.

The archive was rebuilt to preserve historical state; the operator demonstrated historical `eth_getBalance` at block 362. Verify archive mode, full replay, traces, latest/finalized consistency, disk growth and restart recovery. Colocation with Blockscout introduces shared CPU/RAM/disk risk. Scan is reported as 2 vCPU / 8 GB RAM / 96 GB disk; load and capacity evidence is needed.

Public RPC: `~/mcn-rpc`, units `mcn-rpc-geth`/`mcn-rpc-beacon`, upstream HTTP loopback behind HTTPS proxy at rpc.mcnblockchain.com. Intended public modules: eth/net/web3. Collect actual config: check debug/admin/engine exposure, allowed methods, batch/response/timeout limits, CORS and rate limits. No assertion that these controls were verified remotely is made here.

Blockscout versions previously reported: backend 9.0.2, frontend 2.3.5. The beacon explorer at beacon.mcnscan.org runs Dora v1.25.0 with MCN branding (`mcn-dora:v1.25.0-mcn1`). Dora listens on `127.0.0.1:18090` behind Nginx and connects to the local archive beacon REST (`172.30.232.1:23500`) and execution RPC (`172.30.232.1:28545`).

The explorer currently displays a price associated with the existing BNB Chain MCN token. This off-chain display does not establish native MCN market liquidity, a redemption promise, a bridge, stablecoin backing or a consensus price oracle.

## Reference scripts

Files under `operations/reference/` are original launch templates, not a deployable current-state backup. In particular the original Geth script predates the discovery change. `operations/patches/configure-geth-discovery.py` records that later patch, but has not been applied by this repository to any server. Do not run reference scripts blindly against production. Collect sanitized current unit/script settings first.
