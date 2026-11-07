#include <algorithm>
#include <iterator>
#include <numeric>
#include <print>
#include <vector>

int main() {
    const std::vector<int> seconds{2, 3, 5};
    std::vector<int> milliseconds;
    milliseconds.reserve(seconds.size());
    std::ranges::transform(seconds, std::back_inserter(milliseconds), [](int value) {
        return value * 1'000;
    });
    const long long total = std::accumulate(milliseconds.begin(),
                                            milliseconds.end(), 0LL);
    std::println("Total: {} ms", total);
    std::println("Converted items: {}", milliseconds.size());
}
