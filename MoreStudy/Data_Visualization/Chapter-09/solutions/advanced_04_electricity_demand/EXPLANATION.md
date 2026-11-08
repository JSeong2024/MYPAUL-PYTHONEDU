# Advanced Project 04 — 모범 구현 해설

MW와 MWh는 서로 다른 단위입니다. 하루 평균 MW를 하루 총에너지 MWh로 직접 표기해서는 안 됩니다.

## 실행

```bash
python solutions/advanced_04_electricity_demand/reference_solution.py
```

## 코드 검토 순서

1. 지역 기준정보와 시간별 측정 ID를 검증합니다.
2. UTC를 KST로 변환하고 같은 지역·시간 중복을 제외합니다.
3. 지역별 KST 하루의 고유 관측 시간이 24개인지 검사합니다.
4. 각 1시간 기록을 이용해 관측 구간 MWh를 합산합니다.
5. `complete/partial`과 확정값 유무를 CSV 및 추이 그래프에 반영합니다.

이 파일의 계산 규칙은 프로젝트 README의 데이터 검증 및 계산 기준을 따릅니다. 출력 그림은 `figures/projects/`에 생성된 예시와 비교할 수 있습니다.
