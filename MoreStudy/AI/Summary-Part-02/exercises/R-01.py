"""R-01 — The Last Checkpoint

입력: sites.csv, history.csv, R-01/incoming.csv
학습·검증·테스트의 역할과 실패 시 파일 보존 조건을 확인하세요.
"""
from pathlib import Path
import argparse
import torch
import numpy as np
import pandas as pd

def solve(data_dir: Path, output_dir: Path, mode: str = "run") -> None:
    # STEP 1: 입력 스키마 및 데이터 계약 점검
    # TODO: 두 모델, Epoch Resume, 승인·배포·Rollback, Benchmark
    # STEP 2: 모델 또는 Tensor 처리
    # TODO: Validation에서만 모델·Threshold 선택 (해당 문제)
    # STEP 3: 출력 규격 및 오류 처리
    # TODO: 성공 검증 전 기존 정상 결과물을 덮어쓰지 않기
    raise NotImplementedError("R-01 구현")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path(__file__).resolve().parents[1] / "data")
    parser.add_argument("--out", type=Path, default=Path("outputs") / "R-01")
    parser.add_argument("--mode", default="run")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    solve(args.data, args.out, args.mode)
