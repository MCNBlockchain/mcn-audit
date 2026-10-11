# MCN Blockchain

Proof-of-stake network with native currency MCN and chain ID 2325.

## Network parameters

| Parameter | Value |
| --- | --- |
| Decimals | 18 |
| Slot duration | 12 seconds |
| Slots per epoch | 32 |
| Genesis validators | 6 |
| Minimum deposit | 250 MCN |
| Activation balance | 10,000 MCN |
| Maximum compounding effective balance | 640,000 MCN |
| Ejection balance | 8,000 MCN |
| Execution genesis allocation | 119,940,000 MCN |
| Genesis stake allocation | 60,000 MCN |
| Genesis gas limit | 30,000,000 |
| Genesis base fee | 1 Gwei |
| Genesis fork | Prague / Electra |
| First fork transition | Osaka / Fulu, epoch 1 |

## Files

- `network/contracts/`: deposit contract, compiled artifact and system allocations.
- `network/consensus/config.yaml`: consensus configuration.
- `network/genesis/`: execution and consensus genesis.
- `network/tools/`: genesis preparation and validation.
- `network/scripts/02-genesis.sh`: genesis generation.
- `SHA256SUMS`: file checksums.

Contract sources and compiler settings are listed in
[PROVENANCE.md](network/contracts/PROVENANCE.md).
Audit coverage and outstanding requirements are listed in [AUDIT-SCOPE.md](AUDIT-SCOPE.md).

## Genesis generation

Requires Python dependencies from `network/requirements.txt`,
`network/.venv/bin/python` and `network/bin/prysmctl`.
Run `network/scripts/02-genesis.sh` with `TREASURY` and `GENESIS_TIME` set.

The generator creates new validator keys and deposit data. It does not reproduce
the committed genesis without the original deposit inputs.
`verify-genesis.py` checks generated JSON state and deposit data; it does not
decode the committed SSZ state.
