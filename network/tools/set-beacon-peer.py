#!/usr/bin/env python3
import re,sys
from pathlib import Path
if len(sys.argv)!=2 or not re.fullmatch(r'/ip4/[0-9.]+/tcp/[0-9]+/p2p/[A-Za-z0-9]+',sys.argv[1]):
    raise SystemExit('Usage: python3 tools/set-beacon-peer.py /ip4/IP/tcp/PORT/p2p/PEER_ID')
p=Path(__file__).resolve().parents[1]/'node.env'
text=p.read_text()
lines=[line for line in text.splitlines() if not re.match(r'^\s*(BEACON_BOOTNODE|BEACON_PEER)\s*=',line)]
lines += ["BEACON_BOOTNODE=''", "BEACON_PEER='"+sys.argv[1]+"'"]
p.write_text('\n'.join(lines)+'\n')
print('Saved TCP beacon peer:',sys.argv[1])
