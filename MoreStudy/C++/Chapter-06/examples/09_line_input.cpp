#include <iostream>
#include <string>

int main() {
    std::string device;
    std::cout << "Device: " << std::flush;
    if (!std::getline(std::cin, device) || device.empty()) {
        std::cerr << "Error: device name required.\n";
        return 1;
    }
    std::cout << "Registered: " << device << '\n';
}
