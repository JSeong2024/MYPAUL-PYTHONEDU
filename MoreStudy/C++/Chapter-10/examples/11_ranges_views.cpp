#include <iostream>
#include <ranges>
#include <vector>

int main() {
    std::vector<int> readings{10, 21, 30, 42, 50};
    auto selected = readings
        | std::views::filter([](int value) { return value >= 20; })
        | std::views::transform([](int value) { return value / 2; });

    std::cout << "Half of >=20:";
    for (const int value : selected) {
        std::cout << ' ' << value;
    }
    std::cout << '\n';
}
