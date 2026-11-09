#include <cstddef>
#include <span>
#include <stdexcept>
#include <vector>
// window가 0이거나 데이터 길이보다 크면 invalid_argument.
// 각 연속 구간의 최댓값을 입력 순서대로 반환.
std::vector<int> rolling_max(std::span<const int> values, std::size_t window) {
    // TODO: 경계값 및 결과 순서를 확인하며 구현
    (void)values; (void)window;
    return {};
}
#ifndef CH17_LIBRARY_ONLY
#include <iostream>
int main(){std::cout << "rolling_max: TODO\n";}
#endif
