#include <iostream>

int main() {
    int threshold{};
    if (!(std::cin >> threshold)) {
        std::cerr << "Error: invalid threshold.\n";
        return 1;
    }

    // TODO: threshold를 값으로 캡처하고, value > threshold를 반환하는 람다를 정의합니다.
    const auto is_high = [threshold](int value) {
        // TODO
        (void)value;
        return threshold < 0;
    };

    int high_count{};
    for (int index{}; index < 5; ++index) {
        int value{};
        if (!(std::cin >> value)) {
            std::cerr << "Error: invalid reading.\n";
            return 1;
        }
        if (is_high(value)) {
            ++high_count;
        }
    }
    std::cout << "High readings: " << high_count << '\n';
}
