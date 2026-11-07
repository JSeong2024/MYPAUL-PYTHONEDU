#include <print>
#include <string>

[[nodiscard]] std::string make_device_code(std::string prefix, int number) {
    prefix += '-';
    prefix += std::to_string(number);
    return prefix;
}

int main() {
    const std::string prefix{"SENSOR"};
    const std::string code{make_device_code(prefix, 3)};

    std::println("Original: {}", prefix);
    std::println("Generated: {}", code);
}
