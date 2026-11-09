#include <iostream>
#include <span>
[[nodiscard]] int peak(std::span<const int> values) {
    int highest = 0;
    for (const int value : values) if (value > highest) highest = value;
    return highest;
}
int main() {
    const int samples[]{3, 9, 5};
    std::cout << "Peak: " << peak(samples) << '\n';
}
