#include <iostream>
#include <print>
#include <string>

int main() {
    std::cout << "Device name: " << std::flush;
    std::string name;

    if (!std::getline(std::cin, name) || name.empty() || name.size() > 80) {
        std::println(stderr, "Invalid device name");
        return 1;
    }

    std::println("Registered: {}", name);
}
