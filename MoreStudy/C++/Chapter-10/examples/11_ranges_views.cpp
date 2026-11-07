#include <print>
#include <ranges>
#include <vector>

int main() {
    const std::vector<int> readings{12, 4, 20, 15, 8};
    auto processed = readings
        | std::views::filter([](int value) { return value >= 10; })
        | std::views::transform([](int value) { return value * 2; })
        | std::views::take(2);
    for (const int value : processed) {
        std::println("Processed: {}", value);
    }
}
