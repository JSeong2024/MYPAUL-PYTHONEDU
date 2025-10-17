<p align='center'>
  <img src="https://capsule-render.vercel.app/api?type=soft&color=auto&section=header&text=Data%20Visualization&fontSize=40&animation=twinkling"/>
</p>

<p align='center'>
  <a href="https://github.com/JSeong2024/2025-MYPAUL-PYTHONEDU/tree/main/PYTHON-2025-09/MoreStudy">
    <img src="https://img.shields.io/badge/Go%20To%20Back-F3EC69?&style=for-the-badge&&logoColor=white"/>
  </a>
</p>

---
# NOTES
- Last update: 2025.10.17.

# Links
- Numpy 01. https://myvelop.tistory.com/144

# GUIDE
🔗를 클릭하면 이동됩니다.
- CH 01. 자료구조(리스트, 세트, 튜플, 딕셔너리) [🔗 Click Here](https://github.com/JSeong2024/2025-MYPAUL-PYTHONEDU/blob/main/PYTHON-2025-09/MoreStudy/Data_Visualization/Data%20Visualization_CH01.pdf)
- CH 02. Numpy
- CH 03. Pandas
- CH 04. Matplotlib

---

# Data Visualization (데이터 시각화)

# 1. Python Data Structure
- [Click Here](https://github.com/JSeong2024/2025-MYPAUL-PYTHONEDU/blob/main/PYTHON-2025-09/MoreStudy/Data_Visualization/Data%20Visualization_CH01.pdf)

# 2. Numpy
## 2.1. Numpy 란?
- Numpy란 **Numerical Python**의 약자로 대규모 다차원 배열과 행렬 연산에 필요한 다양한 함수를 제공하는 라이브러리이다.
- 파이썬의 list를 개선한 형태인 Numpy의 ndarray 객체는 **더 많은 데이터를 더 빠르게 처리**할 수 있도록 도와준다.
- 넘파이는 N차원 배열 객체, 선형대수학, 푸리에 변환 및 난수 기능, 범용적 데이터 처리를 위한 다차원 컨테이너 등의 기능을 제공한다.

Numpy를 사용하기 위해서 아래와 같이 선언 해준다. (보통 `as np`까지 써주는데, 안써도 상관은 없음)
```
import numpy as np
```
numpy가 설치되어 있지 않다면,
```
pip install numpy
```
또는
```
!pip install numpy
```
명령어를 통해 numpy를 설치하면 된다.

## 2.2. array
### 2.2.1. Numpy array 란?
- array는 python의 list와 비슷한 개념이라고 생각하면 된다.
- Numpy array와 List의 차이? ([Click Here](https://wnwa.tistory.com/2))
<br />

Numpy array는 언제 쓰는가?
- Numpy array는 list에 비해서 **비교적 빠른 연산**을 지원하고 **메모리를 효율적으로 사용**할 수 있는 큰 장점을 지니고 있다.
- 비교적 빠른 연산이 가능한 이유?
  - **데이터 타입이 통일**되므로 원소의 type checking을 할 필요가 없다. 
  - 파이썬 리스트는 다양한 종류의 데이터를 한 번에 담을 수 있다. 이 때문에 연산을 할 때마다 각 원소의 데이터 타입을 확인하는 '타입 체크(type checking)' 과정이 필요하며, 이 과정은 연산 속도를 늦춤.
  - 넘파이 배열의 모든 원소는 동일한 데이터 타입을 가진다. 따라서 타입 체크 과정이 생략되어 연산이 훨씬 빠르게 진행됨.
    
- 메모리를 효율적으로 사용할 수 있는 이유?
  - **universal function**를 제공하기 때문에 같은 연산 반복에 대해 훨씬 빠르다.
  - 유니버설 함수: 넘파이가 제공하는 '유니버설 함수(ufunc)'는 배열의 모든 원소에 대해 반복적인 연산을 효율적으로 처리하는 최적화된 기능.
  - 반복문 대체: 리스트로 동일한 작업을 하려면 파이썬의 for 반복문을 사용해야 하지만, 이는 넘파이의 벡터화된(vectorized) 연산에 비해 훨씬 느리다. 넘파이는 C언어로 구현된 효율적인 함수로 이러한 반복 연산을 대체하여 속도와 메모리 효율을 모두 잡음.
  
### 2.2.2. Numpy array
Numpy 배열인 ndarray객체는 array메소드를 통해 생성할 수 있는데, 파라미터로 파이썬의 list형의 데이터를 넣어주면 된다.

```
import numpy as np
arr=np.array([1,2,3]) # import numpy 라고만 선언할 경우, arr=numpy.array([1,2,3])라고 적어줘야 함
print(arr) # [1 2 3]
```
(이하 코드에서는 import numpy as np는 적혀 있다 가정하고 생략함)

```
arr = np.array([1,2,3], dtype="float64")
print(arr) # [1. 2. 3.]
```

### 2.2.3. Numpy 메소드를 통한 array 생성

```
# 0으로 채운 길이 5의 정수 배열
np.zeros(5, dtype="int") # array([0, 0, 0, 0, 0])
print(np.zeros(5, dtype="int")) # [0 0 0 0 0]
np.zeros(5) # array([0., 0., 0., 0., 0.])
print(np.zeros(5)) # [0. 0. 0. 0. 0.]
```
```
[0 0 0 0 0]
[0. 0. 0. 0. 0.]
```
<br />

```
# 1로 채운 3x5 부동 소수점 배열
arr=np.ones((3, 5), dtype=float)
print(arr)
```
```
[[1. 1. 1. 1. 1.]
 [1. 1. 1. 1. 1.]
 [1. 1. 1. 1. 1.]]
```
<br />

```
# 3.14로 채운 2x3 배열
arr=np.full((2, 3), 3.14)
print(arr)
```
```
[[3.14 3.14 3.14]
 [3.14 3.14 3.14]]
```
<br />

```
# 3x3 단위행렬(곱했을 때 1과 같은 역할을 하는 행렬)
arr=np.eye(3)
print(arr)
```
```
[[1. 0. 0.]
 [0. 1. 0.]
 [0. 0. 1.]]
```
<br/>

np.empty는 지정된 형태와 데이터 유형을 가진 새로운 배열을 생성하지만 값은 초기화하지 않는 NumPy 함수.
```
arr=np.empty(3)
print(arr)
```
