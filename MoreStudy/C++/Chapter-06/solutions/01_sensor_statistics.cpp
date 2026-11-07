#include <algorithm>
#include <iostream>
#include <print>
#include <vector>

int main() {
    int count{};
    if (!(std::cin >> count) || count < 1 || count > 1'000) {
        std::println(stderr, "Invalid sample count");
        return 1;
    }

    std::vector<int> samples;
    samples.reserve(static_cast<std::size_t>(count));
    long long sum{};
    for (int i = 0; i < count; ++i) {
        int value{};
        if (!(std::cin >> value) || value < -1'000'000 || value > 1'000'000) {
            std::println(stderr, "Invalid sample");
            return 1;
        }
        samples.push_back(value);
        sum += value;
    }

    const auto [minimum, maximum] = std::ranges::minmax(samples);
    std::println("Count: {}", samples.size());
    std::println("Min: {}", minimum);
    std::println("Max: {}", maximum);
    std::println("Average: {:.2f}", static_cast<double>(sum) / samples.size());
}
