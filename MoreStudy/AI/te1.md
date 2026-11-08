# Quiz & Review — Part 01

Chapter 01~04 · **객관식 16문항 · 주관식 8문항**

객관식은 가장 적절한 답을 하나 고르시오. 주관식은 계산 과정이나 판단 근거를 포함하여 답하시오. 정답 및 해설은 답안을 작성한 뒤 확인할 수 있습니다.

[← Summary 목차](./README.md) · [Problems](./problem.md) · [AI 목차](../README.md)

## 객관식

### Q-01. Rule-Based Systems와 Machine Learning

**관련 개념:** [Chapter 01](../Chapter-01/README.md) · Rule-Based Systems · Machine Learning

지능형 도서관 시스템 구축을 위해 이용자의 신청 데이터를 자동 분류하는 모델을 설계하려고 합니다. 다음 중 **규칙 기반 시스템(Rule-based System) 대신 학습 기반(머신러닝) 분류 모델을 도입하는 근거로 가장 적절한 것**은 무엇입니까?

1. 필수 입력 필드의 누락 여부나 데이터 형식 검증 등 정형화된 유효성 검사는 머신러닝 모델이 명시적 조건문보다 항상 더 효율적으로 처리하기 때문이다.
2. 분류를 위한 의사결정 기준이 너무 복잡하여 명확한 `if-else` 규칙으로 정의하기 어렵고, 과거에 축적된 정답 레이블(Labeled Data)이 충분히 존재하기 때문이다.
3. 머신러닝 모델은 학습 데이터의 노이즈나 분포 변화에 민감하지 않으므로, 데이터 전처리와 성능 검증 과정을 생략할 수 있기 때문이다.
4. 한 번 학습이 완료된 모델은 운영 환경에서 데이터 특성이 변하더라도 추가적인 성능 모니터링이나 재학습이 필요 없기 때문이다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ②**

도서 분류나 자연어 처리 등 복잡한 패턴을 가진 문제는 명확한 코딩 규칙을 세우기 어렵습니다. 이 경우 충분한 양의 과거 정답 데이터(Labeled Data)가 확보되어 있다면 머신러닝을 통한 학습 기반 접근이 적합합니다.

- ①: 필수값 검사나 단순 형식 체크는 머신러닝 모델을 사용하는 것보다 가볍고 명확한 규칙 기반(Rule-based) 조건문으로 처리하는 것이 원칙입니다.
- ③: 머신러닝 모델은 데이터의 품질에 절대적인 영향을 받으며, 노이즈와 편향을 제거하기 위한 데이터 전처리(Preprocessing)는 필수적입니다.
- ④: 시간 흐름에 따른 데이터 분포 변화(Data/Concept Drift)로 인해 실제 운영 환경에서는 지속적인 모니터링과 재학습(Retraining)이 필수적입니다.

</details>

### Q-02. AI 결과의 자동 처리 범위

**관련 개념:** [Chapter 01](../Chapter-01/README.md) · Inference · Human Review · AI Limitations

손글씨 숫자 이미지 분류 모델이 특정 입력 데이터에 대해 클래스 `8`의 예측 확률(Confidence Score)을 가장 높게 출력했습니다. 이 모델을 실제 서비스 환경에 배포하고 운영할 때, **가장 타당한 의사결정 방식**은 무엇입니까?

1. 모델이 가장 높은 확률값으로 예측했으므로, 실제 정답 여부와 관계없이 해당 결과를 무조건 클래스 `8`로 자동 확정하여 처리한다.
2. 검증 단계의 전체 정확도(Accuracy)가 우수하다면, 운영 환경의 모든 입력 데이터에 대해 사람의 검토나 예외 처리 절차를 완전히 배제한다.
3. 오분류로 인해 발생하는 비즈니스 리스크와 비용을 고려하여, 모델의 예측 신뢰도 임계값(Confidence Threshold)을 기준으로 자동 처리 영역과 사람의 검토(Human-in-the-Loop) 영역을 나누어 설계한다.
4. 운영 중 잘못 인식된 케이스가 발견될 경우, 해당 샘플을 테스트 데이터셋(Test Dataset)에 임의로 추가하여 모델의 예측 점수가 높아질 때까지 평가 지표와 임계값을 반복적으로 튜닝한다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ③**

