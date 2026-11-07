#include <iostream>
#include <print>
#include <string>

int main() {
    // 입력 예: 20,25,19,21
    // 쉼표로 분리된 정수 1~100개, 각 값은 -100~100 범위
    // 필드 앞뒤 ASCII 공백은 허용하지만 빈 필드와 잘못된 숫자는 거부
    std::string line;
    if (!std::getline(std::cin, line)) {
        std::println(stderr, "Invalid input");
        return 1;
    }

    // TODO: ',' 기준으로 분할하고 std::from_chars로 엄격하게 정수로 변환함.
    // TODO: 개수, 평균, 최댓값을 출력함.
    // 출력: Samples / Average(소수 둘째 자리) / Peak
    std::println("TODO: implement measurement parser");
}
