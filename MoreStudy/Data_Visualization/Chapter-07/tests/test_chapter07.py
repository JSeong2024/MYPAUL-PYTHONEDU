"""Chapter 07: correctness, validation, reproducibility and UI configuration tests."""
import importlib.util
import json
import runpy
import tempfile
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'

from project_core.io import export_html
from solutions.mini_01_sales.solution import analyze_sales, make_figures as sales_figures, run as sales_run
from solutions.mini_02_service.solution import load_service, make_figure as service_figure, run as service_run
from solutions.mini_03_support.solution import load_tickets, make_figures as support_figures, run as support_run
from solutions.advanced_01_energy.reference_solution import (
    validate_energy, make_expected_grid, make_figure as energy_figure,
    summarize_grid, run as energy_run, VALID_REGIONS,
)


class TestData(unittest.TestCase):
    def test_sales_columns(self):
        self.assertTrue({'date','store','category','units','unit_price_krw','revenue_krw'}.issubset(pd.read_csv(DATA/'retail_sales.csv')))
    def test_sales_nonnegative(self):
        df=pd.read_csv(DATA/'retail_sales.csv');self.assertTrue((df.revenue_krw>=0).all())
    def test_sales_product(self):
        df=pd.read_csv(DATA/'retail_sales.csv');self.assertTrue((df.units*df.unit_price_krw ==df.revenue_krw).all())
    def test_sales_real_zero_exists(self):
        df=pd.read_csv(DATA/'retail_sales.csv');self.assertTrue((df.revenue_krw==0).any())
    def test_service_three(self):
        self.assertEqual(pd.read_csv(DATA/'service_metrics.csv').service.nunique(),3)
    def test_service_requests_positive(self):
        df=pd.read_csv(DATA/'service_metrics.csv');self.assertTrue((df.total_requests>0).all())
    def test_support_unique(self):
        self.assertFalse(pd.read_csv(DATA/'support_tickets.csv').ticket_id.duplicated().any())
    def test_support_status(self):
        self.assertEqual(set(pd.read_csv(DATA/'support_tickets.csv').status),{'Closed','Open'})
    def test_energy_bad_rows_exist(self):
        df=pd.read_csv(DATA/'regional_energy_hourly.csv');self.assertTrue((df.demand_kw=='sensor_error').any())
    def test_dictionary(self):
        self.assertIn('교육용 가상', (DATA/'DATA_DICTIONARY.md').read_text(encoding='utf-8'))

class TestMiniSales(unittest.TestCase):
    def test_total(self):
        store,date=analyze_sales();self.assertEqual(int(store.revenue_krw.sum()),32734600)
    def test_store_count(self):
        store,_=analyze_sales();self.assertEqual(len(store),4)
    def test_date_rows(self):
        _,date=analyze_sales();self.assertEqual(date.date.nunique(),61)
    def test_bar_type(self):
        bar,line=sales_figures(*analyze_sales());self.assertEqual(bar.data[0].type,'bar')
    def test_line_legend(self):
        _,line=sales_figures(*analyze_sales());self.assertEqual(len(line.data),4)
    def test_line_slider(self):
        _,line=sales_figures(*analyze_sales());self.assertTrue(line.layout.xaxis.rangeslider.visible)
    def test_negative_rejected(self):
        df=pd.read_csv(DATA/'retail_sales.csv');df.loc[0,'units']=-1
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'bad.csv';df.to_csv(p,index=False)
            with self.assertRaises(ValueError):analyze_sales(p)
    def test_mismatch_rejected(self):
        df=pd.read_csv(DATA/'retail_sales.csv');df.loc[0,'revenue_krw']=123
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'bad.csv';df.to_csv(p,index=False)
            with self.assertRaises(ValueError):analyze_sales(p)

