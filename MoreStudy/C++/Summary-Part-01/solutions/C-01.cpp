#include "common.hpp"
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_set>
bool email_valid(const std::string& email){
    const auto at=email.find('@');if(at==std::string::npos||at==0||at+1==email.size()||email.find('@',at+1)!=std::string::npos)return false;
    for(unsigned char c:email)if(std::isspace(c))return false;
    return true;
}
int main(){std::ifstream config("capacity.txt"),source("registrations.csv");int capacity=-1;
    if(!(config>>capacity)||capacity<0||capacity>1000||!source){std::cerr<<"입력 오류\n";return 1;}
    std::unordered_set<std::string> seen;std::ostringstream accepted,waiting,rejected;
    int a=0,w=0,r=0,row=0;std::string line;
    while(std::getline(source,line)){++row;summary::strip_cr(line);const auto f=summary::split(line);
        if(f.size()!=2||summary::trim(f[0]).empty()||summary::trim(f[1]).empty()){
            rejected<<row<<",MISSING_FIELD\n";++r;continue;}
        std::string name=summary::trim(f[0]),email=f[1];
        if(!email_valid(email)){rejected<<row<<",INVALID_EMAIL\n";++r;continue;}
        if(!seen.insert(email).second){rejected<<row<<",DUPLICATE\n";++r;continue;}
        if(a<capacity){accepted<<name<<','<<email<<'\n';++a;}
        else{waiting<<name<<','<<email<<'\n';++w;}}
    if(!source.eof()&&source.fail()){std::cerr<<"입력 오류\n";return 1;}
    std::string error;
    if(!summary::safe_write("accepted.csv",accepted.str(),error)||!summary::safe_write("waitlist.csv",waiting.str(),error)||
       !summary::safe_write("rejected.csv",rejected.str(),error)){std::cerr<<error<<'\n';return 1;}
    std::cout<<"ACCEPTED "<<a<<"\nWAITLIST "<<w<<"\nREJECTED "<<r<<'\n';}
