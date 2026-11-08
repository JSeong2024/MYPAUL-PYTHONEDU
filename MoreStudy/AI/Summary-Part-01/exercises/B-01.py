"""B-01 — Feature & Target Inspector (Starter Code).

입력: N D / N rows of D features and binary target
출력: SAMPLES, FEATURES, TARGET_0, TARGET_1 or INVALID
문제 원문: ../problem.md의 B-01 절
"""
import sys


def solve(source: str) -> str:
    """문제의 입력을 받아 정해진 형식의 출력 문자열을 반환합니다."""
    # STEP 1: 첫 줄의 N·D 범위 및 입력 행 수 검증
    # STEP 2: D개 Feature가 모두 유한한 수인지 검사
    # STEP 3: Target 0/1 빈도 계산, 형식 오류 시 INVALID
    raise NotImplementedError("TODO: solve() 구현")


if __name__ == "__main__":
    print(solve(sys.stdin.read()))
