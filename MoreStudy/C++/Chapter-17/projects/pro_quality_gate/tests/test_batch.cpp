#include "quality_gate/batch.hpp"
#include <array>
#include <iostream>
#include <stdexcept>
#include <vector>
void expect(bool ok) {if(!ok)throw std::runtime_error("quality regression");}
int main() {
 using quality_gate::Reading;
 const std::array data{Reading{"B",100,true},Reading{"A",0,true},Reading{"B",50,true},Reading{"A",-5,false}};
 const auto out=quality_gate::summarize(data);
 expect(out.size()==2);
 expect(out.at(0).device=="A" && out.at(0).count==1 && out.at(0).total==0);
 expect(out.at(1).device=="B" && out.at(1).count==2 && out.at(1).total==150);
 expect(out.at(1).minimum==50 && out.at(1).maximum==100);
 const std::vector<Reading> empty;
 expect(quality_gate::summarize(empty).empty());
 bool rejected=false;
 try {(void)quality_gate::summarize(std::array{Reading{"B",101,true}});}
 catch(const std::invalid_argument&) {rejected=true;}
 expect(rejected);
 std::cout<<"Quality tests: PASS\n";
}
