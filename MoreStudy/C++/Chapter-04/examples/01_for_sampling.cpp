#include <print>

int main() {
    constexpr int sample_count{5};
    int total{};

    for (int i{0}; i < sample_count; ++i) {
        const int sample{10 + 2 * i};
        total += sample;
        std::println("Sample {}: {}", i + 1, sample);
    }

    std::println("Total: {}", total);
}
