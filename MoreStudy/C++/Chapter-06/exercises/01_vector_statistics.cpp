#include <iomanip>
#include <iostream>
#include <vector>

int main() {
    int count{};
    if (!(std::cin >> count) || count < 1 || count > 20) {
        std::cerr << "Error: invalid input.\n";
        return 1;
    }
    std::vector<int> readings;
    for (int i = 0; i < count; ++i) {
        int value{};
        if (!(std::cin >> value) || value < -100 || value > 100) {
            std::cerr << "Error: invalid input.\n";
            return 1;
        }
        readings.push_back(value);
    }
    // TODO: readings의 최소, 최대, 평균(소수 둘째 자리)을 출력합니다.
    return 0;
}
