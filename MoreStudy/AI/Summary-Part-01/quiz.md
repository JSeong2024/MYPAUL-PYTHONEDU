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

의사결정 기준을 규칙으로 일일이 정하기 어렵고, 과거의 정답 레이블이 충분하다면 학습 기반 분류 모델을 검토할 만합니다. 모델이 데이터에서 분류에 필요한 패턴을 학습할 수 있기 때문입니다. 다만 실제 도입 여부는 데이터 품질과 평가 결과를 확인한 뒤 결정해야 합니다.

**오답 해설**

- **①:** 필수값이나 형식 검사는 조건이 명확하므로 규칙 기반 처리에 적합합니다. 머신러닝이 항상 더 효율적인 것은 아닙니다.
- **③:** 머신러닝 모델도 노이즈와 데이터 분포 변화의 영향을 받습니다. 데이터 품질 점검과 성능 검증을 생략할 수 없습니다.
- **④:** 운영 중 데이터 특성이 달라지면 성능이 저하될 수 있습니다. 지속적으로 성능을 확인하고, 필요하면 모델을 재학습해야 합니다.

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

모델의 예측 점수가 가장 높다고 해서 반드시 정답인 것은 아닙니다. 오분류로 발생할 수 있는 비용을 고려하여 자동 처리 기준을 정하고, 불확실하거나 오류의 영향이 큰 사례는 사람이 검토하도록 설계하는 것이 적절합니다. 이때 예측 점수가 실제 정답 가능성을 잘 나타내는지도 검증해야 합니다.

**오답 해설**

- **①:** 가장 높은 예측 점수는 해당 클래스가 반드시 정답이라는 보장이 아닙니다.
- **②:** 전체 Accuracy가 높아도 일부 입력에서는 중요한 오분류가 발생할 수 있습니다. 예외 처리나 모니터링을 무조건 제외할 수 없습니다.
- **④:** 최종 Test Data를 반복적인 모델 조정에 사용하면 독립적인 성능 평가가 어려워집니다. 조정은 Validation Data 등을 활용해야 합니다.

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

`X`는 행이 4개, 열이 3개인 2차원 배열입니다. 각 행이 하나의 Sample, 각 열이 하나의 Feature이므로 `X.shape`는 `(4, 3)`입니다.

`y`에는 4개 Sample의 Target 값이 1차원으로 저장되어 있으므로 `y.shape`는 `(4,)`입니다. `(4,)`는 1차원 배열이고, `(4, 1)`은 2차원 배열이라는 차이가 있습니다.

**오답 해설**

- **①:** `X`의 행과 열을 뒤바꾸었고 `y`를 2차원 배열로 해석했습니다.
- **③:** `X`의 차원과 Sample·Feature 수를 올바르게 반영하지 않았습니다.
- **④:** `y`의 원소 수는 Feature 수인 3이 아니라 Sample 수인 4입니다.

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

이 모델은 택배를 **접수하는 시점**에 배송 지연을 예측해야 합니다. 실제 도착 시각은 배송이 완료된 후에야 알 수 있으므로, 접수 시점의 입력 Feature로 사용할 수 없습니다. 이를 학습에 포함하면 예측 시점에 알 수 없는 정보를 이용하는 데이터 누수(Data Leakage)가 발생합니다.

**오답 해설**

- **①, ②, ③:** 접수 시각, 배송 지역, 접수 당시의 예상 이동 거리는 접수 시점에 확보하거나 계산할 수 있는 정보이므로 Feature 후보가 될 수 있습니다.

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

모델은 $\hat{y}=wx$, 손실 함수는 $L=(wx-y)^2$입니다. 이를 $w$에 대해 미분하면 다음과 같습니다.

$\frac{\partial L}{\partial w}=2(wx-y)\cdot x$

$x=2$, $y=5$, $w=1$을 대입하면,

$\frac{\partial L}{\partial w}=2(1\times2-5)\times2=-12$

**2. 가중치 업데이트**

경사 하강법의 갱신식은 $w_{\text{new}}=w-\eta\frac{\partial L}{\partial w}$입니다. 학습률 $\eta=0.1$을 적용하면,

$w_{\text{new}}=1-0.1\times(-12)=1+1.2=2.2$

따라서 한 번 갱신한 가중치는 **2.2**입니다.

**오답 해설**

- **① `-0.2`:** 기울기에 학습률을 곱한 값을 빼지 않고 더하면 나오는 결과입니다.
- **② `1.2`:** 가중치의 증가량과 갱신된 가중치를 혼동했습니다.
- **④ `3.0`:** 주어진 미분식과 학습률을 적용한 계산 결과가 아닙니다.

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

