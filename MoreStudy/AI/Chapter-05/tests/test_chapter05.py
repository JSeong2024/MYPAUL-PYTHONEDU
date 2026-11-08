"""Chapter 05 예제·Practice·Project 자동 검사."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import os
import subprocess
import sys
import tempfile
import unittest

import pandas as pd
import torch

ROOT = Path(__file__).resolve().parents[1]
torch.set_num_threads(1)


def load_solution(filename):
    path = ROOT / 'solutions' / filename
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Chapter05Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.practice1 = load_solution('practice_01_tensor_shapes.py')
        cls.practice2 = load_solution('practice_02_broadcast_mask.py')
        cls.practice3 = load_solution('practice_03_autograd_derivative.py')
        cls.practice4 = load_solution('practice_04_batch_iteration.py')
        cls.mini1 = load_solution('mini_01_sensor_tensors.py')
        cls.mini2 = load_solution('mini_02_autograd_calibration.py')
        cls.adv1 = load_solution('advanced_01_custom_dataloader.py')
        cls.adv2 = load_solution('advanced_02_gradient_audit.py')

    def test_examples_run(self):
        import contextlib
        import io
        import runpy
        for path in sorted((ROOT / 'examples').glob('*.py')):
            with self.subTest(example=path.name):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    runpy.run_path(str(path), run_name='__main__')
                self.assertTrue(output.getvalue().strip())

    def test_practice_01(self):
        values = torch.tensor([[1, 2, 3], [3, 4, 5]])
        result = self.practice1.summarize(values)
        self.assertEqual(tuple(result.shape), (3,))
        self.assertEqual(result.dtype, torch.float32)
        self.assertTrue(torch.equal(result, torch.tensor([2., 3., 4.])))
        with self.assertRaises(ValueError):
            self.practice1.summarize(torch.zeros((0, 3)))

    def test_practice_02(self):
        original = torch.tensor([[3., -1., 8.]])
        calibrated, mask = self.practice2.calibrate(original, torch.tensor([1., 2., 3.]))
        self.assertEqual(calibrated.tolist(), [[4., 1., 11.]])
        self.assertEqual(mask.tolist(), [[True, False, True]])
        self.assertEqual(original.tolist(), [[3., -1., 8.]])
        with self.assertRaises(ValueError):
            self.practice2.calibrate(original, torch.tensor([1., 2.]))

    def test_practice_03(self):
        self.assertAlmostEqual(self.practice3.derivative_at(2), 14)
        self.assertAlmostEqual(self.practice3.derivative_at(-1), -4)

    def test_practice_04(self):
        self.assertEqual(self.practice4.batch_sizes(10, 4), [4, 4, 2])
        self.assertEqual(self.practice4.batch_sizes(0, 4), [])
        with self.assertRaises(ValueError):
            self.practice4.batch_sizes(10, 0)

    def test_mini_01(self):
        result = self.mini1.analyze_sensor_file(ROOT / 'data/sensor_readings.csv')
        self.assertEqual(result['sensor_id'].tolist(), self.mini1.SENSORS)
        self.assertEqual(result['valid_count'].tolist(), [20, 18, 20, 18])
        self.assertEqual(result['high_count'].tolist(), [0, 0, 7, 13])
        with tempfile.TemporaryDirectory() as temp:
            invalid = pd.read_csv(ROOT / 'data/sensor_readings.csv')
            invalid.loc[0, 'sensor_01'] = -2
            filename = Path(temp) / 'invalid.csv'
            invalid.to_csv(filename, index=False)
            with self.assertRaises(ValueError):
                self.mini1.analyze_sensor_file(filename)

    def test_mini_02(self):
        gradient, loss = self.mini2.one_gradient_step(ROOT / 'data/calibration_pairs.csv')
        self.assertEqual(gradient['parameter'].tolist(), ['w', 'b'])
        self.assertLess(loss.loc[0, 'loss_after'], loss.loc[0, 'loss_before'])
        for _, row in gradient.iterrows():
            self.assertAlmostEqual(row['after'], row['before'] - 0.03 * row['gradient'], places=10)
        self.assertAlmostEqual(float(loss.loc[0, 'loss_before']), 33.287099, delta=2e-6)
        with self.assertRaises(ValueError):
            self.mini2.one_gradient_step(ROOT / 'data/calibration_pairs.csv', -0.1)

    def test_advanced_01(self):
        dataset = self.adv1.FacilityEventDataset(ROOT / 'data/facility_events.csv')
        self.assertEqual(len(dataset), 48)
        sample, label, event_id = dataset[0]
        self.assertEqual(tuple(sample.shape), (3,))
        self.assertEqual(sample.dtype, torch.float32)
        self.assertEqual(label.dtype, torch.int64)
        self.assertEqual(event_id, 'EV001')
        summary, assignment = self.adv1.summarize_batches(ROOT / 'data/facility_events.csv')
        self.assertEqual(summary['sample_count'].tolist(), [7, 7, 7, 7, 7, 7, 6])
        self.assertEqual(assignment['event_id'].tolist(), dataset.event_ids)
        self.assertEqual(int(summary['alert_count'].sum()), int(dataset.labels.sum()))
        with self.assertRaises(ValueError):
            self.adv1.FacilityEventDataset(ROOT / 'data/facility_events_invalid.csv')

    def test_advanced_02(self):
        report = self.adv2.audit_gradients(ROOT / 'data/gradient_audit.csv')
        self.assertEqual(report['parameter'].tolist(), ['w', 'b'])
        self.assertTrue(report['pass'].all())
        self.assertTrue((report['relative_error'] < 1e-5).all())
        with self.assertRaises(ValueError):
            self.adv2.audit_gradients(ROOT / 'data/gradient_audit.csv', epsilon=0)

    def test_cli_project_outputs(self):
        environment = dict(os.environ, OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
        stems = {
            'mini_01_sensor_tensors.py': ['sensor_summary.csv'],
            'mini_02_autograd_calibration.py': ['gradient_report.csv', 'loss_report.csv'],
            'advanced_01_custom_dataloader.py': ['batch_summary.csv', 'event_assignments.csv'],
            'advanced_02_gradient_audit.py': ['gradient_audit_report.csv'],
        }
        with tempfile.TemporaryDirectory() as temp:
            for name, outputs in stems.items():
                with self.subTest(solution=name):
                    out = Path(temp) / name
                    result = subprocess.run([sys.executable, str(ROOT / 'solutions' / name), '--output-dir', str(out)],
                                            cwd=ROOT, text=True, capture_output=True, timeout=40, env=environment)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    for filename in outputs:
                        self.assertTrue((out / filename).is_file(), filename)
                        self.assertGreater(len(pd.read_csv(out / filename)), 0)

    def test_notebook_code_cells(self):
        import contextlib
        import io
        import json
        notebook = json.loads((ROOT / 'notebooks/Chapter_05_PyTorch_Fundamentals.ipynb').read_text(encoding='utf-8'))
        scope = {'__name__': '__main__'}
        executed = 0
        for index, cell in enumerate(notebook['cells']):
            if cell['cell_type'] != 'code':
                continue
            source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
            with contextlib.redirect_stdout(io.StringIO()):
                exec(compile(source, f'Notebook cell {index}', 'exec'), scope, scope)
            executed += 1
        self.assertEqual(executed, 11)

    def test_python_syntax(self):
        for path in ROOT.rglob('*.py'):
            if any(part in ('__pycache__', 'outputs') for part in path.parts):
                continue
            with self.subTest(file=path.relative_to(ROOT).as_posix()):
                compile(path.read_text(encoding='utf-8'), str(path), 'exec')

    def test_links_and_anchor_ids(self):
        import re
        # GitHub README 로컬 링크를 검사합니다. 외부 링크는 제외합니다.
        for doc in ROOT.rglob('*.md'):
            contents = doc.read_text(encoding='utf-8')
            for target in re.findall(r'\]\(([^\s)]+)\)', contents):
                if target.startswith(('http://', 'https://', '#', 'mailto:')):
                    continue
                relative = target.split('#', 1)[0]
                if relative:
                    target_path = (doc.parent / relative).resolve()
                    if target_path.is_relative_to(ROOT):
                        self.assertTrue(target_path.exists(), f'{doc}: {target}')
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        for n in range(1, 18):
            self.assertIn(f'<a id="section-5-{n}"></a>', readme)


if __name__ == '__main__':
    unittest.main(verbosity=2)
