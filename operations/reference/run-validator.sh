#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source node.env
[[ "$NODE_ROLE" =~ ^[ABCDE]$ ]] || exit 1
exec bin/validator \
  --datadir=consensus/validator-data --wallet-dir=consensus/wallet \
  --wallet-password-file="validators/node-$NODE_ROLE/password.txt" \
  --chain-config-file=consensus/config.yaml \
  --beacon-rpc-provider=127.0.0.1:4000 \
  --suggested-fee-recipient="$FEE_RECIPIENT" --suggested-gas-limit=60000000 --graffiti="MCN-$NODE_ROLE" --monitoring-host=127.0.0.1 --monitoring-port=8081 \
  --accept-terms-of-use
