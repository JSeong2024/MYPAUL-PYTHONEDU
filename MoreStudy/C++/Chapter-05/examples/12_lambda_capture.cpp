#include <iostream>

int main() {
    int threshold{60};
    const auto above_threshold = [threshold](int value) {
        return value > threshold;
    };

    int count{};
    for (const int value : {42, 68, 73, 49, 81}) {
        if (above_threshold(value)) {
            ++count;
        }
    }
    std::cout << "Above threshold: " << count << '\n';
}
