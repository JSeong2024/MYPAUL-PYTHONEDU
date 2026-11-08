#include <iostream>
#include <iterator>
#include <vector>

int main() {
    const std::vector<int> readings{12, 15, 19, 24};
    auto first = readings.cbegin();
    auto last = readings.cend();
    std::cout << "First: " << *first << '\n';
    std::cout << "Distance: " << std::distance(first, last) << '\n';

    int sum{};
    for (; first != last; ++first) {
        sum += *first;
    }
    std::cout << "Sum: " << sum << '\n';
}
