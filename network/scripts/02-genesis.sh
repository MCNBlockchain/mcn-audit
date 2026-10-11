#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
umask 077
: "${TREASURY:?Treasury is required}"
[[ ! -e consensus/genesis.ssz ]] || { echo 'Genesis already exists; refusing regeneration'; exit 1; }
# Audit generation workflow: uses fresh random validator keys.
GENESIS_TIME=${GENESIS_TIME:-$(( $(date +%s) + 7200 ))}
.venv/bin/python tools/prepare.py --root . --treasury "$TREASURY" --genesis-time "$GENESIS_TIME"
bin/prysmctl testnet generate-genesis \
  --chain-config-file=consensus/config.yaml \
  --deposit-json-file=consensus/deposit_data.json \
  --num-validators=6 --fork=electra --genesis-time="$GENESIS_TIME" \
  --geth-genesis-json-in=execution/genesis-input.json \
  --geth-genesis-json-out=execution/genesis.json \
  --output-ssz=consensus/genesis.ssz --output-json=consensus/genesis-state.json
.venv/bin/python tools/verify-genesis.py
sha256sum execution/genesis.json consensus/config.yaml consensus/genesis.ssz > GENESIS-SHA256SUMS
