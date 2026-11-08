#!/usr/bin/env python3
"""C++20 Chapter 01~11 Summary: test all reference implementations in temporary folders."""
import argparse
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
IDS = [f'{prefix}-{number:02d}' for prefix, count in [('B',6),('A',5),('C',3),('R',1)] for number in range(1,count+1)]

# Each case: (label, stdin, stdout, input files, expected output files)
def c(label, stdin='', stdout='', files=None, output=None):
    return label, stdin, stdout, files or {}, output or {}

CASES = {
 'B-01': [c('sample','1200 1\n','5500\n'),c('base boundary','1000 0\n','3000\n'),c('rounded block','1001 0\n','3500\n'),c('maximum','20000 1\n','24000\n'),c('invalid weight','0 1\n','INVALID\n'),c('invalid mode','999 4\n','INVALID\n')],
 'B-02': [c('sample','09:00 09:31\n','1500\n'),c('exact 30','09:00 09:30\n','1000\n'),c('exact 40','09:00 09:40\n','1500\n'),c('zero duration','09:00 09:00\n','INVALID\n'),c('invalid time','24:00 23:00\n','INVALID\n')],
 'B-03': [c('sample','4\n60 100 80 60\n','MIN 60\nMAX 100\nAVG 75.0\n'),c('single','1\n0\n','MIN 0\nMAX 0\nAVG 0.0\n'),c('mean precision','3\n1 2 2\n','MIN 1\nMAX 2\nAVG 1.7\n'),c('invalid score','3\n10 101 50\n','INVALID\n')],
 'B-04': [c('sample','3\nP01 1200 4\nP02 700 0\nP03 2000 9\nP02\n','P02 700 0\n'),c('not found','1\nP01 1200 1\nP02\n','NOT_FOUND\n'),c('empty list','0\nP01\n','NOT_FOUND\n'),c('case sensitive','1\np01 10 2\nP01\n','NOT_FOUND\n')],
 'B-05': [c('sample','Demo 1\n4\nBORROW\nBORROW\nRETURN\nRETURN\n','OK 0\nFAIL 0\nOK 1\nFAIL 1\n'),c('zero copies','Book 0\n2\nBORROW\nRETURN\n','FAIL 0\nFAIL 0\n'),c('state transitions','Book 2\n5\nBORROW\nBORROW\nBORROW\nRETURN\nRETURN\n','OK 1\nOK 0\nFAIL 0\nOK 1\nOK 2\n')],
 'B-06': [c('sample','events.log\n','INFO 1\nWARN 1\nERROR 1\nINVALID 2\n',{'events.log':'INFO|boot\nWARN|retry\nERROR|disk\nTRACE|unexpected\ninvalid-line\n'}),c('empty','events.log\n','INFO 0\nWARN 0\nERROR 0\nINVALID 0\n',{'events.log':''}),c('open failure','missing.log\n','OPEN_ERROR\n')],
 'A-01': [c('sample','1999 15\n','300\n'),c('zero','2000 0\n','0\n'),c('maximum','1000000000 100\n','1000000000\n'),c('round-half-up','5 10\n','1\n'),c('invalid','100 101\n','INVALID\n')],
 'A-02': [c('sample','10 3\nSELL 4\nSELL 8\nRESTOCK 2\n','OK 6\nFAIL 6\nOK 8\n'),c('invalid quantity','2 4\nSELL 0\nRESTOCK -3\nSELL 2\nSELL 1\n','FAIL 2\nFAIL 2\nOK 0\nFAIL 0\n'),c('restock from zero','0 2\nRESTOCK 2\nSELL 2\n','OK 2\nOK 0\n')],
 'A-03': [c('sample','4\nT1 2\nT2 5\nT3 2\nT4 5\n','T2\nT4\nT1\nT3\n'),c('stable order','3\nT1 10\nT2 10\nT3 10\n','T1\nT2\nT3\n'),c('invalid priority','1\nT1 11\n','INVALID\n')],
 'A-04': [c('sample','5\nC02\nC01\nC02\nC03\nC01\n','C01 2\nC02 2\nC03 1\n'),c('empty','0\n',''),c('sorting','4\nZ\nA\nZ\nB\n','A 1\nB 1\nZ 2\n')],
 'A-05': [c('sample','products.csv\n','Pencil, Blue|300\nHe said "Hi"|500\nERROR 3 UNCLOSED_QUOTE\n',{'products.csv':'"Pencil, Blue",300\n"He said ""Hi""",500\n"Broken,200\n'}),c('bad price','products.csv\n','ERROR 1 BAD_PRICE\nOK|0\n',{'products.csv':'A,-1\nOK,0\n'}),c('bad column count','products.csv\n','ERROR 1 BAD_FORMAT\n',{'products.csv':'A,10,extra\n'}),c('CRLF records','products.csv\n','Good|42\n',{'products.csv':'Good,42\r\n'})],
 'C-01': [c('sample','','ACCEPTED 2\nWAITLIST 1\nREJECTED 2\n',{'capacity.txt':'2\n','registrations.csv':'Mina,mina@demo.com\nJun,jun@demo.com\nMina Again,mina@demo.com\nHana,hana@demo.com\n,none@demo.com\n'}, {'accepted.csv':'Mina,mina@demo.com\nJun,jun@demo.com\n','waitlist.csv':'Hana,hana@demo.com\n','rejected.csv':'3,DUPLICATE\n5,MISSING_FIELD\n'}),c('zero capacity and duplicates','','ACCEPTED 0\nWAITLIST 1\nREJECTED 2\n',{'capacity.txt':'0\n','registrations.csv':',test@site.net\nA,test@site.net\nB,test@site.net\n'}, {'accepted.csv':'','waitlist.csv':'A,test@site.net\n','rejected.csv':'1,MISSING_FIELD\n3,DUPLICATE\n'})],
 'C-02': [c('sample','','',{'readings.csv':'A01,1,72\nB02,1,86\nA01,2,83\nA01,2,50\nB02,0,81\n'}, {'devices.csv':'A01,2,83,WARN\nB02,1,86,WARN\n','rejected.csv':'4,BAD_SEQUENCE\n5,BAD_SEQUENCE\n'}),c('failed reading does not change seq','','',{'readings.csv':'A,1,101\nA,1,5\nA,2,79\n'}, {'devices.csv':'A,2,79,OK\n','rejected.csv':'1,BAD_READING\n'})],
 'C-03': [c('sample','','',{'stock.csv':'P01,5\n','events.csv':'E01,P01,OUT,3\nE02,P01,OUT,4\nE01,P01,OUT,3\n'}, {'inventory.csv':'P01,2\n','rejected.csv':'2,INSUFFICIENT_STOCK\n3,DUPLICATE_EVENT\n'}),c('failed ID reusable','','',{'stock.csv':'P,5\n','events.csv':'E1,P,OUT,6\nE1,P,OUT,3\nE1,P,OUT,1\n'}, {'inventory.csv':'P,2\n','rejected.csv':'1,INSUFFICIENT_STOCK\n3,DUPLICATE_EVENT\n'})],
 'R-01': [c('sample','','TOTAL_NET 5000\nUNSETTLED_ORDERS 1\nREJECTED 1\n',{'orders.csv':'A01,10000\n','events.csv':'E01,A01,PAY,7000\nE02,A01,REFUND,2000\nE01,A01,PAY,7000\n'}, {'settlement.csv':'A01,10000,5000,5000\n','rejected.csv':'events.csv,3,DUPLICATE_EVENT\n'}),c('rejections sorted and ID reuse','','TOTAL_NET 40\nUNSETTLED_ORDERS 2\nREJECTED 7\n',{'orders.csv':'O1,100\nO1,900\nO2,20\nN,0\n','events.csv':'E1,O1,PAY,60\nE2,O1,REFUND,70\nE2,O1,REFUND,20\nE3,O1,PAY,70\nE4,O3,PAY,1\nE5,O1,FOO,2\nE1,O1,PAY,1\n'}, {'settlement.csv':'O1,100,40,60\nO2,20,0,20\n','rejected.csv':'events.csv,2,REFUND_EXCEEDS_PAY\nevents.csv,4,ORDER_EXCEEDED\nevents.csv,5,UNKNOWN_ORDER\nevents.csv,6,BAD_TYPE\nevents.csv,7,DUPLICATE_EVENT\norders.csv,2,DUPLICATE_ORDER\norders.csv,4,BAD_AMOUNT\n'})]
}

