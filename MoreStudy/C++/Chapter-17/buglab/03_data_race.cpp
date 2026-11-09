// 결함 재현 전용. ThreadSanitizer 도구로만 실행 권장.
#include <iostream>
#include <thread>
int main(){
 int shared=0;
 std::thread a{[&]{for(int i=0;i<1000;++i)++shared;}};
 std::thread b{[&]{for(int i=0;i<1000;++i)++shared;}};
 a.join();b.join();
 std::cout<<shared<<'\n'; // 값의 정상 출력 여부는 안전성의 증거가 아님
}
