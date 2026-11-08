#include <iostream>

int main() {
    int n{};
    if (!(std::cin >> n) || n < 1 || n > 100) {
        std::cerr << "Error: N must be between 1 and 100.\n";
        return 1;
    }

    // TODO: for 반복문으로 1부터 n까지 합계를 구합니다.
    // TODO: "Sum: 합계" 형식으로 출력합니다.
    return 0;
}
