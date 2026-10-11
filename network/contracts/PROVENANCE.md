Sources pinned for this bundle:
- Deposit contract: OffchainLabs/prysm tag v7.2.0, contracts/deposit/deposit_contract.sol.
- Change: `msg.value >= 1 ether` becomes `msg.value >= 250 ether` for MCN.
- Built with solc 0.6.11, optimizer enabled, 200 runs. Output: deposit-artifact.json.
- System contract runtime bytecode: ethereum/go-ethereum tag v1.17.6, params/protocol_params.go.
- EIP-4788 / EIP-2935 / EIP-7002 / EIP-7251 use upstream bytecode without edits.
- EIP-7002 and EIP-7251 initialize storage slot 0 with the upstream excess inhibitor.
- Deposit zero_hashes storage is initialized exactly as its constructor does (array starts at slot 33).

Upstream files:
https://github.com/OffchainLabs/prysm/blob/v7.2.0/contracts/deposit/deposit_contract.sol
https://github.com/ethereum/go-ethereum/blob/v1.17.6/params/protocol_params.go

Rebuild deposit-artifact.json with Node.js and solc@0.6.11; feed deposit_contract.sol
through solc's standard JSON interface with abi, evm.bytecode.object,
evm.deployedBytecode.object and storageLayout selected.
