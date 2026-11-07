#include <charconv>
#include <print>
#include <string_view>
#include <system_error>

int main() {
    constexpr std::string_view input{"250"};
    int port{};

    if (const auto result = std::from_chars(
            input.data(), input.data() + input.size(), port);
        result.ec == std::errc{} &&
        result.ptr == input.data() + input.size()) {
        std::println("Parsed port: {}", port);
    } else {
        std::println("Invalid port number");
        return 1;
    }
}