실제 운영 환경에서는 모델의 예측이 항상 완벽할 수 없으므로, 오인식에 따른 비용(Cost)을 분석해야 합니다. 신뢰도가 높은 데이터는 자동 처리하고, 불확실한 데이터는 전문가가 검토하는 휴먼 인 더 루프(Human-in-the-Loop) 시스템 및 임계값 설계를 적용하는 것이 타당합니다.

- ①: 모델이 출력하는 높은 확률값(Softmax Score 등)이 곧 100%의 실제 정답을 보장하지 않으며, 오버콘피던스(Overconfidence) 현상도 존재합니다.
- ②: 전체 평균 정확도가 높더라도 특정 샘플이나 이상치(Outlier)에서 치명적인 오류가 발생할 수 있으므로 안전장치가 필요합니다.
- ④: 테스트 데이터는 모델의 성능을 독립적으로 평가하기 위해 엄격히 분리되어 있어야 합니다. 테스트 결과를 보고 데이터를 수정하거나 임계값을 맞추는 행위는 데이터 누수(Data Leakage) 및 평가의 독립성 훼손으로 이뤄집니다.

</details>

### Q-03. Sample과 Feature의 형태

**관련 개념:** [Chapter 02](../Chapter-02/README.md) · Sample · Feature · Target · Array Shape

다음 파이썬 코드에서 `X.shape`와 `y.shape`는 무엇입니까?

```python
import numpy as np

X = np.array([
    [2, 10, 1],
    [3, 12, 0],
    [4, 15, 1],
    [5, 18, 0],
])
y = np.array([0, 1, 1, 0])
```

1. `(3, 4)`와 `(4, 1)`
2. `(4, 3)`과 `(4,)`
3. `(4,)`와 `(3,)`
4. `(4, 3)`과 `(3,)`

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ②**

`X`는 4개의 샘플(Sample)과 3개의 특성(Feature)으로 구성된 2차원 배열이므로 `(4, 3)`의 형상을 가집니다. `y`는 각 샘플의 타겟(Target) 값을 담은 1차원 배열(1D Array)이므로 `(4,)`의 형상을 가집니다. (주의: `(4,)`와 `(4, 1)`은 **차원이 다른 서로 다른 형태**입니다.)

- ①: 행과 열의 차원 순서를 거꾸로 잘못 지정하였고, y를 임의의 2차원 열 벡터(Column Vector) 형태로 혼동했습니다.
- ③: X의 전체 샘플 수와 특성 차원 인덱스가 뒤바뀌었습니다.
- ④: 타겟 데이터 y의 크기(4개)를 특성 수(3개)와 혼동했습니다.

</details>

### Q-04. 예측 시점에 사용할 수 없는 Feature

**관련 개념:** [Chapter 02](../Chapter-02/README.md) · Feature · Data Leakage

택배를 **접수하는 시점**에 배송 지연 여부를 예측하려고 합니다. 다음 중 **특성(Feature)에서 반드시 제외해야 하는 항목**은 무엇입니까?

1. 택배 접수 시각
2. 배송 지역
3. 접수 당시의 예상 이동 거리
4. 배송을 완료한 뒤 기록된 실제 도착 시각

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ④**

예측을 하려는 시점은 **택배를 접수할 때**입니다. '실제 도착 시각'은 배송이 완전히 끝난 후에야 알 수 있는 값이므로, 접수 시점에 사용할 수 없습니다. 이를 포함해 학습시키면 실제 서비스에서는 예측을 할 수 없게 됩니다.

- ①, ②, ③은 접수 시점에 이미 알 수 있거나 미리 확인할 수 있는 정보들이므로 특성(Feature)으로 사용할 수 있습니다.

</details>

### Q-05. Loss와 Gradient의 방향

**관련 개념:** [Chapter 02](../Chapter-02/README.md) · Loss Function · Gradient Descent

단일 샘플에 대해 모델을 $\hat{y} = wx$로 정의합니다. 입력 $x = 2$, 실제값 $y = 5$, 현재 가중치 $w = 1$이고 손실 함수(Loss)가 $L = (wx - y)^2$일 때, 학습률(Learning Rate)이 $0.1$이라면 경사 하강법(Gradient Descent)을 **한 번 적용한 이후의 가중치** $w$는 얼마입니까?

