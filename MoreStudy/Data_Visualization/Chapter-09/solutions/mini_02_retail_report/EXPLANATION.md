# Mini Project 02 — 모범 구현 해설

주문 건수가 많다고 매출액도 반드시 큰 것은 아닙니다.

## 실행

```bash
python solutions/mini_02_retail_report/reference_solution.py
```

## 코드 검토 순서

1. 주문별 매출액 계산 열을 만듭니다.
2. 완료된 주문만 필터링합니다.
3. `groupby`로 카테고리별 건수·매출액을 계산합니다.
4. 요약 CSV와 그래프를 비교합니다.

이 파일의 계산 규칙은 프로젝트 README의 데이터 검증 및 계산 기준을 따릅니다. 출력 그림은 `figures/projects/`에 생성된 예시와 비교할 수 있습니다.

---
[← Project README](../../projects/mini_02_retail_report/README.md) · [← Chapter 09](../../README.md)
