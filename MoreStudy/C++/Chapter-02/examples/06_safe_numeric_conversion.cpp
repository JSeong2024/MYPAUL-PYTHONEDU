#include <cstdint>
#include <iostream>
#include <print>
#include <utility>

int main() {
    const std::int64_t raw_adc{3'872};
    constexpr std::int64_t max_adc{4'095};

    if (raw_adc < 0 || raw_adc > max_adc ||
        !std::in_range<std::uint16_t>(raw_adc)) {
        std::cerr << "Error: ADC value is out of range.\n";
        return 1;
    }

    const auto adc = static_cast<std::uint16_t>(raw_adc);
    std::println("ADC value: {}", adc);
}
