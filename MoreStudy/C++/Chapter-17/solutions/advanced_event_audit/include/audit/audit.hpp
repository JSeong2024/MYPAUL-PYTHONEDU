#pragma once
#include <cstddef>
#include <istream>
#include <map>
#include <ostream>
#include <string>
namespace audit {
struct Report {
 std::map<std::string,long long> balances;
 std::size_t accepted{};
 std::size_t rejected{};
};
// 단순 CSV: 정확히 네 필드, 따옴표 및 필드 내부 쉼표 미지원.
// 실패한 행은 rejected 스트림에 '행번호,오류코드'로 기록한다.
[[nodiscard]] Report process(std::istream& input, std::ostream& rejected);
void write_balances(const Report& report,std::ostream& output);
}
