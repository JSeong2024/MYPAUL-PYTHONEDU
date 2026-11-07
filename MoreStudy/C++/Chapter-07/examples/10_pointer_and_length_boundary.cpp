#include <cstddef>
#include <cstdint>
#include <optional>
#include <print>
#include <span>

[[nodiscard]] std::optional<std::uint32_t> sum_bytes(
    const std::uint8_t* data, std::size_t length) {
    if (data == nullptr && length != 0) {
        return std::nullopt;
    }
    if (length == 0) {
        return std::uint32_t{0};
    }
    // 유효한 원본 버퍼와 길이라는 호출 계약이 충족된 경우에만 실행함.
    const std::span<const std::uint8_t> bytes{data, length};
    std::uint32_t total{0};
    for (const std::uint8_t value : bytes) {
        total += value;
    }
    return total;
}

int main() {
    const std::uint8_t bytes[]{1, 2, 3, 4};
    if (const auto total = sum_bytes(bytes, std::size(bytes))) {
        std::println("Checksum sum: {}", *total);
    }
    std::println("Invalid: {}", !sum_bytes(nullptr, 4));
}
