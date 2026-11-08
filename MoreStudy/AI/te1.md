# Problems — Summary Part 01

Chapter 01~04 · **Basic 5 · Advanced 4 · Professional 3 · Challenge 2 · Radiant 1**

각 문제의 입력·출력 조건을 충족하는 Python 프로그램을 작성하시오. 예제는 공개된 검증 사례이며, 예제만 통과하는 코드는 완성된 구현으로 간주하지 않습니다. 관련 개념과 구현 가이드는 필요할 때 확인할 수 있습니다.

[← Summary 목차](./README.md) · [Quiz](./quiz.md) · [AI 목차](../README.md)

## Basic

### B-01. Feature & Target Inspector — 데이터 구조 및 정합성 검사

**관련 개념:** [Chapter 02](../Chapter-02/README.md) · Sample · Feature · Target · Array Shape · Data Validation

#### 문제 설명

머신러닝 파이프라인을 구축할 때 가장 먼저 선행되어야 할 작업은 입력 데이터의 구조와 무결성을 검증하는 것입니다. 학습 데이터의 행(Sample)과 열(Feature/Target)이 올바르게 구성되었는지 사전에 확인하지 않으면, 차원 불일치 오류나 잘못된 레이블로 인해 학습 과정에서 치명적인 문제가 발생할 수 있습니다.

본 문제에서는 첫 줄에 샘플 수와 특성 수가 주어지고, 이어지는 행들에 각 샘플의 특성 값들과 이진 분류용 타겟 레이블이 공백으로 구분되어 입력됩니다. 전체 데이터의 구조를 안전하게 파싱하고 유효성을 검사하여 요약 정보를 출력하는 프로그램을 작성하시오.

#### 요구 사항

1. 첫 줄에서 샘플 수 `N`과 특성 수 `D`를 읽은 뒤, 이어지는 `N`개 행에서 `D`개의 Feature와 1개의 Target을 각각 분리합니다.
2. 독립 변수 `X`의 배열 Shape는 `(N, D)`, 타겟 `y`의 Shape는 `(N,)`으로 올바르게 구성합니다.
3. 타겟 값인 `0`과 `1`의 빈도수를 각각 정확히 집계합니다.
4. 각 행의 데이터 개수가 일치하지 않거나, Target 값이 `0` 또는 `1` 이외의 정수일 경우 `INVALID`를 출력합니다.

#### 입력

첫 줄에 샘플 수 `N`과 특성 수 `D`가 공백으로 구분되어 주어집니다. 이어지는 `N`개 줄에는 실수 형태의 Feature `D`개와 정수 형태의 Target 1개가 공백으로 구분되어 입력됩니다.

- `1 ≤ N ≤ 1,000`, `1 ≤ D ≤ 20`
- Feature 값은 유한한 실수이며, Target 값은 `0` 또는 `1`입니다.

#### 출력

데이터가 유효한 경우, 샘플 수, 특성 수, 그리고 각 타겟별 빈도수를 아래의 정해진 형식에 맞춰 출력합니다. 입력 형식이 잘못되었거나 유효성 검증을 통과하지 못한 경우 `INVALID`를 한 줄에 출력합니다.

**예제 입력**

```text
3 2
1.5 2.0 0
2.1 3.0 1
1.2 2.8 0
```

**예제 출력**

```text
SAMPLES 3
FEATURES 2
TARGET_0 2
TARGET_1 1
```

#### 검증 항목 (Edge Cases)

- **경계값 조건:** `N = 1` 또는 `D = 1`인 최소 크기 입력에서도 배열의 차원(Shape)이 깨지지 않고 올바르게 유지되는지 확인
- **결측 및 초과 데이터:** Feature의 개수가 부족하거나 초과하는 경우, 또는 유효하지 않은 문자열이나 공백 예외 처리
- **타겟 유효성 및 편향:** Target 값이 `0` 또는 `1` 범위를 벗어나는 경우, 혹은 데이터셋 전체의 Target이 모두 `0`이거나 모두 `1`로 편향된 경우에도 집계가 정상적으로 수행되는지 검증

<details>
<summary><strong>구현 가이드</strong></summary>

1. **데이터 파싱 및 길이 검증:** 입력받은 각 행을 공백으로 분리하여, 리스트의 전체 길이가 정확히 `D + 1`(`Feature` `D`개 + `Target` 1개)인지 먼저 검증합니다.
2. **배열 분리 및 변환:** 검증된 데이터에서 마지막 원소를 `Target`(`y`)으로, 앞의 `D`개 원소를 `Feature`(`X`)로 분리한 뒤 각각 적절한 타입의 NumPy 배열(`np.float64`, `np.int64`)로 변환합니다.
3. **구조 및 통계 점검:** 생성된 배열의 `X.shape`, `y.shape`가 각각 `(N, D)`, `(N,)` 형태를 만족하는지 확인하고, 조건에 맞지 않거나 예외가 발생할 경우 즉시 `INVALID`를 출력하도록 처리합니다.

</details>

---

### B-02. Prediction Error Calculator — 회귀 예측 모델과 기준 모델(Baseline)의 오차 비교

**관련 개념:** [Chapter 02](../Chapter-02/README.md) · Linear Regression · MAE · MSE · Baseline Model · Evaluation

#### 문제 설명

회귀(Regression) 모델의 성능을 평가할 때는 복잡한 알고리즘이 예측한 결과가 단순한 기준 모델(Baseline)에 비해 얼마나 더 우수한지 비교하는 것이 중요합니다. 

본 문제에서는 파라미터 `w`와 `b`가 주어지는 단순 선형 회귀 모델($\hat{y} = wx + b$)과, 훈련 타겟의 평균값을 모든 샘플의 예측값으로 사용하는 기준 모델(Baseline)을 각각 설정합니다. 주어진 테스트 데이터셋에 대해 두 모델의 **평균 절대 오차(MAE, Mean Absolute Error)** 를 각각 계산하고, 더 우수한(즉, MAE가 더 작은) 예측 방식을 판별하여 출력하는 프로그램을 작성하시오.

#### 요구 사항

1. **Baseline 설정:** 입력된 Training Target의 평균값을 계산하여 기준 모델(Baseline)의 예측 상수로 설정합니다. (※ 테스트 타겟이 아닌 훈련 타겟의 평균을 사용함에 유의)
2. **회귀 모델 평가:** 주어진 파라미터 `w`, `b`를 바탕으로 Test Sample에 대한 예측값 $\hat{y} = wx + b$를 계산하고, 모델의 **MAE(Mean Absolute Error)**와 **MSE(Mean Squared Error)**를 각각 산출합니다.
3. **Baseline 평가:** 동일한 Test Sample에 대해 훈련 타겟 평균값으로 예측을 수행하고, 이에 대한 Baseline의 **MAE**를 계산합니다.
4. **성능 비교 및 판정:** 두 모델의 MAE를 비교하여 회귀 모델의 오차가 더 작으면 `MODEL`, Baseline의 오차가 더 작으면 `BASELINE`, 두 오차가 정확히 같으면 `TIE`를 출력합니다.

#### 입력

- 첫 번째 줄: 회귀 모델의 파라미터 `w`와 `b`가 공백으로 주어집니다.
- 두 번째 줄: 훈련 타겟의 개수 `K`가 주어집니다.
- 세 번째 줄: `K`개의 훈련 타겟 값들이 공백으로 주어집니다.
- 네 번째 줄: 테스트 샘플의 수 `N`이 주어집니다.
- 다섯 번째 줄부터 `N`개 줄: 각 테스트 샘플의 특성값 `x`와 실제 타겟값 `y`가 공백으로 주어집니다.

- `1 ≤ K, N ≤ 1,000`
- 모든 입력값은 유한한 실수입니다.

#### 출력

계산된 `MODEL_MAE`, `MODEL_MSE`, `BASELINE_MAE` 및 최종 비교 결과(`BEST`)를 소수점 넷째 자리까지 반올림하여 아래 형식으로 출력합니다.

**예제 입력**

```text
2 1
2
2 4
3
1 3
2 6
3 7
```

**예제 출력**

```text
MODEL_MAE 0.3333
MODEL_MSE 0.3333
BASELINE_MAE 2.3333
BEST MODEL
```

#### 검증 항목 (Edge Cases)

- **완벽한 예측 (Zero Residual):** 모델의 예측값이 실제 값과 완전히 일치하여 Residual이 모두 `0`인 경우의 MAE 및 MSE 계산 처리
- **단일 샘플 예외 (K=1):** 훈련 타겟의 개수가 `K = 1`일 때 단일 값의 평균 계산이 예외 없이 정상 동작하는지 확인
- **오차 부호 처리:** 음수 오차가 발생했을 때 MAE는 절댓값을 올바르게 반영하고, MSE는 제곱 연산을 통해 양수로 변환되는지 확인
- **데이터 독립성 (Data Leakage 방지):** Baseline 예측값 산출 시 오직 훈련 타겟의 평균만 사용되며, 테스트 타겟 데이터가 섞이지 않았는지 엄격하게 확인

<details>
<summary><strong>구현 가이드</strong></summary>

1. **Baseline 기준 상수 산출:** 입력된 훈련 타겟 전체의 평균값을 구하여 기준 모델의 고정 예측값으로 설정합니다. (예: 훈련 타겟이 `[2, 4]`인 경우 평균은 `3.0`)
2. **회귀 모델 오차 계산:** 테스트 샘플의 특성 `x`에 대해 $\hat{y} = wx + b$를 계산한 뒤, 실제 테스트 타겟 `y`와 비교하여 MAE와 MSE를 산출합니다. 
   - (예: 모델 예측값이 `[3, 5, 7]`이고 실제 값이 `[3, 6, 7]`일 때, 절댓값 오차의 평균인 MAE와 제곱 오차의 평균인 MSE를 각각 계산)
3. **지표 분모 설정:** MAE와 MSE의 평균을 계산할 때의 분모는 훈련 샘플 수 `K`가 아닌 **테스트 샘플 수 `N`**을 사용해야 함에 유의합니다.
4. **결과 비교 및 출력:** 회귀 모델의 MAE와 Baseline의 MAE를 소수점 넷째 자리까지 정확하게 반올림하여 비교한 뒤 규격에 맞춰 출력합니다.

</details>

---

### B-03. First Gradient Update — 첫 번째 파라미터 갱신 및 예측

**관련 개념:** [Chapter 02](../Chapter-02/README.md) · Loss Function · Partial Derivative · Gradient Descent · Optimization

#### 문제 설명

