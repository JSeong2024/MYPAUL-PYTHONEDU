#include "audit/audit.hpp"
namespace audit {
Report process(std::istream& input,std::ostream& rejected) {
 // TODO: CSV 검증 -> 중복 검사 -> 잔액 검사 -> 적용 순서 유지
 (void)input;(void)rejected;
 return {};
}
void write_balances(const Report& report,std::ostream& output) {
 // TODO: std::map의 장치 ID 정렬 순서로 CSV 생성
 (void)report;(void)output;
}
}
