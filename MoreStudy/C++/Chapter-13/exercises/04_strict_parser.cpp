#include <charconv>
#include <iostream>
#include <optional>
#include <string_view>
#include <system_error>

[[nodiscard]] std::optional<int> parse_port(std::string_view text) {
    // TODO: 빈 문자열과 숫자가 아닌 문자열을 거부
    // TODO: std::from_chars 변환 후 끝까지 소비했는지 확인
    // TODO: 1..65535 범위만 인정
    (void)text;
    return std::nullopt;
}

#ifndef CH13_LIBRARY_ONLY
int main() {
    std::cout << parse_port("8080").value_or(-1) << '\n';
}
#endif
