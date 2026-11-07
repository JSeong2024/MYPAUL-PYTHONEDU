"""Chapter 05 — EDA & Statistical Visualization validation.
Run from Chapter-05/: python -m unittest discover -s tests -v
"""
import ast
import json
from pathlib import Path
import sys
import tempfile
import unittest
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from project_utils.eda import (valid_deliveries,valid_response_times,validated_inspections,
                               bootstrap_mean_ci,wilson_interval)

class TestDataAndEDA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.shipping=pd.read_csv(ROOT/'data/shipments.csv')
        cls.support=pd.read_csv(ROOT/'data/support_tickets.csv')
        cls.quality=pd.read_csv(ROOT/'data/inspections.csv')
        cls.simpson=pd.read_csv(ROOT/'data/simpson_delivery.csv')

    def test_dataset_sizes(self):
        self.assertEqual((len(self.shipping),len(self.support),len(self.quality),len(self.simpson)),(600,540,700,210))

    def test_delivery_valid_count(self):
        self.assertEqual(len(valid_deliveries(self.shipping)),573)

    def test_deliveries_have_nonnegative_durations(self):
        v=valid_deliveries(self.shipping)
        self.assertTrue(v.actual_days.ge(0).all())
        self.assertTrue(v.status.eq('delivered').all())

    def test_delivery_on_time_rate(self):
        self.assertAlmostEqual(valid_deliveries(self.shipping).on_time.mean(),.4973821989528796)

    def test_delivery_rejects_duplicate_id(self):
        bad=pd.concat([self.shipping,self.shipping.iloc[:1]],ignore_index=True)
        with self.assertRaises(ValueError): valid_deliveries(bad)

    def test_delivery_requires_columns(self):
        with self.assertRaises(ValueError):valid_deliveries(self.shipping.drop(columns='actual_days'))

    def test_support_valid_count(self):
        self.assertEqual(len(valid_response_times(self.support)),529)

    def test_support_negative_rejected(self):
        f=self.support.iloc[:2].copy();f.loc[f.index[0],'first_response_min']=-1
        self.assertEqual(len(valid_response_times(f)),1)

    def test_support_rejects_duplicate_id(self):
        with self.assertRaises(ValueError):valid_response_times(pd.concat([self.support,self.support.iloc[:1]],ignore_index=True))

    def test_inspections_duplicates(self):
        cleaned,dups=validated_inspections(self.quality)
        self.assertEqual((len(cleaned),dups),(696,4))

    def test_inspections_measurement_review(self):
        cleaned,_=validated_inspections(self.quality)
        self.assertEqual(int(cleaned.measurement_review.sum()),11)

    def test_inspections_invalid_outcome(self):
        f=self.quality.iloc[:2].copy();f.loc[f.index[0],'is_defective']=4
        with self.assertRaises(ValueError):validated_inspections(f)

    def test_inspections_missing_column(self):
        with self.assertRaises(ValueError):validated_inspections(self.quality.drop(columns='line'))

    def test_simpson_pooled_reverse(self):
        pooled=self.simpson.groupby('carrier').on_time.mean()
        self.assertLess(pooled['A'],pooled['B'])

    def test_simpson_within_groups(self):
        grouped=self.simpson.groupby(['zone','carrier']).on_time.mean()
        for zone in ['Urban','Remote']:
            self.assertGreater(grouped.loc[zone,'A'],grouped.loc[zone,'B'])

    def test_simpson_exact_rates(self):
        g=self.simpson.groupby(['zone','carrier']).on_time.mean()
        self.assertAlmostEqual(g.loc['Urban','A'],.95)
        self.assertAlmostEqual(g.loc['Remote','B'],.60)

    def test_bootstrap_repeatable(self):
        a=bootstrap_mean_ci([2,3,5,7,11],seed=77)
        self.assertEqual(a,bootstrap_mean_ci([2,3,5,7,11],seed=77))

    def test_bootstrap_bounds(self):
        low,high=bootstrap_mean_ci([2,3,5,7,11],seed=71)
        self.assertLess(low,high)
        self.assertGreater(low,1.0)

    def test_bootstrap_small_sample(self):
        self.assertTrue(np.isnan(bootstrap_mean_ci([1])[0]))

    def test_bootstrap_invalid_confidence(self):
        with self.assertRaises(ValueError):bootstrap_mean_ci([1,2,3],confidence=1.2)

    def test_wilson_order_and_sample_size(self):
        lo1,hi1=wilson_interval(1,10)
        lo2,hi2=wilson_interval(100,1000)
        self.assertLess(lo1,.1);self.assertGreater(hi1,.1)
        self.assertGreater(hi1-lo1,hi2-lo2)

    def test_wilson_invalid(self):
        with self.assertRaises(ValueError):wilson_interval(3,2)

    def test_wilson_zero_n(self):
        self.assertTrue(np.isnan(wilson_interval(0,0)[0]))

    def test_data_dictionary_exists(self):
        self.assertTrue((ROOT/'data/DATA_DICTIONARY.md').exists())

    def test_readme_quiz_count(self):
        text=(ROOT/'README.md').read_text(encoding='utf-8')
        self.assertEqual(sum(line.startswith('### Q') for line in text.splitlines()),22)
        self.assertEqual(text.count('정답 및 해설 확인'),22)

    def test_readme_section_count(self):
        text=(ROOT/'README.md').read_text(encoding='utf-8')
        self.assertEqual(sum(line.startswith('## 5.') for line in text.splitlines()),30)

    def test_figures_present(self):
        self.assertEqual(len(list((ROOT/'figures').glob('*.png'))),25)
        self.assertEqual(len(list((ROOT/'figures/quiz').glob('*.png'))),6)

    def test_no_markdown_control_characters(self):
        text=(ROOT/'README.md').read_text(encoding='utf-8')
        self.assertFalse(any(ord(c)<32 and c not in '\t\n' for c in text))

