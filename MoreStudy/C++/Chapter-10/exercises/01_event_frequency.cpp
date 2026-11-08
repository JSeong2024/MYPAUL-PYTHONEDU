#include <iostream>
#include <map>
#include <string>
#include <vector>

[[nodiscard]] std::map<std::string, int> count_events(
    const std::vector<std::string>& events) {
    // TODO: events의 등장 횟수를 이름순 map에 집계합니다.
    (void)events;
    return {};
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