class TestService(unittest.TestCase):
    def test_parse_utc(self):
        df=load_service();self.assertIsNotNone(df.timestamp_utc.dt.tz)
    def test_latency_positive(self):
        df=load_service();self.assertTrue((df.p95_latency_ms>0).all())
    def test_subplots(self):
        fig=service_figure(load_service());self.assertEqual(len(fig.data),6)
    def test_threshold(self):
        fig=service_figure(load_service());self.assertGreaterEqual(len(fig.layout.shapes),1)
    def test_no_p95_of_p95(self):
        self.assertTrue((load_service().columns=='p95_latency_ms').any())
    def test_invalid_threshold(self):
        with self.assertRaises(ValueError):service_figure(load_service(),-5)
    def test_duplicate_rejected(self):
        df=pd.read_csv(DATA/'service_metrics.csv');df=pd.concat([df,df.iloc[[0]]],ignore_index=True)
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'bad.csv';df.to_csv(p,index=False)
            with self.assertRaises(ValueError):load_service(p)
    def test_missing_gap_restored(self):
        fig=service_figure(load_service());
        self.assertTrue(any(any(pd.isna(y) for y in trace.y) for trace in fig.data))

class TestSupport(unittest.TestCase):
    def test_rows(self):self.assertEqual(len(load_tickets()),720)
    def test_box(self):
        box,hist=support_figures(load_tickets());self.assertTrue(all(t.type=='box' for t in box.data))
    def test_hist(self):
        box,hist=support_figures(load_tickets());self.assertTrue(all(t.type=='histogram' for t in hist.data))
    def test_duplicate_rejected(self):
        df=pd.read_csv(DATA/'support_tickets.csv');df=pd.concat([df,df.iloc[[0]]],ignore_index=True)
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'bad.csv';df.to_csv(p,index=False)
            with self.assertRaises(ValueError):load_tickets(p)
    def test_negative_rejected(self):
        df=pd.read_csv(DATA/'support_tickets.csv');df.loc[0,'first_response_min']=-1
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'bad.csv';df.to_csv(p,index=False)
            with self.assertRaises(ValueError):load_tickets(p)

class TestEnergy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid,cls.bad=validate_energy();cls.grid=make_expected_grid(cls.valid)
    def test_bad_count(self):self.assertGreaterEqual(len(self.bad),5)
    def test_duplicate_both_rejected(self):
        self.assertGreaterEqual(self.bad.reason.str.contains('duplicate_slot').sum(),2)
    def test_invalid_time_rejected(self):self.assertTrue(self.bad.reason.str.contains('invalid_time').any())
    def test_unknown_region_rejected(self):self.assertTrue(self.bad.reason.str.contains('unknown_region').any())
    def test_negative_rejected(self):self.assertTrue(self.bad.reason.str.contains('invalid_kw').any())
    def test_valid_nonnegative(self):self.assertTrue((self.valid.kw>=0).all())
    def test_unique_slot(self):self.assertFalse(self.valid.duplicated(['region','timestamp_local']).any())
    def test_timestamp_tz(self):self.assertIsNotNone(self.valid.timestamp_local.dt.tz)
    def test_grid_expected(self):self.assertEqual(len(self.grid),3360)
    def test_grid_real_gaps(self):self.assertTrue(self.grid.kw.isna().any())
    def test_grid_coverage(self):self.assertEqual(int(self.grid.observed.sum()),3336)
    def test_grid_does_not_zero_fill(self):self.assertTrue(self.grid.loc[~self.grid.observed,'kw'].isna().all())
    def test_one_region(self):
        g=make_expected_grid(self.valid,('North',));self.assertEqual(len(g),840)
    def test_invalid_region(self):
        with self.assertRaises(ValueError):make_expected_grid(self.valid,('Missing',))
    def test_duplicate_region(self):
        with self.assertRaises(ValueError):make_expected_grid(self.valid,('North','North'))
    def test_no_regions(self):
        with self.assertRaises(ValueError):make_expected_grid(self.valid,())
    def test_figure_dropdown(self):
        fig=energy_figure(self.grid);self.assertEqual(len(fig.layout.updatemenus[0].buttons),5)
    def test_figure_traces(self):
        fig=energy_figure(self.grid);self.assertEqual(len(fig.data),8)
    def test_figure_visible_length(self):
        fig=energy_figure(self.grid)
        for button in fig.layout.updatemenus[0].buttons:
            self.assertEqual(len(button.args[0]['visible']),len(fig.data))
    def test_time_vs_hour_axis(self):
        fig=energy_figure(self.grid);self.assertFalse(bool(fig.layout.xaxis2.matches))
    def test_summary(self):
        s=summarize_grid(self.grid);self.assertEqual(s['expected_slots'],3360)
    def test_selected_figure(self):
        g=make_expected_grid(self.valid,('East','West'));f=energy_figure(g,('East','West'))
        self.assertEqual(len(f.data),4)
    def test_invalid_source_additional(self):
        df=pd.read_csv(DATA/'regional_energy_hourly.csv');df.loc[0,'region']='UNKNOWN'
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'bad.csv';df.to_csv(p,index=False)
            valid,bad=validate_energy(p);self.assertTrue(bad.reason.str.contains('unknown_region').any())
    def test_no_original_mutation(self):
        before=(DATA/'regional_energy_hourly.csv').read_bytes()
        validate_energy()
        self.assertEqual(before,(DATA/'regional_energy_hourly.csv').read_bytes())

