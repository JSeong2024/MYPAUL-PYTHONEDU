"""Chapter 02 — 계산·입력 검증·모범답안 회귀 테스트."""
from pathlib import Path
import sys
import unittest
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "solutions"))
sys.path.insert(0, str(ROOT / "scripts"))
from practice_01_loss_metrics import calculate_errors
from practice_02_linear_predict import predict_linear
from practice_03_gradient_step import gradient_step
from mini_01_delivery_regression import validate as validate_delivery, evaluate as delivery_evaluate
from mini_02_gradient_descent import sample_data, gradient_descent, compare as gradient_compare
from advanced_01_scaling_knn import validate as validate_sensor, evaluate as sensor_evaluate
from advanced_02_leakage_audit import (
    validate as validate_energy, evaluate as energy_evaluate,
    unavailable_features,
)
from make_datasets import generate


class TestPractice(unittest.TestCase):
    def test_mae_mse_hand_result(self):
        mae, mse = calculate_errors([3, 5, 7], [2, 7, 8])
        self.assertAlmostEqual(mae, 4 / 3)
        self.assertAlmostEqual(mse, 2)

    def test_mae_perfect(self):
        self.assertEqual(calculate_errors([0, 1], [0, 1]), (0.0, 0.0))

    def test_loss_shape_rejected(self):
        with self.assertRaises(ValueError): calculate_errors([1, 2], [1])

    def test_loss_empty_rejected(self):
        with self.assertRaises(ValueError): calculate_errors([], [])

    def test_loss_nan_rejected(self):
        with self.assertRaises(ValueError): calculate_errors([np.nan], [1])

    def test_linear_predict(self):
        np.testing.assert_allclose(predict_linear([[2, 1], [4, 0]], [3, 2], 1), [9, 13])

    def test_linear_wrong_dimensions(self):
        with self.assertRaises(ValueError): predict_linear([[1, 2]], [3], 0)

    def test_linear_nan_rejected(self):
        with self.assertRaises(ValueError): predict_linear([[np.nan]], [1], 0)

    def test_gradient_hand_step(self):
        w, b = gradient_step([0, 1, 2, 3], [1, 3, 5, 7], 0, 0, .02)
        self.assertAlmostEqual(w, .34)
        self.assertAlmostEqual(b, .16)

    def test_gradient_invalid_learning_rate(self):
        with self.assertRaises(ValueError): gradient_step([1], [2], 0, 0, 0)

    def test_gradient_nans(self):
        with self.assertRaises(ValueError): gradient_step([np.nan], [2], 0, 0, .02)


class TestData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.delivery = pd.read_csv(ROOT / "data/delivery_times.csv")
        cls.sensor = pd.read_csv(ROOT / "data/sensor_signals.csv")
        cls.energy = pd.read_csv(ROOT / "data/energy_usage.csv")

    def test_delivery_rows(self):
        self.assertEqual(len(self.delivery), 180)

    def test_sensor_rows(self):
        self.assertEqual(len(self.sensor), 240)

    def test_energy_rows(self):
        self.assertEqual(len(self.energy), 320)

    def test_data_deterministic(self):
        datasets = generate()
        pd.testing.assert_frame_equal(self.delivery, datasets["delivery_times.csv"], check_dtype=False)
        pd.testing.assert_frame_equal(self.sensor, datasets["sensor_signals.csv"], check_dtype=False)
        pd.testing.assert_frame_equal(self.energy, datasets["energy_usage.csv"], check_dtype=False)

    def test_delivery_valid(self):
        self.assertEqual(len(validate_delivery(self.delivery)), 180)

    def test_delivery_duplicate(self):
        bad = self.delivery.copy(); bad.loc[1, "order_id"] = bad.loc[0, "order_id"]
        with self.assertRaises(ValueError): validate_delivery(bad)

    def test_delivery_negative(self):
        bad = self.delivery.copy(); bad.loc[0, "duration_min"] = -2
        with self.assertRaises(ValueError): validate_delivery(bad)

    def test_delivery_missing(self):
        bad = self.delivery.drop(columns=["distance_km"])
        with self.assertRaises(ValueError): validate_delivery(bad)

    def test_delivery_invalid_stops(self):
        bad = self.delivery.copy(); bad["stops"] = bad["stops"].astype(float); bad.loc[0, "stops"] = 2.5
        with self.assertRaises(ValueError): validate_delivery(bad)

    def test_sensor_valid(self):
        self.assertEqual(len(validate_sensor(self.sensor)), 240)

    def test_sensor_invalid_label(self):
        bad = self.sensor.copy(); bad.loc[0, "fault_label"] = 2
        with self.assertRaises(ValueError): validate_sensor(bad)

    def test_sensor_duplicate(self):
        bad = self.sensor.copy(); bad.loc[1, "sample_id"] = bad.loc[0, "sample_id"]
        with self.assertRaises(ValueError): validate_sensor(bad)

    def test_energy_valid(self):
        self.assertEqual(len(validate_energy(self.energy)), 320)

    def test_energy_duplicate(self):
        bad = self.energy.copy(); bad.loc[1, "record_id"] = bad.loc[0, "record_id"]
        with self.assertRaises(ValueError): validate_energy(bad)

    def test_energy_nan(self):
        bad = self.energy.copy(); bad.loc[0, "energy_kwh"] = np.nan
        with self.assertRaises(ValueError): validate_energy(bad)


