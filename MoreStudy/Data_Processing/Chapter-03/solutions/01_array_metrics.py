"""Solution 01 — 정수 측정값 배열의 기본 통계 구하기."""
import numpy as np

def summarize(values: list[int]) -> tuple[int, float, int, int]:
    array = np.array(values, dtype=np.int64)
    if array.size == 0:
        raise ValueError("값이 비어 있습니다.")
    return array.size, float(array.mean()), int(array.min()), int(array.max())

if __name__ == "__main__":
    print(summarize([15, 25, 35, 45]))
