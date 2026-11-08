"""Chapter 04 C++20 compile and behavior checks (GCC/Clang)."""
import argparse
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
# (stdin, exit code, expected stdout, expected stderr)
EXAMPLES = {
    '01_for_and_counter': [('',0,''.join(f'Sample {n}\n' for n in range(1,6))+'Completed: 5\n','')],
    '02_accumulation': [('',0,'Total: 100\nAverage: 25.0\n','')],
    '03_while_countdown': [('',0,'3\n2\n1\nReady!\n','')],
    '04_do_while_menu': [
        ('1\n0\n',0,'1. Show status\n0. Exit\nSelect: Status: READY\n1. Show status\n0. Exit\nSelect: Goodbye\n',''),
        ('2\n0\n',0,'1. Show status\n0. Exit\nSelect: Unknown selection\n1. Show status\n0. Exit\nSelect: Goodbye\n',''),
        ('abc\n',1,'1. Show status\n0. Exit\nSelect: ','Error: integer input required.\n'),
    ],
    '05_break_and_continue': [('',0,'Accepted: 0\nAccepted: 2\nAccepted: 4\nLimit reached\n','')],
    '06_range_for_string': [('',0,'Code: A1B2C\nDigits: 2\n','')],
    '07_limited_retry': [
        ('25\n',0,'Reading (0-100): Accepted: 25\n',''),
        ('120\n25\n',0,'Reading (0-100): Invalid reading\nReading (0-100): Accepted: 25\n',''),
        ('-1\n101\n500\n',1,'Reading (0-100): Invalid reading\n'*3,'Error: retry limit exceeded.\n'),
        ('abc\n',1,'Reading (0-100): ','Error: integer input required.\n'),
    ],
    '08_nested_loops': [('',0,'#.#.#\n.#.#.\n#.#.#\n','')],
    '09_cxx20_iota': [('',0,'Step 1\nStep 2\nStep 3\nStep 4\n','')],
}
EXERCISES = {
    '01_sum_from_one': [
        ('1\n',0,'Sum: 1\n',''),('5\n',0,'Sum: 15\n',''),('100\n',0,'Sum: 5050\n',''),
        *[(x,1,'','Error: N must be between 1 and 100.\n') for x in ('0\n','101\n','abc\n')]],
    '02_countdown': [
        ('1\n',0,'1\nLaunch!\n',''),('3\n',0,'3\n2\n1\nLaunch!\n',''),
        ('20\n',0,''.join(f'{x}\n' for x in range(20,0,-1))+'Launch!\n',''),
        *[(x,1,'','Error: N must be between 1 and 20.\n') for x in ('0\n','21\n')]],
    '03_filter_readings': [
        ('5\n10\n-1\n20\n30\n-5\n',0,'Accepted: 3\nAverage: 20.0\n',''),
        ('1\n0\n',0,'Accepted: 1\nAverage: 0.0\n',''),
        ('2\n-1\n-2\n',1,'','Error: no accepted readings.\n'),
        *[(x,1,'','Error: count must be between 1 and 8.\n') for x in ('0\n','9\n')],
        *[(x,1,'','Error: reading must be between -100 and 100.\n') for x in ('1\n101\n','1\nabc\n')]],
    '04_checkerboard': [
        ('3 4\n',0,'#.#.\n.#.#\n#.#.\n',''),('1 1\n',0,'#\n',''),('2 2\n',0,'#.\n.#\n',''),
        ('8 8\n',0,''.join(''.join('#' if (i+j)%2==0 else '.' for j in range(8))+'\n' for i in range(8)),''),
        *[(x,1,'','Error: rows and columns must be between 1 and 8.\n') for x in ('0 3\n','2 9\n','a 3\n')]],
}
def report_output(readings):
    if not readings: return ''
    total=sum(readings)
    return (f'\n--- Sampling Report ---\nSamples: {len(readings)}\nTotal: {total}\n'
            f'Average: {total/len(readings):.2f}\nMinimum: {min(readings)}\n'
            f'Maximum: {max(readings)}\nHigh readings (>=80): {sum(x>=80 for x in readings)}\n')
