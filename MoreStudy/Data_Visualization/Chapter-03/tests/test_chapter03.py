"""Regression tests for Chapter 03's five runnable reference projects."""
from pathlib import Path
import importlib.util
import tempfile
import unittest
import json
import sys
import csv
import re

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

def load(name,rel):
    spec=importlib.util.spec_from_file_location(name,ROOT/rel)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

W=load('mini_weather','solutions/mini_projects/mini_01_weather/reference_solution.py')
S=load('mini_sales','solutions/mini_projects/mini_02_sales/reference_solution.py')
M=load('mini_server','solutions/mini_projects/mini_03_server/reference_solution.py')
A=load('advanced_weather','solutions/advanced_projects/advanced_01_weather/reference_solution.py')
U=load('advanced_subway','solutions/advanced_projects/advanced_02_subway/reference_solution.py')

class TestChapter03(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.w=W.load_weather();cls.sales=S.load_data();cls.server=M.load_data()
        cls.aw=A.load_data();cls.raw,cls.catalog=U.load_data();cls.good,cls.bad=U.validate_rows(cls.raw)

    def test_01_weather_expected(self):self.assertEqual(W.summarize(self.w)['expected_rows'],42)
    def test_02_weather_observed(self):self.assertEqual(W.summarize(self.w)['observed_rows'],41)
    def test_03_weather_valid(self):self.assertEqual(W.summarize(self.w)['temperature_valid_rows'],40)
    def test_04_weather_missing(self):self.assertEqual(W.summarize(self.w)['missing_rows'],1)
    def test_05_weather_missing_value(self):self.assertEqual(W.summarize(self.w)['missing_temperature_cells'],1)
    def test_06_weather_panels(self):
        fig=W.build_figure(self.w)
        self.assertEqual(len(fig.axes),4)
        plt.close(fig)
    def test_07_weather_duplicate_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'dupe.csv'
            pd.concat([self.w,self.w.iloc[[0]]]).to_csv(p,index=False)
            with self.assertRaisesRegex(ValueError,'Duplicate'):W.load_weather(p)
    def test_08_weather_unknown_region_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.csv';temp=self.w.copy();temp.loc[0,'region']='Mars';temp.to_csv(p,index=False)
            with self.assertRaisesRegex(ValueError,'Unknown'):W.load_weather(p)
    def test_09_sales_row_count(self):self.assertEqual(len(self.sales),336)
    def test_10_sales_total(self):self.assertEqual(int(self.sales['revenue_krw'].sum()),19281100)
    def test_11_sales_date_count(self):self.assertEqual(self.sales['date'].nunique(),28)
    def test_12_sales_store_count(self):self.assertEqual(self.sales['store'].nunique(),3)
    def test_13_sales_duplicate_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.csv';pd.concat([self.sales,self.sales.iloc[[0]]]).to_csv(p,index=False)
            with self.assertRaisesRegex(ValueError,'Duplicate'):S.load_data(p)
    def test_14_sales_negative_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.csv';t=self.sales.copy();t.loc[0,'revenue_krw']=-1;t.to_csv(p,index=False)
            with self.assertRaisesRegex(ValueError,'Invalid'):S.load_data(p)
    def test_15_sales_report_saves_files(self):
        with tempfile.TemporaryDirectory() as d:
            report=S.make_report(self.sales,Path(d))
            self.assertEqual(report['total_revenue_krw'],19281100)
            self.assertTrue((Path(d)/'store_sales_report.png').is_file())
            self.assertEqual(json.loads((Path(d)/'sales_summary.json').read_text())['days'],28)
    def test_16_server_observed(self):self.assertEqual(len(self.server),213)
    def test_17_server_gap(self):
        self.assertEqual(72*3-len(self.server),3)
    def test_18_server_null(self):self.assertEqual(int(self.server['response_ms'].isna().sum()),1)
    def test_19_server_high_cpu_event(self):self.assertGreaterEqual(int(self.server['cpu_pct'].gt(85).sum()),2)
    def test_20_server_duplicate_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'dupe.csv';pd.concat([self.server,self.server.iloc[[0]]]).to_csv(p,index=False)
            with self.assertRaisesRegex(ValueError,'Duplicate'):M.load_data(p)
    def test_21_server_report(self):
        with tempfile.TemporaryDirectory() as d:
            summary=M.make_report(self.server,Path(d))
            self.assertEqual(summary['expected_slots'],216)
            self.assertTrue((Path(d)/'server_performance.png').is_file())
    def test_22_aw_observed(self):self.assertEqual(len(self.aw),145)
    def test_23_aw_missing_temp(self):self.assertEqual(int(self.aw['temperature_c'].isna().sum()),1)
    def test_24_aw_duplicate_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.csv';pd.concat([self.aw,self.aw.iloc[[0]]]).to_csv(p,index=False)
            with self.assertRaisesRegex(ValueError,'Duplicate'):A.load_data(p)
    def test_25_aw_bad_precip(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.csv';t=self.aw.copy();t.loc[0,'precipitation_mm']=-1;t.to_csv(p,index=False)
            with self.assertRaisesRegex(ValueError,'Invalid'):A.load_data(p)
    def test_26_aw_full_report(self):
        with tempfile.TemporaryDirectory() as d:
            summary=A.make_report(self.aw,Path(d))
            self.assertEqual(summary['stations'],5)
            self.assertEqual(summary['expected_slots'],150)
            self.assertEqual(summary['valid_temperature_rows'],144)
            self.assertTrue((Path(d)/'dynamic_station_panels.png').is_file())
    def test_27_aw_single_station(self):
        with tempfile.TemporaryDirectory() as d:
            res=A.make_report(self.aw,Path(d),['WX-01'])
            self.assertEqual(res['stations'],1)
            self.assertEqual(res['expected_slots'],30)
    def test_28_aw_three_stations(self):
        with tempfile.TemporaryDirectory() as d:
            res=A.make_report(self.aw,Path(d),['WX-01','WX-02','WX-05'])
            self.assertEqual(res['stations'],3)
            self.assertTrue((Path(d)/'coverage_by_station.png').exists())
    def test_29_aw_bad_selected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError,'Unknown'):A.make_report(self.aw,Path(d),['X'])
    def test_30_subway_catalog(self):self.assertEqual(len(self.catalog),8)
    def test_31_subway_original(self):self.assertEqual(len(self.raw),4251)
    def test_32_subway_valid(self):self.assertEqual(len(self.good),4246)
    def test_33_subway_invalid(self):self.assertEqual(len(self.bad),5)
    def test_34_subway_reasons(self):
        self.assertEqual(self.bad['reason'].str.contains('duplicate_slot').sum(),2)
        self.assertEqual(self.bad['reason'].str.contains('invalid_count').sum(),2)
        self.assertEqual(self.bad['reason'].str.contains('negative_count').sum(),1)
    def test_35_subway_no_duplicate_slots(self):self.assertFalse(self.good[['station_id','date','hour']].duplicated().any())
    def test_36_subway_positive_counts(self):self.assertTrue((self.good[['boardings','alightings']]>=0).all().all())
    def test_37_subway_boardings(self):self.assertEqual(int(self.good['boardings'].sum()),1536856)
    def test_38_subway_alightings(self):self.assertEqual(int(self.good['alightings'].sum()),1642122)
    def test_39_subway_grid(self):
        full,summary=U.build_summaries(self.good,self.catalog,self.good['date'].min(),self.good['date'].max())
        self.assertEqual(len(full),4256)
        self.assertEqual(int(full['total'].isna().sum()),10)
    def test_40_subway_unknown_station_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.csv';s=self.raw.copy();s.loc[0,'station_id']='N/A';s.to_csv(p,index=False)
            with self.assertRaisesRegex(ValueError,'Unknown'):U.load_data(p,ROOT/'data'/'subway_stations.csv')
    def test_41_subway_dup_catalog_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            cat=Path(d)/'stations.csv'
            pd.concat([self.catalog,self.catalog.iloc[[0]]]).to_csv(cat,index=False)
            with self.assertRaisesRegex(ValueError,'Duplicate'):U.load_data(ROOT/'data'/'subway_ridership.csv',cat)
    def test_42_subway_report_output(self):
        with tempfile.TemporaryDirectory() as d:
            result=U.make_report(self.raw,self.catalog,Path(d),['S01','S03','S07'])
            self.assertEqual(result['accepted_rows'],4246)
            self.assertEqual(result['expected_slots'],4256)
            self.assertTrue((Path(d)/'05_coverage_map.png').is_file())
            self.assertEqual(len(list(Path(d).glob('*.png'))),5)
    def test_43_subway_unknown_selection(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError,'Invalid station'):U.make_report(self.raw,self.catalog,Path(d),['NOT-A-STATION'])
    def test_44_readme_prereq(self):
        readme=(ROOT/'README.md').read_text(encoding='utf-8')
        self.assertIn('<summary><strong>선행 학습 목록</strong></summary>',readme)
    def test_45_readme_has_quiz_18(self):
        readme=(ROOT/'README.md').read_text(encoding='utf-8')
        self.assertEqual(readme.count('정답 및 해설 확인</strong></summary>'),18)
    def test_46_readme_avoids_unwanted_word(self):
        self.assertNotIn('실무',(ROOT/'README.md').read_text(encoding='utf-8'))
    def test_47_readme_local_links_resolve(self):
        text=(ROOT/'README.md').read_text(encoding='utf-8')
        for raw in re.findall(r'\]\(([^)]+)\)',text):
            if raw.startswith(('http://','https://','#','../')):continue
            target=raw.split('#',1)[0]
            if not target:continue
            with self.subTest(link=raw):self.assertTrue((ROOT/target).exists())
    def test_48_all_exercises_have_answers(self):
        for file in (ROOT/'exercises').glob('*.py'):
            with self.subTest(file=file.name):self.assertTrue((ROOT/'solutions/exercises'/file.name).is_file())
    def test_49_all_quiz_images_exist(self):
        for name in ['Q05_bar_and_barh.png','Q06_lines_styles.png','Q07_histogram_edges.png','Q08_axes_positions.png','Q09_missing_vs_zero.png']:
            with self.subTest(name=name):self.assertTrue((ROOT/'figures/quiz'/name).is_file())
    def test_50_reference_project_scripts(self):
        for key in ['mini_01_weather','mini_02_sales','mini_03_server']:
            with self.subTest(key=key):self.assertTrue((ROOT/'solutions/mini_projects'/key/'reference_solution.py').is_file())
        for key in ['advanced_01_weather','advanced_02_subway']:
            with self.subTest(key=key):self.assertTrue((ROOT/'solutions/advanced_projects'/key/'reference_solution.py').is_file())

if __name__=='__main__':unittest.main()
