#include <cstddef>
#include <iostream>
#include <span>
#include <stdexcept>
#include <thread>
#include <vector>

[[nodiscard]] long long parallel_sum(std::span<const int> numbers,
                                     std::size_t worker_count) {
    // TODO 1: worker_count를 1~32 범위로 검증합니다.
    // TODO 2: 입력 데이터를 분할하고 std::jthread를 생성합니다.
    // TODO 3: 스레드별 부분 합을 만든 후 join하고 합산합니다.
    (void)numbers;
    (void)worker_count;
    return 0;
}

#ifndef CH14_LIBRARY_ONLY
int main() {
    const std::vector<int> numbers{10, 20, 30, 40, 50};
    std::cout << "Sum: " << parallel_sum(numbers, 3) << '\n';
}
#endif
