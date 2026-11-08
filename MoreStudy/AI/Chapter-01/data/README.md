[← Chapter 01](../README.md)

# Dataset Notes

Chapter 01의 CSV는 설명을 위해 생성한 **교육용 가상 데이터**입니다. 실제 날씨, 사람의 행동, 센서 이상 빈도를 나타내지 않습니다.

| 파일 | 행 수 | 특징 | 정답 |
|---|---:|---|---|
| `weather_choices.csv` | 100 | 강수 확률(%), 풍속(km/h) | 가상의 우산 선택(0/1) |
| `rare_events.csv` | 400 | 가상 센서 A, B | 가상의 드문 사건 발생 여부(0/1) |

두 파일은 `python scripts/make_datasets.py`로 동일하게 다시 생성할 수 있습니다. 난수 생성기에 고정된 시드가 적용되며, CSV 기록을 학습·평가 과정에서 직접 수정하지 않습니다.

붓꽃(`load_iris`)과 손글씨 숫자(`load_digits`)는 scikit-learn 내장 데이터셋을 사용하므로 별도 CSV가 없습니다.

---

[← Chapter 01](../README.md) · [Contents](../README.md#contents)
