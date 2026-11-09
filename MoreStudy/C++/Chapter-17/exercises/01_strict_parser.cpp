#include <optional>
#include <string_view>
// 입력 전체가 0 이상의 십진 정수여야 한다. 공백, 부호, 범위 초과는 거부.
std::optional<int> parse_count(std::string_view text) {
    // TODO: std::from_chars와 결과 포인터로 전체 소비·오류 확인
    (void)text;
    return std::nullopt;
}
#ifndef CH17_LIBRARY_ONLY
#include <iostream>
int main(){std::cout << "parse_count: TODO\n";}
#endif
