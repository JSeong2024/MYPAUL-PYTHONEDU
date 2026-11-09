# CI 검증 정책

Chapter 17은 다음 흐름으로 검증합니다.

1. **컴파일 경고 확인:** GCC와 Clang의 C++20 `-Wall -Wextra -Wpedantic`.
2. **행동 테스트:** `python3 tests/check.py --compiler <컴파일러>`.
3. **CMake·CTest:** Basic·Advanced·Pro 개별 프로젝트의 테스트.
4. **외부 소비자:** Pro 라이브러리를 임시 위치에 설치한 뒤 다른 경로로 옮겨 `find_package()`로 빌드.
5. **Sanitizer:** 로컬 또는 독립된 선택적 CI 작업에서 ASan·UBSan을 수행.
6. **성능 분석:** 결과 정확성 검증 후 별도 벤치마크에서 수행. 공용 CI에서는 고정 속도 임계값을 사용하지 않음.

**학생용 코드 검증:** 학생용 `exercises/` 및 `projects/`의 TODO는 완료하기 전까지 실패하는 것이 정상입니다. 기본 CI는 모범답안을 검사합니다.

**결함 예제:** `buglab/`은 의도적으로 잘못된 코드를 포함하며 일반 컴파일·CTest 대상에서 제외합니다. 안전한 수정본만 기본 검사에 포함합니다.

모든 작업은 외부 테스트 프레임워크 없이 표준 라이브러리·CMake·Python 기본 모듈만 사용합니다.