PROJECT = {
    'sampling_report': [
        ('4\n80\n15\n95\n45\n',0,'Samples (1-6): '+''.join(f'Reading {n} (0-100): ' for n in range(1,5))+report_output([80,15,95,45]),''),
        ('2\n150\n95\n80\n',0,'Samples (1-6): Reading 1 (0-100): Invalid reading\nReading 1 (0-100): Reading 2 (0-100): '+report_output([95,80]),''),
        ('1\n0\n',0,'Samples (1-6): Reading 1 (0-100): '+report_output([0]),''),
        ('1\n100\n',0,'Samples (1-6): Reading 1 (0-100): '+report_output([100]),''),
        *[(x,1,'Samples (1-6): ','Error: sample count must be between 1 and 6.\n') for x in ('0\n','7\n','abc\n')],
        ('1\n-1\n101\n',1,'Samples (1-6): Reading 1 (0-100): Invalid reading\nReading 1 (0-100): Invalid reading\n','Error: reading retry limit exceeded.\n'),
        ('1\n12\n',0,'Samples (1-6): Reading 1 (0-100): '+report_output([12]),''),
        ('1\nabc\n',1,'Samples (1-6): Reading 1 (0-100): ','Error: integer input required.\n'),
    ],
}

def main():
    parser=argparse.ArgumentParser(description='Compile and validate Chapter 04 programs')
    modes=parser.add_mutually_exclusive_group()
    modes.add_argument('--exercise',choices=('01','02','03','04'),help='Check edited exercise file')
    modes.add_argument('--project',action='store_true',help='Check edited project file')
    args=parser.parse_args()
    compiler=shlex.split(os.environ.get('CXX','g++'))
    targets=[]
    if args.exercise:
        name=next(x for x in EXERCISES if x.startswith(args.exercise+'_'))
        targets=[(f'exercises/{name}.cpp',EXERCISES[name])]
    elif args.project:
        targets=[('project/sampling_report.cpp',PROJECT['sampling_report'])]
    else:
        targets=[(f'examples/{name}.cpp',cases) for name,cases in EXAMPLES.items()]
        targets += [(f'solutions/{name}.cpp',cases) for name,cases in EXERCISES.items()]
        targets += [('solutions/sampling_report.cpp',PROJECT['sampling_report'])]
    total=failed=0
    with tempfile.TemporaryDirectory(prefix='ch04_') as temp:
        for index,(source,cases) in enumerate(targets):
            executable=Path(temp)/f'program_{index}'
            command=compiler+['-std=c++20','-Wall','-Wextra','-Wpedantic','-Werror',str(ROOT/source),'-o',str(executable)]
            compiled=subprocess.run(command,capture_output=True,text=True,check=False)
            if compiled.returncode:
                failed+=1;total+=1
                print('FAIL compile:',source,compiled.stdout,compiled.stderr)
                continue
            for test_index,(stdin,exit_code,stdout,stderr) in enumerate(cases,1):
                total+=1
                try:
                    result=subprocess.run([str(executable)],input=stdin,capture_output=True,text=True,timeout=5,check=False)
                    actual=(result.returncode,result.stdout,result.stderr)
                    expected=(exit_code,stdout,stderr)
                    if actual!=expected:
                        failed+=1
                        print(f'FAIL {source} case {test_index}\n expected={expected!r}\n actual={actual!r}')
                    else: print(f'PASS {source} case {test_index}')
                except subprocess.TimeoutExpired:
                    failed+=1
                    print(f'FAIL {source} case {test_index}: timeout')
    print(f'\nResult: {total-failed}/{total} PASS')
    return 1 if failed else 0

if __name__=='__main__': sys.exit(main())
