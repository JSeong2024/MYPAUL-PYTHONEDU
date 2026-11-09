#include "quality_gate/batch.hpp"
namespace quality_gate {
std::vector<Summary> summarize(std::span<const Reading> readings) {
 // TODO: 데이터 검증 및 std::map 기반 결정론적 집계
 (void)readings;
 return {};
}
}
