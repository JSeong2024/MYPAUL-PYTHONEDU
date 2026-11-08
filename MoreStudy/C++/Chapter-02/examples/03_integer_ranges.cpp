#include <cstdint>
#include <iostream>
#include <limits>

int main() {
    const std::int32_t position{-250};
    const std::uint16_t port{8'080};

    std::cout << "Position: " << position << '\n';
    std::cout << "Port: " << port << '\n';
    std::cout << "uint16_t maximum: "
              << std::numeric_limits<std::uint16_t>::max() << '\n';
    std::cout << "int32_t minimum: "
              << std::numeric_limits<std::int32_t>::min() << '\n';
}
