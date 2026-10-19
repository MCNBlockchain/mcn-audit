# Completed checks — 2026-10-19

Executed on the preparation workstation (macOS arm64), against this repository's supplied network inputs. No remote node authentication, production mutation or production signing was performed.

| Check | Result | Limit |
|---|---|---|
| `python3 tools/verify_snapshot.py` | PASS | Specific Electra SSZ layout; checks listed assertions, not the full consensus transition |
| Exact solc rebuild | PASS | solc 0.6.11+commit.5ef660b1.Emscripten.clang, optimizer 200; compares creation/runtime/ABI/layout |
| `python -m unittest discover -s tests -v` | 8 tests passed | PyEVM simulation of exact deposit allocation; not a Prysm integration test |
| Geth init/export, Keccak(RLP(genesis header)) | PASS | Local Geth v1.17.6; exported block/hash in this directory, not remote attestation |

EVM environment: Python 3.13, eth-tester 0.13.0b1, py-evm 0.12.1b1; exact dependency freeze in `tests/requirements.txt`. The compiler was loaded from an existing local installation via `MCN_SOLC_MODULE`; `npm ci` was not rerun during preparation. Dependency installation and collector operation on Ubuntu hosts remain to be exercised there.

Raw reports: `genesis-analysis.json`, `geth-genesis.json`, `genesis-block.rlp`. SHA256SUMS is generated after the snapshot is complete. Console output is recorded alongside these reports. No test here proves audit completion, peer connectivity, network stability, APR, safe custody, correct integration withdrawals.
