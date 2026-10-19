#!/usr/bin/env python3
"""Export existing Aseprite source into a fresh directory, preserving the source."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path);p.add_argument('output',type=Path)
    p.add_argument('--executable',type=Path,default=Path.home()/'.local/share/Steam/steamapps/common/Aseprite/aseprite')
    args=p.parse_args();source=args.source.resolve();out=args.output.resolve()
    if not source.is_file() or source.suffix.lower() not in ('.ase','.aseprite'):
        raise ValueError('Choose an existing .ase or .aseprite file')
    before=hashlib.sha256(source.read_bytes()).hexdigest()
    out.mkdir(exist_ok=False)
    subprocess.run([str(args.executable),'--batch',str(source),'--sheet',str(out/'sheet.png'),
        '--data',str(out/'sheet.json'),'--format','json-array','--sheet-type','rows'],check=True,timeout=60)
    assert before==hashlib.sha256(source.read_bytes()).hexdigest(),'Source changed unexpectedly'
    with (out/'provenance.json').open('x') as f:
        json.dump({'source':str(source),'source_sha256':before,'source_unchanged':True,
            'aseprite':str(args.executable),'rights':'Retain the source artwork license/provenance separately'},f,indent=2)
    print(json.dumps({'output':str(out),'source_unchanged':True}))

if __name__=='__main__':main()
