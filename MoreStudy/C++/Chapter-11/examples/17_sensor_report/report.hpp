#pragma once
#include <cstddef>
#include <expected>
#include <filesystem>
#include <map>
#include <string>

struct SensorReport {
    std::size_t samples{};
    double minimum{};
    double maximum{};
    double average{};
    std::map<std::string, std::size_t> counts;
};

[[nodiscard]] std::expected<SensorReport, std::string>
build_report(const std::filesystem::path& input_path);

[[nodiscard]] std::expected<void, std::string>
write_report(const std::filesystem::path& output_path, const SensorReport& report);