class TestSolutions(unittest.TestCase):
    def test_all_18_are_parseable(self):
        import ast
        files=list((ROOT/'solutions').glob('[0-9]*.py'));self.assertEqual(len(files),18)
        for p in files:ast.parse(p.read_text(encoding='utf-8'))
    def test_all_18_return_figure_or_path(self):
        files=sorted((ROOT/'solutions').glob('[0-9]*.py'))
        for p in files:
            with self.subTest(file=p.name):
                result=runpy.run_path(str(p))['solve']()
                self.assertTrue(isinstance(result,(go.Figure,Path)))
    def test_18_export_exists(self):
        p=runpy.run_path(str(ROOT/'solutions/18_html_export.py'))['solve']();self.assertTrue(p.exists())
    def test_one_dropdown_buttons(self):
        fig=runpy.run_path(str(ROOT/'solutions/08_dropdown.py'))['solve']()
        self.assertEqual(len(fig.layout.updatemenus[0].buttons),3)
    def test_one_missing_gap(self):
        fig=runpy.run_path(str(ROOT/'solutions/05_missing_gap.py'))['solve']()
        self.assertTrue(any(pd.isna(y) for y in fig.data[0].y))

class TestInteractiveArtifacts(unittest.TestCase):
    def test_22_example_html(self):
        self.assertEqual(len([p for p in (ROOT/'figures/interactive').glob('[0-9][0-9]_*.html') if int(p.name[:2]) <= 22]),23) # 22 examples + self-contained HTML
    def test_js_shared_exists(self):
        self.assertTrue((ROOT/'figures/interactive/plotly.min.js').exists())
    def test_no_cdns_for_directory_files(self):
        for p in (ROOT/'figures/interactive').glob('[0-9][0-9]_*.html'):
            if p.name=='20_single_file.html':continue
            html=p.read_text(encoding='utf-8')
            self.assertIn('plotly.min.js',html)
            self.assertNotIn('https://cdn.plot.ly',html)
    def test_previews(self):
        self.assertEqual(len([p for p in (ROOT/'figures/previews').glob('[0-9][0-9]_*.png') if int(p.name[:2])<=22]),22)
    def test_quiz_images(self):
        self.assertEqual(len(list((ROOT/'figures/quiz').glob('Q[0-9]*_choices.png'))),6)
    def test_quiz_metadata(self):
        quiz=json.loads((ROOT/'figures/quiz/_metadata.json').read_text(encoding='utf-8'))
        self.assertEqual(len(quiz),22)
    def test_practice_metadata(self):
        practice=json.loads((ROOT/'exercises/_metadata.json').read_text(encoding='utf-8'))
        self.assertEqual(len(practice),18)
    def test_offline_export(self):
        with tempfile.TemporaryDirectory() as t:
            p=export_html(go.Figure(go.Bar(x=['A'],y=[1])),Path(t)/'chart.html')
            self.assertTrue(p.exists());self.assertTrue((Path(t)/'plotly.min.js').exists())

if __name__=='__main__':unittest.main()
