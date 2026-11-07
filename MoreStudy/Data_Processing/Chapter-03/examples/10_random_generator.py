"""새 Generator와 seed로 재현 가능한 수치 실험 만들기."""
import numpy as np

rng = np.random.default_rng(2026)
dice = rng.integers(1, 7, size=8)  # 1~6 정수. upper bound는 제외
noise = rng.normal(loc=0.0, scale=1.0, size=4)
print("주사위:", dice)
print("표준정규 난수:", np.round(noise, 2))

repeated = np.random.default_rng(2026).integers(1, 7, size=8)
print("같은 초기 조건:", np.array_equal(dice, repeated))
