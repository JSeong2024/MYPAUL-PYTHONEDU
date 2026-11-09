#include "audit/audit.hpp"
#include <array>
#include <charconv>
#include <set>
#include <string>
#include <string_view>
namespace audit {
namespace {
bool split_four(const std::string& line,std::array<std::string_view,4>& fields) {
 const std::string_view s{line};
 std::size_t pos=0;
 for(std::size_t i=0;i<4;++i) {
  auto end=s.find(',',pos);
  if(i<3 && end==std::string_view::npos) return false;
  if(i==3 && end!=std::string_view::npos) return false;
  fields[i]=s.substr(pos,(end==std::string_view::npos?s.size():end)-pos);
  pos=end+1;
 }
 return true;
}
}
Report process(std::istream& input,std::ostream& rejected) {
 Report report;
 std::set<std::string> accepted_ids;
 std::string line;
 std::size_t number=0;
 while(std::getline(input,line)) {
  ++number;
  if(!line.empty() && line.back()=='\r') line.pop_back();
  auto reject=[&](std::string_view error){++report.rejected;rejected<<number<<','<<error<<'\n';};
  std::array<std::string_view,4> fields{};
  if(!split_four(line,fields) || fields[0].empty() || fields[1].empty() ||
     fields[0].find('"')!=std::string_view::npos || fields[1].find('"')!=std::string_view::npos) {
   reject("BAD_FORMAT");continue;
  }
  long long amount=0;
  auto [last,err]=std::from_chars(fields[3].data(),fields[3].data()+fields[3].size(),amount);
  if(fields[3].empty() || err!=std::errc{} || last!=fields[3].data()+fields[3].size() || amount<=0 || amount>1000000) {
   reject("BAD_AMOUNT");continue;
  }
  if(fields[2]!="ADD" && fields[2]!="REMOVE") {reject("UNKNOWN_KIND");continue;}
  if(accepted_ids.contains(std::string(fields[0]))) {reject("DUPLICATE_EVENT");continue;}
  const std::string device{fields[1]};
  auto it=report.balances.find(device);
  const long long balance=it==report.balances.end()?0:it->second;
  if(fields[2]=="REMOVE" && amount>balance) {reject("INSUFFICIENT_BALANCE");continue;}
  // 총액은 행 수 * 1,000,000 안에서 유효하도록 별도 데이터 규모 제한.
  report.balances[device]=balance+(fields[2]=="ADD"?amount:-amount);
  accepted_ids.insert(std::string(fields[0]));
  ++report.accepted;
 }
 return report;
}
void write_balances(const Report& report,std::ostream& output) {
 for(const auto& [device,amount]: report.balances) output<<device<<','<<amount<<'\n';
}
}
