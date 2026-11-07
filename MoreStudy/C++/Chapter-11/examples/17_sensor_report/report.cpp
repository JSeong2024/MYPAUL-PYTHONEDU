#include "report.hpp"
#include <charconv>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <limits>
#include <string_view>
#include <system_error>

namespace {
[[nodiscard]] bool valid_id(std::string_view id) {
    if (id.empty() || id.size() > 32) return false;
    for (const unsigned char c : id) {
        if (!((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') ||
              (c >= '0' && c <= '9') || c == '_' || c == '-')) return false;
    }
    return true;
}

[[nodiscard]] bool parse_temperature(std::string_view text, double& value) {
    if (text.empty()) return false;
    const auto [end, ec] = std::from_chars(text.data(), text.data() + text.size(), value);
    return ec == std::errc{} && end == text.data() + text.size() &&
           std::isfinite(value) && value >= -50.0 && value <= 120.0;
}
}

std::expected<SensorReport, std::string>
build_report(const std::filesystem::path& input_path) {
    std::ifstream input{input_path};
    if (!input) return std::unexpected("Cannot open CSV file");

    std::string line;
    if (!std::getline(input, line)) {
        return std::unexpected("Missing CSV header");
    }
    if (!line.empty() && line.back() == '\r') line.pop_back();
    if (line != "device,temperature_c") {
        return std::unexpected("Expected header: device,temperature_c");
    }
    SensorReport result;
    long double sum{};
    std::size_t line_number{1};
    while (std::getline(input, line)) {
        ++line_number;
        if (!line.empty() && line.back() == '\r') line.pop_back();
        const auto separator = line.find(',');
        if (separator == std::string::npos || line.find(',', separator + 1) != std::string::npos) {
            return std::unexpected("Invalid CSV fields at line " + std::to_string(line_number));
        }
        const std::string_view device{line.data(), separator};
        const std::string_view numeric{line.data() + separator + 1, line.size() - separator - 1};
        double temperature{};
        if (!valid_id(device) || !parse_temperature(numeric, temperature)) {
            return std::unexpected("Invalid device/temperature at line " + std::to_string(line_number));
        }
        if (result.samples == 0) {
            result.minimum = result.maximum = temperature;
        } else {
            if (temperature < result.minimum) result.minimum = temperature;
            if (temperature > result.maximum) result.maximum = temperature;
        }
        sum += temperature;
        ++result.samples;
        ++result.counts[std::string{device}];
    }
    if (input.bad()) return std::unexpected("CSV read failed");
    if (result.samples == 0) return std::unexpected("CSV has no data rows");
    result.average = static_cast<double>(sum / result.samples);
    return result;
}

std::expected<void, std::string>
write_report(const std::filesystem::path& output_path, const SensorReport& report) {
    std::ofstream output{output_path, std::ios::trunc};
    if (!output) return std::unexpected("Cannot create report file");
    output << std::fixed << std::setprecision(2);
    output << "Readings: " << report.samples << '\n';
    output << "Devices: " << report.counts.size() << '\n';
    output << "Average: " << report.average << " C\n";
    output << "Minimum: " << report.minimum << " C\n";
    output << "Maximum: " << report.maximum << " C\n";
    for (const auto& [id, count] : report.counts) {
        output << id << ": " << count << "\n";
    }
    output.close();
    if (!output) return std::unexpected("Report write/close failed");
    return {};
}
