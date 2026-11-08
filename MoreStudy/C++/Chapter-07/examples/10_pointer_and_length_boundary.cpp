#include <cstddef>
#include <cstdint>
#include <iostream>
#include <iterator>
#include <optional>
#include <span>

[[nodiscard]] std::optional<unsigned long long> sum_bytes(
    const std::uint8_t* data, std::size_t length) {
    if (data == nullptr && length != 0) {
        return std::nullopt;
    }
    if (length == 0) {
        return 0ULL;
    }
    // Caller must guarantee a valid buffer with at least 'length' elements.
    const std::span<const std::uint8_t> bytes{data, length};
    unsigned long long total{};
    for (const std::uint8_t value : bytes) {
        total += value;
    }
    return total;
}

int main() {
    const std::uint8_t bytes[]{1, 2, 3, 4};
    std::cout << "Checksum sum: " << *sum_bytes(bytes, std::size(bytes)) << '\n';
    std::cout << std::boolalpha;
    std::cout << "Invalid: " << !sum_bytes(nullptr, 4) << '\n';
}