선형 모델 $\hat{y} = wx + b$의 예측 오차를 줄이기 위해 경사하강법(Gradient Descent)을 적용하여 파라미터를 단 한 번 갱신(Update)하고, 갱신된 파라미터로 새로운 예측값을 산출하고자 합니다. 단일 샘플 $(x, y)$에 대한 손실 함수(Loss Function)는 다음과 같이 정의됩니다.

$$L = \frac{1}{2}(wx + b - y)^2$$

주어진 단일 샘플, 초기 파라미터($w$, $b$), 그리고 학습률(Learning Rate, $\eta$)을 활용하여 편미분을 통해 기울기(Gradient)를 계산하고, 갱신된 파라미터와 새로운 예측값을 출력하는 프로그램을 작성하시오.

#### 요구 사항

1. **오차 계산:** 예측 오차 $e = wx + b - y$ (또는 $\hat{y} - y$)를 계산합니다.
2. **기울기(Gradient) 산출:** 손실 함수의 편미분 공식을 이용해 각 파라미터의 기울기를 구합니다.
   - $\frac{\partial L}{\partial w} = e \cdot x$
   - $\frac{\partial L}{\partial b} = e$
3. **파라미터 갱신:** 학습률 $\eta$를 반영하여 경사하강법 공식을 통해 새로운 파라미터를 계산합니다.
   - $w_{\text{new}} = w - \eta \cdot \frac{\partial L}{\partial w}$
   - $b_{\text{new}} = b - \eta \cdot \frac{\partial L}{\partial b}$
4. **신규 예측값 산출:** 갱신된 파라미터($w_{\text{new}}$, $b_{\text{new}}$)를 바탕으로 동일한 입력 $x$에 대한 새로운 예측값($\hat{y}_{\text{new}} = w_{\text{new}}x + b_{\text{new}}$)을 구합니다.

#### 입력

한 줄에 특성 `x`, 실제 타겟 `y`, 초기 파력미터 `w`, `b`, 그리고 학습률 `eta`가 공백으로 구분되어 주어집니다.

- 모든 수는 유한한 실수입니다.
- 학습률 조건: `0 < eta ≤ 1`

#### 출력

계산된 `GRAD_W`, `GRAD_B`, `NEW_W`, `NEW_B`, 그리고 `PREDICTION` 값을 소수점 넷째 자리까지 반올림하여 출력합니다.

**예제 입력**

```text
2 5 1 0 0.1
```

**예제 출력**

```text
GRAD_W -6.0000
GRAD_B -3.0000
NEW_W 1.6000
NEW_B 0.3000
PREDICTION 3.5000
```

#### 검증 항목 (Edge Cases)

- **무변동 조건:** 예측 오차가 `0`인 경우 기울기(Gradient)가 `0`이 되어 파라미터가 변경되지 않고 기존 값을 그대로 유지하는지 확인
- **음수 Gradient 방향성:** 기울기가 음수일 때, 경사하강법 공식에 의해 파라미터가 올바른 방향(증가하는 방향)으로 갱신되는지 확인
- **계수 상쇄 효과:** 손실 함수 정의에 포함된 $\frac{1}{2}$ 계수가 편미분 과정에서 지수 `2`와 곱해져 자연스럽게 소거(`1`)되는지 수학적 정합성 확인

<details>
<summary><strong>구현 가이드</strong></summary>

1. **동시 계산 원칙:** 미분을 수행하기 전의 초기 파라미터(`w`, `b`)를 기준으로 $w$와 $b$의 기울기를 각각 독립적으로 계산하세요.
2. **동기화 유지:** 기울기를 구하는 과정에서 $w$를 먼저 변경해버리면 $b$의 기울기 계산 시점에 영향을 주어 잘못된 결과가 산출될 수 있으므로, 두 기울기를 모두 구한 뒤 한꺼번에 갱신하세요.
3. **단계별 적용:** 갱신이 완료된 새로운 $w_{\text{new}}$와 $b_{\text{new}}$는 최종 단계에서 새로운 예측값(`PREDICTION`)을 산출할 때만 사용해야 합니다.

</details>

---

### B-04. Classification Metrics — 이진 분류 결과 및 성능 지표 분석

**관련 개념:** [Chapter 03](../Chapter-03/README.md) · Decision Threshold · [Chapter 04](../Chapter-04/README.md) · Confusion Matrix · Precision · Recall · F1-Score

#### 문제 설명

이진 분류 모델이 산출한 예측 확률(또는 점수)에 결정 임계값(Decision Threshold)을 적용하여 최종 예측 레이블을 결정하고자 합니다. 주어진 임계값을 기준으로 예측 레이블을 생성한 뒤, 실제 레이블과 비교하여 혼동 행렬(Confusion Matrix)의 구성 요소를 도출하고 주요 분류 평가 지표를 계산하는 프로그램을 작성하시오.

#### 요구 사항

1. **임계값 적용:** 각 샘플의 예측 점수(`score`)가 임계값(`threshold`) 이상(`score >= threshold`)이면 양성(`1`), 그렇지 않으면 음성(`0`)으로 예측 레이블을 결정합니다.
2. **혼동 행렬 산출:** 실제 레이블(`actual`)과 예측 레이블을 비교하여 `TP`(True Positive), `FP`(False Positive), `FN`(False Negative), `TN`(True Negative)의 개수를 각각 정확히 계산합니다.
3. **성능 지표 계산:** 정밀도(Precision), 재현율(Recall), 그리고 두 지표의 조화 평균인 F1-Score를 계산합니다.
4. **분모 0 예외 처리:** Precision 또는 Recall 계산 시 분모가 `0`이 되는 상황(예: 양성 예측 개수가 0이거나 실제 양성 개수가 0인 경우)이 발생하면, 해당 지표의 값은 경고나 에러 없이 **`0.0000`**으로 대체하여 출력합니다.

#### 입력

- 첫 번째 줄: 전체 샘플 수 `N`과 결정 임계값 `threshold`가 공백으로 주어집니다.
- 두 번째 줄부터 `N`개 줄: 각 샘플의 실제 레이블 `actual`과 예측 점수 `score`가 공백으로 구분되어 주어집니다.

- `1 ≤ N ≤ 10,000`, `0 ≤ threshold ≤ 1`
- `actual` 값은 `0` 또는 `1`, `score` 값은 `0 이상 1 이하`의 실수입니다.

#### 출력

혼동 행렬 지표인 `TP`, `FP`, `FN`, `TN`을 정수 형태로 출력하고, 이어지는 세 가지 성능 지표(`Precision`, `Recall`, `F1-Score`)를 소수점 넷째 자리까지 반올림하여 출력합니다.

**예제 입력**

```text
5 0.5
0 0.10
1 0.80
1 0.40
0 0.60
1 0.90
```

**예제 출력**

```text
TP 2
FP 1
FN 1
TN 1
PRECISION 0.6667
RECALL 0.6667
F1 0.6667
```

#### 검증 항목 (Edge Cases)

- **경계값 일치 (`Score == Threshold`):** 예측 점수가 임계값과 정확히 일치하는 샘플들이 조건식(`>=`)에 따라 올바르게 양성(`1`)으로 분류되는지 확인
- **제로 디비전 및 극한 상황:** 양성 예측이 전혀 없는 경우(`TP + FP = 0`), 실제 양성이 전혀 없는 경우(`TP + FN = 0`), 혹은 데이터셋 전체에 단 하나의 클래스만 등장하는 입력에서도 프로그램이 중단되지 않고 안정적으로 동작하는지 검증

<details>
<summary><strong>구현 가이드</strong></summary>

1. **혼동 행렬 선집계:** 임계값 비교를 통해 예측 레이블을 먼저 확정한 뒤, `TP`, `FP`, `FN`, `TN`의 네 가지 분류 결과를 완벽하게 먼저 집계합니다.
2. **안전한 지표 함수 분리:** 각 지표의 분모가 `0`인지 사전에 검사하는 전용 함수(또는 안전 나눗셈 로직)를 별도로 구현하여 런타임 오류를 방지하세요.
3. **F1-Score 통합 계산식 활용:** 수식 변형 형태인 $F_1 = \frac{2 \cdot TP}{2 \cdot TP + FP + FN}$ 공식을 활용하면, Precision과 Recall이 모두 0이 되는 예외 상황에서도 분모 조건 처리를 일관되고 간결하게 수행할 수 있습니다.
4. **출력 포맷팅:** 정수는 정수형으로, 소수점 지표들은 `round(val, 4)` 또는 `{:.4f}` 포맷을 적용하여 소수점 넷째 자리까지 정확하게 출력합니다.

</details>

---

### B-05. KMeans Assignment — 클러스터 중심 할당 및 갱신

**관련 개념:** [Chapter 03](../Chapter-03/README.md) · KMeans · Euclidean Distance · Centroid Update · Cluster Assignment

#### 문제 설명

KMeans 클러스터링 알고리즘의 핵심 단계인 **'데이터 할당(Assignment)'** 과 **'중심점 갱신(Centroid Update)'** 과정을 직접 구현하고자 합니다. 2차원 공간 상의 초기 중심점 두 개와 샘플들이 주어졌을 때, 각 샘플을 더 가까운 중심에 할당하고, 새롭게 구성된 클러스터의 평균 좌표를 바탕으로 중심점을 단 한 번 갱신하는 프로그램을 작성하시오.

#### 요구 사항

1. **유클리드 거리 계산:** 각 샘플과 두 초기 중심($C_0, C_1$) 사이의 유클리드 거리(Euclidean Distance)를 각각 계산합니다.
2. **동점 처리 규칙:** 두 중심까지의 거리가 정확히 같다면 **인덱스가 더 작은 중심(클러스터 0)**에 우선적으로 할당합니다.
3. **중심점 갱신:** 각 클러스터(Cluster 0, Cluster 1)에 할당된 샘플들의 좌표별 평균(Mean)을 산출하여 새로운 중심 좌표로 갱신합니다.
4. **빈 클러스터 예외 처리:** 특정 클러스터에 단 하나의 샘플도 할당되지 않아 비어 있게 되는 경우, 해당 클러스터의 중심점은 기존 좌표를 그대로 유지합니다.

#### 입력

- 첫 번째 줄: 중심 0의 좌표 `c0_x c0_y`가 공백으로 주어집니다.
- 두 번째 줄: 중심 1의 좌표 `c1_x c1_y`가 공백으로 주어집니다.
- 세 번째 줄: 샘플의 수 `N`이 주어집니다.
- 네 번째 줄부터 `N`개 줄: 각 샘플의 좌표 `x y`가 공백으로 구분되어 주어집니다.

- `1 ≤ N ≤ 1,000`
- 모든 좌표 값은 유한한 실수입니다.

#### 출력

