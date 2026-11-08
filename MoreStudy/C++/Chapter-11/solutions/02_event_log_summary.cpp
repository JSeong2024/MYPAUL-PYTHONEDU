#include <fstream>
#include <iostream>
#include <map>
#include <string>
int main(int argc,char* argv[]){
 if(argc!=2){std::cerr<<"Usage: event_log_summary <path>\n";return 1;}
 std::ifstream file{argv[1]};if(!file){std::cerr<<"Cannot open file\n";return 1;}
 std::map<std::string,int> counts;
 std::string line;
 while(std::getline(file,line)){
  if(line!="INFO" && line!="WARN" && line!="ERROR"){std::cerr<<"Invalid event\n";return 1;}
  ++counts[line];
 }
 if(file.bad()){return 1;}
 for(const auto& [name,count]:counts){std::cout<<name<<": "<<count<<'\n';}
}
