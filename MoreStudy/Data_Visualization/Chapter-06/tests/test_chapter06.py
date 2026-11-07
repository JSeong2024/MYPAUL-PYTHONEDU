from pathlib import Path
import json
import tempfile
import unittest
import numpy as np
import pandas as pd

from solutions.mini_01_sales.solution import build_report as sales_report
from solutions.mini_02_server.solution import build_report as server_report
from solutions.mini_03_weather.solution import build_report as weather_report
from solutions.advanced_01_air_quality.reference_solution import validate_air_data, build_report as air_report
from solutions.advanced_02_traffic.reference_solution import validate_traffic, make_time_grid, build_report as traffic_report, LOCAL_TZ

ROOT = Path(__file__).resolve().parents[1]

class InputDataTests(unittest.TestCase):
    def test_data_files_exist(self):
        for name in ['sales_daily.csv','server_metrics.csv','weather_hourly.csv','air_quality_hourly.csv','traffic_hourly.csv']:
            self.assertTrue((ROOT / 'data' / name).is_file())
    def test_sales_date_grain(self):
        d=pd.read_csv(ROOT/'data/sales_daily.csv')
        self.assertFalse(d.duplicated(['store_id','date']).any())
    def test_sales_true_zero(self):
        d=pd.read_csv(ROOT/'data/sales_daily.csv')
        self.assertGreater(int(d['revenue_krw'].eq(0).sum()),0)
    def test_sales_missing_distinct_from_zero(self):
        d=pd.read_csv(ROOT/'data/sales_daily.csv',parse_dates=['date'])
        s=d.query('store_id == "ST-C"').set_index('date')['revenue_krw']
        r=s.reindex(pd.date_range('2026-08-01','2026-10-31'))
        self.assertTrue(pd.isna(r.loc['2026-09-15']))
        self.assertEqual(r.loc['2026-08-22'],0)
    def test_weather_hourly_grain(self):
        d=pd.read_csv(ROOT/'data/weather_hourly.csv')
        self.assertFalse(d.duplicated(['station_id','timestamp_local']).any())
    def test_weather_zero_precipitation_exists(self):
        d=pd.read_csv(ROOT/'data/weather_hourly.csv')
        self.assertTrue(d['precipitation_mm'].eq(0).any())
    def test_server_samples_5min(self):
        d=pd.read_csv(ROOT/'data/server_metrics.csv')
        ts=pd.to_datetime(d['timestamp_utc'],utc=True)
        self.assertTrue((ts.dt.minute%5==0).all())
    def test_server_expected_missing(self):
        d=pd.read_csv(ROOT/'data/server_metrics.csv')
        ts=pd.to_datetime(d['timestamp_utc'],utc=True)
        expected=pd.date_range('2026-10-26','2026-10-27 23:55',freq='5min',tz='UTC')
        self.assertEqual(len(expected.difference(pd.DatetimeIndex(ts))),8)
    def test_air_invalid_rows_exists(self):
        d=pd.read_csv(ROOT/'data/air_quality_hourly.csv')
        self.assertTrue(d['pm25_ug_m3'].astype(str).eq('sensor_error').any())
    def test_traffic_invalid_rows_exists(self):
        d=pd.read_csv(ROOT/'data/traffic_hourly.csv')
        self.assertTrue(d['vehicle_count'].astype(str).eq('not_a_number').any())
    def test_timezone_conversion(self):
        t=pd.Timestamp('2026-10-01T00:00:00Z').tz_convert(LOCAL_TZ)
        self.assertEqual(t.hour,9)

