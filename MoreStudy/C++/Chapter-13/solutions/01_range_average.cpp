#include <concepts>
#include <cstddef>
#include <optional>
#include <print>
#include <ranges>
#include <vector>

template <std::ranges::input_range R>
    requires std::convertible_to<std::ranges::range_reference_t<R>, double>
[[nodiscard]] std::optional<double> mean(R&& values) {
    long double total{};
    std::size_t count{};
    for (const auto& value : values) {
        total += static_cast<long double>(value);
        ++count;
    }
    if (count == 0) return std::nullopt;
    return static_cast<double>(total / static_cast<long double>(count));
}

int main() {
    const std::vector values{10, 20, 30};
    if (const auto result = mean(values)) std::println("Mean: {:.1f}", *result);
    const std::vector<int> empty;
    std::println("Empty has mean: {}", mean(empty).has_value());
}
