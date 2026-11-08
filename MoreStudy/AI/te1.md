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

단일 샘플에 대해 모델을 $\hat{y} = wx$로 정의합니다. 입력 $x = 2$, 실제값 $y = 5$, 현재 가중치 $w = 1$이고 손실 함수(Loss)가 $L = (wx-y)^2$일 때, 학습률(Learning Rate)이 $0.1$이라면 경사 하강법(Gradient Descent)을 **한 번 적용한 이후의 가중치** $w$는 얼마입니까?

1. `-0.2`
2. `1.2`
3. `2.2`
4. `3.0`

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ③**

**1. 기울기(Gradient) 계산**

손실 함수 $L$을 가중치 $w$에 대해 미분하면 다음과 같습니다.

$\frac{\partial L}{\partial w} = 2(wx-y)\cdot x$

주어진 값($x=2$, $y=5$, $w=1$)을 대입하면,

$\frac{\partial L}{\partial w} = 2(1\times2-5)\times2 = -12$

**2. 가중치 업데이트**

학습률 $\eta=0.1$을 적용한 경사 하강법의 가중치 갱신 공식은 다음과 같습니다.

$w_{\text{new}} = w-\eta\frac{\partial L}{\partial w}$

계산한 기울기를 대입하면,

$w_{\text{new}} = 1-0.1\times(-12) = 2.2$

따라서 한 번의 경사 하강법 적용 후 가중치는 **2.2**입니다.

**오답 해설**

- **① `-0.2`:** 기울기의 부호를 반대로 적용한 경우입니다.
- **② `1.2`:** 가중치의 변화량과 갱신된 가중치를 혼동한 경우입니다.
- **④ `3.0`:** 기울기와 학습률을 올바르게 적용하지 않은 결과입니다.

</details>

### Q-06. Feature Scaling이 중요한 이유

**관련 개념:** [Chapter 02](../Chapter-02/README.md) · Feature Scaling · KNN

어떤 KNN 모델은 `age`(20 ~ 70)와 `annual_income`(20,000,000 ~ 100,000,000)을 Feature로 사용합니다. 원본 값으로 유클리드 거리를 계산할 때 발생할 수 있는 문제는 무엇입니까?

1. 범위가 큰 `annual_income`이 거리 계산을 지배할 수 있습니다.
2. KNN은 숫자형 Feature를 처리할 수 없습니다.
3. Scaling을 하면 Test Data의 Label이 자동으로 바뀝니다.
4. KNN은 Feature 간 거리를 계산하지 않으므로 Scaling과 관계가 없습니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ①**

**1. 거리 기반 모델과 스케일의 영향**

KNN(K-Nearest Neighbors)은 데이터 간의 거리(예: 유클리드 거리)를 기반으로 이웃을 탐색하는 알고리즘입니다. 이 과정에서 각 특성(Feature)의 값 범위가 다를 경우, 단위의 크기가 절대적으로 큰 변수(예: 연봉)가 거리 계산 결과를 지배하게 되어 상대적으로 범위가 작은 변수(예: 나이)의 영향력이 무시되는 문제가 발생합니다.

**2. 올바른 전처리 방법**

따라서 이러한 문제를 방지하기 위해 훈련 데이터(Training Data)를 기준으로 스케일링(Scaling)을 수행한 뒤, 검증 및 테스트 데이터(Validation·Test Data)에도 동일한 기준을 적용해야 합니다.

**오답 해설**

- **② `KNN은 숫자형 Feature를 처리할 수 없습니다.`:** KNN은 대표적인 거리 기반 알고리즘으로, 기본적으로 수치형 데이터를 입력으로 받아 거리를 계산합니다.
- **③ `Scaling을 하면 Test Data의 Label이 자동으로 바뀝니다.`:** Feature Scaling은 입력 특성(Feature)의 값 범위를 조정하는 변환일 뿐, 정답 레이블(Target Label)과는 무관합니다.
- **④ `KNN은 Feature 간 거리를 계산하지 않으므로 Scaling과 관계가 없습니다.`:** KNN은 샘플 간의 거리를 직접 계산하여 이웃을 선정하므로, 특성의 스케일에 매우 민감합니다.

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

**1. 임계값(Threshold) 비교 조건 확인**

주어진 조건은 `score >= threshold`이며, `threshold = 0.65`입니다. 예측 점수 배열 `[0.40, 0.65, 0.80]`의 각 원소에 조건을 대입하여 판단합니다.

- 첫 번째 값 (`0.40`): $0.40 \ge 0.65$는 **False**이므로 `0`
- 두 번째 값 (`0.65`): $0.65 \ge 0.65$는 **True**이므로 `1` (`>=` 연산이므로 같거나 클 때 포함됨)
- 세 번째 값 (`0.80`): $0.80 \ge 0.65$는 **True**이므로 `1`

**2. 최종 예측 결과**

