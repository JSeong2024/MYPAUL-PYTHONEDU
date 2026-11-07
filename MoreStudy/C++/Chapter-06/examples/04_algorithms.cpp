#include <algorithm>
#include <numeric>
#include <print>
#include <vector>

int main() {
    std::vector<int> delays_ms{42, 18, 31, 18, 55};
    const long long total = std::accumulate(delays_ms.begin(), delays_ms.end(), 0LL);
    const auto slow = std::ranges::count_if(delays_ms, [](int value) {
        return value >= 40;
    });

    std::ranges::sort(delays_ms);
    std::println("Total: {} ms", total);
    std::println("Slow samples: {}", slow);
    std::println("Has 31 ms: {}", std::ranges::binary_search(delays_ms, 31));
    std::println("Sorted first: {} ms", delays_ms.front());
}