- 첫 번째 줄: 원본 샘플 순서에 따른 클러스터 할당 번호(`0` 또는 `1`)를 공백으로 구분하여 출력합니다.
- 두 번째 줄: 갱신된 중심 0의 좌표 `new_c0_x new_c0_y`를 소수점 넷째 자리까지 반올림하여 출력합니다.
- 세 번째 줄: 갱신된 중심 1의 좌표 `new_c1_x new_c1_y`를 소수점 넷째 자리까지 반올림하여 출력합니다.

**예제 입력**

```text
0 0
6 0
3
1 0
5 0
3 0
```

**예제 출력**

```text
ASSIGNMENTS 0 1 0
CENTER_0 2.0000 0.0000
CENTER_1 5.0000 0.0000
```

#### 검증 항목 (Edge Cases)

- **동점 거리 처리:** 두 중심점까지의 거리가 정확히 동일한 샘플이 입력되었을 때, 우선순위 규칙에 따라 안정적으로 처리되는지 확인
- **빈 클러스터(Empty Cluster) 방어:** 데이터 분포에 의해 어느 한쪽 클러스터에 샘플이 단 하나도 할당되지 않는 상황 처리
- **단일 샘플 입력:** `N = 1`인 최소 조건에서도 할당 및 갱신 로직이 정상 작동하는지 확인
- **단발성 갱신 보장:** 중심 갱신을 반복 수행하지 않고, 최초 할당 결과를 바탕으로 **정확히 한 번만** 수행하는지 엄격히 확인

<details>
<summary><strong>구현 가이드</strong></summary>

1. **제곱 거리 활용:** 유클리드 거리를 비교할 때 제곱근 연산을 생략하고 거리의 제곱(`(x - cx)**2 + (y - cy)**2`) 값을 비교하여 연산 효율성과 정밀도를 높이세요.
2. **동기화 및 순서 분리:** 모든 샘플에 대한 클러스터 할당을 완전히 끝마친 뒤에 중심점 갱신 연산을 수행하세요.
3. **갱신 시점 주의:** 갱신된 새로운 중심 좌표를 이미 할당이 진행 중인 다른 샘플 판정에 즉시 반영하지 않도록 독립적인 단계를 유지하세요.

</details>

---

## Advanced

### A-01. Visitor Congestion Classification — 혼잡도 판단 기준

**관련 개념:** [Chapter 03](../Chapter-03/README.md) · Logistic Regression · Threshold · [Chapter 04](../Chapter-04/README.md) · Precision · Recall · F1

#### 문제 설명

지역 문화시설은 방문객 수와 근무 인원 등을 이용해 특정 시간대의 혼잡 여부를 예측합니다. 운영팀은 혼잡 상황을 놓치지 않는 것이 중요하지만, 잘못된 혼잡 경보가 지나치게 많아지는 것도 원하지 않습니다.

기존 모델은 클래스 1(혼잡)에 대한 점수를 제공합니다. Validation Data에서 Threshold를 비교하고, 확정한 Threshold로 독립적인 Test Data를 평가하는 프로그램을 작성하세요.

#### 구현 요구사항

1. `record_id`, `actual`, `score`가 기록된 Validation·Test CSV를 읽습니다. `actual`은 0 또는 1이며 `score`는 0 이상 1 이하입니다.
2. Validation Data에서 Threshold 후보 `[0.30, 0.50, 0.70]`의 F1을 계산합니다.
3. F1이 가장 높은 Threshold를 선택합니다. 동점일 경우 **더 큰 Threshold** 를 선택합니다.
4. 선택한 Threshold로 Test Data를 한 번만 평가하고 TP·FP·FN·TN, Precision·Recall·F1을 기록합니다.
5. `threshold_report.csv`에는 후보별 Validation F1과 선택 여부를, `test_report.txt`에는 최종 Threshold 및 Test 지표를 기록합니다.

#### 입력

- `validation_scores.csv`: `record_id,actual,score`
- `test_scores.csv`: 동일한 열 구조
- 두 파일 모두 UTF-8, 헤더가 있으며 같은 `record_id`가 여러 번 나타나서는 안 됩니다.

유효하지 않은 값, 누락된 열, 중복 ID가 발견되면 해당 파일의 이름과 오류 원인을 보고하고 평가를 중단합니다.

#### 출력

파일 두 개를 생성합니다. 출력 파일에서는 Threshold 오름차순, 숫자는 소수 넷째 자리까지 표시합니다.

**예제 입력** (`validation_scores.csv`)

```csv
record_id,actual,score
R01,0,0.20
R02,1,0.65
R03,1,0.48
R04,0,0.70
```

**예제 출력** (`threshold_report.csv`)

```csv
threshold,validation_f1,selected
0.30,0.8000,1
0.50,0.5000,0
0.70,0.0000,0
```

이 예제에서 선택된 Threshold는 `0.30`입니다. Test 결과는 별도의 `test_scores.csv` 값에 따라 달라지므로 특정 F1을 고정하지 않습니다.

#### 검증 항목

- Threshold와 Score가 같은 경계값 처리
- F1 동점 시 더 큰 Threshold 선택
- Test 점수로 Threshold를 다시 선택하지 않았는지 확인
- Actual Label이 모두 한 클래스인 상황과 잘못된 CSV 값 처리

<details>
<summary><strong>구현 가이드</strong></summary>

1. Threshold별 계산을 하나의 함수로 구성하세요.
2. Validation 단계에서 `f1_score`를 사용하거나 TP·FP·FN으로 직접 계산할 수 있습니다.
3. Threshold를 확정한 이후에는 Test 점수를 이용해 설정을 변경하지 마세요.

</details>

---

### A-02. Water Consumption Prediction — 수도 사용량 예측

**관련 개념:** [Chapter 02](../Chapter-02/README.md) · Linear Regression · Scaling · [Chapter 04](../Chapter-04/README.md) · Baseline · MAE · Residual · Temporal Split

#### 문제 설명

건물 관리팀은 다음 날의 수도 사용량을 예측해 설비 운영 계획에 활용합니다. 기온과 건물 이용 인원, 주말 여부는 사용량과 관련이 있지만 시간에 따른 변화가 있기 때문에 임의의 행 분할만으로 평가해서는 안 됩니다.

과거 데이터로 Regression 모델을 학습하고, Baseline과 비교한 결과를 보고하세요.

#### 구현 요구사항

1. 날짜 기준 오름차순으로 정렬하고 과거 60%, 이후 20%, 마지막 20%를 Train·Validation·Test로 나눕니다. 행 수가 나누어떨어지지 않으면 Train과 Validation은 각각 `floor(0.6N)`, `floor(0.2N)`개이고, 나머지를 Test에 배정합니다.
2. `temperature_c`, `occupants`, `is_weekend`를 Feature로 사용하고 `consumption_m3`를 Target으로 지정합니다. `date` 자체는 Feature로 넣지 않습니다.
3. Training Target 평균을 예측하는 Baseline과 `StandardScaler` + `Ridge` 모델을 비교합니다.
4. Ridge의 `alpha` 후보 `[0.1, 1.0, 10.0]`를 Validation MAE로 비교합니다. 동점일 경우 작은 `alpha`를 선택합니다.
5. 확정된 설정으로 Test의 MAE·RMSE를 구하고, `date`, `actual`, `predicted`, `residual`을 포함한 결과 CSV를 생성합니다. Residual은 `actual - predicted`로 정의합니다.

#### 입력

`daily_water.csv`: `date,temperature_c,occupants,is_weekend,consumption_m3`

- 날짜는 `YYYY-MM-DD` 형식이며 중복되지 않습니다.
- `is_weekend`는 0 또는 1, `occupants`는 0 이상의 정수입니다.
- 최소 30개 행을 사용하며, 모든 수치 값은 유한해야 합니다.

**예제 입력 일부**

```csv
date,temperature_c,occupants,is_weekend,consumption_m3
2026-04-01,17.0,42,0,48.5
2026-04-02,19.0,44,0,52.1
2026-04-03,21.0,36,0,49.3
```

#### 출력

- `model_comparison.csv`: `model,validation_mae` (Baseline과 Ridge 후보별 결과)
- `test_predictions.csv`: `date,actual,predicted,residual` (Test 날짜 오름차순)
- `report.txt`: 선택한 `alpha`, Test MAE, Test RMSE, Test Baseline MAE, 모델·Baseline 비교 결과

제시된 세 행만으로 모델을 학습하지 않습니다. 실제 평가는 최소 30행의 전체 입력에 대해 수행합니다.

#### 검증 항목

- 날짜 순서를 유지한 분할 및 세 구간의 중복 여부
- Scaling과 모델 학습이 Validation·Test Target을 참조하지 않는지 확인
- Validation에서 선택한 `alpha`를 Test 점수로 다시 바꾸지 않는지 확인
- Residual의 부호, 출력 순서, MAE·RMSE 계산 확인

<details>
<summary><strong>구현 가이드</strong></summary>

1. CSV를 날짜로 정렬한 뒤 위치 기준으로 구간을 나누세요.
2. `Pipeline([('scaler', StandardScaler()), ('model', Ridge(...))])`을 사용할 수 있습니다.
3. Test 결과를 확인하기 전에 모델 선택을 끝내고 Baseline 기준도 Training Target으로 고정하세요.

</details>

---

### A-03. Unlabeled Usage Pattern Analysis — 이용 패턴 군집화

**관련 개념:** [Chapter 03](../Chapter-03/README.md) · KMeans · DBSCAN · Feature Scaling · Cluster Profile · Noise

#### 문제 설명

공유 공간의 방문 기록에는 이용자의 유형을 나타내는 정답 Label이 없습니다. 운영팀은 방문 빈도, 체류 시간, 저녁 이용 비율을 참고해 공간 운영 패턴을 찾고자 합니다.

KMeans와 DBSCAN으로 데이터를 분석하고, 두 방법의 결과를 그대로 우열 비교하지 않고 특징을 설명하는 보고서를 작성하세요.

#### 구현 요구사항

1. `weekly_visits`, `avg_minutes`, `evening_ratio`의 결측값과 범위를 검사합니다. 유효하지 않은 행은 `invalid_rows.csv`에 별도로 기록하고 분석에서는 제외합니다.
2. 유효한 Feature에 `StandardScaler`를 적용합니다.
3. `KMeans(n_clusters=3, random_state=42, n_init=10)`와 `DBSCAN(eps=0.6, min_samples=5)`를 각각 실행합니다.
4. 두 모델에 대해 Cluster 크기와 원본 단위의 Feature별 평균을 계산합니다. DBSCAN의 Label `-1`은 Noise로 별도 집계합니다.
5. `cluster_assignments.csv`, `cluster_profiles.csv`, `report.md`를 작성합니다. KMeans와 DBSCAN의 Cluster ID가 같은 의미가 아니라는 점을 보고서에 명시합니다.

