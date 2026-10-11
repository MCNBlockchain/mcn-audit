#!/usr/bin/env bash
set -euo pipefail
rpc() { curl -fsS http://127.0.0.1:8545 -H 'Content-Type: application/json' --data "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"$1\",\"params\":$2}"; printf '\n'; }
rpc eth_chainId '[]'
rpc eth_blockNumber '[]'
rpc net_peerCount '[]'
rpc eth_getBlockByNumber '["latest",false]'
for endpoint in node/syncing node/peer_count beacon/genesis beacon/states/head/finality_checkpoints beacon/states/head/validators; do
  curl -fsS "http://127.0.0.1:3500/eth/v1/$endpoint"
  printf '\n'
done
