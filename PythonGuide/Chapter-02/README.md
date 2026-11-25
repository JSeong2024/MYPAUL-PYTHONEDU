# Chapter 02. Variables, Data Types & Operators

**변수, 자료형과 연산자**

프로그램에서는 숫자를 계산하거나 문장을 다루고, 계산한 결과를 나중에 다시 사용하기도 합니다. 이러한 작업을 하려면 값을 구분할 이름과 값을 계산하는 방법이 필요합니다.

이번 장에서는 **변수(Variable)**, **자료형(Data Type)**, **연산자(Operator)** 를 살펴봅니다. 아직 복잡한 프로그램을 만들지는 않지만, 이후에 배우는 조건문과 반복문, 함수 모두 이 내용을 바탕으로 사용합니다.

## Contents

<table align="center">
  <thead>
    <tr><th align="center">Section</th><th align="center">주요 내용</th></tr>
  </thead>
  <tbody>
    <tr><td align="left"><a href="./2.1.Variables-and-Assignment.md">2.1. Variables &amp; Assignment</a></td><td align="left">값에 이름 붙이기, 변수 이름 짓기, 여러 값 출력하기</td></tr>
    <tr><td align="left"><a href="./2.2.Data-Types.md">2.2. Data Types</a></td><td align="left">숫자·문자열·불리언과 <code>type()</code>으로 자료형 확인하기</td></tr>
    <tr><td align="left"><a href="./2.3.Arithmetic-Operators.md">2.3. Arithmetic Operators</a></td><td align="left">기본 계산, 나눗셈·몫·나머지, 계산 순서</td></tr>
    <tr><td align="left"><a href="./2.4.Comparison-and-Logical-Operators.md">2.4. Comparison &amp; Logical Operators</a></td><td align="left">두 값 비교하기와 여러 조건 판단하기</td></tr>
    <tr><td align="left"><a href="./2.5.Assignment-Operators-and-Expressions.md">2.5. Assignment Operators &amp; Expressions</a></td><td align="left">복합 대입 연산자와 표현식의 계산 결과</td></tr>
  </tbody>
</table>

## Summary

- **변수**는 값에 이름을 붙여 다시 사용할 수 있게 합니다. `=`은 대입, `==`은 비교에 사용합니다.
- 대표적인 **자료형**에는 정수 `int`, 실수 `float`, 문자열 `str`, 불리언 `bool`이 있습니다.
- `+`, `-`, `*`, `/`, `//`, `%`, `**`로 숫자를 계산합니다. 괄호를 사용하면 계산 순서를 분명하게 나타낼 수 있습니다.
- **비교 연산자**는 두 값을 비교하고, **논리 연산자**는 여러 조건을 함께 판단합니다.
- `+=`, `-=` 등의 **복합 대입 연산자**는 계산 결과를 같은 변수에 다시 대입할 때 사용합니다.

## Practice

- [Exercise & Mini Project](./Practice.md)
- [Solutions](./solutions/README.md)

## References

- [Python Tutorial — An Informal Introduction to Python](https://docs.python.org/3/tutorial/introduction.html)
- [Python Standard Library — Built-in Types](https://docs.python.org/3/library/stdtypes.html)
- [Python Language Reference — Expressions](https://docs.python.org/3/reference/expressions.html)
- [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/)

---

<p align="center">
  <a href="../Chapter-01/">← Chapter 01</a>
  &nbsp;·&nbsp;
  <a href="../README.md">Python Guide</a>
  &nbsp;·&nbsp;
  <a href="../Chapter-03/">Chapter 03 →</a>
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
