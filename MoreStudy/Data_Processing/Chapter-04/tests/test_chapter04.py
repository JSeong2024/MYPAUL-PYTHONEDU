"""Chapter 04: answer files + project regression tests (unittest)."""
from __future__ import annotations
import importlib.util
import tempfile
import unittest
from pathlib import Path
import pandas as pd
from pandas.testing import assert_frame_equal

ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class Chapter04Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.orders = pd.read_csv(ROOT / "data" / "orders.csv")
        cls.modules = {p.stem: load_module(p) for p in (ROOT / "solutions").glob("*.py")}
        cls.project = load_module(ROOT / "examples" / "14_sales_report.py")

    def test_dataset_schema_and_counts(self):
        self.assertEqual(self.orders.shape, (20, 8))
        self.assertEqual(int(self.orders["status"].eq("completed").sum()), 17)
        self.assertEqual(int(self.orders["status"].eq("canceled").sum()), 3)
        self.assertTrue(self.orders["order_id"].is_unique)

    def test_dataframe_creation(self):
        frame = self.modules["01_build_dataframe"].build_dataframe()
        self.assertEqual(frame.columns.tolist(), ["product", "quantity", "unit_price"])
        self.assertEqual(frame["quantity"].tolist(), [2, 3, 5])
        self.assertEqual(frame.shape, (3, 3))

    def test_filter_orders(self):
        copy = self.orders.copy(deep=True)
        filtered = self.modules["02_filter_orders"].filter_orders(self.orders, "서울", 2)
        self.assertEqual(filtered.columns.tolist(), ["order_id", "product", "quantity"])
        self.assertEqual(filtered["order_id"].tolist(), ["ORD001", "ORD006", "ORD009", "ORD015"])
        self.assertEqual(filtered.index.tolist(), [0, 1, 2, 3])
        assert_frame_equal(copy, self.orders)

    def test_filter_no_rows(self):
        out = self.modules["02_filter_orders"].filter_orders(self.orders, "대구", 2)
        self.assertTrue(out.empty)
        self.assertEqual(out.columns.tolist(), ["order_id", "product", "quantity"])

    def test_top_revenue(self):
        mod = self.modules["03_top_revenue"]
        frame = mod.top_revenue_orders(self.orders)
        self.assertEqual(frame["order_id"].tolist(), ["ORD007", "ORD011", "ORD012"])
        self.assertEqual(frame["amount"].tolist(), [58000, 36000, 29000])
        self.assertTrue(mod.top_revenue_orders(self.orders, n=0).empty)
        with self.assertRaises(ValueError):
            mod.top_revenue_orders(self.orders, n=-1)

    def test_parse_columns_nullable_types(self):
        raw = pd.DataFrame({"price_text": ["2,500", "N/A", "1,200"],
                            "date_text": ["2026-10-01", "wrong", "2026-10-03"]})
        original = raw.copy(deep=True)
        out = self.modules["04_parse_columns"].parse_columns(raw)
        self.assertEqual(str(out["price"].dtype), "Int64")
        self.assertEqual(out["price"].iloc[0], 2500)
        self.assertTrue(pd.isna(out["price"].iloc[1]))
        self.assertTrue(pd.isna(out["date"].iloc[1]))
        assert_frame_equal(raw, original)

    def test_category_summary(self):
        result = self.modules["05_category_summary"].category_summary(self.orders)
        self.assertEqual(result.columns.tolist(), ["category", "orders", "revenue"])
        self.assertEqual(result["revenue"].sum(), 266300)
        self.assertEqual(result["orders"].sum(), 17)
        self.assertEqual(result["revenue"].tolist(), sorted(result["revenue"].tolist(), reverse=True))

    def test_project_total_and_groups(self):
        loaded = self.project.load_orders(ROOT / "data" / "orders.csv")
        region, category, daily = self.project.make_reports(loaded)
        self.assertEqual(int(region["revenue"].sum()), 266300)
        self.assertEqual(int(category["revenue"].sum()), 266300)
        self.assertEqual(int(daily["revenue"].sum()), 266300)
        self.assertEqual(region["orders"].sum(), 17)
        self.assertEqual(region["region"].tolist(), ["부산", "서울", "인천"])

    def test_project_export_roundtrip(self):
        loaded = self.project.load_orders(ROOT / "data" / "orders.csv")
        summaries = self.project.make_reports(loaded)
        with tempfile.TemporaryDirectory() as temp:
            self.project.export_reports(summaries, Path(temp))
            paths = sorted(Path(temp).glob("*.csv"))
            self.assertEqual(len(paths), 3)
            self.assertEqual(int(pd.read_csv(Path(temp) / "sales_by_region.csv")["revenue"].sum()), 266300)

    def test_project_rejects_duplicate_ids(self):
        df = self.orders.copy()
        df.loc[1, "order_id"] = df.loc[0, "order_id"]
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "bad.csv"
            df.to_csv(p, index=False)
            with self.assertRaises(ValueError):
                self.project.load_orders(p)

    def test_project_rejects_bad_quantity(self):
        df = self.orders.copy()
        df.loc[0, "quantity"] = -2
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "bad.csv"
            df.to_csv(p, index=False)
            with self.assertRaises(ValueError):
                self.project.load_orders(p)

    def test_project_rejects_bad_status_and_date(self):
        for col, value in (("status", "pending"), ("order_date", "not-a-date")):
            df = self.orders.copy()
            df.loc[0, col] = value
            with tempfile.TemporaryDirectory() as temp:
                p = Path(temp) / "bad.csv"
                df.to_csv(p, index=False)
                with self.subTest(col=col), self.assertRaises(ValueError):
                    self.project.load_orders(p)

    def test_project_rejects_missing_column(self):
        df = self.orders.drop(columns=["status"])
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "bad.csv"
            df.to_csv(p, index=False)
            with self.assertRaises(ValueError):
                self.project.load_orders(p)


if __name__ == "__main__":
    unittest.main()