KNN은 Sample 사이의 거리를 이용해 가까운 이웃을 찾습니다. 그런데 `age`는 수십 단위인 반면 `annual_income`은 수천만 단위이므로, 원본 값으로 유클리드 거리를 계산하면 소득 차이가 거리 값에 훨씬 크게 반영될 수 있습니다. 그 결과 나이 정보의 영향이 상대적으로 작아집니다.

필요하다면 `StandardScaler` 등으로 Feature의 스케일을 조정합니다. 이때 변환 기준은 Training Data에서만 학습하고 Validation·Test Data에는 같은 기준을 적용해야 합니다.

**오답 해설**

- **②:** KNN은 수치형 Feature의 거리를 계산하는 데 사용할 수 있습니다.
- **③:** Feature Scaling은 입력값의 변환이며 정답 Label을 자동으로 변경하지 않습니다.
- **④:** KNN은 Sample 간 거리를 이용하므로 Feature의 스케일에 영향을 받습니다.

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

조건은 `score >= threshold`이고, 임계값은 `0.65`입니다. 각 점수를 비교하면 다음과 같습니다.

- `0.40 < 0.65`이므로 `0`
- `0.65 >= 0.65`이므로 `1`
- `0.80 >= 0.65`이므로 `1`

따라서 예측 Label은 `[0, 1, 1]`입니다. 특히 임계값과 **같은 점수도 포함**된다는 점이 중요합니다.

**오답 해설**

- **①:** `>=`가 아니라 `>`로 비교해 경계값을 제외한 경우입니다.
- **③:** `0.40`은 임계값보다 작으므로 `1`이 될 수 없습니다.
- **④:** `0.80`은 임계값보다 크므로 `1`이 되어야 합니다.

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

KMeans는 한 Cluster에 할당된 Sample들의 **좌표별 산술평균**으로 중심점(Centroid)을 갱신합니다.

- 첫 번째 좌표: $(0+2+4)/3=2$
- 두 번째 좌표: $(0+4+2)/3=2$

따라서 새로운 중심점은 `(2, 2)`입니다.

**오답 해설**

- **② `(6, 6)`:** 평균이 아니라 좌표별 합계를 구한 결과입니다.
- **③ `(0, 0)`:** 첫 번째 Sample의 위치를 중심점으로 잘못 사용했습니다.
- **④ `(2, 3)`:** 두 번째 좌표의 평균을 잘못 계산했습니다.

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

KMeans는 각 Sample을 가까운 중심점에 할당하여 군집을 형성합니다. 따라서 길게 휘어진 밀집 영역처럼 복잡한 형태의 군집을 분리하는 데 한계가 있을 수 있습니다.

DBSCAN은 밀도를 기준으로 연결된 영역을 찾기 때문에 이런 형태의 데이터에 적합할 수 있습니다. 주변에 충분한 이웃이 없는 점을 Noise로 분류할 수도 있습니다. 다만 결과는 `eps`, `min_samples`, Feature Scaling 등에 따라 달라지므로 실제 데이터로 확인해야 합니다.

**오답 해설**

- **①:** KMeans가 모든 형태의 군집을 정확히 분리하는 것은 아닙니다.
- **③:** `k`는 KMeans에서 군집 수를 정할 때 사용합니다. DBSCAN은 밀도 관련 매개변수를 사용합니다.
- **④:** Clustering은 정답 Label 없이 데이터의 구조를 탐색하는 비지도 학습 방법입니다.

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

Cluster ID는 군집을 구분하기 위한 번호이며, 실제 클래스의 Label과 같은 의미로 정해지는 것이 아닙니다. 이 문제에서는 군집 번호와 정답 Label이 서로 반대이지만, **앞의 두 Sample을 같은 그룹으로, 뒤의 두 Sample을 다른 그룹으로 묶은 구조**는 정확히 일치합니다.

예를 들어 두 배열을 그대로 `accuracy_score()`로 비교하면 0이 나오지만, 이는 군집 분할의 일치도를 올바르게 나타내지 못합니다. 정답 Label이 있는 평가라면 번호의 교환에 영향을 받지 않는 ARI(Adjusted Rand Index) 등의 지표를 사용할 수 있습니다.

**오답 해설**

