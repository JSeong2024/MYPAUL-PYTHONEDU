"""Run all reference projects with their bundled datasets."""
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
projects=sorted(p for p in (ROOT/'projects').iterdir() if p.is_dir())
failed=[]
for project in projects:
    script=ROOT/'solutions'/project.name/'reference_solution.py'
    result=subprocess.run([sys.executable,str(script)],cwd=ROOT)
    if result.returncode:
        failed.append(project.name)
print(f'{"FAIL" if failed else "PASS"}: {len(projects)-len(failed)}/{len(projects)} projects')
if failed:print('Failed:',', '.join(failed))
raise SystemExit(int(bool(failed)))
