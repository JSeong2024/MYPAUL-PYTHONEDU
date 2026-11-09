#include <cstddef>
#include <iostream>

// 64바이트는 설명용 정렬 예시이며, CPU의 캐시 라인 크기와 항상 같지는 않음.
struct alignas(64) PaddedCounter { int value{}; };
int main() {
    const PaddedCounter counters[2]{{10}, {20}};
    std::cout << std::boolalpha << "Alignment >= 64: "
              << (alignof(PaddedCounter) >= 64) << "\n";
    std::cout << "Values: " << counters[0].value + counters[1].value << "\n";
}
