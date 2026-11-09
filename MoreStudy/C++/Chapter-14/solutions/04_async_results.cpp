#include <future>
#include <iostream>
#include <stdexcept>
#include <vector>

[[nodiscard]] std::vector<long long> evaluate_in_parallel(
    const std::vector<int>& inputs) {
    std::vector<std::future<long long>> pending;
    pending.reserve(inputs.size());
    for (const int value : inputs) {
        pending.push_back(std::async(std::launch::async, [value] {
            if (value < 0) throw std::invalid_argument("negative input");
            return static_cast<long long>(value) * value;
        }));
    }
    std::vector<long long> results;
    results.reserve(inputs.size());
    for (auto& future : pending) results.push_back(future.get());
    return results;
}

#ifndef CH14_LIBRARY_ONLY
int main() {
    const auto results = evaluate_in_parallel({2, 4, 6});
    std::cout << "Results: ";
    for (std::size_t i = 0; i < results.size(); ++i) {
        if (i != 0) std::cout << ", ";
        std::cout << results[i];
    }
    std::cout << '\n';
}
#endif
