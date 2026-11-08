// 흩어진 정산 기록의 진실
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <unordered_set>
#include <vector>
struct Order{long long amount=0,paid=0,refunded=0;};
struct Rejection{std::string filename;int row;std::string error;};
int main(){
 std::map<std::string,Order> orders;
 std::unordered_set<std::string> applied;
 std::vector<Rejection> rejected;
 // TODO 1: 주문 데이터 검증
 // TODO 2: 승인된 이벤트만 중복 집합에 추가
 // TODO 3: 정산 결과와 거부 로그를 결정론적 순서로 생성
 // TODO 4: 임시 파일 기록·교체·실패 처리, 성능 분석
 std::cout<<"TODO\n";
}
