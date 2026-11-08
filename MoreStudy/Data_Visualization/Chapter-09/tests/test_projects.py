"""Integration checks for all ten independently runnable reference projects."""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
PIDS=['mini_01_weather_report','mini_02_retail_report','advanced_01_weather_dashboard','advanced_02_customer_behavior','advanced_03_service_monitor','advanced_04_electricity_demand','advanced_05_urban_metro','challenge_01_airport_operations','challenge_02_energy_anomalies','challenge_03_transit_reliability']

def launch(pid,data,out,flags=()):
 script=ROOT/'solutions'/pid/'reference_solution.py'
 return subprocess.run([sys.executable,str(script),'--data',str(data),'--output',str(out),*flags],text=True,capture_output=True,timeout=90)

class ProjectIntegration(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.temp=tempfile.TemporaryDirectory(prefix='dv09_proj_')
  cls.folder=Path(cls.temp.name)
  cls.results={}
  for pid in PIDS:
   data=ROOT/'projects'/pid/'data';out=cls.folder/pid
   r=launch(pid,data,out)
   if r.returncode!=0:raise AssertionError(f'{pid} failed: {r.stderr}')
   cls.results[pid]=out
 @classmethod
 def tearDownClass(cls):cls.temp.cleanup()
 def test_01_all_ten_projects_run(self):
  self.assertEqual(len(self.results),10)
 def test_02_each_has_independent_readme_starter_solution(self):
  for pid in PIDS:
   with self.subTest(pid=pid):
    self.assertTrue((ROOT/'projects'/pid/'README.md').exists())
    self.assertTrue((ROOT/'projects'/pid/'starter.py').exists())
    self.assertTrue((ROOT/'solutions'/pid/'reference_solution.py').exists())
 def test_03_figure_files_nonempty(self):
  for pid in PIDS:
   self.assertGreater((ROOT/'figures'/'projects'/(pid+'.png')).stat().st_size,5000)
 def test_mini_01_input_sorted_and_14_rows(self):
  d=pd.read_csv(self.results[PIDS[0]]/'daily_summary.csv');self.assertEqual(len(d),14)
  self.assertTrue(d.date.is_monotonic_increasing)
 def test_mini_02_cancelled_revenue_excluded(self):
  orders=pd.read_csv(ROOT/'projects'/PIDS[1]/'data'/'orders.csv')
  valid=orders[orders.status=='completed'];expect=int((valid.quantity*valid.unit_price_krw).sum())
  summary=pd.read_csv(self.results[PIDS[1]]/'category_revenue.csv')
  self.assertEqual(int(summary.revenue_krw.sum()),expect)
  self.assertEqual(int(summary.orders.sum()),len(valid))
 def test_advanced_01_missing_dates_are_nan(self):
  d=pd.read_csv(self.results[PIDS[2]]/'coverage.csv')
  self.assertEqual(len(d),4*21);self.assertEqual(int(d.observed.sum()),78)
  self.assertEqual(d.temperature_c.isna().sum(),6)
 def test_advanced_02_population_denominator(self):
  d=pd.read_csv(self.results[PIDS[3]]/'segment_summary.csv')
  self.assertTrue((d.registered_customers==25).all())
  self.assertTrue((d.participation_pct<=100).all())
  self.assertTrue((d.participation_pct>=0).all())
  self.assertTrue((d.revenue_per_buyer_krw>0).all())
 def test_advanced_03_strict_audit(self):
  out=self.results[PIDS[4]];a=pd.read_csv(out/'audit.csv');s=pd.read_csv(out/'summary.csv')
  self.assertEqual(len(a),7);self.assertEqual(int(s.request_count.sum()),1679)
  self.assertTrue(a.reason_codes.str.contains('invalid_').any())
 def test_advanced_03_p95_and_error_calculation_independent(self):
  out=self.results[PIDS[4]]
  valid=pd.read_csv(out/'valid_requests.csv');summary=pd.read_csv(out/'summary.csv')
  for _,r in summary.iterrows():
   part=valid[valid.service_id==r.service_id]
   self.assertAlmostEqual(r.p95_ms,part.latency_ms.quantile(.95,interpolation='linear'),places=3)
   self.assertAlmostEqual(r.error_rate_pct,100*part.status_code.between(500,599).mean(),places=3)
 def test_advanced_03_hours_include_empty_slots(self):
  h=pd.read_csv(self.results[PIDS[4]]/'hourly.csv')
  self.assertEqual(len(h),3*14*24)
  self.assertTrue(h[h.request_count==0].p95_ms.isna().all())
  self.assertTrue(h[h.request_count==0].error_rate_pct.isna().all())
 def test_advanced_04_incomplete_energy(self):
  d=pd.read_csv(self.results[PIDS[5]]/'daily_energy.csv')
  self.assertTrue(d[d.status=='partial'].energy_confirmed_mwh.isna().all())
  self.assertTrue(d[d.status=='complete'].energy_confirmed_mwh.notna().all())
  self.assertTrue((d.hour_count<=24).all())
 def test_advanced_05_zero_vs_missing(self):
  d=pd.read_csv(self.results[PIDS[6]]/'hourly_coverage.csv')
  self.assertEqual(len(d),960);self.assertEqual(int(d.observed.sum()),956)
  self.assertTrue(d[~d.observed].boardings.isna().all())
  self.assertTrue(d[d.observed].boardings.eq(0).any())
 def test_challenge_01_distinct_denominators(self):
  d=pd.read_csv(self.results[PIDS[7]]/'airport_summary.csv')
  self.assertTrue((d.scheduled==d.operated+d.cancelled).all())
  self.assertTrue((d.operated==d.on_time+d.delayed_15plus).all())
  self.assertTrue((abs(d.cancellation_pct-100*d.cancelled/d.scheduled)<1e-3).all())
  self.assertTrue((abs(d.on_time_pct-100*d.on_time/d.operated)<1e-3).all())
 def test_challenge_02_hourly_expectations(self):
  out=self.results[PIDS[8]];d=pd.read_csv(out/'coverage.csv');a=pd.read_csv(out/'anomalies.csv');summary=json.loads((out/'summary.json').read_text())
  self.assertEqual(len(d),2*15*24)
  self.assertEqual(int(d.observed.sum()),716)
  self.assertEqual(summary['missing_slots'],4)
  self.assertTrue((a.residual_mw.abs()>120).all())
 def test_challenge_03_manifest_output_and_values(self):
  out=self.results[PIDS[9]];summary=json.loads((out/'summary.json').read_text())
  self.assertEqual(summary['scheduled_slots'],672)
  self.assertEqual(summary['valid_slots'],664)
  self.assertEqual(summary['missing_slots'],8)
  self.assertEqual(summary['excluded_source_rows'],8)
  self.assertEqual(summary['observed_boardings'],55912)
  self.assertTrue((out/'manifest.json').is_file())
 def test_challenge_03_partial_day_not_confirmed(self):
  d=pd.read_csv(self.results[PIDS[9]]/'daily_summary.csv')
  self.assertTrue(d[d.status=='partial'].confirmed_boardings.isna().all())
  self.assertTrue(d[d.status=='complete'].confirmed_boardings.notna().all())
 def test_challenge_03_incident_end_exclusive(self):
  incident=pd.read_csv(self.results[PIDS[9]]/'incident_comparison.csv')
  self.assertEqual(int(incident.loc[incident.incident_id=='INC-001','expected_overlap_slots'].iloc[0]),3)
  self.assertEqual(int(incident.loc[incident.incident_id=='INC-001','valid_overlap_slots'].iloc[0]),2)

class MutationChecks(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(prefix='dv09_mut_');self.work=Path(self.temp.name)
 def tearDown(self):self.temp.cleanup()
 def setup_pid(self,pid):
  data=self.work/'data';shutil.copytree(ROOT/'projects'/pid/'data',data)
  return data,self.work/'out'
 def test_bad_mini01_negative_rain_fails(self):
  pid=PIDS[0];data,out=self.setup_pid(pid)
  df=pd.read_csv(data/'weather_daily.csv');df.loc[0,'precipitation_mm']=-5;df.to_csv(data/'weather_daily.csv',index=False)
  self.assertNotEqual(launch(pid,data,out).returncode,0)
 def test_mini02_cancelled_order_change_does_not_affect_revenue(self):
  pid=PIDS[1];data,out=self.setup_pid(pid)
  src=pd.read_csv(data/'orders.csv');idx=src.index[src.status=='cancelled'][0]
  src.loc[idx,'unit_price_krw']=999999;src.to_csv(data/'orders.csv',index=False)
  self.assertEqual(launch(pid,data,out).returncode,0)
  altered=pd.read_csv(out/'category_revenue.csv').revenue_krw.sum()
  original=pd.read_csv(ROOT/'projects'/pid/'data'/'orders.csv');exp=(original.loc[original.status=='completed','quantity']*original.loc[original.status=='completed','unit_price_krw']).sum()
  self.assertEqual(altered,exp)
 def test_advanced03_duplicate_mutation_audited(self):
  pid=PIDS[4];data,out=self.setup_pid(pid)
  df=pd.read_csv(data/'requests.csv',dtype=str);extra=df.iloc[[19]].copy();df=pd.concat([df,extra],ignore_index=True);df.to_csv(data/'requests.csv',index=False)
  self.assertEqual(launch(pid,data,out).returncode,0)
  audit=pd.read_csv(out/'audit.csv');self.assertGreaterEqual(audit.reason_codes.str.contains('duplicate_or_missing_request_id').sum(),4)
 def test_advanced03_no_requests_p95_missing(self):
  pid=PIDS[4];data,out=self.setup_pid(pid)
  self.assertEqual(launch(pid,data,out,('--start','2026-12-01','--end','2026-12-01')).returncode,0)
  d=pd.read_csv(out/'summary.csv');self.assertTrue(d.p95_ms.isna().all());self.assertTrue(d.error_rate_pct.isna().all());self.assertTrue((d.request_count==0).all())
 def test_advanced03_http_decimal_excluded(self):
  pid=PIDS[4];data,out=self.setup_pid(pid)
  self.assertEqual(launch(pid,data,out).returncode,0)
  audit=pd.read_csv(out/'audit.csv');self.assertTrue(audit.reason_codes.str.contains('invalid_status_code').any())
 def test_advanced05_line_filter(self):
  pid=PIDS[6];data,out=self.setup_pid(pid)
  self.assertEqual(launch(pid,data,out,('--line','L1')).returncode,0)
  d=pd.read_csv(out/'station_summary.csv');self.assertEqual(len(d),3);self.assertTrue(d.line.eq('L1').all())
 def test_challenge01_early_arrival_counts_ontime(self):
  pid=PIDS[7];data,out=self.setup_pid(pid)
  df=pd.read_csv(data/'flights.csv');df['arrival_delay_min']=pd.to_numeric(df.arrival_delay_min,errors='coerce')
  row=df[(df.status=='operated')&(df.arrival_delay_min<0)].iloc[0]
  self.assertEqual(launch(pid,data,out).returncode,0)
  self.assertGreater(len(row),0)
 def test_challenge02_high_threshold(self):
  pid=PIDS[8];data,out=self.setup_pid(pid)
  self.assertEqual(launch(pid,data,out,('--threshold-mw','300')).returncode,0)
  d=pd.read_csv(out/'anomalies.csv');self.assertEqual(len(d),0)
 def test_challenge03_unknown_schedule_stop_fails(self):
  pid=PIDS[9];data,out=self.setup_pid(pid)
  df=pd.read_csv(data/'schedule.csv');df.loc[0,'stop_id']='ST-999';df.to_csv(data/'schedule.csv',index=False)
  self.assertNotEqual(launch(pid,data,out).returncode,0)
  self.assertFalse((out/'manifest.json').exists())
 def test_challenge03_line_filter_changes_counts(self):
  pid=PIDS[9];data,out=self.setup_pid(pid)
  self.assertEqual(launch(pid,data,out,('--line','L1')).returncode,0)
  d=json.loads((out/'summary.json').read_text());self.assertEqual(d['scheduled_slots'],224)
 def test_challenge03_same_inputs_reproducible(self):
  pid=PIDS[9];data,out=self.setup_pid(pid)
  self.assertEqual(launch(pid,data,out).returncode,0)
  first=(out/'manifest.json').read_bytes()
  self.assertEqual(launch(pid,data,out).returncode,0)
  self.assertEqual(first,(out/'manifest.json').read_bytes())

if __name__=='__main__':unittest.main()
