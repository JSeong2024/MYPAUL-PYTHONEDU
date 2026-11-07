#include <print>
#include <vector>

int main() {
    std::vector<int> values{3, -1, 5, -2, 7};
    for (auto it = values.begin(); it != values.end();) {
        if (*it < 0) {
            it = values.erase(it);  // 반환된 새 Iterator로 갱신
        } else {
            ++it;
        }
    }
    for (const int value : values) {
        std::println("Valid: {}", value);
    }
}
