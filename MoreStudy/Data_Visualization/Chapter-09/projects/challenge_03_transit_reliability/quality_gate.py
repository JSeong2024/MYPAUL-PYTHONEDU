"""Executable challenge-03 verification gate for a candidate CLI implementation.

PASS = candidate finished the contract and generated coherent artifacts.
FAIL = implementation or input-reference contract did not behave as specified.
Exit 0/1. Rejected individual rows are *not* themselves failures.
"""
from __future__ import annotations
import argparse
import csv
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import pandas as pd
from PIL import Image, ImageStat

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
EXPECTED=['audit.csv','coverage.csv','station_summary.csv','daily_summary.csv','incident_comparison.csv','hourly.csv','overview.png','explorer.html','summary.json','manifest.json']

def hash_file(p):return sha256(p.read_bytes()).hexdigest()

def run_cli(script,data,out,extra=()):
 cmd=[sys.executable,str(script),'--data',str(data),'--output',str(out),*extra]
 r=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
 return r

def check_result(data,out,selected_stops=None):
 for n in EXPECTED:
  if not (out/n).is_file():raise AssertionError(f'G1: missing output: {n}')
 manifest=json.loads((out/'manifest.json').read_text(encoding='utf-8'))
 for name,digest in manifest['input_sha256'].items():
  if hash_file(data/name)!=digest:raise AssertionError(f'G2: input hash differs: {name}')
 for name,digest in manifest['output_sha256'].items():
  if hash_file(out/name)!=digest:raise AssertionError(f'G2: output hash differs: {name}')
 schedule=pd.read_csv(data/'schedule.csv',dtype={'stop_id':str,'local_date':str})
 if selected_stops is not None:schedule=schedule[schedule.stop_id.isin(selected_stops)]
 cov=pd.read_csv(out/'coverage.csv')
 audit=pd.read_csv(out/'audit.csv')
 summary=json.loads((out/'summary.json').read_text(encoding='utf-8'))
 station=pd.read_csv(out/'station_summary.csv')
 daily=pd.read_csv(out/'daily_summary.csv')
 hourly=pd.read_csv(out/'hourly.csv')
 if len(cov)!=len(schedule):raise AssertionError('G3: coverage expected count does not equal schedule')
 if cov.duplicated(['stop_id','local_date','expected_hour']).any():raise AssertionError('G3: duplicate coverage slot')
 cov['observed']=cov['observed'].astype(str).str.lower().eq('true')
 cov['missing']=cov['missing'].astype(str).str.lower().eq('true')
 if not (cov.observed!=cov.missing).all():raise AssertionError('G3: observed/missing flags inconsistent')
 if cov.loc[cov.missing,'boardings'].notna().any():raise AssertionError('G3: missing slot was filled with zero')
 if cov.loc[cov.observed,'boardings'].isna().any():raise AssertionError('G3: valid slot lacks passenger count')
 if (cov.loc[cov.observed,'boardings']<0).any():raise AssertionError('G3: invalid passenger count included')
 if len(audit)>0 and (audit.reason_codes.fillna('')=='').any():raise AssertionError('G3: audit reason missing')
 if summary['scheduled_slots']!=len(cov) or summary['valid_slots']!=int(cov.observed.sum()) or summary['missing_slots']!=int(cov.missing.sum()):raise AssertionError('G3: summary coverage mismatch')
 if summary['observed_boardings']!=int(cov.boardings.sum()):raise AssertionError('G3: passenger KPI mismatch')
 if summary['excluded_source_rows']!=len(audit):raise AssertionError('G3: audit KPI mismatch')
 if int(station.expected.sum())!=len(cov) or int(station.valid.sum())!=int(cov.observed.sum()):raise AssertionError('G3: station totals differ from coverage')
 if int(hourly.expected.sum())!=len(cov) or int(hourly.valid.sum())!=int(cov.observed.sum()):raise AssertionError('G3: hourly totals differ from coverage')
 if (daily.loc[daily.status=='partial','confirmed_boardings'].notna()).any():raise AssertionError('G3: incomplete days have confirmed totals')
 if (daily.loc[daily.status=='complete','confirmed_boardings'].isna()).any():raise AssertionError('G3: complete days missing confirmed totals')
 if summary['partial_station_days']!=int((daily.status=='partial').sum()):raise AssertionError('G3: partial days mismatch')
 with Image.open(out/'overview.png') as im:
  if im.format!='PNG' or im.width<850 or im.height<500:raise AssertionError('G4: PNG figure size/format mismatch')
  if max(ImageStat.Stat(im.convert('RGB')).stddev)<4:raise AssertionError('G4: PNG figure appears blank')
 html=(out/'explorer.html').read_text(encoding='utf-8')
 if 'Plotly.newPlot' not in html or 'transit-reliability' not in html or 'coverage' not in html.lower():raise AssertionError('G4: Plotly traces absent')
 for key,value in summary.items():
  if f'"{key}":{value}' not in html and f'"{key}": {value}' not in html:raise AssertionError(f'G4: interactive chart meta {key} differs')
 return summary,cov,audit,manifest

