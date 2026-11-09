#include <cstddef>
#include <iostream>
#include <vector>

namespace ch15 {
[[nodiscard]] std::vector<int> make_squares(std::size_t count) {
    // TODO: count개 원소를 담을 수 있도록 메모리를 미리 확보하고,
    //       0, 1, 4, 9, ... 순서로 벡터를 반환하세요. (count <= 10000)
    (void)count;
    return {};
}
}
#ifndef CH15_LIBRARY_ONLY
int main() {
    const auto values = ch15::make_squares(5);
    std::cout << "Count: " << values.size() << "\n";
    if (!values.empty()) std::cout << "Last: " << values.back() << "\n";
}
#endif
