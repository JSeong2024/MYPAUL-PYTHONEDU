#include <iostream>
#include <numeric>
#include <vector>

int main() {
    const std::vector<int> values{2, 4, 6, 8};
    const int total = std::accumulate(values.begin(), values.end(), 0);
    const int squared_sum = std::inner_product(values.begin(), values.end(),
                                               values.begin(), 0);
    std::vector<int> prefix(values.size());
    std::partial_sum(values.begin(), values.end(), prefix.begin());

    std::cout << "Total: " << total << '\n';
    std::cout << "Squared sum: " << squared_sum << '\n';
    std::cout << "Prefix:";
    for (const int value : prefix) {
        std::cout << ' ' << value;
    }
    std::cout << '\n';
}