1. `-0.2`
2. `1.2`
3. `2.2`
4. `3.0`

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ③**

**1. 기울기(Gradient) 계산**

손실 함수 $L$을 가중치 $w$에 대해 미분하면 다음과 같습니다.

```math
\frac{\partial L}{\partial w} = 2(wx-y)\cdot x
```

주어진 값($x=2$, $y=5$, $w=1$)을 대입하면,

```math
\frac{\partial L}{\partial w} = 2(1\times2-5)\times2 = -12
```

**2. 가중치 업데이트**

학습률 $\eta=0.1$을 적용한 경사 하강법의 가중치 갱신 공식은 다음과 같습니다.

```math
w_{\text{new}} = w-\eta\frac{\partial L}{\partial w}
```

계산한 기울기를 대입하면,

```math
w_{\text{new}} = 1-0.1\times(-12) = 2.2
```

따라서 한 번의 경사 하강법 적용 후 가중치는 **2.2**입니다.

**오답 해설**

- **① `-0.2`:** 기울기의 부호를 반대로 적용한 경우입니다.
- **② `1.2`:** 가중치의 변화량과 갱신된 가중치를 혼동한 경우입니다.
- **④ `3.0`:** 기울기와 학습률을 올바르게 적용하지 않은 결과입니다.

</details>


### Q-06. Feature Scaling이 중요한 이유

**관련 개념:** [Chapter 02](../Chapter-02/README.md) · Feature Scaling · KNN

어떤 KNN 모델은 `age`(20~70)와 `annual_income`(20,000,000~100,000,000)을 Feature로 사용합니다. 원본 값으로 유클리드 거리를 계산할 때 발생할 수 있는 문제는 무엇입니까?

1. 범위가 큰 `annual_income`이 거리 계산을 지배할 수 있습니다.
2. KNN은 숫자형 Feature를 처리할 수 없습니다.
3. Scaling을 하면 Test Data의 Label이 자동으로 바뀝니다.
4. KNN은 Feature 간 거리를 계산하지 않으므로 Scaling과 관계가 없습니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ①**

거리 기반 모델은 Feature 값의 크기에 민감할 수 있습니다. 필요한 경우 Training Data로 Scaling 기준을 학습한 뒤 Validation·Test Data에 동일한 변환을 적용합니다.

- ② KNN은 숫자형 Feature를 활용할 수 있습니다.
- ③ Scaling은 Feature 변환이며 Target Label을 자동 변경하지 않습니다.
- ④ KNN은 Sample 간 거리 또는 이웃 관계를 이용합니다.

</details>

### Q-07. Decision Threshold 적용

**관련 개념:** [Chapter 03](../Chapter-03/README.md) · Logistic Regression · Decision Threshold

클래스 1에 대한 예측 점수가 `[0.40, 0.65, 0.80]`입니다. `score >= threshold`이면 Label 1로 판단할 때, Threshold가 `0.65`인 예측 결과는 무엇입니까?

1. `[0, 0, 1]`
2. `[0, 1, 1]`
3. `[1, 1, 1]`
4. `[0, 1, 0]`

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ②**

`0.40 < 0.65`이므로 첫 번째는 0입니다. 두 번째 값은 Threshold와 같으므로 1, 세 번째도 1입니다. 비교 연산자가 `>`인지 `>=`인지에 따라 경계값의 처리 결과가 달라집니다.

- ① 경계값 `0.65`를 잘못 제외했습니다.
- ③ `0.40`은 기준을 충족하지 않습니다.
- ④ `0.80`은 기준을 충족합니다.

</details>

### Q-08. KMeans 중심 갱신

**관련 개념:** [Chapter 03](../Chapter-03/README.md) · KMeans · Cluster Centroid

KMeans의 한 Cluster에 `(0, 0)`, `(2, 4)`, `(4, 2)`가 할당되었습니다. 이 Cluster의 새 중심 좌표는 무엇입니까?

1. `(2, 2)`
2. `(6, 6)`
3. `(0, 0)`
4. `(2, 3)`

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ①**

Cluster의 중심은 할당된 Sample의 Feature별 평균입니다. 첫 좌표는 `(0+2+4)/3=2`, 둘째 좌표는 `(0+4+2)/3=2`이므로 `(2, 2)`가 됩니다.

