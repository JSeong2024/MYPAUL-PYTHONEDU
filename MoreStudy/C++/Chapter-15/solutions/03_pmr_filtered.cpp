#include <array>
#include <iostream>
#include <memory_resource>
#include <span>

namespace ch15 {
void append_valid(std::pmr::vector<int>& output, std::span<const int> input) {
    for (int value : input) {
        if (value >= 0 && value <= 100) output.push_back(value);
    }
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
