#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source node.env
export LIBP2P_TCP_REUSEPORT=false
[[ "$NODE_ROLE" =~ ^[ABCDE]$ ]] || exit 1
[[ "$PUBLIC_IP" != REPLACE_WITH_THIS_SERVER_IP && -n "$PUBLIC_IP" ]] || { echo 'Set PUBLIC_IP'; exit 1; }
args=()
if [[ -f consensus/peers.json ]]; then
  peer_lines=$(python3 -c 'import json; p=json.load(open("consensus/peers.json"))["multiaddrs"]; assert len(p)==4; print("\n".join(p))')
  while IFS= read -r peer; do args+=(--peer="$peer"); done <<< "$peer_lines"
  enr_lines=$(python3 -c 'import json; p=json.load(open("consensus/peers.json"))["enrs"]; assert len(p)==4; print("\n".join(p))')
  while IFS= read -r enr; do args+=(--bootstrap-node="$enr"); done <<< "$enr_lines"
else
  # Start APIs to collect identities; validators remain stopped.
  args+=(--bootstrap-node=)
fi
exec bin/beacon-chain \
  --datadir=consensus/beacon-data \
  --chain-config-file=consensus/config.yaml --genesis-state=consensus/genesis.ssz \
  --execution-endpoint=http://127.0.0.1:8551 --jwt-secret=secrets/jwt.hex \
  --deposit-contract=0x00000000219ab540356cBB839Cbe05303d7705Fa --contract-deployment-block=0 \
  --rpc-host=127.0.0.1 --rpc-port=4000 --http-host=127.0.0.1 --http-port=3500 \
  --monitoring-host=127.0.0.1 --monitoring-port=8080 \
  --p2p-host-ip="$PUBLIC_IP" --p2p-static-id \
  --p2p-tcp-port=13000 --p2p-udp-port=12000 --p2p-quic-port=13000 \
  --min-sync-peers=2 --suggested-fee-recipient="$FEE_RECIPIENT" \
  --accept-terms-of-use "${args[@]}"
