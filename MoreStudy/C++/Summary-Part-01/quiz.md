# Quiz — Part 01

Chapter 01~11의 개념을 확인합니다. 문제를 먼저 풀어본 뒤 각 문항의 정답 및 해설을 펼쳐 확인하세요.

[← Summary 목차](./README.md) · [Quiz](./quiz.md) · [Problems](./problem.md) · [HTML 문제집](https://jseong2024.github.io/MYPAUL-PYTHONEDU/MoreStudy/C%2B%2B/Summary-Part-01/Summary-Part-01.html)

## 객관식 (Q-01~Q-12)

### Q-01 · Chapter 01

C++20 표준 출력과 관련된 설명 중 **가장 올바른 것**을 고르시오.

1. `std::cout << std::format("{}", "Hello");`를 출력하려면 `<iostream>`과 `<format>` 헤더가 필요하다.
2. `std::println("Hello");`는 C++20 표준에 포함되어 있으므로 `<iostream>` 없이 바로 사용할 수 있다.
3. `using namespace std;`를 선언하면 `cout.print("Hello");` 형태로 출력할 수 있다.
4. 표준 출력 스트림 객체는 전역 객체이므로 별도의 헤더 없이 `std::cout`을 바로 사용할 수 있다.

<details>
<summary>정답 및 해설</summary>

**정답: 1번 — `std::cout << std::format("{}", "Hello");`를 출력하려면 `<iostream>`과 `<format>` 헤더가 필요하다.**

**정답 설명:** C++20의 `std::format`은 `<format>`에 선언되어 있고, `std::cout`은 `<iostream>`에 선언되어 있습니다. 형식화된 문자열을 출력할 때 두 헤더를 명시적으로 포함하는 것이 올바릅니다.

**2번 — C++20과 C++23 표준 혼동**

`std::println`과 `<print>`는 C++23부터 제공됩니다. C++20의 표준 출력 기능으로 간주할 수 없습니다.

**3번 — 존재하지 않는 멤버 함수**

`std::cout`에는 `.print()` 멤버 함수가 없습니다. `using namespace std;`를 사용하더라도 새로운 멤버 함수가 생기지 않습니다.

**4번 — 헤더 선언과 객체의 수명 혼동**

`std::cout`이 전역 스트림 객체라는 사실과, 소스에서 해당 이름을 사용하기 위한 선언은 별개입니다. `<iostream>`을 직접 포함해야 합니다.

[Chapter 01 README](../Chapter-01/README.md)

</details>

### Q-02 · Chapter 02

다음 코드에서 일어나는 일은 무엇입니까?

```cpp
int value{3.5};
```

1. `value`는 `3`이 됩니다.
2. `value`는 `4`가 됩니다.
3. 축소 변환(Narrowing Conversion) 때문에 컴파일 오류가 발생합니다.
4. 실행할 때만 오류가 발생합니다.

<details>
<summary>정답 및 해설</summary>

**정답: 3번 — 축소 변환(Narrowing Conversion) 때문에 컴파일 오류가 발생합니다.**

**중괄호 초기화(Brace Initialization)** 는 실수에서 정수로의 축소 변환처럼 값이 손실될 수 있는 초기화를 허용하지 않습니다. 따라서 `int value{3.5};`는 컴파일되지 않습니다. 반면 `int value(3.5);`는 변환을 허용해 정수 `3`을 저장합니다.

**1번 — 암묵적 변환과 중괄호 초기화 혼동**

다른 초기화 방식에서 `3.5`가 `3`으로 변환될 수 있지만, 중괄호 초기화는 이 축소 변환을 거부합니다.

**2번 — 반올림 혼동**

실수에서 정수로 변환할 때 자동 반올림하여 `4`가 되는 것은 아닙니다.

**4번 — 오류 발생 시점**

이 코드는 실행 시점이 아니라 컴파일 시점에 진단됩니다.

[Chapter 02 README](../Chapter-02/README.md)

</details>

### Q-03 · Chapter 03

`x`가 `0`일 때, 다음 조건식의 동작은 무엇입니까?

```cpp
x != 0 && 10 / x > 2
```

1. `0`으로 나누기 연산이 실행되어 오류가 발생합니다.
2. 오른쪽 항을 평가하지 않고 전체 결과가 `false`가 됩니다.
3. 조건식은 `true`가 됩니다.
4. 조건식의 문법이 잘못되어 컴파일되지 않습니다.

<details>
<summary>정답 및 해설</summary>

**정답: 2번 — 오른쪽 항을 평가하지 않고 전체 결과가 `false`가 됩니다.**

논리 AND 연산자 `&&`는 **단락 평가(Short-circuit Evaluation)** 를 수행합니다. 왼쪽 조건 `x != 0`이 `false`이므로 오른쪽 `10 / x > 2`는 평가하지 않습니다. 따라서 0으로 나누기 연산은 실행되지 않습니다.

**1번 — 단락 평가 누락**

오른쪽 식은 실행되지 않으므로 0으로 나누지 않습니다.

**3번 — 논리 AND의 결과 판단 오류**

`&&`는 왼쪽 항이 거짓이면 전체 결과도 거짓입니다.

**4번 — 실행 시 평가와 문법의 혼동**

`x`가 정수로 선언되어 있다면 식 자체는 올바른 C++ 표현식입니다.

[Chapter 03 README](../Chapter-03/README.md)

</details>

### Q-04 · Chapter 04

다음 반복문의 출력 결과는 무엇입니까?

```cpp
for (int i = 0; i < 3; ++i) {
    std::cout << i;
}
```

1. `123`
2. `012`
3. `01`
4. `0123`

<details>
<summary>정답 및 해설</summary>

**정답: 2번 — `012`**

`i`는 `0`부터 시작하여 `0`, `1`, `2`일 때만 반복문 본문을 실행합니다. `i`가 `3`이 되는 순간 `i < 3`이 거짓이므로 종료됩니다. 따라서 공백 없이 `012`가 출력됩니다.

**1번 — 시작값 누락**

`i`의 초깃값은 `1`이 아니라 `0`입니다.

**3번 — 반복 종료 시점 오해**

`i == 2`인 반복도 `i < 3`을 만족합니다.

**4번 — 끝값 포함 착각**

`i == 3`에서는 조건이 거짓이므로 `3`은 출력되지 않습니다.

[Chapter 04 README](../Chapter-04/README.md)

</details>

### Q-05 · Chapter 05

함수 내부에서 호출자(Caller)의 정수 변수 값을 **직접 변경**하려면 어떤 매개변수가 가장 적절합니까?

1. `int value`
2. `const int& value`
3. `int& value`
4. `const int value`

<details>
<summary>정답 및 해설</summary>

**정답: 3번 — `int& value`**

`int&`는 호출자의 원본 정수에 대한 **참조 전달(Pass by Reference)** 입니다. 이 참조로 값을 변경하면 호출자의 변수에도 반영됩니다.

**1번 — 값 전달**

매개변수가 복사본이므로 함수 내부의 수정이 원본에 반영되지 않습니다.

**2번 — 읽기 전용 참조**

`const int&`는 원본을 참조하지만 참조를 통한 수정은 금지됩니다.

**4번 — 상수 복사본**

`const int`는 복사된 값을 함수 안에서도 수정할 수 없게 합니다.

[Chapter 05 README](../Chapter-05/README.md)

</details>

### Q-06 · Chapter 06

`std::vector<int> v{1, 2, 3};`에 대한 설명 중 **가장 옳은 것**은 무엇입니까?

1. `v[3]`은 안전하게 `0`을 반환합니다.
2. `v.at(3)`은 범위를 검사한 뒤 예외(`std::out_of_range`)를 던집니다.
3. `v[3]`은 유효하지 않은 인덱스이므로 항상 컴파일 오류를 발생시킵니다.
4. `v.at(3)`은 범위를 벗어나면 자동으로 새 요소를 추가합니다.

<details>
<summary>정답 및 해설</summary>

**정답: 2번 — `v.at(3)`은 범위를 검사한 뒤 예외(`std::out_of_range`)를 던집니다.**

`std::vector`의 유효 인덱스는 `0`, `1`, `2`입니다. `at()`은 인덱스를 검사하고 범위 밖이면 `std::out_of_range` 예외를 던집니다. 반면 `operator[]`는 범위를 검사하지 않으며, 이 경우 접근하면 **미정의 동작(Undefined Behavior, UB)** 입니다.

**1번 — 범위 밖 접근**

`v[3]`으로 존재하지 않는 요소를 읽는 동작은 보장되지 않습니다.

**3번 — 컴파일 오류와 런타임 오류 구별**

`v[3]`은 문법상 유효하며 컴파일러가 반드시 잡아주지 않습니다.

**4번 — 컨테이너 인터페이스 혼동**

`at()`은 접근 함수이고, 요소 추가는 `push_back()` 또는 `emplace_back()` 등의 역할입니다.

[Chapter 06 README](../Chapter-06/README.md)

</details>

### Q-07 · Chapter 07

함수 내부 지역 변수(Local Variable)의 참조(Reference)를 반환한 뒤 호출자가 그 참조로 값에 접근하면 어떤 문제가 발생할 수 있습니까?

1. 항상 자동으로 깊은 복사(Deep Copy)가 이루어집니다.
2. 지역 변수의 수명이 끝나 댕글링 참조(Dangling Reference)가 되며, 이를 사용하면 미정의 동작이 발생할 수 있습니다.
3. 컴파일러가 반드시 문법 오류로 거부합니다.
4. `std::string` 타입에서만 안전하게 작동합니다.

<details>
<summary>정답 및 해설</summary>

**정답: 2번 — 지역 변수의 수명이 끝나 댕글링 참조(Dangling Reference)가 되며, 이를 사용하면 미정의 동작이 발생할 수 있습니다.**

일반 지역 객체는 함수 종료 시 수명이 끝납니다. 그 객체를 가리키는 참조를 반환하면 **댕글링 참조(Dangling Reference)** 가 되며, 수명이 끝난 객체에 접근하는 것은 미정의 동작입니다. 컴파일러 경고가 나오더라도 항상 오류로 차단되는 것은 아닙니다.

**1번 — 참조와 복사 혼동**

참조 반환은 값을 복사하지 않습니다.

**3번 — 컴파일러 진단 보장 오해**

진단이 가능해도 컴파일 오류로 반드시 거부된다는 보장은 없습니다.

**4번 — 자료형에 따른 안전성 착각**

지역 객체 수명이 끝나는 문제는 문자열에만 한정되지 않습니다.

[Chapter 07 README](../Chapter-07/README.md)

</details>

### Q-08 · Chapter 08

클래스가 수량(Quantity)을 항상 `0` 이상으로 유지해야 할 때 가장 알맞은 설계는 무엇입니까?

1. 수량 멤버를 `public`으로 두어 외부에서 자유롭게 수정하게 합니다.
2. 수량 멤버를 `private`으로 보호하고, 생성과 수정 과정에서 유효 범위를 검사합니다.
3. 출력할 때만 음수를 `0`으로 바꿔 보여줍니다.
4. 음수를 그대로 저장하고 문제가 발생하면 나중에 처리합니다.

<details>
<summary>정답 및 해설</summary>

**정답: 2번 — 수량 멤버를 `private`으로 보호하고, 생성과 수정 과정에서 유효 범위를 검사합니다.**

**캡슐화(Encapsulation)** 는 내부 상태에 대한 무분별한 접근을 제한합니다. 생성자와 상태 변경 함수에서 조건을 검사해 **불변 조건(Invariant)** 인 `quantity >= 0`을 계속 만족하도록 만드는 것이 핵심입니다.

**1번 — 무제한 외부 수정**

외부에서 음수를 직접 대입할 수 있어 불변 조건을 유지할 수 없습니다.

**3번 — 표시와 상태 혼동**

화면에서만 값을 고쳐 보여도 객체 내부에는 잘못된 상태가 남습니다.

**4번 — 검증 책임 지연**

객체는 유효하지 않은 값을 받아들이지 않도록 상태 변경 시점에 검증해야 합니다.

[Chapter 08 README](../Chapter-08/README.md)

</details>

### Q-09 · Chapter 09

기본 클래스(Base Class)의 포인터나 참조로 파생 클래스(Derived Class)에서 재정의한 함수를 동적으로 호출하려면 기본 클래스의 해당 함수가 무엇이어야 합니까?

1. `static`
2. `virtual`
3. `explicit`
4. `friend`

<details>
<summary>정답 및 해설</summary>

**정답: 2번 — `virtual`**

기본 클래스의 멤버 함수를 `virtual`로 선언하면 실제 객체 타입에 따라 재정의된 함수가 호출되는 **동적 디스패치(Dynamic Dispatch)** 가 가능합니다. 파생 클래스 쪽에는 `override`를 붙여 재정의를 검사하는 것이 좋습니다.

**1번 — 정적 멤버 혼동**

`static` 멤버 함수는 가상 함수가 될 수 없습니다.

**3번 — 명시적 변환 키워드**

`explicit`은 생성자나 변환 함수의 암묵적 변환을 제어하는 데 사용합니다.

**4번 — 접근 권한 키워드**

`friend`는 지정한 함수나 클래스에 접근 권한을 부여합니다.

[Chapter 09 README](../Chapter-09/README.md)

</details>

### Q-10 · Chapter 10

다음 중 **키(Key)를 기준으로 오름차순 정렬된 상태를 유지**하며 요소를 순회해야 할 때 가장 적절한 C++ STL 컨테이너는 무엇입니까?

1. `std::unordered_map`
2. `std::vector`만 가능
3. `std::map`
4. `std::stack`

<details>
<summary>정답 및 해설</summary>

**정답: 3번 — `std::map`**

`std::map`은 기본 비교자인 `std::less`를 사용해 키의 오름차순으로 요소를 유지하고 순회합니다. 일반적으로 균형 이진 탐색 트리로 구현되지만 구체적인 트리 종류까지 표준에서 강제하지는 않습니다.

**1번 — 해시 컨테이너의 순서 보장 착각**

`std::unordered_map`은 순회 순서를 정렬된 상태로 보장하지 않습니다.

**2번 — 정렬 유지 기능 혼동**

`std::vector`로도 정렬된 결과를 만들 수 있지만 삽입 때마다 정렬을 유지하려면 추가 처리가 필요합니다.

**4번 — 컨테이너 어댑터의 목적**

`std::stack`은 가장 나중에 넣은 요소부터 꺼내는 구조이며 키 기반 정렬 순회용이 아닙니다.

[Chapter 10 README](../Chapter-10/README.md)

</details>

### Q-11 · Chapter 10

정렬 기준(키)이 동일한 항목들의 **원래 순서(상대적 순서)가 정렬 후에도 그대로 유지**되어야 할 때 사용할 수 있는 C++ 표준 알고리즘은 무엇입니까?

1. `std::sort`
2. `std::stable_sort`
3. `std::reverse`
4. `std::find`

<details>
<summary>정답 및 해설</summary>

**정답: 2번 — `std::stable_sort`**

`std::stable_sort`는 비교 기준상 동등한 항목끼리의 **상대적 순서**를 보존하는 안정 정렬(Stable Sort)을 제공합니다. 일반 `std::sort`는 그 순서를 보존한다고 보장하지 않습니다.

**1번 — 일반 정렬의 안정성 착각**

`std::sort`는 키가 같은 요소의 상대적 순서를 유지할 의무가 없습니다.

**3번 — 정렬과 뒤집기 혼동**

`std::reverse`는 구간의 순서를 뒤집을 뿐 키로 정렬하지 않습니다.

**4번 — 탐색 알고리즘**

`std::find`는 일치하는 항목을 찾는 알고리즘이지 정렬 알고리즘이 아닙니다.

[Chapter 10 README](../Chapter-10/README.md)

</details>

### Q-12 · Chapter 11

CSV 데이터에서 `"상품, 파랑",300`처럼 따옴표 안에 쉼표가 있는 필드를 **쉼표(`,`)만 기준으로 분리**하면 어떤 문제가 발생합니까?

1. 문제 없이 정확히 두 필드로 분리됩니다.
2. 따옴표 안의 쉼표까지 구분자로 오해하여 데이터가 잘못 나뉩니다.
3. 파싱할 때 항상 빈 문자열만 반환합니다.
4. C++20에서는 CSV 파일을 읽을 수 없습니다.

<details>
<summary>정답 및 해설</summary>

**정답: 2번 — 따옴표 안의 쉼표까지 구분자로 오해하여 데이터가 잘못 나뉩니다.**

CSV의 인용 필드 안에 있는 쉼표는 필드 내용의 일부입니다. 문자 `,`만 기준으로 분리하면 레코드 구조가 깨질 수 있으므로 **인용 상태(Quoted Field)** 를 추적해야 합니다.

**1번 — 인용 필드 무시**

쉼표만으로 분리하면 `"상품`과 ` 파랑"`이 다른 필드가 됩니다.

**3번 — 파서 동작 일반화**

잘못 분리되는 것이지 항상 빈 문자열을 반환하는 것은 아닙니다.

**4번 — 언어 표준과 파일 포맷 혼동**

C++20에서도 파일을 읽고 CSV 규칙을 구현할 수 있습니다.

[Chapter 11 README](../Chapter-11/README.md)

</details>

## 주관식·서술형 (Q-13~Q-20)

### Q-13 · Chapter 02

C++에서 **정수 나눗셈과 실수 나눗셈**의 차이를 설명하고, 숫자 `5`와 `2`를 피연산자로 사용하여 각각 결과값 `2`와 `2.5`를 얻는 코드를 작성하시오. (C++20 기준)

<details>
<summary>정답 및 해설</summary>

두 피연산자가 정수이면 정수 나눗셈이 수행되어 0 방향으로 소수 부분을 버립니다. 적어도 한 피연산자가 부동소수점 타입이면 실수 나눗셈이 이루어집니다. `5 / 2`는 `2`, `static_cast<double>(5) / 2` 또는 `5.0 / 2`는 `2.5`입니다.

**예시 코드**

```cpp
#include <iostream>

int main() {
    // 정수 나눗셈: 2
    int result_int = 5 / 2;

    // 실수 나눗셈: 2.5
    double result_double = static_cast<double>(5) / 2;

    std::cout << "정수 나눗셈: " << result_int << "\n";
    std::cout << "실수 나눗셈: " << result_double << "\n";
    return 0;
}
```

**실행 결과**

```text
정수 나눗셈: 2
실수 나눗셈: 2.5
```

[Chapter 02 README](../Chapter-02/README.md)

</details>

### Q-14 · Chapter 04

반복문에서 `i < count`와 `i <= count`의 반복 횟수 차이를 설명하시오. (`count = 3`, `i = 0`에서 시작)

<details>
<summary>정답 및 해설</summary>

`i < count`는 `0`, `1`, `2`에서 3회 반복합니다. `i <= count`는 `3`까지 포함해 4회 반복합니다. 범위를 하나 더 순회하는 **오프바이원(Off-by-one) 오류**를 피하도록 조건을 확인해야 합니다.

**예시 코드**

```cpp
#include <iostream>

int main() {
    int count = 3;
    for (int i = 0; i < count; ++i) std::cout << i;
    std::cout << "\n";
    for (int i = 0; i <= count; ++i) std::cout << i;
    std::cout << "\n";
}
```

**실행 결과**

```text
012
0123
```

[Chapter 04 README](../Chapter-04/README.md)

</details>

### Q-15 · Chapter 05

함수가 기존 객체를 **조회만 하는 경우**와 **원본을 수정하는 경우**, 매개변수로 `const T&`와 `T&`를 각각 사용하는 이유를 설명하시오.

<details>
<summary>정답 및 해설</summary>

`const T&`는 원본을 복사하지 않고 읽기 전용으로 참조합니다. `T&`는 원본을 수정해야 할 때 사용합니다. 특히 큰 객체에서 복사 비용을 줄일 수 있지만, `int`처럼 작은 타입은 값 전달도 충분히 적절합니다. 클래스 내부의 변경 가능한 멤버 참조를 외부에 그대로 반환하면 불변 조건이 깨질 수 있으므로 주의해야 합니다.

**예시 코드**

```cpp
#include <iostream>
#include <vector>

int sum(const std::vector<int>& values) {
    int total = 0;
    for (int value : values) total += value;
    return total;
}

void add(std::vector<int>& values, int value) {
    values.push_back(value);
}

int main() {
    std::vector<int> values{1, 2};
    add(values, 3);
    std::cout << sum(values) << "\n";
}
```

**실행 결과**

```text
6
```

[Chapter 05 README](../Chapter-05/README.md)

</details>

### Q-16 · Chapter 07

`std::vector`에 `push_back()`을 호출한 뒤 기존 원소를 가리키던 포인터나 참조가 **무효화될 수 있는 이유**를 설명하시오.

<details>
<summary>정답 및 해설</summary>

새 요소를 저장할 용량이 부족하면 `std::vector`가 더 큰 저장 공간을 확보하고 기존 요소를 옮기는 **재할당(Reallocation)** 을 수행합니다. 그 경우 기존 요소를 가리키던 포인터·참조·반복자는 모두 무효화됩니다. 재할당이 일어나지 않으면 기존 요소에 대한 참조는 유지되지만, 이전의 `end()` 반복자는 무효화됩니다.

**예시 코드**

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> values{10, 20, 30};
    int* first = &values[0];
    auto old_capacity = values.capacity();

    values.push_back(40);
    if (values.capacity() != old_capacity) {
        first = &values[0];  // 다시 주소 획득
    }
    std::cout << *first << "\n";
}
```

**실행 결과**

```text
10
```

[Chapter 07 README](../Chapter-07/README.md)

</details>

### Q-17 · Chapter 08

`struct`와 `class`의 기본 접근 지정자(Access Specifier) 차이를 설명하고, 어떤 기준으로 나누어 사용하는지 예를 들어 서술하시오.

<details>
<summary>정답 및 해설</summary>

`struct`의 기본 멤버 접근은 `public`, `class`의 기본 멤버 접근은 `private`입니다. 기능상 큰 차이는 없지만 단순 데이터 묶음에는 `struct`, 상태 변경 규칙과 불변 조건을 보호해야 하는 타입에는 `class`가 자주 사용됩니다.

**예시 코드**

```cpp
#include <iostream>

