"""Deterministic validation tests. Run from Chapter-09 with unittest discover."""
from __future__ import annotations
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
import sys
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core.analytics import (
    DATA,read_csv,verify_unique_reference,classify_slots,expected_coverage,
    weather_summary,retail_summary,latency_summary,electricity_summary,metro_summary,
    flight_summary,transit_summary)
from solutions.challenge_03_transit_reliability.reliability_engine import (
    Policy,validate_references,quality_gate,daily_completeness,export_manifest)
from solutions.challenge_03_transit_reliability.cli import run

class DataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.weather=weather_summary()
        cls.retail=retail_summary()
        cls.service=latency_summary()
        cls.electricity=electricity_summary()
        cls.metro=metro_summary()
        cls.flights=flight_summary()
        cls.transit=transit_summary()

    def test_input_csv_schema(self):
        for name,cols in [('stations.csv',['station_id','region']),('transit_operations.csv',['stop_id','timestamp_kst','boardings']),('retail_orders.csv',['store_id','quantity'])]:
            self.assertTrue(set(cols).issubset(read_csv(name).columns))
    def test_station_reference_unique(self):verify_unique_reference(read_csv('stations.csv'),'station_id')
    def test_transit_reference_unique(self):verify_unique_reference(read_csv('transit_stops.csv'),'stop_id')
    def test_reference_duplicate_rejected(self):
        frame=pd.DataFrame({'id':['A','A']})
        with self.assertRaises(ValueError):verify_unique_reference(frame,'id')
    def test_reference_missing_rejected(self):
        frame=pd.DataFrame({'id':['A',None]})
        with self.assertRaises(ValueError):verify_unique_reference(frame,'id')
    def test_invalid_schema_rejected(self):
        with self.assertRaises(ValueError):classify_slots(pd.DataFrame({'x':[1]}),entity_col='station',timestamp_col='time',measures={'v':(0,3)},valid_entities={'A'})
    def test_ambiguous_duplicate_removed_both(self):
        f=pd.DataFrame({'station':['A','A'],'time':['2026-09-01 09:00']*2,'v':[1,2]})
        a,b=classify_slots(f,entity_col='station',timestamp_col='time',measures={'v':(0,10)},valid_entities={'A'},expected_times={9})
        self.assertEqual((len(a),len(b)),(0,2))
        self.assertTrue(b['_reason'].str.contains('duplicate_slot').all())
    def test_negative_measure_excluded(self):
        f=pd.DataFrame({'station':['A'],'time':['2026-09-01 09:00'],'v':[-1]})
        a,b=classify_slots(f,entity_col='station',timestamp_col='time',measures={'v':(0,10)},valid_entities={'A'})
        self.assertEqual((len(a),len(b)),(0,1))
    def test_unknown_entity_excluded(self):
        f=pd.DataFrame({'station':['X'],'time':['2026-09-01 09:00'],'v':[1]})
        a,b=classify_slots(f,entity_col='station',timestamp_col='time',measures={'v':(0,10)},valid_entities={'A'})
        self.assertIn('unknown_entity',b.iloc[0]['_reason'])
    def test_invalid_timestamp_excluded(self):
        f=pd.DataFrame({'station':['A'],'time':['???'],'v':[1]})
        a,b=classify_slots(f,entity_col='station',timestamp_col='time',measures={'v':(0,10)},valid_entities={'A'})
        self.assertIn('invalid_timestamp',b.iloc[0]['_reason'])
    def test_unexpected_hour_excluded(self):
        f=pd.DataFrame({'station':['A'],'time':['2026-09-01 15:00'],'v':[1]})
        a,b=classify_slots(f,entity_col='station',timestamp_col='time',measures={'v':(0,10)},valid_entities={'A'},expected_times={9})
        self.assertIn('unexpected_hour',b.iloc[0]['_reason'])
    def test_nonfinite_excluded(self):
        f=pd.DataFrame({'station':['A'],'time':['2026-09-01 09:00'],'v':['inf']})
        a,b=classify_slots(f,entity_col='station',timestamp_col='time',measures={'v':(0,10)},valid_entities={'A'})
        self.assertEqual(len(a),0)
    def test_weather_count(self):self.assertEqual((len(self.weather[0]),len(self.weather[1])),(236,4))
    def test_weather_coverage(self):self.assertEqual((len(self.weather[3]),int(self.weather[3].available.sum())),(240,236))
    def test_weather_precipitation_nonnegative(self):self.assertTrue(self.weather[0].precipitation_mm.ge(0).all())
    def test_weather_daily_count(self):self.assertEqual(len(self.weather[2]),120)
    def test_retail_completed(self):self.assertTrue(self.retail[0].status.eq('completed').all())
    def test_retail_revenue(self):self.assertEqual(int(self.retail[0].revenue_krw.sum()),33240800)
    def test_retail_group_sum(self):self.assertEqual(int(self.retail[1].revenue_krw.sum()),33240800)
    def test_service_count(self):self.assertEqual(len(self.service[0]),2100)
    def test_service_error_rate(self):self.assertTrue(self.service[1].error_rate.between(0,1).all())
    def test_service_p95_gte_median(self):self.assertTrue((self.service[1].p95_ms>=self.service[1].median_ms).all())
    def test_electricity_count(self):self.assertEqual((len(self.electricity[0]),len(self.electricity[1])),(2874,3))
    def test_electricity_kst_zone(self):self.assertIn('Seoul',str(self.electricity[0].timestamp_kst.dt.tz))
    def test_electricity_negative_excluded(self):self.assertTrue(self.electricity[0].demand_mw.ge(0).all())
    def test_metro_coverage(self):self.assertEqual((len(self.metro[3]),int(self.metro[3].available.sum())),(3240,3232))
    def test_metro_accounting(self):self.assertEqual(len(self.metro[0])+len(self.metro[1]),len(read_csv('metro_boardings.csv')))
    def test_metro_no_duplicate_slot(self):self.assertFalse(self.metro[0].duplicated(['station_id','_parsed']).any())
    def test_flight_count(self):self.assertEqual(len(self.flights[0]),1078)
    def test_flight_flags_consistent(self):self.assertTrue((self.flights[0].late_flag==self.flights[0].delay_min.gt(15).astype(int)).all())
    def test_transit_count(self):self.assertEqual((len(self.transit[0]),len(self.transit[1])),(6106,8))
    def test_transit_coverage(self):self.assertEqual((len(self.transit[3]),int(self.transit[3].available.sum())),(6120,6106))
    def test_transit_no_duplicate_slot(self):self.assertFalse(self.transit[0].duplicated(['stop_id','_parsed']).any())
    def test_transit_nonnegative(self):self.assertTrue((self.transit[0].boardings>=0).all())
    def test_transit_incidents_count(self):self.assertEqual(len(self.transit[4]),90)
    def test_missing_slot_not_zero(self):
        slots=self.transit[3]
        self.assertEqual(int((~slots.available).sum()),14)
    def test_quality_gate_valid(self):
        a,b,d,s,i=self.transit
        quality_gate(a,b,s,len(read_csv('transit_operations.csv')))
    def test_quality_gate_bad_raw_count(self):
        a,b,d,s,i=self.transit
        with self.assertRaises(AssertionError):quality_gate(a,b,s,999)
    def test_quality_gate_bad_slot_count(self):
        a,b,d,s,i=self.transit
        with self.assertRaises(AssertionError):quality_gate(a,b,s.head(10),len(read_csv('transit_operations.csv')))
    def test_daily_completeness(self):
        days=daily_completeness(self.transit[3]);self.assertEqual(len(days),360)
        self.assertTrue(days.expected_hours.eq(17).all())
    def test_references_valid(self):validate_references(read_csv('transit_stops.csv'),read_csv('transit_incidents.csv'))
    def test_reference_bad_incident(self):
        i=read_csv('transit_incidents.csv').copy();i.loc[0,'stop_id']='X99'
        with self.assertRaises(ValueError):validate_references(read_csv('transit_stops.csv'),i)
    def test_reference_bad_duration(self):
        i=read_csv('transit_incidents.csv').copy();i.loc[0,'duration_min']=-1
        with self.assertRaises(ValueError):validate_references(read_csv('transit_stops.csv'),i)
    def test_reference_duplicate_stop(self):
        s=pd.concat([read_csv('transit_stops.csv')]*2,ignore_index=True)
        with self.assertRaises(ValueError):validate_references(s,read_csv('transit_incidents.csv'))
    def test_cli_two_stops(self):
        with tempfile.TemporaryDirectory() as td:
            rep=run(Path(td),['X01','X07'])
            self.assertEqual(rep['expected_slots'],1020)
            self.assertEqual(rep['accepted_slots'],1012)
            self.assertTrue((Path(td)/'manifest.json').exists())
    def test_cli_unknown_stop(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):run(Path(td),['X99'])
    def test_cli_empty_selection(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):run(Path(td),[])
    def test_cli_manifest_deterministic(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            run(Path(a),['X01','X07']);run(Path(b),['X01','X07'])
            self.assertEqual((Path(a)/'manifest.json').read_bytes(),(Path(b)/'manifest.json').read_bytes())
    def test_cli_output_files(self):
        with tempfile.TemporaryDirectory() as td:
            run(Path(td),['X02'])
            for name in ['report.json','complete_day_totals.csv','daily_completeness.csv','selected_coverage.png','excluded_rows.csv','manifest.json']:
                self.assertTrue((Path(td)/name).is_file(),name)

if __name__=='__main__':unittest.main()
