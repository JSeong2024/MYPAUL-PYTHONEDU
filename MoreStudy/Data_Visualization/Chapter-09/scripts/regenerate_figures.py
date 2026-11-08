"""Recreate the figures linked from each project README."""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
folder=ROOT/'figures'/'projects'
folder.mkdir(parents=True,exist_ok=True)
for project in sorted(p for p in (ROOT/'projects').iterdir() if p.is_dir()):
    pid=project.name
    script=ROOT/'solutions'/pid/'reference_solution.py'
    output=ROOT/'output'/pid
    result=subprocess.run([sys.executable,str(script),'--output',str(output)],cwd=ROOT)
    if result.returncode:raise SystemExit(f'FAIL: {pid}')
    images=list(output.glob('*.png'))
    if len(images)!=1:raise SystemExit(f'FAIL: expected one PNG for {pid}, found {len(images)}')
    shutil.copy2(images[0],folder/(pid+'.png'))
print('PASS: figures for all 10 projects regenerated')
