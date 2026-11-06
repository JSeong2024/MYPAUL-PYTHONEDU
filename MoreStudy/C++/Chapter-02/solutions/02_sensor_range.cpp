#include <charconv>
#include <cstdint>
#include <iostream>
#include <print>
#include <string>
#include <system_error>
#include <utility>

int main() {
    std::cout << "ADC (0-4095): " << std::flush;

    std::string input;
    if (!std::getline(std::cin, input)) {
        std::cerr << "Error: unable to read input.\n";
        return 1;
    }

    std::int64_t raw_adc{};
    const char* const end = input.data() + input.size();
    const auto [next, error] =
        std::from_chars(input.data(), end, raw_adc);

    if (error != std::errc{} || next != end ||
        raw_adc < 0 || raw_adc > 4'095 ||
        !std::in_range<std::uint16_t>(raw_adc)) {
        std::cerr << "Error: enter an integer from 0 to 4095.\n";
        return 1;
    }

    const auto adc = static_cast<std::uint16_t>(raw_adc);
    std::println("ADC: {}", adc);
}
