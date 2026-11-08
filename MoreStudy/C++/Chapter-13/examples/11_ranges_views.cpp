#include <iostream>
#include <ranges>
#include <vector>

int main() {
    const std::vector readings{5, 12, 19, 20, 7};
    auto selected = readings
        | std::views::filter([](int n) { return n >= 10; })
        | std::views::transform([](int n) { return n * 2; });
    std::vector<int> output;
    for (int value : selected) output.push_back(value);
    std::cout << "Selected:";
    for (int value : output) std::cout << ' ' << value;
    std::cout << '\n';
}
