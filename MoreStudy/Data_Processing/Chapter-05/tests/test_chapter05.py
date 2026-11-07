"""Chapter 05 fixture and Mini Project tests. Run: python -m unittest discover -s tests -v"""
import importlib.util
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from shutil import copy2

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / 'examples' / '15_multiformat_report.py'
spec = importlib.util.spec_from_file_location('multiformat_report', EXAMPLE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Chapter05Tests(unittest.TestCase):
    def test_csv_rows_and_zero_padded_region(self):
        frame = pd.read_csv(ROOT / 'data/orders.csv', dtype={'region_code': 'string'})
        self.assertEqual(len(frame), 12)
        self.assertEqual(frame.loc[0, 'region_code'], '01')

    def test_json_products(self):
        doc = json.loads((ROOT / 'data/products.json').read_text(encoding='utf-8'))
        self.assertEqual(doc['schema_version'], 1)
        self.assertEqual(len(doc['products']), 4)

    def test_jsonl_lines(self):
        rows = [json.loads(line) for line in (ROOT / 'data/readings.jsonl').read_text(encoding='utf-8').splitlines()]
        self.assertEqual(len(rows), 4)

    def test_excel_sheets_and_types(self):
        file = ROOT / 'data/regions.xlsx'
        with pd.ExcelFile(file, engine='openpyxl') as excel:
            self.assertEqual(excel.sheet_names, ['Regions', 'Targets'])
        df = pd.read_excel(file, sheet_name='Regions', engine='openpyxl', dtype={'region_code':'string'})
        self.assertEqual(df.loc[0,'region_code'], '01')

    def test_report_totals(self):
        joined, region, category = module.build_report(ROOT / 'data')
        self.assertEqual(len(joined), 10)
        self.assertEqual(int(joined['revenue'].sum()), 79200)
        self.assertEqual(int(region['revenue'].sum()), 79200)
        self.assertEqual(int(category['revenue'].sum()), 79200)

    def test_region_revenue(self):
        _, region, _ = module.build_report(ROOT / 'data')
        self.assertEqual(dict(zip(region['region_name'], region['revenue'])), {'광주':30500,'부산':27900,'서울':20800})

    def test_category_revenue(self):
        _, _, category = module.build_report(ROOT / 'data')
        self.assertEqual(dict(zip(category['category'], category['revenue'])), {'문구':25700,'생활':36000,'음료':17500})

    def test_export_and_sqlite(self):
        joined, region, category = module.build_report(ROOT / 'data')
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            module.export_report(output, joined, region, category)
            self.assertTrue((output/'revenue_by_region.csv').is_file())
            self.assertTrue((output/'revenue_by_category.json').is_file())
            db = sqlite3.connect(output/'report.sqlite')
            try:
                value = db.execute('SELECT SUM(revenue) FROM revenue_by_region').fetchone()[0]
            finally:
                db.close()
            self.assertEqual(value, 79200)

    def test_solution_summaries(self):
        spec = importlib.util.spec_from_file_location('summary', ROOT / 'solutions/01_csv_order_summary.py')
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        self.assertEqual(mod.summarize(ROOT/'data/orders.csv'), (10,79200))

    def test_solution_sql(self):
        spec = importlib.util.spec_from_file_location('sql_exercise', ROOT / 'solutions/04_sql_parameter_query.py')
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        self.assertEqual(mod.find_devices(22.0), ['ST-01','ST-02'])

    def test_solution_json_export(self):
        spec = importlib.util.spec_from_file_location('json_exercise', ROOT / 'solutions/05_safe_json_export.py')
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / 'converted.json'
            self.assertEqual(mod.convert(ROOT/'data/orders.csv', out), 10)
            self.assertEqual(json.loads(out.read_text(encoding='utf-8'))[0]['region_code'], '01')

    def _mutated_source(self, mutator):
        temp=tempfile.TemporaryDirectory()
        data=Path(temp.name)
        for filename in ('orders.csv','products.json','regions.xlsx'):
            copy2(ROOT/'data'/filename, data/filename)
        orders=pd.read_csv(data/'orders.csv',dtype={'region_code':'string'})
        mutator(orders)
        orders.to_csv(data/'orders.csv',index=False)
        return temp,data

    def test_reject_duplicate_order_id(self):
        temp,data = self._mutated_source(lambda frame: frame.__setitem__('order_id', ['ORD001']*len(frame)))
        try:
            with self.assertRaisesRegex(ValueError, '중복'):
                module.build_report(data)
        finally: temp.cleanup()

    def test_reject_bad_status(self):
        temp,data = self._mutated_source(lambda frame: frame.__setitem__('status', ['unknown']*len(frame)))
        try:
            with self.assertRaisesRegex(ValueError, '상태'):
                module.build_report(data)
        finally: temp.cleanup()

    def test_reject_missing_reference(self):
        temp,data = self._mutated_source(lambda frame: frame.__setitem__('product_id', ['P99']*len(frame)))
        try:
            with self.assertRaisesRegex(ValueError, '일치하지'):
                module.build_report(data)
        finally: temp.cleanup()

    def test_reject_negative_quantity(self):
        temp,data = self._mutated_source(lambda frame: frame.__setitem__('quantity', [-1]*len(frame)))
        try:
            with self.assertRaisesRegex(ValueError, '수량'):
                module.build_report(data)
        finally: temp.cleanup()

    def test_reject_invalid_date(self):
        temp,data = self._mutated_source(lambda frame: frame.__setitem__('order_date', ['not-a-date']*len(frame)))
        try:
            with self.assertRaisesRegex(ValueError, '날짜'):
                module.build_report(data)
        finally: temp.cleanup()


if __name__ == '__main__':
    unittest.main()
