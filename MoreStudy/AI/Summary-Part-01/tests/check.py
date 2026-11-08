#!/usr/bin/env python3
"""Run the AI Summary Part 01 reference solutions in isolated directories."""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
IDS=[f'{letter}-{i:02d}' for letter,count in [('B',5),('A',4),('P',3),('C',2),('R',1)] for i in range(1,count+1)]
BASIC={
 'B-01':('3 2\n1.5 2.0 0\n2.1 3.0 1\n1.2 2.8 0\n','SAMPLES 3\nFEATURES 2\nTARGET_0 2\nTARGET_1 1\n'),
 'B-02':('2 1\n2\n2 4\n3\n1 3\n2 6\n3 7\n','MODEL_MAE 0.3333\nMODEL_MSE 0.3333\nBASELINE_MAE 2.3333\nBEST MODEL\n'),
 'B-03':('2 5 1 0 0.1\n','GRAD_W -6.0000\nGRAD_B -3.0000\nNEW_W 1.6000\nNEW_B 0.3000\nPREDICTION 3.5000\n'),
 'B-04':('5 0.5\n0 0.10\n1 0.80\n1 0.40\n0 0.60\n1 0.90\n','TP 2\nFP 1\nFN 1\nTN 1\nPRECISION 0.6667\nRECALL 0.6667\nF1 0.6667\n'),
 'B-05':('0 0\n6 0\n3\n1 0\n5 0\n3 0\n','ASSIGNMENTS 0 1 0\nCENTER_0 2.0000 0.0000\nCENTER_1 5.0000 0.0000\n')}


def csv_rows(path):
    with open(path,encoding='utf-8',newline='') as file:return list(csv.DictReader(file))


def run(pid, workdir, stdin='', success=True):
    p=subprocess.run([sys.executable,str(ROOT/'solutions'/f'{pid}.py')],cwd=workdir,input=stdin,
                     text=True,capture_output=True,timeout=90)
    if success and p.returncode:
        raise AssertionError(f'{pid} failed: {p.stderr.strip()}')
    if not success and p.returncode==0:
        raise AssertionError(f'{pid} unexpectedly succeeded')
    return p


def prepare(pid, destination):
    src=ROOT/'data'/pid
    if src.exists():
        for f in src.iterdir():shutil.copy2(f,destination/f.name)


