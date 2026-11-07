#include <array>
#include <numeric>
#include <print>

int main() {
    constexpr std::array<int, 4> latencies{20, 30, 10, 40};
    const long long sum = std::accumulate(latencies.begin(), latencies.end(), 0LL);
    const double mean = static_cast<double>(sum) / latencies.size();
    constexpr std::array<int, 4> weights{1, 2, 1, 2};
    const int weighted = std::inner_product(latencies.begin(), latencies.end(),
                                            weights.begin(), 0);
    std::println("Mean: {:.1f} ms", mean);
    std::println("Weighted sum: {}", weighted);
}
