#include "report.hpp"
#include <filesystem>
#include <iostream>
int main(int argc,char* argv[]){
 if(argc!=3){std::cerr<<"Usage: sensor_report <input.csv> <output.txt>\n";return 1;}
 const std::filesystem::path input{argv[1]},output{argv[2]};
 std::error_code ec;
 if(std::filesystem::equivalent(input,output,ec)&&!ec){std::cerr<<"Input and output must differ\n";return 1;}
 const auto report=build_report(input);
 if(!report){std::cerr<<"Invalid input file\n";return 1;}
 if(!write_report(output,*report)){std::cerr<<"Cannot write report\n";return 1;}
 std::cout<<"Saved report: "<<report->samples<<" readings from "<<report->counts.size()<<" devices\n";
}
