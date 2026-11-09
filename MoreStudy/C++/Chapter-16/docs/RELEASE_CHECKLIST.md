# Chapter 16 — Build & Release Checklist

## 빌드 정확성

- [ ] GCC·Clang에서 C++20 표준 모드 확인
- [ ] Debug·Release의 CTest 모두 통과
- [ ] `NDEBUG` 정의 여부와 관계없이 테스트 실패 감지
- [ ] 공개 Header를 독립 소비자 프로젝트에서 직접 포함 가능
- [ ] Include 경로와 컴파일 요구사항의 PUBLIC/PRIVATE 범위 확인

## 라이브러리 배포

- [ ] 설치 대상이 빌드 폴더의 절대 경로를 포함하지 않는지 점검
- [ ] 외부 프로젝트의 `find_package(... CONFIG REQUIRED)` 성공
- [ ] 설치 경로를 옮긴 뒤 소비자 재빌드·실행
- [ ] 라이브러리 버전 및 호환성 정책 확인
- [ ] 타사 의존성의 버전·라이선스·출처 관리

## 작업 환경

- [ ] `build/`·`out/` 등 생성물 Git 제외
- [ ] `CMakePresets.json`은 공유, `CMakeUserPresets.json`은 로컬 유지
- [ ] 툴체인 차이·배포 플랫폼 차이 문서화
- [ ] 변경 후 테스트와 CI 상태 확인

**주의:** CMake 설정만으로 바이너리의 바이트 단위 재현성이나 모든 플랫폼에서의 ABI 호환성이 자동으로 보장되지는 않습니다.
