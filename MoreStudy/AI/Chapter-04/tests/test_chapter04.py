"""Chapter 04: 입력 검증·수치 평가·평가 프로토콜 테스트."""
import sys
import tempfile
import unittest
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"solutions"))
sys.path.insert(0,str(ROOT/"examples"))
sys.path.insert(0,str(ROOT/"scripts"))
from common import load_alerts,load_delivery,load_curve,load_devices,ROOT as PROJECT_ROOT
import mini_01_alert_metrics as alert
import mini_02_eta_regression as eta
import advanced_01_threshold_selection as threshold
import advanced_02_group_audit as grouped
from practice_01_confusion_counts import confusion_counts
from practice_02_binary_scores import binary_scores
from practice_03_regression_scores import regression_scores
from practice_04_threshold_predictions import threshold_predictions
from make_datasets import generate_alerts,generate_delivery,generate_curve,generate_devices
import importlib
curve_example=importlib.import_module("03_overfitting_curve")
grid_example=importlib.import_module("04_grid_search_cv")


def invalid_file(df,change):
    with tempfile.TemporaryDirectory() as d:
        path=Path(d)/"invalid.csv"
        change(df)
        df.to_csv(path,index=False)
        return path


class TestDatasets(unittest.TestCase):
    def test_alert_shape(self): self.assertEqual(load_alerts().shape,(720,6))
    def test_alert_binary(self): self.assertEqual(set(load_alerts().flagged.unique()),{0,1})
    def test_alert_rare(self): self.assertTrue(.05 < load_alerts().flagged.mean() < .25)
    def test_delivery_shape(self): self.assertEqual(load_delivery().shape,(560,5))
    def test_curve_shape(self): self.assertEqual(load_curve().shape,(80,3))
    def test_device_shape(self): self.assertEqual(load_devices().shape,(600,5))
    def test_devices_per_group(self): self.assertEqual(set(load_devices().groupby('device_id').size()),{6})
    def test_device_group_count(self): self.assertEqual(load_devices().device_id.nunique(),100)
    def test_regenerate_alerts(self): pd.testing.assert_frame_equal(load_alerts(),generate_alerts())
    def test_regenerate_delivery(self): pd.testing.assert_frame_equal(load_delivery(),generate_delivery())
    def test_regenerate_curve(self): pd.testing.assert_frame_equal(load_curve(),generate_curve())
    def test_regenerate_devices(self): pd.testing.assert_frame_equal(load_devices(),generate_devices())
    def test_alert_id_unique(self): self.assertFalse(load_alerts().alert_id.duplicated().any())
    def test_delivery_target_positive(self): self.assertTrue((load_delivery().actual_minutes>0).all())
    def test_device_label_stable(self): self.assertTrue((load_devices().groupby('device_id').maintenance_flag.nunique()==1).all())


class TestValidation(unittest.TestCase):
    def check_reject(self,loader,df,mutation):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.csv'; mutation(df);df.to_csv(p,index=False)
            with self.assertRaises(ValueError): loader(p)
    def test_alert_missing(self): self.check_reject(load_alerts,load_alerts(),lambda d:d.drop(columns='flagged',inplace=True))
    def test_alert_duplicate_id(self): self.check_reject(load_alerts,load_alerts(),lambda d:d.__setitem__('alert_id',[d.alert_id.iloc[0]]*len(d)))
    def test_alert_negative(self): self.check_reject(load_alerts,load_alerts(),lambda d:d.loc.__setitem__((0,'temperature_c'),-100))
    def test_alert_bad_label(self): self.check_reject(load_alerts,load_alerts(),lambda d:d.loc.__setitem__((0,'flagged'),3))
    def test_alert_missing_value(self): self.check_reject(load_alerts,load_alerts(),lambda d:d.loc.__setitem__((0,'current_a'),np.nan))
    def test_delivery_nonpositive(self): self.check_reject(load_delivery,load_delivery(),lambda d:d.loc.__setitem__((0,'actual_minutes'),0))
    def test_delivery_duplicate(self): self.check_reject(load_delivery,load_delivery(),lambda d:d.__setitem__('delivery_id',[d.delivery_id.iloc[0]]*len(d)))
    def test_curve_nan(self): self.check_reject(load_curve,load_curve(),lambda d:d.loc.__setitem__((0,'target_y'),np.nan))
    def test_device_bad_group(self): self.check_reject(load_devices,load_devices(),lambda d:d.loc.__setitem__((0,'maintenance_flag'),1-int(d.loc[0,'maintenance_flag'])))
    def test_device_bad_label(self): self.check_reject(load_devices,load_devices(),lambda d:d.loc.__setitem__((0,'maintenance_flag'),2))
    def test_device_missing(self): self.check_reject(load_devices,load_devices(),lambda d:d.drop(columns='device_id',inplace=True))


