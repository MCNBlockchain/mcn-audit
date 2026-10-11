#!/usr/bin/env python3
import base64,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=json.loads((root/'consensus/genesis-state.json').read_text())
g=json.loads((root/'execution/genesis.json').read_text())
d=json.loads((root/'consensus/deposit_data.json').read_text())
def integer(v):return int(v,16) if isinstance(v,str) and v.startswith('0x') else int(v)
assert len(s['validators'])==6 and len(d)==6
assert s['balances']==[10_000*10**9]*6
for v,e in zip(s['validators'],d):
 assert base64.b64decode(v['public_key']).hex()==e['pubkey']
 assert base64.b64decode(v['withdrawal_credentials']).hex()==e['withdrawal_credentials']
 assert v.get('activation_epoch',0)==0 and v['effective_balance']==10_000*10**9
assert base64.b64decode(s['fork']['current_version']).hex()=='23250005'
assert g['config']['chainId']==2325
assert integer(g['timestamp'])==s['genesis_time']
for fork in ['shanghai','cancun','prague']:assert g['config'][fork+'Time']==s['genesis_time']
assert g['config']['osakaTime']==s['genesis_time']+384
assert not g['config'].get('amsterdamTime')
assert integer(g['baseFeePerGas'])==10**9
assert integer(g['gasLimit'])==30000000
execution=sum(integer(v.get('balance',0)) for v in g['alloc'].values())
assert execution+sum(s['balances'])*10**9==120_000_000*10**18
assert (root/'consensus/genesis.ssz').stat().st_size>0
print('Verified: 6 matching active validators, Electra genesis / Fulu epoch 1, fork times, 1 Gwei and total initial supply 120M MCN.')
