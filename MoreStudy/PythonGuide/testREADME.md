<div align="center">

# Python Guide

**From Fundamentals to Real-World Applications**

Python의 핵심 문법부터 프로그램 설계와 실전 응용까지 단계적으로 학습하는 가이드북입니다.  
개념을 이해하고, 코드를 직접 작성하며, 실제 문제를 해결하는 능력을 기르는 데 중점을 둡니다.

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Levels-Basic%20%7C%20Intermediate%20%7C%20Applied-0F766E?style=flat-square" alt="Basic, Intermediate, Applied">
  <img src="https://img.shields.io/badge/Status-In%20Development-64748B?style=flat-square" alt="In Development">
</p>

[교육과정](#contents) · [학습 방식](#learning-materials) · [프로젝트](#mini-project) · [시작하기](#getting-started)

</div>

---

## Overview

Python의 문법을 단순히 암기하는 것보다, **코드가 어떻게 동작하는지 이해하고 필요한 기능을 직접 구현하는 것**을 목표로 합니다.

- **Basic:** 변수와 연산자부터 자료구조, 조건문, 반복문, 함수까지 프로그래밍의 기초 학습
- **Intermediate:** 파일 처리, 객체지향 프로그래밍, 자료구조·알고리즘, 모듈화와 테스트를 통한 설계 능력 강화
- **Applied:** 자동화, API, 실시간 데이터 처리 등 실제 프로그램 개발과 분야별 응용

각 Chapter는 독립적인 학습 단위로 구성하며, 핵심 개념과 실행 예제 뒤에 요약, 연습문제 및 코딩 프로젝트를 배치합니다. 본문에서 다룬 내용만으로 문제를 해결할 수 있도록 선수 학습 범위를 고려합니다.

> **제작 상태:** 해당 가이드북은 제작 중입니다. 아래 Contents는 **전체 교육과정의 계획안**이고 Chapter와 실습 자료는 완성되는 순서대로 공개합니다.

## Contents

### Part 1 — Python Fundamentals · Basic

Python의 기본 문법을 익히고, 자료구조·조건문·반복문·함수를 결합하여 간단한 프로그램을 직접 작성합니다.

| Chapter | Topic | 주요 학습 내용 |
|:---:|---|---|
| 01 | **Introduction to Python** | Python 소개, 개발 환경, 첫 프로그램 실행 |
| 02 | **Variables, Data Types & Operators** | 변수, 기본 자료형, 산술·비교·논리 연산자 |
| 03 | **Input, Output & String Formatting** | `print()`, `input()`, 형 변환, f-string |
| 04 | **Python Data Structures** | List, Tuple, Dictionary, Set, 자료 접근과 수정 |
| 05 | **Conditional Statements** | `if`, `elif`, `else`, 조건식과 중첩 조건문 |
| 06 | **Loops & Iteration** | `for`, `while`, `range()`, 반복 제어 |
| 07 | **Functions & User-Defined Functions** | `def`, 매개변수, 반환값, 변수 범위, 함수 분리 |
| 08 | **Fundamentals Project** | 자료구조·조건문·반복문·함수를 활용한 종합 프로젝트 |

**핵심 학습 범위:** Chapter 04~07. 기본 자료구조와 제어문, 함수를 정확히 이해하는 데 충분한 예제와 실습을 배치합니다.

### Part 2 — Python Programming · Intermediate

문법을 활용하는 수준에서 나아가, 프로그램의 구조를 설계하고 기존 코드를 읽고 개선하는 능력을 기릅니다.

| Chapter | Topic | 주요 학습 내용 |
|:---:|---|---|
| 09 | **Pythonic Code & Sequences** | 슬라이싱, Unpacking, Comprehension, `enumerate()`, `zip()` |
| 10 | **File I/O & Path Management** | `pathlib`, 텍스트·CSV·JSON 파일 입출력 |
| 11 | **Modules, Packages & Environments** | `import`, 패키지, `pip`, `venv`, 프로젝트 구성 |
| 12 | **Exceptions & Debugging** | 예외 처리, 오류 추적, 디버깅 |
| 13 | **Object-Oriented Programming** | Class, 객체, 메서드, 상속, 합성 |
| 14 | **Data Structures & Collections** | Stack, Queue, Heap, Hash, `deque`, `heapq` |
| 15 | **Algorithms & Problem Solving** | 정렬·탐색, 재귀, DFS, BFS, 동적 계획법(DP) 입문 |
| 16 | **NumPy & Pandas Essentials** | 배열, DataFrame, 데이터 선택과 기본 집계 |
| 17 | **Matplotlib Essentials** | Figure, Axes, Subplots, 그래프 작성과 저장 |
| 18 | **Testing & Code Quality** | 테스트, Type Hints, Logging, 코드 품질 |
| 19 | **Intermediate Project** | 파일·객체·알고리즘을 결합한 종합 프로그램 |

Comprehension과 같은 축약 표현은 사용 자체를 목표로 하지 않습니다. **기존 코드를 읽고 해석하며, 상황에 맞게 가독성 높은 구현을 선택하는 능력**을 중점적으로 다룹니다.

NumPy·Pandas·Matplotlib는 기본 활용에 집중하고, 심화 내용은 별도의 전문 학습 자료로 연결합니다.

### Part 3 — Applied Python & Projects · Applied

실제 데이터를 입력받고 외부 시스템과 연동하며, 실행 가능한 프로그램으로 완성하는 과정을 다룹니다.

| Chapter | Topic | 주요 학습 내용 |
|:---:|---|---|
| 20 | **Automation & Scripting** | 반복 작업 자동화, 파일 관리, 스크립트 실행 |
| 21 | **API & Database Integration** | HTTP, REST API, JSON, SQLite |
| 22 | **Real-Time & Event-Driven Programming** | 이벤트 처리, 스레드, `asyncio`, 실시간 데이터 수신 |
| 23 | **Application Design & Integration** | 모듈 연결, 설정 관리, 오류 처리, 실행·배포 기초 |
| 24 | **Applied Python Project** | 외부 데이터 수집부터 처리·저장·출력까지 종합 구현 |

여기서의 실시간 처리는 하드 실시간 시스템보다 **이벤트 기반·준실시간 응용 프로그램**에 중점을 둡니다. 분야별 전문 내용은 아래 연계 자료에서 확장합니다.

## Learning Path

```text
Part 1 · Basic
기본 문법 · 자료구조 · 조건문 · 반복문 · 함수
                  │
                  ▼
Part 2 · Intermediate
파일 처리 · OOP · 알고리즘 · 모듈화 · 테스트
                  │
                  ▼
Part 3 · Applied
자동화 · API · 실시간 처리 · 응용 프로그램 제작
                  │
                  ▼
             Specialized Topics
데이터 · 시각화 · AI · 컴퓨터 비전 · 로봇 · 자율주행
```

Part 1과 Part 2는 순서대로 학습하는 것을 권장합니다. Part 3 이후에는 관심 분야와 필요한 선수 지식에 따라 전문 학습 자료를 선택할 수 있습니다.

### Related Learning Materials

| 분야 | 자료 | 학습 범위 |
|---|---|---|
| 데이터 처리 | [Data Processing](../Data_Processing/) | 데이터 수집·정제·변환 및 처리 자동화 |
| 데이터 시각화 | [Data Visualization](../Data_Visualization/) | Matplotlib, Seaborn, Plotly, 대시보드 |
| 인공지능 | [Artificial Intelligence](../AI/) | 머신러닝, 딥러닝, PyTorch 및 AI 응용 |
| 컴퓨터 비전 | [Computer Vision](../Computer_Vision/) | 영상·이미지 처리 및 객체 인식 |
| 로봇 공학 | [Robotics](../Robotics/) | 센서, 제어 및 로봇 프로그래밍 |
| 자율주행 | [Autonomous Driving](../Autonomous_Driving/) | 경로 계획, 인지 및 시뮬레이션 |

위 자료는 각각 독립된 학습 영역이며, 제작 진행 상태와 실제 수록 내용은 해당 디렉터리에서 확인할 수 있습니다.

## Learning Materials

각 Chapter는 아래 구성에 따라 작성합니다. 개념의 중요도와 난이도에 따라 예제·연습문제·프로젝트 수는 달라질 수 있습니다.

| 구성 | 내용 |
|---|---|
| **Concepts** | 핵심 개념, 문법, 사용 목적 및 주의사항 |
| **Examples** | 실행 가능한 예제 코드, 실행 결과 및 해설 |
| **Summary** | Chapter의 핵심 내용 요약 |
| **Exercise** | 객관식·주관식, 코드 해석 및 오류 수정 |
| **Mini Project** | 직접 구현하는 코딩 과제, 요구사항과 검증 기준 |
| **Solutions** | Exercise 정답과 해설, 프로젝트 힌트·모범 코드·검증 |

Chapter 본문 중간에도 필요한 경우 간단한 Quiz나 Coding Practice를 배치합니다. **정답 및 해설은 학습 본문과 분리**하여 문제를 먼저 해결할 수 있도록 구성합니다.

### Mini Project

| Level | 목표 | 기준 |
|---|---|---|
| **Basic** | 개념 확인 | 학습한 문법으로 단순한 기능 구현 |
| **Advanced** | 개념 응용 | 여러 개념 결합, 추가 조건 및 입력 처리 |
| **Professional** | 실무형 문제 해결 | 실제 사용 상황, 데이터 검증, 예외·경계 조건 처리 |
| **Challenge** | 종합 문제 해결 | 복합 요구사항, 까다로운 제약과 효율성 검토 |

모든 Chapter에 네 가지 난이도를 의무적으로 배치하지 않습니다. **문제의 현실성, 구현 범위, 제약조건, 학습 목표**를 고려하여 필요한 난이도만 선택합니다. 아직 학습하지 않은 문법이나 라이브러리를 필수로 요구하지 않는 것을 원칙으로 합니다.

### Exercise & Project Solutions

- **Exercise Solutions:** 객관식 정답, 주관식 모범답안, 코드 분석 및 오류 수정 해설
- **Project Hints:** 풀이 방향을 스스로 찾을 수 있도록 단계별 힌트 제공
- **Project Solutions:** 독립 실행 가능한 모범 코드와 구현 설명
- **Validation & Review:** 테스트 입력, 예상 결과, 경계 조건 및 대안 구현 검토

프로젝트는 가급적 **문제 설명 → 요구사항 → 입력·출력 → 제약조건 → 실행 예시 → 검증 기준**의 순서로 작성합니다.

## Getting Started

### 1. Development Environment

- **언어:** Python 3
- **에디터:** Visual Studio Code 권장
- **운영체제:** Windows, macOS, Linux
- **외부 라이브러리:** 필요한 Chapter에서 별도 안내

Python과 VS Code의 설치 방법은 공식 사이트를 참고합니다.

- [Download Python](https://www.python.org/downloads/)
- [Visual Studio Code — Python](https://code.visualstudio.com/docs/languages/python)

설치 후 터미널에서 Python 버전을 확인합니다.

```bash
python --version
```

환경에 따라 Windows에서는 `py --version`, macOS·Linux에서는 `python3 --version`이 필요할 수 있습니다.

### 2. Run a Python Program

다음 내용을 `hello.py`로 저장합니다.

```python
name = "Python"
print(f"Hello, {name}!")
```

터미널에서 실행합니다.

```bash
python hello.py
```

**실행 결과**

```text
Hello, Python!
```

### 3. Virtual Environments

외부 패키지를 사용하는 과정에서는 프로젝트별 가상환경을 권장합니다.

```bash
python -m venv .venv
```

| 환경 | 활성화 명령 |
|---|---|
| Windows PowerShell | `.\.venv\Scripts\Activate.ps1` |
| Windows Command Prompt | `.venv\Scripts\activate.bat` |
| macOS / Linux | `source .venv/bin/activate` |

가상환경을 종료할 때는 `deactivate`를 사용합니다. `.venv/`는 Git에 업로드하지 않습니다. Windows의 경우 명령 실행 환경에 따라 `python` 대신 `py`, macOS·Linux에서는 `python3`를 사용해야 할 수 있습니다.

## Editorial & Code Guidelines

- 개념과 코드를 함께 설명하되, 학문적인 세부 이론보다 **정확한 이해와 구현 능력**에 중점을 둡니다.
- 문장은 자연스럽고 간결한 경어체로 작성하며, 기술 용어의 영어·한국어 표기를 일관되게 유지합니다.
- 예제와 모범 코드는 직접 작성하고, 실제 실행 결과 및 경계 조건을 검증합니다.
- f-string을 기본적인 문자열 출력 방식으로 권장하되, 용도에 따라 다른 방식도 함께 설명합니다.
- 축약된 표현보다 가독성이 중요한 상황에서는 명시적인 코드를 우선합니다.
- 예제와 프로젝트에서는 해당 Chapter까지 학습한 내용을 우선 활용합니다.
- 원본 데이터와 생성 결과물을 구분하고, 경로 처리에는 필요한 경우 `pathlib`를 사용합니다.
- 설치 환경과 패키지 의존성은 해당 Chapter에서 구체적으로 안내합니다.

## References & Copyright

본 문서는 향후 PDF 및 출판물로 활용할 가능성을 고려하여 작성합니다. 개념 설명과 예제 코드는 원칙적으로 독자적으로 작성하고, 외부 저작물을 활용할 경우 **출처뿐 아니라 라이선스 및 이용 허락 조건**을 확인합니다.

- **References:** 참고한 공식 문서, 책, 논문, 웹 자료의 서지 정보를 기록합니다.
- **Third-Party Notices:** 외부 코드, 이미지, 도표, 폰트 등 실제로 사용한 제3자 자료의 권리자와 라이선스를 기록합니다.
- **Attribution:** 필요한 인용·변경·라이선스 고지는 해당 자료의 조건에 따라 표시합니다.
- **Publication:** 공개 저장소에 올린다는 사실만으로 외부 저작물의 재배포·상업적 이용이 허용되는 것은 아닙니다.

**주요 공식 참고자료**

- [Python Documentation](https://docs.python.org/3/)
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Python Standard Library](https://docs.python.org/3/library/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/)

참고자료에 포함된 문장·코드·이미지 등을 그대로 사용할 때에는 각 자료의 라이선스를 별도로 확인합니다. **이 가이드북 자체의 배포·재사용 라이선스는 추후 확정**하며, 별도 고지가 없는 상태에서 자유로운 재사용을 허용하는 것으로 해석하지 않습니다.

---

<div align="center">

[← MoreStudy](../README.md)

</div>
