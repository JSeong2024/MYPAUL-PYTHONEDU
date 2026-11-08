#include "common.hpp"
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
bool parse_record(const std::string& line,std::vector<std::string>& f,std::string& err){
    f.clear();std::size_t i=0;
    while(true){std::string field;
        if(i<line.size()&&line[i]=='"'){
            ++i;bool closed=false;
            while(i<line.size()){if(line[i]=='"'){
                if(i+1<line.size()&&line[i+1]=='"'){field+='"';i+=2;}else{++i;closed=true;break;}
            }else field+=line[i++];}
            if(!closed){err="UNCLOSED_QUOTE";return false;}
            if(i<line.size()&&line[i]!=','){err="BAD_FORMAT";return false;}
        }else{while(i<line.size()&&line[i]!=','){
            if(line[i]=='"'){err="BAD_FORMAT";return false;}field+=line[i++];}}
        f.push_back(field);if(i>=line.size())break;++i;
        if(i==line.size()){f.emplace_back();break;}}
    if(f.size()!=2||f[0].empty()){err="BAD_FORMAT";return false;}return true;
}
int main(){std::string path;if(!std::getline(std::cin,path)){std::cout<<"OPEN_ERROR\n";return 0;}
    std::ifstream in(path);if(!in){std::cout<<"OPEN_ERROR\n";return 0;}
    std::string s;int row=0;
    while(std::getline(in,s)){++row;summary::strip_cr(s);std::vector<std::string> f;std::string err;
        if(!parse_record(s,f,err)){std::cout<<"ERROR "<<row<<' '<<err<<'\n';continue;}
        auto amount=summary::number(f[1]);if(!amount||*amount<0||*amount>1000000){std::cout<<"ERROR "<<row<<" BAD_PRICE\n";continue;}
        std::cout<<f[0]<<'|'<<*amount<<'\n';}}
