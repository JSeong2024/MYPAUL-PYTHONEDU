#include <charconv>
#include <cstdint>
#include <iostream>
#include <print>
#include <string>
#include <system_error>

int main() {
    constexpr int sample_count{5};
    std::int64_t sum{};

    for (int i{0}; i < sample_count; ++i) {
        std::cout << "ADC sample " << (i + 1)
                  << " (0-4095): " << std::flush;
        std::string line;
        if (!std::getline(std::cin, line)) {
            std::cerr << "Error: input stream closed.\n";
            return 1;
        }
        int value{};
        const auto result = std::from_chars(
            line.data(), line.data() + line.size(), value);
        if (result.ec != std::errc{} ||
            result.ptr != line.data() + line.size() ||
            value < 0 || value > 4'095) {
            std::cerr << "Error: invalid ADC value.\n";
            return 1;
        }

        sum += value;
    }

    const double average = static_cast<double>(sum) / sample_count;
    std::println("Average: {:.1f}", average);
}
