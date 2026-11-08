#include <iomanip>
#include <iostream>

int main() {
    int count{};
    if (!(std::cin >> count) || count < 1 || count > 8) {
        std::cerr << "Error: count must be between 1 and 8.\n";
        return 1;
    }

    // TODO: count개의 정수를 반복해서 읽습니다.
    // TODO: 정수가 아니거나 -100~100을 벗어나면 오류 종료합니다.
    // TODO: 음수는 continue로 건너뛰고 0 이상의 값만 누적합니다.
    // TODO: 유효한 값이 없다면 오류 종료합니다.
    // TODO: "Accepted: N", "Average: X.X" 형식으로 출력합니다.
    return 0;
}
