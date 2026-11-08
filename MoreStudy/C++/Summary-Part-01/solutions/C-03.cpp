#include "common.hpp"
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <sstream>
#include <string>
#include <unordered_set>
int main(){std::ifstream initial("stock.csv"),events("events.csv");if(!initial||!events){std::cerr<<"파일 열기 실패\n";return 1;}
    std::map<std::string,std::int64_t> stock;std::string line;
    while(std::getline(initial,line)){summary::strip_cr(line);auto f=summary::split(line);
        if(f.size()!=2||f[0].empty()){std::cerr<<"초기 재고 형식 오류\n";return 1;}
        auto amount=summary::number(f[1]);if(!amount||*amount<0||!stock.emplace(f[0],*amount).second){std::cerr<<"초기 재고 오류\n";return 1;}}
    std::unordered_set<std::string> applied;std::ostringstream rejected;int row=0;
    while(std::getline(events,line)){++row;summary::strip_cr(line);auto f=summary::split(line);std::string err;
        if(f.size()!=4||f[0].empty()||f[1].empty())err="BAD_FORMAT";
        else if(applied.contains(f[0]))err="DUPLICATE_EVENT";
        else if(!stock.contains(f[1]))err="UNKNOWN_PRODUCT";
        else if(f[2]!="IN"&&f[2]!="OUT")err="BAD_TYPE";
        else{auto amount=summary::number(f[3]);if(!amount||*amount<=0)err="BAD_QUANTITY";
            else if(f[2]=="OUT"&&stock[f[1]]<*amount)err="INSUFFICIENT_STOCK";
            else if(f[2]=="IN"&&stock[f[1]]>std::numeric_limits<std::int64_t>::max()-*amount)err="BAD_QUANTITY";
            else{stock[f[1]]+=f[2]=="IN"?*amount:-*amount;applied.insert(f[0]);}}
        if(!err.empty())rejected<<row<<','<<err<<'\n';}
    if(!events.eof()&&events.fail()){std::cerr<<"읽기 실패\n";return 1;}
    std::ostringstream report;for(const auto& [id,n]:stock)report<<id<<','<<n<<'\n';
    std::string error;if(!summary::safe_write("inventory.csv",report.str(),error)||!summary::safe_write("rejected.csv",rejected.str(),error)){
        std::cerr<<error<<'\n';return 1;}}
