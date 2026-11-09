#include "device/report.hpp"
#include <stdexcept>
namespace device {
Summary summarize(std::span<const Record> records, int threshold) {
    if (threshold < 0 || threshold > 100) throw std::invalid_argument("invalid threshold");
    Summary result{};
    for (const auto& record : records) {
        if (record.id.empty() || record.reading < 0 || record.reading > 100)
            throw std::invalid_argument("invalid record");
        ++result.count;
        result.total += record.reading;
        if (record.reading >= threshold) ++result.alerts;
    }
    return result;
}
}
