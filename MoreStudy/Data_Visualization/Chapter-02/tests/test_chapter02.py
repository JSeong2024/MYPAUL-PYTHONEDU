"""Run: python -m unittest discover -s tests -v (from Chapter-02)."""
import json
import tempfile
import unittest
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project.chart_design import (  # noqa: E402
    load_visits, branch_summary, completeness, make_charts, make_report,
    EXPECTED_BRANCHES,
)


class TestLibraryVisualization(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = ROOT / 'data' / 'library_visits.csv'
        cls.frame = load_visits(cls.data)

    def write_bad(self, df, directory):
        path = Path(directory) / 'bad.csv'
        df.to_csv(path, index=False)
        return path

    def test_01_observed_rows(self):
        self.assertEqual(len(self.frame), 55)

    def test_02_schema(self):
        self.assertEqual(list(self.frame), ['date', 'branch', 'visitors', 'new_members', 'event_day'])

    def test_03_branches(self):
        self.assertEqual(set(self.frame.branch), set(EXPECTED_BRANCHES))

    def test_04_date_window(self):
        self.assertEqual(self.frame.date.min(), pd.Timestamp('2026-10-01'))
        self.assertEqual(self.frame.date.max(), pd.Timestamp('2026-10-14'))

    def test_05_visitors_total(self):
        self.assertEqual(int(self.frame.visitors.sum()), 9165)

    def test_06_members_total(self):
        self.assertEqual(int(self.frame.new_members.sum()), 1086)

    def test_07_valid_relation(self):
        self.assertTrue(self.frame.new_members.le(self.frame.visitors).all())

    def test_08_unique_grain(self):
        self.assertFalse(self.frame.duplicated(['date','branch']).any())

    def test_09_expected_grid(self):
        self.assertEqual(len(completeness(self.frame)), 56)

    def test_10_one_missing(self):
        self.assertEqual(int((~completeness(self.frame).observed).sum()), 1)

    def test_11_missing_is_not_zero(self):
        missing = completeness(self.frame).query('not observed')
        self.assertTrue(missing['visitors'].isna().all())
        self.assertEqual(missing['date'].iloc[0], pd.Timestamp('2026-10-07'))
        self.assertEqual(missing['branch'].iloc[0], 'Eastgate')

    def test_12_summary_order(self):
        self.assertEqual(branch_summary(self.frame).branch.tolist(),
                         ['Central', 'Riverside', 'Hilltop', 'Eastgate'])

    def test_13_totals_by_branch(self):
        totals = dict(zip(branch_summary(self.frame).branch,branch_summary(self.frame).visitors))
        self.assertEqual(totals, {'Central':3435,'Riverside':2539,'Hilltop':1900,'Eastgate':1291})

    def test_14_observed_days(self):
        days = branch_summary(self.frame).set_index('branch').observed_days
        self.assertEqual(days.loc['Eastgate'], 13)
        self.assertEqual(days.loc['Central'], 14)

    def test_15_rates_sum_then_divide(self):
        summary = branch_summary(self.frame).set_index('branch')
        for row in summary.itertuples():
            self.assertAlmostEqual(row.signup_rate_pct, row.new_members/row.visitors*100)

    def test_16_reject_duplicate_key(self):
        with tempfile.TemporaryDirectory() as t:
            bad = pd.concat([pd.read_csv(self.data), pd.read_csv(self.data).iloc[[0]]], ignore_index=True)
            with self.assertRaises(ValueError): load_visits(self.write_bad(bad, t))

    def test_17_reject_unknown_branch(self):
        with tempfile.TemporaryDirectory() as t:
            bad = pd.read_csv(self.data)
            bad.loc[0,'branch']='Unknown'
            with self.assertRaises(ValueError): load_visits(self.write_bad(bad,t))

    def test_18_reject_negative(self):
        with tempfile.TemporaryDirectory() as t:
            bad=pd.read_csv(self.data)
            bad.loc[0,'visitors']=-1
            with self.assertRaises(ValueError): load_visits(self.write_bad(bad,t))

    def test_19_reject_overcounted_members(self):
        with tempfile.TemporaryDirectory() as t:
            bad=pd.read_csv(self.data)
            bad.loc[0,'new_members']=99999
            with self.assertRaises(ValueError): load_visits(self.write_bad(bad,t))

    def test_20_reject_bad_schema(self):
        with tempfile.TemporaryDirectory() as t:
            bad=pd.read_csv(self.data).rename(columns={'visitors':'persons'})
            with self.assertRaises(ValueError): load_visits(self.write_bad(bad,t))

    def test_21_reject_bad_date(self):
        with tempfile.TemporaryDirectory() as t:
            bad=pd.read_csv(self.data)
            bad.loc[0,'date']='2026-11-02'
            with self.assertRaises(ValueError): load_visits(self.write_bad(bad,t))

    def test_22_reject_missing_cell(self):
        with tempfile.TemporaryDirectory() as t:
            bad=pd.read_csv(self.data)
            bad.loc[0,'visitors']=None
            with self.assertRaises(ValueError): load_visits(self.write_bad(bad,t))

    def test_23_chart_files(self):
        with tempfile.TemporaryDirectory() as t:
            paths=make_charts(self.frame,Path(t))
            self.assertEqual(len(paths),5)
            for p in paths:
                self.assertTrue(p.exists())
                self.assertGreater(p.stat().st_size,3000)
                self.assertEqual(p.read_bytes()[:8],b'\x89PNG\r\n\x1a\n')

    def test_24_report_files(self):
        with tempfile.TemporaryDirectory() as t:
            meta=make_report(self.frame,Path(t))
            self.assertEqual(meta['missing_records'],1)
            self.assertEqual(meta['expected_rows'],56)
            self.assertEqual(meta['total_visitors'],9165)
            self.assertEqual(meta['total_new_members'],1086)
            self.assertEqual(json.loads((Path(t)/'report.json').read_text())['source_rows'],55)
            self.assertTrue((Path(t)/'branch_summary.csv').exists())
            self.assertEqual(len(pd.read_csv(Path(t)/'missing_dates.csv')),1)

    def test_25_solution_scripts(self):
        import subprocess
        with tempfile.TemporaryDirectory() as t:
            for solution in sorted((ROOT / 'solutions').glob('*.py')):
                completed = subprocess.run([sys.executable, str(solution)], cwd=t,
                                           capture_output=True, text=True, check=True)
                self.assertTrue(completed.stdout.strip(), solution.name)

    def test_26_small_multiples_coverage(self):
        import importlib.util
        script = ROOT / 'solutions' / '05_small_multiples.py'
        spec=importlib.util.spec_from_file_location('solution05',script)
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as t:
            counts=module.solve(Path(t)/'chart.png')
            self.assertEqual(counts['Eastgate'],13)
            self.assertEqual(counts['Central'],14)
            self.assertTrue((Path(t)/'chart.png').exists())


if __name__ == '__main__':
    unittest.main()
