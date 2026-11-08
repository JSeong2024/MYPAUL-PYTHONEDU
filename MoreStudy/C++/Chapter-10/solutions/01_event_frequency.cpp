#include <iostream>
#include <map>
#include <string>
#include <vector>

[[nodiscard]] std::map<std::string, int> count_events(
    const std::vector<std::string>& events) {
    std::map<std::string, int> counts;
    for (const auto& event : events) {
        ++counts[event];
    }
    return counts;
}

int main() {
    int n{};
    if (!(std::cin >> n) || n < 1 || n > 10'000) {
        std::cerr << "Error: invalid count\n";
        return 1;
    }
    std::vector<std::string> events;
    events.reserve(static_cast<std::size_t>(n));
    for (int i = 0; i < n; ++i) {
        std::string name;
        if (!(std::cin >> name)) {
            std::cerr << "Error: invalid event\n";
            return 1;
        }
        events.push_back(name);
    }
    for (const auto& [name, count] : count_events(events)) {
        std::cout << name << ": " << count << '\n';
    }
}
