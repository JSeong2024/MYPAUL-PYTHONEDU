# Advanced Reference Solution — Design Notes

## 구조

- `core/metro.py`: 검증, 시간대별 그리드 생성, 집계·Figure 생성. Streamlit에 의존하지 않는 독립 함수입니다.
- `reference_solution.py`: 업로드, 필터, Session State, Page, CSV 내보내기 등 UI 기능을 담당합니다.

## 중요 설계 결정

1. `read_csv(dtype=str, keep_default_na=False)`로 원본 오류를 보존합니다.
2. `duplicated(..., keep=False)`로 중복된 슬롯의 모든 후보 기록을 제외합니다. 임의의 한 건을 유효하다고 가정하지 않습니다.
3. 완전한 역사 × 시간대 조합을 먼저 생성해야 행 자체가 없는 슬롯도 셀 수 있습니다.
4. `boardings = 0`은 관측 성공이며 `NaN`/미관측과 다릅니다.
5. Streamlit 위젯마다 스크립트가 재실행됩니다. 데이터 검증 결과를 `st.cache_data`로 재사용하지만 사용자의 선택값은 `st.session_state`에 보관합니다.
6. 필터는 **KPI 계산보다 먼저 적용**합니다. 전체 대상의 KPI를 필터된 차트와 같이 표시하지 않습니다.
7. 페이지는 `st.Page()`의 함수 기반 구조로 선언하고 entrypoint에서 `st.navigation()`을 한 번만 호출합니다.
8. 업로드된 CSV는 별도로 파싱·검증하며 다른 사용자의 업로드를 공유 캐시에 넣지 않습니다.
9. 실제 보안·인증은 구현하지 않습니다. 로컬 교육용 대시보드이며 민감한 실제 데이터로 공개 배포하지 않습니다.

## 검증 방법

`python -m unittest discover -s tests -v`로 로직 검증을 수행합니다. Streamlit 패키지가 설치되어 있다면 선택적인 AppTest도 실행할 수 있습니다. 실제 브라우저 상호작용은 로컬 환경에서 별도 확인해야 합니다.
