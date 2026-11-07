<p align="center">
  <img src="banner_DataVisualization.png" width="50%" alt="Data Visualization Class Banner">
</p>

Python을 기반으로 데이터를 그래프로 표현하고, 분석 결과를 효과적으로 전달하는 방법을 학습하는 자료입니다. 시각화의 기본 원칙부터 Matplotlib·Seaborn을 활용한 정적 그래프, Plotly 기반 인터랙티브 시각화, Streamlit 대시보드 제작까지 단계적으로 다룹니다.

각 Chapter는 개념 설명, 실행 가능한 예제 코드, 연습문제와 정답 코드로 구성합니다. 마지막에는 [Data Processing](../Data_Processing/)에서 가공한 기상 데이터를 활용하여 시각화 프로젝트를 완성합니다.

- **주요 언어:** Python
- **주요 도구:** Matplotlib, Seaborn, Plotly, Streamlit
- **권장 선수 학습:** Python 기초 문법, NumPy 배열, Pandas DataFrame
- **자료 구성:** 학습 문서, 예제 코드, 연습문제, 정답 코드, 실습 데이터 및 시각화 결과물

## Contents

### Part 1 — Data Visualization Fundamentals

데이터 시각화의 목적과 주요 그래프 유형을 이해하고, 데이터를 정확하게 표현하기 위한 기본 원칙을 학습합니다.

| Chapter | Topic |
|:---:|---|
| [01](./Chapter-01/) | **Introduction to Data Visualization** — 시각화의 개념과 목적, 데이터와 그래프의 관계, 첫 번째 그래프 |
| [02](./Chapter-02/) | **Principles of Data Visualization** — 그래프 선택, 시각적 인코딩, 색상, 축과 스케일, 오해를 일으키는 표현 |

### Part 2 — Static & Statistical Visualization

Python 라이브러리를 활용하여 정적 그래프를 제작하고, 데이터의 분포·관계·시간에 따른 변화를 해석합니다.

| Chapter | Topic |
|:---:|---|
| [03](./Chapter-03/) | **Matplotlib** — Figure, Axes, Line·Bar·Scatter·Histogram, Subplots, 그래프 스타일과 저장 |
| [04](./Chapter-04/) | **Seaborn** — 분포 및 범주형 시각화, 관계 분석, Heatmap, Pairplot |
| [05](./Chapter-05/) | **Exploratory Data Analysis & Statistical Visualization** — EDA, 분포 해석, 상관관계, 이상치, 통계적 해석 |
| [06](./Chapter-06/) | **Time Series Visualization** — 날짜 축, 시계열 비교, 이동평균, 추세, 계절성, 누락된 관측값 |

### Part 3 — Interactive Visualization & Dashboard

사용자가 그래프를 직접 탐색할 수 있는 시각화와 Python 기반 웹 대시보드를 제작합니다.

| Chapter | Topic |
|:---:|---|
| [07](./Chapter-07/) | **Plotly & Interactive Visualization** — Hover, Zoom, 범례·필터, Plotly Express, HTML 내보내기 |
| [08](./Chapter-08/) | **Dashboard Development with Streamlit** — 레이아웃, 차트, 입력 위젯, 상태 관리, 데이터 캐싱, 배포 기초 |

### Part 4 — Data Visualization Project

앞서 학습한 시각화 기법을 연결하여 데이터 탐색부터 결과 해석, 대시보드 제작까지 하나의 프로젝트를 완성합니다.

| Chapter | Topic |
|:---:|---|
| [09](./Chapter-09/) | **Data Visualization Project** — 기상 데이터 탐색, 시각화 설계, 지역·기간별 비교, 인터랙티브 대시보드 |

## Learning Path

```text
처리된 데이터 (Processed Data)
    ↓
데이터와 시각화 목적 확인 (Data Understanding)
    ↓
그래프 종류 및 표현 방법 선택 (Visualization Design)
    ↓
정적·통계 그래프 제작 (Matplotlib & Seaborn)
    ↓
패턴·분포·추세 해석 (Data Interpretation)
    ↓
인터랙티브 그래프 제작 (Plotly)
    ↓
웹 대시보드 구현 (Streamlit)
    ↓
결과 검토 및 공유 (Review & Communication)
```

이 과정은 데이터 처리 방법을 처음부터 반복하기보다, **어떤 그래프를 왜 선택하고 어떻게 해석해야 하는지**에 집중합니다. 데이터의 수집·정제·변환·집계는 [Data Processing](../Data_Processing/)에서 자세히 다룹니다.

<details>
<summary><strong>권장 선행 학습 목록</strong></summary>

- [Data Processing — Chapter 03. NumPy Fundamentals](../Data_Processing/Chapter-03/)
- [Data Processing — Chapter 04. Pandas & DataFrames](../Data_Processing/Chapter-04/)
- [Data Processing — Chapter 06. Data Cleaning & Validation](../Data_Processing/Chapter-06/)
- [Data Processing — Chapter 07. Data Transformation & Aggregation](../Data_Processing/Chapter-07/)
- [Data Processing — Chapter 08. Data Processing Project](../Data_Processing/Chapter-08/)

</details>

## Getting Started

### 1. 개발 환경

- **Python:** 3.13 권장 (다른 버전은 사용하는 라이브러리의 지원 여부 확인)
- **운영체제:** Windows, macOS, Linux
- **에디터:** Visual Studio Code 권장, JupyterLab 선택 사용

