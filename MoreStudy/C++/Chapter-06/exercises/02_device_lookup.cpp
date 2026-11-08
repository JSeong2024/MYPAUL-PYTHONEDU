#include <iostream>
#include <string>
#include <vector>

int main() {
    int count{};
    if (!(std::cin >> count) || count < 1 || count > 10) {
        std::cerr << "Error: invalid input.\n";
        return 1;
    }
    std::string remainder;
    std::getline(std::cin, remainder);
    if (!remainder.empty()) {
        std::cerr << "Error: invalid input.\n";
        return 1;
    }
    std::vector<std::string> devices;
    for (int i = 0; i < count; ++i) {
        std::string device;
        if (!std::getline(std::cin, device) || device.empty()) {
            std::cerr << "Error: invalid input.\n";
            return 1;
        }
        devices.push_back(device);
    }
    std::string target;
    if (!std::getline(std::cin, target) || target.empty()) {
        std::cerr << "Error: invalid input.\n";
        return 1;
    }
    // TODO: target과 정확히 같은 이름을 가진 첫 장치의 1부터 시작하는 위치 출력
    // TODO: 찾지 못하면 Not found 출력
    return 0;
}
