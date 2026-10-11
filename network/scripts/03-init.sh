#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
umask 077
source node.env
[[ "$NODE_ROLE" == A || "$NODE_ROLE" == B ]] || { echo 'NODE_ROLE must be A or B'; exit 1; }
sha256sum -c GENESIS-SHA256SUMS
mkdir -p execution/data consensus/beacon-data consensus/validator-data secrets
# JWT is local to this server; never overwrite it during a restart.
[[ -f secrets/jwt.hex ]] || openssl rand -hex 32 > secrets/jwt.hex
chmod 600 secrets/jwt.hex
bin/geth --datadir=execution/data --state.scheme=path init execution/genesis.json
bin/validator accounts import \
  --wallet-dir="consensus/wallet" \
  --keys-dir="validators/node-$NODE_ROLE/keystores" \
  --account-password-file="validators/node-$NODE_ROLE/password.txt" \
  --wallet-password-file="validators/node-$NODE_ROLE/password.txt" \
  --accept-terms-of-use
[[ -s consensus/wallet/direct/accounts/all-accounts.keystore.json ]] || { echo 'Prysm wallet import failed'; exit 1; }
