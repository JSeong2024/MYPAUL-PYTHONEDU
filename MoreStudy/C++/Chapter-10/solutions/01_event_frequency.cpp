#include <cstdio>
#include <iostream>
#include <map>
#include <print>
#include <string>

int main() {
    int n{};
    if (!(std::cin >> n) || n < 1 || n > 10'000) {
        std::println(stderr, "Invalid count");
        return 1;
    }
    std::map<std::string, int> counts;
    for (int i = 0; i < n; ++i) {
        std::string event;
        if (!(std::cin >> event)) {
            std::println(stderr, "Invalid event");
            return 1;
        }
        ++counts[event];
    }
    for (const auto& [event, count] : counts) {
        std::println("{}: {}", event, count);
    }
}
