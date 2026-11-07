#pragma once
#include <cstdint>
#include <expected>
#include <span>
#include <string>
#include <vector>

struct Event {
    std::string device;
    int duration_ms{};
};

struct DeviceSummary {
    std::string device;
    std::size_t count{};
    std::size_t slow_count{};
    std::int64_t total_ms{};

    [[nodiscard]] double mean_ms() const noexcept {
        return count == 0 ? 0.0 : static_cast<double>(total_ms) / count;
    }
};

[[nodiscard]] std::expected<std::vector<DeviceSummary>, std::string>
summarize_events(std::span<const Event> events, int slow_threshold_ms);
