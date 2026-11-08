#include <charconv>
#include <iomanip>
#include <iostream>
#include <string>
#include <string_view>
#include <system_error>
#include <vector>

int main() {
    std::string line;
    if (!std::getline(std::cin, line)) {
        std::cerr << "Error: invalid input.\n";
        return 1;
    }
    std::vector<int> numbers;
    // TODO: 쉼표로 구분한 정수 1~10개 파싱
    // TODO: 각 값은 -100~100, 빈 항목과 문자는 거부, 앞뒤 ASCII 공백은 허용
    // TODO: 정상값의 합계를 Sum: N 형식으로 출력
    std::cerr << "Error: invalid input.\n";
    return 1;
}
