// 결함 재현 전용. UBSan을 켜고 실행한다.
#include <climits>
#include <iostream>
int main(){volatile int value=INT_MAX;std::cout<<(value+1)<<'\n';}
