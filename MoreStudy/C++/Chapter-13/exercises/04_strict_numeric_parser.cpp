#include <concepts>
#include <expected>
#include <print>
#include <string_view>
#include <system_error>

// TODO: std::integral T에 대해 문자열을 정확히 숫자로 변환
// TODO: std::from_chars를 사용하고 문자열 끝까지 소비됐는지 확인
// TODO: 실패 시 std::unexpected(std::errc::invalid_argument) 등 반환

template <std::integral T>
[[nodiscard]] std::expected<T, std::errc> parse(std::string_view text) {
    (void)text;
    return std::unexpected(std::errc::invalid_argument);
}

int main() {
    const auto result = parse<int>("120");
    std::println("Parsed: {}", result.has_value());
}