class TestPractice(unittest.TestCase):
    def test_counts(self):self.assertEqual(confusion_counts([0,0,1,1,1],[0,1,0,1,1]),(1,1,1,2))
    def test_counts_total(self): self.assertEqual(sum(confusion_counts([0,1,0],[1,0,0])),3)
    def test_counts_length(self):
        with self.assertRaises(ValueError): confusion_counts([0,1],[1])
    def test_counts_label(self):
        with self.assertRaises(ValueError): confusion_counts([0,2],[0,1])
    def test_counts_empty(self):
        with self.assertRaises(ValueError): confusion_counts([],[])
    def test_scores(self):
        result=binary_scores(8,2,4)
        self.assertAlmostEqual(result[0],.8)
        self.assertAlmostEqual(result[1],2/3)
        self.assertAlmostEqual(result[2],8/11)
    def test_scores_zero(self):self.assertEqual(binary_scores(0,0,0),(0.,0.,0.))
    def test_scores_negative(self):
        with self.assertRaises(ValueError): binary_scores(1,-1,0)
    def test_scores_float(self):
        with self.assertRaises(ValueError): binary_scores(1.5,0,0)
    def test_regression(self):
        a,b,c=regression_scores([2,5,10],[3,5,8]);self.assertAlmostEqual(a,1);self.assertAlmostEqual(b,5/3);self.assertAlmostEqual(c,np.sqrt(5/3))
    def test_regression_perfect(self):self.assertEqual(regression_scores([2,3],[2,3]),(0.,0.,0.))
    def test_regression_empty(self):
        with self.assertRaises(ValueError):regression_scores([],[])
    def test_regression_nan(self):
        with self.assertRaises(ValueError):regression_scores([2,float('nan')],[1,2])
    def test_regression_length(self):
        with self.assertRaises(ValueError):regression_scores([1,2],[1])
    def test_threshold(self): self.assertEqual(threshold_predictions([.2,.5,.8],.5).tolist(),[0,1,1])
    def test_threshold_one(self): self.assertEqual(threshold_predictions([1.,.8],1.).tolist(),[1,0])
    def test_threshold_zero(self): self.assertEqual(threshold_predictions([0,.2],0).tolist(),[1,1])
    def test_threshold_invalid(self):
        with self.assertRaises(ValueError):threshold_predictions([.2],1.1)
    def test_score_invalid(self):
        with self.assertRaises(ValueError):threshold_predictions([-0.1,.2],.5)
    def test_score_nan(self):
        with self.assertRaises(ValueError):threshold_predictions([np.nan,.2],.5)


