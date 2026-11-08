# Summary — Part 01. C++ Fundamentals

Chapter 01부터 11까지 학습한 핵심 내용을 유기적으로 연결해 보는 종합 연습 자료입니다. 퀴즈로 개념을 점검한 뒤 Basic부터 Radiant 단계까지 문제를 풀어보세요.

해당 자료는 **C++20(ISO/IEC 14882:2020)** 을 바탕으로 제작되었습니다.

## Contents

| 자료 | 구성 |
|:---|:---|
| [Quiz](./quiz.md) | 객관식 12문항, 주관식·서술형 8문항과 정답 및 해설 |
| [Problems](./problem.md) | Basic 6, Advanced 5, Challenge 3, Radiant 1문제 |
| [HTML 문제집](./Summary-Part-01.html) | 문제별 이동, 객관식 선택, 해설 및 구현 가이드 |
| [학생용 코드](./exercises/) | 각 문제의 미완성 코드 |
| [모범답안](./solutions/) | 독립적으로 실행 가능한 정답 코드 |
| [자동 검증](./tests/check.py) | 컴파일·입출력·파일 결과 테스트 |

## Getting Started

[Quiz](./quiz.md)로 핵심 개념을 확인하고, [Problems](./problem.md)의 입출력 규칙과 검증 사항을 먼저 읽어보세요. 브라우저에서는 [HTML 문제집](./Summary-Part-01.html)을 열면 됩니다.

Windows의 Git Bash에서 저장소 최상위 폴더를 기준으로 실행하는 예시입니다.

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic 'MoreStudy/C++/Summary-Part-01/exercises/B-01.cpp' -o basic01
./basic01
```

모범답안 확인은 `exercises` 대신 `solutions`를 사용합니다. 학생용 코드는 미완성이므로 정답 검증에 실패하는 것이 정상입니다.

```bash
python 'MoreStudy/C++/Summary-Part-01/tests/check.py' --compiler g++
python 'MoreStudy/C++/Summary-Part-01/tests/check.py' --compiler clang++
```

검증 스크립트는 Python 3을 사용하며, 컴파일 결과와 입력·출력 파일은 임시 폴더에서 처리합니다.

## Problems 구성

| 단계 | 문제 수 | 목표 |
|---|---:|---|
| Basic | 6 | 기본 문법과 입력 검증 |
| Advanced | 5 | 자료형·참조·정렬·파싱의 정확한 판단 |
| Challenge | 3 | 현실적인 파일 처리 및 다중 조건 해결 |
| Radiant | 1 | 오류 처리·재현성·정산 검증·성능 분석 |

## Directory Structure

```text
Summary-Part-01/
├── README.md
├── quiz.md
├── problem.md
├── Summary-Part-01.html
├── exercises/        # B-01.cpp ~ R-01.cpp
├── solutions/        # 모범답안과 Radiant 참고 문서
└── tests/
    └── check.py
```

## References

- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- [C++ Reference](https://en.cppreference.com/w/cpp)

[← Summary 목차](./README.md) · [Quiz](./quiz.md) · [Problems](./problem.md) · [HTML 문제집](./Summary-Part-01.html) · [← C++ 목차](../README.md#contents)
