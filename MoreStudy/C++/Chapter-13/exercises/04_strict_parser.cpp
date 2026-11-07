#include <concepts>
#include <expected>
#include <print>
#include <string_view>
#include <system_error>

// TODO: from_chars를 사용해 정수로 변환, 일부만 소비된 문자열은 실패 처리.
// bool은 from_chars 정수 오버로드 지원 대상이 아니므로 제외.
template <std::integral T>
    requires (!std::same_as<T, bool>)
[[nodiscard]] std::expected<T, std::errc> parse_integer(std::string_view text) {
    (void)text;
    return std::unexpected(std::errc::invalid_argument); // TODO: 교체
}

int main() {
    const auto good = parse_integer<int>("2048");
    const auto bad = parse_integer<int>("10ms");
    std::println("Parsed: {}", good.value_or(-1));
    std::println("Rejected: {}", !bad);
}
