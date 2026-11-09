"""B-01 — 텐서 구조와 차원별 집계

입력: stdin: N D 및 행렬
완성 후 problem.md의 출력 형식과 예시를 확인하세요.
"""
import sys
import torch

def solve(raw: str) -> str:
    # TODO: 입력의 행 개수와 자료형 검사
    # TODO: torch.tensor, sum(dim=0), mean(dim=1)
    # TODO: 지정된 출력 형식의 문자열 반환
    raise NotImplementedError("B-01 구현")

if __name__ == "__main__":
    print(solve(sys.stdin.read()))
