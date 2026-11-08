#pragma once
#include <cstddef>
#include <filesystem>
#include <map>
#include <optional>
#include <string>
struct SensorReport {
 std::size_t samples{};
 double minimum{};
 double maximum{};
 double average{};
 std::map<std::string,std::size_t> counts;
};
std::optional<SensorReport> build_report(const std::filesystem::path& input_path);
bool write_report(const std::filesystem::path& output_path,const SensorReport& report);
