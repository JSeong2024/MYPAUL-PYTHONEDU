# Chapter 03. Input, Output & String Formatting

**입력, 출력과 문자열 포매팅**

지난 장에서는 변수에 값을 저장하고 계산하는 방법을 배웠습니다. 하지만 상품의 가격이나 수량을 코드에 미리 적어 두면, 다른 값을 계산할 때마다 코드를 수정해야 합니다.

이번 장에서는 프로그램을 실행하는 사람이 값을 직접 입력하고, 계산 결과를 읽기 좋은 형태로 출력하는 방법을 살펴봅니다. Python에서 입력과 출력에 사용하는 기본 함수인 `input()`과 `print()`, 자료형 변환, f-string을 차례대로 다룹니다.

## Contents

<table align="center">
  <thead>
    <tr><th align="center">Section</th><th align="center">주요 내용</th></tr>
  </thead>
  <tbody>
    <tr><td align="left"><a href="./3.1.Output.md">3.1. Output</a></td><td align="left"><code>print()</code>로 여러 값 출력하기, 구분자와 줄바꿈</td></tr>
    <tr><td align="left"><a href="./3.2.Input.md">3.2. Input</a></td><td align="left"><code>input()</code>으로 입력받고 반환값 확인하기</td></tr>
    <tr><td align="left"><a href="./3.3.Type-Conversion.md">3.3. Type Conversion</a></td><td align="left"><code>int()</code>, <code>float()</code>, <code>str()</code>로 변환하기</td></tr>
    <tr><td align="left"><a href="./3.4.String-Formatting.md">3.4. String Formatting</a></td><td align="left">f-string으로 변수, 소수점 자리, 천 단위 쉼표 표시하기</td></tr>
    <tr><td align="left"><a href="./3.5.Input-to-Output.md">3.5. Input to Output</a></td><td align="left">입력, 계산, 출력을 하나의 코드로 연결하기</td></tr>
  </tbody>
</table>

## Summary

- `print()`는 문자열, 숫자, 변수의 값을 출력합니다. `sep`과 `end`로 값 사이의 구분자와 출력 끝 문자를 조절할 수 있습니다.
- `input()`은 키보드 입력을 받아 **문자열(`str`)** 로 돌려줍니다.
- 숫자를 계산하려면 필요에 따라 `int()`나 `float()`로 변환합니다. `str()`은 값을 문자열로 바꿀 때 사용합니다.
- f-string은 문자열 안에 변수나 계산 결과를 넣어 출력할 수 있게 합니다.
- `:.2f`는 소수점 아래 두 자리, `:,`는 세 자리마다 쉼표를 넣는 출력 형식입니다.

## Practice

- [Exercise & Mini Project](./Practice.md)
- [Solutions](./solutions/README.md)

## References

- [Python Documentation — Built-in Functions](https://docs.python.org/3/library/functions.html)
- [Python Tutorial — Input and Output](https://docs.python.org/ko/3.15/tutorial/inputoutput.html)
- [Python Language Reference — Formatted String Literals](https://docs.python.org/3/reference/lexical_analysis.html#f-strings)
- [Python Documentation — Format Specification Mini-Language](https://docs.python.org/3/library/string.html#format-specification-mini-language)

---

<p align="center">
  <a href="../Chapter-02/">← Chapter 02</a>
  &nbsp;·&nbsp;
  <a href="../README.md">Python Guide</a>
  &nbsp;·&nbsp;
  <a href="../Chapter-04/">Chapter 04 →</a>
</p>

<p align="center">
  <sub>© 2025–2026 Choi Jae-Seong · ONEUL</sub>
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
