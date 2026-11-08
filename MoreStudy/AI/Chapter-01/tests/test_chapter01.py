"""Chapter 01: 실행 코드, 데이터 계약, 프로젝트 핵심 검증."""
from pathlib import Path
import importlib.util
import unittest

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


nearest = load_module("nearest", "examples/01_nearest_example.py")
weather_example = load_module("weather_example", "examples/02_rule_vs_learning.py")
iris_example = load_module("iris_example", "examples/03_iris_classification.py")
mini_weather = load_module("mini_weather", "solutions/mini_01_weather_decision.py")
mini_iris = load_module("mini_iris", "solutions/mini_02_iris_explorer.py")
rare_event = load_module("rare_event", "solutions/advanced_01_rare_event.py")
digit_review = load_module("digit_review", "solutions/advanced_02_digit_review.py")
practice1 = load_module("practice1", "solutions/practice_01_nearest_neighbor.py")
practice2 = load_module("practice2", "solutions/practice_02_accuracy_and_recall.py")
practice3 = load_module("practice3", "solutions/practice_03_review_gate.py")
generator = load_module("dataset_generator", "scripts/make_datasets.py")


class DatasetTests(unittest.TestCase):
    def test_weather_data_shape(self):
        df = pd.read_csv(ROOT / "data/weather_choices.csv")
        self.assertEqual(df.shape, (100, 4))
        self.assertEqual(df.case_id.nunique(), 100)
        self.assertTrue(df.umbrella_chosen.isin([0, 1]).all())

    def test_rare_data_shape(self):
        df = pd.read_csv(ROOT / "data/rare_events.csv")
        self.assertEqual(df.shape, (400, 4))
        self.assertEqual(int(df.is_rare_event.sum()), 40)

    def test_weather_generation_is_reproducible(self):
        df = pd.read_csv(ROOT / "data/weather_choices.csv")
        pd.testing.assert_frame_equal(df, generator.make_weather())

    def test_rare_generation_is_reproducible(self):
        df = pd.read_csv(ROOT / "data/rare_events.csv")
        pd.testing.assert_frame_equal(df, generator.make_rare_events())


class ExampleTests(unittest.TestCase):
    def test_nearest_case(self):
        answer, distance, index = nearest.closest_example(
            np.array([[2, 1], [3, 2], [7, 7], [8, 6]]),
            np.array(["A", "A", "B", "B"]), np.array([4, 3]),
        )
        self.assertEqual(answer, "A")
        self.assertEqual(index, 1)
        self.assertAlmostEqual(distance, 2**0.5)

    def test_nearest_bad_dimension(self):
        with self.assertRaises(ValueError):
            nearest.closest_example(np.array([[1, 2]]), np.array(["A"]), np.array([1]))

    def test_weather_example(self):
        r = weather_example.evaluate()
        self.assertEqual(r["test_size"], 25)
        self.assertAlmostEqual(r["rule_accuracy"], 0.84)
        self.assertAlmostEqual(r["model_accuracy"], 0.96)

    def test_iris_example(self):
        r = iris_example.classify_iris()
        self.assertEqual(r["test_size"], 30)
        self.assertEqual(r["correct"], 28)
        self.assertEqual(len(set(r["test_indices"])), 30)


class ProjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.weather = pd.read_csv(ROOT / "data/weather_choices.csv")
        cls.rare = pd.read_csv(ROOT / "data/rare_events.csv")

    def test_mini01_comparison(self):
        result = mini_weather.evaluate_weather(self.weather)
        self.assertEqual((result["rule_correct"], result["model_correct"]), (21, 24))
        self.assertEqual(result["n_test"], 25)

    def test_mini01_reject_duplicate_id(self):
        df = self.weather.copy()
        df.loc[2, "case_id"] = df.loc[1, "case_id"]
        with self.assertRaises(ValueError):
            mini_weather.evaluate_weather(df)

    def test_mini01_reject_invalid_rain(self):
        df = self.weather.copy()
        df.loc[0, "rain_probability_pct"] = 105
        with self.assertRaises(ValueError):
            mini_weather.evaluate_weather(df)

    def test_mini01_reject_infinite_wind(self):
        df = self.weather.copy()
        df["wind_speed_kmh"] = df["wind_speed_kmh"].astype(float)
        df.loc[0, "wind_speed_kmh"] = np.inf
        with self.assertRaises(ValueError):
            mini_weather.evaluate_weather(df)

    def test_mini01_reject_nonnumeric_rain(self):
        df = self.weather.copy()
        df["rain_probability_pct"] = df["rain_probability_pct"].astype(object)
        df.loc[0, "rain_probability_pct"] = "invalid"
        with self.assertRaises(ValueError):
            mini_weather.evaluate_weather(df)

    def test_mini02_confusion_count(self):
        result = mini_iris.analyze_iris()
        self.assertEqual(result["test_size"], 30)
        self.assertEqual(int(result["confusion_matrix"].sum()), 30)
        self.assertEqual(result["wrong_count"], 2)

    def test_mini02_bad_k(self):
        with self.assertRaises(ValueError):
            mini_iris.analyze_iris(k=0)

    def test_advanced01_baseline(self):
        result = rare_event.evaluate_rare_event(self.rare)
        self.assertEqual((result["n_test"], result["n_rare_test"]), (100, 10))
        self.assertAlmostEqual(result["baseline_accuracy"], 0.9)
        self.assertAlmostEqual(result["baseline_rare_recall"], 0)
        self.assertAlmostEqual(result["model_rare_recall"], 0.8)

    def test_advanced01_bad_label(self):
        df = self.rare.copy()
        df.loc[0, "is_rare_event"] = 3
        with self.assertRaises(ValueError):
            rare_event.evaluate_rare_event(df)

    def test_advanced01_nonfinite(self):
        df = self.rare.copy()
        df.loc[1, "sensor_a"] = np.inf
        with self.assertRaises(ValueError):
            rare_event.evaluate_rare_event(df)

    def test_advanced02_review_partition(self):
        result = digit_review.analyze_digits()
        self.assertEqual(result["n_test"], 360)
        self.assertEqual(result["auto_count"] + result["review_count"], 360)
        self.assertEqual(result["review_count"], 14)
        self.assertGreater(result["auto_accuracy"], 0.95)

    def test_advanced02_threshold_monotonic(self):
        r1 = digit_review.analyze_digits(threshold=0.6)
        r2 = digit_review.analyze_digits(threshold=0.8)
        r3 = digit_review.analyze_digits(threshold=1.0)
        self.assertLessEqual(r1["review_count"], r2["review_count"])
        self.assertLessEqual(r2["review_count"], r3["review_count"])

    def test_advanced02_out_of_range(self):
        with self.assertRaises(ValueError):
            digit_review.analyze_digits(threshold=1.1)
        with self.assertRaises(ValueError):
            digit_review.review_decision(np.array([0.8]), -0.1)


class PracticeTests(unittest.TestCase):
    def test_practice01(self):
        result = practice1.predict_one(
            np.array([[1, 2], [4, 5], [8, 9]]),
            np.array(["A", "B", "C"]), np.array([5, 5]),
        )
        self.assertEqual(result, "B")

    def test_practice02(self):
        a, r = practice2.evaluate(
            np.array([0, 0, 1, 0, 1, 0]), np.array([0, 0, 0, 0, 1, 0]),
        )
        self.assertAlmostEqual(a, 5/6)
        self.assertAlmostEqual(r, 0.5)

    def test_practice02_no_positives(self):
        _, r = practice2.evaluate(np.array([0, 0]), np.array([0, 0]))
        self.assertIsNone(r)

    def test_practice03(self):
        result = practice3.review_flags(np.array([1.0, 0.8, 0.6, 0.4]), 0.8)
        np.testing.assert_array_equal(result, np.array([False, False, True, True]))


if __name__ == "__main__":
    unittest.main()
