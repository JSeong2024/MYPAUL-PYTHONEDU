#include <format>
#include <print>
#include <string>

[[nodiscard]] std::string describe_reading(int count) {
    return std::format("{} counts", count);
}

[[nodiscard]] std::string describe_reading(double temperature) {
    return std::format("{:.2f} C", temperature);
}

int main() {
    std::println("{}", describe_reading(120));
    std::println("{}", describe_reading(23.5));
}
