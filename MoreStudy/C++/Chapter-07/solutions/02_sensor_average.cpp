#include <array>
#include <optional>
#include <print>
#include <span>

[[nodiscard]] std::optional<double> average(std::span<const int> samples) {
    if (samples.empty()) {
        return std::nullopt;
    }
    double sum{0.0};
    for (const int sample : samples) {
        sum += sample;
    }
    return sum / static_cast<double>(samples.size());
}

int main() {
    const std::array readings{10, 20, 30, 40};
    if (const auto value = average(readings)) {
        std::println("Average: {:.1f}", *value);
    }
    const std::span<const int> empty{};
    std::println("Empty: {}", !average(empty));
}
