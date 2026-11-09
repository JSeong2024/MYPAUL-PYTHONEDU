#pragma once
#include <cstddef>
#include <cstdint>
#include <span>
#include <string>
#include <vector>
namespace quality_gate {
struct Reading {std::string device; int value{}; bool valid{true};};
struct Summary {
 std::string device;
 std::size_t count{};
 std::int64_t total{};
 int minimum{};
 int maximum{};
 bool operator==(const Summary&) const = default;
};
// valid==false 측정은 건너뜀. 유효 측정의 기기명은 비어 있으면 안 되며 값은 0..100.
// 유효하지 않은 측정값이 있으면 invalid_argument. 출력은 기기 ID 오름차순.
[[nodiscard]] std::vector<Summary> summarize(std::span<const Reading> readings);
}
