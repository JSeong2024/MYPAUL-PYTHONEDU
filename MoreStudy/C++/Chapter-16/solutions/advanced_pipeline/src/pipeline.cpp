#include "pipeline/pipeline.hpp"
#include <charconv>
#include <istream>
#include <iostream>
#include <stdexcept>
#include <string_view>
#include <utility>

namespace pipeline {
namespace {
[[nodiscard]] bool parse_integer(std::string_view text, int& value) {
    if (text.empty()) return false;
    const auto [position, error] = std::from_chars(text.data(), text.data() + text.size(), value);
    return error == std::errc{} && position == text.data() + text.size();
}
}

Parsed parse_csv(std::istream& input) {
    Parsed result{};
    std::string line;
    while (std::getline(input, line)) {
        // 학습용 간단 CSV: 쉼표/따옴표를 포함하는 필드는 지원하지 않음.
        if (!line.empty() && line.back() == '\r') line.pop_back();
        const auto first = line.find(',');
        const auto second = first == std::string::npos ? first : line.find(',', first + 1);
        if (first == std::string::npos || second == std::string::npos ||
            line.find(',', second + 1) != std::string::npos) {
            ++result.rejected; continue;
        }
        const std::string id = line.substr(0, first);
        const std::string_view amount{line.data() + first + 1, second - first - 1};
        const std::string_view status{line.data() + second + 1, line.size() - second - 1};
        int value{};
        if (id.empty() || !parse_integer(amount, value) || value < 0 || value > 100 ||
            (status != "ok" && status != "bad")) {
            ++result.rejected; continue;
        }
        result.rows.push_back(Reading{id, value, status == "ok"});
    }
#ifdef PIPELINE_VERBOSE
    std::clog << "parsed=" << result.rows.size() << " rejected=" << result.rejected << '\n';
#endif
    return result;
}

std::map<std::string, Summary> summarize(const std::vector<Reading>& rows, int threshold) {
    if (threshold < 0 || threshold > 100) throw std::invalid_argument("invalid threshold");
    std::map<std::string, Summary> report;
    for (const auto& reading : rows) {
        if (!reading.valid) continue;
        if (reading.id.empty() || reading.value < 0 || reading.value > 100)
            throw std::invalid_argument("invalid reading");
        auto& slot = report[reading.id];
        ++slot.count;
        slot.total += reading.value;
        if (reading.value >= threshold) ++slot.alerts;
    }
    return report;
}
}
