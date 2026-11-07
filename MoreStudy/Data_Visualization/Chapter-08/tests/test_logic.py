"""Streamlit 설치 없이 실행되는 데이터 로직 테스트."""
import io
from pathlib import Path
import sys
import unittest
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import (read_retail, read_service, read_tickets, select_dates,
                            select_retail, retail_summary,retail_charts,
                            service_summary, service_charts,ticket_summary,tickets_charts,
                            date_bounds, as_csv_bytes,parse_uploaded_retail)
from core.metro import (load_reference,load_raw,validate_metro,filter_metro,
                        metro_summary,metro_charts,missing_dates)

class RetailTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.df=read_retail()
    def test_01_length(self):self.assertEqual(len(self.df),540)
    def test_02_total_sales(self):self.assertEqual(retail_summary(self.df)['revenue_krw'],33046600)
    def test_03_total_quantity(self):self.assertEqual(retail_summary(self.df)['quantity'],12184)
    def test_04_observed_days(self):self.assertEqual(retail_summary(self.df)['days'],45)
    def test_05_store_filter(self):self.assertEqual(len(select_retail(self.df,stores=['Central'])),135)
    def test_06_multi_store(self):self.assertEqual(len(select_retail(self.df,stores=['Central','Harbor'])),270)
    def test_07_category(self):self.assertEqual(len(select_retail(self.df,categories=['Coffee'])),180)
    def test_08_empty_selection(self):self.assertTrue(select_retail(self.df,stores=[]).empty)
    def test_09_date_inclusive(self):self.assertEqual(len(select_retail(self.df,start='2026-09-01',end='2026-09-03')),36)
    def test_10_single_day(self):self.assertEqual(len(select_retail(self.df,start='2026-10-01',end='2026-10-01')),12)
    def test_11_bad_date_window(self):
        with self.assertRaises(ValueError):select_dates(self.df,'date','2026-10-01','2026-09-01')
    def test_12_empty_summary(self):self.assertEqual(retail_summary(self.df.iloc[0:0])['revenue_krw'],0)
    def test_13_figure_trace(self):
        a,b=retail_charts(self.df);self.assertGreater(len(a.data),0);self.assertGreater(len(b.data),0)
    def test_14_bytes_bom(self):self.assertTrue(as_csv_bytes(self.df).startswith(b'\xef\xbb\xbf'))
    def test_15_roundtrip(self):
        content=as_csv_bytes(self.df);parsed=parse_uploaded_retail(content)
        self.assertEqual(retail_summary(parsed)['revenue_krw'],33046600)
    def test_16_upload_empty(self):
        with self.assertRaises(ValueError):parse_uploaded_retail(b'')
    def test_17_upload_too_large(self):
        with self.assertRaises(ValueError):parse_uploaded_retail(b'abc',max_size=2)
    def test_18_upload_missing_columns(self):
        with self.assertRaises(ValueError):parse_uploaded_retail(b'foo,bar\n1,2\n')
    def test_19_upload_negative(self):
        bad=self.df.head(1).copy();bad.loc[bad.index[0],'quantity']=-3
        with self.assertRaises(ValueError):parse_uploaded_retail(as_csv_bytes(bad))
    def test_20_upload_bad_number(self):
        bad=self.df.head(1).copy();bad['revenue_krw']='oops'
        with self.assertRaises(ValueError):parse_uploaded_retail(as_csv_bytes(bad))
    def test_21_upload_mismatch_revenue(self):
        bad=self.df.head(1).copy();bad['revenue_krw']=12
        with self.assertRaises(ValueError):parse_uploaded_retail(as_csv_bytes(bad))
    def test_22_upload_bad_date(self):
        bad=self.df.head(1).copy();bad['date']='invalid-date'
        with self.assertRaises(ValueError):parse_uploaded_retail(as_csv_bytes(bad))
    def test_23_upload_fractional_quantity(self):
        bad=self.df.head(1).copy();bad['quantity']=1.5;bad['revenue_krw']=1.5*bad['unit_price_krw']
        with self.assertRaises(ValueError):parse_uploaded_retail(as_csv_bytes(bad))
    def test_24_date_bounds(self):self.assertEqual(date_bounds(self.df,'date'),(pd.Timestamp('2026-09-01').date(),pd.Timestamp('2026-10-15').date()))

class ServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.df=read_service()
    def test_01_rows(self):self.assertEqual(len(self.df),1005)
    def test_02_requests(self):self.assertEqual(service_summary(self.df)['requests'],107369)
    def test_03_errors(self):self.assertEqual(service_summary(self.df)['errors'],1436)
    def test_04_rate(self):self.assertAlmostEqual(service_summary(self.df)['error_rate_pct'],1436/107369*100)
    def test_05_hours(self):self.assertEqual(service_summary(self.df)['hours'],336)
    def test_06_negative_guard(self):
        invalid=self.df.head(2).copy();invalid.loc[invalid.index[0],'requests']=-1
        path=ROOT/'tests'/'_temp_service.csv'
        try:
            invalid.to_csv(path,index=False)
            with self.assertRaises(ValueError):read_service(path)
        finally:path.unlink(missing_ok=True)
    def test_07_more_errors_than_requests(self):
        invalid=self.df.head(1).copy();invalid.loc[invalid.index[0],'errors']=99999
        path=ROOT/'tests'/'_temp_service.csv'
        try:
            invalid.to_csv(path,index=False)
            with self.assertRaises(ValueError):read_service(path)
        finally:path.unlink(missing_ok=True)
    def test_08_empty_rate(self):
        empty=self.df.iloc[0:0]
        self.assertIsNone(service_summary(empty)['error_rate_pct'])
    def test_09_threshold_count(self):self.assertGreater(int(self.df['p95_ms'].gt(250).sum()),0)
    def test_10_figures(self):
        a,b=service_charts(self.df);self.assertGreater(len(a.data),0);self.assertGreater(len(b.data),0)
    def test_11_service_count(self):self.assertEqual(self.df['service'].nunique(),3)
    def test_12_p95_is_nonnegative(self):self.assertTrue((self.df['p95_ms']>=0).all())

class TicketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.df=read_tickets()
    def test_01_rows(self):self.assertEqual(len(self.df),640)
    def test_02_open(self):self.assertEqual(ticket_summary(self.df)['open'],125)
    def test_03_rate(self):self.assertAlmostEqual(ticket_summary(self.df)['open_rate_pct'],125/640*100)
    def test_04_median(self):self.assertEqual(ticket_summary(self.df)['median_response_h'],3.49)
    def test_05_team_count(self):self.assertEqual(self.df['team'].nunique(),4)
    def test_06_unique_tickets(self):self.assertTrue(self.df['ticket_id'].is_unique)
    def test_07_empty_summary(self):self.assertIsNone(ticket_summary(self.df.iloc[0:0])['median_response_h'])
    def test_08_figures(self):
        a,b=tickets_charts(self.df);self.assertGreater(len(a.data),0);self.assertGreater(len(b.data),0)
    def test_09_higher_priorities_present(self):self.assertTrue({'High','Urgent'}.issubset(set(self.df['priority'])))
    def test_10_output_unit(self):self.assertTrue((self.df['first_response_hours']>=0).all())

class MetroTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.st,cls.policy=load_reference();cls.raw=load_raw()
        cls.good,cls.bad,cls.coverage=validate_metro(cls.raw,cls.st,cls.policy)
    def test_01_raw_rows(self):self.assertEqual(len(self.raw),2346)
    def test_02_stations(self):self.assertEqual(len(self.st),7)
    def test_03_expected_slots(self):self.assertEqual(len(self.coverage),2352)
    def test_04_accepted_slots(self):self.assertEqual(len(self.good),2330)
    def test_05_rejected_rows(self):self.assertEqual(len(self.bad),16)
    def test_06_accepted_sum(self):self.assertEqual(metro_summary(self.good,self.coverage)['boardings'],408183)
    def test_07_missing_slots(self):self.assertEqual(metro_summary(self.good,self.coverage)['missing_slots'],22)
    def test_08_rate(self):self.assertAlmostEqual(metro_summary(self.good,self.coverage)['coverage_pct'],2330/2352*100)
    def test_09_unique_accepted(self):self.assertFalse(self.good.duplicated(['station_id','timestamp']).any())
    def test_10_negative_rejected(self):self.assertTrue(self.good['boardings_valid'].ge(0).all())
    def test_11_invalid_reason(self):self.assertIn('invalid_boardings','|'.join(self.bad['reason_codes']))
    def test_12_unknown_station(self):self.assertIn('unknown_station','|'.join(self.bad['reason_codes']))
    def test_13_duplicate_rows(self):self.assertEqual(int(self.bad.reason_codes.str.contains('duplicate_slot').sum()),10)
    def test_14_invalid_time(self):self.assertIn('invalid_time','|'.join(self.bad['reason_codes']))
    def test_15_zero_is_observed(self):
        zero=self.good[self.good['boardings_valid'].eq(0)];self.assertGreater(len(zero),0)
        merged=zero.merge(self.coverage,on=['station_id','timestamp'],validate='one_to_one')
        self.assertTrue(merged['observed'].all())
    def test_16_incomplete_daily(self):self.assertGreater(int(missing_dates(self.coverage)['status'].eq('partial').sum()),0)
    def test_17_no_fully_missing(self):self.assertEqual(int(missing_dates(self.coverage)['status'].eq('missing').sum()),0)
    def test_18_one_station_one_day(self):
        g,c=filter_metro(self.good,self.coverage,[self.st.station_id.iloc[0]],'2026-10-01','2026-10-01')
        self.assertEqual(len(c),24);self.assertLessEqual(len(g),24)
    def test_19_two_stations_range(self):
        g,c=filter_metro(self.good,self.coverage,self.st.station_id.iloc[:2].tolist(),'2026-10-01','2026-10-03')
        self.assertEqual(len(c),2*3*24)
    def test_20_empty_selection(self):
        g,c=filter_metro(self.good,self.coverage,[],self.policy['start_date'],self.policy['end_date'])
        self.assertTrue(g.empty);self.assertTrue(c.empty)
        self.assertIsNone(metro_summary(g,c)['coverage_pct'])
    def test_21_bad_dates(self):
        with self.assertRaises(ValueError):filter_metro(self.good,self.coverage,['M1-Central'],'2026-10-14','2026-10-01')
    def test_22_station_coverage_counts(self):
        for station,g in self.coverage.groupby('station_id'):
            with self.subTest(station=station):self.assertEqual(len(g),14*24)
    def test_23_daily_rows(self):self.assertEqual(len(missing_dates(self.coverage)),7*14)
    def test_24_figure_traces(self):
        figs=metro_charts(self.good,self.coverage,self.st)
        self.assertEqual(len(figs),3)
        for fig in figs:self.assertGreater(len(fig.data),0)
    def test_25_empty_figures(self):self.assertEqual(metro_charts(self.good.iloc[0:0],self.coverage.iloc[0:0],self.st),(None,None,None))
    def test_26_bad_required_column(self):
        with self.assertRaises(ValueError):validate_metro(self.raw.drop(columns=['station_id']),self.st,self.policy)
    def test_27_modified_raw_not_mutated(self):
        before=self.raw.copy(deep=True);validate_metro(self.raw,self.st,self.policy)
        pd.testing.assert_frame_equal(self.raw,before)
    def test_28_duplicate_canonical_time(self):
        new=self.raw.head(1).copy()
        # pandas datetime accepts non-zero-padded hour; different text resolves to same parsed time
        new2=new.copy();new2.loc[new2.index[0],'timestamp_kst']=new.iloc[0]['timestamp_kst'].replace(' 00:', ' 0:')
        s=pd.concat([new,new2],ignore_index=True)
        g,b,c=validate_metro(s,self.st,self.policy)
        self.assertEqual(len(g),0);self.assertEqual(len(b),2)
    def test_29_all_possible_times(self):self.assertTrue((self.coverage['timestamp'].dt.minute==0).all())
    def test_30_raw_issues_not_in_accepted(self):self.assertFalse(set(self.good['source_row']) & set(self.bad['source_row']))

if __name__=='__main__':unittest.main()
