#include <array>
#include <print>

int main() {
    constexpr std::array readings{120, 135, 119, 142};
    int total{};

    for (const int reading : readings) {
        total += reading;
    }

    std::println("Samples: {}", readings.size());
    std::println("Total: {}", total);
}
