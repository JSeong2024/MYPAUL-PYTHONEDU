#include <iostream>
#include <optional>

std::optional<double> utilization(int used, int capacity) {
    if (capacity <= 0 || used < 0 || used > capacity) {
        return std::nullopt;
    }
    return 100.0 * used / capacity;
}

int main() {
    const auto valid{utilization(30, 40)};
    if (valid.has_value()) {
        std::cout << "Utilization: " << *valid << "%\n";
    }
    if (!utilization(5, 0).has_value()) {
        std::cout << "Invalid capacity\n";
    }
}
