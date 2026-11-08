[← Chapter 01](../../README.md) · [Advanced Projects](../../README.md#section-1-11)

# Advanced Project 01. Rare Event Detection & Misleading Accuracy

## 문제 상황

가상 센서가 드물게 발생하는 특별한 사건을 구분합니다. 전체 기록에서 특별한 사건은 10% 정도에 불과합니다. **항상 정상이라고 말하는 프로그램도 높은 정확도를 얻을 수 있다는 문제**를 직접 확인하고, 드문 사건을 놓친 정도를 별도로 설명하세요.

## 데이터와 용어

[`rare_events.csv`](../../data/rare_events.csv)는 교육용 가상 기록 400건입니다. 실제 안전·의료·금융 등 고위험 분야에 활용할 수 없습니다.

| 열 | 설명 |
|---|---|
| `record_id` | 사례 ID |
| `sensor_a`, `sensor_b` | 가상의 수치형 센서값 |
| `is_rare_event` | 0: 일반, 1: 드문 사건 |

- **Accuracy(정확도):** 모든 사례 중 정답을 맞힌 비율
- **Rare Event Recall(드문 사건 재현율):** 실제 드문 사건 중 찾아낸 비율
- **Balanced Accuracy(균형 정확도):** 두 클래스 각각의 재현율 평균

이 지표는 Chapter 04에서 더 자세히 학습합니다. 이 프로젝트에서는 **평가 목적에 따라 지표가 달라지는 이유**를 이해하는 데 집중합니다.

## 구현 STEP

1. **Input Validation:** 필수 열·결측·중복 ID·유한한 센서값·0/1 레이블을 검증합니다.
2. **Class Distribution:** 정상/드문 사건의 건수와 비율을 계산합니다.
3. **Train/Test Split:** 75:25 층화 분할을 사용해 양쪽에 드문 사건이 포함되도록 합니다.
4. **Baseline:** 모든 관측을 정상(0)으로 분류하는 비교 기준을 구현합니다.
5. **Learning Model:** `StandardScaler` + `LogisticRegression(class_weight="balanced")`로 학습합니다.
6. **Metric Comparison:** 정확도·드문 사건 재현율·균형 정확도를 같은 평가 자료에서 계산합니다.
7. **Visualization & Explanation:** 지표를 비교하는 막대그래프와 주의점을 작성합니다.

<details>
<summary><strong>코드 힌트 — 드문 사건 재현율</strong></summary>

```python
rare_recall = recall_score(y_test, predicted, pos_label=1, zero_division=0)
```

실제 1인 항목의 분모가 0일 경우 계산 해석에 주의해야 합니다. 제공 데이터에서는 학습·평가 양쪽에 1이 존재합니다.

</details>

<details>
<summary><strong>코드 힌트 — 균형 정확도</strong></summary>

```python
score = balanced_accuracy_score(y_test, predicted)
```

</details>

## 실행 및 확인

`Chapter-01/`에서 실행합니다.

```bash
python projects/advanced_01_rare_event/starter.py
python solutions/advanced_01_rare_event.py
```

기본 평가 데이터 100건(드문 사건 10건)에서 비교 기준은 **정확도 90.0%, 드문 사건 재현율 0.0%**입니다. 학습 모델은 예시 실행에서 **정확도 89.0%, 드문 사건 재현율 80.0%**입니다. 두 모델 중 무엇이 적절한지는 잘못된 판단의 비용을 함께 고려해야 합니다.

![Advanced 01 결과](../../figures/advanced_01_rare_event.png)

## 테스트 시나리오

- `record_id` 중복·누락 및 센서 `NaN`·무한대가 입력되면 검증 실패해야 합니다.
- 비교 기준 모델은 드문 사건을 단 하나도 찾아내지 못합니다.
- 두 모델의 정확도와 드문 사건 재현율을 **동일한 평가 데이터**로 비교합니다.
- 정상 기록 일부를 제거해 클래스 비율을 바꾸면, 기존 성능을 그대로 보장하지 않습니다.
- 결과 보고에는 **데이터 건수와 평가 기준**이 포함되어야 합니다.

**완료 기준:** 높은 정확도가 특정 클래스에서의 실패를 숨길 수 있음을 수치와 그래프로 설명합니다.

---

[← Chapter 01](../../README.md) · [Contents](../../README.md#contents)
