"""B-05 — KMeans Assignment (Starter Code).

입력: Two initial 2-D centers; N points
출력: ASSIGNMENTS, CENTER_0, CENTER_1
문제 원문: ../problem.md의 B-05 절
"""
import sys


def solve(source: str) -> str:
    """문제의 입력을 받아 정해진 형식의 출력 문자열을 반환합니다."""
    # STEP 1: 각 샘플에서 초기 두 중심까지 거리의 제곱 계산
    # STEP 2: 동점이면 Cluster 0 선택
    # STEP 3: 클러스터별 평균으로 한 번 갱신하고 Empty Cluster 유지
    raise NotImplementedError("TODO: solve() 구현")


if __name__ == "__main__":
    print(solve(sys.stdin.read()))