- ② 평균이 아니라 합계를 구했습니다.
- ③ 첫 번째 Sample을 중심으로 고정했습니다.
- ④ 두 번째 좌표의 평균을 잘못 계산했습니다.

</details>

### Q-09. KMeans와 DBSCAN의 선택

**관련 개념:** [Chapter 03](../Chapter-03/README.md) · KMeans · DBSCAN · Noise

좌표 데이터에 길게 휘어진 두 개의 밀집 영역과 몇 개의 고립된 점이 있습니다. 다음 설명 중 **가장 적절한 것** 은 무엇입니까?

1. KMeans는 어떤 형태의 Cluster든 항상 정확하게 구분합니다.
2. DBSCAN은 밀도에 따라 연결된 영역을 찾고 일부 점을 Noise로 구분할 수 있으므로 비교할 가치가 있습니다.
3. DBSCAN은 Cluster 수 `k`를 반드시 입력해야 합니다.
4. Clustering은 정답 Label이 없으면 실행할 수 없습니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ②**

KMeans는 중심까지의 거리로 Sample을 할당하므로 구부러진 영역을 분리하는 데 한계가 있을 수 있습니다. DBSCAN은 밀도 기반 방법이며 `eps`, `min_samples`, 데이터의 Scaling에 따라 결과가 달라집니다.

- ① KMeans가 모든 형태를 정확하게 구분하지는 않습니다.
- ③ `k`는 KMeans의 대표적인 설정입니다. DBSCAN은 밀도 관련 Parameter를 사용합니다.
- ④ Unsupervised Learning은 정답 Label 없이 패턴을 탐색할 수 있습니다.

</details>

### Q-10. Cluster 번호와 실제 Label

**관련 개념:** [Chapter 03](../Chapter-03/README.md) · Unsupervised Learning · Cluster Interpretation

KMeans 결과가 `[0, 0, 1, 1]`, 실제 정답 Label이 `[1, 1, 0, 0]`으로 나왔습니다. 이에 대한 설명 중 **가장 옳은 것** 은 무엇입니까?

1. Cluster ID와 Label이 모두 반대이므로 군집화는 완전히 실패했습니다.
2. Cluster ID를 Target Label로 사용해 `accuracy_score()`를 계산하면 언제나 적절합니다.
3. Cluster ID는 임의의 식별 번호이므로 번호가 다르다는 이유만으로 군집 구조가 틀렸다고 판단할 수 없습니다.
4. KMeans는 학습할 때 정답 Label을 사용하므로 이러한 결과가 나올 수 없습니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ③**

Clustering의 Cluster ID는 클래스 이름과 같은 의미가 아닙니다. 위 결과는 번호만 바꾸면 같은 분할 구조를 나타냅니다. Label이 별도로 있는 평가 상황이라면 ARI처럼 Cluster 번호의 치환에 영향을 받지 않는 지표를 고려할 수 있습니다.

- ① 식별 번호와 분할 구조를 혼동했습니다.
- ② ID를 그대로 Accuracy와 비교하면 결과를 잘못 해석할 수 있습니다.
- ④ KMeans는 정답 Label을 사용하지 않는 대표적인 Unsupervised Learning 방법입니다.

</details>

### Q-11. 높은 Accuracy가 충분하지 않은 경우

**관련 개념:** [Chapter 04](../Chapter-04/README.md) · Imbalanced Data · Accuracy · Recall

100건의 데이터 중 실제 이상 사례는 5건입니다. 모든 사례를 정상(0)으로 예측한 모델의 Accuracy와 이상 클래스(1)의 Recall은 무엇입니까?

1. Accuracy 95%, Recall 0%
2. Accuracy 95%, Recall 95%
3. Accuracy 5%, Recall 0%
4. Accuracy 100%, Recall 5%

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ①**

정상 95건을 모두 맞혔으므로 Accuracy는 `95/100=0.95`입니다. 그러나 실제 이상 5건 중 하나도 찾아내지 못했으므로 Recall은 `0/5=0`입니다.

- ② 정상 사례의 정답률을 이상 사례 Recall과 혼동했습니다.
- ③ 전체 정답 수가 5건이 아니라 95건입니다.
- ④ 모든 Sample을 맞히지 않았습니다.

</details>

### Q-12. Precision·Recall·F1 계산

