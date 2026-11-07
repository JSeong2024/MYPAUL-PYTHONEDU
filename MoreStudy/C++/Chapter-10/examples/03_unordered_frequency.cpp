#include <print>
#include <string>
#include <string_view>
#include <unordered_map>

int main() {
    const std::string_view events[]{"WARN", "INFO", "WARN", "ERROR", "INFO"};
    std::unordered_map<std::string, int> counts;
    counts.reserve(3);
    for (const auto event : events) {
        ++counts[std::string{event}];
    }
    std::println("INFO: {}", counts.at("INFO"));
    std::println("WARN: {}", counts.at("WARN"));
    std::println("ERROR: {}", counts.at("ERROR"));
    std::println("Contains DEBUG: {}", counts.contains("DEBUG"));
}
