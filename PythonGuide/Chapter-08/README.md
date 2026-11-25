# Chapter 08. Fundamentals Project

**기초 종합 프로젝트**

카페에서 여러 메뉴를 주문받아 합계와 할인액을 계산하고, 결제가 끝나면 영수증을 출력하는 프로그램을 만듭니다. 주문 한 건을 기록하는 코드부터 시작해 여러 건을 처리하도록 확장한 뒤, 작업을 함수로 나눕니다.

## Contents

<table align="center">
  <thead>
    <tr><th align="center">Section</th><th align="center">주요 내용</th></tr>
  </thead>
  <tbody>
    <tr><td align="left"><a href="./8.1.Project-Overview.md">8.1. Project Overview</a></td><td align="left">완성 화면과 주문·결제 규칙 확인하기</td></tr>
    <tr><td align="left"><a href="./8.2.Menu-and-Order-Records.md">8.2. Menu and Order Records</a></td><td align="left">메뉴판을 만들고 주문 한 건 기록하기</td></tr>
    <tr><td align="left"><a href="./8.3.Taking-Multiple-Orders.md">8.3. Taking Multiple Orders</a></td><td align="left">반복문으로 여러 주문을 받고 잘못된 입력 건너뛰기</td></tr>
    <tr><td align="left"><a href="./8.4.Payment-and-Receipt.md">8.4. Payment and Receipt</a></td><td align="left">합계와 할인을 계산하고 영수증 출력하기</td></tr>
    <tr><td align="left"><a href="./8.5.Organizing-and-Testing.md">8.5. Organizing and Testing</a></td><td align="left">코드를 함수로 나누고 입력을 바꾸어 결과 확인하기</td></tr>
  </tbody>
</table>

## Summary

- 메뉴판은 딕셔너리에 담고, 메뉴 이름·수량·단가를 묶은 주문 기록은 리스트에 저장합니다.
- `while`로 주문을 반복해서 받습니다. `continue`로 미등록 메뉴나 수량이 1 미만인 주문을 건너뛰고, 메뉴 이름에 `0`을 입력하면 `break`로 주문을 마칩니다.
- `for`로 주문 금액을 더하고, 조건문으로 할인율과 결제 가능 여부를 판단합니다.
- 주문 입력, 금액 계산, 영수증 출력을 함수로 나누고, 입력을 바꾸어 결과를 확인합니다.

---

<p align="center">
  <a href="../Chapter-07/">← Chapter 07</a>
  &nbsp;·&nbsp;
  <a href="../README.md">Python Guide</a>
  &nbsp;·&nbsp;
  <a href="../Chapter-09/">Chapter 09 →</a>
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