**관련 개념:** [Chapter 04](../Chapter-04/README.md) · Confusion Matrix · F1 Score

이진 분류 모델의 결과가 `TP = 8`, `FP = 2`, `FN = 6`, `TN = 24`입니다. Precision과 Recall에 대한 설명 중 **가장 올바른 것** 은 무엇입니까?

1. Precision은 `8/14`, Recall은 `8/10`입니다.
2. Precision은 `8/10`, Recall은 `8/14`입니다.
3. Precision은 `24/26`, Recall은 `8/40`입니다.
4. Precision과 Recall은 모두 `8/40`입니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ②**

$$
\mathrm{Precision}=\frac{TP}{TP+FP}=\frac{8}{10}=0.8
$$

$$
\mathrm{Recall}=\frac{TP}{TP+FN}=\frac{8}{14}\approx0.5714
$$

참고로 $F_1=2TP/(2TP+FP+FN)=16/24\approx0.6667$입니다.

- ① Precision과 Recall의 분모가 바뀌었습니다.
- ③ TN은 위 두 지표의 분자에 사용되지 않습니다.
- ④ 전체 Sample 수는 Accuracy의 분모에 해당합니다.

</details>

### Q-13. Regression Metrics 비교

**관련 개념:** [Chapter 04](../Chapter-04/README.md) · MAE · MSE · RMSE

두 예측의 Residual이 각각 `1`, `-3`입니다. 이 데이터의 MAE와 MSE는 무엇입니까?

1. MAE `2`, MSE `5`
2. MAE `-1`, MSE `-4`
3. MAE `4`, MSE `10`
4. MAE `5`, MSE `2`

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ①**

$$
\mathrm{MAE}=\frac{|1|+|-3|}{2}=2
$$

$$
\mathrm{MSE}=\frac{1^2+(-3)^2}{2}=5
$$

RMSE는 $\sqrt{5}\approx2.236$입니다.

- ② 부호가 있는 Residual의 평균을 MAE로 잘못 사용했습니다.
- ③ 합계를 구하고 Sample 수로 나누지 않았습니다.
- ④ MAE와 MSE의 정의를 혼동했습니다.

</details>

### Q-14. Hyperparameter 선택과 Test Data

**관련 개념:** [Chapter 04](../Chapter-04/README.md) · Validation · Test Data · Hyperparameter Tuning

여러 모델 중 하나를 선택해야 합니다. 다음 절차 중 **최종 Test 평가의 독립성을 가장 잘 유지하는 방법** 은 무엇입니까?

1. Test 점수를 확인하면서 Hyperparameter를 반복 변경하고 가장 높은 점수를 보고합니다.
2. 전체 데이터를 한 번에 학습한 뒤 그 데이터에서 정확도를 측정합니다.
3. Training Data에서 모델을 학습하고 Validation 또는 Cross-Validation으로 설정을 선택한 다음, 확정된 모델을 Test Data에서 평가합니다.
4. Test Data를 모델 선택에 사용했다면 그 데이터를 다시 Validation이라고 부르면 문제가 없습니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ③**

설정 선택과 최종 평가는 분리해야 합니다. Test 결과를 반복적으로 활용하면 Test Data에도 모델 선택이 맞춰집니다.

- ① 반복 사용한 Test 점수는 독립적인 최종 검증 결과가 아닙니다.
- ② Training 성능은 일반화 성능을 대표하지 않습니다.
- ④ 이름만 변경해도 데이터의 사용 목적이 달라지지는 않습니다.

</details>

### Q-15. 반복 측정 데이터의 분할

**관련 개념:** [Chapter 04](../Chapter-04/README.md) · GroupKFold · Group-Aware Evaluation

동일한 산업용 장비에서 일주일 간격으로 여러 번 측정한 데이터가 있습니다. 목표는 **학습에 포함되지 않은 장비** 의 상태를 예측하는 것입니다. 어떤 평가 방식이 가장 적절합니까?

1. 각 행을 완전히 무작위로 나눈 K-Fold
2. 동일 장비의 기록이 Train과 Validation에 동시에 포함되지 않도록 장비 ID를 기준으로 나누는 Group 분할
3. 전체 데이터의 각 Feature 평균으로 Target을 채우는 방법
4. 정확도가 가장 높게 나오는 분할을 반복해서 선택하는 방법

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ②**

