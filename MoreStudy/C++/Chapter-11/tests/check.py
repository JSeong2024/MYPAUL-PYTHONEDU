#!/usr/bin/env python3
"""Chapter 11 GCC/Clang validation without third-party dependencies."""
import argparse
import os
import subprocess
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--mode',choices=['reference','student'],default='reference')
parser.add_argument('--only',default='')
parser.add_argument('--compiler',default=os.environ.get('CXX','g++-14'))
args=parser.parse_args()
checks=[]
def test(name,src,stdin='',expected=None,argv=None,code=0,multi=None):
    if args.only and args.only not in name:return
    with tempfile.TemporaryDirectory() as td:
        dest=Path(td)/'run'
        paths=[str(ROOT/path) for path in (multi or [src])]
        cp=subprocess.run([args.compiler,'-std=c++20','-Wall','-Wextra','-Wpedantic','-Werror',*paths,'-o',str(dest)],capture_output=True,text=True)
        if cp.returncode:
            checks.append((name,False,cp.stderr.strip()[:500]));return
        run=subprocess.run([str(dest),*(argv or [])],input=stdin,capture_output=True,text=True,cwd=ROOT)
        ok=(run.returncode==code and (expected is None or expected in run.stdout))
        checks.append((name,ok, f'return={run.returncode} stdout={run.stdout!r} stderr={run.stderr!r}'))
with tempfile.TemporaryDirectory() as td:
    temp=Path(td)
    file=temp/'sample.txt';file.write_text('first\nsecond\n',encoding='utf-8')
    numbers=temp/'numbers.txt';numbers.write_text('10 20 30\n')
    bad=temp/'bad.txt';bad.write_text('10 20 invalid\n')
    event=temp/'events.txt';event.write_text('WARN\nINFO\nWARN\n')
    inv=temp/'inventory.csv';inv.write_text('battery,5\ncamera,2\n')
    raw=temp/'packet.bin';raw.write_bytes(bytes([0x12,0x34,0x56,0x78]))
    too_short=temp/'short.bin';too_short.write_bytes(bytes([0x12]))
    for f in sorted((ROOT/'examples').glob('*.cpp')):
        key=f.name[:2];name='example-'+key
        if key in {'01','02','07','13','15'}: argv=[str(file)]
        elif key in {'03','04','12','14'}:argv=[str(temp/(name+'.txt'))]
        else:argv=[]
        expected={'01':'Bytes: 13','02':'1: first','03':'Saved 2 lines','04':'Appended event','05':'Token: abc','06':'Filename: result.csv','07':'Exists: true','08':'Reading: 42','09':'Location: north, west','10':'Round trip: true','12':'status=ready','13':'First line: first','14':'Saved report','15':'Lines: 2','16':'UTF-8 bytes: 6'}.get(key)
        test(name, f.relative_to(ROOT),expected=expected,argv=argv)
    folder='solutions' if args.mode=='reference' else 'exercises'
    for key,fn,argv,expected in [
        ('01','01_temperature_summary.cpp',[str(numbers)],'Average: 20.00'),
        ('02','02_event_log_summary.cpp',[str(event)],'WARN: 2'),
        ('03','03_inventory_csv.cpp',[str(inv)],'battery: 5'),
        ('04','04_binary_u32_reader.cpp',[str(raw)],'Value: 305419896'),
    ]:test('exercise-'+key,f'{folder}/{fn}',expected=expected,argv=argv)
    test('exercise-01-bad',f'{folder}/01_temperature_summary.cpp',argv=[str(bad)],code=1)
    test('exercise-04-short',f'{folder}/04_binary_u32_reader.cpp',argv=[str(too_short)],code=1)
    proj='examples/17_sensor_report'
    test('project-valid',None, multi=[f'{proj}/main.cpp',f'{proj}/report.cpp'],argv=[str(ROOT/f'{proj}/data/readings.csv'),str(temp/'result.txt')],expected='Saved report: 4 readings from 3 devices')
    test('project-invalid',None,multi=[f'{proj}/main.cpp',f'{proj}/report.cpp'],argv=[str(bad),str(temp/'bad-report.txt')],code=1)
for name,ok,detail in checks:
 print(f"{'PASS' if ok else 'FAIL'} {name}")
 if not ok:print('    '+detail)
print(f"Results: {sum(ok for _,ok,_ in checks)}/{len(checks)} PASS")
raise SystemExit(0 if all(ok for _,ok,_ in checks) else 1)
