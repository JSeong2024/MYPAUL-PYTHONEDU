"""Practice 01 — 텐서 구조 변환."""
import torch


def summarize(readings: torch.Tensor) -> torch.Tensor:
    """[N,3] 입력의 열별 평균 [3] 반환. 입력은 변경하지 않습니다."""
    if readings.ndim != 2 or readings.shape[1] != 3:
        raise ValueError('readings must have shape [N, 3]')
    if readings.shape[0] == 0:
        raise ValueError('empty readings')
    # TODO: float32로 변환하고 dim=0 방향의 평균 반환
    raise NotImplementedError


if __name__ == '__main__':
    print(summarize(torch.tensor([[1, 2, 3], [3, 4, 5]])))
