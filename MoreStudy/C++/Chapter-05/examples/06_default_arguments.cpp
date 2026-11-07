#include <format>
#include <print>
#include <string>
#include <string_view>

[[nodiscard]] std::string log_message(std::string_view message,
                                      std::string_view level = "INFO") {
    return std::format("[{}] {}", level, message);
}

int main() {
    std::println("{}", log_message("Service started"));
    std::println("{}", log_message("Connection timeout", "WARN"));
}
