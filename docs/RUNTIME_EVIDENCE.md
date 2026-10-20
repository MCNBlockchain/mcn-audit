# Optional runtime data collection

`tools/collect_runtime.py` collects public API responses, chain state through IPC and binary hashes. It does not read wallets, passwords, JWTs or signing databases, and does not restart services or send transactions. Run it as the node user if an auditor requests runtime snapshots.

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

The output directory must be new and outside the repository. Review the files before sharing. Errors are recorded, and missing endpoints or network identity mismatches produce a nonzero exit. API calls are sequential; compare a common finalized checkpoint when comparing nodes collected at different times.
