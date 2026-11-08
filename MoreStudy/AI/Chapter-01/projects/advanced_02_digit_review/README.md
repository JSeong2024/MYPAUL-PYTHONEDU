[← Chapter 01](../../README.md) · [Advanced Projects](../../README.md#section-1-11)

# Advanced Project 02. Handwritten Digit Recognition & Human Review

## 문제 상황

손글씨 숫자 이미지를 자동으로 분류합니다. 그러나 분류가 불확실한 이미지까지 모두 자동 처리할 필요는 없습니다. **사람이 확인해야 할 대상을 구분하는 간단한 검토 기준**을 추가하고, 자동 처리 범위와 그 한계를 분석하세요.

## 데이터와 판단 기준

`sklearn.datasets.load_digits()`는 손글씨 숫자 이미지 1,797개로 구성되며, 각 이미지는 **8×8 픽셀(64개 특징)** 입니다. 별도의 온라인 다운로드가 필요하지 않습니다.

KNN의 `predict_proba()`로 계산한 값은 **가까운 이웃 5개의 투표 비율**입니다. 이 값이 0.8 이상이면 `AUTO`, 0.8 미만이면 `REVIEW`로 분류합니다. **투표 비율을 실제 정답 확률이나 보정된 신뢰도와 동일하게 해석하면 안 됩니다.**

| 상태 | 조건 | 처리 |
|---|---|---|
| `AUTO` | 이웃 투표의 최댓값 ≥ 0.8 | 자동 결과 표시 |
| `REVIEW` | 이웃 투표의 최댓값 < 0.8 | 사람의 확인 대상으로 표시 |

실제 서비스를 운영한다면 검토 비용·오류 비용·검토자 판단의 일관성을 추가로 확인해야 합니다.

## 구현 STEP

1. **Data Inspection:** 이미지 수, 특징 수, 레이블 종류, 이미지 배열(8×8)을 확인합니다.
2. **Data Split:** 80:20 층화 분할하고 `StandardScaler`와 KNN(이웃 5개)을 학습합니다.
3. **Prediction:** 평가 데이터에서 정답 레이블과 예측 레이블을 얻습니다.
4. **Review Gate:** `predict_proba()`의 행별 최댓값이 기준 미만이면 검토 대상으로 분리합니다.
5. **Metrics:** 자동 처리 건수, 검토 건수, 전체 정확도, 자동 처리 대상의 정확도를 계산합니다.
6. **Visualization:** 자동 처리 이미지와 사람 검토 대상을 나란히 표시합니다.
7. **Scenario Check:** 기준을 0.6, 0.8, 1.0으로 변경한 뒤 자동 처리 비중이 어떻게 달라지는지 비교합니다.

<details>
<summary><strong>코드 힌트 — 검토 대상 구분</strong></summary>

```python
votes = model.predict_proba(x_test).max(axis=1)
review_mask = votes < threshold
```

</details>

<details>
<summary><strong>코드 힌트 — 자동 처리 대상이 0건인 경우</strong></summary>

```python
auto_accuracy = (
    accuracy_score(y_test[~review_mask], predicted[~review_mask])
    if (~review_mask).any() else None
)
```

자동 처리 사례가 없다면 자동 처리 정확도는 0%가 아니라 **자료 없음**에 해당합니다.

</details>

## 실행 및 결과

`Chapter-01/`에서 실행합니다.

```bash
python projects/advanced_02_digit_review/starter.py
python solutions/advanced_02_digit_review.py
```

예시 결과(기준 0.8): 평가 360건 중 **자동 처리 346건**, **사람 검토 14건**입니다. 전체 정확도는 약 **96.4%**이며 자동 처리 대상의 정확도는 약 **98.8%**입니다. 검토 대상은 자동으로 틀린 사례와 완전히 일치하지 않습니다.

![Advanced 02 분석 결과](../../figures/advanced_02_digit_review.png)

## 테스트 시나리오

- `AUTO`와 `REVIEW` 건수의 합계가 평가 데이터 수와 같아야 합니다.
- 임계값을 올릴수록 검토 대상의 수가 감소해서는 안 됩니다.
- 임계값 -0.1 또는 1.1은 검증 오류가 발생해야 합니다.
- 실제 정답 레이블은 **평가 단계에서만** 사용합니다. 미래에 입력되는 새로운 이미지의 정답을 미리 안다고 가정하지 않습니다.
- 투표 비율이 높은 사례도 틀릴 수 있으므로 사람의 확인 기능을 완벽한 안전 장치로 표현하지 않습니다.

**완료 기준:** 자동 처리와 검토 대상의 구분, 임계값 변화, 판단 기준의 한계를 함께 설명합니다.

---

[← Chapter 01](../../README.md) · [Contents](../../README.md#contents)
