#include "summary.hpp"

namespace events {

bool add_event(Summary& report, std::string_view name) {
    if (name.empty() || report.total == 1'000'000) {
        return false;
    }
    ++report.frequency[std::string{name}];
    ++report.total;
    return true;
}

std::size_t distinct_count(const Summary& report) noexcept {
    return report.frequency.size();
}

}  // namespace events
