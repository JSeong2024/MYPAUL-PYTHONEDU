#include <iostream>

int main() {
    constexpr int timeout_ms{1'500};
    constexpr int retry_limit{3};
    constexpr int status_mask{0b0101};

    std::cout << "Timeout: " << timeout_ms << " ms\n";
    std::cout << "Retry limit: " << retry_limit << '\n';
    std::cout << "Status mask: " << status_mask << '\n';
}
