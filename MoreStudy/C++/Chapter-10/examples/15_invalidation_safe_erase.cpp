#include <iostream>
#include <vector>

int main() {
    std::vector<int> samples{10, -1, 20, -1, 30};
    for (auto it = samples.begin(); it != samples.end();) {
        if (*it < 0) {
            it = samples.erase(it);  // 삭제 후 반환된 유효한 반복자 사용
        } else {
            ++it;
        }
    }

    std::cout << "Valid:";
    for (const int value : samples) {
        std::cout << ' ' << value;
    }
    std::cout << '\n';
}
