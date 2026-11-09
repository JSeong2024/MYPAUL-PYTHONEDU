#include <future>
#include <iostream>
#include <stdexcept>
#include <vector>

[[nodiscard]] std::vector<long long> evaluate_in_parallel(
    const std::vector<int>& inputs) {
    // TODO 1: std::launch::async로 작업을 시작하고 future를 보관합니다.
    // TODO 2: 음수 입력은 std::invalid_argument를 발생시킵니다.
    // TODO 3: future.get()으로 입력 순서에 맞는 결과를 반환합니다.
    return std::vector<long long>(inputs.size(), 0);
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
