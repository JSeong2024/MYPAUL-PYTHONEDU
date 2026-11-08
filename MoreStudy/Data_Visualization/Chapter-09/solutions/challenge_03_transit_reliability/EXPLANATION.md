# Challenge 03 — 모범 구현 해설

데이터의 정확성, 관측 완전성, 시각화의 일관성, 동일 입력의 재현성을 각각 검증해야 합니다.

## 실행

```bash
python solutions/challenge_03_transit_reliability/reference_solution.py
```

## 코드 검토 순서

1. 계약 검증과 참조 데이터 오류·관측 행 오류 정책을 분리합니다.
2. 원본 행마다 복수 사유를 감사 기록으로 남기고 슬롯 경쟁 기록을 모두 제외합니다.
3. 예정 슬롯과 유효 관측을 조인하고 누락·0명·불완전한 날짜를 구분합니다.
4. 정류장·노선·날짜 필터를 CSV·두 종류의 그림에 통일합니다.
5. 장애 `[start, end)` 기간의 유효·누락 슬롯과 승차 인원을 비교합니다.
6. 산출물 해시 및 재실행 일관성을 검증합니다.
7. 정상·잘못된 입력·값 변경·부분 조회 시나리오를 통과시킵니다.

이 파일의 계산 규칙은 프로젝트 README의 데이터 검증 및 계산 기준을 따릅니다. 출력 그림은 `figures/projects/`에 생성된 예시와 비교할 수 있습니다.

---
[← Project README](../../projects/challenge_03_transit_reliability/README.md) · [← Chapter 09](../../README.md)
