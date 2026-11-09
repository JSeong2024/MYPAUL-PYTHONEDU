#include "quality_gate/batch.hpp"
#include <chrono>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
int main(int argc,char** argv) {
 std::size_t n=100000;
 if(argc>1) {
  char* end=nullptr;
  const unsigned long long parsed=std::strtoull(argv[1],&end,10);
  if(end==argv[1] || *end!='\0' || parsed>10000000 || parsed==0) {std::cerr<<"Invalid size\n";return 2;}
  n=static_cast<std::size_t>(parsed);
 }
 std::vector<quality_gate::Reading> data;data.reserve(n);
 for(std::size_t i=0;i<n;++i)data.push_back({"D"+std::to_string(i%100),static_cast<int>(i%101),true});
 const auto started=std::chrono::steady_clock::now();
 const auto summary=quality_gate::summarize(data);
 const auto elapsed=std::chrono::duration<double,std::milli>(std::chrono::steady_clock::now()-started).count();
 std::int64_t checksum=0;for(const auto& row:summary)checksum+=row.total;
 std::cout<<"rows="<<n<<" groups="<<summary.size()<<" checksum="<<checksum<<" ms="<<elapsed<<'\n';
}
