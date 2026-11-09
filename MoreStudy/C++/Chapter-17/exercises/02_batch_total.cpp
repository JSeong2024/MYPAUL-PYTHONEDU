#include <span>
#include <stdexcept>
// 0..100 범위를 벗어난 값은 invalid_argument. 유효한 값의 합을 반환.
int batch_total(std::span<const int> readings) {
    // TODO: 모든 원소 검증 후 합계 계산. 입력은 최대 10000개.
    (void)readings;
    return 0;
}
#ifndef CH17_LIBRARY_ONLY
#include <iostream>
int main(){std::cout << "batch_total: TODO\n";}
#endif
