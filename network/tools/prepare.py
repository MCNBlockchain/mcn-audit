#!/usr/bin/env python3
"""Prepare random EIP-2335 keys, deposit data and execution genesis input."""
import argparse, hashlib, json, os, secrets, time, uuid
from pathlib import Path
from py_ecc.bls import G2ProofOfPossession as BLS
from py_ecc.optimized_bls12_381 import curve_order
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

ZERO = bytes(32)
VERSION = bytes.fromhex('23250000')
DEPOSIT = '0x00000000219ab540356cBB839Cbe05303d7705Fa'
def sha(x): return hashlib.sha256(x).digest()
def hex32(n): return '0x' + n.to_bytes(32, 'big').hex()
def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as f: json.dump(value, f, indent=2)
def pub_root(pk): return sha(pk[:32] + pk[32:].ljust(32, b'\0'))
def deposit(sk, address):
    pk = BLS.SkToPk(sk)
    creds = bytes.fromhex('02' + '00' * 11 + address[2:])
    amount = 10_000 * 10**9
    ar = amount.to_bytes(8, 'little') + bytes(24)
    domain = bytes.fromhex('03000000') + sha(VERSION + bytes(28) + ZERO)[:28]
    mr = sha(sha(pub_root(pk) + creds) + sha(ar + ZERO))
    sig = BLS.Sign(sk, sha(mr + domain))
    assert BLS.Verify(pk, sha(mr + domain), sig)
    sr = sha(sha(sig[:32] + sig[32:64]) + sha(sig[64:] + ZERO))
    dr = sha(sha(pub_root(pk) + creds) + sha(ar + sr))
    return dict(pubkey=pk.hex(), withdrawal_credentials=creds.hex(), amount=amount,
                signature=sig.hex(), deposit_message_root=mr.hex(), deposit_data_root=dr.hex(),
                fork_version=VERSION.hex(), network_name='mcn-2325')
def encrypt(sk, pk, password):
    salt, iv = secrets.token_bytes(32), secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 262144, 32)
    enc = Cipher(algorithms.AES(dk[:16]), modes.CTR(iv)).encryptor()
    ciphertext = enc.update(sk.to_bytes(32, 'big')) + enc.finalize()
    return {'crypto': {
        'kdf': {'function':'pbkdf2','params':{'dklen':32,'c':262144,'prf':'hmac-sha256','salt':salt.hex()},'message':''},
        'checksum': {'function':'sha256','params':{},'message':sha(dk[16:] + ciphertext).hex()},
        'cipher': {'function':'aes-128-ctr','params':{'iv':iv.hex()},'message':ciphertext.hex()}},
        'description':'MCN genesis validator', 'pubkey':pk, 'path':'', 'uuid':str(uuid.uuid4()),'version':4}
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--treasury', required=True)
    ap.add_argument('--genesis-time', type=int, default=int(time.time())+3600)
    a = ap.parse_args(); root = a.root.resolve(); os.umask(0o077)
    treasury = a.treasury.lower()
    if len(treasury)!=42 or not treasury.startswith('0x'): raise SystemExit('Invalid treasury')
    bytes.fromhex(treasury[2:])
    if int(treasury[2:],16)==0: raise SystemExit('Treasury cannot be zero')
    if (root/'validators').exists() or (root/'execution/genesis.json').exists():
        raise SystemExit('Existing validator/genesis files; refusing regeneration')
    passwords={}
    for role in ['A','B']:
        secret = root/'validators'/('node-'+role)/'password.txt'
        secret.parent.mkdir(parents=True,exist_ok=True)
        passwords[role]=secrets.token_hex(32); secret.write_text(passwords[role]+'\n'); secret.chmod(0o600)
    entries=[]
    for i in range(6):
        role='A' if i<3 else 'B'; sk=secrets.randbelow(curve_order-1)+1
        d=deposit(sk,treasury); entries.append(d)
        write_json(root/'validators'/('node-'+role)/'keystores'/f'keystore-{i}.json',encrypt(sk,d['pubkey'],passwords[role]))
    write_json(root/'consensus/deposit_data.json',entries)
    alloc=json.loads((root/'contracts/system-alloc.json').read_text())
    artifact=json.loads((root/'contracts/deposit-artifact.json').read_text())
    storage={}; z=ZERO
    for height in range(1,32):
        z=sha(z+z);storage[hex32(33+height)]='0x'+z.hex()
    alloc[DEPOSIT]={'balance':'0x0','nonce':'0x1','code':'0x'+artifact['evm']['deployedBytecode']['object'],'storage':storage}
    alloc[treasury]={'balance':hex(119_940_000 * 10**18)}
    config={'chainId':2325}
    for f in ['homestead','eip150','eip155','eip158','byzantium','constantinople','petersburg','istanbul','muirGlacier','berlin','london','arrowGlacier','grayGlacier','mergeNetsplit']:
        config[f+'Block']=0
    config['terminalTotalDifficulty']=0
    config['depositContractAddress']=DEPOSIT
    for f in ['shanghai','cancun','prague']:config[f+'Time']=a.genesis_time
    config['osakaTime']=a.genesis_time+384
    config['blobSchedule']={'cancun':{'target':3,'max':6,'baseFeeUpdateFraction':3338477},'prague':{'target':6,'max':9,'baseFeeUpdateFraction':5007716}}
    gen={'config':config,'nonce':'0x0','timestamp':hex(a.genesis_time),'extraData':'0x',
         'gasLimit':hex(30_000_000),'difficulty':'0x0','mixHash':'0x'+'00'*32,
         'coinbase':'0x'+'00'*20,'baseFeePerGas':hex(10**9),'alloc':alloc}
    write_json(root/'execution/genesis-input.json',gen)
    write_json(root/'consensus/launch.json',{'genesis_time':a.genesis_time,'chain_id':2325,'treasury':treasury,
       'execution_supply_mcn':119940000,'consensus_stake_mcn':60000,'total_initial_supply_mcn':120000000,
       'validators':[dict(index=i,role='A' if i<3 else 'B',pubkey=d['pubkey']) for i,d in enumerate(entries)]})
    print('Prepared 6 random encrypted keys; 119,940,000 liquid + 60,000 staked MCN.')
    print('Genesis UTC:',time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(a.genesis_time)))
if __name__=='__main__': main()
