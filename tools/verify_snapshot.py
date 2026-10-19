#!/usr/bin/env python3
"""Offline checks for this exact Electra/mainnet-preset genesis, not a general SSZ decoder."""
from pathlib import Path
import argparse,hashlib,json,re,struct
ROOT=Path(__file__).resolve().parents[1]
ZERO=bytes(32)
def sha(v):return hashlib.sha256(v).digest()
def integer(v):return int(v,0) if isinstance(v,str) else int(v)
def merkle(chunks):
 chunks=list(chunks);n=1
 while n<len(chunks):n*=2
 chunks+= [ZERO]*(n-len(chunks))
 while len(chunks)>1:chunks=[sha(chunks[i]+chunks[i+1]) for i in range(0,len(chunks),2)]
 return chunks[0]
def read_snapshot(root=ROOT):
 s=(root/'network/genesis.ssz').read_bytes()
 assert len(s)>=2736713,'Not an Electra mainnet-preset state'
 u32=lambda p:struct.unpack_from('<I',s,p)[0]
 va,ba,pa=u32(524552),u32(524556),u32(2687248)
 assert 2736713<=va<=ba<=pa<=len(s)
 assert (ba-va)%121==0 and pa-ba==((ba-va)//121)*8
 validators=[];roots=[]
 for i in range((ba-va)//121):
  v=s[va+i*121:va+(i+1)*121];assert v[88] in (0,1)
  pubkey=v[:48];creds=v[48:80];effective=struct.unpack_from('<Q',v,80)[0]
  epochs=struct.unpack_from('<QQQQ',v,89)
  chunks=[sha(pubkey[:32]+pubkey[32:]+bytes(16)),creds,v[80:88]+bytes(24),bytes([v[88]])+bytes(31)]+[n.to_bytes(8,'little')+bytes(24) for n in epochs]
  roots.append(merkle(chunks))
  validators.append(dict(index=i,pubkey='0x'+pubkey.hex(),withdrawal_credentials='0x'+creds.hex(),balance_gwei=struct.unpack_from('<Q',s,ba+i*8)[0],effective_balance_gwei=effective,slashed=bool(v[88]),activation_eligibility_epoch=epochs[0],activation_epoch=epochs[1],exit_epoch=epochs[2],withdrawable_epoch=epochs[3]))
 # Validators is List[Validator, 2**40]. Extend its subtree to depth 40, then mix in length.
 depth=(max(1,len(roots))-1).bit_length();tree=merkle(roots);z=ZERO
 for _ in range(depth):z=sha(z+z)
 for _ in range(depth,40):tree=sha(tree+z);z=sha(z+z)
 registry_root=sha(tree+len(roots).to_bytes(32,'little'))
 assert registry_root==s[8:40],'Genesis validator registry root mismatch'
 header=u32(2736629)
 return dict(genesis_time=struct.unpack_from('<Q',s)[0],genesis_validators_root='0x'+s[8:40].hex(),slot=struct.unpack_from('<Q',s,40)[0],current_fork_version='0x'+s[52:56].hex(),execution_genesis_hash='0x'+s[header+472:header+504].hex(),validators=validators)
def verify(root=ROOT):
 snap=read_snapshot(root);g=json.loads((root/'network/genesis.json').read_text());a={k.lower().removeprefix('0x'):v for k,v in g['alloc'].items()}
 config={}
 for line in (root/'network/config.yaml').read_text().splitlines():
  line=line.split('#',1)[0].strip()
  if line and ':' in line:
   k,v=line.split(':',1);config[k]=v.strip().strip('"')
 assert snap['genesis_time']==integer(g['timestamp'])==1792218841
 assert snap['slot']==0 and snap['current_fork_version']=='0x23251005'
 assert snap['genesis_validators_root']=='0x84f925eff5a85c006900c4be36bedc53b3ec8ec733606a3301c76f7f1e737cf0'
 assert snap['execution_genesis_hash']=='0x6743b8ab3013af80fe35004034ccd91712d3e6d95699d60742d9fb80f76eb224'
 assert g['config']['chainId']==2325 and integer(g['gasLimit'])==60000000
 for k in ['shanghaiTime','cancunTime','pragueTime']:assert g['config'][k]==snap['genesis_time']
 assert g['config']['osakaTime']==snap['genesis_time']+320
 for k,v in {'SECONDS_PER_SLOT':10,'SLOT_DURATION_MS':10000,'SLOTS_PER_EPOCH':32,'MIN_ACTIVATION_BALANCE':10000*10**9,'MAX_EFFECTIVE_BALANCE':10000*10**9,'MAX_EFFECTIVE_BALANCE_ELECTRA':100000*10**9,'MIN_DEPOSIT_AMOUNT':250*10**9,'EFFECTIVE_BALANCE_INCREMENT':250*10**9,'EJECTION_BALANCE':8000*10**9,'FULU_FORK_EPOCH':1,'GLOAS_FORK_EPOCH':2**64-1}.items():assert integer(config[k])==v,k
 assert config['BLOB_SCHEDULE']=='[]'
 assert len(snap['validators'])==5
 for v in snap['validators']:
  assert v['balance_gwei']==100000*10**9 and v['effective_balance_gwei']==10000*10**9
  assert not v['slashed'] and v['activation_epoch']==v['activation_eligibility_epoch']==0
  assert v['exit_epoch']==v['withdrawable_epoch']==2**64-1
  assert v['withdrawal_credentials']=='0x02'+'00'*11+'fe4800ca5a48670cc5f591a51f517ba8f682d4ae'
 liquid=sum(integer(v.get('balance',0)) for v in a.values())
 assert liquid==119500000*10**18
 assert liquid+sum(v['balance_gwei'] for v in snap['validators'])*10**9==120000000*10**18
 artifact=json.loads((root/'contracts/deposit-artifact.json').read_text());dep=a['00000000219ab540356cbb839cbe05303d7705fa']
 assert dep['code'].removeprefix('0x')==artifact['evm']['deployedBytecode']['object']
 assert integer(dep['nonce'])==1
 storage={integer(k):integer(v) for k,v in dep.get('storage',{}).items()};z=ZERO
 for height in range(32):
  assert storage.get(33+height,0)==int.from_bytes(z,'big'),f'zero_hashes[{height}]'
  z=sha(z+z)
 assert all(v==0 for k,v in storage.items() if not 33<=k<=64)
 upstream=(root/'contracts/upstream/deposit_contract.sol').read_text();local=(root/'contracts/deposit_contract.sol').read_text()
 assert upstream.replace('msg.value >= 1 ether','msg.value >= 250 ether')==local
 params=(root/'upstream/geth-v1.17.6-protocol_params.go').read_text()
 for name,addr in [('BeaconRootsCode','000f3df6d732807ef1319fb7b8bb8522d0beac02'),('HistoryStorageCode','0000f90827f1c53a10cb7a02335b175320002935'),('WithdrawalQueueCode','00000961ef480eb55e80d19ad83579a64c007002'),('ConsolidationQueueCode','0000bbddc7ce488642fb579f8b00f3a590007251')]:
  code=re.search(r'\b'+name+r'\s*=\s*common.FromHex\("(0x[0-9a-fA-F]+|[0-9a-fA-F]+)"\)',params)[1]
  assert a[addr]['code'].removeprefix('0x').lower()==code.removeprefix('0x').lower(),name
 for addr in ['00000961ef480eb55e80d19ad83579a64c007002','0000bbddc7ce488642fb579f8b00f3a590007251']:
  st={integer(k):integer(v) for k,v in a[addr]['storage'].items()};assert st.get(0)==2**256-1
 return snap
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--json',action='store_true');args=p.parse_args();result=verify()
 print(json.dumps(result,indent=2) if args.json else 'PASS: EL/CL genesis snapshot, SSZ validator registry root, 120M initial supply, deposit runtime/storage, upstream system bytecodes and network parameters.')
