"""Python 표준 라이브러리 unittest 기반 Chapter 03 테스트."""
import importlib.util
import unittest
import tempfile
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

def module_from(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"파일을 불러올 수 없습니다: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class SensorReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = module_from(ROOT / 'examples' / '13_sensor_quality_report.py')

    def test_dataset_counts(self):
        result = self.report.analyze_measurements(self.report.load_data())
        self.assertEqual((result['raw_count'], result['missing_count'],
                          result['range_error_count'], result['valid_count']), (28, 1, 1, 26))
        self.assertEqual(result['alarm_count'], 2)
        np.testing.assert_array_equal(result['sensor_alarm_count'], [0, 2, 0, 0])

    def test_report_csv_export(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'report.csv'
            result = self.report.analyze_measurements(self.report.load_data())
            self.report.save_report(result, path)
            lines = path.read_text(encoding='utf-8').splitlines()
            self.assertEqual(lines[0], 'sensor_number,mean_temperature_c,alarm_count')
            self.assertEqual(lines[2], '2,25.86,2')
            self.assertEqual(len(lines), 5)

    def test_incorrect_shape(self):
        with self.assertRaises(ValueError):
            self.report.analyze_measurements(np.array([22, 23, 24]))

    def test_all_invalid_column(self):
        with self.assertRaises(ValueError):
            self.report.analyze_measurements(np.array([[20, 21, -999, 24],
                                                      [22, 23, -999, 26]]))

class SolutionTests(unittest.TestCase):
    def solution(self, name):
        return module_from(ROOT / 'solutions' / (name + '.py'))

    def test_01(self):
        mod = self.solution('01_array_metrics')
        self.assertEqual(mod.summarize([15, 25, 35, 45]), (4, 30.0, 15, 45))
        with self.assertRaises(ValueError):
            mod.summarize([])

    def test_02(self):
        mod = self.solution('02_axis_summary')
        rows, columns = mod.summarize(np.array([[80, 90, 100], [60, 75, 90]]))
        np.testing.assert_allclose(rows, [90, 75])
        np.testing.assert_allclose(columns, [70, 82.5, 95])

    def test_03(self):
        mod = self.solution('03_sensor_calibration')
        actual = mod.calibrate(np.array([[20, 21, 22], [23, 24, 25]]),
                               np.array([0.5, -0.5, 1.0]))
        np.testing.assert_array_equal(actual, [[20.5, 20.5, 23], [23.5, 23.5, 26]])
        with self.assertRaises(ValueError):
            mod.calibrate(np.ones((2, 3)), np.ones(2))

    def test_04(self):
        mod = self.solution('04_clean_temperature')
        cleaned, avg = mod.clean_and_mean(np.array([20, -999, 25, 48, 30]))
        np.testing.assert_allclose(cleaned, [20, np.nan, 25, np.nan, 30], equal_nan=True)
        self.assertEqual(avg, 25.0)
        with self.assertRaises(ValueError):
            mod.clean_and_mean(np.array([-999, 47]))

    def test_05(self):
        mod = self.solution('05_sales_broadcasting')
        result = mod.daily_sales(np.array([[2, 1, 0], [0, 3, 1]]), np.array([1000, 2000, 1500]))
        np.testing.assert_array_equal(result, [4000, 7500])
        with self.assertRaises(ValueError):
            mod.daily_sales(np.ones((2, 3)), np.ones(2))

if __name__ == '__main__':
    unittest.main()
