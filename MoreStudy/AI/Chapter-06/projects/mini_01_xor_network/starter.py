"""Mini 01 — XOR 데이터를 이용해 Linear와 MLP를 비교합니다."""
import torch
from torch import nn


def build_linear():
    # TODO: Feature 2개를 단일 Logit으로 바꾸는 Linear 모델
    raise NotImplementedError


def build_mlp():
    # TODO: Linear(2,8) -> Tanh -> Linear(8,1) 모델
    raise NotImplementedError


def train_and_compare():
    # TODO: data/xor_signals.csv 로드와 Stratified Split
    # TODO: BCEWithLogitsLoss, Adam으로 두 모델을 동일 조건에서 학습
    # TODO: 학습하지 않은 Test Data로 Accuracy 계산하고 CSV 출력
    raise NotImplementedError

if __name__=='__main__':
    train_and_compare()
