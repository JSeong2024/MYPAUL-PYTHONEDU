#include <cstdint>
#include <iostream>
#include <utility>

int main() {
    const double measurement{8.9};
    const int whole_part{static_cast<int>(measurement)};
    const int sample_id{300};
    const bool fits_in_byte{std::in_range<std::uint8_t>(sample_id)};

    std::cout << std::boolalpha;
    std::cout << "Measurement: " << measurement << '\n';
    std::cout << "Whole part: " << whole_part << '\n';
    std::cout << "Fits in uint8_t: " << fits_in_byte << '\n';
}
