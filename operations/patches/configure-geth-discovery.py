#!/usr/bin/env python3
"""Configure existing static execution peers as discovery v4 bootnodes. No restart."""
import datetime,json,re,subprocess,sys,tempfile,tomllib
from pathlib import Path
root=Path(sys.argv[1]).expanduser().resolve() if len(sys.argv)>1 else Path.cwd()
peers=root/'execution/peers.toml'
nodes=tomllib.loads(peers.read_text())['Node']['P2P']['StaticNodes']
if not nodes or not all(re.fullmatch(r'enode://[0-9a-fA-F]{128}@[0-9.]+:30303',n) for n in nodes):
    raise SystemExit('Invalid or empty StaticNodes; no changes made.')
script=root/'scripts/run-geth.sh'
if not script.exists():script=root/'run-geth.sh'
s=script.read_text()
if re.search(r'--nodiscover(?:\s|=|$)',s):raise SystemExit('--nodiscover found; no changes made.')
replacement='--discovery.v4=true --bootnodes='+','.join(dict.fromkeys(nodes))
marker='--discovery.v4=true --bootnodes='
if marker in s:
    updated=re.sub(r'--discovery\.v4=true --bootnodes=\S+',lambda _:replacement,s,count=1)
else:
    updated,n=re.subn(r'--bootnodes=(?=\s|$)',lambda _:replacement,s)
    if n!=1:raise SystemExit('Expected exactly one empty --bootnodes=; no changes made.')
if updated==s:print('Already configured:',script);sys.exit(0)
with tempfile.NamedTemporaryFile(mode='w',suffix='.sh') as f:
    f.write(updated);f.flush();subprocess.run(['bash','-n',f.name],check=True)
backup=script.with_name(script.name+'.before-discovery-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
backup.write_bytes(script.read_bytes());backup.chmod(script.stat().st_mode & 0o777)
script.write_text(updated)
print('Updated:',script)
print('Backup:',backup)
print('Bootnodes:',len(set(nodes)))
print('Restart only the Geth service on this server to apply. Do not restart all validators together.')
