# Chapter 09. Data Visualization Project

데이터를 읽고 그래프를 그리는 단계에서 나아가, **문제를 정의하고 자료를 검증한 뒤 해석 가능한 분석 결과를 전달하는 과정**을 학습합니다. Mini Project에서는 정적 보고서를, Advanced Project에서는 필터·완전성·지표의 일관성을, Challenge에서는 다중 입력·예외 처리·자동 검증을 다룹니다.

입력 데이터의 구성은 [Data Provenance](./resources/DATA_PROVENANCE.md)에서 확인할 수 있습니다.

이번 장에는 총 **10개의 독립 프로젝트**가 있습니다. 각 프로젝트는 `README.md`, 시작 코드, 입력 데이터, 모범 구현과 테스트에 연결되어 있으며, 모범 구현의 출력 그림을 제공합니다.

## Contents

1. [Project Overview](#1-project-overview)
2. [Project Preparation](#2-project-preparation)
3. [Mini Projects](#3-mini-projects)
4. [Advanced Projects](#4-advanced-projects)
5. [Challenge Problems](#5-challenge-problems)
6. [Example & Quiz](#6-example--quiz)
7. [Final Review](#7-final-review)
8. [실행 및 검증](#8-실행-및-검증)

---

## 1. Project Overview

이번 장에서 완성할 결과물은 데이터 자체뿐 아니라 **데이터의 유효성·수집 범위·지표의 분모·시각화의 단위·재현성**을 함께 설명해야 합니다. 아래 원칙을 각 프로젝트에서 반복해서 확인합니다.

- **Data Contract:** 어떤 열과 값이 필요한지, 잘못된 값은 어떻게 처리할지 정의합니다.
- **Observation Grain:** 한 행이 하루·주문·시간·요청 중 무엇을 나타내는지 확인합니다.
- **Metric Definition:** P95, 매출액, 정시 도착률 등 지표마다 계산 범위와 분모를 명시합니다.
- **Completeness:** 관측이 없는 경우와 유효한 측정값이 0인 경우를 구별합니다.
- **Consistent Outputs:** 같은 필터를 적용한 CSV·PNG·HTML·KPI는 같은 값을 설명해야 합니다.
- **Quality Gate:** 정상 입력뿐 아니라 오류·누락·값 변경·재실행 상황까지 검증합니다.

결과 그림에 **측정 단위·날짜 기준·필터 조건**을 적절히 표시하세요. 단순히 그래프가 생성되었다는 사실만으로 분석이 완료되지는 않습니다.

## 2. Project Preparation

이 장의 주요 도구는 `pandas`, `numpy`, `matplotlib`, `plotly`입니다. Python 3.10 이상을 권장합니다.

```bash
python -m pip install -r requirements.txt
```

프로젝트의 구현 전에 필요한 내용은 [Project Preparation](./resources/PROJECT_PREPARATION.md)에 정리했습니다. 시간대 변환, 결측과 0의 차이, P95, 단위, 도표 구성, 해시와 재현성 등을 포함합니다. 기본 문법·데이터프레임 조작은 앞선 Chapter에서 학습한 내용을 적용합니다.

진행할 때는 먼저 **문제별 README → 입력 CSV → `starter.py` → 모범 구현 → 테스트** 순서로 확인하세요. 프로젝트 정답 코드는 문제 본문에 공개하지 않고 `solutions/`에 분리했습니다.

## 3. Mini Projects

| 프로젝트 | 주요 목표 | 결과 예시 |
|---|---|---|
| [Mini 01 — Weather Visualization Report](./projects/mini_01_weather_report/README.md) | 정렬된 기상 관측으로 서로 다른 축의 정적 보고서 작성 | [PNG](./figures/projects/mini_01_weather_report.png) |
| [Mini 02 — Retail Sales Performance Report](./projects/mini_02_retail_report/README.md) | 취소 주문을 제외한 매출액 계산과 막대그래프 | [PNG](./figures/projects/mini_02_retail_report.png) |

## 4. Advanced Projects

| 프로젝트 | 분석 질문 | 추가 구현 요소 |
|---|---|---|
| [Advanced 01 — Weather Monitoring Dashboard](./projects/advanced_01_weather_dashboard/README.md) | 관측소마다 어떤 날짜에 기록이 빠졌나요? | 관측소 × 날짜 완전성, 다중 필터 |
| [Advanced 02 — Customer Behavior Analysis](./projects/advanced_02_customer_behavior/README.md) | 어떤 고객군의 구매 참여율이 높나요? | 모집단 분모, 고객·주문 결합 |
| [Advanced 03 — Service Performance Monitoring](./projects/advanced_03_service_monitor/README.md) | 어느 서비스가 느리거나 오류가 많나요? | 요청 검증, P95, 서버 오류율, KST 변환 |
| [Advanced 04 — Regional Electricity Demand Analysis](./projects/advanced_04_electricity_demand/README.md) | 누락된 시간의 일별 에너지를 확정할 수 있나요? | MW/MWh, 24시간 완전성 |
| [Advanced 05 — Urban Transportation Dashboard](./projects/advanced_05_urban_metro/README.md) | 기록 누락과 실제 승객 0명을 어떻게 구분하나요? | 예정 운행시간, 노선 필터, 인터랙티브 차트 |

Advanced 문제는 각 README에서 **STEP별 구현 가이드와 필요한 경우에만 열리는 코드 힌트**를 제공합니다. 자세한 구현은 `solutions/`에서 확인할 수 있습니다.

## 5. Challenge Problems

| 프로젝트 | 핵심 검증 사항 |
|---|---|
| [Challenge 01 — Airport Operations Analysis](./projects/challenge_01_airport_operations/README.md) | 운항·결항·정시도착 분모와 경계 지연시간 |
| [Challenge 02 — Energy Demand & Anomaly Detection](./projects/challenge_02_energy_anomalies/README.md) | 시간대별 중앙값 기준선, 이상 구간, 장애 구간 `[start,end)` |
| [Challenge 03 — City Transit Reliability Platform](./projects/challenge_03_transit_reliability/README.md) | 예정 슬롯, 전 행 감사, 정적·대화형 분석 일치, SHA-256, Quality Gate |

Challenge 03은 본 장의 통합 프로젝트입니다. 최종 결과에 필요한 파일은 Audit Log, Coverage, Station/Daily/Hourly Summary, Incident Comparison, PNG, HTML, Summary JSON, Manifest입니다. 기본 제공 데이터의 결과는 **672 예정 / 664 유효 / 8 누락 / 원본 8행 제외**입니다. 자세한 입력 계약은 프로젝트 README에 있습니다.

## 6. Example & Quiz

새로운 개념을 따로 길게 반복하기보다, 분석 중 자주 발생하는 실수와 계산을 짧게 점검합니다.

**Example 01 — P95 선형 보간**

```python
import pandas as pd

latency = pd.Series([100, 200, 300])
print(latency.quantile(0.95, interpolation="linear"))  # 290.0
```

값 세 개를 정렬한 뒤 인덱스 1.9의 위치를 선형 보간하므로 P95는 290ms입니다. 이 보간은 **시간대별 누락 데이터를 임의로 채우는 작업이 아닙니다**.

**Example 02 — 결측과 0의 차이**

```python
import pandas as pd

boardings = pd.Series([0, None, 12])
print(boardings.notna().sum())  # 2: 유효 관측 수
print(boardings.sum())         # 12.0: 관측된 인원 합계
```

첫 항목은 실제로 관측된 0명이고, 두 번째 항목은 기록이 없음을 의미합니다. 예정 슬롯 수가 3일 때 관측 완전성은 2/3입니다.

### Quiz

**Q1.** 요청 3건의 응답시간이 100·200·300ms일 때 선형 보간 P95는 얼마인가요?

<details><summary>정답 및 해설</summary>

**290ms**입니다. 위치가 `(3-1) × 0.95 = 1.9`이므로 200ms와 300ms 사이에서 90% 선형 보간합니다.
</details>

**Q2.** 예정 슬롯 8개 중 관측 7개(그중 0명 1개)인 경우 유효 슬롯 수와 누락 슬롯 수는 얼마인가요?

<details><summary>정답 및 해설</summary>

**유효 7개, 누락 1개**입니다. 0명도 유효 관측이므로 누락으로 처리하면 안 됩니다.
</details>

**Q3.** 예정 항공편 100편 중 취소 10편, 운항 90편 중 정시 도착 72편이면 정시 도착률과 결항률은 각각 얼마인가요?

<details><summary>정답 및 해설</summary>

정시 도착률은 `72/90 = 80%`, 결항률은 `10/100 = 10%`입니다. 서로 다른 분모를 사용합니다.
</details>

**Q4.** 같은 `request_id`가 두 번 등장했을 때 첫 행을 보존하고 나머지만 제외해도 되나요?

<details><summary>정답 및 해설</summary>

**안 됩니다.** Advanced 03의 계약에서는 같은 ID를 가진 모든 행을 제외하고 Audit Log에 원본 행 번호와 사유를 기록합니다.
</details>

**Q5.** 시간별 평균 수요가 400MW로 하루 24시간 완전히 관측되었다면 하루 에너지는 얼마인가요?

<details><summary>정답 및 해설</summary>

`400MW × 24h = 9,600MWh`입니다. 단, 24시간 관측이 누락 없이 갖춰졌다는 가정이 필요합니다.
</details>

**Q6.** 아래 중 유효한 요청이 없는 시간대의 처리로 적절한 것은 무엇인가요?

- A. P95와 서버 오류율을 모두 `0`으로 입력합니다.
- B. 요청 수는 `0`, P95와 서버 오류율은 `자료 없음`으로 표시합니다.
- C. 앞 시간대의 P95를 복사합니다.
- D. 서버 오류율만 `100%`로 표기합니다.

<details><summary>정답 및 해설</summary>

**B**입니다. 요청 수는 건수이므로 0이지만, P95와 오류율은 계산할 유효 요청이 없어서 정의되지 않습니다. 서버 오류가 한 건도 없더라도 **유효 요청이 존재할 때의 0%**와 구분해야 합니다.
</details>

**Q7.** UTC `2026-09-30T22:00:00Z` 기록을 한국시간 날짜별로 집계한다면 어느 날짜에 포함되나요?

<details><summary>정답 및 해설</summary>

**2026년 10월 1일**입니다. UTC에 9시간을 더하면 KST 2026-10-01 07:00입니다. 날짜 필터는 이 변환 결과를 기준으로 적용합니다.
</details>

**Q8.** 정적 PNG와 대화형 HTML의 KPI 값이 같아도, 분석 결과의 일관성이 확보되었다고 볼 수 있나요?

<details><summary>정답 및 해설</summary>

**그것만으로는 충분하지 않습니다.** 그래프의 각 Trace·집계 단위·필터가 같아야 하고, CSV 다운로드와 Summary JSON도 같은 모집단을 참조해야 합니다. 또한 누락된 기록의 처리와 단위 표기가 일치하는지 확인해야 합니다.
</details>

## 7. Final Review

결과물을 제출하기 전에 [Final Review](./resources/FINAL_REVIEW.md)에서 다음 항목을 확인하세요. 데이터 검증 사유, 분모와 단위, 날짜·시간대, 관측 완전성, 정적·대화형 결과의 일치, 반복 실행 및 시각적 가독성을 다룹니다.

## 8. 실행 및 검증

모든 경로는 이 `Chapter-09/` 폴더를 기준으로 작성되어 있습니다.

```bash
# 모범 구현 실행 예시
python solutions/mini_01_weather_report/reference_solution.py
python solutions/advanced_03_service_monitor/reference_solution.py
python solutions/challenge_03_transit_reliability/reference_solution.py

# 전체 테스트
python -m unittest discover -s tests -v

# Challenge 03의 변형 입력/재현성/산출물 검증
python projects/challenge_03_transit_reliability/quality_gate.py --script solutions/challenge_03_transit_reliability/reference_solution.py
```

테스트할 프로그램은 `--data`, `--output` 옵션으로 별도 입력·출력 경로를 지정할 수 있어야 합니다. 구현 과정에서는 정답을 그대로 복사하기보다 입력값을 바꾸어도 규칙대로 계산되는지 확인하세요. **정상 정책에 따라 오류 행을 제외한 경우는 성공 실행이 될 수 있지만, 필수 기준정보의 계약 위반은 실패**로 처리합니다.

**자동 검증 범위:** 파일·숫자·스키마·필터·해시·주요 Figure/Trace 구성입니다. 색상 대비·글자 겹침·정보 전달력 등은 결과 PNG·HTML을 열어 별도로 검토해야 합니다.

---

모든 데이터는 교육 목적으로 생성한 가상 데이터입니다. 그래프 수치와 예시 출력은 이 저장소의 모범 구현을 실행해 확인한 결과입니다.

참고 그림을 최신 모범 구현 결과로 다시 만들려면 다음 명령을 사용합니다.

```bash
python scripts/regenerate_figures.py
```
