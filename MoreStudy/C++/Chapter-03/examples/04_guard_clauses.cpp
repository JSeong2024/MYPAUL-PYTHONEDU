#include <iostream>
#include <print>

int main() {
    constexpr int max_retries{3};
    const int requested_retries{2};

    if (requested_retries < 0) {
        std::cerr << "Error: retries cannot be negative.\n";
        return 1;
    }
    if (requested_retries > max_retries) {
        std::cerr << "Error: retry limit exceeded.\n";
        return 1;
    }

    std::println("Retry setting accepted: {}", requested_retries);
}
