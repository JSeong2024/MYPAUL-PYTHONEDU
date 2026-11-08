#!/usr/bin/env python3
"""Run a single reference solution against the bundled reproducible input."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
SAMPLE={
'B-01':'3 2\n1.5 2.0 0\n2.1 3.0 1\n1.2 2.8 0\n',
'B-02':'2 1\n2\n2 4\n3\n1 3\n2 6\n3 7\n',
'B-03':'2 5 1 0 0.1\n',
'B-04':'5 0.5\n0 0.10\n1 0.80\n1 0.40\n0 0.60\n1 0.90\n',
'B-05':'0 0\n6 0\n3\n1 0\n5 0\n3 0\n'}
IDS=[f'{letter}-{i:02d}' for letter,count in [('B',5),('A',4),('P',3),('C',2),('R',1)] for i in range(1,count+1)]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('problem_id',choices=IDS)
    parser.add_argument('--starter',action='store_true',help='Run exercises instead of solutions')
    args=parser.parse_args()
    pid=args.problem_id
    work=ROOT/'outputs'/pid;work.mkdir(parents=True,exist_ok=True)
    fixtures=ROOT/'data'/pid
    if fixtures.is_dir():
        for fixture in fixtures.iterdir():
            # Refresh fixtures, but leave old result files in place to exercise rollback.
            shutil.copy2(fixture,work/fixture.name)
    script=ROOT/('exercises' if args.starter else 'solutions')/f'{pid}.py'
    result=subprocess.run([sys.executable,str(script)],cwd=work,input=SAMPLE.get(pid,''),text=True)
    print(f'Working directory: {work.relative_to(ROOT)}')
    raise SystemExit(result.returncode)


if __name__=='__main__':main()