새로운 장비를 대상으로 일반화 성능을 확인하려면 동일 장비의 Sample이 Train과 Validation에 함께 나타나지 않아야 합니다. `GroupKFold` 또는 적절한 Group 기반 분할을 검토할 수 있습니다.

- ① 행 단위 분할은 동일 장비의 특성이 양쪽으로 전달될 수 있습니다.
- ③ Target을 Feature 평균으로 바꾸는 것은 평가 분할 방법이 아닙니다.
- ④ 높은 점수가 나오는 분할만 선택하면 평가가 편향됩니다.

</details>

### Q-16. 시간 순서가 있는 데이터의 평가

**관련 개념:** [Chapter 04](../Chapter-04/README.md) · Temporal Split · Generalization

지난달까지의 시설 방문 기록을 사용해 다음 달 방문객 수를 예측하려고 합니다. 다음 중 **가장 타당한 평가 방식** 은 무엇입니까?

1. 미래 날짜의 기록을 Train에 포함하고 과거 날짜를 Test로 사용합니다.
2. 모든 행을 무작위로 섞으면 시간 순서는 고려할 필요가 없습니다.
3. 더 최신인 데이터의 통계를 사용해 과거 Training Data의 결측값을 채운 뒤 평가합니다.
4. 과거 기간으로 학습하고 그 이후 기간을 Validation과 Test로 나누어 평가합니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ④**

미래 값을 예측하는 모델은 실제 운영 시점에 확보할 수 있는 과거 정보를 사용해야 합니다. 평가에서도 시간 순서를 유지하고, 전처리 기준을 Training Data로부터 학습해야 합니다.

- ① 미래 정보를 사용해 과거를 예측하면 목표 운영 상황과 다릅니다.
- ② 시간에 따른 변화와 미래 정보 누출을 놓칠 수 있습니다.
- ③ 미래 데이터의 통계도 예측 시점에 이용할 수 없을 수 있습니다.

</details>

## 주관식

### Q-17. 자동화와 AI의 차이

**관련 개념:** [Chapter 01](../Chapter-01/README.md) · Rule-Based Systems · AI Tasks · Human Review

다음 두 업무를 확인하고, 각각 Rule-Based Systems와 Machine Learning 중 어느 접근이 먼저 적절한지 설명하시오.

- 업무 A: 온라인 신청서에서 생년월일이 비어 있으면 `REQUIRED_FIELD` 오류를 반환합니다.
- 업무 B: 과거 상담 기록을 이용해 새로운 상담 문의의 담당 부서를 분류합니다. 문의 문장은 매번 달라지며 과거 분류 Label이 준비되어 있습니다.

두 번째 업무에 학습 모델을 사용하더라도 사람의 검토가 필요한 상황을 한 가지 제시하시오.

<details>
<summary><strong>정답 및 해설</strong></summary>

업무 A는 필수 필드의 존재 여부를 확인하므로 Rule-Based Systems가 적절합니다. 업무 B는 문장 표현이 다양하고 과거 Label을 이용할 수 있으므로 Supervised Learning을 검토할 수 있습니다.

업무 B에서도 모델 점수가 낮거나, 잘못 분류했을 때 처리 지연의 영향이 큰 문의는 사람이 검토하도록 설계할 수 있습니다. 모든 업무에 AI를 적용하는 것이 목표는 아닙니다. **문제의 규칙을 명확히 작성할 수 있는지, 학습 데이터가 있는지, 오류가 발생했을 때 어떤 영향이 있는지** 가 판단 기준입니다.

</details>

### Q-18. Linear Regression의 예측 계산

**관련 개념:** [Chapter 02](../Chapter-02/README.md) · Feature · Linear Regression · Matrix Operation

다음 세 Sample에 대해 `ŷ = 2x₁ - x₂ + 1`을 계산하는 NumPy 코드를 작성하시오. 예측값 배열의 Shape와 값을 함께 제시하시오.

```python
import numpy as np

X = np.array([
    [1, 2],
    [2, 1],
    [3, 4],
], dtype=float)
```

<details>
<summary><strong>정답 및 해설</strong></summary>

```python
import numpy as np

X = np.array([[1, 2], [2, 1], [3, 4]], dtype=float)
w = np.array([2.0, -1.0])
b = 1.0
predictions = X @ w + b

print(predictions)        # [1. 4. 3.]
print(predictions.shape)  # (3,)
```

