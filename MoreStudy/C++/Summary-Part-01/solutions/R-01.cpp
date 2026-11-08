#include "common.hpp"
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <sstream>
#include <string>
#include <unordered_set>
#include <vector>
struct Order{std::int64_t amount=0,paid=0,refunded=0;};
struct ErrorRow{std::string file;std::size_t row;std::string code;};
int main(){std::ifstream input_orders("orders.csv"),input_events("events.csv");
    if(!input_orders||!input_events){std::cerr<<"입력 파일 열기 실패\n";return 1;}
    std::map<std::string,Order> orders;std::vector<ErrorRow> errors;std::string line;std::size_t row=0;
    while(std::getline(input_orders,line)){++row;summary::strip_cr(line);auto f=summary::split(line);std::string error;
        if(f.size()!=2)error="BAD_FIELD_COUNT";
        else if(f[0].empty()||f[1].empty())error="MISSING_FIELD";
        else if(orders.contains(f[0]))error="DUPLICATE_ORDER";
        else{auto amount=summary::number(f[1]);if(!amount||*amount<=0)error="BAD_AMOUNT";
            else orders.emplace(f[0],Order{*amount,0,0});}
        if(!error.empty())errors.push_back({"orders.csv",row,error});}
    if(!input_orders.eof()&&input_orders.fail()){std::cerr<<"orders.csv 읽기 실패\n";return 1;}
    std::unordered_set<std::string> applied;row=0;
    while(std::getline(input_events,line)){++row;summary::strip_cr(line);auto f=summary::split(line);std::string error;
        if(f.size()!=4)error="BAD_FIELD_COUNT";
        else if(f[0].empty()||f[1].empty()||f[2].empty()||f[3].empty())error="MISSING_FIELD";
        else if(applied.contains(f[0]))error="DUPLICATE_EVENT";
        else if(!orders.contains(f[1]))error="UNKNOWN_ORDER";
        else if(f[2]!="PAY"&&f[2]!="REFUND")error="BAD_TYPE";
        else{const auto value=summary::number(f[3]);if(!value||*value<=0)error="BAD_AMOUNT";
            else{Order& o=orders.at(f[1]);const auto net=o.paid-o.refunded;
                if(f[2]=="REFUND"){
                    if(*value>net)error="REFUND_EXCEEDS_PAY";
                    else{o.refunded+=*value;applied.insert(f[0]);}}
                else if(*value>o.amount-net)error="ORDER_EXCEEDED";
                else if(o.paid>std::numeric_limits<std::int64_t>::max()-*value)error="AMOUNT_OVERFLOW";
                else{o.paid+=*value;applied.insert(f[0]);}}}
        if(!error.empty())errors.push_back({"events.csv",row,error});}
    if(!input_events.eof()&&input_events.fail()){std::cerr<<"events.csv 읽기 실패\n";return 1;}
    std::sort(errors.begin(),errors.end(),[](const ErrorRow& a,const ErrorRow& b){return a.file!=b.file?a.file<b.file:a.row<b.row;});
    std::ostringstream settlement,rejected;std::int64_t total=0;std::size_t unsettled=0;
    for(const auto& [id,o]:orders){const auto net=o.paid-o.refunded;
        if(total>std::numeric_limits<std::int64_t>::max()-net){std::cerr<<"합계 오버플로\n";return 1;}
        total+=net;if(net<o.amount)++unsettled;
        settlement<<id<<','<<o.amount<<','<<net<<','<<o.amount-net<<'\n';}
    for(const auto& e:errors)rejected<<e.file<<','<<e.row<<','<<e.code<<'\n';
    std::string error;
    // Each file is staged separately. This is not a two-file atomic transaction.
    if(!summary::safe_write("settlement.csv",settlement.str(),error)||!summary::safe_write("rejected.csv",rejected.str(),error)){
        std::cerr<<error<<'\n';return 1;}
    std::cout<<"TOTAL_NET "<<total<<"\nUNSETTLED_ORDERS "<<unsettled<<"\nREJECTED "<<errors.size()<<'\n';}
