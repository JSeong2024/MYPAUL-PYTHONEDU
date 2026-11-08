#include <algorithm>
#include <charconv>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <string>
#include <string_view>
#include <system_error>
#include <vector>

[[nodiscard]] bool parse_reading(std::string_view field, int& result) {
    const auto first_nonspace = field.find_first_not_of(' ');
    if (first_nonspace == std::string_view::npos) return false;
    const auto last_nonspace = field.find_last_not_of(' ');
    field = field.substr(first_nonspace, last_nonspace - first_nonspace + 1);
    const char* first = field.data();
    const char* last = first + field.size();
    const auto [next, error] = std::from_chars(first, last, result);
    return error == std::errc{} && next == last && result >= -100 && result <= 100;
}

[[nodiscard]] bool parse_readings(std::string_view csv, std::vector<int>& readings) {
    std::size_t start{};
    while (true) {
        const auto comma = csv.find(',', start);
        const auto length = comma == std::string_view::npos ? csv.size() - start : comma - start;
        int value{};
        if (readings.size() >= 20 || !parse_reading(csv.substr(start, length), value)) return false;
        readings.push_back(value);
        if (comma == std::string_view::npos) return true;
        start = comma + 1;
    }
}

int main() {
    std::string device;
    std::string csv;
    std::cout << "Device: " << std::flush;
    if (!std::getline(std::cin, device) || device.empty()) {
        std::cerr << "Error: invalid device.\n";
        return 1;
    }
    std::cout << "Readings (-100 to 100, comma-separated): " << std::flush;
    if (!std::getline(std::cin, csv)) {
        std::cerr << "Error: invalid readings.\n";
        return 1;
    }
    std::vector<int> readings;
    if (!parse_readings(csv, readings)) {
        std::cerr << "Error: invalid readings.\n";
        return 1;
    }
    const int total = std::accumulate(readings.begin(), readings.end(), 0);
    std::ranges::sort(readings);
    std::cout << "\n--- Sensor Batch Report ---\n";
    std::cout << "Device: " << device << '\n';
    std::cout << "Count: " << readings.size() << '\n';
    std::cout << "Minimum: " << readings.front() << '\n';
    std::cout << "Maximum: " << readings.back() << '\n';
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Average: " << static_cast<double>(total) / readings.size() << '\n';
    std::cout << "Sorted: ";
    for (std::size_t i = 0; i < readings.size(); ++i) {
        if (i > 0) std::cout << ", ";
        std::cout << readings[i];
    }
    std::cout << '\n';
}
