"""같은 계산을 Python 루프와 NumPy로 실행해 소요 시간 비교."""
import timeit
import numpy as np

values = list(range(100_000))
array = np.array(values)

def with_python():
    return [value * 2 + 1 for value in values]

def with_numpy():
    return array * 2 + 1

assert np.array_equal(np.array(with_python()), with_numpy())
t_python = min(timeit.repeat(with_python, number=3, repeat=3))
t_numpy = min(timeit.repeat(with_numpy, number=3, repeat=3))
print("계산 결과 일치: True")
print(f"Python 반복: {t_python * 1000:.2f} ms (3회 호출)")
print(f"NumPy 연산: {t_numpy * 1000:.2f} ms (3회 호출)")
print("측정값은 하드웨어·환경에 따라 달라집니다.")
