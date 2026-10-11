# MCN Blockchain — Audit Preparation

Audit package containing the deposit contract, network parameters, user-supplied
genesis files and historical genesis generation tools. This is not an audit report.

## Contents

- `network/contracts/`: Solidity source, ABI, bytecode, system allocations and provenance.
- `network/genesis/`: user-supplied execution genesis, consensus genesis and configuration.
- `network/consensus/config.yaml`: configuration used by the historical generator; identical to the supplied configuration.
- `network/tools/prepare.py`: genesis allocation and validator/deposit generation logic.
- `network/tools/verify-genesis.py`: historical checks of generated JSON state and deposits.
- `network/scripts/02-genesis.sh`: generation workflow; provide TREASURY through the environment.
- `network/requirements.txt`: Python generation dependencies.
- `network/VALIDATION.md`: historical validation limitations.
- `AUDIT-SCOPE.md`: audit scope and missing evidence.
- `GENESIS-VERIFICATION.json`: preliminary checks of supplied files.
- `SOURCE-MANIFEST.json`: current file hashes and source attribution.

Recorded client versions: Geth 1.17.6 and Prysm 7.2.0. Exact commit SHAs,
client source changes and reproducible builds remain to be supplied.
Live deployment correspondence and full SSZ validation remain unverified.

Generation tools require a prepared Python environment and Prysm prysmctl.
They generate new random keys and a new genesis, and cannot recreate the supplied
genesis byte-for-byte without its original public deposit inputs.
The historical verifier expects generated JSON state and deposit data, which are
not included, and has not been run against the supplied SSZ.
The generation wrapper was adapted to accept TREASURY from the environment;
server installation, startup and peer-management files were removed.

Do not commit private keys, keystore passwords or JWT secrets.
Upstream license information is preserved in `network/contracts/`;
no project-wide license has been selected by the owner.
