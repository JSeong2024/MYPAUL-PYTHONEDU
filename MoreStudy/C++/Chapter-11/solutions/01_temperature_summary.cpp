#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
int main(int argc,char* argv[]) {
 if(argc!=2){std::cerr<<"Usage: temperature_summary <path>\n";return 1;}
 std::ifstream file{argv[1]};if(!file){std::cerr<<"Cannot open file\n";return 1;}
 double value{};double sum{};double lo{};double hi{};std::size_t count{};
 while(file>>value){
  if(value < -100 || value > 100){std::cerr<<"Invalid reading\n";return 1;}
  if(count==0){lo=value;hi=value;}
  if (value < lo) { lo = value; }
  if (value > hi) { hi = value; }
  sum+=value;++count;
 }
 if(!file.eof()){std::cerr<<"Invalid reading\n";return 1;}
 if(count==0){std::cerr<<"Empty file\n";return 1;}
 std::cout<<std::fixed<<std::setprecision(2)<<"Count: "<<count<<"\nMin: "<<lo<<"\nMax: "<<hi<<"\nAverage: "<<sum/count<<'\n';
}
