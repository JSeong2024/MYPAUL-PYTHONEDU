#pragma once

#include <cstddef>
#include <span>
#include <vector>

namespace sensor {
struct Reading {
    int device_id{};
    int value{};
};
struct DeviceStat {
    int device_id{};
    std::size_t count{};
    long long total{};
    bool operator==(const DeviceStat&) const = default;
};
struct Report {
    std::vector<DeviceStat> devices;  // 장치 ID 오름차순
    std::size_t accepted{};
    std::size_t rejected{};
    long long total{};
    bool operator==(const Report&) const = default;
};

// 유효한 데이터: device_id > 0, 0 <= value <= 100.
// 모든 입력은 원본 순서대로 처리하며, 실패한 행은 합계에서 제외한다.
[[nodiscard]] Report analyze_reference(std::span<const Reading> readings);
[[nodiscard]] Report analyze_optimized(std::span<const Reading> readings);
} // namespace sensor
