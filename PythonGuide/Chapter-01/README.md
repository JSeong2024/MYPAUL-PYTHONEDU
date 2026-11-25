# Chapter 01. Introduction to Python

**파이썬 소개**

## 1.1. 파이썬이란?

**파이썬**(**Python**)은 컴퓨터에게 할 일을 코드로 적어 전달할 수 있는 프로그래밍 언어입니다. 계산을 하거나 반복되는 작업을 자동화할 때 쓸 수 있고, 데이터를 분석하거나 인공지능 프로그램을 만들 때도 사용합니다. 이 챕터에서는 파이썬으로 화면에 짧은 인사를 출력해 봅니다.

## 1.2. 개발 환경 준비하기

1. [Python 다운로드](https://www.python.org/downloads/)에서 운영체제에 맞는 Python 3을 설치합니다.
2. [Visual Studio Code](https://code.visualstudio.com/)를 설치한 뒤, 확장 메뉴에서 Microsoft의 **Python** 확장을 설치합니다.
3. VS Code에서 명령 팔레트를 열고 **Python: Select Interpreter**를 선택합니다. 목록에서 설치한 Python 3을 고릅니다.

> VS Code는 코드를 작성하는 편집기입니다. 작성한 코드를 읽고 실행하는 프로그램을 **파이썬 인터프리터**(**Python Interpreter**)라고 합니다.

## 1.3. 첫 프로그램 실행하기

VS Code에서 `hello.py` 파일을 만들고 아래 코드를 저장합니다. 오른쪽 위의 **Run Python File** 버튼을 눌러 실행합니다.

```python
print(f"Hello, World!")
```

**실행 결과**

```text
Hello, World!
```

`print()`는 괄호 안의 내용을 화면에 출력합니다. 따옴표 안의 문장을 바꿔 `print(f"안녕하세요!")`를 실행해 보세요. 결과는 VS Code 아래쪽 터미널에서 볼 수 있습니다.

> 따옴표 앞에 `f`를 붙인 문자열을 **f-string**이라고 합니다. 챕터 3에서는 f-string에 변수의 값을 넣어 봅니다.

## References

- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Getting Started with Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial)

---

<p align="center">
  <a href="../README.md">Python Guide</a>
  &nbsp;·&nbsp;
  <a href="../Chapter-02/">Chapter 02 →</a>
</p>

<p align="center">
  <sub>© 2026 Choi Jae-Seong · ONEUL</sub>
  <br>
  <sub>
    Educational Content ·
    <a href="../../LICENSE-CONTENT.md">CC BY-NC 4.0</a>
  </sub>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/JSeong2024/oneul/main/.github/assets/logo_ONEUL_01.png"
       width="90" alt="ONEUL">
</p>
