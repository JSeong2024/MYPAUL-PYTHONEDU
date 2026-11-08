"""Practice 02 — Broadcasting과 유효 샘플 Mask."""
import torch


def calibrate(readings: torch.Tensor, offsets: torch.Tensor):
    """[N,3], [3] -> 교정 텐서 및 값이 0 이상인 Mask."""
    # TODO: 입력 shape 검증, Broadcasting 덧셈, 원본 값을 기준으로 mask 생성
    raise NotImplementedError
