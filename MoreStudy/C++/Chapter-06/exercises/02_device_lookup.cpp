#include <iostream>
#include <print>
#include <string>
#include <vector>

int main() {
    // 첫 줄: 장치 개수 N(1~20)
    // 다음 N줄: 장치명(공백 포함 가능, 1~60바이트)
    // 마지막 줄: 조회할 장치명
    int count{};
    if (!(std::cin >> count) || count < 1 || count > 20) {
        std::println(stderr, "Invalid device count");
        return 1;
    }

    std::string ignored;
    std::getline(std::cin, ignored);  // 개수 뒤 줄바꿈 제거
    std::vector<std::string> devices;

    // TODO: getline()으로 이름을 저장하고 입력 오류를 검증함.
    // TODO: 마지막 줄의 이름을 찾아 1부터 시작하는 위치를 출력함.
    // 출력: Found: 이름 (index N) / Not found
    std::println("TODO: implement device lookup");
}
