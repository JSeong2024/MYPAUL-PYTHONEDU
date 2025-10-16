<p align='center'>
  <img src="https://capsule-render.vercel.app/api?type=soft&color=auto&section=header&text=C%+%+&fontSize=40&animation=twinkling"/>
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

- `cin`: 데이터를 입력 받는다. (`>>` 기호를 사용함)
- `cout`: 화면에 데이터를 출력한다. (`<<` 기호를 사용함)
- `endl`: 줄 바꿈을 의미 (C언어 및 Python의 '\n'과 동일)

```
#include <iostream>

int main(void) {
    std::cout << "C++ Code!!" << std::endl;
    return 0;
}
```
`C++ Code!!`

```
#include <iostream>

using namespace std;

int main(void) {
    cout << "C++ Code!!" << endl;
    return 0;
}
```
`C++ Code!!`

- using namespace std 를 추가하여 `std::`를 생략할 수 있다. [Links](https://developak.tistory.com/entry/C-C-using-namespace-std) (하지만 **권장하지는 않음**)
- [namespace의 장단점](https://99bugs.tistory.com/113#google_vignette)
- namespace의 장점: 코드 간결화
- namespace의 단점: namespace 충돌 가능성, 가독성 저하, 컴파일러 성능 저하

string 출력을 위해 헤더파일 `#include <string>`을 추가한다.
```
#include <iostream>
#include <string>

int main(void) {
  string name;
  std::cout << "이름을 입력하세요 : ";
  std::cin >> name;
  std::cout << name + "님 환영합니다." << std::endl;
  return 0;
}
```

## 연습문제
### 1.1. 1 ~ n 까지 정수의 합 구하기
```
#include <iostream>

int main(void) {
  int start_num=0, end_num=0, result=0;
  std::cout << "시작 수를 입력하세요: ";
  std::cin >> start_num;
  std::cout << "끝 수를 입력하세요: ";
  std::cin >> end_num;

  for (int i=start_num; i<=end_num; i++) {
    result +=i;
  }
  std::cout << "결과:" << result << std::endl;
  return 0;
}
```
### 1.2. 실수 5개를 입력 받아 가장 큰 수를 출력하기
```
#include <iostream>

int main(void) {
    double num[5], max_val=0;

    std::cout << "실수 5개를 입력하세요." << std::endl;

    for (int i = 0; i < 5; i++) {
        std::cout << i + 1 << "번째 숫자를 입력하세요: ";
        std::cin >> num[i];
    }

    max_val = num[0];
    for (int i = 1; i < 5; i++) {
        if (num[i] > max_val) {
            max_val = num[i];
        }
    }

    std::cout << "결과: " << max_val << std::endl;
    return 0;
}
```
