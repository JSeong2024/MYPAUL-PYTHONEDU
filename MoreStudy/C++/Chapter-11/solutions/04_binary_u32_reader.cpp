#include <array>
#include <cstdint>
#include <fstream>
#include <print>

[[nodiscard]] bool read_u32(std::istream& input, std::uint32_t& result) {
    std::array<unsigned char, 4> bytes{};
    if (!input.read(reinterpret_cast<char*>(bytes.data()),
                    static_cast<std::streamsize>(bytes.size()))) return false;
    result = (std::uint32_t{bytes[0]} << 24) |
             (std::uint32_t{bytes[1]} << 16) |
             (std::uint32_t{bytes[2]} << 8) |
              std::uint32_t{bytes[3]};
    return true;
}

int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    std::ifstream input{argv[1], std::ios::binary};
    if (!input) return 1;
    std::array<char, 4> magic{};
    if (!input.read(magic.data(), static_cast<std::streamsize>(magic.size())) ||
        magic != std::array{'C', 'N', 'T', '1'}) return 1;
    std::uint32_t count{};
    if (!read_u32(input, count) || count > 100'000) return 1;
    std::uint64_t sum{};
    for (std::uint32_t i = 0; i < count; ++i) {
        std::uint32_t value{};
        if (!read_u32(input, value)) return 1;
        sum += value;
    }
    char extra{};
    if (input.get(extra)) return 1; // 불필요한 추가 데이터
    if (input.bad() || !input.eof()) return 1;
    std::println("Count: {}", count);
    std::println("Sum: {}", sum);
}
