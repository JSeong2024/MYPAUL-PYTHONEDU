"""Exercise 01. 결측치: None/NaN과 빈 문자열·공백 문자열을 모두 검출하세요."""
import pandas as pd


def missing_counts(frame: pd.DataFrame) -> pd.Series:
    # TODO: 원본 frame을 변경하지 않고 각 열의 결측 수를 반환합니다.
    raise NotImplementedError


if __name__ == "__main__":
    demo = pd.DataFrame({"name": ["Kim", "  ", None], "score": [80, 90, None]})
    print(missing_counts(demo))
