# Collect runtime evidence

The preparer could not authenticate to the VPS hosts. No live deployment inspection is claimed. Run the read-only collector locally on each host after copying `tools/collect_runtime.py` there. It reads public APIs, public chain state through IPC and binary files; no wallet, environment, JWT or signing database is read. Outputs include public withdrawal addresses; review before sharing. No sudo is needed if the normal node user can read the binary and IPC.

Example on validator E (use the appropriate label on A–D):

```sh
python3 collect_runtime.py --label E --root "$HOME/mcn-launch"   --out "$HOME/mcn-audit-E-$(date -u +%Y%m%dT%H%M%SZ)"
```

Scan:

```sh
python3 collect_runtime.py --label scan --root "$HOME/mcnscan-archive"   --beacon-url http://172.30.232.1:23500   --out "$HOME/mcn-audit-scan-$(date -u +%Y%m%dT%H%M%SZ)"
```

RPC:

```sh
python3 collect_runtime.py --label rpc --root "$HOME/mcn-rpc"   --out "$HOME/mcn-audit-rpc-$(date -u +%Y%m%dT%H%M%SZ)"
```

The destination must not already exist and must be outside the repository. Each response/error is saved; identity mismatches or missing endpoints cause a nonzero exit. A nonzero exit is evidence to investigate, not a reason to weaken the checks. Sequential calls are not atomic. Compare a common finalized root on all nodes rather than demanding identical heads from different collection times.

## Additional evidence still needed

- Reviewed service unit contents and launch arguments for seven nodes, showing sync/archive mode, fork/config paths, peer/discovery and bind interfaces. Manually redact tokens/password arguments; do not export `systemctl show Environment` or full `.env` files.
- Compare installed binary fingerprints with independently verified upstream release hashes/signatures or a documented reproducible build. The collector's hash alone cannot prove origin.
- Current config/genesis hashes on every host, independently compared to this repository's manifest; confirm inherited parameters via `/eth/v1/config/spec`.
- Firewall, reverse-proxy API method limits and external exposure checks; private Engine/debug/JWT scope.
- Validator custody/backup/restore and slashing-protection review, handled privately with the auditor; never commit these secrets or databases.
- Current chain integration receipts/epochs/payouts for the pending matrix; resource metrics, monitoring/alerts and capacity plan.
- Beacon explorer deployment name/version/configuration and backend source, plus Blockscout version/configuration evidence.

Do not change genesis, delete live databases, restart validators or send transactions just to run this collector. Those actions are not performed by it.