따라서 계산된 예측 레이블 결과는 순서대로 `[0, 1, 1]`이 됩니다.

**오답 해설**

- **① `[0, 0, 1]`:** 경계값인 `0.65`를 초과(`>`) 조건으로 잘못 오인하여 두 번째 값을 `0`으로 처리한 경우입니다.
- **③ `[1, 1, 1]`:** 첫 번째 값인 `0.40`은 임계값 `0.65`보다 작으므로 레이블 `1`이 될 수 없습니다.
- **④ `[0, 1, 0]`:** 세 번째 값인 `0.80`은 임계값 이상이므로 레이블 `1`이 되어야 하는데 이를 잘못 제외한 경우입니다.

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

**1. 군집 중심(Centroid) 계산 원리**

KMeans 알고리즘에서 클러스터의 새로운 중심 좌표는 해당 클러스터에 속한 모든 샘플들의 각 특성(Feature)별 **산술 평균(Mean)**으로 계산됩니다.

**2. 좌표별 평균 계산**

- **첫 번째 좌표 ($x$축):** 
  $$\frac{0 + 2 + 4}{3} = \frac{6}{3} = 2$$

- **두 번째 좌표 ($y$축):** 
  $$\frac{0 + 4 + 2}{3} = \frac{6}{3} = 2$$

따라서 갱신된 새로운 클러스터의 중심 좌표는 **`(2, 2)`**가 됩니다.

**오답 해설**

- **①이 아닌 이유들:**
  - **② `(6, 6)`:** 각 좌표의 평균을 구하지 않고 단순히 총합을 구한 경우입니다.
  - **③ `(0, 0)`:** 첫 번째 샘플의 좌표를 중심으로 잘못 고정한 경우입니다.
  - **④ `(2, 3)`:** 두 번째 좌표($y$축)의 평균 계산을 잘못 수행한 결과입니다.

</details>

### Q-09. KMeans와 DBSCAN의 선택

**관련 개념:** [Chapter 03](../Chapter-03/README.md) · KMeans · DBSCAN · Noise

좌표 데이터에 길게 휘어진 두 개의 밀집 영역과 몇 개의 고립된 점이 있습니다. 다음 설명 중 **가장 적절한 것**은 무엇입니까?

1. KMeans는 어떤 형태의 Cluster든 항상 정확하게 구분합니다.
2. DBSCAN은 밀도에 따라 연결된 영역을 찾고 일부 점을 Noise로 구분할 수 있으므로 비교할 가치가 있습니다.
3. DBSCAN은 Cluster 수 `k`를 반드시 입력해야 합니다.
4. Clustering은 정답 Label이 없으면 실행할 수 없습니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ②**

**1. 알고리즘별 특징과 데이터 형태**

KMeans는 기본적으로 구형(Spherical) 혹은 볼록한 형태의 클러스터를 찾는 데 최적화되어 있어, 길게 휘어진 비선형 형태의 밀집 영역을 분리하는 데는 한계가 있습니다. 반면, DBSCAN은 데이터의 **밀도(Density)**를 기반으로 연결된 영역을 탐색하므로 복잡한 형태의 군집을 잘 찾아내며, 밀도가 낮은 고립된 점들은 **노이즈(Noise)**로 판별할 수 있습니다.

**2. 비지도 학습(Unsupervised Learning)의 특성**

군집화(Clustering)는 정답 레이블(Label)이 필요 없는 대표적인 비지도 학습 알고리즘입니다.

**오답 해설**

- **① `KMeans는 어떤 형태의 Cluster든 항상 정확하게 구분합니다.`:** KMeans는 거리 기반 중심점을 사용하므로 비선형적이고 복잡한 형태의 클러스터 분리에 취약합니다.
- **③ `DBSCAN은 Cluster 수 k를 반드시 입력해야 합니다.`:** 클러스터의 개수 `k`를 입력하는 것은 KMeans의 특징이며, DBSCAN은 밀도 기준을 정하는 `eps`와 `min_samples` 등의 파라미터를 사용합니다.
- **④ `Clustering은 정답 Label이 없으면 실행할 수 없습니다.`:** 군집화는 정답 레이블이 없는 데이터에서 데이터 간의 유사성을 바탕으로 스스로 그룹을 나누는 비지도 학습입니다.

</details>

### Q-10. Cluster 번호와 실제 Label

**관련 개념:** [Chapter 03](../Chapter-03/README.md) · Unsupervised Learning · Cluster Interpretation

KMeans 결과가 `[0, 0, 1, 1]`, 실제 정답 Label이 `[1, 1, 0, 0]`으로 나왔습니다. 이에 대한 설명 중 **가장 옳은 것**은 무엇입니까?

1. Cluster ID와 Label이 모두 반대이므로 군집화는 완전히 실패했습니다.
2. Cluster ID를 Target Label로 사용해 `accuracy_score()`를 계산하면 언제나 적절합니다.
3. Cluster ID는 임의의 식별 번호이므로 번호가 다르다는 이유만으로 군집 구조가 틀렸다고 판단할 수 없습니다.
4. KMeans는 학습할 때 정답 Label을 사용하므로 이러한 결과가 나올 수 없습니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ③**

