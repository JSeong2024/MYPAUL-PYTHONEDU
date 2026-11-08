#include <iostream>

int main() {
    int rows{};
    int columns{};
    if (!(std::cin >> rows >> columns) ||
        rows < 1 || rows > 8 || columns < 1 || columns > 8) {
        std::cerr << "Error: rows and columns must be between 1 and 8.\n";
        return 1;
    }

    // TODO: 중첩 for 반복문으로 rows × columns 격자를 출력합니다.
    // TODO: (행+열)이 짝수이면 '#', 홀수이면 '.'을 출력합니다.
    // TODO: 행을 출력한 뒤 줄바꿈을 추가합니다.
    return 0;
}
