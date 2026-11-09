"""Chapter 07: 데이터·Practice·Project·Notebook·문서 무결성 검증."""
from __future__ import annotations
import ast
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import re
import runpy
import sys
import tempfile
import unittest
import numpy as np
import pandas as pd
import torch
from torch import nn
import nbformat

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
torch.set_num_threads(1)

from solutions import (practice_01_sgd_update as p1,
                       practice_02_weighted_epoch_loss as p2,
                       practice_03_clip_gradients as p3,
                       practice_04_early_stopper as p4,
                       practice_05_scheduler_steps as p5,
                       practice_06_micro_batch as p6,
                       mini_01_optimizer_comparison as mini1,
                       mini_02_learning_rate_scheduler as mini2,
                       advanced_01_generalization_clinic as advanced1,
                       advanced_02_gradient_audit as advanced2,
                       advanced_03_checkpoint_resume as advanced3,
                       professional_01_fleet_training as professional)
from scripts.make_datasets import generate
from solutions.common import energy_data,alert_data,seed_everything

class Chapter07Tests(unittest.TestCase):
    def test_01_data_sets_and_determinism(self):
        energy=pd.read_csv(ROOT/'data/energy_demand.csv')
        alerts=pd.read_csv(ROOT/'data/device_alerts.csv')
        fleet=pd.read_csv(ROOT/'data/fleet_events.csv')
        self.assertEqual((len(energy),len(alerts),len(fleet)),(360,420,768))
        self.assertFalse(any(df.isna().any().any() for df in (energy,alerts,fleet)))
        self.assertEqual(set(alerts.alert_label),{0,1})
        self.assertEqual(set(fleet.maintenance_label),{0,1})
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(generate(Path(td)),{
                'energy_demand.csv':360,'device_alerts.csv':420,'fleet_events.csv':768})
            for name in ['energy_demand.csv','device_alerts.csv','fleet_events.csv']:
                self.assertTrue(pd.read_csv(ROOT/'data'/name).equals(pd.read_csv(Path(td)/name)))

    def test_02_splits_and_scaling(self):
        d=energy_data()
        self.assertEqual([len(d[x][0]) for x in ['train','validation','test']],[240,60,60])
        x=d['train'][0].numpy()
        self.assertTrue(np.allclose(x.mean(axis=0),0,atol=2e-5))
        self.assertTrue(np.allclose(x.std(axis=0),1,atol=2e-5))
        a=alert_data()
        self.assertEqual([len(a[x][0]) for x in ['train','validation','test']],[252,84,84])
        indices=a['indices'];self.assertEqual(len(set(indices['train'])&set(indices['test'])),0)

    def test_03_practice_sgd(self):
        w=torch.tensor([2.,-1.]);g=torch.tensor([.5,-.2])
        self.assertTrue(torch.allclose(p1.sgd_update(w,g,.1),torch.tensor([1.95,-.98])))
        self.assertTrue(torch.equal(w,torch.tensor([2.,-1.])))
        with self.assertRaises(ValueError):p1.sgd_update(w,g,0)
        with self.assertRaises(ValueError):p1.sgd_update(w,torch.ones(2,1),.1)

    def test_04_practice_weighted_loss(self):
        self.assertAlmostEqual(p2.weighted_epoch_loss([.4,.9],[8,2]),.5)
        with self.assertRaises(ValueError):p2.weighted_epoch_loss([1.],[])
        with self.assertRaises(ValueError):p2.weighted_epoch_loss([float('nan')],[3])
        with self.assertRaises(ValueError):p2.weighted_epoch_loss([.5],[0])

    def test_05_practice_clipping(self):
        m=nn.Linear(2,1)
        m(torch.ones(2,2)).sum().backward()
        before,after=p3.clip_gradients(m,.5)
        self.assertGreater(before,.5)
        self.assertLessEqual(after,.50001)
        with self.assertRaises(ValueError):p3.clip_gradients(m,0)

    def test_06_practice_early_stopping(self):
        e=p4.EarlyStopper(patience=2)
        result=[e.update(n,v) for n,v in enumerate([.8,.6,.61,.62],1)]
        self.assertEqual(result,[False,False,False,True])
        self.assertEqual(e.best_epoch,2)
        with self.assertRaises(ValueError):p4.EarlyStopper(patience=0)

    def test_07_practice_scheduler(self):
        history=p5.learning_rate_history(.1,2,.5,5)
        self.assertTrue(np.allclose(history,[.1,.1,.05,.05,.025]))
        with self.assertRaises(ValueError):p5.learning_rate_history(.1,2,1.1,5)

    def test_08_practice_accumulation(self):
        seed_everything(16)
        x=torch.randn(11,2);y=torch.randn(11,1)
        m=nn.Linear(2,1)
        init={k:v.clone() for k,v in m.state_dict().items()}
        g_micro=p6.accumulate_gradient(m,x,y,4)
        full=nn.Linear(2,1);full.load_state_dict(init)
        full.zero_grad(set_to_none=True)
        nn.MSELoss()(full(x),y).backward()
        g_full=torch.cat([p.grad.flatten() for p in full.parameters()])
        self.assertTrue(torch.allclose(g_micro,g_full,atol=1e-6))

    def test_09_mini_optimizer(self):
        with tempfile.TemporaryDirectory() as td:
            summary,history,pred=mini1.run(output_dir=td)
            self.assertEqual(set(summary.optimizer),{'sgd_momentum','adamw'})
            self.assertEqual(len(history),72)
            self.assertEqual(len(pred),60)
            self.assertTrue(summary.test_mae_kwh.between(0,5).all())
            self.assertTrue((Path(td)/'optimizer_comparison.csv').exists())
            self.assertTrue((Path(td)/'test_predictions.csv').exists())

    def test_10_mini_scheduler(self):
        result,history=mini2.run()
        self.assertEqual(set(result.schedule),{'fixed_lr','step_lr'})
        self.assertEqual(len(history),56)
        fixed=history[history.schedule=='fixed_lr']
        step=history[history.schedule=='step_lr'].reset_index(drop=True)
        self.assertTrue(np.allclose(fixed.learning_rate,.085))
        self.assertAlmostEqual(step.loc[7,'learning_rate'],.085)
        self.assertAlmostEqual(step.loc[8,'learning_rate'],.0425)
        self.assertTrue(result.test_f1.between(0,1).all())

    def test_11_advanced_generalization(self):
        report,history,pred=advanced1.run()
        self.assertEqual(set(report.variant),{'unregularized','regularized'})
        self.assertEqual(len(pred),60)
        self.assertTrue((report.best_epoch<=report.epochs_run).all())
        self.assertTrue((report.best_epoch>=1).all())
        self.assertTrue((history.validation_loss>=0).all())

    def test_12_advanced_gradient_audit(self):
        audit,frame=advanced2.run()
        self.assertEqual(audit['micro_batch_sizes'],[4,4,3])
        self.assertLess(audit['max_gradient_difference'],1e-6)
        self.assertGreater(audit['gradient_norm_before_clip'],audit['clip_max_norm'])
        self.assertLessEqual(audit['gradient_norm_after_clip'],audit['clip_max_norm']+1e-5)
        self.assertEqual(len(frame),5)

    def test_13_advanced_resume(self):
        with tempfile.TemporaryDirectory() as td:
            report,history=advanced3.run(output_dir=td)
            self.assertLessEqual(report['max_parameter_difference'],1e-7)
            self.assertLessEqual(report['max_history_difference'],1e-7)
            self.assertEqual(len(history),24)
            state=torch.load(Path(td)/'checkpoint.pt',weights_only=True,map_location='cpu')
            self.assertEqual(state['epoch'],5)
            self.assertIn('optimizer',state)
            self.assertIn('scheduler',state)

    def test_14_professional_training(self):
        with tempfile.TemporaryDirectory() as td:
            report,candidates,pred=professional.run(output_dir=td)
            self.assertEqual(report['split_sizes'],{'train':512,'validation':128,'test':128})
            self.assertEqual(len(pred),128)
            self.assertTrue((pred.site_id=='S06').all())
            self.assertEqual(set(candidates.model),{'linear','mlp'})
            self.assertTrue(candidates.validation_f2.between(0,1).all())
            self.assertFalse(report['post_inspection_used_as_feature'])
            self.assertTrue(report['test_capacity_ok'])
            for fname in ['candidate_scores.csv','training_history.csv','test_predictions.csv',
                          'evaluation.json','metadata.json','model_weights.pt']:
                self.assertTrue((Path(td)/fname).exists(),fname)
            meta=json.loads((Path(td)/'metadata.json').read_text())
            self.assertEqual(meta['features'],professional.FEATURES)
            self.assertNotIn('post_inspection_result',meta['features'])
            self.assertEqual(len(meta['train_mean']),6)

    def test_15_professional_validation_errors(self):
        df=pd.read_csv(ROOT/'data/fleet_events.csv')
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'bad.csv'
            bad=df.copy();bad.loc[1,'event_id']=bad.loc[0,'event_id']
            bad.to_csv(path,index=False)
            with self.assertRaises(ValueError):professional.validate_source(path)
            bad=df.drop(columns=['vibration']);bad.to_csv(path,index=False)
            with self.assertRaises(ValueError):professional.validate_source(path)
            bad=df.copy();bad.loc[1,'vibration']=np.inf;bad.to_csv(path,index=False)
            with self.assertRaises(ValueError):professional.validate_source(path)

    def test_16_professional_threshold_capacity(self):
        true=np.array([1,0,1,0,0,1,0,0,0,1])
        prob=np.array([.92,.85,.78,.75,.65,.45,.4,.3,.2,.1])
        weeks=np.array([1]*5+[2]*5)
        chosen=professional.select_threshold(true,prob,weeks,max_review_fraction=.2)
        flags=prob>=chosen['threshold']
        feasible,_=professional.capacity_check(weeks,flags,.2)
        self.assertTrue(feasible)
        self.assertTrue(0<=chosen['validation_f2']<=1)

    def test_17_examples_execute(self):
        for path in sorted((ROOT/'examples').glob('*.py')):
            with self.subTest(example=path.name):
                ast.parse(path.read_text(encoding='utf-8'))
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    runpy.run_path(str(path),run_name='__main__')
                self.assertTrue(output.getvalue().strip())

    def test_18_notebook_code_cells(self):
        path=ROOT/'notebooks/Chapter_07_Model_Training_and_Optimization.ipynb'
        notebook=nbformat.read(path,as_version=4)
        nbformat.validate(notebook)
        cells=[cell for cell in notebook.cells if cell.cell_type=='code']
        self.assertEqual(len(cells),15)
        namespace={'__name__':'__main__'}
        for i,cell in enumerate(cells):
            with self.subTest(code_cell=i):
                with contextlib.redirect_stdout(io.StringIO()):
                    exec(compile(cell.source,f'notebook_cell_{i}','exec'),namespace)

    def test_19_syntax_and_starter_separation(self):
        scripts=[*ROOT.glob('examples/*.py'),*ROOT.glob('exercises/*.py'),
                 *ROOT.glob('projects/*/starter.py'),*ROOT.glob('solutions/*.py'),
                 *ROOT.glob('scripts/*.py'),*ROOT.glob('tests/*.py')]
        for path in scripts:
            with self.subTest(script=path.name):ast.parse(path.read_text(encoding='utf-8'))
        starters=list(ROOT.glob('projects/*/starter.py'))
        self.assertEqual(len(starters),6)
        self.assertEqual(len(list(ROOT.glob('exercises/*.py'))),6)
        self.assertFalse(list(ROOT.glob('solutions/*_v[0-9]*.py')))  # no duplicated version copies
        for path in starters:
            self.assertIn('TODO',path.read_text(encoding='utf-8'))
            self.assertIn('NotImplementedError',path.read_text(encoding='utf-8'))
        for path in ROOT.glob('solutions/*.py'):
            self.assertNotIn('raise NotImplementedError',path.read_text(encoding='utf-8'))

    def test_20_markdown_links_figures_and_anchors(self):
        markdown_files=list(ROOT.rglob('*.md'))
        self.assertGreaterEqual(len(markdown_files),9)
        for path in markdown_files:
            content=path.read_text(encoding='utf-8')
            for dest in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)|!\[[^\]]*\]\(([^)]+)\)',content):
                rel=next((x for x in dest if x),'')
                if not rel or rel.startswith(('https://','http://','mailto:','#')):continue
                filepart,_,anchor=rel.partition('#')
                target=(path.parent/filepart).resolve()
                with self.subTest(markdown=str(path.relative_to(ROOT)),link=rel):
                    # 상위 AI 목차와 Chapter 06은 ZIP 바깥에 있음.
                    if target.is_relative_to(ROOT):
                        self.assertTrue(target.is_file())
                        if anchor:
                            t=target.read_text(encoding='utf-8')
                            self.assertTrue(f'id="{anchor}"' in t or f'#{anchor}' in t,
                                            f'Unknown anchor: {anchor}')
        self.assertEqual(len(list((ROOT/'figures').glob('*.png'))),6)

if __name__=='__main__':
    unittest.main()
