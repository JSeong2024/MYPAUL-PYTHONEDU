"""Professional 01 — Fleet Training Starter."""
FEATURES=['equipment_type','vibration','temperature_c','utilization','days_since_service','prior_alerts']

def validate_source(path):
    # TODO: Schema, 중복 ID, 결측값, 유한한 Feature와 이진 Label 확인
    raise NotImplementedError

def select_threshold(y_true,probabilities,weeks,max_review_fraction=.30):
    # TODO: 각 주차의 검토 한도 만족 여부 검사
    # TODO: Validation F2 최대인 Threshold 선택
    raise NotImplementedError

def run(data_path=None,output_dir=None,max_epochs=24,patience=6,max_review_fraction=.30):
    # TODO: 시설 단위 512/128/128 Split; 미래 정보 제외
    # TODO: Train Scaling, 후보 모델 학습, Early Stopping, 모델 선택
    # TODO: Test 평가, 메타데이터/Weight 저장 및 복원 검증
    raise NotImplementedError

if __name__=='__main__':
    run()
