#include <iostream>
#include <string>

int main() {
    int n{};
    if (!(std::cin >> n) || n < 1 || n > 10'000) {
        std::cerr << "Invalid count\n";
        return 1;
    }
    // TODO: 장치별 측정 횟수와 합계를 기록
    // TODO: 장치 이름 오름차순으로 횟수와 평균(소수 첫째 자리) 출력
    std::string device;
    int latency{};
    for (int i = 0; i < n; ++i) {
        if (!(std::cin >> device >> latency) || latency < 0 || latency > 1'000'000) {
            std::cerr << "Invalid reading\n";
            return 1;
        }
    }
    return 0;
}
