#!/usr/bin/env python3
import json,sys
from pathlib import Path
from urllib.parse import urlsplit
peer=sys.argv[1]
u=urlsplit(peer)
if u.scheme!='enode' or not u.username or len(u.username)!=128 or not u.hostname or not u.port:
 raise SystemExit('Expected enode://128_HEX_PUBLIC_KEY@SERVER_IP:30303')
int(u.username,16)
p=Path(__file__).resolve().parents[1]/'execution/peers.toml'
p.write_text('[Node.P2P]\nStaticNodes = ['+json.dumps(peer)+']\n')
print('Saved persistent peer:',p)