- **①:** 번호가 다르다고 군집의 분할 구조까지 잘못된 것은 아닙니다.
- **②:** Cluster ID를 클래스 Label과 그대로 비교하면 번호 지정에 따라 평가 결과가 달라질 수 있습니다.
- **④:** KMeans는 학습 과정에서 정답 Label을 요구하지 않습니다.

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

실제 정상은 95건, 실제 이상은 5건입니다. 모든 사례를 정상으로 예측했으므로 `TN = 95`, `FN = 5`, `TP = 0`, `FP = 0`입니다.

- **Accuracy:** 전체 100건 중 95건을 맞혔으므로 $(95/100)\times100=95\%$입니다.
- **이상 클래스의 Recall:** 실제 이상 5건 중 맞힌 사례가 없으므로 $(0/5)\times100=0\%$입니다.

즉, Accuracy가 95%로 높아도 이상 사례를 하나도 찾아내지 못한 모델입니다.

**오답 해설**

- **②:** 전체 정확도 95%를 이상 클래스의 Recall과 혼동했습니다.
- **③:** 전체에서 맞힌 사례는 5건이 아니라 95건입니다.
- **④:** 실제 이상 5건을 놓쳤으므로 Accuracy가 100%일 수 없습니다.

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

**1. 정밀도(Precision)**

양성으로 예측한 Sample 중 실제 양성인 비율입니다.

$\mathrm{Precision}=\frac{TP}{TP+FP}=\frac{8}{8+2}=\frac{8}{10}=0.8$

**2. 재현율(Recall)**

실제 양성인 Sample 중 모델이 찾아낸 비율입니다.

$\mathrm{Recall}=\frac{TP}{TP+FN}=\frac{8}{8+6}=\frac{8}{14}\approx0.5714$

참고로 $F_1=\frac{2TP}{2TP+FP+FN}=\frac{16}{24}\approx0.6667$입니다.

**오답 해설**

- **①:** Precision과 Recall의 분모를 서로 바꾸었습니다.
- **③:** `TN`은 이 두 지표의 분자에 사용하지 않으며, 전체 Sample 수도 Recall의 분모가 아닙니다.
- **④:** Precision과 Recall은 전체 Sample 수가 아니라 각각 예측 양성 수와 실제 양성 수를 기준으로 계산합니다.

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

**1. MAE(Mean Absolute Error)**

잔차의 절댓값을 구한 뒤 평균을 계산합니다.

$\mathrm{MAE}=\frac{|1|+|-3|}{2}=\frac{1+3}{2}=2$

**2. MSE(Mean Squared Error)**

잔차를 제곱한 뒤 평균을 계산합니다.

$\mathrm{MSE}=\frac{1^2+(-3)^2}{2}=\frac{1+9}{2}=5$

참고로 $\mathrm{RMSE}=\sqrt{5}\approx2.236$입니다.

**오답 해설**

- **②:** 잔차를 그대로 평균 내면 `-1`이지만 이는 MAE가 아닙니다. MSE는 제곱의 평균이므로 음수가 될 수 없습니다.
- **③:** 절댓값과 제곱의 합계만 구하고 Sample 수 2로 나누지 않았습니다.
- **④:** MAE와 MSE의 결과를 서로 바꾼 경우입니다.

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

모델과 하이퍼파라미터를 선택할 때는 Training Data로 학습하고, Validation Data 또는 Cross-Validation 결과로 설정을 비교해야 합니다. 최종 Test Data는 선택이 끝난 모델을 **독립적으로 평가할 때** 사용합니다.

Test 점수를 확인하면서 설정을 계속 바꾸면 모델 선택 과정에 Test Data의 정보가 반영되어 최종 성능이 실제보다 높게 보일 수 있습니다.

**오답 해설**

- **①:** Test 점수에 맞춰 반복적으로 조정하면 독립적인 최종 평가가 어렵습니다.
- **②:** 학습에 사용한 데이터에서 측정한 성능만으로 미지의 데이터에 대한 일반화 성능을 판단할 수 없습니다.
- **④:** 데이터의 이름을 바꾸더라도 이미 모델 선택에 사용했다는 사실은 달라지지 않습니다.

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

목표는 **한 번도 학습하지 않은 장비**에 대한 예측 성능을 측정하는 것입니다. 동일 장비에서 반복 측정한 기록은 서로 비슷한 특성을 가질 수 있으므로, 행 단위로 나누면 같은 장비의 데이터가 Training과 Validation에 동시에 포함될 수 있습니다. 그러면 신규 장비에 대한 성능이 실제보다 높게 평가될 위험이 있습니다.

