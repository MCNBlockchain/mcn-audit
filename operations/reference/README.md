# Historical launch reference only

These three scripts were copied from the original five-validator launch package. They are not the current service configurations or a standalone installer. They reference files deliberately omitted here (wallets, JWT, node.env, directories).

The original Geth script has empty bootnodes. The later discovery patch is recorded under ../patches/. No patch or restart has been applied to servers during this audit preparation.

Use these scripts for change-history review, not as an instruction to replace a live node. In particular, do not regenerate signing keys/genesis, discard slashing protection or delete data. Collect sanitized current scripts and service units to establish the actual deployed revision.