첫 Sample의 예측은 `2×1 - 2 + 1 = 1`이며, 나머지는 각각 `4`, `3`입니다. `X`의 Shape는 `(3, 2)`, `w`는 `(2,)`이므로 `X @ w`는 각 Sample에 대한 예측값 3개를 반환합니다.

</details>

### Q-19. Scaling과 평가 데이터의 분리

**관련 개념:** [Chapter 02](../Chapter-02/README.md) · Feature Scaling · Data Leakage

다음 코드는 데이터를 나누기 전에 전체 Feature에서 Scaling 기준을 계산합니다. 문제가 되는 이유를 설명하고, Training Data에서만 Scaling 기준을 학습하도록 수정하시오.

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X_scaled = StandardScaler().fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)
```

<details>
<summary><strong>정답 및 해설</strong></summary>

`fit_transform(X)`는 전체 Sample의 평균과 표준편차를 이용합니다. 따라서 Test Data가 Training Data에 적용할 변환 기준에 영향을 미칩니다.

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

모델 평가를 여러 번 수행하거나 Cross-Validation을 사용하는 경우에는 `Pipeline` 안에 `StandardScaler`를 넣어 Fold별 Training Data에서만 `fit()`이 수행되도록 하는 편이 안전합니다.

</details>

### Q-20. Cluster 결과를 업무에 해석하기

**관련 개념:** [Chapter 03](../Chapter-03/README.md) · Clustering · Cluster Profile · KMeans

공간 이용 기록을 KMeans로 분류한 뒤 다음 결과를 얻었습니다.

| Cluster ID | 평균 방문 횟수(주당) | 평균 체류 시간(분) | Sample 수 |
|---|---:|---:|---:|
| 0 | 2 | 160 | 45 |
| 1 | 8 | 35 | 70 |

Cluster ID가 각각 무엇을 의미한다고 단정할 수 없는 이유를 설명하고, 운영팀이 참고할 수 있는 해석 두 가지와 추가 확인할 사항 한 가지를 작성하시오.

<details>
<summary><strong>정답 및 해설</strong></summary>

Cluster ID는 알고리즘이 부여한 번호이며, `0`이 일반 이용자이고 `1`이 우수 이용자라는 의미가 자동으로 정해지지 않습니다.

Cluster 0은 방문 빈도가 낮지만 한 번 방문할 때 오래 머무르는 집단, Cluster 1은 자주 방문하지만 짧게 이용하는 집단으로 해석할 수 있습니다. 운영팀에서는 장시간 사용 좌석과 짧은 회전 이용 공간을 구분하는 데 참고할 수 있습니다.

다만 이 결과는 집단별 평균만 보여줍니다. 각 Cluster 내부의 분포, Feature Scaling 여부, 서로 다른 초기화에서 Cluster가 유지되는지 등을 확인해야 합니다. Cluster를 사람에 대한 확정적 성격이나 자격 등급으로 해석해서는 안 됩니다.

</details>

### Q-21. Threshold와 예측 결과

**관련 개념:** [Chapter 03](../Chapter-03/README.md) · Logistic Regression · Decision Threshold

클래스 1의 예측 점수가 `[0.20, 0.45, 0.60, 0.85]`입니다. Threshold가 `0.50`일 때와 `0.40`일 때의 예측 Label을 각각 작성하고, Threshold를 낮췄을 때 일반적으로 어떤 변화가 나타날 수 있는지 설명하시오. NumPy 코드로 작성해도 됩니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

Threshold가 `0.50`일 때는 `[0, 0, 1, 1]`, `0.40`일 때는 `[0, 1, 1, 1]`입니다.

```python
import numpy as np

