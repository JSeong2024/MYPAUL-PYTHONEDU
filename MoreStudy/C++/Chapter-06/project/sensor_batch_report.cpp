#include <iostream>
#include <string>
#include <vector>

int main() {
    std::string device;
    std::string csv;
    std::cout << "Device: " << std::flush;
    if (!std::getline(std::cin, device) || device.empty()) {
        std::cerr << "Error: invalid device.\n";
        return 1;
    }
    std::cout << "Readings (-100 to 100, comma-separated): " << std::flush;
    if (!std::getline(std::cin, csv)) {
        std::cerr << "Error: invalid readings.\n";
        return 1;
    }
    // TODO: csv를 1~20개의 정수로 나누고, 각 값을 검증합니다.
    // TODO: 원본을 유지한 채 정렬한 값을 출력하고 통계를 계산합니다.
    std::cerr << "Error: invalid readings.\n";
    return 1;
}
