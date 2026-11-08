# Advanced Project 05 — 모범 구현 해설

관측되지 않았다는 사실 자체가 중요한 데이터 품질 지표입니다.

## 실행

```bash
python solutions/advanced_05_urban_metro/reference_solution.py
```

## 코드 검토 순서

1. 노선별 역 목록과 운영 시간·기간을 정의합니다.
2. 행 검증 후 유효한 실제 기록을 분리합니다.
3. 예정 시간 슬롯을 생성하고 관측 기록을 left join합니다.
4. 누락과 0명 관측을 구분해 역별 요약을 계산합니다.
5. 그래프와 CSV가 같은 노선 필터를 사용하도록 연결합니다.

이 파일의 계산 규칙은 프로젝트 README의 데이터 검증 및 계산 기준을 따릅니다. 출력 그림은 `figures/projects/`에 생성된 예시와 비교할 수 있습니다.
