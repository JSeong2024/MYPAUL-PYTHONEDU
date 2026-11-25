# Chapter 08. Fundamentals Project

**기초 종합 프로젝트**

지금까지 배운 자료구조, 조건문, 반복문, 함수를 종합적으로 활용하여 카페 주문 프로그램을 만들어 봅니다. 여러 메뉴를 연속으로 주문받고, 전체 주문 합계와 할인액을 계산하여 결제가 완료되면 영수증을 출력합니다.

주문 한 건을 기록하는 기능부터 시작하여 여러 건의 주문을 처리할 수 있도록 프로그램을 단계적으로 확장합니다. 마지막에는 프로그램을 기능별 함수로 구성하고, 다양한 입력 조건에서 올바르게 동작하는지 검증합니다.

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
      <td align="left"><a href="./8.1.Project-Overview.md">8.1. Project Overview</a></td>
      <td align="left">프로젝트의 목표, 완성 화면 및 주문·결제 규칙</td>
    </tr>
    <tr>
      <td align="left"><a href="./8.2.Menu-and-Order-Records.md">8.2. Menu and Order Records</a></td>
      <td align="left">메뉴판 구성, 주문 기록 저장 및 주문 금액 계산</td>
    </tr>
    <tr>
      <td align="left"><a href="./8.3.Taking-Multiple-Orders.md">8.3. Taking Multiple Orders</a></td>
      <td align="left">반복문을 활용한 주문 입력, 입력값 검사 및 주문 종료</td>
    </tr>
    <tr>
      <td align="left"><a href="./8.4.Payment-and-Receipt.md">8.4. Payment and Receipt</a></td>
      <td align="left">주문 합계와 할인액 계산, 결제 확인 및 영수증 출력</td>
    </tr>
    <tr>
      <td align="left"><a href="./8.5.Organizing-and-Testing.md">8.5. Organizing and Testing</a></td>
      <td align="left">함수를 활용한 기능 분해, 리팩터링 및 프로그램 검증</td>
    </tr>
  </tbody>
</table>

## Summary

- **딕셔너리**(**Dictionary**)에 메뉴 이름과 단가를 키와 값의 형태로 저장하면 메뉴 이름을 통해 가격을 조회할 수 있습니다.
- 메뉴 이름, 수량, 단가를 하나의 **튜플**(**Tuple**)로 구성하고, `append()` 메서드를 사용하여 여러 건의 주문 기록을 **리스트**(**List**)에 추가할 수 있습니다.
- `while True`를 사용하여 주문을 반복해서 입력받습니다. 잘못된 입력은 `continue` 문으로 건너뛰고, 주문 종료 조건을 만족하면 `break` 문으로 반복문을 종료합니다.
- `for` 문과 **언패킹**(**Unpacking**)을 활용하여 각 주문 기록에서 메뉴 이름, 수량, 단가를 꺼내고 주문 금액을 누적합니다.
- `if-elif-else` 문으로 주문 합계에 따른 할인율을 결정하고, `//` 연산자를 활용하여 할인액의 1원 미만 단위를 버립니다. 조건의 범위가 겹치는 경우에는 조건을 검사하는 순서에 주의해야 합니다.
- 받은 돈과 최종 결제 금액을 비교하여 결제 가능 여부를 판단합니다. 결제가 가능하면 거스름돈을 계산하고 영수증을 출력하며, 받은 돈이 부족하면 부족한 금액을 안내합니다.
- 주문 입력, 주문 합계 계산, 할인액 계산, 영수증 출력 등의 기능을 함수로 분리하고, 매개변수와 반환값을 활용하여 함수 사이에서 데이터를 전달합니다.
- `main()` 함수에서 각 기능을 담당하는 함수를 호출하여 프로그램의 전체 실행 흐름을 관리합니다. 값 없이 `return` 문을 사용하면 현재 함수의 실행을 일찍 종료할 수 있습니다.
- 기존 기능을 유지하면서 코드의 구조를 개선하는 작업을 **리팩터링**(**Refactoring**)이라고 합니다. 프로그램을 기능별로 나누면 코드의 가독성과 유지보수성을 높일 수 있습니다.
- 정상적인 입력뿐만 아니라 잘못된 입력, 빈 데이터, **경계값**(**Boundary Value**)과 그 주변의 값도 사용하여 프로그램을 검증합니다. 함수로 구성된 프로그램은 개별 기능을 독립적으로 검증할 수도 있습니다.

---

<p align="center">
  <a href="../Chapter-07/">← Chapter 07</a>
  &nbsp;·&nbsp;
  <a href="../README.md">Python Guide</a>
  &nbsp;·&nbsp;
  <a href="../Chapter-09/">Chapter 09 →</a>
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