def main():
 p=argparse.ArgumentParser(description='Challenge 03 Quality Gate')
 p.add_argument('--script',type=Path,default=HERE/'starter.py',help='candidate CLI; accepts --data and --output')
 p.add_argument('--data',type=Path,default=HERE/'data')
 args=p.parse_args();script=args.script.resolve();errors=[];checks=0
 def check(name,fn):
  nonlocal checks
  try:fn();checks+=1;print(f'PASS {name}')
  except Exception as exc:errors.append(f'{name}: {exc}');print(f'FAIL {name}: {exc}')
 with tempfile.TemporaryDirectory(prefix='dv09_gate_') as temporary:
  work=Path(temporary);original=work/'original';shutil.copytree(args.data,original)
  base=work/'base'
  def baseline():
   r=run_cli(script,original,base)
   if r.returncode!=0:raise AssertionError(f'G1 base run exit {r.returncode}: {r.stderr[-500:]}')
   return check_result(original,base)
  base_result=[]
  def base_check():base_result.append(baseline())
  check('G1-G4 base artifacts, data contract, plots, hashes',base_check)
  if not base_result:
   print('FAIL: baseline could not be verified; remaining scenarios skipped');return 1
  baseline_summary,_,_,manifest=base_result[0]
  def determinism():
   out=work/'repeat';r=run_cli(script,original,out)
   if r.returncode!=0:raise AssertionError(f'exit {r.returncode}: {r.stderr[-300:]}')
   check_result(original,out)
   for name in EXPECTED:
    if hash_file(base/name)!=hash_file(out/name):raise AssertionError(f'G5 non-reproducible {name}')
  check('G5 deterministic repeat',determinism)
  def scenario(name,mutate,verify,expected_exit=0,params=()):
   data=work/('data_'+name);shutil.copytree(original,data)
   mutate(data);out=work/('out_'+name)
   r=run_cli(script,data,out,params)
   if r.returncode!=expected_exit:raise AssertionError(f'exit {r.returncode}, expected {expected_exit}; stderr={r.stderr[-350:]}')
   if expected_exit==0:
    actual=check_result(data,out,selected_stops={'ST-01','ST-02','ST-03','ST-04'} if '--line' in params else None)
    verify(actual)
   elif (out/'manifest.json').exists():raise AssertionError('contract failure should not publish successful manifest')
  def change_operations(data,callback):
   path=data/'operations.csv';d=pd.read_csv(path,dtype=str,keep_default_na=False);callback(d)
   d.to_csv(path,index=False)
  def duplicate(d):
   row=d.iloc[15].copy();row['observation_id']='OB-QG-DUP';d.loc[len(d)]=row
  def verify_dup(a):
   summary,cov,audit,_=a
   if summary['valid_slots']!=baseline_summary['valid_slots']-1:raise AssertionError('duplicate slot did not invalidate original')
   if audit.reason_codes.astype(str).str.contains('duplicate_slot').sum()<2:raise AssertionError('both competing rows not audited')
  check('G3 duplicate-slot: remove all competing rows',lambda:scenario('duplicate',lambda data:change_operations(data,duplicate),verify_dup))
  def negative(d):d.loc[15,'boardings']='-10'
  def verify_negative(a):
   summary,cov,audit,_=a
   if summary['valid_slots']!=baseline_summary['valid_slots']-1:raise AssertionError('negative passenger row not excluded')
   if not audit.reason_codes.astype(str).str.contains('invalid_boardings').any():raise AssertionError('invalid_boardings audit missing')
  check('G3 invalid passenger record: exclude with reason',lambda:scenario('negative',lambda data:change_operations(data,negative),verify_negative))
  def zero(d):d.loc[15,'boardings']='0'
  def verify_zero(a):
   summary,cov,audit,_=a
   if summary['valid_slots']!=baseline_summary['valid_slots']:raise AssertionError('zero passengers should remain a valid observation')
   if not cov.loc[cov.observed,'boardings'].eq(0).any():raise AssertionError('zero was not retained')
  check('G3 zero versus missing distinction',lambda:scenario('zero',lambda data:change_operations(data,zero),verify_zero))
  def corrupt_ref(data):
   path=data/'schedule.csv';d=pd.read_csv(path,dtype=str);d.loc[len(d)]={'stop_id':'ST-999','local_date':'2026-10-02','expected_hour':'7'};d.to_csv(path,index=False)
  check('G1 invalid schedule must FAIL',lambda:scenario('bad_schedule',corrupt_ref,lambda _:None,expected_exit=1))
  def noop(data):pass
  def verify_line(a):
   summary,cov,_,_=a
   if summary['scheduled_slots']!=224 or not cov.stop_id.str.match('ST-0[1-4]').all():raise AssertionError('line filter is inconsistent')
  check('G3 filtered line across all outputs',lambda:scenario('filter',noop,verify_line,params=('--line','L1')))
  def tamper():
   pth=base/'summary.json';value=json.loads(pth.read_text());value['observed_boardings']+=1;pth.write_text(json.dumps(value))
   try:check_result(original,base)
   except AssertionError:return
   raise AssertionError('tampered output was not detected')
  check('G2 altered artifact must FAIL integrity check',tamper)
 print(f'\n{"PASS" if not errors else "FAIL"}: {checks}/{checks+len(errors)} checks passed')
 return int(bool(errors))
if __name__=='__main__':raise SystemExit(main())
