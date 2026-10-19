// Rebuild without changing the SSZ/genesis or any saved artifact.
const fs = require('node:fs');
const path = require('node:path');
const solc = process.env.MCN_SOLC_MODULE ? require(path.resolve(process.env.MCN_SOLC_MODULE)) : require('solc');
const base=__dirname;
const input=JSON.parse(fs.readFileSync(path.join(base,'standard-input.json')));
const source=fs.readFileSync(path.join(base,'deposit_contract.sol'),'utf8');
if(input.sources['deposit_contract.sol'].content!==source) throw Error('Compiler input source differs');
const artifact=JSON.parse(fs.readFileSync(path.join(base,'deposit-artifact.json')));
if(solc.version()!==artifact.compiler) throw Error('Wrong compiler: '+solc.version());
const output=JSON.parse(solc.compile(JSON.stringify(input)));
const errors=(output.errors||[]).filter(x=>x.severity==='error');
if(errors.length) throw Error(JSON.stringify(errors));
const built=output.contracts['deposit_contract.sol'].DepositContract;
for(const key of ['bytecode','deployedBytecode']) {
 if(built.evm[key].object!==artifact.evm[key].object) throw Error(key+' mismatch');
}
if(JSON.stringify(built.abi)!==JSON.stringify(artifact.abi)) throw Error('ABI mismatch');
if(JSON.stringify(built.storageLayout)!==JSON.stringify(artifact.storageLayout)) throw Error('Storage layout mismatch');
console.log('PASS: solc '+solc.version()+' reproduces creation/runtime bytecode, ABI and storage layout.');
