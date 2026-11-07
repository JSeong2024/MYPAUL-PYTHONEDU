#include <print>

int main() {
    constexpr bool connected{true};
    constexpr double temperature_c{78.5};
    constexpr int sample_count{0};
    constexpr int total_samples{120};

    const bool overheating = connected && temperature_c >= 75.0;
    const bool has_high_average =
        sample_count != 0 && total_samples / sample_count > 30;

    std::println("Overheating: {}", overheating);
    std::println("High average: {}", has_high_average);
}
