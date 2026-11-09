// 결함 재현 전용. 학습 외 사용 금지. AddressSanitizer로만 실행 권장.
#include <iostream>
#include <vector>
int main() {
 std::vector<int> values{1,2,3};
 volatile std::size_t index=3;
 std::cout<<values[index]<<'\n'; // 의도적인 범위 초과: 정의되지 않은 동작
}
