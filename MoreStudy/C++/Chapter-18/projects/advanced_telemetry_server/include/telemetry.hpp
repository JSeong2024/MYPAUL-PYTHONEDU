#pragma once
#include <cstddef>
#include <map>
#include <string>
#include <string_view>
#include <vector>
namespace telemetry {
struct Aggregate { std::size_t count{}; long long sum{}; };
struct Result {
    std::map<std::string, Aggregate> devices;
    std::size_t accepted{};
    std::size_t rejected{};
};
[[nodiscard]] bool parse(std::string_view wire, std::string& device, int& value);
[[nodiscard]] Result collect(const std::vector<std::string>& requests);
}
