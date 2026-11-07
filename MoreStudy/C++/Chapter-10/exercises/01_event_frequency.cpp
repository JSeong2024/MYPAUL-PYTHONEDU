#include <iostream>
#include <string>

int main() {
    int n{};
    if (!(std::cin >> n) || n < 1 || n > 10'000) {
        std::cerr << "Invalid count\n";
        return 1;
    }
    // TODO: n개의 이벤트 이름을 입력받고 빈도 계산
    // TODO: 이벤트 이름을 사전순으로 정렬하여 출력
    // 예: ERROR: 1
    std::string event;
    for (int i = 0; i < n; ++i) {
        if (!(std::cin >> event)) {
            std::cerr << "Invalid event\n";
            return 1;
        }
    }
    return 0;
}
