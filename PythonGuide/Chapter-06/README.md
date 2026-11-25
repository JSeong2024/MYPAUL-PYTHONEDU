# Chapter 06. Loops & Iteration

**반복문**

플레이리스트에 저장된 노래 제목을 하나씩 출력하거나 여러 건의 주문 금액을 차례로 더하는 작업처럼, 프로그램에서는 동일한 작업을 여러 번 수행해야 하는 경우가 있습니다.

이번 챕터에서는 `for` 문과 `while` 문을 사용하여 반복 작업을 효율적으로 처리하는 방법을 배웁니다. 또한 반복문과 조건문을 함께 사용하여 원하는 조건을 만족하는 데이터만 처리하고, 중첩 반복문을 활용하여 다양한 모양의 패턴을 그려 봅니다. 마지막으로 `break`와 `continue`를 사용하여 반복문의 실행 흐름을 제어하는 방법을 알아봅니다.

## Contents

<table align="center">
  <thead>
    <tr>
      <th align="center">Section</th>
      <th align="center">주요 내용</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="left"><a href="./6.1.Loops.md">6.1. Loops</a></td>
      <td align="left">반복문의 개념과 <code>for</code> 문, <code>while</code> 문의 차이</td>
    </tr>
    <tr>
      <td align="left"><a href="./6.2.For.md">6.2. For</a></td>
      <td align="left"><code>for</code> 문의 기본 구조, 리스트 순회 및 누적합 계산</td>
    </tr>
    <tr>
      <td align="left"><a href="./6.3.Range.md">6.3. Range</a></td>
      <td align="left"><code>range()</code>의 시작값, 끝값, 간격 설정 및 계단 모양 그리기</td>
    </tr>
    <tr>
      <td align="left"><a href="./6.4.Loops-with-Conditions.md">6.4. Loops with Conditions</a></td>
      <td align="left">반복문과 조건문을 활용한 데이터 선택, 합계 및 개수 계산</td>
    </tr>
    <tr>
      <td align="left"><a href="./6.5.Loops-with-Data-Structures.md">6.5. Loops with Data Structures</a></td>
      <td align="left">리스트와 딕셔너리 순회, 키와 값의 활용</td>
    </tr>
    <tr>
      <td align="left"><a href="./6.6.Nested-Loops-and-Patterns.md">6.6. Nested Loops &amp; Patterns</a></td>
      <td align="left">중첩 반복문의 실행 구조, 행과 열의 탐색 및 패턴 그리기</td>
    </tr>
    <tr>
      <td align="left"><a href="./6.7.While.md">6.7. While</a></td>
      <td align="left"><code>while</code> 문의 기본 구조, 반복적인 사용자 입력 및 무한 반복</td>
    </tr>
    <tr>
      <td align="left"><a href="./6.8.Loop-Control.md">6.8. Loop Control</a></td>
      <td align="left"><code>break</code>와 <code>continue</code>를 활용한 반복문의 실행 흐름 제어</td>
    </tr>
  </tbody>
</table>

## Summary

- **반복문**(**Loop**)은 특정 코드를 일정한 규칙에 따라 반복해서 실행하기 위한 제어문입니다. Python에서는 `for` 문과 `while` 문을 사용합니다.

- `for` 문은 리스트, 딕셔너리, 문자열, `range()` 등 순회할 수 있는 대상으로부터 항목을 하나씩 꺼내 처리합니다. 더 이상 꺼낼 항목이 없으면 반복을 종료합니다.

- `range()`는 일정한 규칙을 따르는 정수의 범위를 지정할 때 사용합니다. 시작값, 끝값, 간격을 설정할 수 있으며, 끝값은 범위에 포함되지 않습니다.

- 합계나 개수를 누적하여 기록하는 변수는 반복을 시작하기 전에 초기화합니다. 반복문과 조건문을 함께 사용하면 원하는 조건을 만족하는 값만 선택하여 합계나 개수를 구할 수 있습니다.

- 자료구조에 저장된 항목을 하나씩 방문하는 과정을 **순회**(**Traversal**)라고 합니다. 리스트를 순회하면 저장된 항목을 순서대로 꺼내고, 딕셔너리를 그대로 순회하면 **키**(**Key**)를 하나씩 꺼냅니다.

- 딕셔너리에서 **값**(**Value**)만 필요할 때는 `values()`를 사용하고, 키와 값이 모두 필요할 때는 `items()`를 사용합니다. `items()`를 순회하면서 꺼낸 키와 값의 쌍은 언패킹을 통해 각각의 변수에 나누어 저장할 수 있습니다.

- 반복문 안에 또 다른 반복문을 작성하는 구조를 **중첩 반복문**(**Nested Loop**)이라고 합니다. 별도의 반복 제어가 없다면 바깥 반복문이 한 번 반복될 때마다 안쪽 반복문은 처음부터 끝까지 실행됩니다.

- `while` 문은 새로운 반복을 시작하기 전에 조건식을 평가하고, 조건이 참인 동안 반복문 내부의 코드를 실행합니다. 조건이 처음부터 거짓이라면 반복문 내부의 코드는 한 번도 실행되지 않습니다.

- 반복문이 종료되지 않고 계속 실행되는 것을 **무한 반복**(**Infinite Loop**)이라고 합니다. `while` 문을 작성할 때는 조건식에 사용되는 변수의 값이 적절하게 변경되는지 확인해야 합니다.

- `break`는 자신을 직접 감싸고 있는 가장 안쪽 반복문을 즉시 종료합니다. `continue`는 현재 반복에서 아직 실행하지 않은 코드를 건너뛰고 다음 반복 단계로 이동합니다.

- `while True`와 `break`를 함께 사용하면 반복문 내부에서 종료 조건을 검사하여 원하는 시점에 반복을 종료할 수 있습니다.

> `for` 문과 `while` 문은 모두 반복 작업을 처리할 수 있지만, 반복을 진행하는 기준에 차이가 있습니다. 자료의 항목을 순서대로 처리하거나 일정한 횟수만큼 반복할 때는 `for` 문이 편리하고, 사용자 입력이나 프로그램의 상태에 따라 반복 여부를 결정할 때는 `while` 문이 적합합니다.

## Practice

Chapter 06에서 배운 반복문과 조건문을 활용하여 다양한 문제를 해결해 보세요. 종합 실습을 통해 반복문의 기본 구조와 실행 흐름을 익히고, 미니 프로젝트를 통해 여러 개념을 하나의 프로그램에 적용해 봅시다.

- [Exercise & Mini Project](./Practice.md) — 짝수의 합과 개수 구하기, 가운데 정렬 피라미드 그리기, 판매 가능한 메뉴 골라 출력하기, 카페 주문 금액 집계하기
- [Solutions](./solutions/README.md) — 종합 실습 및 미니 프로젝트의 예제 풀이와 해설

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
