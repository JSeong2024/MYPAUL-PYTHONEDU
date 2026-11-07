#include <charconv>
#include <expected>
#include <print>
#include <string>
#include <string_view>

struct SensorRecord {
    std::string device_id;
    int temperature;
    std::string status;
};

[[nodiscard]] std::expected<SensorRecord, std::string_view>
parse_record(std::string_view line) {
    const auto first = line.find('|');
    if (first == std::string_view::npos) {
        return std::unexpected("missing delimiter");
    }
    const auto second = line.find('|', first + 1);
    if (second == std::string_view::npos || line.find('|', second + 1) != std::string_view::npos) {
        return std::unexpected("expected three fields");
    }

    const auto id = line.substr(0, first);
    const auto number = line.substr(first + 1, second - first - 1);
    const auto status = line.substr(second + 1);
    if (id.empty() || id.size() > 40 || (status != "OK" && status != "WARN")) {
        return std::unexpected("invalid device or status");
    }

    int temperature{};
    const auto [end, error] = std::from_chars(
        number.data(), number.data() + number.size(), temperature);
    if (error != std::errc{} || end != number.data() + number.size() ||
        temperature < -40 || temperature > 125) {
        return std::unexpected("invalid temperature");
    }

    return SensorRecord{std::string{id}, temperature, std::string{status}};
}

int main() {
    for (const std::string_view input : {"ROOM-01|23|OK", "ROOM-02|23C|WARN"}) {
        const auto result = parse_record(input);
        if (result) {
            std::println("{}: {} C ({})", result->device_id,
                         result->temperature, result->status);
        } else {
            std::println("Rejected: {}", result.error());
        }
    }
}
