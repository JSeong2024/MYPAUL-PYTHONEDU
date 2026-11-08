#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
int main(int argc,char* argv[]){
 if(argc!=2){std::cerr<<"Usage: binary_u32_reader <path>\n";return 1;}
 std::ifstream file{argv[1],std::ios::binary};if(!file){std::cerr<<"Cannot open file\n";return 1;}
 std::array<unsigned char,4> bytes{};
 if(!file.read(reinterpret_cast<char*>(bytes.data()),static_cast<std::streamsize>(bytes.size()))){std::cerr<<"Expected 4 bytes\n";return 1;}
 char extra{};if(file.get(extra)){std::cerr<<"Expected exactly 4 bytes\n";return 1;}
 if(file.bad()){return 1;}
 std::uint32_t value{};for(auto byte:bytes){value=(value<<8)|byte;}
 std::cout<<"Value: "<<value<<'\n';
}
