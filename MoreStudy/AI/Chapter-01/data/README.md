[← Chapter 01](../README.md)

# Dataset Notes

날씨·센서 CSV는 **실습용 합성 데이터(Synthetic Data)** 입니다. 실제 사람의 행동이나 현장 센서에서 수집한 기록이 아닙니다.

| 파일 | 샘플 수 | 입력 특성(Feature) | 타깃(Target) |
|---|---:|---|---|
| `weather_choices.csv` | 100 | 강수 확률(%), 풍속(km/h) | 우산 선택 여부(0/1) |
| `rare_events.csv` | 400 | 센서 A, 센서 B | 드문 사건 발생 여부(0/1) |

두 CSV는 `python scripts/make_datasets.py`로 재생성할 수 있습니다. 난수 시드를 고정해 같은 데이터를 얻도록 구성했습니다.

Iris(`load_iris`)와 Digits(`load_digits`)는 scikit-learn에서 제공하는 공개 데이터셋이며 합성 데이터가 아닙니다. 별도 CSV 없이 라이브러리에서 불러옵니다.

---

[← Chapter 01](../README.md) · [Contents](../README.md#contents)
