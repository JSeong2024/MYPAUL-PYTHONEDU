"""Advanced 02 — 전처리 규격, 가중치 저장/복원, 추론 검증."""
from torch import nn

FEATURES = [f'f{i}' for i in range(1, 7)]

class TriageNet(nn.Module):
    def __init__(self):
        super().__init__()
        # TODO: Linear(6,24), ReLU, Dropout(0.15), Linear(24,3)
        raise NotImplementedError

    def forward(self, x):
        # TODO: 입력 Shape 검사 및 Logit 반환
        raise NotImplementedError


def validate_features(frame):
    # TODO: 입력 열·순서와 NaN/무한대 검증
    raise NotImplementedError


def predict(model, frame, mean, std):
    # TODO: 동일한 Train 기준으로 스케일링, eval()/inference_mode() 사용
    raise NotImplementedError


def run():
    # TODO: Train/Validation/Test 분리, 모델 학습 및 선택
    # TODO: State_dict와 전처리 메타데이터 저장/복원, 예측 일치 검사
    raise NotImplementedError

if __name__=='__main__':
    run()
