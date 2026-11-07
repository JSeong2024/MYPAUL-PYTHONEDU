#include <iostream>
#include <string>

int main() {
    int n{}, k{};
    if (!(std::cin >> n >> k) || n < 1 || n > 10'000 || k < 1 || k > n) {
        std::cerr << "Invalid size\n";
        return 1;
    }
    // TODO: 이름과 우선순위(0~100)를 n개 입력
    // TODO: 우선순위 내림차순, 동점이면 이름 오름차순으로 k개 출력
    std::string name;
    int priority{};
    for (int i = 0; i < n; ++i) {
        if (!(std::cin >> name >> priority) || priority < 0 || priority > 100) {
            std::cerr << "Invalid task\n";
            return 1;
        }
    }
    return 0;
}
