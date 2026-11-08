[← Chapter 01](../../README.md) · [Mini Projects](../../README.md#section-1-10)

# Mini Project 01. Rule-Based vs Learning-Based Weather Decision

## 문제 상황

강수 확률과 풍속으로 우산 선택 여부를 예측합니다. 사람이 지정한 규칙과 학습 모델을 동일한 평가 데이터에서 비교하고, 두 방식의 차이를 분석하세요.

## 입력 데이터

[`weather_choices.csv`](../../data/weather_choices.csv)는 우산 선택 여부를 나타낸 **실습용 합성 데이터** 100건입니다. 실제 기상 예보나 안전 판단에 사용하지 않습니다.

| 열 | 의미 | 값의 범위 |
|---|---|---|
| `case_id` | 샘플 식별자 | 중복 없는 문자열 |
| `rain_probability_pct` | 강수 확률 | 0~100 (%) |
| `wind_speed_kmh` | 풍속 | 0 이상 (km/h) |
| `umbrella_chosen` | 선택 여부를 나타내는 레이블(Label) | 0: 미선택, 1: 선택 |

각 행은 하나의 샘플(Sample)입니다. 강수 확률과 풍속은 입력 특성(Feature), `umbrella_chosen`은 예측 대상인 타깃(Target)입니다.

## 구현 STEP

1. **Data Inspection:** 필수 열, 행 수, 결측값, 중복 ID, 수치 범위를 검증합니다.
2. **Rule-Based Decision:** 강수 확률이 60% 이상이면 우산을 선택하는 규칙을 구현합니다.
3. **Train/Test Split:** 전체 자료의 75%를 학습, 25%를 평가에 사용합니다. `random_state=42`, `stratify=y`를 적용합니다.
4. **Learning Model:** `StandardScaler`와 `KNeighborsClassifier(n_neighbors=5)`를 연결해 학습합니다.
5. **Comparison:** 두 방식의 Accuracy를 같은 평가 데이터에서 계산하고 오분류 사례를 그래프로 표시합니다.
6. **Interpretation:** 결과 차이와 일반화 가능성의 한계를 설명합니다.

<details>
<summary><strong>코드 힌트 — 데이터 분할</strong></summary>

```python
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.25, random_state=42, stratify=y
)
```

</details>

## 실행 및 결과

`Chapter-01/`에서 다음 명령을 실행합니다.

```bash
python projects/mini_01_weather_decision/starter.py
```

`starter.py`는 미완성 실습 코드이며, 구현 전에는 `NotImplementedError`가 발생합니다. 모범 구현은 [`solutions/mini_01_weather_decision.py`](../../solutions/mini_01_weather_decision.py)에 있습니다.

```bash
python solutions/mini_01_weather_decision.py
```

기본 데이터에서 규칙 기반 방식은 21/25(84.0%), 학습 모델은 24/25(96.0%)를 맞혔습니다. 결과 이미지는 `outputs/mini_01_weather_decision.png`에 생성됩니다. 이 비교는 제공된 합성 데이터와 고정된 분할 조건에 한정됩니다.

![Mini 01 분석 결과](../../figures/mini_01_weather_decision.png)

## 테스트 시나리오

- 두 방식의 Accuracy가 0~1 범위인지 확인합니다.
- `case_id` 중복 또는 강수 확률 101 입력 시 검증 오류가 발생해야 합니다.
- 동일한 입력과 분할 조건에서 결과가 재현되어야 합니다.
- 풍속이 같아도 강수 확률이 다른 샘플의 예측이 반드시 같다고 가정하지 않습니다.

**완료 기준:** 두 예측 방법의 성능을 같은 평가 조건에서 비교하고, 결과의 의미와 한계를 설명합니다.

---

[← Chapter 01](../../README.md) · [Contents](../../README.md#contents)
