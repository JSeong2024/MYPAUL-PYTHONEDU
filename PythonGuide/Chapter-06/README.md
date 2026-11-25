# Chapter 06. Loops & Iteration

**반복문**

플레이리스트에서 노래 제목을 하나씩 출력하고, 여러 주문의 금액을 더해 봅니다. 이번 챕터에서는 같은 작업을 반복하는 방법을 배우고, 조건문을 함께 써서 필요한 값만 골라 처리하거나 별 모양을 그립니다.

## Contents

<table align="center">
  <thead>
    <tr><th align="center">Section</th><th align="center">주요 내용</th></tr>
  </thead>
  <tbody>
    <tr><td align="left"><a href="./6.1.Loops.md">6.1. Loops</a></td><td align="left">반복문을 쓰는 이유와 <code>for</code>·<code>while</code>을 고르는 기준</td></tr>
    <tr><td align="left"><a href="./6.2.For.md">6.2. For</a></td><td align="left">리스트에서 값을 하나씩 꺼내고 누적합 구하기</td></tr>
    <tr><td align="left"><a href="./6.3.Range.md">6.3. Range</a></td><td align="left">시작값·끝값·간격을 정하고 별 계단 그리기</td></tr>
    <tr><td align="left"><a href="./6.4.Loops-with-Conditions.md">6.4. Loops with Conditions</a></td><td align="left">조건을 만족하는 값만 골라 합계와 개수 구하기</td></tr>
    <tr><td align="left"><a href="./6.5.Loops-with-Data-Structures.md">6.5. Loops with Data Structures</a></td><td align="left">리스트와 딕셔너리에서 항목, 키, 값 꺼내기</td></tr>
    <tr><td align="left"><a href="./6.6.Nested-Loops-and-Patterns.md">6.6. Nested Loops &amp; Patterns</a></td><td align="left">행과 열을 차례로 돌며 별 패턴 그리기</td></tr>
    <tr><td align="left"><a href="./6.7.While.md">6.7. While</a></td><td align="left">조건을 다시 검사하며 입력받고 합계 구하기</td></tr>
    <tr><td align="left"><a href="./6.8.Loop-Control.md">6.8. Loop Control</a></td><td align="left"><code>break</code>로 끝내고 <code>continue</code>로 이번 차례 건너뛰기</td></tr>
  </tbody>
</table>

## Summary

- `for`는 리스트나 `range()` 등에서 값을 하나씩 꺼내며 반복합니다. `range()`의 끝값은 포함하지 않습니다.
- 합계나 개수를 기록하는 변수는 반복을 시작하기 전에 초기화합니다. 조건문을 반복문 안에 쓰면 필요한 값만 더하거나 셀 수 있습니다.
- 딕셔너리를 그대로 순회하면 키를 꺼냅니다. `values()`는 값을, `items()`는 키와 값의 쌍을 꺼낼 때 씁니다.
- 중첩 반복문에서는 바깥 반복문의 매 차례마다 안쪽 반복문을 실행합니다.
- `while`은 매 차례 조건을 검사하고, 조건이 참인 동안 반복합니다.
- `break`는 가장 가까운 반복문을 끝냅니다. `continue`는 이번 차례의 남은 코드를 건너뜁니다.

## Practice

- [Exercise & Mini Project](./Practice.md) — 짝수의 합과 개수, 별 패턴, 메뉴 출력, 주문 금액 집계
- [Solutions](./solutions/README.md) — 연습문제와 미니 프로젝트 풀이

---

<p align="center">
  <a href="../Chapter-05/">← Chapter 05</a>
  &nbsp;·&nbsp;
  <a href="../README.md">Python Guide</a>
  &nbsp;·&nbsp;
  <a href="../Chapter-07/">Chapter 07 →</a>
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
