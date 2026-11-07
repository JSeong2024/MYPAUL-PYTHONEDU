"""Exercise 05 — 수집 커버리지 계산 함수를 작성하세요."""
import pandas as pd


def calculate_coverage(observations: pd.DataFrame, expected_slots: int) -> float:
    """observations 행 수 / expected_slots * 100을 소수 둘째 자리로 반환하세요.

    expected_slots는 양수여야 하며 아니면 ValueError를 발생시킵니다.
    중복 제거와 품질 검증을 완료한 accepted DataFrame만 입력한다고 가정합니다.
    """
    # TODO: 누락/오류 상태의 데이터는 입력에 포함하지 않습니다.
    raise NotImplementedError


if __name__ == "__main__":
    sample = pd.DataFrame({"observation_id": ["A", "B", "C"]})
    print(calculate_coverage(sample, 4))
