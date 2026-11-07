#include <fstream>
#include <print>
#include <string>

// 구분자: |  형식: LEVEL|DEVICE|MESSAGE
// LEVEL: INFO / WARN / ERROR. MESSAGE에는 | 문자가 포함될 수 있음.
// 빈 필드 또는 알 수 없는 LEVEL을 만나면 비정상 종료.
int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    std::ifstream input{argv[1]};
    if (!input) return 1;
    std::string line;
    // TODO: 앞의 두 구분자 위치를 찾고 필드 검증
    // TODO: 레벨별 개수 계산 및 INFO/WARN/ERROR 순서로 출력
    std::println("TODO");
}