따라서 장비 ID를 Group으로 지정하여 동일 장비의 기록이 서로 다른 세트에 나뉘지 않도록 해야 합니다. 교차 검증에는 `GroupKFold` 같은 방법을 사용할 수 있습니다.

**오답 해설**

- **①:** 행 단위 무작위 분할은 장비 간 독립성을 보장하지 못합니다.
- **③:** Feature 평균으로 Target을 채우는 것은 장비별 데이터 분할 방법이 아닙니다.
- **④:** 높은 점수가 나오는 분할을 골라 사용하면 평가 결과에 선택 편향이 생깁니다.

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

다음 달 방문객 수를 예측하려면 실제 운영과 마찬가지로 **과거 데이터로 학습하고 그 이후 기간으로 평가**해야 합니다. Validation과 Test도 시간 순서를 고려해 분리하며, 결측값 처리나 Feature 생성에 미래 시점의 정보를 사용하지 않도록 해야 합니다.

**오답 해설**

- **①:** 미래 기록을 학습에 넣고 과거 기록으로 평가하면 다음 달 예측이라는 목표와 맞지 않습니다.
- **②:** 데이터를 무작위로 섞으면 미래의 정보가 학습에 들어갈 수 있어 실제 운영 성능을 과대평가할 위험이 있습니다.
- **③:** 더 최신인 데이터의 통계를 과거의 전처리에 사용하면 예측 시점에 이용할 수 없는 정보가 반영될 수 있습니다.

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

**1. 업무별 접근 방식**

- **업무 A — Rule-Based Systems:** 생년월일이 비어 있는지만 확인하면 되므로 조건문으로 처리할 수 있습니다. 판단 기준이 명확해 머신러닝 모델을 사용할 필요가 없습니다.
- **업무 B — Supervised Learning:** 상담 문장은 표현이 다양해 모든 분류 규칙을 직접 작성하기 어렵습니다. 과거 문의와 담당 부서의 정답 Label이 있으므로 지도학습 기반 분류 모델을 검토할 수 있습니다.

**2. 사람의 검토가 필요한 상황**

예측 점수가 기준보다 낮거나 잘못 배정했을 때 처리 지연의 영향이 큰 문의는 담당자가 확인하도록 할 수 있습니다. 자동 처리 여부는 예측 결과의 신뢰성과 오분류 위험을 고려해 결정해야 합니다.

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

**모범 답안**

```python
import numpy as np

X = np.array([
    [1, 2],
    [2, 1],
    [3, 4],
], dtype=float)

w = np.array([2.0, -1.0])
b = 1.0
predictions = X @ w + b

print(predictions)        # [1. 4. 3.]
print(predictions.shape)  # (3,)
```

**1. 예측값 계산**

모델은 $\hat{y}=2x_1-x_2+1$입니다. 각 Sample에 대입하면 다음과 같습니다.

- 첫 번째 `[1, 2]`: $2\times1-2+1=1$
- 두 번째 `[2, 1]`: $2\times2-1+1=4$
- 세 번째 `[3, 4]`: $2\times3-4+1=3$

따라서 예측값은 `[1. 4. 3.]`입니다.

**2. 배열의 Shape**

`X`의 Shape는 `(3, 2)`, `w`의 Shape는 `(2,)`입니다. `X @ w`는 Sample마다 하나의 예측값을 계산하므로 결과는 3개 원소를 가진 1차원 배열입니다. 스칼라 절편 `b`를 더해도 Shape는 **(3,)**으로 유지됩니다.

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

**모범 답안**

**1. 문제가 되는 이유**

원본 코드의 `StandardScaler().fit_transform(X)`는 데이터를 나누기 전에 **전체 Sample의 평균과 표준편차**를 계산합니다. 이 과정에 Test Data의 정보까지 포함되므로 Training Data에 적용할 변환 기준이 평가 데이터의 영향을 받습니다. 이를 데이터 누수(Data Leakage)라고 합니다.

**2. 수정 코드**

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

먼저 데이터를 나눈 뒤 Training Data에서만 `fit_transform()`을 실행합니다. Test Data에는 이미 학습한 기준으로 `transform()`만 적용해야 합니다.

교차 검증 환경에서는 각 Fold 안에서도 같은 원칙이 지켜져야 하므로, `Pipeline`을 사용하면 전처리 단계의 누수를 방지하기 쉽습니다.

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

**모범 답안**

**1. Cluster ID를 단정할 수 없는 이유**