#### 입력

`space_usage.csv`: `record_id,weekly_visits,avg_minutes,evening_ratio`

- `weekly_visits`: 0 이상의 정수
- `avg_minutes`: 0 이상의 유한 실수
- `evening_ratio`: 0 이상 1 이하
- 유효한 Sample은 최소 30개여야 하며, 30개 미만이면 분석을 중단합니다.

**예제 입력 일부**

```csv
record_id,weekly_visits,avg_minutes,evening_ratio
S01,2,135,0.15
S02,7,32,0.82
S03,3,102,0.38
```

#### 출력

- `cluster_assignments.csv`: `record_id,kmeans_cluster,dbscan_cluster` (원본 유효 행 순서)
- `cluster_profiles.csv`: `method,cluster_id,sample_count,mean_weekly_visits,mean_avg_minutes,mean_evening_ratio`
- `invalid_rows.csv`: `row_number,error_code` (없으면 헤더만 출력)
- `report.md`: Cluster별 이용 특징, DBSCAN Noise 수, 알고리즘별 차이 및 해석상 한계

Cluster 번호와 평균값은 입력 데이터의 전체 분포에 따라 달라지므로 예제 세 행만으로 고정하지 않습니다.

#### 검증 항목

- 비정상 행이 Scaling과 Clustering에 포함되지 않는지 확인
- DBSCAN Noise를 유효 Sample 집계에서 누락하지 않는지 확인
- 유효 Sample 수와 KMeans Cluster별 Count의 합이 일치하는지 확인
- Cluster ID를 실제 이용자 유형의 정답 Label로 오해하지 않는지 확인

<details>
<summary><strong>구현 가이드</strong></summary>

1. Feature의 유효성 검사를 먼저 수행하세요.
2. `fit_predict()` 결과는 원본 유효 행과 같은 순서로 기록하세요.
3. Cluster Profile은 Scaling된 값이 아닌 원본 단위에서 계산해야 운영팀이 해석하기 쉽습니다.

</details>

---

### A-04. Misleading Validation Score — 잘못된 평가 흐름 수정

**관련 개념:** [Chapter 02](../Chapter-02/README.md) · Data Leakage · [Chapter 04](../Chapter-04/README.md) · Pipeline · Cross-Validation · Hyperparameter Tuning

#### 문제 설명

한 개발자가 모델 성능을 높이기 위해 KNN의 이웃 수를 조정했습니다. 보고된 Cross-Validation Score는 높았지만, 코드에서는 전체 데이터로 Scaling을 수행한 뒤 Training과 Test를 나누고 있습니다. Test 결과도 Hyperparameter를 선택하는 과정에서 여러 번 확인했습니다.

다음 평가 코드를 검토하고, 동일한 실수를 반복하지 않도록 처리 순서를 수정하세요.

**문제가 있는 코드**

```python
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

X_scaled = StandardScaler().fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)
search = GridSearchCV(
    KNeighborsClassifier(), {"n_neighbors": [3, 5, 7]}, cv=5
)
search.fit(X_train, y_train)
# 이후 Test 점수를 반복 확인해 n_neighbors를 변경함
```

#### 구현 요구사항

1. 코드에서 발생하는 평가 절차상의 문제를 두 가지 이상 찾아 설명합니다.
2. 원본 `X`, `y`를 Train·Test로 먼저 분할합니다. 이 문제의 데이터는 독립 Sample로 구성된 이진 분류이며 클래스별 Sample이 충분하다고 가정합니다.
3. `StandardScaler`와 `KNeighborsClassifier`를 `Pipeline`으로 구성하고, `GridSearchCV`로 `n_neighbors` 후보를 비교합니다.
4. 선택된 설정을 고정한 뒤 독립적인 Test Data에서 Accuracy와 Balanced Accuracy를 한 번 평가합니다.
5. `audit_report.md`에 기존 코드의 문제, 수정 코드의 처리 순서, 평가에 사용한 데이터의 역할을 명시합니다.

#### 입력

- 변수 `X`: Shape `(N, D)`인 숫자형 Feature 배열
- 변수 `y`: Shape `(N,)`인 이진 Target 배열
- `N ≥ 100`, `D ≥ 2`, 클래스별 Sample 수는 5-Fold CV를 수행할 만큼 충분합니다.

검증용 데이터가 필요하면 `sklearn.datasets.make_classification(n_samples=400, n_features=5, n_informative=3, n_redundant=0, random_state=42)`를 사용할 수 있습니다.

#### 출력

- `best_params.json`: 선택된 `n_neighbors`와 평균 Cross-Validation Accuracy
- `test_metrics.json`: 최종 Test Accuracy·Balanced Accuracy
- `audit_report.md`: 발견한 문제와 수정 이유

모델 성능의 고정된 목표 숫자는 없습니다. **평가 절차를 올바르게 분리했는지** 가 이 문제의 핵심입니다.

#### 검증 항목

- `StandardScaler.fit()`이 Test Data 및 각 CV Fold의 Validation Data를 참조하지 않는지 확인
- Test 결과를 보고 후보를 다시 변경하지 않는지 확인
- Pipeline에서 `model__n_neighbors`가 올바르게 설정되는지 확인
- 동일한 `random_state`에서 일관된 분할을 사용하는지 확인

<details>
<summary><strong>구현 가이드</strong></summary>

1. `train_test_split()`을 모든 데이터 변환보다 먼저 호출하세요.
2. `Pipeline`의 각 단계 이름을 정하고 `GridSearchCV`에는 `model__n_neighbors`를 전달하세요.
3. `search.best_estimator_`는 최적 설정으로 Training Data에 다시 학습된 모델입니다. 최종 Test Data를 사용해 별도로 설정을 조정하지 마세요.

</details>

---

## Professional

### P-01. Warranty Repair Triage — 보증수리 접수 우선순위

**관련 개념:** [Chapter 01](../Chapter-01/README.md) · Human Review · [Chapter 03](../Chapter-03/README.md) · Logistic Regression · [Chapter 04](../Chapter-04/README.md) · Imbalanced Evaluation · F2 · Group-Aware Split · Threshold

#### 문제 설명

가전제품 수리센터에는 매일 여러 건의 보증수리 신청이 접수됩니다. 일부 신청은 실제 고장으로 판정되지만, 단순 사용 안내만으로 해결되는 사례도 있습니다. 센터는 **실제 고장 가능성이 높은 접수를 우선 검토** 하려고 합니다.

기존 접수 기록에는 동일 제품의 반복 신청이 포함되어 있습니다. 또한 실제 고장 판정과 최종 수리비는 현장 점검이 끝난 후에야 확인할 수 있습니다. 이 값들을 접수 시점의 예측 Feature로 사용하면 평가 결과가 왜곡됩니다.

하루에 검토할 수 있는 신청은 최대 3건입니다. 학습·평가 절차와 운영용 우선순위 목록을 함께 설계하세요.

#### 제공 데이터

`historical_claims.csv` (학습 및 평가용):

| 열 | 의미 | 예측 시점 사용 |
|---|---|---|
| `claim_id` | 접수 번호 | 결과 연결용 식별자 |
| `received_date` | 접수일 | 분할·운영 날짜 |
| `unit_id` | 제품 고유 번호 | Group 분할 |
| `age_months` | 제품 사용 개월 수 | 가능 |
| `alarm_count_30d` | 최근 30일 오류 알림 횟수 | 가능 |
| `prior_claim_count` | 해당 접수 이전의 누적 수리 신청 수 | 가능 |
| `confirmed_failure` | 점검 후 실제 고장 여부(0/1) | **Target 전용** |
| `final_repair_cost` | 점검 후 확정된 수리비 | **사용 금지** |

`incoming_claims.csv` (운영용): `claim_id,received_date,unit_id,age_months,alarm_count_30d,prior_claim_count` — Target이 없습니다.

두 파일 모두 UTF-8 CSV이며 헤더가 있습니다. `unit_id`가 같은 Sample은 같은 제품에서 발생한 기록입니다.

#### 구현 요구사항

1. 필수 Feature 누락과 범위 오류를 검사합니다. 유효하지 않은 행은 명확한 오류 이유와 함께 별도로 관리합니다. `age_months`, `alarm_count_30d`, `prior_claim_count`는 0 이상의 정수입니다.
2. 기존 데이터를 **제품 단위로** Train 60%·Validation 20%·Test 20%에 가깝게 나눕니다. 비율은 고유 제품 수 기준이며, 제품 ID가 세 구간에 중복되어서는 안 됩니다. `GroupShuffleSplit(random_state=42)` 등을 사용할 수 있습니다.
3. `DummyClassifier(strategy='most_frequent')`를 Baseline으로, `StandardScaler`와 `LogisticRegression(max_iter=1000)`을 연결한 Pipeline을 후보로 사용합니다.
4. Validation에서 Threshold `[0.35, 0.50, 0.65]`의 F2를 계산해 가장 높은 값을 선택합니다. 동점이라면 **더 높은 Threshold** 를 선택합니다. Train·Validation에서 실제 고장이 한 클래스뿐이어서 모델 학습 또는 F2 평가가 불가능하면 이유를 보고하고 중단합니다.
5. 선택한 Threshold를 적용해 Test의 Precision·Recall·F2·Confusion Matrix를 기록합니다. Test 결과로 Threshold를 다시 변경하지 않습니다.
6. 운영 데이터에는 동일 모델의 점수를 적용합니다. Threshold 이상인 접수만 날짜별로 **점수 내림차순, 동점이면 `claim_id` 오름차순** 으로 정렬하고 하루 최대 3건까지 검토 목록에 등록합니다. 나머지는 `NOT_SELECTED`로 기록합니다.
7. 보고서에 **모델 Threshold 기준의 Test 성능** 과 **하루 3건 제한이 적용된 운영 선택 결과** 를 별도로 제시합니다. 두 기준을 같은 지표로 혼동하지 않습니다.

#### 입력 및 출력

**입력:** `historical_claims.csv`, `incoming_claims.csv`

**출력:**

- `evaluation.json`: 분할별 고유 제품·Sample 수, Baseline 점수, 선택 Threshold, Test Metrics
- `daily_review_queue.csv`: `received_date,rank,claim_id,failure_score` — 선택된 신청만 날짜·순위 오름차순
- `incoming_decisions.csv`: `claim_id,decision` — `SELECTED` 또는 `NOT_SELECTED`, 입력 순서 유지
- `report.md`: Feature 선택, Leakage 점검, 운영 제약, 제한 사항

**예제 운영 점수** — Threshold가 `0.50`으로 결정된 경우

