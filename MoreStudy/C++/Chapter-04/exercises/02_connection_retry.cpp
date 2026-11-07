#include <array>
#include <cstddef>
#include <cstddef>
#include <cstddef>
#include <print>

int main() {
    constexpr std::array responses{false, false, true, false, true};
    constexpr std::size_t max_attempts{4};

    // TODO: try at most max_attempts times.
    // Stop immediately after the first successful response.
    // Print "Connected on attempt N" or "Connection failed".
    (void)responses;
    (void)max_attempts;
    std::println("TODO: implement retry loop");
}
