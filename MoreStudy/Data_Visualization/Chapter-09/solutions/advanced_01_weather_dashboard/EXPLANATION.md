# Advanced Project 01 — 모범 구현 해설

관측 기록 자체의 개수와 관측하기로 예정된 날짜 수는 서로 다릅니다.

## 실행

```bash
python solutions/advanced_01_weather_dashboard/reference_solution.py
```

## 코드 검토 순서

1. 관측소 기준정보의 ID가 고유한지 확인합니다.
2. 관측 ID·수치·참조키·날짜를 검증하고 유효한 행을 분리합니다.
3. 선택 관측소 × 모든 날짜의 슬롯을 만든 다음 left join을 수행합니다.
4. 관측률 분모를 예정 날짜 수로 두고 평균 기온은 관측된 값만 계산합니다.
5. 누락 구간이 유지된 다중 선 그래프와 CSV를 저장합니다.

이 파일의 계산 규칙은 프로젝트 README의 데이터 검증 및 계산 기준을 따릅니다. 출력 그림은 `figures/projects/`에 생성된 예시와 비교할 수 있습니다.
