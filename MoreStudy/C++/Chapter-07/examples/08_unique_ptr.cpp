#include <iostream>
#include <memory>
#include <string>
#include <utility>

int main() {
    auto owner = std::make_unique<std::string>("sensor-A");
    std::unique_ptr<std::string> current{std::move(owner)};
    std::cout << std::boolalpha;
    std::cout << "Previous owner empty: " << (owner == nullptr) << '\n';
    if (current) {
        std::cout << "Current device: " << *current << '\n';
    }
}
