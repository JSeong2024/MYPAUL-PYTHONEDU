"""Run a reference solution with a clean output directory."""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
IDS = [f'{prefix}-{i:02d}' for prefix,count in [('B',5),('A',4),('P',3),('C',2),('R',1)] for i in range(1,count+1)]

def main():
    parser=argparse.ArgumentParser(description='Run a Part 02 model solution')
    parser.add_argument('problem_id',choices=IDS)
    parser.add_argument('--data',type=Path,default=ROOT/'data')
    parser.add_argument('--out',type=Path,default=None)
    parser.add_argument('--mode',default='run')
    args=parser.parse_args()
    if args.problem_id.startswith('B-'):
        print(f'{args.problem_id}: 표준 입력을 전달하세요. 예: echo "5 3 4 2" | python tests/run_solution.py B-04',file=sys.stderr)
        result=subprocess.run([sys.executable,str(ROOT/'solutions'/f'{args.problem_id}.py')],stdin=sys.stdin)
    else:
        output=args.out or (ROOT/'outputs'/args.problem_id)
        result=subprocess.run([sys.executable,str(ROOT/'solutions'/f'{args.problem_id}.py'),'--data',str(args.data),'--out',str(output),'--mode',args.mode])
    sys.exit(result.returncode)

if __name__=='__main__':main()