```csv
claim_id,received_date,failure_score
C04,2026-10-12,0.62
C02,2026-10-12,0.91
C03,2026-10-12,0.74
C01,2026-10-12,0.91
C05,2026-10-12,0.44
```

**예제 검토 목록**

```csv
received_date,rank,claim_id,failure_score
2026-10-12,1,C01,0.91
2026-10-12,2,C02,0.91
2026-10-12,3,C03,0.74
```

`C04`는 Threshold는 통과했지만 하루 검토 한도 때문에 선택되지 않았고, `C05`는 Threshold보다 낮습니다.

#### 검증 항목

- 동일 제품의 접수 기록이 서로 다른 평가 구간에 포함되지 않는지 확인
- `confirmed_failure`, `final_repair_cost`가 Feature에 들어가지 않는지 확인
- Threshold 동점, 점수 동점, Threshold 미달, 하루 최대 3건의 검토 한도가 정확하게 적용되는지 검증
- Test 평가 이후 운영 목록을 만들 때 Test Label을 사용하지 않는지 확인
- 3건 제한을 적용하기 전후 결과를 구분하는지 확인

<details>
<summary><strong>구현 가이드</strong></summary>

1. `unit_id` 기준의 분할을 먼저 구현하고 세 구간의 교집합이 비어 있는지 검사하세요.
2. 허용된 숫자형 Feature만 Pipeline에 전달하세요.
3. Validation의 F2로 Threshold를 선택한 뒤 Test 지표를 기록하세요.
4. 운영 데이터에서는 예측 점수와 일일 검토 용량을 별개의 규칙으로 처리하세요.

</details>

---

### P-02. Municipal Waste Demand Prediction — 지역별 수거량 예측

**관련 개념:** [Chapter 02](../Chapter-02/README.md) · Regression · [Chapter 04](../Chapter-04/README.md) · Temporal Split · Baseline · Residual Analysis · Hyperparameter Selection

#### 문제 설명

지방자치단체는 구역별 다음 주 폐기물 수거량을 예측해 차량과 인력을 배치하려고 합니다. 데이터에는 지난주 실제 수거량과 다음 주의 예정 행사 수 등이 포함됩니다.

수거량이 적은 구역과 많은 구역의 오차를 같은 크기로 취급할 것인지도 고민해야 합니다. 평균 오차가 낮아도 특정 구역에서 반복적으로 큰 오차가 발생하면 실제 배차 업무에는 문제가 생길 수 있습니다.

과거 주차의 정보만 사용해 다음 주 수거량을 예측하고, 구역별 오류까지 분석하는 프로젝트를 설계하세요.

#### 제공 데이터

`weekly_waste.csv`: `zone_id,forecast_week,last_week_kg,planned_events,holiday_days,next_week_kg`

- `forecast_week`: 예측 대상 주의 시작일(월요일)
- `last_week_kg`: 예측 대상 주 **직전 주** 의 실제 수거량
- `planned_events`: 예측 대상 주에 계획된 행사 수(예측 시점에 이미 확정된 일정)
- `holiday_days`: 예측 대상 주의 공휴일 수(사전에 확인 가능한 값)
- `next_week_kg`: 예측 대상 주가 끝난 후 확인된 **Target**

각 구역과 주의 조합은 유일하며, `next_week_kg`는 0 이상의 유한한 실수입니다. 데이터는 `forecast_week`가 서로 다른 주 최소 15개를 포함한다고 가정합니다.

#### 구현 요구사항

1. 날짜 형식, 중복 구역·주 조합, 음수 수거량 및 비정상 입력을 검사합니다.
2. 구역별 Sample을 섞지 않고 **고유한 주차를 날짜 순서로** Train 60%, Validation 20%, Test 나머지 20%로 나눕니다. 구간의 비율은 고유 `forecast_week` 수를 기준으로 하며, `floor(0.6W)`·`floor(0.2W)`를 사용합니다.
3. `last_week_kg`, `planned_events`, `holiday_days`를 Feature로 사용합니다. `zone_id`는 구역별 결과 분류에만 사용하며 모델의 입력 Feature에는 넣지 않습니다. `next_week_kg`는 Target입니다.
4. Baseline은 `last_week_kg`를 그대로 예측합니다. 후보 모델은 `StandardScaler` + `Ridge`이며 `alpha` 후보는 `[0.1, 1.0, 10.0]`입니다.
5. Ridge 후보 중 Validation MAE가 가장 낮은 `alpha`를 선택합니다. 동점이라면 작은 `alpha`를 선택합니다. Baseline은 모델 후보 선택에 사용하지 않고 비교 기준으로 유지합니다. 선택을 끝낸 뒤 Test에서 Baseline과 Ridge 모델의 MAE·RMSE를 비교합니다.
6. `zone_id`별 Test MAE와 Residual의 평균을 계산합니다. 실제 값보다 **적게 예측한 사례** 중 `actual - predicted`가 가장 큰 상위 5건도 별도로 표시합니다.
7. 보고서에는 전체 성능과 구역별 성능이 다르게 보일 수 있는 이유, 수거량 과소 예측이 운영에 미치는 영향을 기술합니다.

#### 입력 및 출력

**입력:** `weekly_waste.csv`

**출력:**

- `test_predictions.csv`: `zone_id,forecast_week,actual,predicted,baseline,residual`
- `zone_metrics.csv`: `zone_id,sample_count,mae,mean_residual`
- `underprediction_top5.csv`: `zone_id,forecast_week,actual,predicted,residual`
- `report.md`: 분할 방법, 선택한 모델, Baseline 비교, 구역별 오류 분석

**예제 데이터 일부**

```csv
zone_id,forecast_week,last_week_kg,planned_events,holiday_days,next_week_kg
Z01,2026-06-01,420,2,0,455
Z02,2026-06-01,310,0,0,300
Z01,2026-06-08,455,1,0,448
```

Baseline은 각 행에서 `[420, 310, 455]`를 예측합니다. 이 세 행은 형식 확인용이며, 제시된 일부 데이터만으로 Train·Validation·Test를 구성하지 않습니다.

#### 검증 항목

- 같은 `forecast_week`의 여러 구역 기록이 서로 다른 평가 구간으로 갈라지지 않는지 확인
- Target과 예측 시점에 확정되지 않은 자료를 Feature에 넣지 않는지 확인
- 주차를 섞어 분할하거나 Test에서 `alpha`를 다시 조정하지 않았는지 확인
- `actual - predicted`의 부호에 따라 과소·과대 예측을 올바르게 구분하는지 확인
- 전체 MAE가 개선되어도 일부 구역에서 오차가 커질 수 있는지 분석

<details>
<summary><strong>구현 가이드</strong></summary>

1. 먼저 고유 `forecast_week` 목록을 정렬하고 주차 집합으로 Train·Validation·Test를 만드세요.
2. Baseline의 Test 예측값은 각 행의 `last_week_kg`입니다. Training Target 평균을 사용하는 Baseline과 다르므로 문제에서 정의한 기준을 유지하세요.
3. 각 구역의 Test Sample 수와 MAE를 함께 기록해야 적은 Sample로 나온 값도 해석할 수 있습니다.

</details>

---

### P-03. Workspace Utilization Strategy — 공간 운영 패턴 분석

**관련 개념:** [Chapter 03](../Chapter-03/README.md) · Unsupervised Learning · KMeans · Cluster Profile · [Chapter 04](../Chapter-04/README.md) · Evaluation Reliability

#### 문제 설명

공유 오피스 운영사는 여러 공간의 예약률과 취소율을 분석하고 있습니다. 공간별 이용 형태를 구분해 운영 방식을 개선하려고 하지만, 미리 정해진 유형 Label은 없습니다.

운영팀은 단순히 Cluster 번호를 얻는 것으로는 의사결정을 할 수 없습니다. 어떤 공간에서 이용 패턴이 비슷한지, 다른 초기화에서도 비슷한 결과가 나타나는지, 도출된 그룹에 어떤 운영 변경을 적용할 수 있는지가 필요합니다.

#### 제공 데이터

`workspace_usage.csv`: `room_id,week_start,weekly_bookings,avg_session_min,evening_ratio,cancel_ratio`

각 행은 한 공간의 일주일 기록입니다. 비율 열은 0~1, 예약 수와 평균 이용 시간은 0 이상입니다. `room_id`와 `week_start`의 조합은 유일합니다. 유효 Sample은 최소 50개입니다.

#### 구현 요구사항

1. 범위 오류·결측값·중복 행을 검사하고 제외한 행의 이유를 기록합니다.
2. `weekly_bookings`, `avg_session_min`, `evening_ratio`, `cancel_ratio`를 StandardScaler로 변환합니다.
3. `KMeans(n_clusters=3, n_init=10)`을 `random_state` `[7, 21, 42]`에서 각각 실행합니다.
4. 모든 실행 결과를 **같은 유효 Sample 순서에서** 비교하고, 각 실행 쌍의 Adjusted Rand Index(ARI)를 계산합니다. Cluster ID의 숫자 자체는 비교 기준으로 사용하지 않습니다.
5. 기준 결과는 `random_state=42`로 정합니다. 이 결과의 Cluster별 Sample 수, 원본 단위 Feature 평균, 공간별 배정 건수를 계산합니다.
6. 운영 변경안을 세 개 작성합니다. 각 변경안에는 관찰한 Cluster 특징, 제안 이유, 적용 후 확인할 지표가 포함되어야 합니다. 결과가 불안정하다면 그 한계를 보고합니다.

#### 입력 및 출력

**입력:** `workspace_usage.csv`

**출력:**

- `cluster_assignments.csv`: `room_id,week_start,cluster_id` (기준 결과)
- `cluster_profiles.csv`: `cluster_id,sample_count,mean_weekly_bookings,mean_avg_session_min,mean_evening_ratio,mean_cancel_ratio`
- `stability.csv`: `seed_a,seed_b,ari` (7–21, 7–42, 21–42 순서)
- `report.md`: 세 가지 운영 변경안과 검증 지표

**예제 데이터 일부**

```csv
room_id,week_start,weekly_bookings,avg_session_min,evening_ratio,cancel_ratio
M01,2026-09-07,18,55,0.62,0.05
M02,2026-09-07,6,160,0.14,0.10
M01,2026-09-14,20,48,0.70,0.08
```

출력 Cluster ID와 ARI 값은 전체 데이터에 따라 달라지므로 고정된 정답 숫자를 요구하지 않습니다.

#### 검증 항목

