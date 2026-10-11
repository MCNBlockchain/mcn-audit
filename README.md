# MCN Blockchain — Audit Preparation

Historical source and configuration bundle recovered from the previous MCN chat.
This repository is an audit preparation package, not an audit report or certification.

## Scope

- `network/contracts/`: deposit contract, compiled artifact, system allocation and upstream provenance.
- `network/consensus/config.yaml`: consensus parameters.
- `network/tools/` and `network/scripts/`: genesis preparation, validation and node operation.
- `network/systemd/` and `network/nginx/`: deployment configuration.
- `SOURCE-MANIFEST.json`: SHA-256 hashes of recovered files.

Client versions recorded by the bundle: Geth 1.17.6 and Prysm 7.2.0.
The clients' complete source trees and exact commit SHAs are not included.
The deployment correspondence and reproducibility of this package remain unverified.

## Recorded network parameters

Chain ID 2325; native currency MCN; 18 decimals; 12-second slots;
32 slots per epoch; activation balance 10,000 MCN; minimum deposit 250 MCN;
six genesis validators; initial allocation 120,000,000 MCN.
These are historical bundle values, not a live network assertion.

## Before audit

See [AUDIT-SCOPE.md](AUDIT-SCOPE.md) for missing evidence and required checks.
Existing launch instructions are preserved in `network/README.md`.
They contain stale references to five validators and a 3/2 split: the six-validator
revision records a 3/3 split. Resolve this discrepancy before using the instructions.

Do not commit validator keys, keystore passwords, JWT secrets or node databases.
Public genesis files from the running network must be collected separately and verified.
Upstream license information is preserved under `network/contracts/`;
no project-wide license has been selected by the owner.
