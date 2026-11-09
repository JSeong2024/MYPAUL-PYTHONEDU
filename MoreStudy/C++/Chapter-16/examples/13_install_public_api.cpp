#include <iostream>
#include <span>
[[nodiscard]] int total(std::span<const int> readings) {
    int sum = 0;
    for (int n : readings) sum += n;
    return sum;
}
int main() {
    const int readings[]{5, 15};
    std::cout << "Public API total: " << total(readings) << '\n';
}