- ARI를 동일한 Sample에 대한 서로 다른 Cluster 할당 결과로 계산했는지 확인
- Cluster 번호가 서로 바뀌어도 ARI 해석이 올바른지 확인
- 정답 Label이 없는 문제에서 Accuracy를 사용하지 않는지 확인
- 운영 제안을 Cluster별 실제 특징과 연결했는지 확인
- 공간별 반복 기록이 있다는 사실을 결과 해석에서 고려했는지 확인

<details>
<summary><strong>구현 가이드</strong></summary>

1. `fit_predict()`의 출력을 동일한 유효 Sample 순서로 저장하세요.
2. `adjusted_rand_score(labels_a, labels_b)`로 초기화에 따른 결과의 일치 정도를 살펴볼 수 있습니다.
3. ARI가 높더라도 Cluster가 운영상 유용하다는 사실까지 자동으로 증명되는 것은 아닙니다. 평균·분포와 실제 업무 목적을 함께 확인하세요.

</details>

---

## Challenge

### C-01. Equipment Failure Model Audit — 설비 고장 예측 시스템 감사

**관련 개념:** [Chapter 02](../Chapter-02/README.md) · Data Leakage · [Chapter 04](../Chapter-04/README.md) · GroupKFold · Generalization · Error Analysis · Pipeline

#### 문제 설명

제조 시설에서 사용하던 설비 고장 예측 모델은 내부 평가에서 높은 점수를 기록했습니다. 그러나 새로운 설비에 적용하자 실제 고장을 놓치는 사례가 크게 늘어났습니다.

개발 기록을 조사하던 운영팀은 동일 설비의 여러 측정 기록이 Train과 Test에 섞였을 가능성을 발견했습니다. 또한 입력 Feature 목록에는 **고장이 확인된 후 기록되는 수리 처리 코드** 가 포함되어 있었습니다.

기존 구현의 문제를 재현한 뒤, 어떤 원인이 성능을 과대평가했는지 근거를 제시하고 평가 절차를 복구하세요. 모델을 무조건 복잡하게 만드는 것이 목표는 아닙니다.

#### 제공 데이터

`equipment_history.csv`: 다음 열이 포함됩니다.

| 열 | 설명 | 사용 방식 |
|---|---|---|
| `record_id` | 측정 번호 | 결과 연결용 |
| `device_id` | 설비 ID | Group 분할 기준 |
| `observed_at` | 측정 시각 | 기록 시점 점검 |
| `temperature_c` | 측정 시점의 온도 | Feature |
| `vibration_rms` | 측정 시점의 진동값 | Feature |
| `load_pct` | 측정 시점의 부하율(0~100) | Feature |
| `days_since_service` | 마지막 정비 이후 경과일 | Feature |
| `failure_next_14d` | 측정 뒤 14일 안에 발생한 고장(0/1) | Target |
| `final_repair_code` | 고장 확인 후 기록한 수리 코드 | **사용 금지** |

동일 `device_id`가 여러 번 등장하며, 데이터에는 최소 30대의 설비가 포함되어 있습니다. 결측·유효하지 않은 Feature 값도 일부 존재할 수 있습니다.

#### 구현 요구사항

1. **기존 평가 재현:** 전체 데이터를 무작위로 분할한 경우의 점수를 계산하고, 해당 과정에서 동일 설비가 Train·Test에 겹치는지 확인합니다. 기존 방식의 오류를 조사하기 위한 실험임을 명시합니다.
2. **Feature Audit:** 각 열의 확보 시점을 검토하고 `final_repair_code` 및 Target이 Feature에 섞이지 않도록 차단합니다. 허용된 열의 목록을 코드에 명시합니다.
3. **Group-Based Evaluation:** 설비 ID 기준으로 Train·Validation·Test를 분할합니다. 비율은 고유 설비 수 기준 약 60%·20%·20%이고, 동일 설비가 여러 구간에 속하지 않아야 합니다.
4. **Pipeline 복구:** 숫자형 결측값은 Training Data의 중앙값으로 대체하고 StandardScaler 및 Logistic Regression으로 연결합니다. 모든 전처리의 `fit()`은 해당 Training 구간에만 수행합니다.
5. **평가:** Majority Baseline과 복구 모델의 Accuracy·Recall·Balanced Accuracy·F1을 비교합니다. 각 평가 구간에 실제 양성이 없다면 해당 지표의 정의와 보고 방식을 명시합니다.
6. **원인 분석:** 행 단위 분할과 Group 분할의 점수 차이, Feature Leakage 여부, 설비별 오류 분포를 근거로 어떤 평가 결과가 실제 도입 목표에 더 적합한지 설명합니다. 점수가 반드시 특정 수치만큼 떨어져야 한다고 가정하지 않습니다.
7. **회귀 테스트:** 다음 항목을 자동 확인하는 테스트를 작성합니다. (a) Group 교집합이 비어 있음 (b) 금지된 Feature가 학습에 들어가지 않음 (c) Training Data 밖에서 Scaling·Imputation을 학습하지 않음 (d) 동일 `random_state`에서 분할 재현 가능.

#### 입력 및 출력

**입력:** `equipment_history.csv`

**출력:**

- `data_audit.csv`: `record_id,error_code` — 처리 불가능한 행과 오류 이유
- `split_audit.json`: 행 단위 분할의 Group 중복 수, 복구 분할의 Group 교집합 수, Sample·Group 수
- `metric_comparison.csv`: `evaluation,model,accuracy,recall,balanced_accuracy,f1`
- `error_by_device.csv`: `device_id,sample_count,false_negative_count,false_positive_count` (복구된 Test 대상)
- `root_cause_report.md`: 원인, 수정 근거, 남아 있는 한계, 테스트 결과

**점검용 예시**

```text
Train device_id = {D01, D02, D03}
Test  device_id = {D03, D04}
```

위 분할의 `D03`은 양쪽에 존재합니다. **새 설비 평가를 위한 Group 분할은 해당 교집합이 빈 집합이 되어야 합니다.** 점검용 예시는 실제 CSV의 전체 데이터가 아닙니다.

#### 검증 항목

- 허용된 Feature를 명시적으로 선택하고 결과가 나온 뒤 금지 열을 다시 사용하지 않는지 확인
- 유효하지 않은 입력이 학습에 포함되는지 여부와 처리 기준의 일관성
- 행 단위 무작위 분할과 설비별 분할을 구분해 보고했는지 확인
- Test 점수를 좋게 만들기 위해 분할이나 Hyperparameter를 반복 변경하지 않았는지 확인
- 수정 전의 높은 점수가 실제 새 설비 성능을 입증하는 근거가 될 수 없는 이유를 논리적으로 설명

<details>
<summary><strong>구현 가이드</strong></summary>

1. 우선 데이터의 열 목록과 각 열을 얻을 수 있는 시점을 확인하세요. 이름이 숫자로 인코딩되어 있어도 예측 이후에 만들어진 값이라면 Feature로 사용할 수 없습니다.
2. `GroupShuffleSplit`으로 설비를 서로 다른 구간에 배정할 수 있습니다. 각 단계에서 Group 교집합이 비어 있는지 검사하세요.
3. `SimpleImputer`·`StandardScaler`·`LogisticRegression`을 하나의 Pipeline으로 구성하세요.
4. 모델 개선과 평가 설계의 복구를 구분해 기록하세요. 점수 하락이 오히려 더 신뢰할 수 있는 평가로의 변화일 수 있습니다.

</details>

---

### C-02. Library Demand Forecast Recovery — 방문객 예측 시스템 복구

**관련 개념:** [Chapter 02](../Chapter-02/README.md) · Feature Consistency · Regression · [Chapter 04](../Chapter-04/README.md) · Error Analysis · Temporal Evaluation · Pipeline

#### 문제 설명

도서관 방문객 예측 프로그램은 과거 방문 기록을 이용해 다음 날의 운영 인력을 배치합니다. 최근 데이터 제공 시스템이 변경된 뒤부터 특정 날짜의 예측이 지나치게 커지거나, 입력 파일을 읽는 도중 프로그램이 중단되는 문제가 발생했습니다.

조사 결과 이전 파일에서는 온도가 섭씨(`temperature_c`)였지만 새 파일에서는 화씨(`temperature_f`)로 제공되고 있습니다. 일부 행에는 필수 값이 누락되어 있으며 같은 날짜가 중복 전송되기도 합니다.

데이터 형식 변경을 인식하고 정상 행만 예측에 사용하도록 프로그램을 복구하세요. 잘못된 입력을 임의의 값으로 바꿔 결과를 만들어서는 안 됩니다.

#### 제공 데이터

- `history_v1.csv`: `date,temperature_c,scheduled_events,is_weekend,visitors_next_day`
- `incoming_v2.csv`: `date,temperature_f,scheduled_events,is_weekend`

`history_v1.csv`에는 최소 120일의 기록이 있으며 날짜는 유일합니다. `visitors_next_day`는 Target입니다. `incoming_v2.csv`에는 예측 대상 날짜에 **그 날짜의 업무 시작 전에 확보된** 날씨 예보 온도와 예정 행사 수가 기록되어 있다고 가정합니다.

#### 구현 요구사항

1. 입력 버전별 Schema를 명시합니다. `history_v1`은 `temperature_c`, `incoming_v2`는 `temperature_f`를 사용하며, 명시되지 않은 다른 열 이름으로 자동 추측하지 않습니다.
2. 화씨 온도는 `temperature_c = (temperature_f - 32) × 5/9`로 변환합니다. `temperature_f`는 유한한 실수이며, 빈 값은 필수 Feature 누락으로 처리합니다.
3. `scheduled_events`는 0 이상의 정수, `is_weekend`는 0 또는 1입니다. 필수 필드가 누락되거나 범위 밖인 행은 예측하지 않고 `rejected_rows.csv`에 오류 코드를 남깁니다.
4. 같은 날짜의 입력이 중복되면 **첫 번째 유효 행만 유지** 합니다. 무효 행은 해당 날짜를 점유하지 않습니다. 이후의 유효 중복 행은 `DUPLICATE_DATE`로 거부합니다.
5. 기존 History를 날짜순 Train 60%·Validation 20%·Test 나머지로 분리합니다. Baseline은 Training Target 평균이며, 후보 모델은 `StandardScaler` + `Ridge(alpha=1.0)`입니다. Validation에서는 두 방법의 MAE를 비교하지만 Test 결과로 모델을 다시 선택하지 않습니다.
6. 선택한 모델은 테스트를 통과한 뒤에만 새로운 입력에 적용합니다. 새로운 입력에서 예측 가능한 행과 거부된 행을 별도로 출력합니다.
7. 정상 입력에 대해서는 예측 날짜, 변환된 섭씨 온도, 예상 방문객 수를 저장합니다. 예측 결과는 실수로 유지하며 파일 출력 시 소수 둘째 자리까지 표시합니다.
8. `recovery_report.md`에 오류 원인, 정상 행 처리 여부, 과거 Test 성능, 새 입력에서의 거부 건수 및 복구 검증 결과를 작성합니다.

