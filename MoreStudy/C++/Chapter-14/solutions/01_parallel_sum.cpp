#include <algorithm>
#include <cstddef>
#include <iostream>
#include <span>
#include <stdexcept>
#include <thread>
#include <vector>

[[nodiscard]] long long parallel_sum(std::span<const int> numbers,
                                     std::size_t worker_count) {
    if (worker_count == 0 || worker_count > 32)
        throw std::invalid_argument("worker_count must be 1..32");
    if (numbers.empty()) return 0;
    const std::size_t count = std::min(worker_count, numbers.size());
    std::vector<long long> partial(count, 0);
    std::vector<std::jthread> threads;
    threads.reserve(count);
    for (std::size_t i = 0; i < count; ++i) {
        threads.emplace_back([&, i] {
            const auto begin = i * numbers.size() / count;
            const auto end = (i + 1) * numbers.size() / count;
            for (auto j = begin; j < end; ++j)
                partial[i] += numbers[j];
        });
    }
    for (auto& thread : threads) thread.join();
    long long result = 0;
    for (const auto value : partial) result += value;
    return result;
}

#ifndef CH14_LIBRARY_ONLY
int main() {
    const std::vector<int> numbers{10, 20, 30, 40, 50};
    std::cout << "Sum: " << parallel_sum(numbers, 3) << '\n';
}
#endif
