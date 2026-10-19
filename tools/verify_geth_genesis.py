#!/usr/bin/env python3
"""Initialize/export only a disposable temporary database; never starts network services."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
import rlp
from eth_utils import keccak
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--geth',required=True,type=Path);a=p.parse_args()
geth=a.geth.expanduser().resolve()
with tempfile.TemporaryDirectory(prefix='mcn-audit-genesis-') as td:
 directory=Path(td)
 for args in [['--datadir',str(directory/'data'),'init',str(ROOT/'network/genesis.json')],['--datadir',str(directory/'data'),'export',str(directory/'block.rlp'),'0','0']]:
  result=subprocess.run([str(geth)]+args,capture_output=True,text=True,timeout=120)
  if result.returncode:raise SystemExit(result.stderr)
 block=rlp.decode((directory/'block.rlp').read_bytes())
 digest='0x'+keccak(rlp.encode(block[0])).hex()
 assert digest=='0x6743b8ab3013af80fe35004034ccd91712d3e6d95699d60742d9fb80f76eb224',digest
 print(json.dumps({'status':'PASS','execution_genesis_hash':digest,'method':'Fresh temporary Geth init/export; Keccak256(RLP(header))'},indent=2))
