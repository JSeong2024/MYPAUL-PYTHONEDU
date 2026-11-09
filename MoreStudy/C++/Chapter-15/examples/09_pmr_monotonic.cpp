#include <array>
#include <cstddef>
#include <iostream>
#include <memory_resource>
#include <vector>

int main() {
    alignas(std::max_align_t) std::array<std::byte, 4096> buffer{};
    // 버퍼가 부족하면 예외를 던지도록 업스트림 할당 금지.
    std::pmr::monotonic_buffer_resource arena{
        buffer.data(), buffer.size(), std::pmr::null_memory_resource()};
    std::pmr::vector<int> data{&arena};
    data.reserve(5);
    for (int value = 1; value <= 5; ++value) data.push_back(value);
    std::cout << "Items: " << data.size() << ", Last: " << data.back() << "\n";
    // arena는 data보다 먼저 생성되어 더 늦게 파괴됨.
}
