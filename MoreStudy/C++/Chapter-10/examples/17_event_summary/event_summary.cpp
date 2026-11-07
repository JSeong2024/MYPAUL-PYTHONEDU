#include "event_summary.hpp"
#include <algorithm>
#include <limits>
#include <unordered_map>
#include <utility>

std::expected<std::vector<DeviceSummary>, std::string>
summarize_events(std::span<const Event> events, int slow_threshold_ms) {
    if (slow_threshold_ms < 0) {
        return std::unexpected("threshold must be nonnegative");
    }
    std::unordered_map<std::string, DeviceSummary> grouped;
    grouped.reserve(events.size());
    for (const Event& event : events) {
        if (event.device.empty() || event.duration_ms < 0) {
            return std::unexpected("invalid event");
        }
        auto [it, inserted] = grouped.try_emplace(event.device);
        DeviceSummary& summary = it->second;
        if (inserted) {
            summary.device = event.device;
        }
        if (summary.total_ms > std::numeric_limits<std::int64_t>::max() - event.duration_ms) {
            return std::unexpected("duration sum overflow");
        }
        ++summary.count;
        summary.slow_count += (event.duration_ms >= slow_threshold_ms);
        summary.total_ms += event.duration_ms;
    }
    std::vector<DeviceSummary> result;
    result.reserve(grouped.size());
    for (auto& [device, summary] : grouped) {
        (void)device;
        result.push_back(std::move(summary));
    }
    std::ranges::sort(result, {}, &DeviceSummary::device);
    return result;
}
