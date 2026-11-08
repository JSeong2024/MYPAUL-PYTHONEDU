"""B-03 — First Gradient Update (Starter Code).

입력: x y w b eta
출력: GRAD_W, GRAD_B, NEW_W, NEW_B, PREDICTION
문제 원문: ../problem.md의 B-03 절
"""
import sys


def solve(source: str) -> str:
    """문제의 입력을 받아 정해진 형식의 출력 문자열을 반환합니다."""
    # STEP 1: 초기 w, b에서 예측 오차 산출
    # STEP 2: 동시에 grad_w, grad_b 계산
    # STEP 3: 한 번 갱신한 w, b로 예측
    raise NotImplementedError("TODO: solve() 구현")


if __name__ == "__main__":
    print(solve(sys.stdin.read()))
