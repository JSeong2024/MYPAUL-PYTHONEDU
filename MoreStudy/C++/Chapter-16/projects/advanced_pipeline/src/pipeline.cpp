#include "pipeline/pipeline.hpp"
#include <stdexcept>

namespace pipeline {
Parsed parse_csv(std::istream& input) {
    // TODO 1: 쉼표 2개, 정수 변환, 0~100 범위, status(ok/bad) 검증.
    // TODO 2: 유효한 행은 rows에 추가, 오류 행은 rejected 증가.
    (void)input;
    return {};
}
std::map<std::string, Summary> summarize(const std::vector<Reading>& rows, int threshold) {
    // TODO 3: 유효 측정값만 장치 ID 오름차순으로 집계.
    // TODO 4: threshold 검증, 총합/건수/경보 집계.
    (void)rows;
    if (threshold < 0 || threshold > 100) throw std::invalid_argument("invalid threshold");
    return {};
}
}