KMeans의 Cluster ID는 군집을 구분하기 위한 식별 번호입니다. `0`과 `1`이라는 번호 자체에 우열이나 고정된 의미는 없습니다. 군집의 특성은 실제 데이터의 분포와 중심값을 바탕으로 해석해야 합니다.

**2. 운영팀이 참고할 수 있는 해석**

- **Cluster 0 — 저빈도·장시간 이용 그룹(Sample 45개):** 주당 평균 2회 방문하며 평균 160분 동안 머무릅니다. 장시간 이용자를 위한 좌석이나 편의 시설 운영을 검토할 수 있습니다.
- **Cluster 1 — 고빈도·단시간 이용 그룹(Sample 70개):** 주당 평균 8회 방문하지만 평균 체류 시간은 35분입니다. 짧고 반복적인 이용에 적합한 동선이나 공간 운영을 검토할 수 있습니다.

이는 **군집별 평균으로부터 얻은 해석**이며, 방문 목적이나 이용자 성격을 확정하는 근거는 아닙니다. 또한 Sample 수가 곧 고유 이용자 수라는 보장도 없습니다.

**3. 추가로 확인할 사항 — Feature Scaling**

방문 횟수와 체류 시간은 단위와 값의 범위가 다릅니다. KMeans는 거리의 영향을 받으므로 스케일이 큰 Feature가 군집 형성에 과도하게 작용할 수 있습니다. 적절한 Scaling을 적용했는지 확인하고, 필요하다면 적용 전후의 군집 결과를 비교해야 합니다.

</details>

### Q-21. Threshold와 예측 결과

**관련 개념:** [Chapter 03](../Chapter-03/README.md) · Logistic Regression · Decision Threshold

클래스 1의 예측 점수가 `[0.20, 0.45, 0.60, 0.85]`입니다. Threshold가 `0.50`일 때와 `0.40`일 때의 예측 Label을 각각 작성하고, Threshold를 낮췄을 때 일반적으로 어떤 변화가 나타날 수 있는지 설명하시오. NumPy 코드로 작성해도 됩니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**모범 답안**

**1. 임계값별 예측 Label**

- Threshold `0.50`: `[0, 0, 1, 1]`
- Threshold `0.40`: `[0, 1, 1, 1]`

```python
import numpy as np

scores = np.array([0.20, 0.45, 0.60, 0.85])

print((scores >= 0.50).astype(int))  # [0 0 1 1]
print((scores >= 0.40).astype(int))  # [0 1 1 1]
```

**2. Threshold를 낮췄을 때의 변화**

임계값을 `0.50`에서 `0.40`으로 낮추면 두 번째 Sample(`0.45`)도 양성으로 분류되어 예측 양성 수가 2개에서 3개로 늘어납니다.

일반적으로 임계값을 낮추면 양성으로 예측하는 수는 **줄어들지 않으며**, 실제 양성에 대한 Recall도 감소하지 않습니다. 반면 Precision은 새로 양성으로 분류된 Sample의 실제 Label에 따라 높아지거나 낮아질 수 있습니다. 이 문제에는 실제 Label이 없으므로 Precision과 Recall의 수치를 계산할 수 없습니다.

</details>

### Q-22. Precision이 정의되지 않는 상황

**관련 개념:** [Chapter 04](../Chapter-04/README.md) · Precision · Recall · Confusion Matrix

평가 데이터에 실제 양성(Positive)이 5건 포함되어 있지만, 모델은 모든 Sample을 음성(Negative)으로 예측했습니다. 이 경우 양성 클래스의 Precision과 Recall을 각각 어떻게 해석해야 하는지 설명하시오. 또한, Scikit-learn 등에서 사용되는 `zero_division=0` 옵션의 의미도 함께 작성하시오.

<details>
<summary><strong>정답 및 해설</strong></summary>

**모범 답안**

**1. Precision과 Recall 해석**

모든 Sample을 음성(Negative)으로 예측했으므로 양성 클래스에 대한 `TP = 0`, `FP = 0`, `FN = 5`입니다.

- **Recall = 0:** 실제 양성 5건 중 찾아낸 사례가 없으므로 $\mathrm{Recall}=\frac{TP}{TP+FN}=\frac{0}{5}=0$입니다.
- **Precision = 정의되지 않음:** 양성으로 예측한 Sample이 없으므로 $\mathrm{Precision}=\frac{TP}{TP+FP}=\frac{0}{0}$입니다. 분모가 0이어서 수학적으로 계산할 수 없습니다.

**2. `zero_division=0`의 의미**

