"""B-05 — DataLoader의 배치 구성

입력: stdin: N B drop_last, IDs
완성 후 problem.md의 출력 형식과 예시를 확인하세요.
"""
import sys
import torch

def solve(raw: str) -> str:
    # TODO: 입력의 행 개수와 자료형 검사
    # TODO: TensorDataset, DataLoader
    # TODO: 지정된 출력 형식의 문자열 반환
    raise NotImplementedError("B-05 구현")

if __name__ == "__main__":
    print(solve(sys.stdin.read()))
