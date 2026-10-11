#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source node.env
[[ -s execution/data/geth/chaindata/CURRENT ]] || [[ -d execution/data/geth/chaindata ]] || { echo 'Run 03-init.sh'; exit 1; }
args=()
[[ ! -f execution/peers.toml ]] || args+=(--config=execution/peers.toml)
if [[ -n "${PUBLIC_IP:-}" && "$PUBLIC_IP" != REPLACE_WITH_THIS_SERVER_IP ]]; then args+=(--nat="extip:$PUBLIC_IP"); fi
exec bin/geth \
  --datadir=execution/data --state.scheme=path --networkid=2325 --syncmode=full \
  --miner.gaslimit=30000000 --port=30303 --bootnodes= \
  --http --http.addr=127.0.0.1 --http.port=8545 --http.api=eth,net,web3 \
  --authrpc.addr=127.0.0.1 --authrpc.port=8551 --authrpc.vhosts=localhost,127.0.0.1 \
  --authrpc.jwtsecret=secrets/jwt.hex "${args[@]}"
