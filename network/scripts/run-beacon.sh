#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source node.env
export LIBP2P_TCP_REUSEPORT=false
args=()
if [[ -n "${PUBLIC_IP:-}" && "$PUBLIC_IP" != REPLACE_WITH_THIS_SERVER_IP ]]; then args+=(--p2p-host-ip="$PUBLIC_IP"); fi
if [[ -n "${BEACON_PEER:-}" ]]; then args+=(--peer="$BEACON_PEER"); fi
exec bin/beacon-chain \
  --datadir=consensus/beacon-data \
  --chain-config-file=consensus/config.yaml --genesis-state=consensus/genesis.ssz \
  --execution-endpoint=http://127.0.0.1:8551 --jwt-secret=secrets/jwt.hex \
  --deposit-contract=0x00000000219ab540356cBB839Cbe05303d7705Fa --contract-deployment-block=0 \
  --rpc-host=127.0.0.1 --rpc-port=4000 --http-host=127.0.0.1 --http-port=3500 \
  --p2p-static-id --p2p-tcp-port=13000 --p2p-udp-port=12000 --p2p-quic-port=13000 \
  --bootstrap-node="${BEACON_BOOTNODE:-}" --min-sync-peers=0 \
  --accept-terms-of-use "${args[@]}"
