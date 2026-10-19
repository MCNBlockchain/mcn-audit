# Deposit contract provenance

Address: `0x00000000219ab540356cBB839Cbe05303d7705Fa`.

Source baseline: Prysm v7.2.0 `contracts/deposit/deposit_contract.sol`. MCN changes one condition from `msg.value >= 1 ether` to `msg.value >= 250 ether`; see `contracts/deposit-change.patch`. Solidity `ether` is an 18-decimal amount literal; in this execution network it denotes the same base-unit multiplier for MCN.

The contract is **preallocated in genesis**, with initialized nonce and storage. A normal deployment transaction is not expected. Source verification in an explorer and a successful deposit receipt are not independent audits.

## Reproduction

```sh
cd contracts
npm ci
npm run verify
```

`standard-input.json` pins source filename `deposit_contract.sol`, optimizer 200 runs and compiler settings. `rebuild.cjs` requires exact compiler version 0.6.11+commit.5ef660b1 and compares creation bytecode, deployed bytecode, ABI and storage layout with `deposit-artifact.json`. Metadata includes the source key, so changing its path changes bytecode even when executable behavior is similar. `MCN_SOLC_MODULE` optionally points to an already installed solc module; the recorded local run used that override instead of downloading packages.

`tools/verify_snapshot.py` compares deployed bytecode against the genesis allocation and checks constructor-equivalent zero-hash storage, nonce and zero deposit count. The EVM tests instantiate the committed allocation directly and exercise actual calls/logs. These tests do not start Prysm or prove successful activation.

## Boundaries that require careful review

- A 250 MCN deposit can be accepted without activating a validator. Activation uses consensus rules and threshold 10,000 MCN.
- Deposits above 100,000 MCN are accepted by the contract. The configured consensus effective cap is not a maximum deposit condition.
- Deposits are denominated in gwei, integral multiples of 10⁹ execution wei. Their uint64 limit is inherited from upstream.
- The deposit contract checks lengths and the SSZ deposit-data root, but **does not validate BLS proof of possession**. That is a consensus responsibility. One test deliberately demonstrates invalid-proof acceptance by the contract; the required CL negative test must prove no validator activation.
- Deposited funds are not withdrawn through a Solidity `withdraw()` method. Review execution-triggered requests, consensus processing and execution payload withdrawals, including authorization and replay/reorg handling.

Other genesis system contract runtime bytecodes are compared to Geth v1.17.6 constants: beacon roots, historical block hashes, withdrawal queue and consolidation queue. Queue sentinel storage is checked locally. This comparison does not by itself test their operation across forks.
