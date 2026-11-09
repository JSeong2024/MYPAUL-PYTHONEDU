#include <array>
#include <iostream>
#include <memory_resource>
#include <span>

namespace ch15 {
void append_valid(std::pmr::vector<int>& output, std::span<const int> input) {
    // TODO: 0 이상 100 이하의 값만 기존 output 뒤에 추가하세요.
    //       output의 할당자를 교체하거나 임시 자원을 반환하지 마세요.
    (void)output;
    (void)input;
}
}
#ifndef CH15_LIBRARY_ONLY
int main() {
    std::pmr::monotonic_buffer_resource arena;
    std::pmr::vector<int> output{&arena};
    const std::array input{20, -1, 80, 150};
    ch15::append_valid(output, input);
    std::cout << "Accepted: " << output.size() << "\n";
}
#endif
