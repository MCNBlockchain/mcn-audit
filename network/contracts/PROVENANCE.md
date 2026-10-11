# Contract provenance

## Deposit contract

Source: [Prysm v7.2.0](https://github.com/OffchainLabs/prysm/blob/v7.2.0/contracts/deposit/deposit_contract.sol).

MCN change: minimum deposit increased from `1 ether` to `250 ether`.
In this network, `ether` denotes 10^18 native MCN units.

Compiler: `0.6.11+commit.5ef660b1.Emscripten.clang`.
Optimizer: enabled, 200 runs.
Artifact: `deposit-artifact.json`, including ABI, creation bytecode,
runtime bytecode and storage layout.

Compile `deposit_contract.sol` with the Solidity standard JSON interface,
selecting `abi`, `evm.bytecode.object`, `evm.deployedBytecode.object`
and `storageLayout`.

## System contracts

Source: [Geth v1.17.6](https://github.com/ethereum/go-ethereum/blob/v1.17.6/params/protocol_params.go).

EIP-4788, EIP-2935, EIP-7002 and EIP-7251 runtime bytecode is stored in
`system-alloc.json`. EIP-7002 and EIP-7251 initialize storage slot 0 with
the upstream excess inhibitor.

The deposit contract zero-hash array starts at storage slot 33.
Genesis initializes its entries to the values computed by the constructor.

## Licenses

The deposit source declares `CC0-1.0`.
The Prysm repository license is preserved in `UPSTREAM-LICENSE.md`.
