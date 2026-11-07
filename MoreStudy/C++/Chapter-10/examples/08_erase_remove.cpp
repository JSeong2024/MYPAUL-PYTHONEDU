#include <algorithm>
#include <print>
#include <vector>

int main() {
    std::vector<int> measurements{-1, 16, 21, -1, 19};
    const auto removed = std::erase_if(measurements, [](int value) {
        return value < 0;
    });
    std::println("Removed: {}", removed);
    for (const int value : measurements) {
        std::println("Measurement: {}", value);
    }
}