**1. 군집 번호(Cluster ID)의 특성**

비지도 학습인 군집화(Clustering)에서 부여하는 Cluster ID는 알고리즘이 임의로 붙인 식별 번호에 불과합니다. 따라서 실제 정답 레이블의 값과 번호가 직접 일치하지 않더라도, 데이터가 나누어진 그룹의 분할 구조 자체(예: 1, 2번 샘플이 한 그룹, 3, 4번 샘플이 다른 그룹으로 묶인 형태)가 정확하다면 성공적인 군집화로 볼 수 있습니다.

**2. 평가 지표의 선택**

이와 같은 이유로 단순히 Cluster ID를 정답 레이블과 직접 비교해 정확도(Accuracy)를 계산하면 잘못된 해석을 낳을 수 있으며, 번호의 치환에 영향을 받지 않는 ARI(Adjusted Rand Index) 등의 평가 지표를 고려해야 합니다.

**오답 해설**

- **① `Cluster ID와 Label이 모두 반대이므로 군집화는 완전히 실패했습니다.`:** 번호 자체만 다를 뿐 데이터가 갈라진 그룹의 구조는 일치하므로 실패로 볼 수 없습니다.
- **② `Cluster ID를 Target Label로 사용해 accuracy_score()를 계산하면 언제나 적절합니다.`:** ID의 매칭 여부에 따라 정확도가 왜곡될 수 있으므로 직접 비교는 적절하지 않습니다.
- **④ `KMeans는 학습할 때 정답 Label을 사용하므로 이러한 결과가 나올 수 없습니다.`:** KMeans는 정답을 사용하지 않는 비지도 학습 알고리즘입니다.

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

**1. 정확도(Accuracy) 계산**

전체 데이터 100건 중 실제 정상 사례인 95건을 모두 정상(0)으로 맞혔으므로, 정확도는 다음과 같습니다.
$$\text{Accuracy} = \frac{95}{100} = 95\%$$

**2. 재현율(Recall) 계산**

이상 클래스(1)에 대한 재현율은 실제 이상 사례 5건 중에서 모델이 올바르게 찾아낸(True Positive) 건수의 비율입니다. 모델이 모든 사례를 정상(0)으로 예측했으므로 찾아낸 이상 사례는 0건입니다.
$$\text{Recall} = \frac{0}{5} = 0\%$$

**오답 해설**

- **② `Accuracy 95%, Recall 95%`:** 모델이 실제 이상 사례를 전혀 찾아내지 못했음에도 재현율을 높게 잘못 산정한 경우입니다.
- **③ `Accuracy 5%, Recall 0%`:** 다수 클래스의 개수(95건)를 전체 정답 수로 고려하지 않고 정확도를 잘못 계산했습니다.
- **④ `Accuracy 100%, Recall 5%`:** 모든 사례를 올바르게 맞히지 못했으므로 정확도가 100%가 될 수 없습니다.

</details>

### Q-12. Precision·Recall·F1 계산

**관련 개념:** [Chapter 04](../Chapter-04/README.md) · Confusion Matrix · F1 Score

이진 분류 모델의 결과가 `TP = 8`, `FP = 2`, `FN = 6`, `TN = 24`입니다. Precision과 Recall에 대한 설명 중 **가장 올바른 것**은 무엇입니까?

1. Precision은 `8/14`, Recall은 `8/10`입니다.
2. Precision은 `8/10`, Recall은 `8/14`입니다.
3. Precision은 `24/26`, Recall은 `8/40`입니다.
4. Precision과 Recall은 모두 `8/40`입니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ②**

**1. 정밀도(Precision) 계산**

정밀도는 모델이 양성(Positive)이라고 예측한 전체 샘플 중 실제 양성인 비율입니다.
$$\text{Precision} = \frac{TP}{TP + FP} = \frac{8}{8 + 2} = \frac{8}{10} = 0.8$$

**2. 재현율(Recall) 계산**

재현율은 실제 양성인 전체 샘플 중 모델이 양성으로 올바르게 예측한 비율입니다.
$$\text{Recall} = \frac{TP}{TP + FN} = \frac{8}{8 + 6} = \frac{8}{14} \approx 0.5714$$

(참고: $F_1 \text{ Score} = \frac{2 \times TP}{2 \times TP + FP + FN} = \frac{16}{24} \approx 0.6667$)

**오답 해설**

- **① `Precision은 8/14, Recall은 8/10입니다.`:** 정밀도와 재현율의 분모·분자(분할표의 합산 기준)가 서로 뒤바뀐 경우입니다.
- **③ `Precision은 24/26, Recall은 8/40입니다.`:** 혼동 행렬의 음성 예측 관련 값(TN 등)을 잘못 조합하거나 전체 샘플 수를 잘못 사용한 경우입니다.
- **④ `Precision과 Recall은 모두 8/40입니다.`:** 전체 데이터 수(40건)를 분모로 잘못 사용한 경우입니다.

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