scikit-learn에서 `zero_division=0`을 지정하면 분모가 0이어서 정의되지 않는 지표를 **0으로 반환**합니다. 기본값인 `zero_division="warn"`은 0을 반환하면서 관련 경고도 발생시킵니다.

이때 반환된 Precision 0은 수학적으로 계산된 값이 아니라 **정의되지 않는 상황을 표시하기 위해 선택한 값**입니다. 따라서 지표를 해석할 때 예측 양성 건수와 실제 양성 건수도 함께 확인해야 합니다.

</details>


### Q-23. 장비 고장 예측 모델의 평가 설계

**관련 개념:** [Chapter 04](../Chapter-04/README.md) · Temporal Split · Group-Aware Evaluation · Generalization

총 200대 장비의 주간 센서 누적 기록을 활용하여 장비의 고장 위험을 예측하는 모델을 개발하고자 합니다. 비즈니스 목적에 따른 올바른 검증을 위해, 다음 두 가지 시나리오에 각각 적합한 **데이터 분할 전략(Splitting Strategy)**을 제시하고 그 이유를 설명하시오.

- **시나리오 A:** **이미 운영 중인 기존 장비**의 **다음 달** 고장 위험을 예측합니다.
- **시나리오 B:** 공장에서 새로 도입되어 **학습에 한 번도 사용된 적 없는 신규 장비**의 고장 위험을 예측합니다.

<details>
<summary><strong>정답 및 해설</strong></summary>

**모범 답안**

**1. 시나리오 A — 시계열 분할(Temporal Split)**

- **분할 전략:** 시간 순서를 유지하여 과거의 센서 기록으로 학습하고, 이후 기간의 기록으로 검증 및 테스트합니다.
- **선택 이유:** 기존 장비의 다음 달 고장 위험을 예측할 때는 그 시점까지 확보된 정보만 사용할 수 있습니다. 미래 기록이 학습이나 전처리에 반영되면 시간적 데이터 누수(Temporal Data Leakage)가 발생하여 예측 성능이 과대평가될 수 있습니다.

**2. 시나리오 B — 그룹 기반 분할(Group-Aware Split)**

- **분할 전략:** 장비 ID(Device ID)를 기준으로 데이터를 나누어, 동일 장비의 기록이 훈련 데이터와 평가 데이터에 동시에 포함되지 않도록 합니다. 교차 검증에는 `GroupKFold` 등을 사용할 수 있습니다.
- **선택 이유:** 동일 장비의 반복 측정 기록은 고유 특성을 공유할 수 있습니다. 같은 장비의 기록이 양쪽에 있으면 처음 보는 신규 장비에 대한 일반화 성능이 실제보다 높게 평가될 위험이 있습니다.

**추가 고려 사항**

새 장비의 **미래** 고장을 예측하는 상황이라면 장비 ID와 시간 조건을 함께 만족하도록 데이터를 나누어야 합니다. 평가 방식은 실제 운영 시점과 예측 대상을 반영해야 합니다.

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

**모범 답안**

**1. 문제가 되는 이유**

원본 코드는 `GridSearchCV`로 Fold를 나누기 **전에** 전체 `X_train`에 `StandardScaler().fit_transform()`을 적용합니다. 각 Fold의 검증 데이터도 평균과 표준편차 계산에 이미 사용된 상태이므로, 교차 검증 결과에 데이터 누수가 발생할 수 있습니다. 독립적으로 보관한 최종 Test Data와는 별개로, **교차 검증 내부의 평가가 오염된 것**입니다.

**2. 수정 코드**

```python
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", KNeighborsClassifier()),
])

search = GridSearchCV(
    pipeline,
    {"classifier__n_neighbors": [3, 5, 7]},
    cv=5,
)
search.fit(X_train, y_train)

print(search.best_params_)
```

**3. 코드 설명**

- **전처리 시점:** `Pipeline`을 사용하면 각 Fold의 Training Data에서만 `StandardScaler`가 `fit()`되고, 해당 Fold의 Validation Data에는 `transform()`만 적용됩니다.
- **하이퍼파라미터 지정:** `classifier__n_neighbors`는 Pipeline의 `classifier` 단계에 있는 `n_neighbors`를 조정한다는 뜻입니다. 형식은 `단계이름__파라미터명`입니다.

최종 Test Data는 모델과 설정을 확정한 뒤 별도로 평가할 때 사용합니다.

</details>

---

[← Summary 목차](./README.md) · [Problems](./problem.md) · [AI 목차](../README.md)
