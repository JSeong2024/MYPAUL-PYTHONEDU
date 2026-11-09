"""End-to-end checks of 15 reference programs, including failure paths."""
from pathlib import Path
import csv,json,subprocess,sys,tempfile,unittest
import pandas as pd
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
SOL=ROOT/'solutions'
DATA=ROOT/'data'

class SummaryTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(prefix='summary02-')
  self.addCleanup(self.tmp.cleanup)
  self.out=Path(self.tmp.name)/'output';self.out.mkdir()
 def execute(self,pid,stdin='',mode='run',data=None,expected_code=0):
  cmd=[sys.executable,str(SOL/f'{pid}.py')]
  if not pid.startswith('B-'):cmd+=['--data',str(data or DATA),'--out',str(self.out),'--mode',mode]
  r=subprocess.run(cmd,input=stdin,text=True,capture_output=True,timeout=80)
  self.assertEqual(r.returncode,expected_code,f'{pid}: {r.stderr[-1500:]}')
  return r.stdout.strip()
 def js(self,fn):return json.loads((self.out/fn).read_text())
 def test_basic_01(self):
  self.assertEqual(self.execute('B-01','2 3\n1 2 3\n4 5 6\n'),'SHAPE 2 3\nDTYPE float32\nCOLUMN_SUM 5.00 7.00 9.00\nROW_MEAN 2.00 5.00')
  self.assertEqual(self.execute('B-01','1 2\n1 NaN\n'),'INVALID')
 def test_basic_02(self):
  self.assertEqual(self.execute('B-02','2 2\n1 -2\n2 0.5\n10 20\n12 30\n'),'SAMPLE_1 22.00 9.00\nSAMPLE_2 26.00 14.00\nCHANNEL_MEAN 24.00 11.50')
  self.assertEqual(self.execute('B-02','1 1\n0\n0\n1\n'),'INVALID')
 def test_basic_03(self):
  self.assertEqual(self.execute('B-03','1 0 2 5 0.1\n'),'PREDICTION 2.0000\nLOSS 9.0000\nGRAD_W -12.0000\nGRAD_B -6.0000\nUPDATED_W 2.2000\nUPDATED_B 0.6000\nUPDATED_PREDICTION 5.0000')
 def test_basic_04(self):
  self.assertEqual(self.execute('B-04','5 3 4 2\n'),'LAYER_1_PARAMETERS 16\nLAYER_2_PARAMETERS 10\nTOTAL_PARAMETERS 26\nOUTPUT_SHAPE 5 2')
 def test_basic_05(self):
  self.assertEqual(self.execute('B-05','7 3 0\n10 20 30 40 50 60 70\n'),'BATCHES 3\nBATCH_1 10 20 30\nBATCH_2 40 50 60\nBATCH_3 70\nDROPPED 0')
  self.assertEqual(self.execute('B-05','2 5 1\n1 2\n'),'BATCHES 0\nDROPPED 2')
 def test_a01(self):
  self.execute('A-01');rep=self.js('quality_report.json');self.assertEqual(rep['valid_count'],14);self.assertEqual(rep['rejected_count'],3)
  self.assertEqual(len(pd.read_csv(self.out/'calibrated.csv')),14)
  self.assertTrue(set(pd.read_csv(self.out/'rejected_rows.csv').error_code).issuperset({'MISSING_VALUE','DUPLICATE_ID','INVALID_NUMBER'}))
 def test_a02(self):
  self.execute('A-02');hist=pd.read_csv(self.out/'training_history.csv');meta=self.js('model_selection.json')
  self.assertEqual(len(hist),100);self.assertEqual(meta['best_epoch'],int(hist.loc[hist.validation_accuracy.idxmax(),'epoch']))
  self.assertTrue((pd.read_csv(self.out/'test_predictions.csv').probability.between(0,1)).all())
 def test_a03(self):
  self.execute('A-03');history=pd.read_csv(self.out/'training_history.csv');self.assertEqual(len(history),60)
  comparison=self.js('comparison.json');self.assertIn(comparison['selected_candidate'],['A','B']);self.assertEqual(len(pd.read_csv(self.out/'test_predictions.csv')),46)
 def test_a04(self):
  self.execute('A-04',mode='train');self.assertTrue((self.out/'model_weights.pt').exists());self.assertFalse((self.out/'incoming_predictions.csv').exists())
  self.execute('A-04',mode='predict');self.assertEqual(self.js('handoff_report.json')['reload_max_abs_diff'],0)
  self.assertEqual(len(pd.read_csv(self.out/'incoming_predictions.csv')),40)
 def test_p01(self):
  self.execute('P-01');audit=self.js('split_audit.json');self.assertEqual(audit['intersection_train_validation'],0);self.assertEqual(audit['intersection_train_test'],0)
  p=pd.read_csv(self.out/'incoming_priorities.csv');self.assertTrue((p[p.selected].groupby(['site_id','recorded_date']).size()<=5).all())
  self.assertIn('threshold',self.js('evaluation.json'))
 def test_p02(self):
  self.execute('P-02');dates=self.js('split_dates.json');self.assertEqual(len(dates['gap_dates']),2)
  self.assertEqual(len(pd.read_csv(self.out/'underprediction_top5.csv')),5)
  self.assertIn('mlp',self.js('model_comparison.json'))
 def test_p03(self):
  self.execute('P-03');runs=pd.read_csv(self.out/'runs.csv');comp=pd.read_csv(self.out/'comparison.csv')
  self.assertEqual(len(runs),12);self.assertTrue((runs.optimizer_updates==120).all());self.assertEqual(len(comp),4)
  self.assertLessEqual(self.js('gradient_audit.json')['max_abs_diff'],1e-6)
 def test_c01(self):
  self.execute('C-01');audit=self.js('resume_audit.json');self.assertTrue(audit['matched']);self.assertEqual(audit['resumed_from_epoch'],9)
  self.assertEqual(len(pd.read_csv(self.out/'resumed_history.csv')),20)
 def test_c02(self):
  self.execute('C-02');report=self.js('incident_report.json');self.assertTrue(report['schema_valid']);self.assertEqual(report['invalid_count'],1)
  # Tampered model config must not replace the last accepted predictions.
  before=(self.out/'predictions.csv').read_bytes()
  with tempfile.TemporaryDirectory() as tmp:
   d=Path(tmp);import shutil
   for f in DATA.iterdir():
    if f.is_file():shutil.copy2(f,d/f.name)
   (d/'C-02').mkdir();shutil.copy2(DATA/'C-02'/'incoming.csv',d/'C-02'/'incoming.csv')
   config=json.loads((d/'model_config.json').read_text());config['input_dim']=5;(d/'model_config.json').write_text(json.dumps(config))
   self.execute('C-02',data=d,expected_code=1)
  self.assertEqual((self.out/'predictions.csv').read_bytes(),before)
 def test_r01(self):
  self.execute('R-01');r=self.js('resume_audit.json');self.assertTrue(r['matched']);self.assertLessEqual(r['max_parameter_diff'],1e-6)
  m=self.js('validation_selection.json');self.assertIn(m['selected_version'],['v1','v2'])
  b=self.js('benchmark.json');self.assertTrue(b['results_match']);self.assertTrue((self.out/'incoming_predictions.csv').exists())
  # Preserve the no-rollback-target edge case when v1 is active.
  self.execute('R-01',mode='rollback');self.assertEqual(self.js('rollback_report.json')['status'],'NO_ROLLBACK_TARGET')
  # Activate already verified v2 artifacts as a simulated prior deployment,
  # then verify rollback restores the previously saved v1 predictions.
  m=self.js('deployment_manifest.json');m.update({'active_version':'v2','previous_version':'v1'});(self.out/'deployment_manifest.json').write_text(json.dumps(m))
  self.execute('R-01',mode='rollback');self.assertEqual(self.js('rollback_report.json')['status'],'ROLLED_BACK')
  self.assertEqual((self.out/'incoming_predictions.csv').read_bytes(),(self.out/'versions'/'v1'/'incoming_predictions.csv').read_bytes())

if __name__=='__main__':unittest.main(verbosity=2)