**1. MAE (Mean Absolute Error) 계산**

잔차(Residual)의 절댓값 평균을 구합니다.
$$\text{MAE} = \frac{|1| + |-3|}{2} = \frac{1 + 3}{2} = \frac{4}{2} = 2$$

**2. MSE (Mean Squared Error) 계산**

잔차의 제곱 평균을 구합니다.
$$\text{MSE} = \frac{1^2 + (-3)^2}{2} = \frac{1 + 9}{2} = \frac{10}{2} = 5$$

(참고: RMSE는 $\sqrt{5} \approx 2.236$입니다.)

**오답 해설**

- **② `MAE -1, MSE -4`:** 부호가 있는 잔차를 절댓값 처리나 제곱 처리 없이 그대로 평균을 낸 경우입니다.
- **③ `MAE 4, MSE 10`:** 오차의 합계를 구한 뒤 샘플 수(2)로 나누지 않고 그대로 산출한 경우입니다.
- **④ `MAE 5, MSE 2`:** MAE와 MSE의 계산 방식을 서로 혼동하여 적용한 경우입니다.

</details>

### Q-14. Hyperparameter 선택과 Test Data

**관련 개념:** [Chapter 04](../Chapter-04/README.md) · Validation · Test Data · Hyperparameter Tuning

여러 모델 중 하나를 선택해야 합니다. 다음 절차 중 **최종 Test 평가의 독립성을 가장 잘 유지하는 방법**은 무엇입니까?

1. Test 점수를 확인하면서 Hyperparameter를 반복 변경하고 가장 높은 점수를 보고합니다.
2. 전체 데이터를 한 번에 학습한 뒤 그 데이터에서 정확도를 측정합니다.
3. Training Data에서 모델을 학습하고 Validation 또는 Cross-Validation으로 설정을 선택한 다음, 확정된 모델을 Test Data에서 평가합니다.
4. Test Data를 모델 선택에 사용했다면 그 데이터를 다시 Validation이라고 부르면 문제가 없습니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ③**

**1. 모델 평가와 선택의 분리**

하이퍼파라미터 튜닝이나 모델 선택 과정에서는 훈련 데이터(Training Data)와 검증 데이터(Validation Data)만을 활용해야 합니다. 최종 테스트 데이터(Test Data)는 모델의 최적화 과정에 일체 관여하지 않은 상태로 남겨두어야, 실제 운영 환경에서의 일반화 성능을 객관적이고 독립적으로 평가할 수 있습니다.

**2. 올바른 머신러닝 파이프라인**

따라서 교차 검증(Cross-Validation)이나 별도의 검증 셋을 통해 최적의 설정을 확정한 후, 마지막에 단 한 번 Test Data로 평가를 수행하는 방식이 데이터 누수(Data Leakage)를 방지하는 올바른 절차입니다.

**오답 해설**

- **①:** Test 점수를 확인하며 반복적으로 파라미터를 수정하면 모델이 Test Data에 과적합(Overfitting)되어, 더 이상 독립적인 평가 지표로 기능할 수 없습니다.
- **②:** 모델을 학습시킨 동일한 데이터로 성능을 측정하면 낙관적인 결과만 나오며 실제 미지의 데이터에 대한 일반화 성능을 알 수 없습니다.
- **④:** 데이터의 명칭을 바꾼다고 하여 이미 모델 선택 과정에서 테스트 데이터의 정보가 반영된(Data Leakage) 문제가 해결되지는 않습니다.

</details>

### Q-15. 반복 측정 데이터의 분할

**관련 개념:** [Chapter 04](../Chapter-04/README.md) · GroupKFold · Group-Aware Evaluation

동일한 산업용 장비에서 일주일 간격으로 여러 번 측정한 데이터가 있습니다. 목표는 **학습에 포함되지 않은 새로운 장비**의 상태를 예측하는 것입니다. 어떤 평가 방식이 가장 적절합니까?

1. 각 행을 완전히 무작위로 나눈 K-Fold
2. 동일 장비의 기록이 Train과 Validation에 동시에 포함되지 않도록 장비 ID를 기준으로 나누는 Group 분할
3. 전체 데이터의 각 Feature 평균으로 Target을 채우는 방법
4. 정확도가 가장 높게 나오는 분할을 반복해서 선택하는 방법

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ②**

**1. 그룹 기반 분할(Group-Aware Splitting)의 필요성**

