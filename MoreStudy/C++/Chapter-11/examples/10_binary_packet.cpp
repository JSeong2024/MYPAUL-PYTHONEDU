#include <array>
#include <cstdint>
#include <fstream>
#include <print>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::println(stderr, "Usage: binary_packet <path>");
        return 1;
    }
    // 명시적 8-byte 포맷: Magic(4) + Version(1) + Value(Big-Endian, 3)
    constexpr std::array<unsigned char, 8> packet{'S', 'N', 'S', '1', 1, 0, 1, 44};
    {
        std::ofstream output{argv[1], std::ios::binary | std::ios::trunc};
        if (!output) return 1;
        output.write(reinterpret_cast<const char*>(packet.data()),
                     static_cast<std::streamsize>(packet.size()));
        output.close();
        if (!output) return 1;
    }
    std::array<unsigned char, 8> restored{};
    std::ifstream input{argv[1], std::ios::binary};
    if (!input.read(reinterpret_cast<char*>(restored.data()),
                    static_cast<std::streamsize>(restored.size()))) return 1;
    if (input.peek() != std::char_traits<char>::eof()) return 1;
    if (!input.eof() && input.bad()) return 1;
    if (restored != packet) return 1;
    const std::uint32_t value = (std::uint32_t{restored[5]} << 16) |
                                (std::uint32_t{restored[6]} << 8) |
                                 std::uint32_t{restored[7]};
    std::println("Version: {}, Value: {}", restored[4], value);
}
