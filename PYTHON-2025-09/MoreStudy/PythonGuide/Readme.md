<p align='center'>
  <img src="https://capsule-render.vercel.app/api?type=soft&color=auto&section=header&text=Python%20Guide&fontSize=40&animation=twinkling"/>
</p>

<p align='center'>
  <a href="https://github.com/JSeong2024/2025-MYPAUL-PYTHONEDU/tree/main/PYTHON-2025-09/MoreStudy">
    <img src="https://img.shields.io/badge/Go%20To%20Back-F3EC69?&style=for-the-badge&&logoColor=white"/>
  </a>
</p>

---

# NOTES
- Python Basic Guide. [click here](https://github.com/JSeong2024/2025-MYPAUL-PYTHONEDU/blob/main/PYTHON-2025-09/MoreStudy/PythonGuide/Python_Basic_Guide.pdf)
- Last update: 2025.09.28.

# SUMMARY

## Chapter 01. 입력과 출력

### 1.1. print()
- **괄호 안의 내용을 출력**하는 함수
- **따옴표로 묶은 것은 문자열**이 되고, print() 함수의 괄호 안에 문자열을 쓰면 가장 바깥의 따옴표를 제외한 나머지가 출력된다.
  ```
  print('apple')
  ```
  ```
  print("apple")
  ```
  위의 두 코드는 모두 ``apple`` 이라고 출력된다.
  
- 여러 개를 출력하려면 콤마(,)로 나눠야 한다.
  ```
  print('Happy New', 2026)
  ```
  실행 결과: ``2026``

- 문자열을 콤마(,)로 구분해서 print() 함수로 출력하면 한 칸 띄어져 출력된다.
  ```
  print('Red', 'Apple')
  ```
  실행 결과: ``Red Apple``
- 문자열+문자열을 print() 함수로 출력하면 서로 붙어 출력된다.
  ```
  print('Red'+'Apple')
  ```
  실행 결과: ``RedApple``
  
- **[심화]** **f-string formatting**: 앞에 f가 붙어있는 문자열에는 변수를 중괄호로 묶어서 표현할 수 있다. f'' 혹은 f""
  ```
  a, b = 3, 3
  print(f"{a}을 {b}번 곱하면 {a**b}이다.")
  ```
  실행 결과: ``3을 3번 곱하면 27이다.``

### 1.2. input()
- 키보드로 **값을 입력받는** 함수.
- 키보드로 입력받은 값을 변수에 저장하는 코드는 다음과 같다.
  ```
  a = input()
  ```
  
- input() 함수를 통해 받은 값은 **문자열(string)** 형태로 저장된다.
- 만약 숫자 형태로 받고 싶다면 int() 함수를 이용해 int(input())라고 작성하면 된다.
  ```
  a = int(input())
  ```
  *int() 함수는 괄호 안의 숫자를 정수(integer)로 바꿔주는 함수

- 괄호 안에 문장을 쓸 수도 있다.
  ```
  a = int(input('1~6 사이의 자연수를 적으세요: '))
  ```
  실행 결과: ``1~6 사이의 자연수를 적으세요:               ``


## Chapter 02. 연산자

### 2.1. 산술 연산자
- 곱하기(*), 거듭제곱(**), 나누기(/), 몫(//), 나머지(%)
- **[심화]** 비트 쉬프트 연산: 곱하기 $2^n$ (<< n), 곱하기 $2^{-n}$ (>> n)

### 2.2. 비교 연산자
- 식이 참이면 ``True``, 거짓이면 ``False``를 반환한다.
- 같다(==), 같지 않다(!=), 크다(>), 작다(<), 크거나 같다(>=), 작거나 같다(<=)
  ```
  print(10==20)
  print(5!=2)
  print(10<20)
  print(4>6)
  print(len([1,2,3])>=3)
  print(sum(range(7))<=5**2)
  ```
  
  
### 2.3. 논리 연산자
- and: 양쪽 식이 모두 참일 때만 True
- or: 양쪽 식 중에 하나라도 참이면 True
- not: 식이 참이면 False, 거짓이면 True

### 2.4. 조건문
- if 문: *만약-라면*
  ```
  if (조건식):
    (코드1)
  (코드2)
  ```
  (조건식)이 참이면 if 부분이 실행. 즉, (코드1)이 실행됨.

  (코드2)는 조건문 밖에 있으므로 (조건식)의 참, 거짓과 관계없이 실행됨.

- if-else 문: *만약-라면, 그렇지 않으면-*
  ```
  if (조건식):
    (코드1)
  else:
    (코드2)
  (코드3)
  ```
  (조건식)이 참이면 if 부분이 실행. 즉, (코드1)이 실행됨.
  
  (조건식)이 거짓이면 if 부분은 실행되지 않고, else 부분이 실행. 즉, (코드2)가 실행됨.
  
  (코드3)은 조건문 밖에 있으므로 (조건식)의 참, 거짓과 관계없이 실행됨.

- if-elif-else 문: *만약-라면, 또는-라면, 다 아니면-*
  ```
  if (조건식1):
    (코드1)
  elif (조건식2):
    (코드2)
  else:
    (코드3)
  (코드4)
  ```
  (조건식1)이 참이면 if 부분이 실행. 즉, (코드1)이 실행됨.
 
  (조건식1)이 거짓이면 if 부분은 실행되지 않고, elif 부분으로 넘어가서 (조건식2)가 참인지 거짓인지 확인하게됨.
 
  (조건식1)이 거짓이고 (조건식2)가 참이면 elif 부분이 실행. 즉, (코드2)가 실행됨.
 
  (조건식1)과 (조건식2)가 모두 거짓이라면 else 부분이 실행. 즉, (코드3)이 실행됨.
 
  (코드4)는 조건문 밖에 있으므로 (조건식1)이나 (조건식2)의 참, 거짓과 관계없이 실행됨.


 ## Chapter 03. (Update 예정)
