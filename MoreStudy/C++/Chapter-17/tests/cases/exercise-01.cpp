#define CH17_LIBRARY_ONLY
#include CH17_SOURCE_PATH
#include <cassert>
#include <climits>
#include <stdexcept>
int main(){
 auto good=parse_count("0");if(!good || *good!=0)throw std::runtime_error("zero");
 auto max=parse_count("2147483647");if(!max || *max!=INT_MAX)throw std::runtime_error("max");
 auto zeros=parse_count("00017");if(!zeros || *zeros!=17)throw std::runtime_error("leading zero");
 for(auto bad:{"","-1","+1","2 "," 2","2.0","12x","2147483648"})
  if(parse_count(bad))throw std::runtime_error("invalid accepted");
}
