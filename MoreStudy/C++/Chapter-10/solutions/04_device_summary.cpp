#include <iomanip>
#include <iostream>
#include <map>
#include <string>
#include <utility>
#include <vector>

struct Stats {
    long long sum{};
    int count{};
};

[[nodiscard]] std::map<std::string, Stats> summarize(
    const std::vector<std::pair<std::string, int>>& entries) {
    std::map<std::string, Stats> result;
    for (const auto& [name, latency] : entries) {
        auto& stats = result[name];
        stats.sum += latency;
        ++stats.count;
    }
    return result;
}

int main() {
    int n{};
    if (!(std::cin >> n) || n < 1 || n > 10'000) {
        std::cerr << "Error: invalid count\n";
        return 1;
    }
    std::vector<std::pair<std::string, int>> entries;
    entries.reserve(static_cast<std::size_t>(n));
    for (int i = 0; i < n; ++i) {
        std::string name;
        int latency{};
        if (!(std::cin >> name >> latency) || latency < 0 || latency > 1'000'000) {
            std::cerr << "Error: invalid device entry\n";
            return 1;
        }
        entries.emplace_back(name, latency);
    }
    std::cout << std::fixed << std::setprecision(1);
    for (const auto& [name, stats] : summarize(entries)) {
        std::cout << name << ": count=" << stats.count
                  << ", mean=" << static_cast<double>(stats.sum) / stats.count << '\n';
    }
}
