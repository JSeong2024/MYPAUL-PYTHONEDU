import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


project = load_module(ROOT / "examples/13_order_quality_pipeline.py")
answers = {n: load_module(ROOT / "solutions" / f"{n:02d}_{name}.py") for n, name in [
    (1, "missing_profile"), (2, "deduplicate_orders"), (3, "validate_quantities"),
    (4, "normalize_regions"), (5, "validate_sensor"),
]}


class ExerciseTests(unittest.TestCase):
    def test_missing_profile(self):
        frame = pd.DataFrame({"a": ["hello", "  ", None], "b": [1, None, 3]})
        actual = answers[1].missing_counts(frame)
        self.assertEqual(actual.to_dict(), {"a": 2, "b": 1})
        self.assertEqual(frame.loc[1, "a"], "  ")

    def test_deduplicate_keep_first(self):
        raw = pd.DataFrame({"order_id": ["A", "B", "A"], "value": [2, 3, 5]})
        clean = answers[2].deduplicate_orders(raw)
        self.assertEqual(clean["value"].tolist(), [2, 3])
        self.assertEqual(len(raw), 3)

    def test_quantity_numeric_validation(self):
        raw = pd.Series(["1", "100", "2.5", "0", "oops", None, "inf"])
        self.assertEqual(answers[3].valid_quantity_mask(raw).tolist(),
                         [True, True, False, False, False, False, False])

    def test_normalize_regions(self):
        raw = pd.Series([" SEOUL ", "busan", "Daegu", None])
        actual = answers[4].normalize_regions(raw)
        self.assertEqual(actual.iloc[:2].tolist(), ["Seoul", "Busan"])
        self.assertTrue(pd.isna(actual.iloc[2]))
        self.assertTrue(pd.isna(actual.iloc[3]))

    def test_sensor_range_and_invalid_date(self):
        raw = pd.DataFrame({"date": ["2026-10-01", "2026-02-30", "2026-10-03", "2026-10-04"],
                            "temperature_c": ["20.5", "18.0", "999", "-40"]})
        actual = answers[5].valid_sensor_rows(raw)
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual["temperature_c"].tolist(), [20.5, -40.0])

    def test_sensor_missing_column(self):
        with self.assertRaises(ValueError):
            answers[5].valid_sensor_rows(pd.DataFrame({"date": ["2026-10-01"]}))


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.src = ROOT / "data/raw_orders.csv"
        self.policy = ROOT / "data/cleaning_policy.json"

    def test_read_input_without_implicit_conversion(self):
        raw = pd.read_csv(self.src, dtype="string", keep_default_na=False)
        self.assertEqual(len(raw), 31)
        self.assertEqual(raw.loc[8, "quantity"], "")

    def test_source_is_not_mutated(self):
        raw = pd.read_csv(self.src, dtype="string", keep_default_na=False)
        before = raw.copy(deep=True)
        project.clean_orders(raw, project.load_policy(self.policy))
        pd.testing.assert_frame_equal(raw, before)

    def test_output_counts_balance(self):
        with tempfile.TemporaryDirectory() as dirname:
            result = project.run_pipeline(self.src, self.policy, Path(dirname))
            self.assertEqual(result["source_records"], result["accepted_records"] +
                             result["rejected_records"] + result["review_records"])

    def test_duplicate_is_rejected(self):
        with tempfile.TemporaryDirectory() as dirname:
            project.run_pipeline(self.src, self.policy, Path(dirname))
            audit = pd.read_csv(Path(dirname) / "audit_log.csv")
            target = audit.loc[audit["issues"].fillna("").str.contains("DUPLICATE_ORDER_ID")]
            self.assertEqual(len(target), 1)
            self.assertEqual(target.iloc[0]["source_line"], 18)

    def test_outlier_is_reviewed_not_deleted(self):
        with tempfile.TemporaryDirectory() as dirname:
            result = project.run_pipeline(self.src, self.policy, Path(dirname))
            review = pd.read_csv(Path(dirname) / "review_orders.csv")
            self.assertEqual(result["review_records"], 1)
            self.assertEqual(review.iloc[0]["order_id"], "ORD-013")
            self.assertIn("HIGH_UNIT_PRICE", review.iloc[0]["issues"])

    def test_aggregate_uses_only_accepted_completed(self):
        with tempfile.TemporaryDirectory() as dirname:
            result = project.run_pipeline(self.src, self.policy, Path(dirname))
            cleaned = pd.read_csv(Path(dirname) / "cleaned_orders.csv")
            revenue = cleaned.loc[cleaned.status == "completed", "total_price"].sum()
            self.assertEqual(result["completed_revenue_krw"], int(revenue))

    def test_unknown_status_is_rejected(self):
        with tempfile.TemporaryDirectory() as dirname:
            project.run_pipeline(self.src, self.policy, Path(dirname))
            rejected = pd.read_csv(Path(dirname) / "rejected_orders.csv")
            record = rejected.loc[rejected.order_id == "ORD-021"]
            self.assertIn("INVALID_STATUS", record.iloc[0]["issues"])

    def test_missing_column_fails(self):
        raw = pd.read_csv(self.src, dtype="string", keep_default_na=False).drop(columns=["unit_price"])
        with self.assertRaises(ValueError):
            project.clean_orders(raw, project.load_policy(self.policy))

    def test_policy_validation(self):
        with tempfile.TemporaryDirectory() as dirname:
            p = Path(dirname) / "policy.json"
            obj = json.loads(self.policy.read_text(encoding="utf-8"))
            obj["max_quantity"] = -2
            p.write_text(json.dumps(obj), encoding="utf-8")
            with self.assertRaises(ValueError):
                project.load_policy(p)

    def test_rerun_is_deterministic(self):
        with tempfile.TemporaryDirectory() as dirname:
            out = Path(dirname)
            first = project.run_pipeline(self.src, self.policy, out)
            initial = {p.name: p.read_bytes() for p in out.iterdir()}
            second = project.run_pipeline(self.src, self.policy, out)
            again = {p.name: p.read_bytes() for p in out.iterdir()}
            self.assertEqual(first, second)
            self.assertEqual(initial, again)

    def test_expected_outputs(self):
        with tempfile.TemporaryDirectory() as dirname:
            project.run_pipeline(self.src, self.policy, Path(dirname))
            actual = {p.name for p in Path(dirname).iterdir()}
            self.assertEqual(actual, {
                "cleaned_orders.csv", "rejected_orders.csv", "review_orders.csv",
                "audit_log.csv", "revenue_by_region.csv", "quality_report.json",
            })


if __name__ == "__main__":
    unittest.main()
