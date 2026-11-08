#include <algorithm>
#include <iostream>
#include <iterator>
#include <ranges>
#include <vector>

int main() {
    const std::vector<int> readings{8, 15, 23, 4, 19};
    auto high_values = readings | std::views::filter([](int value) {
        return value >= 15;
    });

    // C++20에서는 ranges::copy와 back_inserter로 뷰를 소유 컨테이너에 복사합니다.
    std::vector<int> selected;
    std::ranges::copy(high_values, std::back_inserter(selected));
    std::cout << "Selected:";
    for (const int value : selected) {
        std::cout << ' ' << value;
    }
    std::cout << '\n';
}