Python 설치 여부를 확인합니다.

```bash
python --version
```

일부 Windows 환경에서는 `py --version`, macOS·Linux 환경에서는 `python3 --version`을 사용해야 할 수 있습니다.

### 2. 가상환경 생성

프로젝트별 라이브러리 관리를 위해 가상환경 사용을 권장합니다. `Data_Visualization/` 디렉터리에서 실행합니다.

```bash
python -m venv .venv
```

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt**

```bat
.venv\Scripts\activate.bat
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

가상환경을 종료하려면 `deactivate`를 실행합니다. `.venv/` 디렉터리는 Git에 커밋하지 않습니다.

### 3. 라이브러리 설치

```bash
python -m pip install --upgrade pip
python -m pip install numpy pandas matplotlib seaborn plotly streamlit
```

| 라이브러리 | 주요 용도 |
|---|---|
| `numpy` | 수치 배열과 기본 연산 |
| `pandas` | 시각화할 데이터 선택 및 구성 |
| `matplotlib` | 정적 그래프와 세부 스타일 제어 |
| `seaborn` | 통계 그래프와 데이터 분포·관계 표현 |
| `plotly` | 인터랙티브 그래프와 HTML 출력 |
| `streamlit` | Python 기반 웹 대시보드 |

Notebook 환경이 필요한 경우 JupyterLab을 추가로 설치할 수 있습니다.

```bash
python -m pip install jupyterlab
jupyter lab
```

Chapter별로 필요한 추가 패키지는 해당 Chapter의 README에서 안내합니다.

### 4. 첫 번째 데이터 시각화

다음 예제는 일주일간의 가상 기온 데이터를 선 그래프로 표현합니다. 그래프의 가로축은 날짜, 세로축은 기온을 나타냅니다.

```python
import matplotlib.pyplot as plt

# 교육용 가상 기온 데이터
weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
temperatures = [21.5, 23.0, 22.4, 25.1, 26.3, 24.8, 23.2]

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(weekdays, temperatures, marker="o", linewidth=2)
ax.set(title="Weekly Temperature", xlabel="Day", ylabel="Temperature (°C)")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()

fig.savefig("weekly_temperature.png", dpi=150)
plt.show()
```

**실행 결과**

- 요일별 기온 변화를 보여주는 선 그래프가 표시됩니다.
- 실행 위치에 `weekly_temperature.png` 파일이 생성됩니다.
- 영어 축 제목을 사용하여 운영체제별 한글 글꼴 설정 없이도 실행할 수 있도록 구성했습니다.

**그래프 해석:** 목요일부터 금요일까지 기온이 상승한 뒤 주말에 감소합니다. 다만 7일간의 예시만으로 장기적인 기후 추세를 판단할 수는 없습니다.

그래프의 목적에 따라 막대그래프·산점도 등의 다른 표현이 더 적절할 수 있습니다. 그래프 선택 기준은 Chapter 02에서 다룹니다.

## Directory Structure

```text
Data_Visualization/
├── README.md
├── banner_DataVisualization.png
├── datasets/             # 여러 Chapter에서 사용하는 공통 데이터
├── Chapter-01/
│   ├── README.md
│   ├── examples/
│   ├── exercises/
│   └── solutions/
├── Chapter-02/
├── Chapter-03/
├── Chapter-04/
├── Chapter-05/
├── Chapter-06/
├── Chapter-07/
├── Chapter-08/
└── Chapter-09/
    ├── README.md
    ├── examples/
    ├── exercises/
    ├── solutions/
    └── project/
```

위 구조는 **학습자료 제작에 따라 추가할 예정인 디렉터리 구성**입니다. Chapter별로 필요하면 `data/`, `outputs/`, `tests/` 등의 디렉터리를 추가할 수 있습니다.

## Code Guidelines

- 모든 주요 예제는 Python으로 작성하고 실행 가능한 형태로 제공합니다.
- 그래프를 작성하기 전에 데이터 출처, 단위, 기간, 결측 여부를 확인합니다.
- 축 제목, 단위, 범례를 명확히 표시하고 불필요한 시각적 장식을 줄입니다.
- 그래프 유형과 축 범위가 데이터의 의미를 왜곡하지 않도록 검토합니다.
- 원본 데이터는 변경하지 않으며, 생성된 그래프와 가공 데이터는 필요에 따라 별도로 보관합니다.
- 학습자료에서 사용하는 그래프와 코드의 결과가 일치하도록 유지합니다.
- `examples/`와 `solutions/`을 구분하고, 연습문제는 `exercises/`에 제공합니다.
- Quiz 정답은 각 문항 아래의 접기·펼치기 형식으로 개별 확인할 수 있도록 구성합니다.
- 그래프의 특징과 한계, 결과를 해석할 때 주의할 점을 함께 설명합니다.

## References

- [Python Documentation](https://docs.python.org/3/)
- [NumPy Documentation](https://numpy.org/doc/stable/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/)
- [Matplotlib Tutorials](https://matplotlib.org/stable/tutorials/index.html)
- [Seaborn Documentation](https://seaborn.pydata.org/)
- [Plotly Python Documentation](https://plotly.com/python/)
- [Plotly Express](https://plotly.com/python/plotly-express/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit — Getting Started](https://docs.streamlit.io/get-started)
- [Jupyter — Installation](https://jupyter.org/install)

---

[← MoreStudy](../Readme.md) · [Data Processing](../Data_Processing/)
