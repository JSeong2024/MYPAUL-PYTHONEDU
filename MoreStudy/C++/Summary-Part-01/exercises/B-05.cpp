// 도서 대출 상태 관리
#include <iostream>
#include <string>
class LibraryBook{
public:
 LibraryBook(std::string title,int total):title_(title),total_(total),available_(total){}
 bool borrow(){return false;/* TODO */}
 bool give_back(){return false;/* TODO */}
 int available()const{return available_;}
private:std::string title_;int total_,available_;
};
int main(){/* TODO: BORROW/RETURN 명령 처리 */std::cout<<"TODO\n";}
