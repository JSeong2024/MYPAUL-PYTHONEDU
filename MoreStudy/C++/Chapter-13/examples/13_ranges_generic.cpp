#include <array>
#include <concepts>
#include <print>
#include <ranges>
#include <utility>
#include <vector>

template <std::ranges::input_range R>
    requires std::ranges::viewable_range<R> &&
             std::convertible_to<std::ranges::range_reference_t<R>, int>
[[nodiscard]] std::vector<int> high_values(R&& readings, int threshold) {
    auto selected = std::forward<R>(readings)
                  | std::views::filter([threshold](int value) { return value >= threshold; })
                  | std::views::transform([](int value) { return value * 2; });
    return selected | std::ranges::to<std::vector>(); // C++23
}

int main() {
    const std::array readings{10, 25, 40, 15};
    const auto result = high_values(readings, 20);
    std::println("Selected: {}, first: {}", result.size(), result.front());
}
