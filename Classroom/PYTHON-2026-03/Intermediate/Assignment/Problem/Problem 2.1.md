# **Problem 2.1. 숫자 업다운 게임**
## 배경 지식(Background)
### random 함수
- random 모듈을 import 해야 random 함수를 사용할 수 있다.
  
  ```
  import random
  a = random.randint(10)
  ```
  ```
  import random as ran
  a = ran.randint(10)
  ```
- randint(): 범위내에서 정수를 임의로 하나 선택한다.
- randint(1, 10): 1 ~ 10 사이의 정수 중 하나를 선택한다. 

### Example
- **1 ~ 100 사이의 정수** 중 **무작위**로 하나를 선택하는 시행을 **2번** 진행한다.
- 뽑은 두 수 중 **큰 수**를 **변수 a**에 저장하고, **작은 수**를 **변수 b**에 저장한다.
- **a, b** 순서로 출력하는 프로그램을 만들어보자.
```
import random as ran

a = ran.randint(1, 100)
b = ran.randint(1, 100)

if a < b:
  a, b = b, a

print(a, b)
```

---

## Question

- 프로그램은 1부터 100사이의 임의의 자연수를 선택한다. (1이상 100이하의 임의의 자연수)
- 플레이어는 정답을 제시할 수 있다.
- 만약 정답 숫자가 제시한 숫자보다 크다면 **UP** 이라고 출력되고, 제시한 숫자보다 작다면 **DOWN** 이라고 출력되며, 제시한 숫자와 일치한다면 **Good Game**을 출력한다.
    
  ```
  import random
  ans = random.randint(1, 100)
  ```
- 위의 코드를 참고해서 업다운 게임을 만드세요.
