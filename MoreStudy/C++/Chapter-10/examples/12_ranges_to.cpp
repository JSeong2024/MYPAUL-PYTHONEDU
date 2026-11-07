#include <algorithm>
#include <iterator>
#include <print>
#include <ranges>
#include <vector>

int main() {
    auto squares = std::views::iota(1, 7)
        | std::views::filter([](int value) { return value % 2 == 0; })
        | std::views::transform([](int value) { return value * value; });

#if defined(__cpp_lib_ranges_to_container) && __cpp_lib_ranges_to_container >= 202202L
    const auto result = std::ranges::to<std::vector<int>>(squares);
#else
    std::vector<int> result;
    std::ranges::copy(squares, std::back_inserter(result));
#endif

    for (const int value : result) {
        std::println("Square: {}", value);
    }
}