scores = np.array([0.20, 0.45, 0.60, 0.85])
print((scores >= 0.50).astype(int))  # [0 0 1 1]
print((scores >= 0.40).astype(int))  # [0 1 1 1]
```

Threshold를 낮추면 양성으로 분류하는 Sample이 늘어납니다. 실제 Label에 따라 Recall이 증가하거나 유지될 수 있고, False Positive가 늘어 Precision이 낮아질 수도 있습니다. 점수만으로 실제 Precision과 Recall을 계산할 수는 없습니다.

</details>

### Q-22. Precision이 정의되지 않는 상황

**관련 개념:** [Chapter 04](../Chapter-04/README.md) · Precision · Recall · Confusion Matrix

평가 데이터에 실제 양성이 5건 포함되어 있지만, 모델은 모든 Sample을 음성으로 예측했습니다. 이 경우 양성 클래스의 Precision과 Recall을 각각 어떻게 해석해야 하는지 설명하시오. `zero_division=0` 옵션의 의미도 함께 작성하시오.

<details>
<summary><strong>정답 및 해설</strong></summary>

모델이 양성으로 예측한 Sample이 없으므로 `TP + FP = 0`이고, Precision의 분모는 0입니다. 수학적으로 Precision은 정의되지 않습니다. 실제 양성 5건을 모두 놓쳤으므로 Recall은 `0/5 = 0`입니다.

scikit-learn에서 `zero_division=0`을 지정하면 계산상 정의되지 않는 값을 보고 편의상 0으로 처리합니다. 이는 **측정된 Precision이 실제로 0이었다는 뜻과는 다릅니다.** 모델을 평가할 때 예측 양성 건수와 실제 양성 건수도 함께 확인해야 합니다.

</details>

### Q-23. 장비 예측 모델의 평가 설계

**관련 개념:** [Chapter 04](../Chapter-04/README.md) · Group-Aware Evaluation · Temporal Split · Generalization

장비 200대의 주간 센서 기록으로 고장 위험을 예측합니다. 다음 두 목표에 알맞은 데이터 분할 기준을 각각 제시하고, 이유를 설명하시오.

- 목표 A: 과거 기록이 있는 장비의 **다음 달** 고장 위험을 예측합니다.
- 목표 B: 학습에 한 번도 사용하지 않은 **새 장비** 의 고장 위험을 예측합니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

목표 A에서는 시간 순서를 유지해 과거 기간으로 학습하고 이후 기간에서 평가하는 Temporal Split이 우선입니다. 다음 달에 알 수 없는 정보를 전처리나 Feature 생성에 사용하지 않아야 합니다.

목표 B에서는 장비 ID를 Group으로 정의하고 같은 장비의 기록이 Train과 평가 데이터에 함께 들어가지 않도록 Group 분할을 적용합니다. 두 목표가 동시에 중요하다면 장비와 시간 조건을 모두 만족하도록 평가를 별도로 설계해야 합니다.

데이터를 무작위로 나누는 것 자체가 잘못은 아니지만, **실제 사용 환경과 평가 대상이 서로 다르면 높은 평가 점수도 운영 성능을 설명하지 못합니다.**

</details>

### Q-24. Cross-Validation의 Leakage 수정

**관련 개념:** [Chapter 04](../Chapter-04/README.md) · Pipeline · Cross-Validation · Hyperparameter Tuning

다음 코드는 Cross-Validation을 수행하기 전에 전체 Training Data로 Scaling 기준을 계산합니다. 문제를 설명하고, `Pipeline`을 사용해 수정하시오. `X_train`, `y_train`은 독립적인 Test Data를 따로 확보한 뒤 남은 Training Data라고 가정합니다.

```python
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)

search = GridSearchCV(
    KNeighborsClassifier(),
    {"n_neighbors": [3, 5, 7]},
    cv=5,
)
search.fit(X_scaled, y_train)
```

<details>
<summary><strong>정답 및 해설</strong></summary>

`X_train` 안에서 5-Fold Cross-Validation을 실행하더라도, Scaling 기준은 이미 **전체 X_train** 에서 계산되었습니다. 각 Fold의 Validation Sample이 변환 기준에 영향을 주므로 Fold별 평가가 완전히 분리되지 않습니다.

```python
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", KNeighborsClassifier()),
])

search = GridSearchCV(
    pipeline,
    {"model__n_neighbors": [3, 5, 7]},
    cv=5,
)
search.fit(X_train, y_train)

print(search.best_params_)
```

`Pipeline`을 사용하면 각 Fold의 Training Data에서 Scaling을 학습하고 Validation Data에는 `transform()`만 적용합니다. 독립적으로 보관한 Test Data는 최종 모델을 선택한 뒤 평가에 사용합니다.

</details>

---

[← Summary 목차](./README.md) · [Problems](./problem.md) · [AI 목차](../README.md)
