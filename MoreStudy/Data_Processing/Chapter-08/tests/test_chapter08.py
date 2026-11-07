"""Chapter 08 통합 테스트. 표준 라이브러리 unittest 사용."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project.processing.pipeline import (  # noqa: E402
    load_inputs, validate_and_clean, make_summaries, make_quality_report, run_pipeline,
)


def load_solution(number: int, name: str):
    path = ROOT / "solutions" / f"{number:02d}_{name}.py"
    spec = importlib.util.spec_from_file_location(f"solution_ch08_{number}", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


solutions = [
    load_solution(1, "required_columns"),
    load_solution(2, "temperature_validation"),
    load_solution(3, "station_aggregation"),
    load_solution(4, "safe_station_join"),
    load_solution(5, "observation_coverage"),
]


class WeatherPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_dir = ROOT / "data"
        cls.raw, cls.stations, cls.policy = load_inputs(cls.data_dir)
        cls.clean, cls.issues, cls.audit = validate_and_clean(cls.raw, cls.stations, cls.policy)
        cls.daily, cls.station, cls.monthly, cls.coverage = make_summaries(cls.clean, cls.stations, cls.policy)

    def test_01_input_sizes(self):
        self.assertEqual(len(self.raw), 92)
        self.assertEqual(len(self.stations), 3)

    def test_02_sources_preserve_raw_strings(self):
        self.assertEqual(self.raw.loc[self.raw.observation_id.eq("OBS-MISS-TEMP"), "temperature_c"].iloc[0], "")
        self.assertEqual(self.raw.loc[0, "observation_id"], "OBS-01-01-1")

    def test_03_statuses(self):
        self.assertEqual(self.audit.status.value_counts().to_dict(), {"accepted": 79, "rejected": 10, "review": 3})

    def test_04_reject_reason(self):
        issue = self.issues.loc[self.issues.observation_id.eq("OBS-NEG-RAIN")].iloc[0]
        self.assertEqual(issue.status, "rejected")
        self.assertIn("negative_precipitation", issue.reason)

    def test_05_review_reason(self):
        issue = self.issues.loc[self.issues.observation_id.eq("OBS-03-01-2")].iloc[0]
        self.assertEqual(issue.status, "review")
        self.assertIn("missing_temperature_c", issue.reason)

    def test_06_invalid_datetime(self):
        issue = self.issues.loc[self.issues.observation_id.eq("OBS-BAD-DATE")].iloc[0]
        self.assertIn("invalid_timestamp", issue.reason)

    def test_07_no_invalid_numbers_accepted(self):
        self.assertTrue(self.clean.temperature_c.between(-30, 45).all())
        self.assertTrue(self.clean.humidity_pct.between(0, 100).all())
        self.assertTrue(self.clean.precipitation_mm.ge(0).all())

    def test_08_only_expected_times(self):
        self.assertTrue(self.clean.timestamp_local.dt.strftime("%H:%M").isin(["09:00", "18:00"]).all())

    def test_09_no_duplicate_accepted_slots(self):
        self.assertFalse(self.clean.duplicated(["station_id", "timestamp_local"]).any())
        self.assertTrue(self.clean.observation_id.is_unique)

    def test_10_station_join_complete(self):
        self.assertEqual(set(self.clean.region), {"Seoul", "Busan", "Gwangju"})
        self.assertFalse(self.clean.region.isna().any())

    def test_11_daily_and_station_consistency(self):
        self.assertEqual(int(self.daily.readings.sum()), len(self.clean))
        self.assertEqual(int(self.station.readings.sum()), len(self.clean))
        self.assertEqual(int(self.monthly.readings.sum()), len(self.clean))

    def test_12_precipitation_reconciles(self):
        self.assertAlmostEqual(float(self.daily.total_precipitation_mm.sum()),
                               float(self.clean.precipitation_mm.sum()), places=6)

    def test_13_missing_date_not_zero(self):
        row = self.coverage.loc[(self.coverage.station_id == "ST-02") &
                                (self.coverage.date == "2026-10-09")].iloc[0]
        self.assertEqual(row.status, "missing")
        self.assertEqual(int(row.observed_readings), 0)
        self.assertFalse(((self.daily.station_id == "ST-02") & (self.daily.date == "2026-10-09")).any())

    def test_14_partial_dates(self):
        self.assertEqual(int((self.coverage.status == "partial").sum()), 3)

    def test_15_expected_slots(self):
        self.assertEqual(int(self.coverage.expected_readings.sum()), 84)
        self.assertEqual(int(self.coverage.observed_readings.sum()), 79)

    def test_16_report(self):
        report = make_quality_report(self.audit, self.clean, self.coverage)
        self.assertEqual(report["missing_observation_slots"], 5)
        self.assertEqual(report["coverage_pct"], 94.05)
        self.assertEqual(report["missing_station_days"], 1)

    def test_17_output_files(self):
        with tempfile.TemporaryDirectory() as temp:
            result = run_pipeline(self.data_dir, Path(temp))
            names = {p.name for p in Path(temp).iterdir()}
            self.assertEqual(names, {
                "cleaned_weather.csv", "issues.csv", "audit.csv", "daily_station_summary.csv",
                "station_summary.csv", "monthly_region_summary.csv", "coverage.csv", "quality_report.json",
            })
            self.assertEqual(json.loads((Path(temp) / "quality_report.json").read_text(encoding="utf-8")), result.report)

    def test_18_outputs_stable_on_repeat(self):
        with tempfile.TemporaryDirectory() as temp:
            run_pipeline(self.data_dir, Path(temp))
            first = {p.name: p.read_bytes() for p in Path(temp).iterdir()}
            run_pipeline(self.data_dir, Path(temp))
            second = {p.name: p.read_bytes() for p in Path(temp).iterdir()}
            self.assertEqual(first, second)

    def test_19_sources_not_modified(self):
        previous = {p.name: p.read_bytes() for p in self.data_dir.iterdir() if p.is_file()}
        with tempfile.TemporaryDirectory() as temp:
            run_pipeline(self.data_dir, Path(temp))
        current = {p.name: p.read_bytes() for p in self.data_dir.iterdir() if p.is_file()}
        self.assertEqual(previous, current)

    def test_20_duplicate_station_reference_fails_before_output(self):
        with tempfile.TemporaryDirectory() as temp:
            d = Path(temp)
            source = d / "data"
            shutil.copytree(self.data_dir, source)
            path = source / "stations.json"
            rows = json.loads(path.read_text(encoding="utf-8"))
            rows.append(rows[0])
            path.write_text(json.dumps(rows), encoding="utf-8")
            out = d / "output"
            with self.assertRaisesRegex(ValueError, "유일"):
                run_pipeline(source, out)
            self.assertFalse(out.exists())

    def test_21_missing_column_fails_before_output(self):
        with tempfile.TemporaryDirectory() as temp:
            d = Path(temp)
            source = d / "data"
            shutil.copytree(self.data_dir, source)
            path = source / "weather_observations.csv"
            df = pd.read_csv(path)
            df.drop(columns="humidity_pct").to_csv(path, index=False)
            out = d / "output"
            with self.assertRaisesRegex(ValueError, "헤더"):
                run_pipeline(source, out)
            self.assertFalse(out.exists())

    def test_22_unknown_station_rejected(self):
        unknown = self.issues.loc[self.issues.observation_id.eq("OBS-UNKNOWN")].iloc[0]
        self.assertIn("unknown_station", unknown.reason)

    def test_23_same_input_output_disallowed(self):
        with self.assertRaisesRegex(ValueError, "원본"):
            run_pipeline(self.data_dir, self.data_dir)

    def test_24_cli_runs_from_another_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp) / "output"
            r = subprocess.run([sys.executable, str(ROOT / "project" / "main.py"),
                                "--data-dir", str(self.data_dir), "--output-dir", str(dest)],
                               cwd=temp, capture_output=True, text=True, check=True)
            self.assertIn("Accepted: 79", r.stdout)
            self.assertTrue((dest / "coverage.csv").exists())

    def test_25_solution_1(self):
        df = pd.DataFrame({"a": [1]})
        self.assertTrue(solutions[0].check_required_columns(df, []))
        self.assertTrue(solutions[0].check_required_columns(df, ["a"]))
        self.assertFalse(solutions[0].check_required_columns(df, ["a", "b"]))

    def test_26_solution_2(self):
        got = solutions[1].temperature_status(pd.Series(["19", "", "100", "bad", "inf"]))
        self.assertEqual(got.valid.tolist(), [True, False, False, False, False])

    def test_27_solution_3(self):
        df = pd.DataFrame({"station_id": ["B", "A", "A"], "temperature_c": [9.0, 10.0, 20.0]})
        result = solutions[2].station_mean(df)
        self.assertEqual(result.station_id.tolist(), ["A", "B"])
        self.assertEqual(result.avg_temperature_c.tolist(), [15.0, 9.0])

    def test_28_solution_4(self):
        observations = pd.DataFrame({"station_id": ["A", "B"]})
        lookup = pd.DataFrame({"station_id": ["A", "B"], "region": ["alpha", "beta"]})
        got = solutions[3].join_station_region(observations, lookup)
        self.assertEqual(got.region.tolist(), ["alpha", "beta"])
        with self.assertRaises(ValueError):
            solutions[3].join_station_region(observations, pd.concat([lookup, lookup.iloc[[0]]]))
        with self.assertRaises(ValueError):
            solutions[3].join_station_region(pd.DataFrame({"station_id": ["C"]}), lookup)

    def test_29_solution_5(self):
        df = pd.DataFrame({"observation_id": ["A", "B", "C"]})
        self.assertEqual(solutions[4].calculate_coverage(df, 4), 75.0)
        with self.assertRaises(ValueError):
            solutions[4].calculate_coverage(df, 0)
        with self.assertRaises(ValueError):
            solutions[4].calculate_coverage(df, 2)

    def test_30_copy_of_clean_is_stable(self):
        clean2, issues2, audit2 = validate_and_clean(self.raw, self.stations, self.policy)
        assert_frame_equal(clean2, self.clean)
        assert_frame_equal(issues2, self.issues)
        assert_frame_equal(audit2, self.audit)

    def test_31_missing_parquet_dependency_is_informative(self):
        try:
            import pyarrow  # noqa: F401
        except ImportError:
            with tempfile.TemporaryDirectory() as temp:
                dest = Path(temp) / "output"
                with self.assertRaisesRegex(RuntimeError, "pyarrow"):
                    run_pipeline(self.data_dir, dest, parquet=True)
                self.assertFalse(dest.exists())
        else:
            with tempfile.TemporaryDirectory() as temp:
                dest = Path(temp) / "output"
                run_pipeline(self.data_dir, dest, parquet=True)
                self.assertTrue((dest / "cleaned_weather.parquet").exists())


if __name__ == "__main__":
    unittest.main()
