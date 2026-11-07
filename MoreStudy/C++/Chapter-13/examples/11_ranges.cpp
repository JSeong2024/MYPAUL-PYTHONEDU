#include <algorithm>
#include <array>
#include <iterator>
#include <print>
#include <ranges>
#include <vector>

int main() {
    const std::array readings{10, 25, 40, 15};
    auto selected = readings
        | std::views::filter([](int x) { return x >= 20; })
        | std::views::transform([](int x) { return x * 2; });

#ifdef __cpp_lib_ranges_to_container
    const auto output = selected | std::ranges::to<std::vector<int>>();
#else
    std::vector<int> output;
    std::ranges::copy(selected, std::back_inserter(output));
#endif
    std::println("Selected: {}", output.size());
    for (int x : output) std::println("{}", x);
}
