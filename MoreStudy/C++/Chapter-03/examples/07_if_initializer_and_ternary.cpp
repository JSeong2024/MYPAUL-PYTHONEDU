#include <iostream>

int main() {
    constexpr int response_ms{180};
    constexpr int limit_ms{200};

    std::cout << "Response: "
              << (response_ms > limit_ms ? "SLOW" : "NORMAL") << '\n';

    if (const int retries_left{2}; retries_left > 0) {
        std::cout << "Retries available: " << retries_left << '\n';
    } else {
        std::cout << "No retries left\n";
    }
}
