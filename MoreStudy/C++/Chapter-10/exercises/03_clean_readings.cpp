#include <iostream>

int main() {
    int n{};
    if (!(std::cin >> n) || n < 1 || n > 10'000) {
        std::cerr << "Invalid count\n";
        return 1;
    }
    // TODO: -1은 무효 데이터로 제외, 0~1000의 측정값만 허용
    // TODO: 유효한 측정값을 오름차순으로 정렬하고 중복 제거
    // TODO: 유효한 값이 없으면 EMPTY 출력
    for (int i = 0, value{}; i < n; ++i) {
        if (!(std::cin >> value) || value < -1 || value > 1'000) {
            std::cerr << "Invalid reading\n";
            return 1;
        }
    }
    return 0;
}
