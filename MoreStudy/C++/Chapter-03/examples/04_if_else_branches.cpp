#include <iostream>

int main() {
    constexpr int distance_cm{30};

    if (distance_cm < 0 || distance_cm > 400) {
        std::cout << "INVALID\n";
    } else if (distance_cm < 30) {
        std::cout << "STOP\n";
    } else if (distance_cm <= 100) {
        std::cout << "SLOW DOWN\n";
    } else {
        std::cout << "CLEAR\n";
    }
}
