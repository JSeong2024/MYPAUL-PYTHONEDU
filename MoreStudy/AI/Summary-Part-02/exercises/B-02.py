"""B-02 — 센서 측정값 보정

입력: stdin: N D, Offset, Scale, 행렬
완성 후 problem.md의 출력 형식과 예시를 확인하세요.
"""
import sys
import torch

def solve(raw: str) -> str:
    # TODO: 입력의 행 개수와 자료형 검사
    # TODO: Broadcasting으로 z=(x+offset)*scale
    # TODO: 지정된 출력 형식의 문자열 반환
    raise NotImplementedError("B-02 구현")

if __name__ == "__main__":
    print(solve(sys.stdin.read()))