#### 입력 및 출력

**입력:** `history_v1.csv`, `incoming_v2.csv`

**출력:**

- `normalized_incoming.csv`: `date,temperature_c,scheduled_events,is_weekend` (유효하고 중복 없는 행, 입력 순서)
- `rejected_rows.csv`: `source_line,error_code` (헤더 포함 실제 파일 행 번호)
- `predictions.csv`: `date,predicted_visitors` (정상 행의 원본 순서)
- `recovery_report.md`: 수정 내용과 검증 결과

**예제 입력** (`incoming_v2.csv`)

```csv
date,temperature_f,scheduled_events,is_weekend
2026-10-01,77,1,0
2026-10-02,,0,0
2026-10-01,80,1,0
2026-10-03,68,0,1
```

**예제 정규화 결과** (`normalized_incoming.csv`)

```csv
date,temperature_c,scheduled_events,is_weekend
2026-10-01,25.0000,1,0
2026-10-03,20.0000,0,1
```

**예제 거부 결과** (`rejected_rows.csv`)

```csv
source_line,error_code
3,MISSING_TEMPERATURE
4,DUPLICATE_DATE
```

이 예제는 입력 검증용입니다. `predictions.csv`의 예상 방문객 수는 학습된 모델에 따라 달라지므로 여기서는 고정하지 않습니다.

#### 검증 항목

- `77°F → 25°C`, `68°F → 20°C` 변환 확인
- 무효 행이 중복 날짜를 먼저 점유하지 않는지 확인
- 무효 행을 0이나 평균값으로 조용히 대체하지 않는지 확인
- 온도 단위 변경 전후에 Feature의 의미가 일관되게 유지되는지 확인
- 기존 Test 성능과 새 입력에 대한 예측 결과를 혼동하지 않는지 확인
- 복구 실패 시 정상 예측 파일을 무분별하게 덮어쓰지 않도록 처리하는지 확인

<details>
<summary><strong>구현 가이드</strong></summary>

1. 파일을 읽는 단계에서 Schema 버전을 구분하고 공통 Feature 이름으로 정규화하세요.
2. 원본 행 번호를 보존하면 오류 목록의 위치를 추적할 수 있습니다.
3. 유효성 검사와 중복 확인을 끝낸 뒤에만 예측 대상을 모델에 전달하세요.
4. 기존 데이터로 Train·Validation·Test 절차를 검증한 다음, 새로운 버전의 입력을 처리하세요. 새로운 입력에는 정답 Target이 없으므로 Accuracy나 MAE를 계산하지 않습니다.

</details>

---

## Radiant

### R-01. The City That Never Sleeps — 도시 공공시설 통합 운영 분석

**관련 개념:** [Chapter 01](../Chapter-01/README.md) · AI Application & Limitations · [Chapter 02](../Chapter-02/README.md) · Regression · Feature Engineering · Leakage · [Chapter 03](../Chapter-03/README.md) · Classification · Clustering · [Chapter 04](../Chapter-04/README.md) · Evaluation Protocol · Imbalanced Metrics · Group·Temporal Split · Pipeline

#### 문제 설명

한 도시의 여러 공공시설은 방문객 수, 전력 사용량, 설비 경보를 매일 기록하고 있습니다. 운영 부서는 다음 날의 시설 이용 규모를 예측하고, 가까운 시일 내 고장 위험이 높은 시설을 찾아 점검 순서를 결정하려고 합니다. 시설별 이용 패턴을 구분해 운영 계획에 참고하는 기능도 필요합니다.

기존 분석 시스템에서는 문제가 반복되고 있습니다. 같은 날짜의 기록이 중복 전송되고, 일부 시설은 다른 시설과 데이터의 범위가 크게 다릅니다. 미래에 확인된 고장 여부가 학습 Feature에 섞인 코드도 발견되었습니다. 이전 담당자는 전체 Accuracy가 높다는 이유로 모델을 배포했지만, 실제 고장을 놓친 사례가 여러 건 발생했습니다.

문제는 **공공시설 운영을 위한 분석 시스템을 신뢰할 수 있는 상태로 재설계하는 것** 입니다. 단순히 모델 세 개를 학습하는 것으로 끝나지 않습니다. 데이터 검증, 적절한 평가, 운영 제약, 오류 처리, 결과 재현성과 처리 효율까지 하나의 프로그램으로 연결해야 합니다.

#### 제공 데이터와 시점

모든 데이터는 실습용 합성 데이터입니다. 실제 시설 운영 기록이나 개인 정보는 포함하지 않습니다.

**1. `facilities.csv` — 시설 기준 정보**

```csv
facility_id,district,capacity
F01,NORTH,300
F02,SOUTH,180
```

- `facility_id`: 시설의 고유 ID
- `district`: 지역명(집계·운영 규칙에 사용)
- `capacity`: 시설의 수용 인원, 1 이상의 정수

**2. `daily_operations.csv` — 과거 관측값과 사후 확정 Target**

```csv
facility_id,date,visitors,energy_kwh,temperature_c,alarms_7d,failure_next_7d,visitors_next_day,final_repair_cost
F01,2026-04-01,120,50,21,1,0,126,0
F01,2026-04-02,126,52,22,0,0,119,0
```

| 열 | 의미 | 사용 기준 |
|---|---|---|
| `facility_id`, `date` | 시설·관측 날짜 | 데이터 연결, 시점 구분 |
| `visitors` | 해당 날짜에 관측한 방문객 수 | Feature |
| `energy_kwh` | 해당 날짜의 전력 사용량 | Feature |
| `temperature_c` | 해당 날짜의 기온 | Feature |
| `alarms_7d` | 해당 날짜까지 최근 7일의 경보 건수 | Feature |
| `failure_next_7d` | 해당 날짜 **이후 7일 안에** 고장이 발생했는지 여부 | Classification Target |
| `visitors_next_day` | 해당 날짜 다음 날의 방문객 수 | Regression Target |
| `final_repair_cost` | 고장 처리 후 확정된 수리 비용 | **Feature 사용 금지** |

**3. `incoming_operations.csv` — 운영용 최신 관측값**

```csv
facility_id,date,visitors,energy_kwh,temperature_c,alarms_7d
F01,2026-07-01,130,53,23,1
F02,2026-07-01,82,34,23,0
```

최신 관측값에는 정답 Target이 없으며, 그날의 관측이 끝난 뒤 다음 날 수요와 향후 7일의 고장 위험을 예측합니다.

#### 데이터 처리 규칙

1. 세 파일은 헤더가 있는 UTF-8 CSV입니다. `facility_id`와 `date`의 조합은 `daily_operations.csv`에서 유일해야 하며, `incoming_operations.csv`에서도 유일해야 합니다.
2. `facilities.csv`의 `facility_id`는 중복되면 안 됩니다. 시설 기준 정보에 중복 또는 필수 열 누락이 있으면 전체 처리를 중단하고 원인을 출력합니다.
3. `daily_operations.csv`와 `incoming_operations.csv`에서는 **첫 번째 유효한 시설·날짜 기록만 인정** 합니다. 무효 행은 해당 키를 점유하지 않으며, 이후 발견된 유효 중복 행은 `DUPLICATE_RECORD`로 거부합니다.
4. 등록되지 않은 시설은 `UNKNOWN_FACILITY`, 유한하지 않은 수 또는 음수 방문객·전력·경보 수는 `INVALID_NUMBER`, 과거 Target의 형식이나 범위가 잘못된 경우는 `INVALID_TARGET`으로 기록합니다.
5. `failure_next_7d`는 0 또는 1이고, `visitors_next_day`는 0 이상의 정수입니다. `visitors`, `alarms_7d`도 0 이상의 정수입니다. `energy_kwh`는 0 이상의 유한 실수입니다. `temperature_c`는 유한 실수이며 음수도 허용합니다.
6. `final_repair_cost`는 이 과제에서 사용하지 않는 사후 기록입니다. 입력 파일에 존재하더라도 학습 Feature 또는 평가 기준으로 이용하지 않습니다.
7. 무효 행을 제외한 뒤 `facility_id`, `date`의 고유성이 유지되어야 합니다. 오류 행은 `source_file,source_line,error_code` 순으로 기록하며, `source_line`은 헤더를 포함한 실제 파일 행 번호입니다.

#### 구현 요구사항

**STEP 01 — 데이터 검증과 추적 가능성**

- 입력 파일의 Schema, 필수 열, 숫자 범위, 시설 ID의 존재 여부를 확인합니다.
- 유효한 기록과 오류 기록을 분리하고, 데이터 건수·시설 수·오류 코드별 건수를 기록합니다.
- 정상 데이터를 정렬한 파일을 생성합니다. 정렬 기준은 **날짜 오름차순, 같은 날짜에서는 시설 ID 오름차순** 입니다.
- 거부된 행은 이후 모델 학습·예측에 영향을 주어서는 안 됩니다.

**STEP 02 — 미래 정보가 섞이지 않는 평가 분할**

과거 데이터는 다음 기간으로 구분합니다.

| 구간 | 기록 날짜 | 사용 목적 |
|---|---|---|
| Training | 2026-01-01 ~ 2026-04-30 | 모델·전처리 기준 학습 |
| Gap 1 | 2026-05-01 ~ 2026-05-07 | 평가에서 제외 |
| Validation | 2026-05-08 ~ 2026-05-31 | Threshold·모델 후보 선택 |
| Gap 2 | 2026-06-01 ~ 2026-06-07 | 평가에서 제외 |
| Test | 2026-06-08 ~ 2026-06-30 | 최종 성능 확인 |

고장 Target이 미래 7일을 대상으로 하므로 구간 사이에 7일의 Gap을 둡니다. Gap의 기록은 학습·설정 선택·최종 점수에 포함하지 않습니다. 제공된 데이터는 최소 10개 시설과 각 평가 구간의 유효 기록을 포함한다고 가정합니다.

또한 새로운 시설에 대한 일반화 여부도 따로 확인합니다.

- 고유한 `facility_id`를 문자열 오름차순으로 정렬합니다.
- **5번째, 10번째, 15번째 … 시설** 을 신규 시설 평가용 Holdout으로 정합니다. 이 시설의 모든 기록은 Training·Validation 및 전처리 학습에서 제외합니다.
- **평가 A:** Holdout이 아닌 기존 시설의 Test 기간 성능
- **평가 B:** 학습에 전혀 사용하지 않은 Holdout 시설의 Test 기간 성능

