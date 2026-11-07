# Advanced Project 01 — Reference Implementation Notes

- **Data contract:** CSV 열 검증과 고유 검사 ID 확인. 중복은 행 수와 함께 별도 기록.
- **Quality review:** 두께가 8~12mm 범위를 벗어나거나 결측인 경우 자동 삭제하지 않고 측정 검토 표시. 이 규칙은 학습용 예시.
- **Group denominators:** 결함 비율은 라인별 검사 건수를 분모로 사용. `n`과 함께 제시.
- **Wilson interval:** 이항 비율의 구간 추정 예시. 신뢰구간을 데이터의 완전한 품질 보증으로 해석하지 않음.
- **Bootstrap interval:** 두께 평균의 퍼센타일 부트스트랩 95% 구간; 임의 추출 표본을 가정. 누락과 측정 오류에 따른 편향은 보정하지 못함.
- **Dynamic report:** 입력에 실제 존재하는 Plant만 선택. 각 Plant마다 2×2 Figure를 별도로 저장, 매번 `plt.close(fig)` 실행.
- **Testability:** `prepare_data`, `summarize`, `render_plant`, `run`으로 책임 분리.
- **Alternative:** 설계 목적이 대규모 데이터 처리라면 데이터 검증 파이프라인과 시각화 생성기를 별도 모듈로 분리할 수 있음.
- **Caution:** 관측 자료로 제조 원인을 확정하지 않으며, 검사 표본을 전체 생산량과 혼동하지 않음.
