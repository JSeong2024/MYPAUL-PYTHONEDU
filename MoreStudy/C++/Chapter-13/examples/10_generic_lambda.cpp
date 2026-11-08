#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    const std::vector readings{8, 19, 32, 7};
    const auto over_ten = [](const auto& value) { return value > 10; };
    const auto count = std::ranges::count_if(readings, over_ten);
    std::cout << "Above 10: " << count << '\n';
}
