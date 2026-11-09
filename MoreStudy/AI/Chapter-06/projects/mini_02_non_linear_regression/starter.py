"""Mini 02 — 수요 데이터를 이용해 Linear와 MLP의 RMSE를 비교합니다."""
from torch import nn


def build_regression_mlp():
    # TODO: Linear(2,24) -> Tanh -> Linear(24,12) -> Tanh -> Linear(12,1)
    raise NotImplementedError


def evaluate_models():
    # TODO: CSV 로드와 Train/Test Split
    # TODO: MSELoss를 이용해 Linear/MLP 학습
    # TODO: Test RMSE 계산 및 비교 CSV 생성
    raise NotImplementedError

if __name__=='__main__':
    evaluate_models()