두 평가 결과는 따로 보고합니다. Holdout 시설의 Target을 이용해 모델이나 Threshold를 선택하지 않습니다. Holdout이 아닌 시설의 Training과 Validation에서만 설정을 선택합니다.

**STEP 03 — 설비 고장 위험 Classification**

- 허용된 숫자형 Feature는 `visitors`, `energy_kwh`, `temperature_c`, `alarms_7d`, `capacity`입니다.
- Baseline으로 `DummyClassifier(strategy='most_frequent')`를 사용합니다.
- 후보 모델은 `StandardScaler`와 `LogisticRegression(max_iter=1000)`을 연결한 Pipeline입니다.
- Validation에서 Threshold `[0.25, 0.40, 0.55]`의 F2를 비교합니다. 동점일 경우 큰 Threshold를 선택합니다.
- 확정한 모델과 Threshold를 사용해 평가 A·B에서 Precision·Recall·F2·Confusion Matrix를 구합니다. 평가 구간에 실제 양성이 없거나 양성 예측이 없을 때는 분모가 0인 지표를 구분하여 보고합니다.
- 운영용 입력에서는 Threshold를 통과한 시설을 **지역·날짜별 최대 10개** 까지 점검 대상으로 등록합니다. 점수 내림차순, 동점이면 시설 ID 오름차순으로 선택합니다. 선택하지 않은 시설도 점수와 미선택 이유를 보존합니다.

**STEP 04 — 다음 날 방문객 수 Regression**

- 같은 Feature에서 Target을 `visitors_next_day`로 바꿉니다.
- Baseline은 각 시설의 **해당 날짜 `visitors`를 다음 날 값으로 그대로 예측** 하는 방법입니다.
- 후보 모델은 `StandardScaler` + `Ridge`이며 `alpha` 후보 `[0.1, 1.0, 10.0]`을 Validation MAE로 비교합니다. 동점이면 작은 `alpha`를 선택합니다.
- 평가 A·B에서 MAE·RMSE를 계산합니다. 지역별 MAE와 과소 예측이 큰 사례도 별도로 기록합니다.
- 최종 선택한 회귀 모델을 운영용 입력에 적용합니다.

**STEP 05 — 시설 이용 패턴 Clustering**

- Training 기간의 Holdout이 아닌 시설 기록에서 `visitors`, `energy_kwh`, `alarms_7d`만 사용합니다.
- Training Data로 StandardScaler를 학습하고 `KMeans(n_clusters=3, n_init=10, random_state=42)`를 적용합니다.
- Cluster별 Sample 수와 **원본 단위** 의 Feature 평균을 계산합니다.
- 기준 결과의 안정성을 확인하기 위해 동일한 Training Data에서 `random_state=7` 결과와 ARI를 계산합니다.
- 운영용 데이터의 Cluster를 지정할 때는 이미 학습한 Scaler와 KMeans의 `predict()`를 사용합니다. 운영 데이터로 중심을 다시 학습하지 않습니다.
- Cluster ID를 시설의 확정된 등급이나 정답 Label로 해석하지 않습니다.

**STEP 06 — 결과 재현성 및 장애 대응**

- 동일 입력, 동일 라이브러리 환경, 동일 Parameter에서 반복 실행했을 때 결과 행 순서와 파일 내용이 일치해야 합니다.
- 필수 입력 파일을 읽지 못하면 이전 정상 결과 파일을 덮어쓰지 않습니다.
- 유효한 데이터가 부족하거나 학습 구간의 Classification Target이 한 클래스뿐이라 모델을 학습할 수 없다면, 임의의 점수를 생성하지 않고 이유를 보고합니다.
- 결과 파일은 먼저 별도 임시 디렉터리에 모두 생성·검사한 뒤 배포합니다. 여러 파일을 한 번에 교체하는 작업은 원자적이지 않으므로 부분 실패를 탐지하고 이전 결과로 복구하는 방법을 문서화합니다.
- 운영 입력에는 실제 Target이 없으므로 운영용 데이터에 대한 MAE나 Recall을 계산하지 않습니다.

**STEP 07 — 처리 효율 분석**

- 올바른 기준 구현을 완성한 뒤 같은 Schema의 **100,000행 이상 실습용 합성 데이터** 로 처리 시간과 메모리 사용량을 측정합니다.
- 행마다 전체 시설 목록을 반복 탐색하는 방법과 Dictionary 조회·Pandas 결합 등을 이용한 방법을 비교할 수 있습니다.
- 최적화 전후에 데이터 검증 결과와 출력 행이 동일한지 확인해야 합니다.
- 처리 시간, 데이터 규모, 측정 환경과 개선 근거를 기록합니다. 빠른 실행을 위해 검증이나 평가를 생략해서는 안 됩니다.

#### 입력 및 출력 규격

**입력:** `facilities.csv`, `daily_operations.csv`, `incoming_operations.csv`

**출력:**

| 파일 | 포함할 내용 |
|---|---|
| `clean_history.csv` | 허용된 과거 행, 날짜·시설 ID 오름차순 |
| `rejected_rows.csv` | `source_file,source_line,error_code` |
| `split_report.json` | 구간별 Sample·시설 수, Gap 제외 수, 신규 시설 Holdout ID, Group 교집합 확인 |
| `model_report.json` | 모델·Threshold·Alpha 선택 결과, Baseline, 평가 A·B의 지표 |
| `test_predictions.csv` | 시설 ID, 날짜, 고장 실제값·점수·예측, 방문객 실제값·예측값·Residual, 평가 A/B |
| `operational_predictions.csv` | 시설 ID, 날짜, 고장 점수, 다음 날 방문객 예측, Cluster ID |
| `inspection_queue.csv` | 날짜, 지역, 점검 순위, 시설 ID, 고장 점수 |
| `cluster_profiles.csv` | Cluster ID, Sample 수, 원본 단위 평균 |
| `performance_report.md` | 데이터 규모, 처리 시간, 메모리 사용량, 비교 결과 |
| `final_report.md` | 설계 근거, 장애 원인, 복구 정책, 평가·오류 분석, 남아 있는 한계 |

숫자형 점수는 파일에서 소수 넷째 자리까지, 예측 방문객 수는 소수 둘째 자리까지 기록합니다. 파일 내부 정렬 규칙을 일관되게 적용합니다. 출력 폴더에 기존 결과가 있다면 복구 가능한 상태로 보존해야 합니다.

#### 공개 검증 예제 — 행 검증과 중복 제어

다음 입력은 **STEP 01 검증용** 입니다. 전체 모델 학습을 수행하기 위한 크기의 데이터는 아닙니다.

**예제 입력** (`daily_operations.csv`)

```csv
facility_id,date,visitors,energy_kwh,temperature_c,alarms_7d,failure_next_7d,visitors_next_day,final_repair_cost
F01,2026-04-01,120,50,21,1,0,126,0
F01,2026-04-01,130,51,22,1,0,129,0
F02,2026-04-01,-5,30,19,0,1,45,0
F02,2026-04-01,55,30,19,0,0,60,0
```

`facilities.csv`에는 `F01`, `F02`가 유효하게 등록되어 있다고 가정합니다.

**예제 출력** (`rejected_rows.csv`)

```csv
source_file,source_line,error_code
daily_operations.csv,3,DUPLICATE_RECORD
daily_operations.csv,4,INVALID_NUMBER
```

**정상 기록 결과** (`clean_history.csv`에 포함되는 데이터 행)

```csv
F01,2026-04-01,120,50,21,1,0,126,0
F02,2026-04-01,55,30,19,0,0,60,0
```

첫 번째 `F01` 기록만 인정합니다. `F02`의 무효 행은 키를 점유하지 않으므로 그다음 유효 기록은 정상 처리합니다.

#### 최종 검증 항목

1. **데이터 무결성:** 입력 오류와 중복이 예측 결과에 반영되지 않는지 확인
2. **정보 누출 방지:** 사후 Target·수리비, 미래 날짜, 평가용 Holdout 데이터가 학습 Feature나 설정 선택에 사용되지 않는지 확인
3. **독립적인 평가:** 기존 시설과 신규 시설의 성능을 별도로 계산하고 Test에서 재조정하지 않는지 확인
4. **운영 규칙:** 지역별 일일 점검 한도, 동점 처리, Threshold 미달 및 정렬 규칙이 지켜지는지 확인
5. **Clustering 해석:** Cluster ID가 임의의 번호이고, 결과의 안정성과 실제 특징을 분석했는지 확인
6. **복구 가능성:** 실패한 실행이 이전의 정상 결과를 손상하지 않고, 오류 이유가 추적 가능한지 확인
7. **재현성:** 같은 입력에 대한 파일 내용과 순서가 반복 실행에서 일치하는지 확인
8. **성능 개선:** 처리 시간이 줄어도 분석 결과가 바뀌지 않는지 검증

#### 제출 결과물

실행 코드, 요구되는 출력 파일, 자동 테스트, 실행 명령과 의존 라이브러리를 기록한 문서, 최종 분석 보고서를 제출합니다. 코드 구조는 자유롭게 설계할 수 있지만, **예측 결과를 재현하고 오류가 발생한 이유를 설명할 수 있어야 합니다.**

<details>
<summary><strong>구현 가이드</strong></summary>

1. **입력 계약부터 고정:** CSV별 필수 열과 오류 코드를 정의하세요. 정상 행만 모아 모델 단계에 전달하면 학습 코드가 단순해집니다.
2. **분할과 Feature 목록부터 검증:** 모델을 만들기 전에 날짜 구간, Holdout 시설 목록, 허용 Feature 목록을 먼저 검사하세요.
3. **Baseline과 첫 모델 구현:** Classification·Regression의 기준 성능을 기록한 다음 후보 모델을 추가하세요. 설정 선택은 Validation에서 끝내야 합니다.
4. **분석 과제 분리:** Classification과 Regression은 Label이 필요하지만 Clustering은 Label 없이 패턴을 찾습니다. 세 결과가 서로 다른 목적을 가진다는 점을 유지하세요.
5. **운영 규칙과 평가 분리:** Test의 성능 지표와 운영 점검 대상 선정은 서로 다른 출력입니다. 후자는 용량 제한까지 반영해야 합니다.
6. **오류·재현성 테스트:** 누락 열, 비정상 숫자, 중복 키, 미래 Target 혼입, 한 클래스만 있는 데이터, 결과 파일 교체 실패를 각각 검증하세요.
7. **최적화는 마지막에:** 기준 구현과 결과가 동일하다는 것을 먼저 확인한 뒤 처리 시간을 비교하세요.

</details>

---

[← Summary 목차](./README.md) · [Quiz](./quiz.md) · [AI 목차](../README.md)
