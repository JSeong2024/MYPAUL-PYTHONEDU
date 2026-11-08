// 배송비 계산기
#include <iostream>
int delivery_fee(int weight,int express){ (void)weight; (void)express; return -1; /* TODO */ }
int main(){int w=0,e=0;if(!(std::cin>>w>>e))return 1;/* TODO: 입력 검증 */std::cout<<delivery_fee(w,e)<<'\n';}
