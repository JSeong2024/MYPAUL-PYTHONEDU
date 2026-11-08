#include <iostream>

int main() {
    int n{};
    if (!(std::cin >> n) || n < 1 || n > 20) {
        std::cerr << "Error: N must be between 1 and 20.\n";
        return 1;
    }

    // TODO: while을 사용해 n부터 1까지 한 줄에 하나씩 출력합니다.
    // TODO: 반복이 끝나면 "Launch!"를 출력합니다.
    return 0;
}
