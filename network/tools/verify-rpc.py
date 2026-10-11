#!/usr/bin/env python3
import base64,json,urllib.request
from pathlib import Path
root=Path(__file__).resolve().parents[1]
s=json.loads((root/'consensus/genesis-state.json').read_text())
def rpc(method,params):
 req=urllib.request.Request('http://127.0.0.1:8545',data=json.dumps({'jsonrpc':'2.0','id':1,'method':method,'params':params}).encode(),headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=15) as r:obj=json.load(r)
 if 'error' in obj:raise SystemExit(obj['error'])
 return obj['result']
assert rpc('eth_chainId',[])=='0x915'
gen=rpc('eth_getBlockByNumber',['0x0',False])
h=s['latest_execution_payload_header_deneb']
assert gen['hash']=='0x'+base64.b64decode(h['block_hash']).hex(), 'EL genesis hash differs from CL genesis header'
assert gen['stateRoot']=='0x'+base64.b64decode(h['state_root']).hex()
print('Verified: chain 2325; EL genesis block hash/state root match the CL genesis payload header.')
