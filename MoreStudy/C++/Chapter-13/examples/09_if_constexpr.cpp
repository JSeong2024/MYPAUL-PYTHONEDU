#include <concepts>
#include <print>
#include <string_view>

template <typename T>
void log_measurement(const T& value) {
    if constexpr (std::integral<T>) {
        std::println("Count: {}", value);
    } else if constexpr (std::floating_point<T>) {
        std::println("Measurement: {:.2f}", value);
    } else {
        std::println("Text: {}", std::string_view{value});
    }
}

int main() {
    log_measurement(7);
    log_measurement(23.456);
    log_measurement(std::string_view{"ready"});
}
