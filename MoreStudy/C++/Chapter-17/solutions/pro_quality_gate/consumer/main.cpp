#include <quality_gate/batch.hpp>
#include <array>
#include <iostream>
int main(){
 const std::array data{quality_gate::Reading{"D1",8,true}};
 const auto out=quality_gate::summarize(data);
 if(out.size()!=1 || out.front().total!=8)return 1;
 std::cout<<"Consumer: PASS\n";
}
