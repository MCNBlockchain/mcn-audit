# MCN Blockchain — audit handoff repository

Audit materials for the MCN test network launched **2026-10-17**. No production credentials or validator databases are included.

The current network has five project-operated validators on separate servers. Mainnet is planned after the audit, on upgraded infrastructure, with independent validators joining. The operator reports that 100 independent validators, each with 100,000 MCN, are ready to join after the audit.

## Start here

1. [Scope and questions for the auditor](docs/SCOPE.md)
2. [Network parameters and genesis](docs/NETWORK.md)
3. [Architecture and trust boundaries](docs/ARCHITECTURE.md)
4. [Contract provenance and reproduction](docs/CONTRACT.md)
5. [Test results](docs/TEST_MATRIX.md)
6. [Completed local checks](evidence/local/RESULTS.md)
7. [Optional runtime data collection](docs/RUNTIME_EVIDENCE.md)

Public network endpoints:

- Execution explorer: https://mcnscan.org
- Beacon explorer: https://beacon.mcnscan.org
- Public execution RPC: https://rpc.mcnblockchain.com

## Contents

`network/` contains the exact supplied genesis files and public seed peers. `contracts/` contains the modified deposit source, upstream source, one-line diff, compiler input and compiled artifact. `upstream/` contains the particular client source excerpts used to compare defaults/system bytecode, not complete client repositories. `operations/reference/` contains the current Geth launch script supplied by the operator and Prysm launch references. `evidence/local/` records locally reproduced checks. `tools/` and `tests/` make those checks repeatable.

## Reproduce

Run from this repository root. Python 3.11+ is needed for standard-library checks; the recorded EVM run used Python 3.13. Dependencies and a compatible Node.js runtime are required for the other checks.

```sh
python3 tools/verify_snapshot.py
python3 -m venv .venv
.venv/bin/python -m pip install -r tests/requirements.txt
.venv/bin/python -m unittest discover -s tests -v

# Optional independent execution-genesis reconstruction, using a verified Geth binary:
.venv/bin/python tools/verify_geth_genesis.py --geth /absolute/path/to/geth
cd contracts
npm ci
npm run verify
```

Compiler: **solc 0.6.11+commit.5ef660b1**, optimizer enabled, 200 runs, source key `deposit_contract.sol`. The lockfile pins compiler dependencies. Packages are not vendored; installation requires network access. The SSZ checker is specific to this Electra state layout and is not a general SSZ implementation.

The execution genesis includes initialized system contracts. The supplied genesis files are the exact inputs used by the local verification tools.

## Licenses

Upstream licenses and SPDX notices are preserved in `licenses/` and source files. The deposit source carries CC0-1.0; copied Prysm and Geth source remains under its respective upstream notices. No blanket relicensing of MCN material is asserted. See [provenance](docs/PROVENANCE.md).
