"""Chapter 08: Weather Data Processing System 실행 진입점."""

import argparse
from pathlib import Path

from processing.pipeline import run_pipeline


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="기상 관측 데이터 검증 및 집계")
    parser.add_argument("--data-dir", type=Path, default=root / "data", help="원본 파일 폴더")
    parser.add_argument("--output-dir", type=Path, default=root / "output", help="결과 저장 폴더")
    parser.add_argument("--parquet", action="store_true", help="PyArrow를 이용한 Parquet 저장 추가")
    args = parser.parse_args()
    result = run_pipeline(args.data_dir, args.output_dir, parquet=args.parquet)
    report = result.report
    print(f"Raw: {report['total_raw_rows']} | Accepted: {report['accepted_rows']} | "
          f"Review: {report['review_rows']} | Rejected: {report['rejected_rows']}")
    print(f"Coverage: {report['valid_observations']}/{report['expected_observation_slots']} "
          f"({report['coverage_pct']:.2f}%)")
    print(f"Output: {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
