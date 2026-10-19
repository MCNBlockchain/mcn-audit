#!/usr/bin/env python3
"""Read-only public network evidence. Never reads wallets, JWTs, passwords or environments."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request

EXPECTED_GENESIS='0x6743b8ab3013af80fe35004034ccd91712d3e6d95699d60742d9fb80f76eb224'
EXPECTED_REGISTRY='0x84f925eff5a85c006900c4be36bedc53b3ec8ec733606a3301c76f7f1e737cf0'
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--label',required=True,choices=['A','B','C','D','E','scan','rpc'])
p.add_argument('--root',type=Path,default=Path.home()/'mcn-launch')
p.add_argument('--beacon-url',default='http://127.0.0.1:3500')
p.add_argument('--out',type=Path,required=True,help='New directory outside this repository, review before sharing')
a=p.parse_args()
a.root=a.root.expanduser().resolve()
a.out=a.out.expanduser().resolve()
repo=Path(__file__).resolve().parents[1]
if a.out==repo or repo in a.out.parents:p.error('Collect outside the audit repository; review before importing.')
a.out.mkdir(parents=True,exist_ok=False)
errors={}
def save(name,value):
 (a.out/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n')
def command(argv):
 r=subprocess.run(argv,capture_output=True,text=True,timeout=60)
 if r.returncode:raise RuntimeError(r.stderr[-2000:])
 return r.stdout.strip()
def get(path):
 with urllib.request.urlopen(a.beacon_url.rstrip('/')+path,timeout=30) as r:return json.load(r)
def attempt(name,fn):
 try:
  value=fn();save(name,value);return value
 except Exception as e:errors[name]=str(e);return None
start=dt.datetime.now(dt.timezone.utc).isoformat()
endpoints={
 'cl-version':'/eth/v1/node/version','cl-genesis':'/eth/v1/beacon/genesis',
 'cl-spec':'/eth/v1/config/spec','cl-fork-schedule':'/eth/v1/config/fork_schedule',
 'cl-syncing':'/eth/v1/node/syncing','cl-peer-count':'/eth/v1/node/peer_count',
 'cl-head':'/eth/v1/beacon/headers/head','cl-finality':'/eth/v1/beacon/states/head/finality_checkpoints',
 'cl-validators':'/eth/v1/beacon/states/head/validators',
 'cl-pending-partials':'/eth/v1/beacon/states/head/pending_partial_withdrawals'}
results={name:attempt(name,lambda path=path:get(path)) for name,path in endpoints.items()}
finality=results.get('cl-finality')
if finality:
 root=finality['data']['finalized']['root']
 attempt('cl-finalized-header',lambda:get('/eth/v1/beacon/headers/'+root))
# Only public chain state and hashes; no admin.nodeInfo/private-node key material.
script='''JSON.stringify({client:web3.version.node,chainId:eth.chainId(),head:eth.blockNumber,syncing:eth.syncing,peers:admin.peers.length,genesis:eth.getBlock(0).hash,latest:eth.getBlock("latest"),finalized:eth.getBlock("finalized")})'''
def execution():
 value=json.loads(command([str(a.root/'bin/geth'),'attach','--exec',script,str(a.root/'execution/data/geth.ipc')]))
 return json.loads(value) if isinstance(value,str) else value
el=attempt('el-status',execution)
binaries={}
for name in ['geth','beacon-chain','validator','prysmctl']:
 path=a.root/'bin'/name
 if path.is_file():binaries[name]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size}
checks={
 'el_genesis_matches':el.get('genesis')==EXPECTED_GENESIS if el else None,
 'chain_id_matches':el.get('chainId') in (2325,'0x915') if el else None,
 'cl_registry_matches':results['cl-genesis']['data']['genesis_validators_root']==EXPECTED_REGISTRY if results['cl-genesis'] else None}
save('collection',dict(label=a.label,started_utc=start,finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),binaries=binaries,identity_checks=checks,errors=errors,limitations=['Sequential calls are not an atomic snapshot.','Binary hashes are fingerprints, not signed-release verification.','No service configuration, secret storage or signing-history audit performed.']))
manifest={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(a.out.glob('*.json'))}
save('SHA256',manifest)
print(json.dumps({'output':str(a.out),'identity_checks':checks,'errors':errors},indent=2))
raise SystemExit(1 if errors or any(v is not True for v in checks.values()) else 0)
