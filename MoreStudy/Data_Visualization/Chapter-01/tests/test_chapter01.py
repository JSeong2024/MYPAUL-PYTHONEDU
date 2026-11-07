import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def load_solution(stem: str):
    path = ROOT / "solutions" / f"{stem}.py"
    spec = importlib.util.spec_from_file_location(stem, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


class DataVisualizationChapter01Tests(unittest.TestCase):
    def setUp(self):
        from project.park_report import load_data, summarize
        self.frame = load_data(ROOT / "data" / "park_visits.csv")
        self.summary = summarize(self.frame)

    def test_input_has_14_rows(self):
        self.assertEqual(len(self.frame), 14)

    def test_day_unique(self):
        self.assertFalse(self.frame["date"].duplicated().any())

    def test_summary_day_counts(self):
        self.assertEqual(self.summary["dry_days"] + self.summary["rainy_days"], 14)

    def test_summary_total(self):
        self.assertEqual(self.summary["total_visitors"], int(self.frame["visitors"].sum()))

    def test_summary_rainy_count(self):
        self.assertEqual(self.summary["rainy_days"], 4)

    def test_load_rejects_bad_columns(self):
        from project.park_report import load_data
        with tempfile.TemporaryDirectory() as temp:
            file=Path(temp)/"wrong.csv"
            pd.DataFrame({"day": ["2026-01-01"], "visitors": [20]}).to_csv(file,index=False)
            with self.assertRaises(ValueError):load_data(file)

    def test_load_rejects_duplicate_day(self):
        from project.park_report import load_data
        with tempfile.TemporaryDirectory() as temp:
            file=Path(temp)/"dup.csv"
            pd.concat([self.frame, self.frame.iloc[[0]]]).to_csv(file,index=False)
            with self.assertRaises(ValueError):load_data(file)

    def test_load_rejects_negative_visitors(self):
        from project.park_report import load_data
        with tempfile.TemporaryDirectory() as temp:
            file=Path(temp)/"negative.csv"
            sample=self.frame.copy(); sample.loc[0,"visitors"]=-1
            sample.to_csv(file,index=False)
            with self.assertRaises(ValueError):load_data(file)

    def test_load_rejects_noninteger_visitors(self):
        from project.park_report import load_data
        with tempfile.TemporaryDirectory() as temp:
            file=Path(temp)/"fraction.csv"
            sample=self.frame.copy(); sample["visitors"] = sample["visitors"].astype(float); sample.loc[0,"visitors"]=20.5
            sample.to_csv(file,index=False)
            with self.assertRaises(ValueError):load_data(file)

    def test_load_rejects_invalid_temperature(self):
        from project.park_report import load_data
        with tempfile.TemporaryDirectory() as temp:
            file=Path(temp)/"temperature.csv"
            sample=self.frame.copy();sample.loc[0,"temperature_c"]=100
            sample.to_csv(file,index=False)
            with self.assertRaises(ValueError):load_data(file)

    def test_report_writes_four_charts_and_json(self):
        from project.park_report import run_report
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)
            result=run_report(ROOT / "data" / "park_visits.csv",path)
            for name in ("visitor_trend.png", "rain_status_comparison.png", "temperature_scatter.png", "visitor_histogram.png"):
                self.assertGreater((path/name).stat().st_size,1000)
            saved=json.loads((path/"summary.json").read_text(encoding="utf-8"))
            self.assertEqual(saved,result)

    def test_solution_01(self):
        mod=load_solution("01_weekly_temperature")
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/"one.png"
            self.assertEqual(mod.draw_chart(out),(19.0,23.0));self.assertGreater(out.stat().st_size,1000)

    def test_solution_02(self):
        mod=load_solution("02_product_sales_bar")
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/"two.png"
            self.assertEqual(mod.draw_chart(out),155);self.assertGreater(out.stat().st_size,1000)

    def test_solution_03(self):
        mod=load_solution("03_temperature_visitors_scatter")
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/"three.png"
            self.assertEqual(mod.draw_chart(ROOT / "data" / "park_visits.csv",out),14)
            self.assertGreater(out.stat().st_size,1000)

    def test_solution_04(self):
        mod=load_solution("04_park_dashboard")
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/"four.png"
            result=mod.build_dashboard(ROOT / "data" / "park_visits.csv",out)
            self.assertEqual(result,{"total_visitors":self.summary["total_visitors"],"rainy_days":4})
            self.assertGreater(out.stat().st_size,1000)


if __name__=="__main__":unittest.main()
