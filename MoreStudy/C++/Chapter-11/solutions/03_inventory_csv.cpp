#include <charconv>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <system_error>
int main(int argc,char* argv[]){
 if(argc!=2){std::cerr<<"Usage: inventory_csv <path>\n";return 1;}
 std::ifstream file{argv[1]};if(!file){std::cerr<<"Cannot open file\n";return 1;}
 std::map<std::string,int> inventory;std::string line;
 while(std::getline(file,line)){
  const auto pos=line.find(',');
  if(pos==std::string::npos||pos==0||pos+1==line.size()||line.find(',',pos+1)!=std::string::npos){std::cerr<<"Invalid record\n";return 1;}
  const std::string name=line.substr(0,pos);const std::string number=line.substr(pos+1);
  int quantity{};const auto parsed=std::from_chars(number.data(),number.data()+number.size(),quantity);
  if(parsed.ec!=std::errc{}||parsed.ptr!=number.data()+number.size()||quantity<0||quantity>1000||inventory.contains(name)){std::cerr<<"Invalid record\n";return 1;}
  inventory[name]=quantity;
 }
 if(file.bad()){return 1;}
 for(const auto& [name,value]:inventory){std::cout<<name<<": "<<value<<'\n';}
}
