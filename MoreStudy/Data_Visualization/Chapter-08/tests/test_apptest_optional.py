"""선택적 Streamlit AppTest. Streamlit 설치 환경에서만 실행됩니다."""
from pathlib import Path
import importlib.util
import unittest
ROOT=Path(__file__).resolve().parents[1]
try:
    from streamlit.testing.v1 import AppTest
except ImportError:
    AppTest=None

@unittest.skipUnless(AppTest is not None,'Streamlit 미설치 — AppTest 검증 건너뜀')
class AppTests(unittest.TestCase):
    def test_first_app(self):
        app=AppTest.from_file(str(ROOT/'examples/01_first_app.py'),default_timeout=15).run()
        self.assertFalse(app.exception)
        self.assertTrue(any('Store Snapshot' in x.value for x in app.title))
    def test_metrics(self):
        app=AppTest.from_file(str(ROOT/'examples/03_metrics_columns.py'),default_timeout=15).run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.metric),3)
    def test_store_selector(self):
        app=AppTest.from_file(str(ROOT/'examples/04_selectbox.py'),default_timeout=15).run()
        self.assertFalse(app.exception)
        app.selectbox[0].select('Harbor').run()
        self.assertFalse(app.exception)
    def test_session_counter(self):
        app=AppTest.from_file(str(ROOT/'examples/13_session_state.py'),default_timeout=15).run()
        self.assertFalse(app.exception)
        app.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state['count'],1)
