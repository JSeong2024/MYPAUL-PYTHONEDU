#include <charconv>
#include <iostream>
#include <print>
#include <string>
#include <system_error>

int main() {
    constexpr int max_attempts{3};

    for (int attempt{1}; attempt <= max_attempts; ++attempt) {
        std::cout << "Port (1-65535): " << std::flush;
        std::string line;
        if (!std::getline(std::cin, line)) {
            std::cerr << "Error: input stream closed.\n";
            return 1;
        }

        int port{};
        const auto result = std::from_chars(
            line.data(), line.data() + line.size(), port);
        const bool valid = result.ec == std::errc{} &&
                           result.ptr == line.data() + line.size() &&
                           port >= 1 && port <= 65'535;

        if (valid) {
            std::println("Selected port: {}", port);
            return 0;
        }

        std::println("Invalid port ({}/{})", attempt, max_attempts);
    }

    std::cerr << "Error: retry limit exceeded.\n";
    return 1;
}
