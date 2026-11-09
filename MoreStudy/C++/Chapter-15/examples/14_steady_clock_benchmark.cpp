#include <chrono>
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    const std::vector<int> values(1000, 2);
    constexpr int repetitions = 5;
    long long checksum = 0;
    for (int trial = 0; trial < repetitions; ++trial) {
        const auto start = std::chrono::steady_clock::now();
        checksum += std::accumulate(values.begin(), values.end(), 0LL);
        const auto elapsed = std::chrono::steady_clock::now() - start;
        (void)elapsed; // 실제 측정 시 여러 반복의 분포를 기록하고 분석할 것.
    }
    std::cout << "Trials: " << repetitions << ", Checksum: " << checksum << "\n";
}
