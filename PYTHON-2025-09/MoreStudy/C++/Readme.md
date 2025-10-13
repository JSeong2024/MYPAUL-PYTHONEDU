<p align='center'>
  <img src="https://capsule-render.vercel.app/api?type=soft&color=auto&section=header&text=C%+%+&fontSize=40&animation=twinkling"/>
</p>

<p align='center'>
  <a href="https://github.com/JSeong2024/2025-MYPAUL-PYTHONEDU/tree/main/PYTHON-2025-09/MoreStudy">
    <img src="https://img.shields.io/badge/Go%20To%20Back-F3EC69?&style=for-the-badge&&logoColor=white"/>
  </a>
</p>

---

# Links
- 표준 라이브러리: https://chaoyue.tistory.com/38

---
# Colab에서 C++ 실행하기
C나 C++은 전용 컴파일러로 실행하는 것을 추천하지만, Colab에서 테스트하고 싶다면 다음의 방법을 사용하면 됨.

1. GNU C++ 컴파일러 설치
```
# G++ Complier 설치
!apt-get install g++
```

2. `%%writefile test1.cpp`를 적어야 그 아래에 C++ 코드를 작성할 수 있음.
```
%%writefile (파일 이름).cpp
(C++ 코드 작성)
```

3. 코드 컴파일 및 실행
```
!g++ (실행할 파일 이름).cpp -o (컴파일 후 저장될 파일 이름)
!./(컴파일된 파일 이름)
```

---

# 1. cout, cin, endl, string
- [Links](https://y-min.tistory.com/8)

```
#include <iostream>

int main() {
    std::cout << "C++ Code!!" << std::endl;
    return 0;
}
```
`C++ Code!!`

```
#include <iostream>

using namespace std;

int main() {
    cout << "C++ Code!!" << endl;
    return 0;
}
```
`C++ Code!!`

- `cin`: 데이터를 입력 받는다. (`>>` 기호를 사용함)
- `cout`: 화면에 데이터를 출력한다. (`<<` 기호를 사용함)
- `endl`: 줄 바꿈을 의미 (C언어 및 Python의 '\n'과 동일)

- 
