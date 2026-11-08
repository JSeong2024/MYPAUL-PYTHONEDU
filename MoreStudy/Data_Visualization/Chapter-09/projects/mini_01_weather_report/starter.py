"""Mini Project 01 — Weather Visualization Report (student starter)."""
from __future__ import annotations
import argparse
from pathlib import Path

def read_weather(*args, **kwargs):
    """Read weather."""
    raise NotImplementedError("read_weather: 해당 STEP을 구현하세요.")

def render_weather_report(*args, **kwargs):
    """Render weather report."""
    raise NotImplementedError("render_weather_report: 해당 STEP을 구현하세요.")

def main():
    parser = argparse.ArgumentParser(description="Weather Visualization Report")
    parser.add_argument("--data", type=Path, default=Path(__file__).parent / "data")
    parser.add_argument("--output", type=Path, default=Path(__file__).parents[2] / "output" / "mini_01_weather_report")
    args = parser.parse_args()
    # STEP 01부터 구현한 함수를 이곳에서 연결하세요.
    raise NotImplementedError("프로젝트 README의 요구사항을 순서대로 구현하세요.")

if __name__ == "__main__":
    main()
