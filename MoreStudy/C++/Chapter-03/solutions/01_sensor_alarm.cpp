#include <charconv>
#include <iostream>
#include <print>
#include <string>
#include <system_error>

int main() {
    std::cout << "Distance (0-400 cm): " << std::flush;
    std::string line;
    if (!std::getline(std::cin, line)) {
        std::cerr << "Error: missing input.\n";
        return 1;
    }

    int distance_cm{};
    const auto parsed = std::from_chars(
        line.data(), line.data() + line.size(), distance_cm);
    if (parsed.ec != std::errc{} ||
        parsed.ptr != line.data() + line.size() ||
        distance_cm < 0 || distance_cm > 400) {
        std::cerr << "Error: invalid distance.\n";
        return 1;
    }

    if (distance_cm < 30) {
        std::println("STOP");
    } else if (distance_cm <= 100) {
        std::println("SLOW DOWN");
    } else {
        std::println("CLEAR");
    }
}
