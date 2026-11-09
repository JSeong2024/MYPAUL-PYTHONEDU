#include "audit/audit.hpp"
#include <sstream>
#include <stdexcept>
#include <iostream>
void expect(bool ok) {if(!ok) throw std::runtime_error("audit regression");}
int main() {
 std::istringstream input{
  "e1,D1,ADD,10\n"
  "e2,D1,REMOVE,3\n"
  "e2,D1,ADD,5\n"
  "e3,D2,ADD,6\n"
  "e4,D1,REMOVE,11\n"
  "e5,D2,ADD,bad\n"
  "e6,D2,UNKNOWN,4\n"};
 std::ostringstream rejected;
 const auto r=audit::process(input,rejected);
 expect(r.accepted==3 && r.rejected==4);
 expect(r.balances.at("D1")==7 && r.balances.at("D2")==6);
 expect(rejected.str()=="3,DUPLICATE_EVENT\n5,INSUFFICIENT_BALANCE\n6,BAD_AMOUNT\n7,UNKNOWN_KIND\n");
 std::ostringstream balances; audit::write_balances(r,balances);
 expect(balances.str()=="D1,7\nD2,6\n");
 std::istringstream empty{};std::ostringstream ignored;
 expect(audit::process(empty,ignored).balances.empty());
 std::cout<<"Audit tests: PASS\n";
}
