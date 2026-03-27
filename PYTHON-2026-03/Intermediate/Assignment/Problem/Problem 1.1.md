(수정중)

# **Problem 1.1. 시간 분 초**
## 배경 지식(Background)

- 두 정수와 연산자(+, -, *, /)를 입력하면 해당 연산의 결과가 출력되도록 프로그램을 만들어보자.
- 이 때, 프로그램은 첫 번째 정수, 연산자, 두 번째 정수 순서로 값을 입력 받는다.
- 다음과 같은 코드를 설계할 수 있다.

```
def calculator(num1, op, num2):
  if op=='+':
    return num1+num2
  elif op=='-':
    return num1-num2
  elif op=='*':
    return num1*num2
  elif op=='/':
    return num1/num2

num1=int(input())
op=input()
num2=int(input())

result=calculator(num1, op, num2)
print(result)
```
위의 코드를 실행하면 결과는 다음과 같다
```
3
+
2
5
```

**dictionary**와 **lambda**식을 이용해서 표현하는 것도 가능하다.
```
OPERATORS = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b,
}

num1=int(input())
op=input()
num2=int(input())

result=OPERATORS[op](num1, num2)
print(result)
```
위의 코드를 실행하면 결과는 다음과 같다
```
1
+
2
3
```

**while**을 사용해서 두 숫자의 연산을 반복하는 것도 가능하다.
```
def calculator(num1, op, num2):
  if op=='+':
    return num1+num2
  elif op=='-':
    return num1-num2
  elif op=='*':
    return num1*num2
  elif op=='/':
    return num1/num2

while True:
  num1=int(input())
  op=input()
  num2=int(input())
  result=calculator(num1, op, num2)
  print(f"{num1} {op} {num2} = {result}")
```
위의 코드를 실행하면 결과는 다음과 같다.
```
1
+
2
1 + 2 = 3
```

이 때, **while**은 조건이 `True`일 때 무한반복 되므로 특정 조건에서 **while**문을 **빠져나오도록 설정**해주는 것이 좋다.
```
  if input("더 계산하시겠습니까?(y/n): ")=='n':
    break
```
while문 안에 위의 코드를 추가하여 y를 입력하면 계속 계산이 가능하고, n을 입력하면 프로그램이 종료되도록 설정할 수 있다.
```
while True:
  num1=int(input())
  op=input()
  num2=int(input())
  result=calculator(num1, op, num2)
  print(f"{num1} {op} {num2} = {result}")
  if input("더 계산하시겠습니까?(y/n): ")=='n':
    break
```
실행 결과는 다음과 같다.
```
1
+
10
1 + 10 = 11
더 계산하시겠습니까?(y/n): y
10
/
5
10 / 5 = 2.0
더 계산하시겠습니까?(y/n): n
```

---

## Question

- 실제 계산기는 **계산을 이어할 수 있는 기능**이 있다.
- 예를들어 `3+5`를 계산하면 `8`이 나오는데, 이 상태에서 `x10`을 하면 `8x10`이 계산되여 `80`이라는 값을 얻을 수 있다.
- 다음은 실행 결과의 예시입니다.
```
숫자를 입력하세요: 10
연산자를 입력하세요: +
숫자를 입력하세요: 5
10 + 5 = 15
연산자를 입력하세요: *
숫자를 입력하세요: 2
15 * 2 = 30
연산자를 입력하세요: *
숫자를 입력하세요: 0
30 * 0 = 0
연산자를 입력하세요: +
숫자를 입력하세요: 11
0 + 11 = 11
```

- Background의 코드는 매번 '정수, 연산자, 정수'를 입력해야 합니다. 이 부분을 개선하고자 합니다.
- **처음 수를 입력한 이후부터는 '연산자'와 '다음 수' 두 개만 입력해도 연산이 계속 이루어질 수 있도록** 프로그램을 설계하시오.
- (예시와 동일한 결과가 나올 필요는 없습니다. **계속 연산**되는 기능만 구현하면 됩니다.)
