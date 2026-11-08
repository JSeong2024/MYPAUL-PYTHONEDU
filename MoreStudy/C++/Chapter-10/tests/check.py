#!/usr/bin/env python3
"""Compile and check Chapter 10 examples, solutions, and Mini Project."""
import argparse
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = {
    '01_sequence_containers': 'Samples: 4\nFirst task: 1\nCheckpoint: 10\nCheckpoint: 20\nCheckpoint: 30\n',
    '02_ordered_containers': 'battery: 5\ncamera: 2\nUnique channels: 3\nFirst channel >= 4: 5\n',
    '03_unordered_frequency': 'INFO: 2\nWARN: 2\nERROR: 1\nContains DEBUG: false\n',
    '04_container_adaptors': 'Next queue item: 101\nLatest history item: 2\nHighest priority: 90\n',
    '05_iterator_ranges': 'First: 12\nDistance: 4\nSum: 70\n',
    '06_search_predicates': 'First slow: 90 ms\nAll valid: true\nAt least 40 ms: 2\n',
    '07_stable_sort': 'scan: 2\nupload: 2\nsave: 1\n',
    '08_erase_remove': 'Removed: 2\nRemaining: 20 18 25\n',
    '09_transform_and_aggregate': 'Calibrated: 12 22 32\nTotal: 66\n',
    '10_numeric_algorithms': 'Total: 20\nSquared sum: 120\nPrefix: 2 6 12 20\n',
    '11_ranges_views': 'Half of >=20: 10 15 21 25\n',
    '12_ranges_to': 'Selected: 15 23 19\n',
    '13_binary_search': 'Has 7: true\nFirst 2 index: 0\n',
    '14_transparent_lookup': 'lidar: 4\nHas imu: false\n',
    '15_invalidation_safe_erase': 'Valid: 10 20 30\n',
    '16_priority_scheduling': 'navigate: 90\nupload: 90\nscan: 70\n',
}
SOLUTIONS = {
    '01_event_frequency': [
        ('counts', '6\nWARN INFO WARN ERROR INFO INFO\n',0,'ERROR: 1\nINFO: 3\nWARN: 2\n',''),
        ('one', '1\nOK\n',0,'OK: 1\n',''),
        ('invalid', '0\n',1,'','Error: invalid count\n'),
        ('missing', '2\nOK\n',1,'','Error: invalid event\n'),
    ],
    '02_top_k_tasks': [
        ('top-three', '5 3\nscan 70\nsave 30\nnavigate 90\nupload 90\nidle 10\n',0,'navigate 90\nupload 90\nscan 70\n',''),
        ('ties', '3 2\nz 10\na 10\nb 10\n',0,'a 10\nb 10\n',''),
        ('invalid', '2 3\n',1,'','Error: invalid task count\n'),
        ('bad-priority', '1 1\nA 101\n',1,'','Error: invalid task\n'),
    ],
    '03_clean_readings': [
        ('mixed', '8\n12 -1 7 12 30 -1 7 10\n',0,'7 10 12 30\n',''),
        ('empty', '2\n-1 -1\n',0,'EMPTY\n',''),
        ('range', '4\n0 1000 0 500\n',0,'0 500 1000\n',''),
        ('invalid', '1\n1001\n',1,'','Error: invalid reading\n'),
    ],
    '04_device_summary': [
        ('means', '5\nA 10\nB 20\nA 14\nB 30\nC 8\n',0,'A: count=2, mean=12.0\nB: count=2, mean=25.0\nC: count=1, mean=8.0\n',''),
        ('bound', '2\nX 0\nX 1000000\n',0,'X: count=2, mean=500000.0\n',''),
        ('invalid', '1\nA -1\n',1,'','Error: invalid device entry\n'),
    ],
}
PROJECT = [
    ('mixed', '6\nCAM INFO 12\nLIDAR WARN 80\nCAM ERROR 24\nCAM WARN 36\nLIDAR INFO 20\nIMU INFO 5\n',0,
     '--- Device Event Summary ---\nEvents: 6\nDevices: 3\nWarnings: 2\nErrors: 1\nAverage latency: 29.50 ms\nCAM: 3 events, avg 24.0 ms\nIMU: 1 events, avg 5.0 ms\nLIDAR: 2 events, avg 50.0 ms\nTop device: CAM (3)\n', ''),
    ('one', '1\nCPU INFO 0\n',0,
     '--- Device Event Summary ---\nEvents: 1\nDevices: 1\nWarnings: 0\nErrors: 0\nAverage latency: 0.00 ms\nCPU: 1 events, avg 0.0 ms\nTop device: CPU (1)\n',''),
    ('tie', '2\nZ WARN 100\nA ERROR 200\n',0,
     '--- Device Event Summary ---\nEvents: 2\nDevices: 2\nWarnings: 1\nErrors: 1\nAverage latency: 150.00 ms\nA: 1 events, avg 200.0 ms\nZ: 1 events, avg 100.0 ms\nTop device: A (1)\n',''),
    ('invalid-count','0\n',1,'','Error: invalid record count\n'),
    ('invalid-level','1\nCPU DEBUG 20\n',1,'','Error: invalid record\n'),
    ('negative','1\nCPU INFO -1\n',1,'','Error: invalid record\n'),
    ('too-large','1\nCPU INFO 1000001\n',1,'','Error: invalid record\n'),
    ('missing','1\nCPU INFO\n',1,'','Error: invalid record\n'),
]
DRIVERS = {
    '01_event_frequency':r'''
int main() {
    const auto a = count_events({"WARN", "INFO", "WARN"});
    const auto empty = count_events({});
    return a.size()==2 && a.at("WARN")==2 && a.at("INFO")==1 && empty.empty()
      && count_events({"z","a"}).begin()->first == "a" ? 0 : 1;
}
''',
    '02_top_k_tasks':r'''
int main() {
    const std::vector<Task> input{{"z",10},{"a",10},{"b",50},{"c",1}};
    const auto top = top_k(input,3);
    if (top.size()!=3 || top[0].name!="b" || top[1].name!="a" || top[2].name!="z") return 1;
    if (!top_k(input,0).empty() || top_k({},3).size()!=0) return 2;
    return 0;
}
''',
    '03_clean_readings':r'''
int main() {
    if (clean_readings({}).size()!=0) return 1;
    if (clean_readings({-1,-1}).size()!=0) return 2;
    if (clean_readings({10,-1,3,10,0,3})!=std::vector<int>({0,3,10})) return 3;
    if (clean_readings({1000,1000,1})!=std::vector<int>({1,1000})) return 4;
    return 0;
}
''',
    '04_device_summary':r'''
int main() {
    const auto empty = summarize({});
    if (!empty.empty()) return 1;
    const auto counts = summarize({{"B",7},{"A",5},{"B",3}});
    if (counts.size()!=2 || counts.at("B").sum!=10 || counts.at("B").count!=2) return 2;
    if (counts.at("A").sum!=5 || counts.at("A").count!=1) return 3;
    return 0;
}
''',
}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--compiler',default='g++')
    parser.add_argument('--mode',choices=['reference','student'],default='reference')
    parser.add_argument('--only',help='Examples: exercise-02, project, example-12')
    args=parser.parse_args()
    passed=failed=0

    with tempfile.TemporaryDirectory() as scratch:
        build=Path(scratch)

        def compile_program(source,exe):
            cmd=[args.compiler,'-std=c++20','-Wall','-Wextra','-Wpedantic',str(source),'-o',str(exe)]
            r=subprocess.run(cmd,capture_output=True,text=True)
            return r.returncode==0,r.stderr

        def report(label,ok,info=''):
            nonlocal passed, failed
            if ok:
                passed+=1
                print('PASS',label)
            else:
                failed+=1
                print('FAIL',label,info[:700])

        def cases_for(source,cases,label):
            exe=build/re.sub(r'[^a-zA-Z0-9_]', '_',label)
            ok,err=compile_program(source,exe)
            report(label+' compile',ok,err)
            if not ok: return
            for name,stdin,rc,stdout,stderr in cases:
                r=subprocess.run([str(exe)],input=stdin,capture_output=True,text=True,timeout=3)
                good=(r.returncode==rc and r.stdout==stdout and r.stderr==stderr)
                report(label+' '+name,good,f'got rc={r.returncode} out={r.stdout!r} err={r.stderr!r}')

        if args.mode=='reference':
            for name,stdout in OUTPUTS.items():
                if args.only and args.only!=f'example-{name[:2]}': continue
                cases_for(ROOT/'examples'/f'{name}.cpp',[('output','',0,stdout,'')],name)
        folder='solutions' if args.mode=='reference' else 'exercises'
        for name,cases in SOLUTIONS.items():
            if args.only and args.only!=f'exercise-{name[:2]}': continue
            cases_for(ROOT/folder/f'{name}.cpp',cases,name)
            # Test the actual function, not just a memorized console output.
            code=(ROOT/folder/f'{name}.cpp').read_text(encoding='utf-8')
            driver=build/(name+'_driver.cpp')
            driver.write_text('#define main chapter_original_main\n'+code+'\n#undef main\n'+DRIVERS[name],encoding='utf-8')
            exe=build/(name+'_driver')
            ok,err=compile_program(driver,exe)
            if ok:
                r=subprocess.run([str(exe)],capture_output=True,text=True,timeout=3)
                ok=r.returncode==0
                err=f'driver exit {r.returncode} {r.stderr}'
            report(name+' function cases',ok,err)

        if not args.only or args.only=='project':
            src=ROOT/('solutions/device_event_summary.cpp' if args.mode=='reference' else 'project/device_event_summary.cpp')
            exe=build/'device_event_summary'
            ok,err=compile_program(src,exe)
            report('project compile',ok,err)
            if ok:
                for name,stdin,rc,stdout,stderr in PROJECT:
                    r=subprocess.run([str(exe)],input=stdin,capture_output=True,text=True,timeout=3)
                    expected_out= '' if rc else ''.join(['Records (1-100): ']+[f'Record {i} (device level latency_ms): ' for i in range(1,int(stdin.split()[0])+1)]+[stdout])
                    if rc:
                        count=int(stdin.split()[0]) if stdin.split()[0].isdigit() else 0
                        expected_out='Records (1-100): '+('Record 1 (device level latency_ms): ' if count>=1 else '')
                    good=r.returncode==rc and r.stdout==expected_out and r.stderr==stderr
                    report('project '+name,good,f'got rc={r.returncode} out={r.stdout!r} err={r.stderr!r}')
    print(f'PASS {passed}, FAIL {failed}')
    return 0 if failed==0 else 1

if __name__=='__main__':
    sys.exit(main())