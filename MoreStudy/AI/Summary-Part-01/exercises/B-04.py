"""B-04 — Classification Metrics (Starter Code).

입력: N threshold; N lines of (actual, score)
출력: TP, FP, FN, TN, PRECISION, RECALL, F1
문제 원문: ../problem.md의 B-04 절
"""
import sys


def solve(source: str) -> str:
    """문제의 입력을 받아 정해진 형식의 출력 문자열을 반환합니다."""
    # STEP 1: score >= threshold일 때 양성 판정
    # STEP 2: Confusion Matrix 네 값 계산
    # STEP 3: 분모가 0일 때 Precision·Recall·F1을 0으로 처리
    raise NotImplementedError("TODO: solve() 구현")


if __name__ == "__main__":
    print(solve(sys.stdin.read()))
