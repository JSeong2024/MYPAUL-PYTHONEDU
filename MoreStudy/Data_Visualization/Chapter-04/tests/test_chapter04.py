"""Chapter 04 tests: sample data, semantic correctness, reports and README links."""
from __future__ import annotations
from pathlib import Path
import importlib.util
import json
import re
import sys
import tempfile
import unittest
import pandas as pd
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

def load(rel):
    p=ROOT/rel
    spec=importlib.util.spec_from_file_location(p.stem+'_'+p.parent.name,p)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

retail=load('solutions/mini_projects/mini_01_retail.py')
service=load('solutions/mini_projects/mini_02_service.py')
library=load('solutions/mini_projects/mini_03_library.py')
bike=load('solutions/advanced_projects/advanced_01_bike.py')

class TestData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=pd.read_csv(ROOT/'data/retail_orders.csv')
        cls.s=pd.read_csv(ROOT/'data/service_requests.csv')
        cls.l=pd.read_csv(ROOT/'data/library_visits.csv')
        cls.t=pd.read_csv(ROOT/'data/bike_trips.csv')
        cls.status=pd.read_csv(ROOT/'data/bike_reporting.csv')
    def test_retail_rows(self): self.assertEqual(len(self.r),672)
    def test_completed_rows(self): self.assertEqual(int(self.r.status.eq('Completed').sum()),619)
    def test_revenue_sum(self): self.assertEqual(int(self.r.revenue_krw.sum()),7654200)
    def test_returned_zero_revenue(self): self.assertTrue(self.r.loc[self.r.status.eq('Returned'),'revenue_krw'].eq(0).all())
    def test_retail_dates(self): self.assertEqual(self.r.date.nunique(),42)
    def test_service_rows(self): self.assertEqual(len(self.s),756)
    def test_service_median(self): self.assertEqual(float(self.s.response_ms.median()),170.0)
    def test_service_over_limit(self): self.assertEqual(int(self.s.response_ms.gt(500).sum()),15)
    def test_library_rows(self): self.assertEqual(len(self.l),110)
    def test_library_visits(self): self.assertEqual(int(self.l.visitors.sum()),19561)
    def test_bike_raw_rows(self): self.assertEqual(len(self.t),6824)
    def test_reporting_slots(self): self.assertEqual(len(self.status),378)
    def test_reporting_missing(self): self.assertEqual(int(self.status.reporting.eq(0).sum()),16)
    def test_station_count(self): self.assertEqual(len(pd.read_csv(ROOT/'data/bike_stations.csv')),6)

