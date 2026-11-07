#include <optional>
#include <print>

[[nodiscard]] std::optional<double> utilization(int used, int capacity) noexcept {
    if (capacity <= 0 || used < 0 || used > capacity) {
        return std::nullopt;
    }
    return static_cast<double>(used) / capacity;
}

int main() {
    if (const auto ratio = utilization(75, 100)) {
        std::println("Utilization: {:.1f}%", *ratio * 100.0);
    }

    if (!utilization(15, 0)) {
        std::println("Invalid capacity");
    }
}
