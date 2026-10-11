#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
[[ $(uname -s) == Linux && $(uname -m) == x86_64 ]] || { echo 'This installer targets Linux x86_64'; exit 1; }
mkdir -p bin downloads
curl -fL --retry 3 https://gethstore.blob.core.windows.net/builds/geth-linux-amd64-1.17.6-3d84c6b2.tar.gz -o downloads/geth.tar.gz
tar -xzf downloads/geth.tar.gz -C downloads
install -m 755 downloads/geth-linux-amd64-1.17.6-3d84c6b2/geth bin/geth
for name in beacon-chain validator prysmctl; do
  asset="$name-v7.2.0-linux-amd64"
  base="https://github.com/OffchainLabs/prysm/releases/download/v7.2.0/$asset"
  curl -fL --retry 3 "$base" -o "downloads/$asset"
  curl -fL --retry 3 "$base.sha256" -o "downloads/$asset.sha256"
  python3 - "$asset" <<'PY'
import hashlib,sys,re
from pathlib import Path
p=Path('downloads')/sys.argv[1]
s=p.with_name(p.name+'.sha256').read_text()
match=re.search(r'\b[0-9a-fA-F]{64}\b',s)
assert match and hashlib.sha256(p.read_bytes()).hexdigest()==match.group(0).lower(), 'Checksum mismatch'
PY
  install -m 755 "downloads/$asset" "bin/$name"
done
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
bin/geth version
bin/beacon-chain --version
bin/validator --version
