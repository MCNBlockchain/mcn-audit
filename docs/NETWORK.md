# Network snapshot

These values come from committed genesis/configuration files and the local checker. Current runtime configuration still needs comparison.

| Property | Snapshot |
|---|---|
| Chain/network ID | 2325 (chain ID verified in genesis; running network ID pending) |
| Native unit | MCN, 18 decimals; consensus amounts use gwei (10⁻⁹ MCN) |
| Genesis UTC | 2026-10-17 06:34:01; Unix 1792218841 |
| Execution genesis hash | `0x6743b8ab3013af80fe35004034ccd91712d3e6d95699d60742d9fb80f76eb224` |
| Genesis validators root | `0x84f925eff5a85c006900c4be36bedc53b3ec8ec733606a3301c76f7f1e737cf0` |
| Slot / epoch | 10 seconds / 32 slots = 320 seconds |
| Genesis gas limit | 60,000,000 (not an immutable future block limit) |
| Genesis base fee | 1 gwei |
| Contract minimum deposit | 250 MCN |
| Activation threshold | 10,000 MCN |
| Effective-balance increment | 250 MCN |
| Legacy / Electra effective cap | 10,000 / 100,000 MCN |
| Ejection balance | 8,000 MCN |
| Genesis validators | 5, activation epoch 0 |
| Actual genesis balance per validator | 100,000 MCN |
| Effective genesis balance per validator | **10,000 MCN** |
| Initial total supply | 120,000,000 MCN |

The effective-balance distinction is present in the supplied SSZ. It is not evidence that current effective balances remain 10,000. Capture epoch transitions and the live state before assessing rewards, concentration or economic safety. Preserve the original genesis for forensic reproducibility.

Initial EL balances sum to **119,500,000 MCN**, plus **500,000 MCN** in CL genesis balances. The initial supply is not a lifetime supply cap: consensus rewards issue additional MCN, and fee burning/withdrawals must be accounted for appropriately. Withdrawals transfer consensus balances to execution; they are not additional issuance on their own.

All five genesis validators use compounding withdrawal credentials (`0x02`) pointing to `0xfe4800ca5a48670cc5f591a51f517ba8f682d4ae`. Public keys and raw balance units are in `evidence/local/genesis-analysis.json`.

## Fork schedule

EL historical block forks are set to block 0 and terminal total difficulty to 0. Shanghai, Cancun and Prague activate at genesis time. Osaka activates at genesis +320 seconds. CL genesis fork version is `0x23251000`; Altair through Electra epochs are 0; the supplied state's current version is Electra `0x23251005`. Fulu `0x23251006` activates at epoch 1. Gloas is disabled with FAR_FUTURE_EPOCH. `BLOB_SCHEDULE` is `[]`.

Review the entire `config.yaml`, upstream defaults inherited by omitted settings, Fulu/Osaka alignment and blob/data availability behavior. A short YAML file does not enumerate every effective client parameter. Never infer that an empty blob schedule disables all blob handling without testing the specific client configuration.

The 100,000 cap applies to a validator's effective voting/reward balance. It does not prohibit depositing more, does not limit one owner's aggregate stake, and does not enforce one operator per server. Minimum contract deposit also does not mean activation at 250 MCN.
