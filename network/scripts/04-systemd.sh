#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT=$(pwd -P)
USER_NAME=$(id -un)
[[ $USER_NAME != root ]] || { echo 'Run as the node user (sudo is used only for installing units)'; exit 1; }
for component in geth beacon validator; do
  sed -e "s|@ROOT@|$ROOT|g" -e "s|@USER@|$USER_NAME|g" "systemd/mcn-$component.service" > "systemd/mcn-$component.generated.service"
  sudo install -m 644 "systemd/mcn-$component.generated.service" "/etc/systemd/system/mcn-$component.service"
done
sudo systemctl daemon-reload
sudo systemctl enable mcn-geth mcn-beacon
sudo systemctl start mcn-geth mcn-beacon
echo "Validators stay stopped. Verify EL/CL peers on both servers before starting mcn-validator."