동일한 장비에서 시간 간격을 두고 수집된 데이터들은 서로 높은 상관관계를 가집니다. 이를 일반적인 무작위 K-Fold 방식으로 나누면 동일 장비의 기록이 훈련 데이터(Train)와 검증 데이터(Validation) 양쪽에 동시에 섞이게 되어 **데이터 누수(Data Leakage)**가 발생합니다. 즉, 모델이 '새로운 장비'의 고장 여부를 맞히는 것이 아니라 '이미 학습한 장비의 특성'을 단순히 기억해 높은 성능을 내는 것처럼 착시를 일으키게 됩니다.

**2. 올바른 평가 방식**

따라서 학습에 한 번도 참여하지 않은 새로운 장비에 대한 실제 운영 환경에서의 일반화 성능을 정확히 평가하려면, 장비 ID(`Group`)를 기준으로 그룹이 통째로 분할되도록 설계(`GroupKFold` 등)해야 합니다.

**오답 해설**

- **① `각 행을 완전히 무작위로 나눈 K-Fold`:** 동일 장비의 데이터가 양쪽 세트에 유출되어 성능이 과대평가되는 심각한 문제가 발생합니다.
- **③ `전체 데이터의 각 Feature 평균으로 Target을 채우는 방법`:** 이는 결측치 처리나 특성 엔지니어링의 일종일 뿐, 교차 검증이나 데이터 분할 방법이 아닙니다.
- **④ `정확도가 가장 높게 나오는 분할을 반복해서 선택하는 방법`:** 원하는 결과가 나올 때까지 분할을 편파적으로 선택하면 평가 지표가 왜곡되고 신뢰성을 잃게 됩니다.

</details>

### Q-16. 시간 순서가 있는 데이터의 평가

**관련 개념:** [Chapter 04](../Chapter-04/README.md) · Temporal Split · Generalization

지난달까지의 시설 방문 기록을 사용해 다음 달 방문객 수를 예측하려고 합니다. 다음 중 **가장 타당한 평가 방식**은 무엇입니까?

1. 미래 날짜의 기록을 Train에 포함하고 과거 날짜를 Test로 사용합니다.
2. 모든 행을 무작위로 섞으면 시간 순서는 고려할 필요가 없습니다.
3. 더 최신인 데이터의 통계를 사용해 과거 Training Data의 결측값을 채운 뒤 평가합니다.
4. 과거 기간으로 학습하고 그 이후 기간을 Validation과 Test로 나누어 평가합니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**정답: ④**

**1. 시계열 데이터(Temporal Data) 분할의 원칙**

시간의 흐름에 따른 트렌드나 패턴을 예측하는 시계열 및 순차적 데이터 분석에서는, 미래의 데이터가 과거를 예측하는 데 쓰이는 **시간 누수(Time Leakage)**를 방지해야 합니다. 실제 운영 환경을 반영하기 위해 과거 기간의 데이터로 모델을 학습(Train)하고, 그 이후의 미래 기간 데이터를 검증(Validation) 및 테스트(Test)용으로 분할하여 평가해야 합니다.

**2. 일반화 성능 검증**

과거의 패턴으로 미래를 맞히는 실제 서비스 구조와 동일한 방식으로 평가 파이프라인을 구축해야 모델의 실전 성능을 왜곡 없이 측정할 수 있습니다.

**오답 해설**

- **① `미래 날짜의 기록을 Train에 포함하고 과거 날짜를 Test로 사용합니다.`:** 실제 서비스 환경에서는 미래의 데이터를 미리 알고 과거를 예측할 수 없으므로, 현실성이 없으며 치명적인 데이터 누수가 발생합니다.
- **② `모든 행을 무작위로 섞으면 시간 순서는 고려할 필요가 없습니다.`:** 시계열 데이터를 무작위로 섞으면(Shuffle) 시간적 선후 관계가 파괴되어 모델이 과거의 데이터로 미래를 예측하는 법을 올바르게 학습할 수 없습니다.
- **③ `더 최신인 데이터의 통계를 사용해 과거 Training Data의 결측값을 채운 뒤 평가합니다.`:** 미래의 정보(최신 데이터 통계)가 과거 모델 학습에 유입되는 구조이므로 이 역시 심각한 데이터 누수(Data Leakage)를 유발합니다.

</details>

## 주관식

### Q-17. 자동화와 AI의 차이

**관련 개념:** [Chapter 01](../Chapter-01/README.md) · Rule-Based Systems · AI Tasks · Human Review

다음 두 업무를 확인하고, 각각 Rule-Based Systems와 Machine Learning 중 어느 접근이 먼저 적절한지 설명하시오.

- **업무 A:** 온라인 신청서에서 생년월일이 비어 있으면 `REQUIRED_FIELD` 오류를 반환합니다.
- **업무 B:** 과거 상담 기록을 이용해 새로운 상담 문의의 담당 부서를 분류합니다. 문의 문장은 매번 달라지며 과거 분류 Label이 준비되어 있습니다.

두 번째 업무에 학습 모델을 사용하더라도 사람의 검토가 필요한 상황을 한 가지 제시하시오.

