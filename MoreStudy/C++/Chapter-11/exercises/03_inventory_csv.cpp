#include <fstream>
#include <map>
#include <print>
#include <string>

// Header: id,quantity. id: 영숫자·_·-, 길이 1~32.
// quantity: 0~1000000. 중복 id와 잘못된 CSV는 오류.
// id를 오름차순으로 출력하고 총수량을 출력.
int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    std::ifstream input{argv[1]};
    if (!input) return 1;
    std::map<std::string, int> inventory;
    // TODO: 헤더 및 데이터 파싱/검증
    // TODO: 중복 검사, 정렬 출력 및 Total 계산
    std::println("TODO");
}
