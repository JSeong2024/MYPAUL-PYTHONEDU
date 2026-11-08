#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> channels{9, 2, 7, 2, 5};
    std::ranges::sort(channels);

    const bool has_seven = std::ranges::binary_search(channels, 7);
    const auto first_two = std::ranges::lower_bound(channels, 2);
    std::cout << std::boolalpha << "Has 7: " << has_seven << '\n';
    std::cout << "First 2 index: " << (first_two - channels.begin()) << '\n';
}
