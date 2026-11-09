#include "quality_gate/batch.hpp"
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <map>
#include <stdexcept>
#include <vector>
void expect(bool value){if(!value)throw std::runtime_error("property regression");}
int main(){
 using quality_gate::Reading;
 std::uint32_t state=1729;
 auto random=[&]() {state=state*1664525u+1013904223u;return state;};
 std::vector<Reading> rows;rows.reserve(1200);
 std::map<std::string,std::int64_t> expected;
 for(int i=0;i<1200;++i) {
  const auto id=std::string{"D"}+std::to_string(random()%13);
  const int value=static_cast<int>(random()%101);
  const bool valid=random()%5!=0;
  rows.push_back({id,value,valid});
  if(valid)expected[id]+=value;
 }
 const auto original=quality_gate::summarize(rows);
 expect(original.size()==expected.size());
 for(const auto& item:original)expect(item.total==expected.at(item.device));
 std::reverse(rows.begin(),rows.end());
 expect(quality_gate::summarize(rows)==original); // 순서와 무관한 집계
 std::cout<<"Property checks: PASS\n";
}