def run_case(exe, pid, test):
    label, stdin, expected, inputs, outputs=test
    with tempfile.TemporaryDirectory(prefix='summary-case-') as temp:
        path=Path(temp)
        for name,text in inputs.items(): (path/name).write_bytes(text.encode('utf-8'))
        result=subprocess.run([str(exe)],input=stdin,text=True,encoding='utf-8',capture_output=True,cwd=path,timeout=15)
        if result.returncode!=0:raise AssertionError(f'exit={result.returncode}; stderr={result.stderr}')
        if result.stdout!=expected:raise AssertionError(f'stdout {result.stdout!r} != {expected!r}')
        for name,text in outputs.items():
            f=path/name
            if not f.is_file():raise AssertionError(f'missing {name}')
            got=f.read_text(encoding='utf-8')
            if got!=text:raise AssertionError(f'{name} {got!r} != {text!r}')
        if pid=='R-01':
            again=subprocess.run([str(exe)],input=stdin,text=True,encoding='utf-8',capture_output=True,cwd=path,timeout=15)
            if again.returncode or again.stdout!=expected:raise AssertionError('not repeatable on second run')
            for name,text in outputs.items():
                if (path/name).read_text(encoding='utf-8')!=text:raise AssertionError(f'rerun changed {name}')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--compiler',default='g++')
    parser.add_argument('--problem',choices=IDS)
    args=parser.parse_args()
    tested=[args.problem] if args.problem else IDS
    passed=total=0
    with tempfile.TemporaryDirectory(prefix='cpp-summary-build-') as temp:
        for pid in tested:
            exe=Path(temp)/(pid+('.exe' if __import__('os').name=='nt' else ''))
            command=[args.compiler,'-std=c++20','-Wall','-Wextra','-Wpedantic','-Werror',str(ROOT/'solutions'/f'{pid}.cpp'),'-o',str(exe)]
            p=subprocess.run(command,capture_output=True,text=True,timeout=90)
            if p.returncode:
                print(f'COMPILE FAIL {pid}: {p.stderr}')
                total+=len(CASES[pid]);continue
            for test in CASES[pid]:
                total+=1
                try:run_case(exe,pid,test);passed+=1
                except Exception as err:print(f'FAIL {pid} {test[0]}: {err}')
            print(f'CHECKED {pid}: {len(CASES[pid])} cases')
    print(f'RESULT: {passed}/{total} passed ({args.compiler})')
    return 0 if passed==total else 1

if __name__=='__main__':raise SystemExit(main())
