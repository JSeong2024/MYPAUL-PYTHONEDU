#include <array>
#include <print>

int main() {
    constexpr std::array readings{-1, 10, 25, 150, 30};

    for (const int reading : readings) {
        if (reading < 0) {
            continue;
        }
        if (reading > 100) {
            std::println("Threshold exceeded: {}", reading);
            break;
        }
        std::println("Accepted: {}", reading);
    }
}