class TestProjects(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # import paths are safe: filenames are not user-provided and scripts do not run on import.
        import importlib.util
        cls.modules={}
        files={
            'mini1':ROOT/'solutions/mini_01_delivery/solution.py',
            'mini2':ROOT/'solutions/mini_02_support/solution.py',
            'mini3':ROOT/'solutions/mini_03_quality/solution.py',
            'advanced':ROOT/'solutions/advanced_01_quality/reference_solution.py'
        }
        for name,path in files.items():
            spec=importlib.util.spec_from_file_location('dv05_'+name,path)
            mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
            cls.modules[name]=mod

    def test_mini_01_files_and_numbers(self):
        with tempfile.TemporaryDirectory() as tmp:
            result=self.modules['mini1'].run(output=tmp)
            self.assertEqual(result['valid_count'],573)
            self.assertEqual(result['excluded_count'],27)
            self.assertTrue((Path(tmp)/'report.png').is_file())
            self.assertEqual(len(pd.read_csv(Path(tmp)/'zone_summary.csv')),3)

    def test_mini_02_files_and_numbers(self):
        with tempfile.TemporaryDirectory() as tmp:
            result=self.modules['mini2'].run(output=tmp)
            self.assertEqual(result['valid_count'],529)
            self.assertTrue((Path(tmp)/'report.png').is_file())
            self.assertEqual(len(pd.read_csv(Path(tmp)/'priority_summary.csv')),3)

    def test_mini_03_files_and_numbers(self):
        with tempfile.TemporaryDirectory() as tmp:
            result=self.modules['mini3'].run(output=tmp)
            self.assertEqual(result['duplicate_count'],4)
            self.assertEqual(result['measurement_review_count'],11)
            self.assertTrue((Path(tmp)/'report.png').is_file())

    def test_advanced_all_plants(self):
        with tempfile.TemporaryDirectory() as tmp:
            result=self.modules['advanced'].run(output=tmp)
            self.assertEqual(result['selected_rows'],696)
            self.assertEqual(len(result['plants']),3)
            self.assertTrue((Path(tmp)/'Plant-A.png').is_file())
            self.assertEqual(len(pd.read_csv(Path(tmp)/'line_summary.csv')),6)

    def test_advanced_select_one(self):
        with tempfile.TemporaryDirectory() as tmp:
            result=self.modules['advanced'].run(output=tmp,plants=['Plant-B'])
            self.assertEqual(result['selected_plants'],['Plant-B'])
            self.assertTrue((Path(tmp)/'Plant-B.png').exists())
            self.assertFalse((Path(tmp)/'Plant-A.png').exists())
            self.assertEqual(len(pd.read_csv(Path(tmp)/'line_summary.csv')),2)

    def test_advanced_bad_plant(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):self.modules['advanced'].run(output=tmp,plants=['NO-SUCH-PLANT'])

    def test_advanced_bad_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):self.modules['advanced'].run(output=tmp,source=Path(tmp)/'nonexistent.csv')

    def test_advanced_summary_rate(self):
        df,_=validated_inspections(pd.read_csv(ROOT/'data/inspections.csv'))
        result=self.modules['advanced'].summarize(df)
        self.assertTrue(result.defect_rate.between(0,1).all())
        self.assertTrue((result.rate_ci_low<=result.defect_rate).all())
        self.assertTrue((result.defect_rate<=result.rate_ci_high).all())

# Syntax checks are lightweight and catch broken code snippets without executing student starters.
def _syntax_test(path):
    def check(self):
        ast.parse(path.read_text(encoding='utf-8'),filename=str(path))
    return check

for path in sorted((ROOT/'examples').glob('*.py')):
    setattr(TestDataAndEDA,'test_syntax_example_'+path.stem,_syntax_test(path))
for path in sorted((ROOT/'solutions').glob('??_*.py')):
    setattr(TestDataAndEDA,'test_syntax_solution_'+path.stem,_syntax_test(path))

if __name__=='__main__':unittest.main()
