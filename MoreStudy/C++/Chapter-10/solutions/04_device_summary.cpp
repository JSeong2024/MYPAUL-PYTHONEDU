#include <cstdio>
#include <cstdint>
#include <iostream>
#include <map>
#include <print>
#include <string>

struct Aggregate {
    std::int64_t total{};
    int count{};
};

int main() {
    int n{};
    if (!(std::cin >> n) || n < 1 || n > 10'000) {
        std::println(stderr, "Invalid count");
        return 1;
    }
    std::map<std::string, Aggregate> devices;
    for (int i = 0; i < n; ++i) {
        std::string device;
        int latency{};
        if (!(std::cin >> device >> latency) || latency < 0 || latency > 1'000'000) {
            std::println(stderr, "Invalid reading");
            return 1;
        }
        auto& entry = devices[device];
        entry.total += latency;
        ++entry.count;
    }
    for (const auto& [device, entry] : devices) {
        const double mean = static_cast<double>(entry.total) / entry.count;
        std::println("{}: count={}, mean={:.1f}", device, entry.count, mean);
    }
}