<details>
<summary><strong>정답 및 해설</strong></summary>

**모범 답안**

**1. 업무별 적절한 접근 방식**
- **업무 A (Rule-Based Systems):** 생년월일의 입력 유무라는 명확하고 고정된 조건(If-Else)으로 판단할 수 있으므로, 복잡한 머신러닝 모델 대신 규칙 기반 시스템을 적용하는 것이 가장 단순하고 정확합니다.
- **업무 B (Supervised Learning):** 고객이 작성하는 상담 문장은 표현이 다양하고 비정형적이어서 명확한 규칙을 코드로 일일이 정의하기 어렵습니다. 하지만 정답 레이블(Label)이 포함된 과거 데이터가 존재하므로 지도학습 기반의 분류 모델을 적용하는 것이 적절합니다.

**2. 사람의 검토(Human-in-the-Loop)가 필요한 상황**
- 모델의 예측 확신도가 현저히 낮거나(예: 임계값 미달), 오분류로 인해 고객 응대가 크게 지연되거나 중요한 비즈니스 손실이 발생할 수 있는 고위험 문의의 경우, 모델이 단독으로 처리하기보다 **담당 직원의 최종 검토 및 확인**을 거치도록 설계해야 합니다.

**핵심 판단 기준 요약**
모든 업무에 AI를 무조건 도입하는 것이 능사는 아니며, **(1) 문제의 규칙을 명확히 코드로 작성할 수 있는지**, **(2) 적절한 학습 데이터가 확보되어 있는지**, **(3) 오류가 발생했을 때의 리스크(영향도)가 어느 정도인지**를 종합적으로 고려하여 접근 방식을 선택해야 합니다.

</details>

### Q-18. Linear Regression의 예측 계산

**관련 개념:** [Chapter 02](../Chapter-02/README.md) · Feature · Linear Regression · Matrix Operation

다음 세 Sample에 대해 $\hat{y} = 2x_1 - x_2 + 1$을 계산하는 NumPy 코드를 작성하시오. 예측값 배열의 Shape와 값을 함께 제시하시오.

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

1. 샘플별 예측값 계산 과정

주어진 예측 모델 식 $\hat{y} = 2x_1 - x_2 + 1$ (가중치 $w_1 = 2$, $w_2 = -1$, 절편 $b = 1$)을 각 샘플의 특성 값에 대입하여 계산합니다.

- **첫 번째 샘플 `[1, 2]`:** 
  $$\hat{y}_1 = (2 \times 1) - (1 \times 2) + 1 = 2 - 2 + 1 = 1$$
- **두 번째 샘플 `[2, 1]`:** 
  $$\hat{y}_2 = (2 \times 2) - (1 \times 1) + 1 = 4 - 1 + 1 = 4$$
- **세 번째 샘플 `[3, 4]`:** 
  $$\hat{y}_3 = (2 \times 3) - (1 \times 4) + 1 = 6 - 4 + 1 = 3$$

2. 배열의 형태(Shape) 분석

입력 데이터 `X`의 형태는 `(3, 2)`, 가중치 벡터 `w`의 형태는 `(2,)`입니다. 따라서 행렬곱 연산 `X @ w`는 크기가 `(3,)`인 1차원 배열을 반환하며, 여기에 스칼라 절편 `b`를 더한 최종 예측값 `predictions`의 **Shape 역시 `(3,)`이 됩니다.**

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

1. 문제가 되는 이유 (데이터 누수, Data Leakage)

분할하기 전 전체 데이터에 `fit_transform(X)`를 수행하면, 테스트 데이터(Test Data)의 정보(평균 및 표준편차)가 스케일러의 계산에 포함됩니다. 이는 실제 운영 환경에서는 알 수 없는 미래 혹은 평가용 데이터의 통계적 특성이 훈련 데이터로 유출되는 **데이터 누수(Data Leakage)**를 발생시키며, 이로 인해 모델의 성능이 과대평가(낙관적 측정)될 위험이 있습니다.

2. 올바른 수정 방법

데이터를 먼저 훈련 세트와 테스트 세트로 분리(`train_test_split`)한 뒤, **훈련 데이터(Training Data)**만을 기준으로 스케일러를 학습(`fit_transform`)해야 합니다. 테스트 데이터(Test Data)에는 훈련 세트에서 학습된 기준만을 바탕으로 변환(`transform`)만 수행해야 합니다.

(참고: 교차 검증을 반복하는 환경에서는 데이터 누수를 근본적으로 차단하기 위해 `sklearn.pipeline.Pipeline`을 사용하여 각 폴드별 훈련 데이터에서만 스케일러가 학습되도록 구성하는 것이 가장 안전합니다.)

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

1. Cluster ID를 단정할 수 없는 이유

KMeans가 부여하는 `0`, `1` 등의 Cluster ID는 각 군집을 구분하기 위한 식별 번호입니다. 번호 자체에는 우열이나 고정된 의미가 없으므로, 각 군집에 속한 데이터의 특성을 분석하여 해석해야 합니다.

