#define CH17_LIBRARY_ONLY
#include CH17_SOURCE_PATH
#include <array>
#include <stdexcept>
int main(){
 const std::array vals{0,50,100};
 if(batch_total(vals)!=150)throw std::runtime_error("sum");
 const std::array<int,0> empty{};if(batch_total(empty)!=0)throw std::runtime_error("empty");
 const std::array<int,2> bad{-1,3};
 bool thrown=false;
 try{(void)batch_total(bad);}catch(const std::invalid_argument&){thrown=true;}
 if(!thrown)throw std::runtime_error("bad value");
 thrown=false;const std::array<int,1> high{101};
 try{(void)batch_total(high);}catch(const std::invalid_argument&){thrown=true;}
 if(!thrown)throw std::runtime_error("high value");
}
