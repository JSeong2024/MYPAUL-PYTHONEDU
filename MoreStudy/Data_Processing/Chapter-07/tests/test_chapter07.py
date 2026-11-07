from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
import pandas as pd
from pandas.testing import assert_frame_equal

ROOT = Path(__file__).resolve().parents[1]


def load_py(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


pipeline = load_py(ROOT / 'examples/14_store_sales_pipeline.py', 'store_sales_pipeline')
solutions = {i: load_py(ROOT / f'solutions/{i:02}_{name}.py', f'solution_{i}') for i, name in [
    (1, 'conditional_columns'),(2, 'groupby_region'),(3, 'safe_product_merge'),
    (4, 'pivot_melt_roundtrip'),(5, 'daily_rolling'),
]}


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.orders, self.products, self.stores = pipeline.load_sources()

    def test_01_raw_shape(self):
        self.assertEqual(len(self.orders), 48)
        self.assertEqual(len(self.products), 5)
        self.assertEqual(len(self.stores), 3)

    def test_02_original_keys_are_unique(self):
        pipeline.validate_sources(self.orders, self.products, self.stores)
        self.assertTrue(self.orders.line_id.is_unique)
        self.assertEqual(self.orders.order_id.nunique(), 24)

    def test_03_enrichment_keeps_row_count(self):
        result = pipeline.enrich_orders(self.orders, self.products, self.stores)
        self.assertEqual(len(result), len(self.orders))
        self.assertTrue(result.category.notna().all())

    def test_04_revenue_total(self):
        enriched = pipeline.enrich_orders(self.orders, self.products, self.stores)
        self.assertEqual(int(enriched.net_sales_won.sum()), 1523300)

    def test_05_store_and_category_totals_reconcile(self):
        enriched = pipeline.enrich_orders(self.orders, self.products, self.stores)
        summary = pipeline.make_summaries(enriched, self.stores.store_id)
        for k in ('sales_by_store', 'sales_by_category_month'):
            self.assertEqual(int(summary[k].net_sales_won.sum()), 1523300)

    def test_06_daily_calendar_and_total(self):
        enriched = pipeline.enrich_orders(self.orders, self.products, self.stores)
        daily = pipeline.make_summaries(enriched, self.stores.store_id)['sales_daily_by_store']
        self.assertEqual(len(daily), 45 * 3)
        self.assertEqual(int(daily.net_sales_won.sum()), 1523300)

    def test_07_rolling_not_mixing_stores(self):
        enriched = pipeline.enrich_orders(self.orders, self.products, self.stores)
        daily = pipeline.make_summaries(enriched, self.stores.store_id)['sales_daily_by_store']
        for _, frame in daily.groupby('store_id'):
            self.assertEqual(float(frame.rolling_7d_avg_won.iloc[0]), float(frame.net_sales_won.iloc[0]))
            self.assertAlmostEqual(float(frame.rolling_7d_avg_won.iloc[6]),
                                   round(frame.net_sales_won.iloc[:7].mean(), 2),places=2)

    def test_08_missing_product_rejected(self):
        data = self.orders.copy()
        data.loc[0,'product_id']='UNKNOWN'
        with self.assertRaisesRegex(ValueError, 'Unknown product_id'):
            pipeline.enrich_orders(data, self.products, self.stores)

    def test_09_missing_store_rejected(self):
        data = self.orders.copy()
        data.loc[0,'store_id']='UNKNOWN'
        with self.assertRaisesRegex(ValueError, 'Unknown store_id'):
            pipeline.enrich_orders(data, self.products, self.stores)

    def test_10_duplicate_dimension_rejected(self):
        data = pd.concat([self.products, self.products.iloc[[0]]],ignore_index=True)
        with self.assertRaisesRegex(ValueError, 'duplicated key'):
            pipeline.validate_sources(self.orders, data, self.stores)

    def test_11_duplicate_order_line_rejected(self):
        data = self.orders.copy()
        data.loc[1,'line_id']=data.loc[0,'line_id']
        with self.assertRaisesRegex(ValueError, 'duplicated key'):
            pipeline.validate_sources(data,self.products,self.stores)

    def test_12_duplicate_order_id_allowed(self):
        self.assertLess(self.orders.order_id.nunique(), len(self.orders))
        pipeline.validate_sources(self.orders,self.products,self.stores)

    def test_13_invalid_quantity_rejected(self):
        data=self.orders.copy()
        data.loc[0,'quantity']=0
        with self.assertRaisesRegex(ValueError, 'quantity'):
            pipeline.validate_sources(data,self.products,self.stores)

    def test_14_discount_bounds_rejected(self):
        data=self.orders.copy()
        data.loc[0,'discount_pct']=101
        with self.assertRaisesRegex(ValueError, 'Discount'):
            pipeline.validate_sources(data,self.products,self.stores)

    def test_15_fractional_won_rejected(self):
        data=self.orders.copy()
        data.loc[0,'quantity']=1
        data.loc[0,'unit_price_won']=101
        data.loc[0,'discount_pct']=5
        with self.assertRaisesRegex(ValueError, 'fractional KRW'):
            pipeline.enrich_orders(data,self.products,self.stores)

    def test_16_missing_required_value_rejected(self):
        data=self.orders.copy()
        data.loc[0,'store_id']=pd.NA
        with self.assertRaisesRegex(ValueError,'Missing required'):
            pipeline.validate_sources(data,self.products,self.stores)

    def test_17_pipeline_writes_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            result=pipeline.run_pipeline(output_dir=Path(d))
            self.assertEqual(result['net_sales_won'],1523300)
            names={p.name for p in Path(d).iterdir()}
            self.assertEqual(names,{
                'enriched_order_lines.csv', 'sales_by_store.csv', 'sales_by_category_month.csv',
                'sales_daily_by_store.csv','summary.json'})
            self.assertEqual(json.loads((Path(d)/'summary.json').read_text(encoding='utf8'))['distinct_orders'],24)

    def test_18_pipeline_repeat_is_deterministic(self):
        with tempfile.TemporaryDirectory() as d:
            pipeline.run_pipeline(output_dir=Path(d))
            before={p.name:p.read_bytes() for p in Path(d).iterdir()}
            pipeline.run_pipeline(output_dir=Path(d))
            after={p.name:p.read_bytes() for p in Path(d).iterdir()}
            self.assertEqual(before,after)

    def test_19_input_files_unchanged(self):
        original={p.name:p.read_bytes() for p in pipeline.DATA_DIR.iterdir() if p.is_file()}
        with tempfile.TemporaryDirectory() as d:
            pipeline.run_pipeline(output_dir=Path(d))
        after={p.name:p.read_bytes() for p in pipeline.DATA_DIR.iterdir() if p.is_file()}
        self.assertEqual(original,after)

    def test_20_bad_lookup_fails_before_export(self):
        with tempfile.TemporaryDirectory() as d:
            sample=Path(d)/'data';sample.mkdir()
            for name in ('order_lines.csv','products.csv','stores.csv'):
                (sample/name).write_bytes((pipeline.DATA_DIR/name).read_bytes())
            bad=pd.read_csv(sample/'order_lines.csv')
            bad.loc[0,'product_id']='WRONG'
            bad.to_csv(sample/'order_lines.csv',index=False)
            out=Path(d)/'result'
            with self.assertRaises(ValueError):
                pipeline.run_pipeline(data_dir=sample,output_dir=out)
            self.assertFalse(out.exists())


class SolutionTests(unittest.TestCase):
    def test_21_conditional_and_no_mutation(self):
        frame=pd.DataFrame({'quantity':[2,4,1],'unit_price_won':[10000,10000,5000]})
        original=frame.copy()
        result=solutions[1].classify_sales(frame)
        self.assertEqual(result.sales_won.tolist(),[20000,40000,5000])
        self.assertEqual(result.size_class.tolist(),['일반','대량','일반'])
        assert_frame_equal(frame,original)

    def test_22_groupby(self):
        frame=pd.DataFrame({'region':['서울','서울','부산'],'quantity':[2,1,3],'sales_won':[10000,5000,9000]})
        result=solutions[2].summarize_region(frame)
        self.assertEqual(result.sales_won.tolist(),[9000,15000])
        self.assertEqual(result.units.tolist(),[3,3])

    def test_23_merge(self):
        orders=pd.DataFrame({'line_id':['L1','L2'],'product_id':['P1','P2']})
        products=pd.DataFrame({'product_id':['P1','P2'],'category':['디지털','문구']})
        result=solutions[3].attach_category(orders,products)
        self.assertEqual(result.category.tolist(),['디지털','문구'])
        wrong=orders.copy()
        wrong.loc[0,'product_id']='UNKNOWN'
        with self.assertRaises(ValueError):solutions[3].attach_category(wrong,products)

    def test_24_pivot_roundtrip(self):
        frame=pd.DataFrame({'store':['A','A','B','B'],'month':['2026-01','2026-02']*2,'sales_won':[10,20,30,40]})
        wide,long=solutions[4].pivot_and_restore(frame)
        self.assertEqual(wide.shape,(2,2))
        assert_frame_equal(long,frame.sort_values(['store','month']).reset_index(drop=True))

    def test_25_rolling(self):
        frame=pd.DataFrame({'date':['2026-01-01','2026-01-03','2026-01-03'],'sales_won':[100,200,50]})
        result=solutions[5].daily_rolling_sum(frame,'2026-01-01','2026-01-04')
        self.assertEqual(result.sales_won.tolist(),[100,0,250,0])
        self.assertEqual(result.rolling_3d_sum.tolist(),[100,100,350,250])


if __name__=='__main__':unittest.main()