struct Position {
    int x{0};
    int y{0};
};

class Counter {
public:
    void add() { ++count_; }
    int value() const { return count_; }
private:
    int count_{0};
};

int main() {
    Position p{2, 3};
    Counter c;
    c.add();
    std::cout << p.x << "," << p.y << " / " << c.value() << "\n";
}
```

**실행 결과**

```text
2,3 / 1
```

[Chapter 08 README](../Chapter-08/README.md)

</details>

### Q-18 · Chapter 09

다형적 기본 클래스(Polymorphic Base Class)의 포인터를 통해 파생 객체를 삭제할 때 **가상 소멸자(Virtual Destructor)** 가 필요한 이유를 설명하시오.

<details>
<summary>정답 및 해설</summary>

일반적으로 파생 객체를 기본 클래스 포인터로 `delete`할 때 기본 클래스 소멸자가 가상이 아니면 **미정의 동작(Undefined Behavior)** 이 발생합니다. 따라서 단순히 파생 클래스 소멸자가 빠지거나 메모리 누수가 발생하는 것으로만 설명하면 불충분합니다. 가상 소멸자를 선언하면 파생 객체와 기본 부분의 소멸이 올바르게 이루어집니다.

**예시 코드**

```cpp
#include <iostream>
#include <memory>

struct Base {
    virtual ~Base() { std::cout << "Base\n"; }
};

