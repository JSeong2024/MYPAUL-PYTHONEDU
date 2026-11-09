#define CH17_LIBRARY_ONLY
#include CH17_SOURCE_PATH
#include <array>
#include <stdexcept>
int main(){
 const std::array sample{3,1,7,2};
 if(rolling_max(sample,2)!=std::vector<int>{3,7,7})throw std::runtime_error("window2");
 if(rolling_max(sample,1)!=std::vector<int>{3,1,7,2})throw std::runtime_error("window1");
 if(rolling_max(sample,4)!=std::vector<int>{7})throw std::runtime_error("window4");
 bool thrown=false;
 try{(void)rolling_max(sample,0);}catch(const std::invalid_argument&){thrown=true;}
 if(!thrown)throw std::runtime_error("window0");
 thrown=false;
 try{(void)rolling_max(sample,5);}catch(const std::invalid_argument&){thrown=true;}
 if(!thrown)throw std::runtime_error("window too big");
 const std::array<int,0> empty{};
 thrown=false;
 try{(void)rolling_max(empty,1);}catch(const std::invalid_argument&){thrown=true;}
 if(!thrown)throw std::runtime_error("empty");
}
