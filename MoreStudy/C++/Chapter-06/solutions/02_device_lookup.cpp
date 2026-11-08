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
    for (std::size_t i = 0; i < devices.size(); ++i) {
        if (devices[i] == target) {
            std::cout << "Found: " << devices[i] << " (index " << i + 1 << ")\n";
            return 0;
        }
    }
    std::cout << "Not found\n";
}