class TestProjects(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.delivery = pd.read_csv(ROOT / "data/delivery_times.csv")
        cls.sensor = pd.read_csv(ROOT / "data/sensor_signals.csv")
        cls.energy = pd.read_csv(ROOT / "data/energy_usage.csv")

    def test_delivery_baseline(self):
        r=delivery_evaluate(self.delivery)
        self.assertLess(r["mae"], r["baseline_mae"])

    def test_delivery_expected_mae(self):
        self.assertAlmostEqual(delivery_evaluate(self.delivery)["mae"], 3.3885, places=3)

    def test_delivery_slope(self):
        self.assertAlmostEqual(delivery_evaluate(self.delivery)["slope"], 3.2761, places=3)

    def test_delivery_split_count(self):
        self.assertEqual(len(delivery_evaluate(self.delivery)["X_test"]), 45)

    def test_gradient_slope(self):
        r=gradient_compare()
        self.assertAlmostEqual(r["weight"], r["reference_weight"], places=7)

    def test_gradient_bias(self):
        r=gradient_compare()
        self.assertAlmostEqual(r["bias"], r["reference_bias"], places=7)

    def test_gradient_loss_decreasing(self):
        r=gradient_compare()
        self.assertLess(r["losses"][-1], r["losses"][0])
        self.assertTrue(np.all(np.diff(r["losses"]) <= 1e-10))

    def test_gradient_iterations(self):
        x, y = sample_data()
        self.assertEqual(len(gradient_descent(x, y, steps=73)[2]), 73)

    def test_gradient_invalid_nans(self):
        with self.assertRaises(ValueError): gradient_descent([1], [np.inf])

    def test_sensor_scaling_comparison(self):
        r=sensor_evaluate(self.sensor)
        self.assertGreater(r["scaled_accuracy"], r["raw_accuracy"])

    def test_sensor_expected_accuracy(self):
        r=sensor_evaluate(self.sensor)
        self.assertAlmostEqual(r["raw_accuracy"], .35)
        self.assertAlmostEqual(r["scaled_accuracy"], 58/60)

    def test_sensor_changed_predictions(self):
        self.assertEqual(sensor_evaluate(self.sensor)["changed"], 39)

    def test_sensor_test_count(self):
        self.assertEqual(sensor_evaluate(self.sensor)["n_test"], 60)

    def test_leakage_feature(self):
        self.assertEqual(unavailable_features(["temperature_c", "meter_finalized_kwh"]), ["meter_finalized_kwh"])

    def test_leakage_model_gap(self):
        r=energy_evaluate(self.energy)
        self.assertGreater(r["legitimate_mae"], r["leaked_mae"] * 40)

    def test_leakage_expected_mae(self):
        r=energy_evaluate(self.energy)
        self.assertAlmostEqual(r["legitimate_mae"], 11.2199, places=2)
        self.assertAlmostEqual(r["leaked_mae"], .09898, places=2)

    def test_leakage_test_count(self):
        self.assertEqual(energy_evaluate(self.energy)["n_test"], 80)

    def test_model_inputs_exclude_identifiers(self):
        self.assertNotIn("order_id", ["distance_km"])
        self.assertNotIn("record_id", ["temperature_c", "floor_area_m2", "occupancy"])


if __name__ == "__main__":
    unittest.main()
