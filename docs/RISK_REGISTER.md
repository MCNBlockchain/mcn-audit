# Open audit questions and risks

These are preparation observations, not independent auditor severity ratings. No item is closed merely because an explorer renders or a process reports `active`.

| ID | Priority | Observation / status | Evidence required to close |
|---|---|---|---|
| MCN-01 | High | Five validators share an operator and withdrawal destination | Custody/backup design, honest independence claims, concentration and correlated-failure analysis |
| MCN-02 | High | Genesis effective balances are 10k, balances 100k; Electra cap 100k | Epoch-transition trace, actual effective balances, justified economic model |
| MCN-03 | High | Current-network activation and requested partial/full withdrawal test evidence incomplete | End-to-end tests with tx hash, consensus processing, payout and finality, negative cases |
| MCN-04 | High | Live binaries, service settings, key/slashing backups not independently attested | Reviewed release fingerprints/build provenance and per-host configuration/custody review |
| MCN-05 | Medium | 10s slots and 60M genesis gas target lack load/failure evidence | Geographic latency, full blocks, CPU/memory/disk, missed duties and finality benchmark |
| MCN-06 | Medium | Discovery added after original templates; current network configuration not captured | Peer/discovery/firewall/identity review on seven hosts; restart/partition recovery tests |
| MCN-07 | Medium | Archive and explorer colocated on limited host resources | Historical state/trace and backup tests, capacity plan and disk alerts |
| MCN-08 | Medium | Public RPC/Engine/debug isolation is intended, not independently checked | Exposure/method limits audit, authenticated Engine boundary, safe negative requests |
| MCN-09 | Medium | Explorer market display uses BNB token data | Clear attribution, asset-equivalence assumptions and freshness/failure handling |
| MCN-10 | Pending | Initial supply verified; lifetime economics/APR not reviewed | Issuance/burn/penalty model with actual inherited defaults, effective stake and participation |

Before treating the network as ready to hold public funds: resolve correctness/economic questions, collect runtime evidence, complete the integration matrix and obtain independent review. Auditors can start reviewing this repository now; receiving a package does not require all findings already be resolved.

A per-validator cap cannot cap an owner's total voting power: one operator can use multiple keys. Offline penalties and slashings are distinct. No slashing is inferred from a noncanonical block signed by a different proposer; the relevant signing/attestation offenses need their own evidence. Never create double-signing tests with live validator keys.
