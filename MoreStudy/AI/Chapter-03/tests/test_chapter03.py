"""Chapter 03 학습 자료의 단위 테스트."""
import sys
import unittest
from pathlib import Path
import tempfile
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "solutions"))
import practice_01_binary_threshold as p1
import practice_02_nearest_centroid as p2
import practice_03_cluster_means as p3
import mini_01_ticket_classification as mini1
import mini_02_station_clustering as mini2
import advanced_01_classification_vs_clustering as adv1
import advanced_02_density_clustering as adv2

class PracticeTests(unittest.TestCase):
    def test_threshold_boundaries(self):
        np.testing.assert_array_equal(p1.predict_labels([.0, .5, 1.0]), [0, 1, 1])
    def test_threshold_custom(self):
        np.testing.assert_array_equal(p1.predict_labels([.3,.6,.9], .7), [0,0,1])
    def test_threshold_empty(self):
        np.testing.assert_array_equal(p1.predict_labels([]), [])
    def test_threshold_invalid_probability(self):
        with self.assertRaises(ValueError): p1.predict_labels([1.01])
    def test_threshold_invalid_finite(self):
        with self.assertRaises(ValueError): p1.predict_labels([np.nan])
    def test_threshold_invalid_range(self):
        with self.assertRaises(ValueError): p1.predict_labels([.2],1.1)
    def test_threshold_invalid_dimensions(self):
        with self.assertRaises(ValueError): p1.predict_labels([[.2]])
    def test_assign_centers(self):
        np.testing.assert_array_equal(p2.assign_clusters([[0,1],[9,9],[2,2]], [[0,0],[10,10]]),[0,1,0])
    def test_assign_tie_first(self):
        np.testing.assert_array_equal(p2.assign_clusters([[1,0]], [[0,0],[2,0]]),[0])
    def test_assign_invalid_shape(self):
        with self.assertRaises(ValueError): p2.assign_clusters([[1,0]], [[0,0,1]])
    def test_assign_no_centers(self):
        with self.assertRaises(ValueError): p2.assign_clusters([[1,0]], np.empty((0,2)))
    def test_centroid_update(self):
        np.testing.assert_allclose(p3.update_centers([[0,0],[2,2],[8,8],[10,10]], [0,0,1,1],2), [[1,1],[9,9]])
    def test_centroid_empty_cluster(self):
        with self.assertRaises(ValueError): p3.update_centers([[1,1]], [0],2)
    def test_centroid_illegal_label(self):
        with self.assertRaises(ValueError): p3.update_centers([[1,1]], [-1],1)

class Mini01Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = mini1.load_data(); cls.result = mini1.train_model(cls.df)
    def test_count(self): self.assertEqual(len(self.df),480)
    def test_unique_ids(self): self.assertTrue(self.df.ticket_id.is_unique)
    def test_label_binary(self): self.assertEqual(set(self.df.urgent.unique()),{0,1})
    def test_predictions_length(self): self.assertEqual(len(self.result['predicted']),120)
    def test_probability_range(self): self.assertTrue(np.all((self.result['probabilities']>=0)&(self.result['probabilities']<=1)))
    def test_accuracy_bounds(self): self.assertGreaterEqual(self.result['accuracy'],.7)
    def test_confusion_total(self): self.assertEqual(self.result['confusion'].sum(),120)
    def test_result_reproducible(self):
        self.assertAlmostEqual(self.result['accuracy'],mini1.train_model(self.df)['accuracy'])
    def test_duplicate_rejection(self):
        df=pd.concat([self.df,self.df.iloc[[0]]],ignore_index=True)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'a.csv';df.to_csv(path,index=False)
            with self.assertRaises(ValueError):mini1.load_data(path)
    def test_negative_rejection(self):
        df=self.df.copy();df.loc[0,'waiting_hours']=-1
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'a.csv';df.to_csv(path,index=False)
            with self.assertRaises(ValueError):mini1.load_data(path)
    def test_missing_feature_rejection(self):
        df=self.df.drop(columns=['failed_attempts'])
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'a.csv';df.to_csv(path,index=False)
            with self.assertRaises(ValueError):mini1.load_data(path)

class Mini02Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df=mini2.load_data();cls.result=mini2.cluster_stations(cls.df)
    def test_count(self):self.assertEqual(len(self.df),270)
    def test_clusters(self):self.assertEqual(len(np.unique(self.result['labels'])),3)
    def test_cluster_counts(self):self.assertEqual(int(self.result['counts'].sum()),270)
    def test_cluster_profile_columns(self):self.assertEqual(list(self.result['profile'].columns),mini2.FEATURES)
    def test_cluster_reproducible(self):
        np.testing.assert_array_equal(self.result['labels'],mini2.cluster_stations(self.df)['labels'])
    def test_no_negative(self): self.assertTrue((self.df[mini2.FEATURES]>=0).all().all())
    def test_duplicate_rejection(self):
        df=self.df.copy();df.loc[1,'station_id']=df.loc[0,'station_id']
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'a.csv';df.to_csv(path,index=False)
            with self.assertRaises(ValueError):mini2.load_data(path)

class Advanced01Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.df=adv1.load_data();cls.result=adv1.compare_methods(cls.df)
    def test_count(self):self.assertEqual(len(self.df),540)
    def test_accuracy(self):self.assertGreater(self.result['accuracy'],.6)
    def test_ari_range(self):self.assertLessEqual(self.result['ari'],1.0)
    def test_ari_not_accuracy(self):self.assertLess(self.result['ari'],self.result['accuracy'])
    def test_label_classes(self):self.assertEqual(set(self.df.work_mode.unique()),{0,1,2})
    def test_clusters(self):self.assertEqual(len(set(self.result['groups'])),3)
    def test_reproducible(self): self.assertAlmostEqual(self.result['ari'],adv1.compare_methods(self.df)['ari'])

class Advanced02Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.df=adv2.load_data();cls.result=adv2.compare_clusters(cls.df)
    def test_count(self):self.assertEqual(len(self.df),464)
    def test_labels_include_noise(self):self.assertIn(-1,set(self.result['reference']))
    def test_kmeans_two_clusters(self):self.assertEqual(len(set(self.result['kmeans'])),2)
    def test_dbscan_noise(self):self.assertGreater(self.result['dbscan_noise'],0)
    def test_dbscan_two_groups(self):self.assertEqual(self.result['dbscan_clusters'],2)
    def test_ari_improvement(self):self.assertGreater(self.result['dbscan_ari'],self.result['kmeans_ari'])
    def test_dbscan_reproducible(self):
        np.testing.assert_array_equal(self.result['dbscan'],adv2.compare_clusters(self.df)['dbscan'])
    def test_invalid_reference(self):
        df=self.df.copy();df.loc[0,'reference_group']=3
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'a.csv';df.to_csv(path,index=False)
            with self.assertRaises(ValueError):adv2.load_data(path)

class FigureTests(unittest.TestCase):
    def test_mini_01_graph(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertTrue(mini1.plot_result(mini1.train_model(mini1.load_data()),Path(d)/'a.png').exists())
    def test_mini_02_graph(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertTrue(mini2.plot_result(mini2.cluster_stations(mini2.load_data()),Path(d)/'a.png').exists())
    def test_advanced_01_graph(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertTrue(adv1.plot_result(adv1.compare_methods(adv1.load_data()),Path(d)/'a.png').exists())
    def test_advanced_02_graph(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertTrue(adv2.plot_result(adv2.compare_clusters(adv2.load_data()),Path(d)/'a.png').exists())

if __name__=='__main__': unittest.main()