2. 운영팀이 참고할 수 있는 해석 두 가지

- **Cluster 0 — 저빈도·장시간 이용 그룹 (45명):** 주당 평균 방문 횟수는 2회로 적지만, 평균 체류 시간은 160분으로 긴 편입니다. 장시간 이용자를 위한 좌석이나 편의 시설을 운영하는 데 참고할 수 있습니다.
- **Cluster 1 — 고빈도·단시간 이용 그룹 (70명):** 주당 평균 8회 방문하며, 평균 체류 시간은 35분입니다. 짧은 시간 동안 반복적으로 이용하는 집단으로 볼 수 있으며, 빠른 이용과 회전율을 고려한 공간 운영에 참고할 수 있습니다.

3. 추가로 확인할 사항

- **Feature Scaling 적용 여부:** 방문 횟수와 체류 시간은 단위와 값의 범위가 다릅니다. KMeans는 거리 기반 알고리즘이므로, 값의 범위가 큰 특성이 군집 형성에 더 큰 영향을 줄 수 있습니다. 따라서 `StandardScaler` 등을 이용해 적절한 Feature Scaling이 적용되었는지 확인할 필요가 있습니다.
  
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

**Threshold를 낮췄을 때의 일반적인 변화**

결정 임계값(Threshold)을 낮추면 모델이 양성(Positive)으로 판단하는 기준이 관대해지므로, 양성으로 예측되는 샘플 수가 늘어나게 됩니다.

- 이로 인해 실제 양성인 샘플을 놓치지 않고 더 많이 잡아내게 되어 **재현율(Recall)**은 증가하거나 유지될 수 있습니다.
- 반면, 음성 샘플을 양성으로 잘못 예측하는 경우(False Positive)가 늘어나기 때문에 **정밀도(Precision)**는 낮아질 위험이 있습니다. (단, 제공된 점수 데이터만으로는 실제 레이블 값을 알 수 없으므로 실제 Precision과 Recall의 정확한 수치를 직접 확정할 수는 없습니다.)
- 
</details>

### Q-22. Precision이 정의되지 않는 상황

**관련 개념:** [Chapter 04](../Chapter-04/README.md) · Precision · Recall · Confusion Matrix

평가 데이터에 실제 양성(Positive)이 5건 포함되어 있지만, 모델은 모든 Sample을 음성(Negative)으로 예측했습니다. 이 경우 양성 클래스의 Precision과 Recall을 각각 어떻게 해석해야 하는지 설명하시오. 또한, Scikit-learn 등에서 사용되는 `zero_division=0` 옵션의 의미도 함께 작성하시오.

<details>
<summary><strong>정답 및 해설</strong></summary>

**1. Precision과 Recall 해석**

모델이 모든 Sample을 음성(Negative)으로 예측했으므로, 양성 클래스에 대한 `TP = 0`, `FP = 0`, `FN = 5`입니다.

- **재현율(Recall = 0.0):** 실제 양성 5건 중 모델이 양성으로 예측한 사례가 없으므로, Recall은 $\frac{TP}{TP+FN} = \frac{0}{5} = 0.0$입니다. 이는 실제 양성 사례를 하나도 찾아내지 못했다는 의미입니다.

- **정밀도(Precision = 정의되지 않음):** 모델이 양성으로 예측한 사례가 없으므로, Precision은 $\frac{TP}{TP+FP} = \frac{0}{0}$이 됩니다. 분모가 0이므로 수학적으로 정의할 수 없습니다.

**2. `zero_division=0` 옵션의 의미**

scikit-learn에서는 Precision이나 Recall을 계산할 때 분모가 0이 되는 경우를 처리하기 위해 `zero_division` 옵션을 제공합니다.

기본값인 `zero_division="warn"`은 정의되지 않는 지표를 0으로 반환하면서 경고를 발생시킵니다. 반면 `zero_division=0`을 지정하면 해당 지표를 `0.0`으로 반환하며, 이와 관련된 경고는 발생하지 않습니다.

단, **정의되지 않는 Precision을 편의상 0으로 처리한 것과 실제 계산 결과가 0인 것은 구분해야 합니다.** 따라서 모델을 평가할 때는 지표의 값뿐 아니라 실제 양성 건수와 예측 양성 건수도 함께 확인해야 합니다.

</details>


### Q-23. 장비 고장 예측 모델의 평가 설계

**관련 개념:** [Chapter 04](../Chapter-04/README.md) · Temporal Split · Group-Aware Evaluation · Generalization

총 200대 장비의 주간 센서 누적 기록을 활용하여 장비의 고장 위험을 예측하는 모델을 개발하고자 합니다. 비즈니스 목적에 따른 올바른 검증을 위해, 다음 두 가지 시나리오에 각각 적합한 **데이터 분할 전략(Splitting Strategy)**을 제시하고 그 이유를 설명하시오.

