import sys
from pathlib import Path
import tempfile
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project.processing.pipeline import run_pipeline

with tempfile.TemporaryDirectory() as temp_dir:
    result = run_pipeline(ROOT / "data", Path(temp_dir))
    loaded = pd.read_csv(Path(temp_dir) / "daily_station_summary.csv")
    assert len(loaded) == len(result.daily)
    print("Saved daily rows:", len(loaded))
    print("Saved files:", len(list(Path(temp_dir).iterdir())))