class SummaryTests(unittest.TestCase):
    def test_basic(self):
        for pid,(inp,expected) in BASIC.items():
            with self.subTest(pid=pid),tempfile.TemporaryDirectory() as tmp:
                self.assertEqual(run(pid,tmp,inp).stdout,expected)
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(run('B-01',tmp,'1 2\nNaN 2 1\n').stdout,'INVALID\n')
            self.assertEqual(run('B-01',tmp,'1 1\n7 1\n').stdout,'SAMPLES 1\nFEATURES 1\nTARGET_0 0\nTARGET_1 1\n')
            self.assertIn('TIE',run('B-02',tmp,'0 2\n1\n2\n1\n2 2\n').stdout)
            self.assertEqual(run('B-04',tmp,'2 0.9\n0 0.2\n0 0.8\n').stdout.splitlines()[-3:],['PRECISION 0.0000','RECALL 0.0000','F1 0.0000'])
            self.assertIn('CENTER_1 6.0000 0.0000',run('B-05',tmp,'0 0\n6 0\n1\n1 0\n').stdout)

    def test_a01(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);prepare('A-01',d);run('A-01',d)
            report=csv_rows(d/'threshold_report.csv');self.assertEqual(len(report),3)
            self.assertEqual(sum(r['selected']=='True' for r in report),1)
            self.assertEqual([r['threshold'] for r in report],['0.30','0.50','0.70'])
            # Invalid duplicated ID must abort without publishing new assessment.
            with (d/'validation_scores.csv').open('a') as out:out.write('R01,1,0.42\n')
            self.assertNotEqual(run('A-01',d,success=False).returncode,0)

    def test_a02(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);prepare('A-02',d);run('A-02',d)
            rows=csv_rows(d/'test_predictions.csv');self.assertEqual(len(rows),10)
            self.assertEqual([r['date'] for r in rows],sorted(r['date'] for r in rows))
            self.assertTrue(all(abs(float(r['actual'])-float(r['predicted'])-float(r['residual']))<.00011 for r in rows))
            self.assertEqual(len(csv_rows(d/'model_comparison.csv')),4)

    def test_a03(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);prepare('A-03',d);run('A-03',d)
            accepted=csv_rows(d/'cluster_assignments.csv');rejected=csv_rows(d/'invalid_rows.csv')
            prof=csv_rows(d/'cluster_profiles.csv')
            self.assertEqual(len(accepted),69)
            self.assertEqual([r['row_number'] for r in rejected],['71','72'])
            self.assertEqual(sum(int(p['sample_count']) for p in prof if p['method']=='kmeans'),len(accepted))
            self.assertEqual(sum(int(p['sample_count']) for p in prof if p['method']=='dbscan'),len(accepted))

    def test_a04(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);run('A-04',d)
            options=json.loads((d/'best_params.json').read_text());self.assertIn(options['best_n_neighbors'],[3,5,7])
            self.assertTrue(0<=options['mean_cv_accuracy']<=1)
            m=json.loads((d/'test_metrics.json').read_text());self.assertTrue(0<=m['test_balanced_accuracy']<=1)
            self.assertIn('Pipeline',(d/'audit_report.md').read_text())

    def test_p01(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);prepare('P-01',d);run('P-01',d)
            ev=json.loads((d/'evaluation.json').read_text());self.assertEqual(ev['group_intersections'],0)
            self.assertIn(ev['chosen_threshold'],[.35,.5,.65])
            self.assertIn('test_model_metrics',ev)
            source=csv_rows(d/'incoming_claims.csv')
            decisions=csv_rows(d/'incoming_decisions.csv')
            self.assertEqual([x['claim_id'] for x in source],[x['claim_id'] for x in decisions])
            queue=csv_rows(d/'daily_review_queue.csv')
            self.assertTrue(all(v<=3 for v in Counter(x['received_date'] for x in queue).values()))
            self.assertEqual(len(csv_rows(d/'invalid_claims.csv')),2)

    def test_p02(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);prepare('P-02',d);run('P-02',d)
            rows=csv_rows(d/'test_predictions.csv')
            self.assertEqual(len(set(r['forecast_week'] for r in rows)),6)
            self.assertEqual(len(rows),48)
            self.assertTrue(all(abs(float(r['actual'])-float(r['predicted'])-float(r['residual']))<.00011 for r in rows))
            self.assertLessEqual(len(csv_rows(d/'underprediction_top5.csv')),5)

    def test_p03(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);prepare('P-03',d);run('P-03',d)
            self.assertEqual(len(csv_rows(d/'cluster_assignments.csv')),132)
            self.assertEqual([(s['seed_a'],s['seed_b']) for s in csv_rows(d/'stability.csv')],[('7','21'),('7','42'),('21','42')])
            self.assertEqual(sum(int(s['sample_count']) for s in csv_rows(d/'cluster_profiles.csv')),132)
            self.assertIn('운영 변경안',(d/'report.md').read_text())

    def test_c01(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);prepare('C-01',d);run('C-01',d)
            split=json.loads((d/'split_audit.json').read_text())
            self.assertEqual(split['repaired_group_intersection_count'],0)
            self.assertGreater(split['vulnerable_random_split_group_overlap'],0)
            self.assertNotIn('final_repair_code',split['allowed_input_features'])
            metrics=csv_rows(d/'metric_comparison.csv');self.assertEqual(len(metrics),4)
            self.assertGreater(len(csv_rows(d/'error_by_device.csv')),0)
            self.assertGreaterEqual(len(csv_rows(d/'data_audit.csv')),1)

    def test_c02(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);prepare('C-02',d);run('C-02',d)
            result=d/'results';self.assertEqual(len(csv_rows(result/'normalized_incoming.csv')),2)
            self.assertEqual([(x['source_line'],x['error_code']) for x in csv_rows(result/'rejected_rows.csv')],[('3','MISSING_TEMPERATURE'),('4','DUPLICATE_DATE')])
            self.assertEqual([r['temperature_c'] for r in csv_rows(result/'normalized_incoming.csv')],['25.0000','20.0000'])
            before=(result/'predictions.csv').read_bytes()
            (d/'history_v1.csv').unlink()
            run('C-02',d,success=False)
            self.assertEqual((result/'predictions.csv').read_bytes(),before)

    def test_r01(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);prepare('R-01',d);run('R-01',d)
            result=d/'results'
            expected={'clean_history.csv','rejected_rows.csv','split_report.json','model_report.json',
                      'test_predictions.csv','operational_predictions.csv','inspection_queue.csv',
                      'cluster_profiles.csv','performance_report.md','final_report.md'}
            self.assertEqual({p.name for p in result.iterdir()},expected)
            splits=json.loads((result/'split_report.json').read_text());self.assertEqual(splits['holdout_train_intersection'],0)
            self.assertEqual(splits['holdout_facilities'],['F05','F10','F15'])
            self.assertEqual(len(csv_rows(result/'rejected_rows.csv')),4)
            self.assertEqual(len(csv_rows(result/'operational_predictions.csv')),15)
            self.assertGreater(len(csv_rows(result/'test_predictions.csv')),0)
            queue=csv_rows(result/'inspection_queue.csv')
            self.assertTrue(all(v<=10 for v in Counter((x['date'],x['district']) for x in queue).values()))
            self.assertIn('evaluation_A',json.loads((result/'model_report.json').read_text()))
            stable={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in result.iterdir() if x.name!='performance_report.md'}
            run('R-01',d)
            self.assertEqual(stable,{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in result.iterdir() if x.name!='performance_report.md'})
            before=(result/'model_report.json').read_bytes()
            (d/'facilities.csv').unlink();run('R-01',d,success=False)
            self.assertEqual(before,(result/'model_report.json').read_bytes())


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--only',choices=['basic','a01','a02','a03','a04','p01','p02','p03','c01','c02','r01'])
    args=parser.parse_args()
    suite=unittest.TestSuite()
    methods=['test_'+args.only] if args.only else sorted(x for x in dir(SummaryTests) if x.startswith('test_'))
    for method in methods:suite.addTest(SummaryTests(method))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
