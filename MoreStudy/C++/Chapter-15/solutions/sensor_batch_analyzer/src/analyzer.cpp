#include "sensor/analyzer.hpp"

#include <algorithm>
#include <unordered_map>
#include <utility>

namespace sensor {
namespace {
[[nodiscard]] bool valid(const Reading& reading) noexcept {
    return reading.device_id > 0 && reading.value >= 0 && reading.value <= 100;
}
} // namespace

Report analyze_reference(std::span<const Reading> readings) {
    Report report;
    for (const Reading& reading : readings) {
        if (!valid(reading)) {
            ++report.rejected;
            continue;
        }
        ++report.accepted;
        report.total += reading.value;
        auto found = std::find_if(report.devices.begin(), report.devices.end(),
                                  [&](const DeviceStat& item) {
                                      return item.device_id == reading.device_id;
                                  });
        if (found == report.devices.end()) {
            report.devices.push_back(DeviceStat{reading.device_id, 1, reading.value});
        } else {
            ++found->count;
            found->total += reading.value;
        }
    }
    std::ranges::sort(report.devices, {}, &DeviceStat::device_id);
    return report;
}

Report analyze_optimized(std::span<const Reading> readings) {
    Report report;
    std::unordered_map<int, DeviceStat> index;
    // reserve()는 리해시 비용을 줄일 수 있으나 메모리 사용량도 늘릴 수 있음.
    index.reserve(std::min<std::size_t>(readings.size(), 4096));
    for (const Reading& reading : readings) {
        if (!valid(reading)) {
            ++report.rejected;
            continue;
        }
        ++report.accepted;
        report.total += reading.value;
        auto [it, inserted] = index.try_emplace(
            reading.device_id, DeviceStat{reading.device_id, 0, 0});
        (void)inserted;
        ++it->second.count;
        it->second.total += reading.value;
    }
    report.devices.reserve(index.size());
    for (const auto& [id, stat] : index) {
        (void)id;
        report.devices.push_back(stat);
    }
    // unordered_map의 순회 순서는 지정되지 않으므로 출력 전에 정렬한다.
    std::ranges::sort(report.devices, {}, &DeviceStat::device_id);
    return report;
}
} // namespace sensor
