# Challenge 02 — 모범 구현 해설

이상값의 정의는 기준선과 임계값에 의존합니다. 이상 탐지는 원인 판단과 별개입니다.

## 실행

```bash
python solutions/challenge_02_energy_anomalies/reference_solution.py
```

## 코드 검토 순서

1. 입력과 참조 기준의 유효성을 구분합니다.
2. 지역·시간 슬롯 중복과 결측의 감사 정책을 설계합니다.
3. 지역×시간대 중앙값과 잔차를 계산합니다.
4. 장애의 시작 포함·종료 제외 정책을 적용합니다.
5. 기간 완전성을 계산하고 하루 에너지 확정 조건을 확인합니다.
6. 동일 데이터 재실행에서 파일 내용이 같아지는지 검사합니다.

이 파일의 계산 규칙은 프로젝트 README의 데이터 검증 및 계산 기준을 따릅니다. 출력 그림은 `figures/projects/`에 생성된 예시와 비교할 수 있습니다.

---
[← Project README](../../projects/challenge_02_energy_anomalies/README.md) · [← Chapter 09](../../README.md)
