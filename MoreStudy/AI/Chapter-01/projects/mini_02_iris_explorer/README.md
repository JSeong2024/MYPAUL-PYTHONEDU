[← Chapter 01](../../README.md) · [Mini Projects](../../README.md#section-1-10)

# Mini Project 02. Iris Classification Explorer

## 문제 상황

붓꽃의 꽃받침과 꽃잎 크기를 이용해 품종을 분류합니다. 학습과 평가에 서로 다른 샘플을 사용하는 이유를 실제 예측 결과로 확인하세요.

## 입력 데이터

`sklearn.datasets.load_iris()`는 붓꽃 샘플 150개, 측정 특성(Feature) 4개, 품종 3개를 포함합니다. 별도 다운로드가 필요하지 않으며 길이 단위는 cm입니다. 실제 수집된 공개 데이터셋으로, 합성 데이터가 아닙니다.

| 입력 | 내용 |
|---|---|
| `X` | 꽃받침 길이·너비, 꽃잎 길이·너비 |
| `y` | 품종을 나타내는 타깃(Target): 0, 1, 2 |

분류에서 품종 값은 레이블(Label)이라고도 부릅니다.

## 구현 STEP

1. **Data Inspection:** 샘플 수, Feature 개수, 품종별 건수를 확인합니다.
2. **Data Split:** 학습 80%, 평가 20%로 분리하고 `random_state=42`, `stratify=y`를 적용합니다.
3. **Training:** `StandardScaler`와 `KNeighborsClassifier(n_neighbors=5)`를 Pipeline으로 연결합니다.
4. **Prediction:** 평가 데이터 30개에서 예측 Label과 실제 Label을 비교합니다.
5. **Visualization:** 품종별 예측 결과를 혼동행렬(Confusion Matrix)로 시각화합니다.
6. **Interpretation:** 오분류 사례와 평가 결과의 해석 범위를 설명합니다.

<details>
<summary><strong>코드 힌트 — 모델 학습</strong></summary>

```python
model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
model.fit(x_train, y_train)
```

</details>

## 실행 및 결과

`Chapter-01/`에서 다음 명령을 실행합니다.

```bash
python projects/mini_02_iris_explorer/starter.py
python solutions/mini_02_iris_explorer.py
```

`starter.py`는 미완성 실습 코드입니다. 모범 구현은 기본 분할의 평가 데이터 30개 중 28개를 정확히 분류합니다. 그림은 `outputs/mini_02_iris_confusion.png`에 저장됩니다.

![Mini 02 분석 결과](../../figures/mini_02_iris_confusion.png)

## 테스트 시나리오

- 학습·평가 데이터의 샘플 수 합계가 150이어야 합니다.
- 혼동행렬에 포함된 건수의 합은 평가 데이터 수 30과 같아야 합니다.
- `k=0`은 유효하지 않은 모델 설정으로 처리해야 합니다.
- 오분류가 0건이어도 모든 새로운 샘플에서 완벽한 성능을 보장하지 않습니다.

**완료 기준:** 학습·예측·평가를 구분하고 Accuracy 및 혼동행렬을 해석합니다.

---

[← Chapter 01](../../README.md) · [Contents](../../README.md#contents)
