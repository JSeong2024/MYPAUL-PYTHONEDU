#include <print>

int main() {
    constexpr double distance_cm{28.5};

    if (distance_cm < 0.0) {
        std::println("Invalid measurement");
    } else if (distance_cm < 30.0) {
        std::println("STOP");
    } else if (distance_cm <= 100.0) {
        std::println("SLOW DOWN");
    } else {
        std::println("CLEAR");
    }
}
