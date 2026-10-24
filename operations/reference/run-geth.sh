#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source node.env
[[ -s execution/data/geth/chaindata/CURRENT ]] || [[ -d execution/data/geth/chaindata ]] || { echo 'Run 03-init.sh'; exit 1; }
args=()
[[ ! -f execution/peers.toml ]] || args+=(--config=execution/peers.toml)
if [[ -n "${PUBLIC_IP:-}" && "$PUBLIC_IP" != REPLACE_WITH_THIS_SERVER_IP ]]; then args+=(--nat="extip:$PUBLIC_IP"); fi
exec bin/geth \
  --datadir=execution/data --state.scheme=path --cache=512 --networkid=2325 --syncmode=full \
  --miner.gaslimit=60000000 --miner.gasprice=1000000000 --txpool.pricelimit=1000000000 --port=30303 --discovery.v4=true --bootnodes=enode://1f76ad3ec6bdc79a301fdb5d71d51dcf371df9d6a730e6022978164f54e7ff4411910e196fe827c53fadef344c853a685f1ec04e3460f6e90153f4d524b28832@103.228.169.164:30303,enode://7bd55d5a1131d35004588193a0b6f6f84595f1e76ce34a6006de25241665ce282d364a8f02843f8df04fe28362b916bd818f95d29c447c31f31e7eb81a88b61b@38.180.143.231:30303,enode://0483248049ef2dbe6715ea765451209fc88e215c3aa92abc42477bcbd548d98ea45787e69b6f5b56a0d469cd958264e1f74a860cac90ad3236f60071039d2c6a@195.35.29.253:30303,enode://48a8921c651048cd5e505afbef5b0a9cfa5b62810e218abb47e8d28c55dbd8e6570405daa041ce7e761c9022efdf2957b33216d28456475f1edc3445b8f85b8b@77.73.20.222:30303 \
  --http --http.addr=127.0.0.1 --http.port=8545 --http.api=eth,net,web3 \
  --authrpc.addr=127.0.0.1 --authrpc.port=8551 --authrpc.vhosts=localhost,127.0.0.1 \
  --authrpc.jwtsecret=secrets/jwt.hex "${args[@]}"
