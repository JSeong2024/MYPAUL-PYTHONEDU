#include <concepts>
#include <print>
#include <string_view>

template <typename T>
void log_value(const T& value) {
    if constexpr (std::integral<T>) {
        std::println("Integer: {}", value);
    } else if constexpr (std::floating_point<T>) {
        std::println("Decimal: {:.2f}", value);
    } else {
        std::println("Other value");
    }
}

int main() {
    log_value(12);
    log_value(3.25);
    log_value(std::string_view{"ready"});
}
