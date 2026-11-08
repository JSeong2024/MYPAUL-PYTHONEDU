#include "common.hpp"
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
struct Device{std::int64_t seq=0,count=0,last=0;};
int main(){std::ifstream file("readings.csv");if(!file){std::cerr<<"입력 파일 열기 실패\n";return 1;}
    std::map<std::string,Device> devices;std::ostringstream rejected;std::string line;int row=0;
    while(std::getline(file,line)){++row;summary::strip_cr(line);auto f=summary::split(line);
        if(f.size()!=3||f[0].empty()){rejected<<row<<",BAD_FORMAT\n";continue;}
        auto seq=summary::number(f[1]),value=summary::number(f[2]);
        if(!seq||*seq<=0){rejected<<row<<",BAD_SEQUENCE\n";continue;}
        if(!value||*value<0||*value>100){rejected<<row<<",BAD_READING\n";continue;}
        auto found=devices.find(f[0]);if(found!=devices.end()&&*seq<=found->second.seq){rejected<<row<<",BAD_SEQUENCE\n";continue;}
        Device& d=devices[f[0]];d.seq=*seq;d.last=*value;++d.count;}
    if(!file.eof()&&file.fail()){std::cerr<<"읽기 실패\n";return 1;}
    std::ostringstream report;
    for(const auto& [id,d]:devices)report<<id<<','<<d.count<<','<<d.last<<','<<(d.last>=80?"WARN":"OK")<<'\n';
    std::string error;if(!summary::safe_write("devices.csv",report.str(),error)||!summary::safe_write("rejected.csv",rejected.str(),error)){
        std::cerr<<error<<'\n';return 1;}}
