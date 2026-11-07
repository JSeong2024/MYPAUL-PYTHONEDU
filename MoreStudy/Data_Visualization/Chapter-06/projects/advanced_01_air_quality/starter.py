from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def build_report(output_dir=None):
    """Multi-Station Air Quality Report: 요구사항에 맞게 아래 코드를 완성하세요."""
    output = Path(output_dir) if output_dir is not None else ROOT / 'output/advanced_01_air_quality'
    output.mkdir(parents=True, exist_ok=True)
    # TODO 1: 입력 데이터와 관측 단위를 확인합니다.
    # TODO 2: 필요한 검증·시계열 집계 함수를 완성합니다.
    # TODO 3: 그래프·요약 파일을 output에 저장합니다.
    raise NotImplementedError('Complete the project here')


if __name__ == '__main__':
    print(build_report())
