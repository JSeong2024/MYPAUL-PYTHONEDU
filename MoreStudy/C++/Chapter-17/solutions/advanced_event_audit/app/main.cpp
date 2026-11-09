#include "audit/audit.hpp"
#include <fstream>
#include <iostream>
int main(int argc,char** argv) {
 if(argc!=4) {std::cerr<<"Usage: audit_cli events.csv balances.csv rejected.csv\n";return 2;}
 std::ifstream input{argv[1],std::ios::binary};
 if(!input) {std::cerr<<"Cannot open input\n";return 1;}
 std::ofstream output{argv[2],std::ios::binary|std::ios::trunc};
 std::ofstream rejected{argv[3],std::ios::binary|std::ios::trunc};
 if(!output || !rejected) {std::cerr<<"Cannot open output\n";return 1;}
 const auto report=audit::process(input,rejected);
 audit::write_balances(report,output);
 output.flush();rejected.flush();
 if(input.bad() || !output || !rejected) {std::cerr<<"I/O error\n";return 1;}
 std::cout<<"Accepted: "<<report.accepted<<", Rejected: "<<report.rejected<<'\n';
}
