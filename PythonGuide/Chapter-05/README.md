# Chapter 05. Conditional Statements

카페에서 주문을 받으려면 메뉴가 등록되어 있는지, 어떤 할인율을 적용할지, 손님이 낸 돈이 충분한지 차례대로 확인해야 합니다. 이번 챕터에서는 이러한 판단 기준을 파이썬 조건문으로 표현하고, 참과 거짓에 따라 실행할 코드를 다르게 선택하는 방법을 배웁니다.

## Contents

<table align="center">
  <thead>
    <tr><th>Section</th><th>주요 내용</th></tr>
  </thead>
  <tbody>
    <tr><td><a href="./5.1.Conditions.md">5.1. Conditions</a></td><td>비교 연산자와 <code>in</code>으로 참·거짓 판단하기</td></tr>
    <tr><td><a href="./5.2.If-and-Else.md">5.2. If &amp; Else</a></td><td>조건에 따라 실행할 코드 고르기와 들여쓰기</td></tr>
    <tr><td><a href="./5.3.Elif-and-Branch-Order.md">5.3. Elif &amp; Branch Order</a></td><td>여러 조건의 검사 순서와 경계값 확인하기</td></tr>
    <tr><td><a href="./5.4.Combining-Conditions.md">5.4. Combining Conditions</a></td><td><code>and</code>, <code>or</code>, <code>not</code>으로 조건 묶기</td></tr>
    <tr><td><a href="./5.5.Nested-Conditions.md">5.5. Nested Conditions</a></td><td>바깥 조건을 통과한 뒤 안쪽 조건 검사하기</td></tr>
  </tbody>
</table>

## Summary

- `if`는 조건이 참(`True`)일 때 들여쓴 코드 블록을 실행합니다. `else`는 앞선 조건을 만족하지 않았을 때 실행됩니다.
- `if`와 `elif`로 이어진 조건문은 위에서부터 차례대로 조건을 검사하여, 처음으로 참이 되는 분기 하나만 실행합니다.
- `and`는 두 조건이 모두 참일 때, `or`는 둘 중 하나 이상이 참일 때 전체 조건이 참이 됩니다. `not`은 참과 거짓을 반대로 뒤집습니다.
- `if` 블록 안에 작성한 중첩 조건문은 바깥쪽 조건이 참이어서 해당 블록에 진입했을 때만 검사합니다.

---

<p align="center">
  <a href="../Chapter-04/">← Chapter 04</a>
  &nbsp;·&nbsp;
  <a href="../README.md">Python Guide</a>
  &nbsp;·&nbsp;
  <a href="../Chapter-06/">Chapter 06 →</a>
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
  <img src="https://githubusercontent.com"
       width="90" alt="ONEUL">
</p>
