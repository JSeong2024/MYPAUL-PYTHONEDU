"""B-02 — Prediction Error Calculator (Starter Code).

입력: w b; K train targets; N test (x, y)
출력: MODEL_MAE, MODEL_MSE, BASELINE_MAE, BEST
문제 원문: ../problem.md의 B-02 절
"""
import sys


def solve(source: str) -> str:
    """문제의 입력을 받아 정해진 형식의 출력 문자열을 반환합니다."""
    # STEP 1: Training Target에서만 평균 Baseline 산출
    # STEP 2: w*x+b의 Test MAE·MSE 계산
    # STEP 3: Test Baseline MAE와 반올림 전 점수 비교
    raise NotImplementedError("TODO: solve() 구현")


if __name__ == "__main__":
    print(solve(sys.stdin.read()))
