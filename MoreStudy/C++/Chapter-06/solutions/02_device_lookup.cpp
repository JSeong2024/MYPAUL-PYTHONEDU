#include <iostream>
#include <print>
#include <string>
#include <utility>
#include <vector>

int main() {
    int count{};
    if (!(std::cin >> count) || count < 1 || count > 20) {
        std::println(stderr, "Invalid device count");
        return 1;
    }

    std::string ignored;
    std::getline(std::cin, ignored);

    std::vector<std::string> devices;
    devices.reserve(static_cast<std::size_t>(count));
    for (int i = 0; i < count; ++i) {
        std::string name;
        if (!std::getline(std::cin, name) || name.empty() || name.size() > 60) {
            std::println(stderr, "Invalid device name");
            return 1;
        }
        devices.push_back(std::move(name));
    }

    std::string query;
    if (!std::getline(std::cin, query) || query.empty() || query.size() > 60) {
        std::println(stderr, "Invalid query");
        return 1;
    }

    for (std::size_t i = 0; i < devices.size(); ++i) {
        if (devices[i] == query) {
            std::println("Found: {} (index {})", devices[i], i + 1);
            return 0;
        }
    }
    std::println("Not found");
}
