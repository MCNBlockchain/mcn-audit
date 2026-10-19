#!/usr/bin/env python3
"""Integrity manifest; not a signature or proof of live deployment."""
import argparse,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EXCLUDED={'.git','node_modules','__pycache__','.venv','.local-evidence'}
def files():
 return sorted(p for p in ROOT.rglob('*') if p.is_file() and not any(x in EXCLUDED for x in p.relative_to(ROOT).parts) and p.name!='SHA256SUMS')
p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args()
actual=''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.relative_to(ROOT).as_posix()+'\n' for f in files())
if a.write:(ROOT/'SHA256SUMS').write_text(actual);print('Wrote SHA256SUMS')
else:
 if (ROOT/'SHA256SUMS').read_text()!=actual:raise SystemExit('FAIL: missing, added or changed file; compare to committed SHA256SUMS')
 print('PASS: all snapshot files match SHA256SUMS')
