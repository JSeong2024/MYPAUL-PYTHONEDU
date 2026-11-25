# Chapter 07. Functions

**함수**

함수의 개념과 필요성을 이해하고, 함수를 직접 정의하고 호출하는 방법을 알아봅니다. 매개변수와 인수를 활용하여 함수에 필요한 값을 전달하고, 반환값을 다른 연산에 활용하는 방법을 학습합니다. 또한 지역 변수와 전역 변수의 차이를 이해하고, 프로그램을 기능별로 나누어 사칙연산 계산기를 완성해 봅니다.

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
      <td align="left"><a href="./7.1.Functions.md">7.1. Functions</a></td>
      <td align="left">함수의 개념과 필요성, 내장 함수와 사용자 정의 함수</td>
    </tr>
    <tr>
      <td align="left"><a href="./7.2.Defining-and-Calling-Functions.md">7.2. Defining and Calling Functions</a></td>
      <td align="left"><code>def</code>를 사용한 함수 정의와 호출</td>
    </tr>
    <tr>
      <td align="left"><a href="./7.3.Parameters-and-Arguments.md">7.3. Parameters and Arguments</a></td>
      <td align="left">매개변수와 인수의 차이, 인수의 전달 순서와 개수</td>
    </tr>
    <tr>
      <td align="left"><a href="./7.4.Return-Values.md">7.4. Return Values</a></td>
      <td align="left"><code>print()</code>와 <code>return</code>의 차이, 반환값의 활용</td>
    </tr>
    <tr>
      <td align="left"><a href="./7.5.Variable-Scope.md">7.5. Variable Scope</a></td>
      <td align="left">변수의 유효 범위, 지역 변수와 전역 변수</td>
    </tr>
    <tr>
      <td align="left"><a href="./7.6.Organizing-Code-with-Functions.md">7.6. Organizing Code with Functions</a></td>
      <td align="left">함수 내부에서 다른 함수 호출하기, 기능 분해와 사칙연산 계산기</td>
    </tr>
  </tbody>
</table>

## Summary

- **함수**(**Function**)는 특정 작업을 수행하도록 구성한 코드의 단위입니다. 함수를 활용하면 코드를 재사용하고 프로그램을 기능별로 구성할 수 있습니다.
- **내장 함수**(**Built-in Function**)는 Python에서 기본적으로 제공하는 함수이며, **사용자 정의 함수**(**User-Defined Function**)는 개발자가 필요한 기능을 직접 정의한 함수입니다.
- `def` 키워드를 사용하여 함수를 정의합니다. 함수 이름 뒤에 소괄호 `()`를 붙여 호출하면 함수 내부의 코드가 실행됩니다. 한 번 정의한 함수는 여러 번 호출할 수 있습니다.
- **매개변수**(**Parameter**)는 함수가 전달받은 값을 사용하는 변수이며, **인수**(**Argument**)는 함수를 호출할 때 실제로 전달하는 값입니다.
- **위치 인수**(**Positional Argument**)는 작성한 순서에 따라 매개변수에 전달됩니다. 함수를 호출할 때는 필요한 인수의 순서와 개수를 확인해야 합니다.
- **반환값**(**Return Value**)은 함수가 호출한 곳으로 돌려주는 값입니다. 반환값은 변수에 저장하거나 다른 연산 및 함수의 인수로 활용할 수 있습니다.
- `print()`는 값을 화면에 출력하는 함수이며, `return`은 값을 반환하고 현재 함수의 실행을 종료하는 키워드입니다. 반환할 값을 별도로 지정하지 않은 함수는 `None`을 반환합니다.
- **스코프**(**Scope**)는 변수의 이름을 참조할 수 있는 범위입니다. **지역 변수**(**Local Variable**)는 해당 함수의 지역 범위에 속하며, **전역 변수**(**Global Variable**)는 파일의 최상위 영역에 정의된 변수입니다.
- 함수 내부에서 다른 함수를 호출하고 그 반환값을 다시 반환할 수 있습니다. 이러한 방식을 활용하면 복잡한 작업을 여러 함수로 나누어 처리할 수 있습니다.
- **기능 분해**(**Functional Decomposition**)는 하나의 프로그램을 여러 기능으로 나누어 구성하는 방식입니다. 각 함수의 역할을 명확하게 구분하면 코드의 가독성과 유지보수성을 높일 수 있습니다.

## Practice

- [Exercise & Mini Project](./Practice.md)
- [Solutions](./solutions/README.md)

---

<p align="center">
  <a href="../Chapter-06/">← Chapter 06</a>
  &nbsp;·&nbsp;
  <a href="../README.md">Python Guide</a>
  &nbsp;·&nbsp;
  <a href="../Chapter-08/">Chapter 08 →</a>
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
