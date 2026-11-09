"""Chapter 06 코드, 데이터, Notebook, 링크 검증."""
from __future__ import annotations
import ast
import contextlib
import io
import json
from pathlib import Path
import re
import runpy
import sys
import tempfile
import unittest

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from torch import nn

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
torch.set_num_threads(1)

from solutions import mini_01_xor_network as mini1
from solutions import mini_02_nonlinear_regression as mini2
from solutions import advanced_01_architecture_audit as adv1
from solutions import advanced_02_model_handoff as adv2
from solutions import practice_01_linear_forward as p1
from solutions import practice_02_parameters as p2
from solutions import practice_03_activation as p3
from solutions import practice_04_logit_predictions as p4
from solutions import practice_05_gradient_step as p5


class Chapter06Tests(unittest.TestCase):
    def test_01_data_files_and_labels(self):
        a=pd.read_csv(ROOT/'data/xor_signals.csv')
        b=pd.read_csv(ROOT/'data/nonlinear_demand.csv')
        c=pd.read_csv(ROOT/'data/triage_signals.csv')
        self.assertEqual((len(a),len(b),len(c)),(256,300,360))
        self.assertEqual(a.label.value_counts().to_dict(),{0:128,1:128})
        self.assertTrue((a.label==( (a.signal_x>0) != (a.signal_y>0)).astype(int)).all())
        self.assertEqual(set(c.class_id),{0,1,2})
        for data in (a,b,c):self.assertFalse(data.isna().any().any())

    def test_02_practice_linear_forward(self):
        x=torch.tensor([[1.,2.],[3.,4.]])
        w=torch.tensor([[2.,3.],[-1.,1.]])
        b=torch.tensor([.5,1.])
        self.assertTrue(torch.allclose(p1.linear_forward(x,w,b),x@w.T+b))
        with self.assertRaises(ValueError):p1.linear_forward(x,w,torch.tensor([1.]))

    def test_03_practice_parameter_count(self):
        model=nn.Sequential(nn.Linear(4,6),nn.ReLU(),nn.Linear(6,2))
        self.assertEqual(p2.parameter_count(model),44)
        for p in model[0].parameters():p.requires_grad_(False)
        self.assertEqual(p2.parameter_count(model),14)

    def test_04_practice_activation(self):
        x=torch.tensor([-2.,0.,3.])
        self.assertTrue(torch.equal(p3.hidden_activation(x),torch.tensor([0.,0.,3.])))
        self.assertTrue(torch.allclose(p3.hidden_activation(x,'tanh'),torch.tanh(x)))
        with self.assertRaises(ValueError):p3.hidden_activation(x,'bad')

    def test_05_practice_logits(self):
        logits=torch.tensor([[0.3,2.,-1.],[4.,2.,1.]])
        probs,labels=p4.multiclass_predictions(logits)
        self.assertEqual(labels.tolist(),[1,0])
        self.assertTrue(torch.allclose(probs.sum(1),torch.ones(2)))
        with self.assertRaises(ValueError):p4.multiclass_predictions(torch.zeros(4))

    def test_06_practice_gradient_step(self):
        model=nn.Linear(1,1)
        with torch.no_grad():model.weight.fill_(0);model.bias.fill_(0)
        before,after=p5.one_step(model,torch.tensor([[1.]]),torch.tensor([[2.]]),lr=.1)
        self.assertLess(after,before)
        with self.assertRaises(ValueError):p5.one_step(model,torch.tensor([[1.]]),torch.tensor([[2.]]),lr=0)

    def test_07_mini_01_xor_comparison(self):
        report,pred,hl,hm=mini1.run()
        self.assertEqual(len(pred),64)
        self.assertEqual(set(report.model),{'linear','mlp'})
        self.assertEqual(report.set_index('model').loc['linear','parameter_count'],3)
        self.assertLess(report.set_index('model').loc['linear','test_accuracy'],.8)
        self.assertGreater(report.set_index('model').loc['mlp','test_accuracy'],.90)
        self.assertGreater(hl[0],hl[-1])
        self.assertGreater(hm[0],hm[-1])
        self.assertTrue(((pred[['linear_probability','mlp_probability']] >= 0) & (pred[['linear_probability','mlp_probability']] <= 1)).all().all())

    def test_08_mini_01_invalid_data(self):
        with tempfile.TemporaryDirectory() as td:
            df=pd.read_csv(ROOT/'data/xor_signals.csv')
            df.loc[0,'signal_x']=np.nan
            p=Path(td)/'bad.csv';df.to_csv(p,index=False)
            with self.assertRaises(ValueError):mini1.run(p)

    def test_09_mini_02_regression(self):
        report,pred,hl,hm=mini2.run()
        self.assertEqual(len(pred),75)
        rmses=report.set_index('model')['test_rmse']
        self.assertLess(rmses['mlp'],rmses['linear'])
        self.assertLess(rmses['mlp'],.40)
        self.assertGreater(hl[0],hl[-1])
        self.assertGreater(hm[0],hm[-1])

    def test_10_advanced_01_architectures(self):
        report,m_small,m_large=adv1.run()
        self.assertEqual(report.parameter_count.tolist(),[83,323])
        self.assertTrue(report.validation_macro_f1.between(0,1).all())
        self.assertEqual(tuple(m_small(torch.zeros(2,6)).shape),(2,3))
        with self.assertRaises(ValueError):m_large(torch.zeros(2,5))

    def test_11_advanced_02_outputs_and_restore(self):
        with tempfile.TemporaryDirectory() as td:
            result,model,(mean,std),indices=adv2.run(output_dir=td)
            out=Path(td)
            for f in ['model_weights.pt','model_metadata.json','evaluation.json','predictions.csv']:
                self.assertTrue((out/f).is_file())
            metadata=json.loads((out/'model_metadata.json').read_text(encoding='utf-8'))
            self.assertEqual(metadata['features'],adv2.FEATURES)
            self.assertTrue(np.all(np.asarray(metadata['std'])>0))
            self.assertEqual((result['train_count'],result['validation_count'],result['test_count']),(216,72,72))
            df=pd.read_csv(ROOT/'data/triage_signals.csv')
            p=adv2.predict(model,df.iloc[indices][adv2.FEATURES],mean,std)
            self.assertEqual(p.shape,(72,3))
            self.assertTrue(np.allclose(p.sum(axis=1),1,atol=1e-6))
            self.assertGreater(result['test_macro_f1'],.60)

    def test_12_advanced_02_bad_schema(self):
        frame=pd.read_csv(ROOT/'data/triage_signals.csv')[adv2.FEATURES].head(4)
        with self.assertRaises(ValueError):adv2.validate_features(frame[adv2.FEATURES[::-1]])
        bad=frame.copy();bad.iloc[1,2]=np.inf
        with self.assertRaises(ValueError):adv2.validate_features(bad)

    def test_13_example_syntax_and_execution(self):
        for path in sorted((ROOT/'examples').glob('*.py')):
            with self.subTest(path=path.name):
                ast.parse(path.read_text(encoding='utf-8'))
                with contextlib.redirect_stdout(io.StringIO()) as capture:
                    runpy.run_path(str(path),run_name='__main__')
                self.assertTrue(capture.getvalue().strip())

    def test_14_student_starters_are_distinct(self):
        for path in list((ROOT/'exercises').glob('*.py'))+list((ROOT/'projects').glob('*/starter.py')):
            text=path.read_text(encoding='utf-8')
            ast.parse(text)
            self.assertIn('TODO',text)
            self.assertIn('NotImplementedError',text)
        self.assertEqual(len(list((ROOT/'exercises').glob('*.py'))),5)
        self.assertEqual(len(list((ROOT/'projects').glob('*/starter.py'))),4)

    def test_15_notebook_code_cells(self):
        import nbformat
        nb=nbformat.read(ROOT/'notebooks/Chapter_06_Neural_Networks_and_Deep_Learning.ipynb',as_version=4)
        nbformat.validate(nb)
        code_cells=[c for c in nb.cells if c.cell_type=='code']
        self.assertGreaterEqual(len(code_cells),10)
        namespace={'__name__':'__main__'}
        for i,cell in enumerate(code_cells,1):
            with self.subTest(cell=i):
                import warnings
                with contextlib.redirect_stdout(io.StringIO()), warnings.catch_warnings():
                    warnings.filterwarnings('ignore',message='FigureCanvasAgg is non-interactive')
                    exec(compile(cell.source,f'<notebook cell {i}>','exec'),namespace)
        plt.close('all')

    def test_16_figures_exist_and_valid(self):
        from PIL import Image
        for path in (ROOT/'figures').glob('*.png'):
            with Image.open(path) as im:
                self.assertGreater(im.width,350)
                self.assertGreater(im.height,200)
        self.assertEqual(len(list((ROOT/'figures').glob('*.png'))),4)

    def test_17_links_in_markdown(self):
        for path in ROOT.rglob('*.md'):
            text=path.read_text(encoding='utf-8')
            for dest in re.findall(r'\]\(([^)]+)\)',text):
                if dest.startswith(('https://','http://','#','mailto:')):continue
                dest=dest.split('#',1)[0]
                if not dest:continue
                if dest.startswith('../Chapter-05') or dest=='../README.md':continue
                resolved=(path.parent/dest).resolve()
                with self.subTest(doc=str(path.relative_to(ROOT)),link=dest):
                    self.assertTrue(resolved.exists(),f'Broken relative link: {resolved}')

    def test_18_quiz_has_answers(self):
        readme=(ROOT/'README.md').read_text(encoding='utf-8')
        self.assertEqual(len(re.findall(r'\*\*Q-\d{2}\.\*\*',readme)),14)
        self.assertEqual(readme.count('<details>'),14+5)
        self.assertEqual(readme.count('</details>'),14+5)

if __name__=='__main__':unittest.main()