struct Derived : Base {
    ~Derived() override { std::cout << "Derived\n"; }
};

int main() {
    std::unique_ptr<Base> p = std::make_unique<Derived>();
}
```

**실행 결과**

```text
Derived
Base
```

[Chapter 09 README](../Chapter-09/README.md)

</details>

### Q-19 · Chapter 10

코드별 발생 횟수를 집계하면서 결과는 **코드 오름차순**으로 출력해야 합니다. 적절한 STL 컨테이너를 선택하고 이유를 설명하시오.

<details>
<summary>정답 및 해설</summary>

`std::map<std::string, int>`는 키가 정렬된 순서로 유지되므로 별도 정렬 없이 순회할 수 있습니다. 삽입·검색·수정은 일반적으로 `O(log N)`입니다. `std::unordered_map`을 사용해 평균적으로 빠르게 집계한 뒤 키를 별도 정렬하는 대안도 가능합니다.

**예시 코드**

```cpp
#include <iostream>
#include <map>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> codes{"C02", "C01", "C02"};
    std::map<std::string, int> counts;
    for (const auto& code : codes) ++counts[code];
    for (const auto& [code, count] : counts) {
        std::cout << code << " " << count << "\n";
    }
}
```

**실행 결과**

```text
C01 1
C02 2
```

[Chapter 10 README](../Chapter-10/README.md)

</details>

### Q-20 · Chapter 11

기존 결과 파일을 갱신하는 보고서 프로그램에서 **중간 실패로 이전 정상 결과가 손상되는 것을 방지할 방법**을 설명하시오.

<details>
<summary>정답 및 해설</summary>

원본에 바로 기록하지 말고 같은 파일시스템의 임시 파일에 결과를 모두 작성합니다. 스트림 쓰기·닫기 오류를 확인한 뒤 최종 경로로 교체합니다. 이때 `std::filesystem::rename`의 기존 대상 교체 가능 여부와 원자성은 운영체제·파일시스템 조건을 확인해야 합니다. 특히 Windows에서는 대상 파일이 이미 있거나 열려 있을 때 교체가 실패할 수 있으므로, 오류 처리와 복구 정책을 별도로 설계해야 합니다. 단순히 파일 이름을 바꿨다고 전원 차단까지 포함한 완전한 내구성이 보장되는 것은 아닙니다.

**예시 코드**

```cpp
#include <filesystem>
#include <fstream>
#include <iostream>
#include <system_error>

int main() {
    const std::filesystem::path temp = "report.tmp";
    const std::filesystem::path target = "report.txt";

    {
        std::ofstream out(temp, std::ios::trunc);
        if (!out) return 1;
        out << "REPORT OK\n";
        out.flush();
        if (!out) return 1;
        out.close();
        if (!out) return 1;
    }

    std::error_code ec;
    std::filesystem::rename(temp, target, ec);
    if (ec) {
        std::cerr << "교체 실패: " << ec.message() << "\n";
        return 1;
    }
    std::cout << "저장 완료\n";
}
```

[Chapter 11 README](../Chapter-11/README.md)

</details>

[← Summary 목차](./README.md) · [Quiz](./quiz.md) · [Problems](./problem.md) · [HTML 문제집](https://jseong2024.github.io/MYPAUL-PYTHONEDU/MoreStudy/C%2B%2B/Summary-Part-01/Summary-Part-01.html)