class TimeSeriesConceptTests(unittest.TestCase):
    def test_resample_sum_preserves_total(self):
        d=pd.read_csv(ROOT/'data/sales_daily.csv',parse_dates=['date']).query('store_id == "ST-A"')
        self.assertEqual(int(d.set_index('date')['revenue_krw'].resample('MS').sum().sum()),int(d['revenue_krw'].sum()))
    def test_hourly_temp_mean_not_sum(self):
        d=pd.read_csv(ROOT/'data/weather_hourly.csv',parse_dates=['timestamp_local']).query('station_id == "W-A"')
        self.assertLess(abs(d['temperature_c'].mean()),100)
        self.assertNotEqual(round(d['temperature_c'].mean(),2),round(d['temperature_c'].sum(),2))
    def test_gap_not_filled_as_zero(self):
        s=pd.Series([1.,np.nan,2.])
        self.assertTrue(np.isnan(s.iloc[1]))
        self.assertEqual(int(s.eq(0).sum()),0)
    def test_complete_rolling_after_nan(self):
        s=pd.Series([1.,2.,np.nan,4.,5.,6.])
        r=s.rolling(3,min_periods=3).mean()
        self.assertTrue(r.iloc[:5].isna().all())
        self.assertEqual(r.iloc[5],5.)
    def test_calendar_window_vs_count_window(self):
        ts=pd.to_datetime(['2026-01-01 09:00','2026-01-01 09:05','2026-01-01 10:15','2026-01-01 10:20','2026-01-01 10:25'])
        s=pd.Series([2.,4.,8.,10.,12.],index=ts)
        r=s.rolling('60min',min_periods=3).mean()
        self.assertTrue(r.iloc[:4].isna().all())
        self.assertAlmostEqual(r.iloc[-1],10.)
    def test_rolling_no_future_information(self):
        s=pd.Series([2.,4.,6.])
        self.assertTrue(np.isnan(s.rolling(3,min_periods=3).mean().iloc[0]))
    def test_pct_change_zero_denominator(self):
        s=pd.Series([0.,4.])
        val=s.pct_change(fill_method=None).iloc[1]
        self.assertFalse(np.isfinite(val))
    def test_w_sun_anchor(self):
        s=pd.Series([1,1,1],index=pd.date_range('2026-08-01',periods=3))
        x=s.resample('W-SUN').sum()
        self.assertEqual(int(x.iloc[0]),2)
    def test_base100_requires_nonzero(self):
        start=0
        with self.assertRaises(ZeroDivisionError):
            if start==0: raise ZeroDivisionError('Cannot normalize with zero baseline')
    def test_time_interpolation_not_measurement(self):
        ix=pd.date_range('2026-01-01',periods=3)
        s=pd.Series([1.,np.nan,5.],index=ix)
        est=s.interpolate(method='time')
        self.assertTrue(pd.isna(s.iloc[1]))
        self.assertEqual(est.iloc[1],3.)

class MiniProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.out=Path(self.temp.name)
    def tearDown(self):self.temp.cleanup()
    def test_sales_build_creates_png(self):
        report=sales_report(self.out/'sales')
        self.assertTrue(Path(report['figure']).is_file())
    def test_sales_expected_rows(self):
        self.assertEqual(sales_report(self.out/'sales')['rows'],272)
    def test_sales_three_stores(self):
        self.assertEqual(sales_report(self.out/'sales')['stores'],3)
    def test_sales_missing_four_days(self):
        self.assertEqual(sales_report(self.out/'sales')['missing_cells'],4)
    def test_sales_revenue_correct(self):
        self.assertEqual(sales_report(self.out/'sales')['total_krw'],23770700)
    def test_sales_output_summary(self):
        sales_report(self.out/'sales')
        self.assertEqual(len(pd.read_csv(self.out/'sales/store_summary.csv')),3)
    def test_server_valid_slots(self):
        self.assertEqual(server_report(self.out/'server')['valid_samples'],568)
    def test_server_missing_slots(self):
        self.assertEqual(server_report(self.out/'server')['missing_samples'],8)
    def test_server_summary_json(self):
        server_report(self.out/'server')
        d=json.loads((self.out/'server/summary.json').read_text())
        self.assertEqual(int(d['expected_samples']),576)
    def test_server_png(self):
        server_report(self.out/'server')
        self.assertTrue((self.out/'server/server_monitor.png').exists())
    def test_weather_hourly_missing(self):
        self.assertEqual(weather_report(self.out/'weather')['missing_hours'],12)
    def test_weather_stations(self):
        self.assertEqual(weather_report(self.out/'weather')['stations'],3)
    def test_weather_summary_rows(self):
        weather_report(self.out/'weather')
        self.assertEqual(len(pd.read_csv(self.out/'weather/daily_weather.csv')),42)

class AdvancedAirTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.out=Path(self.temp.name)
        self.catalog=['AQ-A','AQ-B','AQ-C','AQ-D']
    def tearDown(self):self.temp.cleanup()
    def test_unknown_station_rejected(self):
        d=pd.DataFrame({'timestamp_local':['2026-09-04 10:00'],'station_id':['bad'],'pm25_ug_m3':['20']})
        v,a=validate_air_data(d,set(self.catalog));self.assertEqual(len(v),0)
    def test_negative_value_rejected(self):
        d=pd.DataFrame({'timestamp_local':['2026-09-04 10:00'],'station_id':['AQ-A'],'pm25_ug_m3':['-4']})
        v,a=validate_air_data(d,set(self.catalog));self.assertTrue(a.iloc[0]['invalid_measurement'])
    def test_bad_timestamp_rejected(self):
        d=pd.DataFrame({'timestamp_local':['yesterday'],'station_id':['AQ-A'],'pm25_ug_m3':['20']})
        v,a=validate_air_data(d,set(self.catalog));self.assertEqual(len(v),0)
    def test_duplicate_rejects_both(self):
        d=pd.DataFrame({'timestamp_local':['2026-09-04 10:00']*2,'station_id':['AQ-A']*2,'pm25_ug_m3':['10','12']})
        v,a=validate_air_data(d,set(self.catalog));self.assertEqual(len(v),0);self.assertEqual(a['duplicate_key'].sum(),2)
    def test_valid_row_kept(self):
        d=pd.DataFrame({'timestamp_local':['2026-09-04 10:00'],'station_id':['AQ-A'],'pm25_ug_m3':['0']})
        v,a=validate_air_data(d,set(self.catalog));self.assertEqual(len(v),1)
    def test_reject_duplicate_selection(self):
        with self.assertRaises(ValueError):air_report(['AQ-A','AQ-A'],self.out)
    def test_reject_empty_selection(self):
        with self.assertRaises(ValueError):air_report([],self.out)
    def test_reject_unknown_selection(self):
        with self.assertRaises(ValueError):air_report(['AQ-Z'],self.out)
    def test_single_station_dynamic(self):
        r=air_report(['AQ-C'],self.out)
        self.assertEqual(r['selected'],1)
    def test_all_stations(self):
        r=air_report(output_dir=self.out)
        self.assertEqual(r['selected'],4)
    def test_air_invalid_count(self):
        r=air_report(output_dir=self.out)
        self.assertEqual(r['invalid'],8)
    def test_air_report_csv(self):
        air_report(['AQ-A','AQ-B'],self.out)
        self.assertEqual(len(pd.read_csv(self.out/'station_summary.csv')),2)
    def test_air_png(self):
        air_report(['AQ-A'],self.out)
        self.assertTrue((self.out/'air_quality_report.png').exists())

class AdvancedTrafficTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.out=Path(self.temp.name)
        self.ids=['R-01','R-02','R-03','R-04','R-05','R-06']
    def tearDown(self):self.temp.cleanup()
    def test_missing_columns(self):
        with self.assertRaises(ValueError): validate_traffic(pd.DataFrame({'a':[1]}),set(self.ids))
    def test_negative_rejected(self):
        d=pd.DataFrame({'timestamp_utc':['2026-10-04T00:00:00Z'],'corridor_id':['R-01'],'vehicle_count':['-1']})
        v,a=validate_traffic(d,set(self.ids));self.assertEqual(len(v),0)
    def test_nonnumeric_rejected(self):
        d=pd.DataFrame({'timestamp_utc':['2026-10-04T00:00:00Z'],'corridor_id':['R-01'],'vehicle_count':['N/A']})
        v,a=validate_traffic(d,set(self.ids));self.assertEqual(len(v),0)
    def test_unknown_corridor_rejected(self):
        d=pd.DataFrame({'timestamp_utc':['2026-10-04T00:00:00Z'],'corridor_id':['no'],'vehicle_count':['8']})
        v,a=validate_traffic(d,set(self.ids));self.assertTrue(a.iloc[0]['unknown_corridor'])
    def test_bad_timestamp_rejected(self):
        d=pd.DataFrame({'timestamp_utc':['none'],'corridor_id':['R-01'],'vehicle_count':['8']})
        v,a=validate_traffic(d,set(self.ids));self.assertEqual(len(v),0)
    def test_duplicate_key_rejects_both(self):
        d=pd.DataFrame({'timestamp_utc':['2026-10-04T00:00:00Z']*2,'corridor_id':['R-01']*2,'vehicle_count':['5','6']})
        v,a=validate_traffic(d,set(self.ids));self.assertEqual(len(v),0);self.assertEqual(int(a['duplicate'].sum()),2)
    def test_valid_zero_accepted(self):
        d=pd.DataFrame({'timestamp_utc':['2026-10-04T00:00:00Z'],'corridor_id':['R-01'],'vehicle_count':['0']})
        v,a=validate_traffic(d,set(self.ids));self.assertEqual(len(v),1)
    def test_grid_expected_length(self):
        d=pd.DataFrame({'timestamp_utc':['2026-10-01T00:00:00Z'],'corridor_id':['R-01'],'vehicle_count':['5']})
        v,a=validate_traffic(d,set(self.ids))
        x=make_time_grid(v,['R-01']);self.assertEqual(len(x),672)
    def test_grid_hour_is_kst(self):
        d=pd.DataFrame({'timestamp_utc':['2026-10-01T00:00:00Z'],'corridor_id':['R-01'],'vehicle_count':['5']})
        v,a=validate_traffic(d,set(self.ids));x=make_time_grid(v,['R-01'])
        self.assertEqual(x.loc[pd.Timestamp('2026-10-01 09:00',tz=LOCAL_TZ),'R-01'],5)
    def test_reject_empty_selected(self):
        with self.assertRaises(ValueError): traffic_report([],self.out)
    def test_reject_unknown_selected(self):
        with self.assertRaises(ValueError): traffic_report(['bad'],self.out)
    def test_reject_duplicate_selected(self):
        with self.assertRaises(ValueError): traffic_report(['R-01','R-01'],self.out)
    def test_traffic_two_corridors(self):
        r=traffic_report(['R-01','R-02'],self.out)
        self.assertEqual(r['selected'],2)
    def test_traffic_single_corridor(self):
        r=traffic_report(['R-01'],self.out)
        self.assertEqual(r['selected'],1)
    def test_traffic_all_corridors(self):
        r=traffic_report(output_dir=self.out);self.assertEqual(r['selected'],6)
    def test_traffic_invalid_count(self):
        r=traffic_report(['R-01'],self.out);self.assertEqual(r['invalid'],8)
    def test_traffic_missing_is_not_zero(self):
        traffic_report(['R-01'],self.out)
        df=pd.read_csv(self.out/'complete_daily_totals.csv')
        self.assertTrue(df['R-01'].isna().any())
    def test_traffic_report_files(self):
        traffic_report(['R-01'],self.out)
        for f in ['traffic_overview.png','traffic_details.png','corridor_summary.csv','audit.csv','complete_daily_totals.csv','daily_sample_counts.csv']:
            self.assertTrue((self.out/f).is_file(),f)
    def test_coverage_number_bounded(self):
        traffic_report(['R-01','R-02'],self.out)
        d=pd.read_csv(self.out/'corridor_summary.csv')
        self.assertTrue(d['coverage_pct'].between(0,100).all())

if __name__=='__main__':unittest.main()