class TestMini(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.binary=alert.evaluate(load_alerts())
        cls.regression=eta.evaluate(load_delivery())
    def test_binary_test_count(self):self.assertEqual(self.binary['test_count'],180)
    def test_binary_positive(self):self.assertEqual(self.binary['positive_count'],25)
    def test_binary_dummy_zero_recall(self):self.assertEqual(self.binary['dummy']['recall'],0)
    def test_binary_dummy_accuracy(self):self.assertAlmostEqual(self.binary['dummy']['accuracy'],155/180)
    def test_binary_model_recall(self):self.assertAlmostEqual(self.binary['model']['recall'],2/25)
    def test_binary_matrix_sum(self):self.assertEqual(self.binary['model']['matrix'].sum(),180)
    def test_binary_specificity(self):self.assertAlmostEqual(self.binary['model']['specificity'],154/155)
    def test_binary_model_f1(self):self.assertTrue(0<=self.binary['model']['f1']<=1)
    def test_eta_mae_improves(self):self.assertLess(self.regression['model']['mae'],self.regression['baseline']['mae'])
    def test_eta_r2(self):self.assertGreater(self.regression['model']['r2'],0.9)
    def test_eta_cv_folds(self):self.assertEqual(len(self.regression['cv_mae']),5)
    def test_eta_mae_positive(self):self.assertGreater(self.regression['model']['mae'],0)
    def test_eta_rmse_ge_mae(self):self.assertGreaterEqual(self.regression['model']['rmse'],self.regression['model']['mae'])
    def test_eta_prediction_count(self):self.assertEqual(len(self.regression['actual']),140)


class TestAdvanced(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.threshold=threshold.evaluate(load_alerts())
        cls.grouped=grouped.evaluate(load_devices())
    def test_threshold_choice(self):self.assertAlmostEqual(self.threshold['chosen'],.10)
    def test_threshold_validation_count(self):self.assertEqual(self.threshold['val_size'],144)
    def test_threshold_test_count(self):self.assertEqual(self.threshold['test_size'],144)
    def test_threshold_search_points(self):self.assertEqual(len(self.threshold['validation_f2']),19)
    def test_threshold_max(self):self.assertEqual(self.threshold['validation_f2'].max(),max(self.threshold['validation_f2']))
    def test_threshold_recall(self):self.assertGreater(self.threshold['selected_test']['recall'],self.threshold['default_test']['recall'])
    def test_threshold_precision(self):self.assertLess(self.threshold['selected_test']['precision'],self.threshold['default_test']['precision'])
    def test_threshold_matrix_total(self):self.assertEqual(int(self.threshold['selected_test']['matrix'].sum()),144)
    def test_threshold_tiebreak(self):
        t,s=threshold.choose_threshold([1,0],[.9,.1],[.2,.3]);self.assertEqual(t,.3)
    def test_threshold_bad_input(self):
        with self.assertRaises(ValueError):threshold.choose_threshold([0,1],[.3])
    def test_threshold_bad_scores(self):
        with self.assertRaises(ValueError):threshold.choose_threshold([0,1],[.2,np.nan])
    def test_group_random_optimistic(self):self.assertGreater(self.grouped['random']['balanced_accuracy'],.95)
    def test_group_random_overlap(self):self.assertGreater(self.grouped['random']['group_overlap'],0)
    def test_group_holdout_no_overlap(self):self.assertEqual(self.grouped['grouped']['group_overlap'],0)
    def test_group_cv_length(self):self.assertEqual(len(self.grouped['group_cv_balanced']),5)
    def test_group_cv_nontrivial(self):self.assertTrue(np.isfinite(self.grouped['group_cv_balanced']).all())
    def test_group_holdout_lower(self):self.assertLess(self.grouped['grouped']['balanced_accuracy'],self.grouped['random']['balanced_accuracy'])


class TestExamples(unittest.TestCase):
    def test_curve_degree(self):
        ds,es,choice,test=curve_example.run(load_curve())
        self.assertEqual(ds,[1,3,5,9,14,24]);self.assertEqual(choice,5)
    def test_curve_test_rmse(self):
        ds,es,choice,test=curve_example.run(load_curve());self.assertTrue(.2<test<.5)
    def test_curve_overfit(self):
        ds,es,choice,test=curve_example.run(load_curve());self.assertGreater(es[-1],es[2])
    def test_grid_params(self):
        result=grid_example.run(load_alerts())
        self.assertIn(result['params']['knn__n_neighbors'],[3,7,15,31])
        self.assertIn(result['params']['knn__weights'],['uniform','distance'])
    def test_grid_f1(self):
        result=grid_example.run(load_alerts())
        self.assertTrue(0<=result['test_f1']<=1)


if __name__ == '__main__': unittest.main()