- **시나리오 A:** **이미 운영 중인 기존 장비**의 **다음 달** 고장 위험을 예측합니다.
- **시나리오 B:** 공장에서 새로 도입되어 **학습에 한 번도 사용된 적 없는 신규 장비**의 고장 위험을 예측합니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**모범 답안**

**1. 시나리오 A: 시계열 분할 (Temporal Split)**
- **분할 전략:** 시간 순서를 엄격히 유지하여 과거 기간의 센서 기록은 훈련 세트(Train)로, 그 이후의 미래 기간(다음 달) 기록은 평가 세트(Test)로 분할해야 합니다.
- **이유:** 미래의 이벤트를 예측하는 실제 운영 환경의 타임라인을 그대로 모사해야 합니다. 만약 미래의 데이터가 훈련 세트에 무작위로 섞이거나 역방향으로 분할되면 **시간적 누수(Time Leakage)**가 발생하여 모델 성능이 심각하게 과대평가되므로, 반드시 시간 축을 기준으로 분할해야 합니다.

**2. 시나리오 B: 그룹 인식 분할 (Group-Aware Split / 예: `GroupKFold`)**
- **분할 전략:** 데이터의 행(Row) 단위가 아니라 **장비 고유 ID(Device ID)**를 그룹 기준으로 설정하여, 특정 장비의 모든 주간 기록이 훈련 세트 또는 테스트 세트 중 **어느 한쪽에만** 온전히 속하도록 분할해야 합니다.
- **이유:** 동일한 장비에서 수집된 시계열 기록들은 서로 강한 상관관계와 고유한 물리적 특성을 공유합니다. 만약 같은 장비의 데이터가 양쪽 세트에 나뉘어 들어가면 모델이 '새로운 장비'를 판별하는 것이 아니라 '이미 익숙한 특정 장비의 개별 특성'을 암기하게 되어 **데이터 누수(Data Leakage)**가 발생합니다. 따라서 한 번도 보지 못한 신규 장비에 대한 실제 **일반화 성능(Generalization)**을 정확히 측정하려면 장비 단위로 완전히 격리해야 합니다.

</details>

### Q-24. Cross-Validation 과정에서의 데이터 누수와 Pipeline 수정

**관련 개념:** [Chapter 04](../Chapter-04/README.md) · Pipeline · Cross-Validation · Hyperparameter Tuning

다음 코드는 교차 검증(`GridSearchCV`)을 수행하기 전에 전체 훈련 데이터(`X_train`)를 대상으로 미리 스케일링을 수행하고 있습니다. 이 방식이 교차 검증 환경에서 문제가 되는 이유를 설명하고, `sklearn.pipeline.Pipeline`을 활용하여 올바르게 수정된 코드를 작성하시오. (단, `X_train`, `y_train`은 이미 독립적인 테스트 데이터가 분리된 상태의 훈련 데이터라고 가정합니다.)

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

1. 문제가 되는 이유 (교차 검증에서의 데이터 누수, Data Leakage)

`GridSearchCV` 내부에서 5개의 폴드(Fold)로 나누어 교차 검증을 수행하기 전에, 전체 `X_train`에 대해 미리 `fit_transform()`을 적용했습니다. 이는 향후 검증용 폴드로 사용되어야 할 데이터의 통계치(평균 및 표준편차)가 이미 스케일링 과정에서 전체 데이터에 반영되도록 만듭니다. 즉, **교차 검증 과정에서 각 폴드의 검증 데이터 정보가 훈련 과정으로 누수(Data Leakage)**되어 최적의 하이퍼파라미터 튜닝 결과가 과대평가(낙관적 측정)되는 문제를 일으킵니다.

2. 올바른 수정 코드 (`Pipeline` 활용)

```python
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Pipeline을 이용해 전처리(StandardScaler)와 분류 모델을 순차적으로 연결
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', KNeighborsClassifier())
])

# GridSearchCV에 Pipeline 객체 전달
search = GridSearchCV(
    pipeline,
    {"classifier__n_neighbors": [3, 5, 7]},
    cv=5,
)
search.fit(X_train, y_train)
```

3. 코드 설명 및 핵심 포인트

- **데이터 누수 방지:** `Pipeline`을 사용하면 `GridSearchCV`가 각 폴드를 순회할 때, **오직 각 폴드의 훈련 세트에서만** `StandardScaler`가 `fit()`되고, 검증 세트에는 학습된 기준으로 `transform()`만 안전하게 적용됩니다.
- **파라미터 이름 지정:** Pipeline 내부 모델의 하이퍼파라미터를 튜닝할 때는 파라미터 딕셔너리의 키에 `단계이름__파라미터명` 형식(예: `"classifier__n_neighbors"`)을 사용해야 합니다.

</details>

---

[← Summary 목차](./README.md) · [Problems](./problem.md) · [AI 목차](../README.md)