class TestMiniProjects(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ret=retail.prepare()
        cls.svc=service.prepare()
        cls.lib=library.prepare()
    def test_retail_filters(self):self.assertEqual(len(self.ret),619)
    def test_retail_branch_sum(self):
        d,b,c=retail.summarize(self.ret)
        self.assertEqual(int(d.revenue_krw.sum()),7654200)
        self.assertEqual(int(b.revenue_krw.sum()),7654200)
        self.assertEqual(int(c.revenue_krw.sum()),7654200)
    def test_retail_daily_has_dates(self):self.assertEqual(len(retail.summarize(self.ret)[0]),42)
    def test_retail_empty_fails(self):
        with self.assertRaises(ValueError):retail.summarize(self.ret.iloc[0:0])
    def test_retail_negative_fails(self):
        with tempfile.TemporaryDirectory() as d:
            x=pd.read_csv(ROOT/'data/retail_orders.csv');x.loc[0,'revenue_krw']=-1
            p=Path(d)/'orders.csv';x.to_csv(p,index=False)
            with self.assertRaises(ValueError):retail.prepare(p)
    def test_service_count(self):self.assertEqual(len(self.svc),756)
    def test_service_counts_preserved(self):self.assertEqual(int(service.summarize(self.svc).requests.sum()),756)
    def test_service_p95_vs_median(self):
        out=service.summarize(self.svc)
        self.assertTrue(all(out.p95_ms>=out.median_ms))
    def test_service_threshold_counts(self):self.assertEqual(int(service.summarize(self.svc).over_limit.sum()),15)
    def test_service_duplicate_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            x=self.svc.copy();x.loc[1,'request_id']=x.loc[0,'request_id']
            p=Path(d)/'service.csv';x.to_csv(p,index=False)
            with self.assertRaises(ValueError):service.prepare(p)
    def test_library_calendar_length(self):self.assertEqual(len(library.build_calendar(self.lib)),112)
    def test_library_calendar_missing(self):self.assertEqual(int((~library.build_calendar(self.lib).observed).sum()),2)
    def test_library_missing_remains_nan(self):
        missing=library.build_calendar(self.lib)
        self.assertTrue(missing.loc[~missing.observed,'visitors'].isna().all())
    def test_library_duplicate_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            x=pd.concat([self.lib,self.lib.iloc[:1]],ignore_index=True)
            p=Path(d)/'duplicate.csv';x.to_csv(p,index=False)
            with self.assertRaises(ValueError):library.prepare(p)

class TestAdvanced(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rides,cls.stations,cls.reporting=bike.load_inputs()
        cls.clean,cls.rejected=bike.clean_rides(cls.rides,cls.stations,cls.reporting)
        cls.slots=bike.build_slot_counts(cls.clean,cls.reporting,cls.stations)
    def test_load_station_count(self):self.assertEqual(len(self.stations),6)
    def test_rejected_count(self):self.assertEqual(len(self.rejected),5)
    def test_accepted_count(self):self.assertEqual(len(self.clean),6819)
    def test_accepted_unique_ids(self):self.assertFalse(self.clean.ride_id.duplicated().any())
    def test_valid_duration(self):self.assertTrue(self.clean.duration_min.between(.0001,240).all())
    def test_slots_count(self):self.assertEqual(len(self.slots),378)
    def test_unreported_is_missing(self):self.assertTrue(self.slots.loc[self.slots.reporting.eq(0),'rides'].isna().all())
    def test_reported_is_present(self):self.assertTrue(self.slots.loc[self.slots.reporting.eq(1),'rides'].notna().all())
    def test_reporting_sum(self):self.assertEqual(int(self.slots.reporting.sum()),362)
    def test_ride_slot_count_sums(self):self.assertEqual(int(self.slots.rides.sum()),6819)
    def test_unknown_station_rejected(self):
        with self.assertRaises(ValueError):bike.filter_stations(self.slots,['ST-XX'])
    def test_empty_selection_rejected(self):
        with self.assertRaises(ValueError):bike.filter_stations(self.slots,[])
    def test_station_filter_exact(self):
        selected=bike.filter_stations(self.slots,['ST-01','ST-03'])
        self.assertEqual(set(selected.station_id),{'ST-01','ST-03'})
        self.assertEqual(len(selected),126)
    def test_coverage_in_bounds(self):
        summary,_,_=bike.summarize(self.slots,self.clean)
        self.assertTrue(summary.coverage_pct.between(0,100).all())
    def test_no_negative_count(self):
        self.assertTrue(self.slots.rides.dropna().ge(0).all())
    def test_station_summary_unique(self):
        summary,_,_=bike.summarize(self.slots,self.clean)
        self.assertFalse(summary.station_name.duplicated().any())
    def test_reference_duplicate_station_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            td=Path(d)
            for name in ['bike_trips.csv','bike_stations.csv','bike_reporting.csv']:
                (td/name).write_bytes((ROOT/'data'/name).read_bytes())
            p=td/'bike_stations.csv';stations=pd.read_csv(p);stations.loc[1,'station_id']=stations.loc[0,'station_id'];stations.to_csv(p,index=False)
            with self.assertRaises(ValueError):bike.load_inputs(td)
    def test_reference_duplicate_slot_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            td=Path(d)
            for name in ['bike_trips.csv','bike_stations.csv','bike_reporting.csv']:
                (td/name).write_bytes((ROOT/'data'/name).read_bytes())
            p=td/'bike_reporting.csv';x=pd.read_csv(p);x.loc[1,['date','station_id','time_band']]=x.loc[0,['date','station_id','time_band']];x.to_csv(p,index=False)
            with self.assertRaises(ValueError):bike.load_inputs(td)

class TestReports(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        td=Path(cls.tmp.name)
        cls.one=retail.run(td/'retail')
        cls.two=service.run(td/'service')
        cls.three=library.run(td/'library')
        cls.four=bike.run(td/'bike',station_ids=['ST-01','ST-03'])
        cls.out=td
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def test_mini_1_revenue(self):self.assertEqual(self.one['total_revenue_krw'],7654200)
    def test_mini_1_png(self):self.assertTrue((self.out/'retail/retail_report.png').stat().st_size>5000)
    def test_mini_1_csv(self):self.assertEqual(len(pd.read_csv(self.out/'retail/daily_revenue.csv')),42)
    def test_mini_2_median(self):self.assertEqual(self.two['overall_median_ms'],170)
    def test_mini_2_files(self):self.assertTrue((self.out/'service/service_summary.csv').exists())
    def test_mini_3_missing(self):self.assertEqual(self.three['missing_records'],2)
    def test_mini_3_png(self):self.assertTrue((self.out/'library/library_facets.png').exists())
    def test_adv_subset_station_count(self):self.assertEqual(self.four['selected_station_count'],2)
    def test_adv_all_rejected(self):self.assertEqual(self.four['rejected_rows'],5)
    def test_adv_subset_slots(self):self.assertEqual(self.four['selected_expected_slots'],126)
    def test_adv_subset_pngs(self):
        for filename in ['bike_overview.png','bike_heatmap.png','bike_station_facets.png']:
            self.assertGreater((self.out/'bike'/filename).stat().st_size,5000)
    def test_adv_missing_slot_output(self):
        df=pd.read_csv(self.out/'bike/reporting_slots.csv')
        self.assertTrue(df.loc[df.reporting.eq(0),'rides'].isna().all())

class TestLearningArtifacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.text=(ROOT/'README.md').read_text(encoding='utf-8')
    def test_examples_number(self):self.assertEqual(len(list((ROOT/'examples').glob('*.py'))),22)
    def test_practice_number(self):self.assertEqual(len(list((ROOT/'exercises').glob('[0-9][0-9]_*.py'))),18)
    def test_solutions_number(self):self.assertEqual(len(list((ROOT/'solutions/practice').glob('*.py'))),18)
    def test_starters_number(self):self.assertEqual(len(list((ROOT/'projects').rglob('starter.py'))),4)
    def test_projects_documented(self):
        for title in ['Retail Sales Comparison','Service Response Time Report','Library Usage Review','Public Bicycle Demand Report Generator']:
            self.assertIn(title,self.text)
    def test_quiz_count(self):
        answers=re.findall(r'<summary><strong>Q\d{2}\. 정답 및 해설 확인</strong></summary>',self.text)
        self.assertEqual(len(answers),20)
    def test_quiz_answer_is_collapsible(self):
        for i in range(1,21):
            self.assertIn(f'Q{i:02d}. 정답 및 해설 확인</strong></summary>',self.text)
    def test_visual_quiz_assets(self):self.assertEqual(len(list((ROOT/'figures/quiz').glob('*.png'))),6)
    def test_graph_images_exist(self):
        from PIL import Image
        for f in (ROOT/'figures').rglob('*.png'):
            with Image.open(f) as im:
                im.verify()
            self.assertGreater(f.stat().st_size,3000,str(f))
    def test_readme_links_exist(self):
        targets=re.findall(r'\]\((\.[^\s)]*)\)',self.text)
        for x in targets:
            # only relative file and directory links, not anchors
            target=(ROOT/x).resolve()
            if not target.is_relative_to(ROOT.resolve()):
                # Sibling chapter links are only available within the full repository.
                continue
            self.assertTrue(target.exists(),f'Missing link: {x}')
    def test_sections_anchors(self):
        for x in range(1,27):self.assertIn(f'<a id="section-4-{x}"></a>',self.text)
    def test_no_unescaped_tilde_strikethrough(self):
        # Outside code fences, check for accidental two tildes / ambiguous shorthand ranges
        pieces=re.split(r'```[\s\S]*?```',self.text)
        for s in pieces:self.assertNotIn('~~',s)
    def test_no_practice_solution_in_main_body(self):
        area=self.text.split('## 4.22. Coding Practice',1)[1].split('## 4.24. Quiz',1)[0]
        self.assertNotIn('def clean_rides(',area)
        self.assertNotIn('def build_slot_counts(',area)
    def test_data_dictionary_exists(self):self.assertTrue((ROOT/'data/DATA_DICTIONARY.md').exists())
    def test_all_examples_execute(self):
        import runpy, warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for script in sorted((ROOT/'examples').glob('*.py')):
                with self.subTest(script=script.name):
                    runpy.run_path(str(script),run_name='__main__')
    def test_all_practice_solutions_execute(self):
        import runpy, warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for script in sorted((ROOT/'solutions/practice').glob('*.py')):
                with self.subTest(script=script.name):
                    runpy.run_path(str(script),run_name='__main__')

if __name__=='__main__':unittest.main(verbosity=2)
